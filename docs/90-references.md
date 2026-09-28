# 参考资料与证据台账

> 本章是 TRA-1《车云安全技术方案调研》的**参考资料来源台账（Reference & Evidence Ledger）**。它不是一篇论述性章节，而是一份**可核验清单**：报告正文中出现的每一条带证据等级的断言，都应能在本章中找到对应的来源条目，用于回答验收标准 AC-7「信源可靠、逐条标注参考资料」。
>
> 维护原则（与信源档案 `docs/sources/source-dossier.md` 保持一致）：
> - 本章**不新增任何 dossier 中不存在的 URL**。凡本章出现的 URL，均逐字取自 source-dossier.md；凡 dossier 标记为不完整或不可核验的 URL，本章**如实照录其不完整状态**，绝不"修复"、绝不补全、绝不推测。
> - 本章**不把 `[未验证]` 写成已验证**，也不把「未找到公开来源」反向表述为能力缺失。
> - 新增来源时，先就地追加到 source-dossier.md，再同步到本章；本章只做「台账化转写」，不承担收集职能。

---

## 90.0 使用说明

### 90.0.1 本章定位

本报告的工作流把「事实」与「来源」做了分离：事实底座集中在 `docs/sources/source-dossier.md`（唯一事实底座），本章则把该底座中散落的条目**重新组织为可逐条引用的台账**。这样做的目的有三：

1. **可核验性**：审阅者拿到报告正文的任一断言，可在本章按编号回溯到原始 URL 与证据等级。
2. **可追溯的边界**：本章显式列出未能取证、区域封锁、工具受限的全部条目，使"报告没写到"与"世界上不存在"这两件事被清晰地区分开。
3. **引用纪律的执行载体**：本章 90.11 定义正文的标注约定，90.10 定义红线清单，两者共同约束正文不得引用任何未取证内容。

### 90.0.2 证据分级定义（逐字照搬 00-engagement-plan.md §3.1 六级）

本委托的统一口径为六级，任何一条事实必须携带其中一个等级：

| 等级 | 定义 | 允许的表述措辞 |
|---|---|---|
| **[A] 一手** | 标准正文（openstd.samr.gov.cn / RFC Editor / 官方规范库）、OEM 官方开发者文档、官方白皮书、官方漏洞政策、官方年报 | \"**文档明载**…\" |
| **[B] 权威第三方** | 学术论文、检测认证机构、权威媒体、官方 SDK 仓库、行业联盟规范页 | \"**据 …（第三方）**…\" |
| **[C] 二手** | 自媒体、博客、论坛、聚合站 | \"**有报道称**…（未经一手核实）\" |
| **[未验证]** | 站点可达性已确认但正文未取到 | \"**尚未取证**，URL 结构待复核\" |
| **[合理推测]** | 由已知架构/规范推导 | \"**本报告判断**…（推测，非事实）\" |
| **未找到公开来源** | 已检索指定对象无果 | \"该方向**未找到公开来源**，不等同于能力缺失\" |

**阅读本章时请注意**：`[A]` 并不等于"本条事实被本报告独立复现"，而是"该来源属官方一手页面且本次直接取到"；`[B]`/`[C]` 的区分在于来源的权威性与一手程度；`[未验证]` 是**明确不可作为事实断言使用**的等级，只能用于"提示该项目仍需复核"的语境。

### 90.0.3 本章的编号与字段约定

- 台账条目编号采用 `R-<段>-<序>` 形式（如 `R-2.1-03`），便于正文脚注精确指向。
- 中国法规与标准条目统一携带字段：**编号 / 名称 / 状态 / 发布-实施日期 / URL / 证据等级 / 备注**。
- 国际标准、RFC、规范、厂商条目统一携带字段：**标识 / 标题 / 年份或版本 / URL / 用途一句话 / 证据等级**。
- 厂商一手证据条目统一携带字段：**主体 / 入口 URL / 证据等级 / 取证结果一句话**。
- 凡 dossier 注明「未取得可核验 URL」「无 DNS」「HTTP 403/000」「区域封锁」者，本章照录其结果，并在 90.10 集中复述。

### 90.0.4 采集日期与采集方式

- **采集日期**：2026-09-28（全部条目同批采集，未做跨日增量）。
- **执行方式**：`terminal + curl` 与 `browser_navigate / browser_console` 直连权威站点取证（见 source-dossier §0）。
- **采集结果的一般形态**：由于检索工具额度耗尽，本次为"直取已知权威 URL"模式，而非开放网络发现；因此本章条目的**覆盖面受已知 URL 集合限制**，不代表公开可用信源的全集。
- **等级标注时点**：证据等级标注于 2026-09-28 的取证状态；站点可达性可能随时间变化，引用前如需严格核验应重跑可达性检查。

---

## 90.1 采集方法与工具局限声明

本节逐字落实 source-dossier §0 的采集方法与局限要求。**凡引用本报告任何结论，都必须连同本节声明的局限一并理解**，否则会系统性地高估报告覆盖度。

### 90.1.1 检索工具不可用

- `web_search` / `web_extract` 全程返回 `Insufficient credits`（Firecrawl 402/429），额度耗尽且不自动恢复。因此本次调研**无法做开放网络发现**，只能"直取已知权威 URL"。
- **含义**：本报告无法回答"是否存在某个更好的公开来源"，只能说"在已知的权威 URL 集合内取到了什么"。凡是需要"全网检索才能发现的一手材料"，本次均可能漏检 —— 这是覆盖度风险，而非事实风险。

### 90.1.2 公开搜索引擎在本运行环境同样不可用

- Bing 被地理重定向至 cn.bing.com 且对中文品牌词返回噪声结果；
- Baidu / Sogou / 360 触发验证码；
- Google 返回 `/sorry` 机器人墙或空结果；
- DuckDuckGo 验证码。
- **含义**：国内车企的品牌词、产品页、"车云安全/开放平台"等入口无法通过搜索引擎定位；本章对国内车企的条目密度因此显著低于其真实公开信息的可能规模。

### 90.1.3 区域/网络封锁清单

以下站点在本次网络出口下**被区域封锁或拦截**，其正文未能取到：

- `bmw.com` / `bmwgroup.com` / `rivian.com` —— 被 Akamai / CloudFront 区域封锁（HTTP 000 / 403）；
- `unece.org`、`iso.org`、`autosar.org`、`trustedcomputinggroup.org` —— 被 Cloudflare 或超时拦截；
- `open.xiaopeng.com` —— 对所有请求返回 403（openresty）。
- **含义**：上述对象的条目在 90.10 中集中列出，且一律标注 `[未验证]` 或「未找到公开来源」。**不得**因其封锁而推断其不设相应能力。

### 90.1.4 覆盖度偏置声明（本条为中立性红线，务必随结论一并引用）

证据密度向"文档公开可达"的企业倾斜：

- **证据最厚**：Tesla、Mercedes-Benz（公开开发者文档最完整）。
- **证据薄弱或空缺**：BMW、Rivian、小鹏、极氪、零跑、理想、华为、奇瑞。

**关键声明**：「未找到公开来源」= **本次披露缺口**，**绝不等于**能力缺口，**不得**反向推断为"该企业没有该能力"。这一条同时是 00-engagement-plan §3.2 的红线第 4 条（AC-11 中立性红线）。

### 90.1.5 关于 `[未验证]` 的含义

- 凡标 `[未验证]` 者，**URL 结构或站点可达性已确认，但正文未取到**，交付前须复核；**不得作为事实断言使用**。
- 本报告中凡涉及 R155/R156 的**具体条款号、强制时间表、审核要求**，本次**无一手来源**；凡引用必须标注「[未验证] 依通行公开认知」或改为待补证陈述，**不得给出条款编号**（见 source-dossier §1.4 写作纪律提示）。

---

## 90.2 中国法规与标准

本节按 source-dossier §1.1（强制性国标 GB）/ §1.2（推荐性国标 GB/T）/ §1.3（行政法规与部门规章）逐条列出，覆盖 dossier 中全部条目。中国国标条目的一手来源均为**国家标准全文公开系统**（openstd.samr.gov.cn），证据等级为 `[A]`。

### 90.2.1 强制性国家标准（GB，[A]）

