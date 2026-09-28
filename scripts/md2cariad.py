#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md2cariad.py — 确定性 Markdown → CARIAD 风格 HTML 转换器
TRA-1 车云安全技术方案调研 · 唯一允许的 HTML 生成路径

用法:
    python3 scripts/md2cariad.py docs/<file>.md docs/html/<file>.html
    python3 scripts/md2cariad.py --all               # 转换 docs/ 下全部 md（排除 sources/）
    python3 scripts/md2cariad.py --verify docs/html/<file>.html   # 结构断言

设计约束（见 docs/00-engagement-plan.md §6.2）:
  * 只依赖 Python 标准库，完全确定性：同一输入 → 逐字节相同输出。
  * 内容是 Markdown；HTML 是派生物。禁止手写 HTML。
  * 不联网、不取远程字体、不执行 JS 之外的任何外部资源（无 CDN 依赖）。
"""

import html
import os
import re
import sys
import glob

# ----------------------------------------------------------------------------
# CARIAD 设计令牌（来源：CARIAD PPT Master v1.6 / cariad-frontend-design 技能）
# ----------------------------------------------------------------------------
CARIAD_CSS = """
:root{
  --c-primary-dark:#1D0638;   /* Midnight */
  --c-secondary-dark:#373741; /* Night Grey */
  --c-secondary-light:#CDCDD2;/* Day Grey */
  --c-accent-blue:#442EE0;    /* Twilight */
  --c-accent-green:#1EEF97;   /* Future Green */
  --c-accent-yellow:#FEF04A;  /* Sunlight */
  --c-accent-red:#EE4C40;     /* Sun Red */
  --c-surface:#FFFFFF;
  --c-surface-alt:#F5F5F8;
  --c-body:#2A2A33;
  --font:"FK CARIAD Light",Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",
         "Noto Sans SC","Source Han Sans SC","PingFang SC","Microsoft YaHei",sans-serif;
  --mono:ui-monospace,SFMono-Regular,"JetBrains Mono",Menlo,Consolas,"Courier New",monospace;
  --sp-xs:4px; --sp-sm:8px; --sp-md:16px; --sp-lg:24px; --sp-xl:32px; --sp-2xl:48px; --sp-3xl:64px;
  --r-sm:4px; --r-md:8px; --r-lg:16px;
  --shadow-sm:0 1px 2px rgba(29,6,56,.05);
  --shadow-md:0 4px 6px rgba(29,6,56,.10);
  --shadow-lg:0 10px 15px rgba(29,6,56,.15);
}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0;background:var(--c-surface);color:var(--c-body);
  font-family:var(--font);font-size:16px;font-weight:400;line-height:1.75;
  text-rendering:optimizeLegibility;
}
.skip{position:absolute;left:-9999px}
.wrap{max-width:1280px;margin:0 auto;padding:0 var(--sp-lg)}