- **R-1.1-01** GB 44495-2024《汽车整车信息安全技术要求》—— 状态：现行（强制性）—— 发布 2024-08-23，实施 2026-01-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=2DB552CAA58F589705C3DC7AD47AC2AB —— [A]。用途：中国车云与 OTA 安全的**合规基线**，2026-01-01 起对新车型强制适用。
- **R-1.1-02** GB 44496-2024《汽车软件升级通用技术要求》—— 状态：现行（强制性）—— 发布 2024-08-23，实施 2026-01-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=8BC0D8B44DD4E71F9557BADE5175565A —— [A]。用途：OTA（软件升级）方向的强制基线，与 GB/T 47325-2026 互为强制/推荐配套。
- **R-1.1-03** GB 44495 / GB 44496 组合说明 —— 属**强制性**国标（"现行"状态），是中国车云与 OTA 安全的合规基线，2026-01-01 起对新车型强制适用 —— 证据等级承接 R-1.1-01/02 [A]。备注：本条为 dossier §1.1 中对两项强标的合并定性，非独立来源。

### 90.2.2 推荐性国家标准（GB/T，[A]）

- **R-1.2-01** GB/T 40855-2021《电动汽车远程服务与管理系统信息安全技术要求及试验方法》—— 发布 2021-10-11，实施 2022-05-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=AC47DD65376598FB44E0F24FBEBBF769 —— [A]。用途：远程服务与管理系统（车云远程服务面）的信息安全技术要求。
- **R-1.2-02** GB/T 40856-2021《车载信息交互系统信息安全技术要求及试验方法》—— 发布 2021-10-11，实施 2022-05-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=9995D55CBCAE667570C36F6A6CD1712D —— [A]。用途：车载信息交互系统（座舱侧交互面）技术要求。
- **R-1.2-03** GB/T 40857-2021《汽车网关信息安全技术要求及试验方法》—— 发布 2021-10-11，实施 2022-05-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=2977F0AC1719BBEFB9649C0146B0FC55 —— [A]。用途：汽车网关（车内与车云边界）技术要求。
- **R-1.2-04** GB/T 38628-2020《信息安全技术 汽车电子系统网络安全指南》—— 发布 2020-04-28，实施 2020-11-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=59F8899E944C9ED52288FE5E0146C621 —— [A]。用途：汽车电子系统网络安全的通用指南（早于 40855~40857 系列的框架性文件）。
- **R-1.2-05** GB/T 41871-2022《信息安全技术 汽车数据处理安全要求》—— 发布 2022-10-14，实施 2023-05-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=4D3C5BB193E079AD54294E5845749B8F —— [A]。用途：汽车数据处理的安全要求，与《汽车数据安全管理若干规定（试行）》配套。
- **R-1.2-06** GB/T 44464-2024《汽车数据通用要求》—— 发布/实施 2024-08-23 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=D63AAC0203E9B169F74B10E547A3CBCE —— [A]。用途：汽车数据通用要求。
- **R-1.2-07** GB/T 45112-2024《基于 LTE 的车联网无线通信技术 安全证书管理系统技术要求》—— 发布 2024-12-31，实施 2025-04-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=FB30FC033090F346D1B53E892DCD23BB —— [A]。用途：中国 C-V2X 证书管理体系，是"车-云-车"证书体系的国家级规范。
- **R-1.2-08** GB/T 45181-2024《车联网网络安全异常行为检测机制》—— 发布 2024-12-31，实施 2025-04-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=29740120554AA4DCB87A8FEAE106BA43 —— [A]。用途：车联网网络安全异常行为检测（监测与检测面）。
- **R-1.2-09** GB/T 47324-2026《车联网平台网络安全防护要求》—— 发布 2026-03-31，实施 2026-10-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=90F36FFBED2E85627B648B837A522527 —— [A]。用途：**直接命中本报告主题：车联网云平台侧的防护要求**。
- **R-1.2-10** GB/T 47325-2026《车联网在线升级安全技术要求与测试方法》—— 发布 2026-03-31，实施 2026-10-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=8407225889D602060265D0ABB8D14AA7 —— [A]。用途：车联网 OTA（在线升级）安全的技术要求与测试方法。
- **R-1.2-11** GB/T 47467-2026《车联网安全管理接口规范》—— 发布 2026-04-30，实施 2026-11-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=AC95A675E7B6E8E822E66B30BE14ED5C —— [A]。用途：**接口层规范，与授权/访问控制的 API 治理直接相关**。
- **R-1.2-12** GB/T 44402.1-2024《卡及身份识别安全设备 数字钥匙系统 第 1 部分：参考架构》—— 发布 2024-08-23，实施 2025-03-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=9CDE5F17C28F5332BA9CBEDD4618FD77 —— [A]。用途：中国数字钥匙授权模型的国标参考架构（对应第 90.7 节数字钥匙主题）。
- **R-1.2-13** GB/T 32918.1~.5-2016/2017《SM2 椭圆曲线公钥密码算法（总则/数字签名/密钥交换/公钥加密/参数定义）》—— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=3EE2FD47B962578070541ED468497C5B 等 —— [A]。用途：国密 SM2 算法族基础规范。备注：dossier 以「等」标注该系列含多个分册，本台账照录其首条 URL，不补其他分册 URL。
- **R-1.2-14** GB/T 32905-2016《SM3 密码杂凑算法》—— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=45B1A67F20F3BF339211C391E9278F5E —— [A]。用途：国密杂凑算法。
- **R-1.2-15** GB/T 32907-2016《SM4 分组密码算法》—— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=7803DE42D3BC5E80B0C3E5D8E873D56A —— [A]。用途：国密分组密码算法。
- **R-1.2-16** GB/T 35275-2017《SM2 密码算法加密签名消息语法规范》—— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=A7B91213CC4862B31BE2C84665CB8F7E —— [A]。用途：SM2 消息语法（与 RFC 8998 国密 TLS 落点配套）。
- **R-1.2-17** GB/T 35276-2017《SM2 密码算法使用规范》—— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=2127A9F19CB5D7F20D17D334ECA63EE5 —— [A]。用途：SM2 使用规范。

### 90.2.3 行政法规与部门规章（[A]）

- **R-1.3-01** 《汽车数据安全管理若干规定（试行）》（网信办等五部门令第 7 号）—— 2021-08-16 成文，2021-10-01 施行 —— https://www.gov.cn/zhengce/zhengceku/2021-09/12/content_5640023.htm —— [A]。用途：规定重要数据目录、境内存储、年度报送、出境评估等义务。
- **R-1.3-02** 《汽车数据安全管理若干规定（试行）》答记者问 —— http://www.gov.cn/zhengce/2021-08/20/content_5632437.htm —— [A]。用途：对上述规定的官方解释口径（答记者问）。备注：dossier 以「同上，答记者问」标注，与 R-1.3-01 同文件族。

**中国法规与标准小结**：本节共 20 条台账（R-1.1-01~03、R-1.2-01~17、R-1.3-01~02），全部为 `[A]`，均逐字取自 dossier。其中与本报告主题「车云安全」直接命中的有 R-1.2-09（车联网平台防护）、R-1.2-10（OTA 安全）、R-1.2-11（安全管理接口）、R-1.2-07（C-V2X 证书管理）与 R-1.1-01/02（整车信息安全和软件升级强制基线）。

---

## 90.3 国际标准与法规（对应 dossier §1.4，覆盖度受限）

本节整体受区域封锁与检索受限影响，**多数条目为 `[未验证]` 或 `[C]`**，请务必连同等级一并引用。

- **R-1.4-01** ISO/SAE 21434:2021《Road vehicles — Cybersecurity engineering》—— SAE 收录页 https://www.sae.org/standards/content/iso21434/ ；ISO 官方页 https://www.iso.org/standard/70918.html 被 Cloudflare 拦截 —— [未验证：编号与年份为通行共识，正文未取到]。用途：整车网络安全工程国际标准。
- **R-1.4-02** SAE J3061《Cybersecurity Guidebook for Cyber-Physical Vehicle Systems》（21434 前身）—— https://www.sae.org/standards/j3061_201601-cybersecurity-guidebook-cyber-physical-vehicle-systems/ —— [B：HTTP 200]。用途：21434 之前的车联网安全指南。
- **R-1.4-03** ISO 24089:2023《Road vehicles — Software update engineering》—— https://www.iso.org/standard/77796.html —— [未验证：iso.org Cloudflare 拦截]。用途：软件升级工程国际标准。
- **R-1.4-04** UN Regulation No.155（CSMS 网络安全管理体系）与 No.156（SUMS 软件更新管理体系）—— https://unece.org/transport/vehicle-regulations/wp29/grva —— [未验证：unece.org 被 Cloudflare 全站拦截，URL 结构需复核]。用途：欧盟型式认证相关的网络安全管理体系与软件更新管理体系法规。
- **R-1.4-05** 欧盟 GDPR Regulation (EU) 2016/679 —— https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng —— [C：EUR-Lex 返回 202异步状态，正文未取到]。用途：个人数据保护（车辆数据涉个人数据的合规底座）。
- **R-1.4-06** 欧盟 Data Act Regulation (EU) 2023/2854（车辆数据可携权/互联产品数据访问权）—— https://eur-lex.europa.eu/eli/reg/2023/2854/oj —— [C：HTTP 202，正文未取到]。用途：车辆数据可携与互联产品数据访问权。

**写作纪律提示（照录 dossier §1.4）**：涉及 R155/R156 的**具体条款号、强制时间表、审核要求**时，本次无一手来源。凡引用必须标注「[未验证] 依通行公开认知」或改为待补证陈述，**不得给出条款编号**。

---

## 90.4 授权与身份协议规范（对应 dossier §2.1）

本节是报告授权与访问控制章节的**规范底座**，全部经 RFC Editor / openid.net 取证（HTTP 200），绝大多数为 `[A]`。引用格式建议 `RFC 编号 §章节`。

- **R-2.1-01** RFC 6749 (2012) The OAuth 2.0 Authorization Framework（Obsoletes RFC 5849）—— https://www.rfc-editor.org/rfc/rfc6749.txt —— [A]。用途：OAuth 2.0 授权框架总纲。
- **R-2.1-02** RFC 6750 (2012) OAuth 2.0 Bearer Token Usage —— https://www.rfc-editor.org/rfc/rfc6750.txt —— [A]。用途：Bearer 令牌在 HTTP 中的使用、`WWW-Authenticate` 错误语义。
- **R-2.1-03** RFC 8252 (2017) OAuth 2.0 for Native Apps —— https://www.rfc-editor.org/rfc/rfc8252.txt —— [A]。用途：原生 App 必须使用系统浏览器/外部用户代理，禁止内嵌 WebView。
- **R-2.1-04** RFC 7636 (2015) PKCE（Proof Key for Code Exchange）—— https://www.rfc-editor.org/rfc/rfc7636.txt —— [A]。用途：公共客户端授权码拦截防护。
- **R-2.1-05** RFC 9068 (2021) JWT Profile for OAuth 2.0 Access Tokens —— https://www.rfc-editor.org/rfc/rfc9068.txt —— [A]。用途：`typ: at+jwt`、`aud`/`iss`/`exp` 校验要求。
- **R-2.1-06** RFC 8705 (2020) OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens —— https://www.rfc-editor.org/rfc/rfc8705.txt —— [A]。用途：mTLS 客户端认证 + 证书绑定令牌（持有的令牌不可被复制盗用）；**车云链路最关键的授权规范**。
- **R-2.1-07** RFC 9449 (2023) OAuth 2.0 Demonstrating Proof of Possession (DPoP) —— https://www.rfc-editor.org/rfc/rfc9449.txt —— [A]。用途：发送方约束令牌，`DPoP` 头 + JWK 指纹绑定。
- **R-2.1-08** RFC 9396 (2023) OAuth 2.0 Rich Authorization Requests —— https://www.rfc-editor.org/rfc/rfc9396.txt —— [A]。用途：`authorization_details` 结构化权限对象，替代裸字符串 scope；**车控场景"资源级授权"的规范依据**。
- **R-2.1-09** RFC 8693 (2020) OAuth 2.0 Token Exchange —— https://www.rfc-editor.org/rfc/rfc8693.txt —— [A]。用途：`subject_token`/`actor_token`，代理链授权。
- **R-2.1-10** RFC 7523 (2015) JWT Profile for OAuth 2.0 Client Authentication and Authorization Grants —— https://www.rfc-editor.org/rfc/rfc7523.txt —— [A]。用途：服务账号 + 客户端断言。
- **R-2.1-11** RFC 7662 (2015) OAuth 2.0 Token Introspection —— https://www.rfc-editor.org/rfc/rfc7662.txt —— [A]。用途：令牌内省，不透明令牌的实时校验。
- **R-2.1-12** RFC 8414 (2018) OAuth 2.0 Authorization Server Metadata —— https://www.rfc-editor.org/rfc/rfc8414.txt —— [A]。用途：`.well-known/oauth-authorization-server` 自动发现（与 Tesla 元数据发布对应）。
- **R-2.1-13** RFC 7009 (2013) OAuth 2.0 Token Revocation —— https://www.rfc-editor.org/rfc/rfc7009.txt —— [A]。用途：令牌吊销端点。
- **R-2.1-14** RFC 9470 (2023) OAuth 2.0 Step Up Authentication Challenge Protocol —— https://www.rfc-editor.org/rfc/rfc9470.txt —— [A]。用途：`acr`/`amr` 步进认证挑战。
- **R-2.1-15** RFC 8628 (2019) OAuth 2.0 Device Authorization Grant —— https://www.rfc-editor.org/rfc/rfc8628.txt —— [A]。用途：无浏览器设备授权，车机/受限 UI 场景适用。
- **R-2.1-16** RFC 9635 (2024) Grant Negotiation and Authorization Protocol (GNAP)，Standards Track，2024-10 —— https://www.rfc-editor.org/rfc/rfc9635.txt —— [A]。用途：**下一代授权协议，面向"细粒度 + 可协商"授权，代表演进方向**。
- **R-2.1-17** OAuth 2.1 草案 draft-ietf-oauth-v2-1-16 —— https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/ —— [A]。用途：强制 PKCE、废弃隐式流与密码模式、Bearer 令牌最小化。
- **R-2.1-18** OpenID Connect Core 1.0 —— https://openid.net/specs/openid-connect-core-1_0.html —— [A]。用途：`id_token`、UserInfo、认证与授权分离。
- **R-2.1-19** OpenID Connect Discovery 1.0 —— https://openid.net/specs/openid-connect-discovery-1_0.html —— [A]。用途：`/.well-known/openid-configuration` 自动发现。
- **R-2.1-20** FIDO Alliance 规范（无密码/抗钓鱼凭证）—— https://fidoalliance.org/specifications/ —— [B]。用途：抗钓鱼的强身份凭证。
- **R-2.1-21** W3C WebAuthn Level 2 —— https://www.w3.org/TR/webauthn-2/ —— [A]。用途：WebAuthn 认证器接口规范。
- **R-2.1-22** UMA 2.0（User-Managed Access，用户自管授权）—— https://docs.kantarainitiative.org/uma/wg/rec-oauth-uma-grant-2.0.html —— [未验证：Kantara 站点 curl 超时]。用途：用户自管授权模型（待补证）。

---

## 90.5 通信安全与 PKI（对应 dossier §3，[A] 为主）

- **R-3-01** RFC 8446 (2018) TLS 1.3 —— https://www.rfc-editor.org/rfc/rfc8446.txt —— [A]。用途：1-RTT 握手、0-RTT 重放风险、前向保密。
- **R-3-02** RFC 5280 (2008) X.509 PKI 证书与 CRL 规范 —— https://www.rfc-editor.org/rfc/rfc5280.txt —— [A]。用途：证书链、扩展、吊销列表。
- **R-3-03** RFC 6960 (2013) OCSP（在线证书状态查询）—— https://www.rfc-editor.org/rfc/rfc6960.txt —— [A]。用途：在线证书状态查询。
- **R-3-04** RFC 3161 (2001) Time-Stamp Protocol —— https://www.rfc-editor.org/rfc/rfc3161.txt —— [A]。用途：可信时间戳，**防重放的时间基准**。
- **R-3-05** RFC 8555 (2019) ACME —— https://www.rfc-editor.org/rfc/rfc8555.txt —— [A]。用途：自动化证书签发/轮换，短周期证书的工程前提。
- **R-3-06** RFC 5480 (2009) ECDSA/EC 公钥在 X.509 中的表示 —— https://www.rfc-editor.org/rfc/rfc5480.txt —— [A]。用途：椭圆曲线公钥的证书表示。
- **R-3-07** RFC 8017 (2016) PKCS #1 RSA —— https://www.rfc-editor.org/rfc/rfc8017.txt —— [A]。用途：RSA 加解密与签名格式。
- **R-3-08** RFC 6090 (2011) ECDSA/ECC 基础 —— https://www.rfc-editor.org/rfc/rfc6090.txt —— [A]。用途：ECDSA/ECC 基础算法。
- **R-3-09** RFC 8998 (2021) ShangMi (SM) Cipher Suites for TLS 1.3 —— https://www.rfc-editor.org/rfc/rfc8998.txt —— [A]。用途：SM2 签名、AEAD_SM4_GCM / AEAD_SM4_CCM、SM3；**国密 TLS 在国际标准层面的唯一落点，国产车云链路合规的关键**。
- **R-3-10** IEEE 1609.2（WAVE 安全服务 / 证书格式）—— https://standards.ieee.org/ieee/1609.2/6865/ —— [C：HTTP 200，正文未解析]。用途：WAVE/V2X 安全服务与证书格式。
- **R-3-11** 美国 SCMS（V2X 安全证书管理体系）—— [未验证：未取得可核验官方 URL]。用途：美国 V2X 证书管理体系（本次未取得可核验 URL）。