/* ---------- Hero / 头部 ---------- */
.hero{background:var(--c-primary-dark);color:#fff;padding:var(--sp-3xl) 0 var(--sp-2xl);position:relative;overflow:hidden}
.hero::after{content:"";position:absolute;right:-120px;top:-120px;width:420px;height:420px;
  border-radius:50%;background:radial-gradient(circle at 30% 30%,rgba(68,46,224,.85),rgba(30,239,151,.15) 60%,transparent 70%);opacity:.55}
.hero .brand{display:flex;align-items:center;gap:var(--sp-md);font-size:14px;letter-spacing:.18em;text-transform:uppercase;color:var(--c-accent-green)}
.hero .brand .dot{width:10px;height:10px;border-radius:50%;background:var(--c-accent-green);box-shadow:0 0 12px var(--c-accent-green)}
.hero h1{font-size:36px;font-weight:300;line-height:1.25;margin:var(--sp-lg) 0 var(--sp-md);color:#fff;max-width:22em}
.hero .sub{font-size:14px;color:var(--c-secondary-light);margin:0;max-width:60em}
.hero .rule{height:2px;width:96px;background:var(--c-accent-blue);margin:var(--sp-lg) 0 var(--sp-md);border:0}

/* ---------- Meta 卡 ---------- */
.meta-card{background:#fff;border:1px solid var(--c-secondary-light);border-left:4px solid var(--c-accent-blue);
  border-radius:var(--r-md);box-shadow:var(--shadow-sm);padding:var(--sp-md) var(--sp-lg);margin:calc(-1 * var(--sp-xl)) 0 var(--sp-xl)}
.meta-card dl{display:grid;grid-template-columns:auto 1fr;gap:var(--sp-xs) var(--sp-lg);margin:0}
.meta-card dt{font-size:14px;color:var(--c-secondary-dark);font-weight:400;white-space:nowrap}
.meta-card dd{margin:0;font-size:14px;color:var(--c-primary-dark)}

/* ---------- 布局 ---------- */
.layout{display:grid;grid-template-columns:290px minmax(0,1fr);gap:var(--sp-2xl);align-items:start;padding-bottom:var(--sp-3xl)}
.toc{position:sticky;top:var(--sp-lg);max-height:calc(100vh - 48px);overflow:auto;
  border:1px solid var(--c-secondary-light);border-radius:var(--r-md);background:var(--c-surface-alt);padding:var(--sp-md)}
.toc h2{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--c-secondary-dark);margin:0 0 var(--sp-md);font-weight:400}
.toc ol{list-style:none;margin:0;padding:0;counter-reset:tocsec}
.toc li{margin:0 0 var(--sp-xs)}
.toc a{display:block;font-size:13px;line-height:1.5;color:var(--c-secondary-dark);text-decoration:none;
  padding:5px var(--sp-sm);border-radius:var(--r-sm);border-left:2px solid transparent}
.toc a:hover{background:#fff;color:var(--c-accent-blue);border-left-color:var(--c-accent-blue)}
.toc .lvl3 a{padding-left:22px;font-size:12px;color:#5b5b68}

/* ---------- 章节 ---------- */
.rep-section{margin:0 0 var(--sp-3xl);scroll-margin-top:var(--sp-lg)}
.sec-head{display:flex;align-items:baseline;gap:var(--sp-md);border-top:2px solid var(--c-primary-dark);padding-top:var(--sp-md);margin-bottom:var(--sp-lg)}
.sec-badge{flex:0 0 auto;font-family:var(--mono);font-size:12px;letter-spacing:.08em;color:#fff;
  background:var(--c-primary-dark);border-radius:9999px;padding:4px 12px}
.rep-section:nth-of-type(3n+2) .sec-badge{background:var(--c-accent-blue)}
.rep-section:nth-of-type(3n+3) .sec-badge{background:var(--c-secondary-dark)}
h1,h2,h3,h4{color:var(--c-primary-dark);font-weight:300;letter-spacing:-.005em}
h2{font-size:28px;line-height:1.3;margin:0}
h3{font-size:20px;font-weight:400;margin:var(--sp-xl) 0 var(--sp-md);padding-left:var(--sp-md);border-left:3px solid var(--c-accent-green)}
h4{font-size:16px;font-weight:400;margin:var(--sp-lg) 0 var(--sp-sm);color:var(--c-accent-blue)}
p{margin:0 0 var(--sp-md)}
strong{font-weight:600;color:var(--c-primary-dark)}
em{font-style:italic;color:var(--c-secondary-dark)}
a{color:var(--c-accent-blue);text-decoration:none;border-bottom:1px solid rgba(68,46,224,.35);word-break:break-word}
a:hover{border-bottom-color:var(--c-accent-blue)}
hr{border:0;border-top:1px solid var(--c-secondary-light);margin:var(--sp-2xl) 0}
ul,ol{margin:0 0 var(--sp-md);padding-left:1.5em}
li{margin:var(--sp-xs) 0}
li>ul,li>ol{margin-top:var(--sp-xs)}
code{font-family:var(--mono);font-size:.875em;background:var(--c-surface-alt);
  border:1px solid var(--c-secondary-light);border-radius:var(--r-sm);padding:1px 5px;color:#2b1a52;word-break:break-word}
pre{background:var(--c-primary-dark);color:#EDEBF5;border-radius:var(--r-md);padding:var(--sp-md) var(--sp-lg);
  overflow-x:auto;box-shadow:var(--shadow-md);margin:0 0 var(--sp-lg)}
pre code{background:none;border:0;padding:0;color:inherit;font-size:13px;line-height:1.6;white-space:pre}
blockquote{margin:0 0 var(--sp-lg);padding:var(--sp-md) var(--sp-lg);background:var(--c-surface-alt);
  border-left:4px solid var(--c-accent-yellow);border-radius:0 var(--r-md) var(--r-md) 0;color:#4a4a55}
blockquote p:last-child{margin-bottom:0}

/* ---------- 表格 ---------- */
.table-wrap{overflow-x:auto;margin:0 0 var(--sp-lg);border:1px solid var(--c-secondary-light);border-radius:var(--r-md);box-shadow:var(--shadow-sm)}
table{border-collapse:collapse;width:100%;font-size:14px;background:#fff}
thead th{background:var(--c-primary-dark);color:#fff;text-align:left;font-weight:400;letter-spacing:.02em;
  padding:10px var(--sp-md);border-right:1px solid rgba(255,255,255,.12);white-space:nowrap}
thead th:last-child{border-right:0}
tbody td{padding:9px var(--sp-md);border-top:1px solid var(--c-secondary-light);vertical-align:top;line-height:1.65}
tbody tr:nth-child(even){background:var(--c-surface-alt)}
tbody td:first-child{color:var(--c-primary-dark)}

/* ---------- 脚注 / 页脚 ---------- */
.doc-footer{background:var(--c-secondary-dark);color:#fff;padding:var(--sp-2xl) 0;font-size:13px}
.doc-footer .wrap{display:flex;flex-wrap:wrap;gap:var(--sp-lg);justify-content:space-between}
.doc-footer strong{color:var(--c-accent-green);font-weight:400}

/* ---------- 响应式 ---------- */
@media (max-width:1024px){
  .layout{grid-template-columns:1fr;gap:var(--sp-xl)}
  .toc{position:static;max-height:none}
  .hero h1{font-size:28px}
  h2{font-size:24px}
}
@media print{
  .toc{display:none}.layout{grid-template-columns:1fr}
  .hero::after{display:none}pre{background:#f2f2f5;color:#111}
  a{color:#111;border:0}
}
"""

HTML_SHELL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · TRA-1 车云安全技术方案调研</title>
<meta name="generator" content="md2cariad.py (deterministic)">
<meta name="description" content="{desc}">
<style>{css}</style>
</head>
<body>
<a class="skip" href="#main">跳到正文</a>
<header class="hero">
  <div class="wrap">
    <div class="brand"><span class="dot"></span><span>TRAIL OF BITS SECURITY</span><span>·</span><span>CARIAD STYLE REPORT</span></div>
    <h1>{title}</h1>
    <hr class="rule">
    <p class="sub">{subtitle}</p>
  </div>
</header>
<div class="wrap">
  {meta}
</div>
<div class="wrap layout">
  <nav class="toc" aria-label="目录">
    <h2>目录 / CONTENTS</h2>
    {toc}
  </nav>
  <main id="main">
{body}
  </main>
</div>
<footer class="doc-footer">
  <div class="wrap">
    <div><strong>TRA-1 车云安全技术方案调研</strong> · 授权与访问控制专题</div>
    <div>本页为 Markdown 内容源的确定性派生件 · 生成器 md2cariad.py</div>
    <div>正文 {chars} 字符</div>
  </div>
</footer>
</body>
</html>
"""


# ----------------------------------------------------------------------------
# 行内解析
# ----------------------------------------------------------------------------
def _slug(i):
    return "sec-%d" % i


def inline(text):
    """行内 Markdown → HTML（确定性）。"""
    text = html.escape(text, quote=False)

    codes = []

    def stash_code(m):
        codes.append(m.group(1))
        return "\x00C%d\x00" % (len(codes) - 1)

    text = re.sub(r"`([^`]+)`", stash_code, text)

    links = []

    def stash_link(m):
        links.append((m.group(1), m.group(2)))
        return "\x00L%d\x00" % (len(links) - 1)

    text = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+|mailto:[^)\s]+)\)", stash_link, text)

    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\*\w])\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"~~([^~]+)~~", r"<del>\1</del>", text)

    def bare_url(m):
        return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (m.group(1), m.group(1))

    text = re.sub(r"(?<![\"'>=/\w])(https?://[^\s<)\x00]+)", bare_url, text)

    for i, (label, url) in enumerate(links):
        text = text.replace(
            "\x00L%d\x00" % i,
            '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, label),
        )
    for i, c in enumerate(codes):
        text = text.replace("\x00C%d\x00" % i, "<code>%s</code>" % c)
    return text


# ----------------------------------------------------------------------------
# 块级解析
# ----------------------------------------------------------------------------
RE_H = re.compile(r"^(#{1,6})\s+(.*)$")
RE_UL = re.compile(r"^(\s*)([-*+])\s+(.*)$")
RE_OL = re.compile(r"^(\s*)(\d+)[.)]\s+(.*)$")
RE_TBL_SEP = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$")
RE_META = re.compile(r"^\*\*(.+?)\*\*\s*[：:]\s*(.*)$")


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


class Converter:
    def __init__(self, source):
        self.lines = source.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        self.title = ""
        self.meta = []
        self.sections = []  # [(level, text, anchor, [blocks...])]
        self._anchors = {}
        self._n = 0

    # -- 工具 --
    def anchor(self, text):
        n = self._n
        self._n += 1
        return _slug(n)

    # -- 主流程 --
    def parse(self):
        lines = self.lines
        i = 0
        # 标题
        while i < len(lines):
            if lines[i].strip():
                m = RE_H.match(lines[i])
                if m and len(m.group(1)) == 1:
                    self.title = m.group(2).strip()
                    i += 1
                break
            i += 1
        # 头部元信息
        j = i
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines) and RE_META.match(lines[j].strip()):
            while j < len(lines):
                raw = lines[j].strip()
                m = RE_META.match(raw)
                if m:
                    self.meta.append((m.group(1), m.group(2)))
                    j += 1
                elif not raw:
                    if j + 1 < len(lines) and RE_META.match(lines[j + 1].strip()):
                        j += 1
                    else:
                        break
                else:
                    break
            i = j
        # 正文按 H2/H3 分节
        cur = None
        buf = []

        def flush(buf, target):
            for b in self.blocks(buf):
                target.append(b)

        body = []
        depth = 2
        for line in lines[i:]:
            m = RE_H.match(line)
            if m and len(m.group(1)) == 2:
                flush(buf, body if cur is None else cur[3])
                buf = []
                anchor = self.anchor(m.group(2))
                cur = (2, m.group(2).strip(), anchor, [])
                self.sections.append(cur)
                depth = 2
                continue
            if m and len(m.group(1)) == 3:
                flush(buf, body if cur is None else cur[3])
                buf = []
                target = cur[3] if cur else body
                anchor = self.anchor(m.group(2))
                target.append(("h", 3, m.group(2).strip(), anchor))
                if not cur:
                    self.sections.append((3, m.group(2).strip(), anchor, target))
                continue
            if m and len(m.group(1)) >= 4 and cur:
                flush(buf, cur[3])
                buf = []
                cur[3].append(("h", 4, m.group(2).strip(), None))
                continue
            buf.append(line)
        flush(buf, body if cur is None else cur[3])
        self.prefix_blocks = body
        return self

    def blocks(self, lines):
        out = []
        i = 0
        n = len(lines)
        while i < n:
            line = lines[i]
            s = line.strip()
            if not s:
                i += 1
                continue
            # 代码块
            if s.startswith("```"):
                lang = s[3:].strip()
                i += 1
                code = []
                while i < n and not lines[i].strip().startswith("```"):
                    code.append(lines[i])
                    i += 1
                i += 1
                cls = ' class="language-%s"' % lang if lang else ""
                out.append(("code", "<pre><code%s>%s</code></pre>" % (cls, html.escape("\n".join(code)))))
                continue
            # 表格
            if s.startswith("|") and i + 1 < n and RE_TBL_SEP.match(lines[i + 1]):
                head = split_row(s)
                i += 2
                rows = []
                while i < n and lines[i].strip().startswith("|"):
                    rows.append(split_row(lines[i]))
                    i += 1
                th = "".join("<th>%s</th>" % inline(c) for c in head)
                trs = []
                for r in rows:
                    tds = "".join("<td>%s</td>" % inline(c) for c in r)
                    trs.append("<tr>%s</tr>" % tds)
                out.append(("table", '<div class="table-wrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (th, "".join(trs))))
                continue
            # 引用
            if s.startswith(">"):
                q = []
                while i < n and lines[i].strip().startswith(">"):
                    q.append(re.sub(r"^\s*>\s?", "", lines[i]))
                    i += 1
                inner = self.blocks(q)
                out.append(("quote", "<blockquote>%s</blockquote>" % "".join(b[1] for b in inner)))
                continue
            # 分隔线
            if re.match(r"^(-{3,}|\*{3,}|_{3,})$", s):
                out.append(("hr", "<hr>"))
                i += 1
                continue
            # 列表
            if RE_UL.match(line) or RE_OL.match(line):
                lst, i = self.list_(lines, i)
                out.append(("ul", lst))
                continue
            # 段落
            para = [line]
            i += 1
            while i < n:
                nxt = lines[i]
                ns = nxt.strip()
                if not ns:
                    break
                if RE_H.match(nxt) or RE_UL.match(nxt) or RE_OL.match(nxt) or ns.startswith("```") or ns.startswith(">") or ns.startswith("|"):
                    break
                if re.match(r"^(-{3,}|\*{3,}|_{3,})$", ns):
                    break
                para.append(nxt)
                i += 1
            out.append(("p", "<p>%s</p>" % inline(" ".join(x.strip() for x in para))))
        return out

    def list_(self, lines, i):
        """解析（可嵌套的）列表，返回 (html, next_i)。"""
        n = len(lines)
        items = []  # (indent, ordered, text, [children])
        stack = []
        while i < n:
            line = lines[i]
            if not line.strip():
                # 允许列表项之间空行（松列表）
                if i + 1 < n and (RE_UL.match(lines[i + 1]) or RE_OL.match(lines[i + 1])):
                    i += 1
                    continue
                break
            mu = RE_UL.match(line)
            mo = RE_OL.match(line)
            if not (mu or mo):
                # 列表项续行
                if items and line.startswith((" ", "\t")):
                    items[-1][2] += " " + line.strip()
                    i += 1
                    continue
                break
            ind = len((mu or mo).group(1).replace("\t", "    "))
            ordered = bool(mo)
            text = (mu or mo).group(3).strip()
            node = [ind, ordered, text, []]
            items.append(node)
            i += 1
        # 构建层级
        root = []
        for node in items:
            ind = node[0]
            while stack and stack[-1][0] >= ind:
                stack.pop()
            if stack:
                stack[-1][3].append(node)
            else:
                root.append(node)
            stack.append(node)

        def render(nodes, ordered):
            tag = "ol" if ordered else "ul"
            parts = []
            for nd in nodes:
                inner = inline(nd[2])
                if nd[3]:
                    inner += render(nd[3], nd[3][0][1])
                parts.append("<li>%s</li>" % inner)
            return "<%s>%s</%s>" % (tag, "".join(parts), tag)

        return render(root, root[0][1] if root else False), i

    # -- 渲染 --
    def render(self):
        # 目录
        toc = ['<ol>']
        for lvl, text, anchor, _ in self.sections:
            if lvl == 2:
                toc.append('<li class="lvl2"><a href="#%s">%s</a></li>' % (anchor, inline(text)))
            else:
                toc.append('<li class="lvl3"><a href="#%s">%s</a></li>' % (anchor, inline(text)))
        toc.append("</ol>")

        body = []
        for b in self.prefix_blocks:
            body.append(b[1])
        badge = 0
        for lvl, text, anchor, blocks in self.sections:
            if lvl != 2:
                continue
            badge += 1
            inner = []
            for b in blocks:
                if b[0] == "h":
                    lvl2, t2, a2 = b[1], b[2], b[3]
                    if lvl2 == 3:
                        inner.append('<h3 id="%s">%s</h3>' % (a2, inline(t2)))
                    else:
                        inner.append("<h4>%s</h4>" % inline(t2))
                else:
                    inner.append(b[1])
            body.append(
                '<section class="rep-section" id="%s">\n'
                '  <div class="sec-head"><span class="sec-badge">%02d</span><h2>%s</h2></div>\n'
                "%s\n</section>" % (anchor, badge, inline(text), "\n".join(inner))
            )

        meta_html = ""
        if self.meta:
            rows = "".join("<dt>%s</dt><dd>%s</dd>" % (inline(k), inline(v)) for k, v in self.meta)
            meta_html = '<section class="meta-card"><dl>%s</dl></section>' % rows
        return body, toc, meta_html

    def to_html(self):
        body, toc, meta_html = self.render()
        title = self.title or "车云安全技术方案调研"
        subtitle = "Trail of Bits Security · 授权与访问控制专题 · 公开信息调研（区分公开信息与合理推测，逐条标注证据等级）"
        chars = len("\n".join(self.lines))
        return HTML_SHELL.format(
            title=html.escape(title),
            desc=html.escape(title + " — CARIAD 风格技术调研报告"),
            css=CARIAD_CSS,
            subtitle=subtitle,
            meta=meta_html,
            toc="\n".join(toc),
            body="\n".join(body),
            chars="{:,}".format(chars),
        )


# ----------------------------------------------------------------------------
# 结构断言（G7）
# ----------------------------------------------------------------------------
def verify(path):
    src = open(path, encoding="utf-8").read()
    ok = True

    def chk(name, cond, extra=""):
        nonlocal ok
        ok = ok and cond
        print("  [%s] %s %s" % ("PASS" if cond else "FAIL", name, extra))

    print("校验:", path, "(%d 字节)" % len(src.encode("utf-8")))
    chk("html/head/body 齐备", all(t in src for t in ("<!DOCTYPE html>", "</head>", "</body>", "</html>")))
    chk("<section>/</section> 配对", src.count("<section") == src.count("</section>"),
        "%d/%d" % (src.count("<section"), src.count("</section>")))
    chk("<div>/</div> 配对", src.count("<div") == src.count("</div>"),
        "%d/%d" % (src.count("<div"), src.count("</div>")))
    chk("<table>/</table> 配对", src.count("<table>") == src.count("</table>"))
    chk("<pre>/</pre> 配对", src.count("<pre>") == src.count("</pre>"))
    chk("<ul>/<ol> 与 </ul>/</ol> 配对",
        src.count("<ul>") == src.count("</ul>") and src.count("<ol>") == src.count("</ol>"))
    chk("无未替换占位符", "\x00" not in src and "{title}" not in src and "{body}" not in src)
    chk("含 CARIAD 主色令牌", "--c-primary-dark:#1D0638" in src and "--c-accent-blue:#442EE0" in src)
    chk("无外部资源依赖", "http" not in src.split("</head>")[0].replace('lang="zh-CN"', "").replace("http-equiv", ""))
    chk("章节数 >= 1", src.count('class="rep-section"') >= 1, "sections=%d" % src.count('class="rep-section"'))
    print("=> %s\n" % ("全部通过" if ok else "存在问题"))
    return ok


def char_report(md_path):
    txt = open(md_path, encoding="utf-8").read()
    print("%-46s %8d 字符  %9d 字节" % (os.path.basename(md_path), len(txt), len(txt.encode("utf-8"))))


def main(argv):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if len(argv) >= 2 and argv[1] == "--all":
        mds = [p for p in sorted(glob.glob(os.path.join(root, "docs", "*.md")))]
        for md in mds:
            out = os.path.join(root, "docs", "html", os.path.basename(md)[:-3] + ".html")
            os.makedirs(os.path.dirname(out), exist_ok=True)
            src = open(md, encoding="utf-8").read()
            open(out, "w", encoding="utf-8").write(Converter(src).parse().to_html())
            print("生成", os.path.relpath(out, root))
        for md in mds:
            char_report(md)
        tot = sum(len(open(md, encoding="utf-8").read()) for md in mds)
        print("\n合计 %d 字符" % tot)
        return 0
    if len(argv) >= 3 and argv[1] == "--verify":
        return 0 if verify(argv[2]) else 1
    if len(argv) >= 3:
        src = open(argv[1], encoding="utf-8").read()
        os.makedirs(os.path.dirname(os.path.abspath(argv[2])), exist_ok=True)
        html_doc = Converter(src).parse().to_html()
        open(argv[2], "w", encoding="utf-8").write(html_doc)
        print("生成 %s（正文 %d 字符 → HTML %d 字节）" % (argv[2], len(src), len(html_doc.encode("utf-8"))))
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