---

## 90.6 硬件根信任（TEE / SE / HSM，对应 dossier §4）

- **R-4-01** GlobalPlatform TEE System Architecture v1.3（规范号 GPD_SPE_009）—— https://globalplatform.org/specs-library/tee-system-architecture/ —— [A]。用途：TEE 系统架构规范。
- **R-4-02** GlobalPlatform 规范库 — Secure Element 分类 —— https://globalplatform.org/specs-library/?filter-committee=secure-element —— [A]。用途：安全元件（SE）规范入口。
- **R-4-03** OP-TEE（开源 TEE OS，TrustZone 之上的 TEE 实现）—— https://optee.readthedocs.io/en/latest/ —— [A]。用途：开源 TEE 实现。
- **R-4-04** ARM TrustZone for Cortex-A —— https://www.arm.com/technologies/trustzone-for-cortex-a —— [B]。用途：Cortex-A 上的 TEE 隔离技术。
- **R-4-05** ARM TrustZone for Cortex-M —— https://www.arm.com/technologies/trustzone-for-cortex-m —— [B]。用途：Cortex-M 上的 TEE 隔离技术。
- **R-4-06** EVITA 项目（E-safety Vehicle Intrusion Protected Applications）—— https://www.evita-project.org/ —— [B]。用途：定义车载 HSM 的 Full / Medium / Light 三级分级。
- **R-4-07** NIST FIPS 140-3（密码模块安全要求）—— https://csrc.nist.gov/pubs/fips/140-3/final —— [A]。用途：HSM 认证基线。
- **R-4-08** NIST FIPS 186-5（数字签名标准 DSS）—— https://csrc.nist.gov/pubs/fips/186-5/final —— [A]。用途：数字签名标准。
- **R-4-09** NIST FIPS 197（AES）—— https://csrc.nist.gov/pubs/fips/197/final —— [A]。用途：AES 分组密码标准。
- **R-4-10** NIST SP 800-57 Part 1 Rev.5（密钥管理建议）—— https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final —— [A]。用途：密钥生命周期、密码周期建议。
- **R-4-11** NIST SP 800-38D（GCM 模式）—— https://csrc.nist.gov/pubs/sp/800/38/d/final —— [A]。用途：GCM 认证加密模式。
- **R-4-12** NIST SP 800-90A Rev.1（确定性随机比特发生器）—— https://csrc.nist.gov/pubs/sp/800/90/a/r1/final —— [A]。用途：确定性随机比特发生器。
- **R-4-13** NIST SP 800-133（密钥生成）—— https://csrc.nist.gov/pubs/sp/800/133/final —— [A]。用途：密钥生成建议。
- **R-4-14** Infineon AURIX / TriCore 32 位汽车微控制器 —— https://www.infineon.com/cms/en/product/microcontroller/32-bit-tricore-microcontroller/ —— [C：HTTP 202，型号页未解析]。用途：汽车 MCU 产品线。
- **R-4-15** NXP S32 汽车平台 —— https://www.nxp.com/products/processors-and-microcontrollers/s32-automotive-platform:S32 —— [未验证：curl 超时]。用途：汽车处理器平台。
- **R-4-16** Renesas 汽车产品线（RH850 系列）—— https://www.renesas.com/en/products/automotive-products —— [C]。用途：汽车 MCU 产品线。
- **R-4-17** TI Jacinto TDA4VM —— https://www.ti.com/product/TDA4VM —— [C]。用途：汽车 ADAS/域控 SoC。
- **R-4-18** AUTOSAR Classic Platform（Crypto Stack、SecOC、IdsM 入侵检测）—— https://www.autosar.org/standards/classic-platform/ —— [未验证：autosar.org 超时]。用途：车载基础软件的密码栈/安全车载通信/入侵检测。
- **R-4-19** TCG TPM 2.0 规范 —— https://trustedcomputinggroup.org/ —— [未验证：TCG 站点 403/超时]。用途：可信平台模块规范。
- **R-4-20** SHE（Secure Hardware Extension）规范 —— [未找到可核验公开一手 URL：成员制规范]。用途：安全硬件扩展（成员制规范，本次未取得公开一手 URL）。

---

## 90.7 数字钥匙与近场授权（对应 dossier §5）

- **R-5-01** CCC Digital Key Release 3.0 发布公告（2021-04-21）—— https://carconnectivity.org/car-connectivity-consortium-delivers-digital-key-release-3-0-specification-businesswire/ —— [A]。用途：新增 **BLE + UWB** 实现被动无钥匙进入与启动，NFC 保留为强制备用方案，密钥存储于 **Secure Element**。
- **R-5-02** CCC Digital Key 主页面（跨 OS 生态、认证计划）—— https://carconnectivity.org/digital-key/ —— [A]。用途：CCC 数字钥匙总入口。
- **R-5-03** CCC Digital Key Release 3 v1.1 规范向公众开放 —— https://carconnectivity.org/car-connectivity-consortium-makes-digital-key-release-3-v1-1-specification-available-to-the-public/ —— [B]。用途：Release 3 v1.1 公众开放说明。
- **R-5-04** CCC 与 FiRa Consortium 就 UWB 技术合作 —— https://carconnectivity.org/car-connectivity-consortium-and-fira-consortium-partner-on-uwb-technology-used-in-the-ccc-digital-key/ —— [B]。用途：CCC/FiRa UWB 合作。
- **R-5-05** FiRa Consortium 2.0 技术规范（2023-11）—— https://www.firaconsortium.org/news/press-releases/2023/11/fira-consortium-publishes-fira-2-0-technical-specifications —— [B]。用途：UWB 技术规范 2.0。
- **R-5-06** FiRa Core 3.0 规范与认证（2025-01）—— https://www.firaconsortium.org/news/press-releases/2025/01/fira-consortium-unveils-fira-core-3-0-specifications-and-certification —— [B]。用途：UWB 核心规范 3.0 与认证。
- **R-5-07** FiRa Core 4.0 规范与认证（2025-12）—— https://www.firaconsortium.org/news/press-releases/2025/12/fira-consortium-unveils-fira-core-4-0-specifications-and-certification —— [B]。用途：UWB 核心规范 4.0 与认证。
- **R-5-08** GB/T 44402.1-2024 数字钥匙系统参考架构 —— 见 90.2.2 的 R-1.2-12（https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=9CDE5F17C28F5332BA9CBEDD4618FD77）—— [A]。用途：中国数字钥匙授权模型国标参考架构（交叉引用）。
- **R-5-09** IEEE 802.15.4z（UWB 物理层增强）—— [未验证：未取得可核验官方 URL]。用途：UWB 物理层增强（本次未取得可核验官方 URL）。

---

## 90.8 OTA 与供应链安全（对应 dossier §6）

- **R-6-01** Uptane 框架官网 —— https://uptane.org/ —— [A]。用途：首个面向汽车、面向"可抵御国家级攻击者"设计的软件更新安全系统；Linux Foundation Joint Development Foundation 项目。
- **R-6-02** Uptane Standard 最新版 **2.1.0** —— https://uptane.org/docs/latest/standard/uptane-standard —— [A]。用途：Director 仓库 + Image 仓库双仓库模型。
- **R-6-03** The Update Framework (TUF) 官网 —— https://theupdateframework.io/ —— [B]。用途：阈值签名，防仓库/密钥泄露。
- **R-6-04** TUF 规范 —— https://theupdateframework.github.io/specification/latest/ —— [A]。用途：Root / Targets / Snapshot / Timestamp 四角色 + 委托 + threshold/quorum 阈值模型。
- **R-6-05** RFC 9019 (2021) A Firmware Update Architecture for IoT Devices（SUIT 架构）—— https://www.rfc-editor.org/rfc/rfc9019.txt —— [A]。用途：IoT 固件更新架构（SUIT）。
- **R-6-06** RFC 9124 (2022) A Manifest Information Model for Firmware Updates in IoT Devices（SUIT Manifest 信息模型）—— https://www.rfc-editor.org/rfc/rfc9124.txt —— [A]。用途：SUIT Manifest 信息模型。
- **R-6-07** IETF SUIT 工作组 —— https://datatracker.ietf.org/wg/suit/about/ —— [A]。用途：SUIT 标准工作组入口。
- **R-6-08** SUIT Manifest 草案 draft-ietf-suit-manifest-27 —— https://www.ietf.org/archive/id/draft-ietf-suit-manifest-27.html —— [C]。用途：SUIT Manifest 草案文本。
- **R-6-09** GB 44496-2024 / GB/T 47325-2026（中国 OTA 强制与推荐国标）—— 见 90.2 的 R-1.1-02 与 R-1.2-10 —— [A]。用途：中国 OTA 合规基线（交叉引用）。
- **R-6-10** SPDX 规范（SBOM；对应国际标准 ISO/IEC 5962:2021）—— https://spdx.dev/use/specifications/ —— [A]。用途：SBOM 规范。
- **R-6-11** CycloneDX 规范概览（SBOM）—— https://cyclonedx.org/specification/overview/ —— [B]。用途：SBOM 规范。
- **R-6-12** SLSA v1.0 分级（Build L0–L3）—— https://slsa.dev/spec/v1.0/levels —— [A]。用途：供应链构建完整性分级。
- **R-6-13** in-toto 规范（供应链完整性元数据与签名链）—— https://in-toto.io/specs/ —— [B]。用途：供应链完整性元数据与签名链。
- **R-6-14** OCPP 1.6 / 2.0.1 / 2.1（充电侧协议族，授权与计量）—— https://www.openchargealliance.org/protocols/ —— [A]。用途：充电侧协议族的授权与计量（Open Charge Alliance）。
- **R-6-15** ISO 15118-2 / -20（Plug & Charge，TLS + contract certificate）—— https://www.iso.org/standard/55366.html —— [未验证：iso.org Cloudflare 拦截，标准号需复核]。用途：充电授权的证书模型。

---

## 90.9 车企与平台一手证据（对应 dossier §7.1–§7.9，逐主体列出）

本节是报告车企实践章节的证据台账。**每条给出入口 URL、证据等级、取证结果一句话**。凡 dossier 标注为封锁/未取到者，照录其结果并指向 90.10。

### 90.9.1 Tesla（对应 dossier §7.1，证据最厚，全部来自 developer.tesla.com，[A]）

- **R-7.1-01** 令牌类型与鉴权头（`Authorization: Bearer <token>`、partner token、third-party token、third-party-for-business token）—— https://developer.tesla.com/docs/fleet-api/authentication/overview —— [A]。取证结果：Fleet API 目前公开文档中最完整的"车-云第三方授权"实现范例。
- **R-7.1-02** Scope 全清单（`openid`、`offline_access`、`user_data`、`vehicle_device_data`、`vehicle_location`、`vehicle_cmds`、`vehicle_charging_cmds`、`vehicle_specs`、`vehicle_pricing_info`、`energy_device_data`、`energy_cmds`、`enterprise_management`）—— https://developer.tesla.com/docs/fleet-api/authentication/overview —— [A]。取证结果：scope 模型可直接作为行业标尺。
- **R-7.1-03** `granular_access.hide_private=true` 资源级收窄 —— https://developer.tesla.com/docs/fleet-api/authentication/overview —— [A]。取证结果：带该标志的车辆共享即使被授予 `vehicle_location` 也拿不到任何位置，且无法流式传输位置字段（"授权被授予但资源级策略进一步收窄"的双层控制实例）。
- **R-7.1-04** `vehicle_specs` 仅 Partner Token 可用、对任意车辆可用、无需车主授权 —— https://developer.tesla.com/docs/fleet-api/authentication/overview —— [A]。取证结果：存在不进入"逐车主同意"模型的资源访问路径（重要的授权控制例外）。
- **R-7.1-05** 授权服务器元数据 —— https://fleet-auth.prd.vn.cloud.tesla.com/oauth2/v3/thirdparty/.well-known/openid-configuration —— [A]。取证结果：对应 RFC 8414 / OIDC Discovery。
- **R-7.1-06** 授权码流程细节（含授权端点 `https://auth.tesla.com/oauth2/v3/authorize`、`state`/`nonce`、`prompt_missing_scopes`/`require_requested_scopes`/`show_keypair_step`）—— https://developer.tesla.com/docs/fleet-api/authentication/third-party-tokens —— [A]。取证结果：认证端点"不计费"；刷新令牌一次性使用且 3 个月过期，24 小时宽限。
- **R-7.1-07** 令牌端点（`POST https://fleet-auth.prd.vn.cloud.tesla.com/oauth2/v3/token`，`audience` 必须是 Fleet API base URL）—— https://developer.tesla.com/docs/fleet-api/authentication/third-party-tokens —— [A]。取证结果：令牌端点与 API 端点分属不同主机。
- **R-7.1-08** 授权撤销入口 `https://auth.tesla.com/user/revoke/consent?revoke_client_id=$CLIENT_ID&back_url=$RETURN_URL` —— https://developer.tesla.com/docs/fleet-api/authentication/third-party-tokens —— [A]。取证结果：车主侧可撤销入口。
- **R-7.1-09** 虚拟密钥（Virtual Key）——车端授权校验 —— https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide —— [A]。取证结果：公私钥对，公钥由可信用户添加到车辆，车辆执行命令前验证载荷签名；文档称虚拟密钥"甚至能阻止 Tesla 自己的后端访问这些能力"。
- **R-7.1-10** 虚拟密钥工程细节（`prime256v1`/P-256，公钥托管于 `https://developer-domain.com/.well-known/appspecific/com.tesla.3p.public-key.pem`，配对深链 `https://tesla.com/_ak/<developer-domain.com>`）—— https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide —— [A]。取证结果：B2B 车辆可自动添加密钥（条件为已配对密钥少于 20 把）；非 B2B 渠道车辆无法远程添加。
- **R-7.1-11** Fleet Telemetry（客户端源码 https://github.com/teslamotors/fleet-telemetry ，命令代理 https://github.com/teslamotors/vehicle-command ）—— https://developer.tesla.com/docs/fleet-api/fleet-telemetry —— [A]。取证结果：车辆直连开发者服务器，取代轮询 `vehicle_data`；配置由应用私钥签名且"Tesla 无法编辑"；单台车辆最多同时向 5 个第三方应用推流。
- **R-7.1-12** 限流与计费 —— https://developer.tesla.com/docs/fleet-api/billing-and-limits —— [A]。取证结果：实时数据 60 次/分、唤醒 3 次/分、设备命令 30 次/分，同账号多应用共享限额；超限会暂停 API 并移除 Fleet Telemetry 推流配置（且不恢复）；明确过渡日期 "Application access will not be disabled during the payment transition period which ends February 1, 2024"。
- **R-7.1-13** 漏洞披露与赏金 —— https://bugcrowd.com/engagements/tesla —— [A/B]。取证结果：Tesla 在 Bugcrowd 运营漏洞赏金项目，启动于 2015-08-04；车辆/能源产品问题须邮件报至 `vulnerabilityreporting@tesla.com` 并使用 Tesla GPG 公钥。

**Tesla 未能证实项（禁止当作事实写入，见 dossier §7.1）**：① "访问令牌有效期约 8 小时"在已读页面中**未获证实**，已证实的是刷新令牌一次性且 3 个月有效、以及 24 小时复用宽限，访问令牌 TTL 标记为待补证；② "2023 年 Toyota/Tesla 漏洞披露事件"与"Tesla 2023 年 API 收紧"的叙事版本未取到一手来源，仅有 "2024-02-01 计费过渡结束"这一硬日期，标记为待补证。

### 90.9.2 Mercedes-Benz（对应 dossier §7.2，全部来自 developer.mercedes-benz.com，[A]）

- **R-7.2-01** 开发者平台入口 —— https://developer.mercedes-benz.com —— [A]。取证结果：运营主体 Mercedes-Benz Connectivity Services GmbH（页脚版权 "© 2026"）；产品分类含 Fleet Data、Smart Vehicle Data、Infrastructure Data、Vehicle Commerce Data、Repair & Maintenance Data。
- **R-7.2-02** 文档页（两种鉴权集成模式：OAuth Authorization Code Flow 与 Client Credentials Flow）—— https://developer.mercedes-benz.com/product-docs —— [A]。取证结果：明确列出两种鉴权集成模式。
- **R-7.2-03** 授权码流说明 —— https://developer.mercedes-benz.com/get-started/oauth/authorization-code-flow —— [A]。取证结果：部分 API 提供燃油状态、车门锁状态等 GDPR 意义上的个人数据，因此需要终端用户同意；平台自称使用"standard OAuth 2.0"；五步流程；`openid` 为获得有效令牌所必需、`offline_access` 为获得刷新令牌所必需；授权端点示例 `https://ssoalpha.dvb.corpinter.net/v1/auth?...`、令牌端点 `https://ssoalpha.dvb.corpinter.net/v1/token`；示例 scope `scope=openid offline_access mb:vehicle:mbdata:fuelstatus`（`mb:` 命名空间式三段 scope，是车企资源级 scope 设计的典型样本）；令牌端点客户端认证采用 HTTP Basic；`expires_in` 默认 3599 秒；刷新令牌一次性使用。

**Mercedes 未取到（见 dossier §7.2）**：数字钥匙（CCC）、mTLS/证书固定、TEE/安全元件、OTA 安全、2024–2025 车辆数据 API 政策文档、MBition、Mercedes Pay —— 全部标记待补证，见 90.10。

### 90.9.3 Volkswagen Group / CARIAD（对应 dossier §7.3，[A]，但为自述营销口径）

- **R-7.3-01** Automotive Cloud 定位与指标 —— https://cariad.technology/de/en/solutions/automotive-cloud-connectivity.html —— [A，公司自述口径]。取证结果：自称"超过 4500 万辆网联车""全球最大的汽车云基础设施"；指标条含 "1 ecosystem for all VW brands"、"45 million connected vehicles"、"90 markets connected"、"365 days global support"；称数据平台是"所有车辆相关 AI 创新的关键使能器"，云支持"安全关键更新"的 OTA 下发。
- **R-7.3-02** CARIAD 自我定位与产品分类 —— https://cariad.technology/ —— [A]。取证结果："We are the Volkswagen Group's automotive software company... for iconic car brands, including Audi, Volkswagen and Porsche"；产品分类含 Infotainment、Automated Driving、Connectivity & Cloud、Motion & Energy。

**VW/CARIAD 未取到（见 dossier §7.3）**：E3 架构、VW.OS、ID 系列 OTA 细节、UN R155 集团合规声明、与 Mobileye/Bosch 的合作、任何 CARIAD 安全白皮书；VW Newsroom 对 `R155` 的站内检索返回零结果项 —— 全部标记待补证。

### 90.9.4 BMW（对应 dossier §7.4，本次网络封锁，未取到）

- **R-7.4-01** https://developer.bmwgroup.com/ —— [A，直接观测]。取证结果：DNS 可解析（160.46.244.54）但返回 Apache 占位页："BMW Group – no content deployed … This project didn't deploy any content yet"（Last-Modified 2026-04-27），未提供 CarData / OAuth 文档。
- **R-7.4-02** https://crd.bmwgroup.com/ 与 https://b2b-developer.bmwgroup.com/ —— [A，直接观测]。取证结果：前者无法解析；后者超时。
- **R-7.4-03** `www.bmw.com` / `www.bmwgroup.com` —— [A，直接观测]。取证结果：从本网络被区域封锁（HTTP 000 / 边缘封锁）；`www.bmwgroup.com/en/innovation/vehicle-data.html` 经浏览器返回站点自身 404。
- **R-7.4-04** https://b2b.bmw.com —— [A]。取证结果：可达，但为**供应商采购门户**（purchasing/logistics 登录），非车辆数据开发者 API 门户。

**BMW 未取到（见 dossier §7.4）**：BMW CarData OAuth scope 清单、令牌有效期、CCC 数字钥匙、BMW 安全白皮书 —— 原因是网络/检索封锁，**不得据此推断 BMW 无相应方案**。

### 90.9.5 Rivian（对应 dossier §7.5，本次区域封锁，未取到）

- **R-7.5-01** https://rivian.com —— [A，直接观测]。取证结果：从本出口返回 Amazon CloudFront 403："The CloudFront distribution is configured to block access from your country"。
- **R-7.5-02** `developer.rivian.com` 与 `api.rivian.com` —— [A，直接观测]。取证结果：前者无 DNS 解析；后者可解析（13.35.190.19）但为 App 后端，非公开开发者门户。

**Rivian 未取到**：Rivian Fleet API、OAuth 支持、数字钥匙文档 —— 原因同上。

### 90.9.6 比亚迪 BYD（对应 dossier §7.6，i迪桥开放平台，[A]）

- **R-7.6-01** i迪桥开放平台入口 —— https://open.byd.com/ —— [A]。取证结果：官方开放平台名为「**i迪桥**」，首页显示"12 已上线服务 / 60 服务总系统 / 53.8 亿+ 累计服务请求数"，© 2025 比亚迪提供计算服务，粤 ICP 备 10216027 号；接入五步流程（登录平台 → 用户认证 → 应用创建 → 注册/订阅 → 服务访问授权后调试）；对接邮箱 `openapi@byd.com`。
- **R-7.6-02** 鉴权方式为 API Key（appKey）—— https://open.byd.com/platform?id=1848412878248345602 —— [A]（文档发布 2024-01-23）。取证结果：接口调用文档明确"用户创建应用 → 审核后生成 appKey 作为调用者身份识别"、"`x-Gateway-APIKey`：应用的 appKey，用于调用接口鉴权，传入 Header 头"；网关示例域名 `esb.byd.com.cn`（示例 URL `https://esb.byd.com.cn/tong/restful/api/mdm07670/package_1`），文档注明"以上示例只作为参考不可实际调用"。
- **R-7.6-03** 平台版本公告「i迪桥平台 3.3.4 版本全面升级」—— https://open.byd.com/notices-details?id=1994268247284723713&toB=1 —— [A]。取证结果：含 API 在线导出、API 提供者信息、API 注册暂存。
- **R-7.6-04** 定位判断 —— [A，依据平台自述]。取证结果：i迪桥为企业级 ESB/API 网关（覆盖供应链/研发/智造/营销/物流/品质/财务七大领域），**非车控开放平台**；未见 mTLS / 国密 / 数字钥匙 / OAuth scope 文档。

### 90.9.7 蔚来 NIO（对应 dossier §7.7，Open NSC，[A] 但文档陈旧）

- **R-7.7-01** Open NSC 入口 —— https://developer.nio.com/ —— [A]。取证结果：官方开放平台为 GitBook 托管的「**Open NSC（NIO Service Cloud）**」；文档首页标注"文档最后更新于: 2019-08-13，字段后续还有可能微调"，站点自述"正在建设中"；平台业务范围为服务云（一键加电/维保/拖车/租车/代泊/航班），**不含车控/数字钥匙 API**。
- **R-7.7-02** 鉴权为 app-id + secret 双凭证，非 OAuth —— https://developer.nio.com/docs/open-nsc/spec/integration-process.html —— [A]。取证结果："app-id 和 secret 是系统对接调用的唯一凭证……通过商务渠道获取"。
- **R-7.7-03** 环境 —— https://developer.nio.com/docs/open-nsc/spec/env.html —— [A]。取证结果：stg `https://open-stg.nio.com`，prod `https://open.nio.com`。
- **R-7.7-04** 接口规范正文受 token 保护 —— https://developer.nio.com/docs/open-nsc/spec/interface.html —— [A]。取证结果："请联系文档提供人获取文档访问 token"（平台侧把文档访问本身也纳入授权控制）。
- **R-7.7-05** NIO 隐私政策页 —— https://www.nio.cn/privacy-policy —— [A，JS 渲染，正文未取到]。

### 90.9.8 小米（对应 dossier §7.8，小米 IoT 开发者平台 / 信任中心，[A]）

- **R-7.8-01** 小米 IoT 开发者平台 —— https://iot.mi.com/ —— [A]。取证结果：2026 年品牌为「小米澎湃智联」，与 Xiaomi HyperOS Connect 联动，宣称"人车家全生态"；平台接入流程"成为开发者 → 创建产品 → 研发配置 → 认证发布"面向**硬件模组厂商**，非面向车企的车云 API 开放平台。
- **R-7.8-02** 文档中心 —— https://iot.mi.com/v2/new/doc/home —— [A]（HTTP 200，标题「小米IoT文档与资源中心」）。
- **R-7.8-03** 小米信任中心 —— https://trust.mi.com/zh-CN/compliance —— [A]。取证结果：载明 ISO/IEC 27001 认证（编号 IS 831552，范围含小米科技 IT 运维与云服务），并自述定期发布安全与隐私白皮书。

**小米未取到**：小米汽车（xiaomiev.com）专属开放平台、车控 API、OAuth scope、数字钥匙官方技术文档；小米汽车官网可达但无开发者入口。

### 90.9.9 理想 / 小鹏 / 极氪 / 零跑 / 奇瑞 / 华为（对应 dossier §7.9，覆盖度薄弱）

- **R-7.9-01** 理想：官方用户隐私政策（生效 2026-01-22，主体北京车励行信息技术有限公司、北京罗克维尔斯科技有限公司；覆盖官网/App/小程序/车机端）—— https://www.lixiang.com/agreement/privacy.html —— [A]。取证结果：`open.lixiang.com`、`developer.lixiang.com` 均**无 DNS 解析**；[未找到公开来源]。
- **R-7.9-02** 小鹏：`open.xiaopeng.com/dev/` 站点存在但对所有请求返回 **403 Forbidden（openresty）**，无法核实鉴权机制/scope/令牌有效期 —— [A 站点存在，内容不可验证]；`xmart.xiaopeng.com` 有 DNS 解析（47.96.221.177）但证书无效（ERR_CERT_AUTHORITY_INVALID）—— [未找到可验证公开来源]。
- **R-7.9-03** 小鹏：用户协议 —— https://login.xiaopeng.com/policy.html —— [A]（主体广州智鹏车联网科技有限公司）。
- **R-7.9-04** 极氪：`open.zeekrlife.com` 返回 HTTP 500 空页；`www.zeekrlife.com` 为官网但未发现开发者/开放平台入口 —— [A 站点存在，无可用信息]。
- **R-7.9-05** 零跑：`cn.leapmotor.com` 可达但无开放平台入口；`developer./dev./open.leapmotor.com` 均无 DNS —— [未找到公开来源]。
- **R-7.9-06** 奇瑞：官网设「网络产品安全漏洞」专栏 —— https://www.chery.cn/others/networksecurity/ —— [A，页面可达]。取证结果：`developer.chery.cn`、`open.chery.cn` 无 DNS —— [未找到公开来源]。
- **R-7.9-07** 华为：开发者联盟统一入口 —— https://developer.huawei.com/consumer/cn/ —— [A]。取证结果：尝试抓取 Wallet Kit 数字车钥匙文档（`/doc/harmonyos-guides/wallet-kit-*`）与安全文档均返回 JS 空壳页（标题仅「文档中心」，1749 字节），正文无法取证 —— [未找到可验证公开来源]。

### 90.9.10 车企侧矛盾与不确定项（对应 dossier §7.10，写作时必须处理）

- **R-7.10-01** 「蔚来 UWB+蓝牙+NFC 三合一数字钥匙」仅见新浪汽车等二手报道 —— https://auto.sina.cn/2026-07-18/detail-iniicyyt8275101.d.html —— [C]。取证结果：蔚来官方未取得技术说明；无法确认是否 CCC 3.0、是否有 SE 保护。
- **R-7.10-02** 小鹏 UWB 钥匙为论坛/短视频内容，官方未证实具体车型与安全实现；`open.xiaopeng.com` 403 使"小鹏开放座舱 API"一说无法向一手文档求证。
- **R-7.10-03** 比亚迪 i迪桥是**企业级 ESB 网关**（供应链/研发/智造），与"车控开放平台 / 车主 API"不是同一事物；未见其 OAuth 与数字钥匙能力。报告中必须区分，避免误导向"比亚迪车云授权=APIKey"的过度归纳。
- **R-7.10-04** 蔚来 Open NSC 文档停留在 2019 年且站点自述"建设中"，**不能代表蔚来当前车云安全架构**。
- **R-7.10-05** **9 家国内车企本次全部未取得关于"国密 SM2/SM3/SM4"、"mTLS 双向证书"、"证书轮换"、"HSM/SE/TEE"的任何官方一手来源** —— 报告中这些方向的结论一律写为"未找到公开来源 / 待补证"，禁止以行业常识冒充车企事实。
- **R-7.10-06** Xiaomi HyperOS Connect 宣称覆盖"人车家"，但 iot.mi.com 文档面向硬件模组厂商，未见小米汽车车云 API/鉴权细节。

---

## 90.10 未取证与不可达清单（[未验证] 与「未找到公开来源」集中列表）

本节把 source-dossier 中所有 `[未验证]`、`[C]`（正文未取到）、区域封锁、无 DNS、HTTP 403/000、以及「未找到公开来源」的条目**集中列出**，每条给出**原因**与**建议补证方式**（后者照录 dossier §8 覆盖度局限表）。本节的作用是把"披露缺口"显式化，防止下游读者把"本章没写"误读为"事实不存在"。

### 90.10.1 国际标准/法规正文不可达

| 台账编号 | 对象 | 等级 | 原因 | 建议补证方式 |
|---|---|---|---|---|
| R-1.4-01 | ISO/SAE 21434:2021 正文 | [未验证] | iso.org 被 Cloudflare 拦截 | 通过标准购买渠道或 SAE 页面补 |
| R-1.4-03 | ISO 24089:2023 正文 | [未验证] | iso.org Cloudflare 拦截 | 同上 |
| R-1.4-04 | UN R155/R156 条款与时间表 | [未验证] | unece.org 被 Cloudflare 全站拦截 | 恢复检索额度或用官方 PDF 直链 |
| R-1.4-05 | 欧盟 GDPR 正文 | [C] | EUR-Lex 返回 202 异步状态 | 重跑或换镜像渠道 |
| R-1.4-06 | 欧盟 Data Act 正文 | [C] | EUR-Lex HTTP 202 异步状态 | 同上 |
| R-6-15 | ISO 15118-2/-20 正文 | [未验证] | iso.org Cloudflare 拦截，标准号需复核 | 通过标准购买渠道补 |

### 90.10.2 规范/框架站点不可达或成员制

| 台账编号 | 对象 | 等级 | 原因 | 建议补证方式 |
|---|---|---|---|---|
| R-2.1-22 | UMA 2.0 | [未验证] | Kantara 站点 curl 超时 | 恢复检索额度后重取 |
| R-4-18 | AUTOSAR Classic Platform | [未验证] | autosar.org 超时 | 会员渠道获取规范正文 |
| R-4-19 | TCG TPM 2.0 | [未验证] | TCG 站点 403/超时 | 会员渠道获取规范正文 |
| R-4-20 | SHE 规范 | 未找到公开来源 | 成员制规范 | 会员渠道获取规范正文 |
| R-5-09 | IEEE 802.15.4z | [未验证] | 未取得可核验官方 URL | 恢复检索额度后补 |
| R-3-11 | 美国 SCMS | 未验证 | 未取得可核验官方 URL | 恢复检索额度或用官方 PDF 直链 |

### 90.10.3 厂商门户封锁/未取到

| 台账编号 | 对象 | 等级 | 原因 | 建议补证方式 |
|---|---|---|---|---|
| R-7.4-01~04 | BMW CarData / OAuth | [A 直接观测]（内容缺口） | developer.bmwgroup.com 占位页"no content deployed" | 换出口 IP 或代理后重跑 |
| R-7.5-01~02 | Rivian Fleet API | [A 直接观测]（内容缺口） | rivian.com CloudFront 区域封锁 | 换出口 IP |
| R-7.9-02 | 小鹏开放平台鉴权细节 | [A 站点存在，内容不可验证] | open.xiaopeng.com HTTP 403 拒绝服务 | 商务渠道申请沙箱账号 |
| R-7.9-07 | 华为鸿蒙座舱安全与数字车钥匙 | 未找到可验证公开来源 | developer.huawei.com 文档 JS 空壳，正文不可取 | 用带 JS 渲染的抓取（须登录） |
| R-7.9-01/05/06 | 理想/零跑/奇瑞 开发者入口 | 未找到公开来源 | 对应子域无 DNS 解析 | 商务渠道/专利与招标文件 |

### 90.10.4 主题方向的整体缺口（对应 dossier §8）

| 缺口方向 | 已检索对象 | 结果 | 建议补证方式 |
|---|---|---|---|
| 国内 9 家车企的车云通信安全（mTLS/国密） | 官网、开放平台、隐私政策、SRC 页 | 未找到公开一手来源 | 向车企发起 RFI / 采购安全白皮书 / 查专利与招标文件 |
| 国内车企 TEE/SE/HSM 实现 | 开发者门户、安全页 | 未找到公开一手来源 | 器件选型逆向、T-BOX 拆解、芯片厂 Design Win 公告 |
| 小鹏开放平台鉴权细节 | open.xiaopeng.com | HTTP 403 拒绝服务 | 商务渠道申请沙箱账号 |
| 华为鸿蒙座舱安全与数字车钥匙 | developer.huawei.com 文档 | JS 空壳，正文不可取 | 用带 JS 渲染的抓取（须登录） |
| BMW CarData / OAuth | developer.bmwgroup.com | 占位页"no content deployed" | 换出口 IP 或代理后重跑 |
| Rivian Fleet API | rivian.com / developer.rivian.com | CloudFront 区域封锁 | 换出口 IP |
| R155/R156 条款与时间表 | unece.org | Cloudflare 拦截 | 恢复检索额度或用官方 PDF 直链 |
| ISO 21434 / 24089 / 15118 正文 | iso.org | Cloudflare 拦截 | 通过标准购买渠道或 SAE 页面补 |
| Tesla 访问令牌 TTL | developer.tesla.com 已读页面 | 仅有刷新令牌 3 个月 + 24h 宽限 | 实机走一遍 token 响应读取 `expires_in` |
| UMA 2.0 / AUTOSAR / TPM 2.0 / SHE / IEEE 802.15.4z | 对应官网 | 站点不可达或成员制 | 会员渠道获取规范正文 |

### 90.10.5 方法论声明（写入报告正文，照录 dossier §8）

本次调研因检索工具额度耗尽，采用"权威 URL 直取 + 逐条标注证据等级"的方法。凡 `[A]` 条目为官方一手页面直接取证；`[B]` 为权威第三方；`[C]` 为二手；`[未验证]` 表示站点可达性确认但正文未取到。报告中另设"待补证清单"，明确区分"公开信息缺失"与"能力缺失"。

---

## 90.11 引用规范

本节定义报告正文的标注约定，用于把 90.0–90.10 的台账真正变成正文可执行的引用纪律。

### 90.11.1 正文标注约定

1. **每一条带事实性的断言**，必须在句末或段末标注其证据等级标签（`[A]/[B]/[C]/[未验证]/[合理推测]/未找到公开来源`）以及对应台账编号（如 `R-2.1-06`）。等级标签是强制项，台账编号是追溯便利项。
2. **措辞必须与等级匹配**（沿用 00-engagement-plan §3.1 的"允许的表述措辞"）：`[A]` 写"文档明载…"；`[B]` 写"据 …（第三方）…"；`[C]` 写"有报道称…（未经一手核实）"；`[未验证]` 写"尚未取证，URL 结构待复核"；`[合理推测]` 写"本报告判断…（推测，非事实）"；`未找到公开来源` 写"该方向未找到公开来源，不等同于能力缺失"。
3. **规范引用格式**：引用 RFC 时使用 `RFC 编号 §章节`（如 `RFC 8705 §3`）；引用国标时使用标准编号（如 `GB/T 47324-2026`）并可在括号内附台账编号。
4. **同一断言多源支撑**时，列出主源台账编号，其余作为佐证；`[A]` 与 `[C]` 并存时，以 `[A]` 为准，并对 `[C]` 加"未经一手核实"限定。

### 90.11.2 链接使用规则

1. 正文**不得新增**本章（以及 source-dossier.md）之外的任何 URL；需要引用某个来源时，从本章台账复制其 URL，不作任何改写。
2. **不得"修复" URL**：对 dossier 标记为不完整或结构待复核的 URL（如 `www.bmw.com`、`developer.rivian.com`、`open.xiaopeng.com/dev/`），正文照录其原始形态并保留对应等级；**不得**补全为主域名、不得补 `https://`、不得拼接路径。
3. 对 `[未验证]` 条目：正文**可以**指出"该 URL 结构或站点可达性已确认但正文未取到"，**不得**将其作为事实断言的依据。
4. 对「未找到公开来源」条目：正文**可以**写"未找到公开来源"，**不得**写"不存在/不支持/不具备"。
5. 厂商站点 URL 中出现变量占位（如 `$CLIENT_ID`、`<developer-domain.com>`）时，照录占位符，不替换为真实值。

### 90.11.3 不得引用未取证正文的规则

1. 凡以 `[未验证]` 或 `[C]`（正文未取到）标注的条目，**其正文内容不得被当作事实陈述**；只能出现在"待补证/局限说明"的语境中。
2. 凡与 R155/R156 **具体条款号、强制时间表、审核要求**相关的内容，本次**无一手来源**：正文只能标注「[未验证] 依通行公开认知」或改为待补证陈述，**不得给出条款编号**。
3. 凡涉及国内 9 家车企的"国密 / mTLS / 证书轮换 / HSM/SE/TEE"结论，正文只能写"未找到公开来源 / 待补证"，**禁止以行业常识冒充车企事实**（dossier §7.10 第 5 条）。
4. 单篇原文直接引用不得超过其所在章节篇幅的 5%（00-engagement-plan §3.2 第 5 条），以避免搬运替代分析。
5. 引用 Tesla 时，若涉及"访问令牌有效期约 8 小时"或"2023 年 Toyota/Tesla 漏洞披露事件"，一律不得写成事实（见 90.9.1 末段）。

---

## 90.12 版本与修订记录

### 90.12.1 版本表

| 版本 | 日期 | 变更摘要 | 维护人 |
|---|---|---|---|
| v1.0 | 2026-09-28 | 首版。建立 90.0–90.12 骨架，逐条转写 source-dossier 全部条目并标注证据等级，集中列出未取证清单与引用规范。 | TRA-1 参考台账工作流 |

### 90.12.2 维护规则（"就地覆盖、不新建版本"）

1. **就地覆盖**：本文件为唯一写入点。更新时**直接覆盖本文件**，**不新建** `90-references-v2.md` 之类的平行版本文件，避免同一台账出现多个"最新版本"。
2. **先底座后台账**：新增来源时，**先在 `docs/sources/source-dossier.md` 就地追加**（dossier 规定"发现新来源时就地追加到本文件，不另建文件"），**再**同步到本章；本章不承担来源收集职能。
3. **不新增 URL**：本章的任何一次修订，都**不得引入 dossier 之外的新 URL**。若某次修订需要引用新 URL，则修订的第一步必须是"把该 URL 就地追加到 dossier"，并注明其采集日期与证据等级。
4. **等级不得上调**：除经实际复取到正文并留下取证记录外，**不得**把 `[未验证]`/`[C]` 上调为 `[A]`/`[B]`。等级的任何变更都必须能指向对应的取证动作（日期 + 方式 + 结果）。
5. **缺口只增不减**：90.10 的未取证清单在未实际补证前**不得删除条目**；补证成功后，将该条目从 90.10 移入对应正文章节，并在 90.12.1 版本表登记变更摘要。
6. **修订登记**：每次修订在 90.12.1 版本表新增一行，注明版本、日期、变更摘要与维护人；变更摘要应可对应到具体台账编号段。

### 90.12.3 与其他文件的关系

- **上游唯一事实底座**：`docs/sources/source-dossier.md`（本章全部条目的来源）。
- **证据分级与红线口径**：`docs/00-engagement-plan.md` §3.1（六级证据分级）、§3.2（写作红线）、§6.4（兜底投递）。
- **本章角色**：把上述两者中"来源"与"纪律"的部分，转化为一条条可核验、可追溯、可复核的台账条目，服务于 AC-7（信源可靠、逐条标注参考资料）与 AC-11（中立性红线）。

---

（本章为纯台账章节，不含任何 dossier 之外的新增 URL；全部条目均逐字转写自 `docs/sources/source-dossier.md`，证据等级原样保留，未取证条目一律照录其未取证状态。）
