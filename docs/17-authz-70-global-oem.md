# 授权与访问控制 · 国际新能源车企实践分析

> **文件编号**：`17-authz-70-global-oem.md`
> **所属工作流**：WF-5（授权与访问控制 · 国际车企实践，5 家）
> **覆盖验收标准**：AC-2（授权章节 ≥300K 字符的组成部分）、AC-5（国际 ≥5 家逐家拆解）、AC-7（信源可靠并标注等级）、AC-11（客观中立）
> **证据底座**：`docs/sources/source-dossier.md`（唯一事实底座）
> **编制**：Trail of Bits Security · Reverse Engineering Lead
> **版本**：v1.0 · 生效 2026-09-28
> **阅读提示**：本章全部事实后紧跟 `—— 来源名称 —— URL —— [等级]`。等级口径沿用审计计划 §3.1：`[A]` 一手官方文档、`[B]` 权威第三方、`[C]` 二手、`[未验证]` 站点可达但正文未取到、`[合理推测（本报告判断）]`、`未找到公开来源`。凡本报告无法在信源档案中定位到对应条目的断言，一律标记为 `未找到公开来源`，**绝不以行业常识填充**（写作红线 §3.2.3）。

---

## 17.0 本章方法与覆盖度声明

### 17.0.1 本章的定位：把两类"可读文档"当作标尺，而非清单

本章研究对象为五家国际新能源车企——Tesla（特斯拉）、Mercedes-Benz（梅赛德斯-奔驰）、Volkswagen Group / CARIAD（大众集团／软件子公司 CARIAD）、BMW（宝马）、Rivian。与国内车企章节（`16-authz-60-cn-oem.md`）相比，本章的写作目标不是"每家企业平均分配篇幅"，而是**识别出其中文档公开度最高、机制可被逐条复现的实现，将其规范化为"行业标尺"**，再用标尺去度量其余各家。

审计计划 §4.5 已确立"对标基准法"：以 **Tesla Fleet API**（公开文档最完整）与 **Mercedes-Benz Developer Platform** 为"已公开实现的标尺"，其他车企与通用方案均与此对标，量化差异（scope 命名空间、令牌 TTL、轮换策略、同意模型、密钥模型）—— 来源：审计计划 §4.5 —— `docs/00-engagement-plan.md` —— [A，本项目内部方法论文档]。

因此，本章的篇幅与深度分布是**刻意不对称**的：

- Tesla 一节（§17.2）为本章最重要的技术剖析，逐机制拆解到"可控工程复现"的粒度；
- Mercedes-Benz 一节（§17.3）次之，聚焦其 OAuth 实现细节与 scope 命名空间约定；
- CARIAD（§17.4）仅有企业自述口径可引；
- BMW（§17.5）与 Rivian（§17.6）本次**未能取证**，按审计计划 §3.1 的 `未找到公开来源` 口径诚实处理，并单列补证动作。

### 17.0.2 取证条件与本次覆盖度声明

本章写作的前提条件必须显式声明，因为它决定了全部结论的可信度边界。信源档案 §0"采集方法与局限"记载：采集日期 2026-09-28，执行方式为 `terminal + curl` 与浏览器直连权威站点；**检索工具 `web_search` / `web_extract` 全程返回额度耗尽（Firecrawl 402/429），本次调研无法做开放网络发现，只能"直取已知权威 URL"**；公开搜索引擎在本运行环境同样不可用（Bing 地理重定向、Baidu/Sogou/360 验证码、Google 机器人墙、DuckDuckGo 验证码）；`bmw.com` / `bmwgroup.com` / `rivian.com` 被 Akamai/CloudFront 区域封锁 —— 来源：信源档案 §0 —— `docs/sources/source-dossier.md` —— [A，本项目内部采证记录]。

由此产生的覆盖度偏置是：**证据密度向"文档公开可达"的企业倾斜**，Tesla、Mercedes-Benz 证据最厚，BMW、Rivian 证据薄弱。信源档案 §0 对此有强制写作纪律：**"未找到公开来源" = 本次披露缺口，绝不等于能力缺口，不得反向推断为"该企业没有该能力"** —— 来源：信源档案 §0 —— 同上 —— [A]。

本任务执行说明（如实声明）：本次写作在 **web_search / web_extract 完全不可用**的条件下进行，`terminal + curl` 直取档案中已列 URL 为可选项但未被要求执行；本章全部事实仅来自信源档案中已核实的条目，**未引入任何档案之外的新 URL、数字或条款号**。凡国际标准正文（GDPR、欧盟 Data Act、UN R155/R156、ISO/SAE 21434）在本次取证中"站点可达性已确认但正文未取到"者，本章一律标 `[未验证]` 或 `未找到公开来源`，且**不给条款编号**（对齐信源档案 §1.4 写作纪律提示）。

### 17.0.3 BMW / Rivian 未取证的诚实说明

在本章动笔前必须先把两家"缺证据"的企业交代清楚，避免读者把"本章对 BMW/Rivian 着墨少"误读为"两家技术能力弱"。

**BMW**：本次取证结果为——`https://developer.bmwgroup.com/` 的 DNS 可解析（160.46.244.54），但返回的是 Apache 占位页，页面文本为 "BMW Group – no content deployed … This project didn't deploy any content yet"，`Last-Modified` 头为 2026-04-27，且**未提供 CarData / OAuth 任何文档**；`https://crd.bmwgroup.com/` 无法解析；`https://b2b-developer.bmwgroup.com/` 超时；`www.bmw.com` / `www.bmwgroup.com` 从本网络被区域封锁（HTTP 000 / 边缘封锁）；`www.bmwgroup.com/en/innovation/vehicle-data.html` 经浏览器返回站点自身 404；`https://b2b.bmw.com` 虽可达，但为**供应商采购门户**（purchasing / logistics 登录），并非车辆数据开发者 API 门户 —— 来源：信源档案 §7.4 —— `docs/sources/source-dossier.md` —— [A，直接观测]。

**Rivian**：本次取证结果为——`https://rivian.com` 从本出口返回 Amazon CloudFront 403，正文为 "The CloudFront distribution is configured to block access from your country"；`developer.rivian.com` 无 DNS 解析；`api.rivian.com` 可解析（13.35.190.19）但为 App 后端，非公开开发者门户 —— 来源：信源档案 §7.5 —— 同上 —— [A，直接观测]。

**结论**：BMW 与 Rivian 在本次调研中属于**"披露缺口"而非"能力缺口"**（信源档案 §0 表述）。本章 §17.5 / §17.6 把上述观测事实如实记录，并给出补证动作清单（换出口 IP、代理重跑、RFI），而不对两家的授权与访问控制能力下任何否定性判断。这是 AC-11 中立性红线的直接要求 —— 来源：审计计划 §3.2.4 —— `docs/00-engagement-plan.md` —— [A]。

### 17.0.4 本章结构导航

| 小节 | 主题 | 主证据强度 |
|---|---|---|
| 17.1 | 国际车企授权治理的合规底座（GDPR / Data Act / R155-R156） | 多为 [未验证]／未找到公开来源 |
| 17.2 | Tesla Fleet API 深度剖析 | [A] 厚 |
| 17.3 | Mercedes-Benz Developer Platform 剖析 | [A] 厚 |
| 17.4 | Volkswagen Group / CARIAD | [A，企业自述口径] 薄 |
| 17.5 | BMW（未取证） | [A，直接观测] |
| 17.6 | Rivian（未取证） | [A，直接观测] |
| 17.7 | 五家横向对照矩阵（≥12 维度） | 综合 |
| 17.8 | 国际路线的方法论启示 | [合理推测] |
| 17.9 | 待补证清单 | 综合 |

---

## 17.1 国际车企授权治理的合规底座

### 17.1.1 本节的取证限制（必须先读）

讨论国际车企的授权治理，绕不开三部法律/标准文本：欧盟 **GDPR**（General Data Protection Regulation，通用数据保护条例）、欧盟 **Data Act**（数据法案，涉及互联产品与车辆数据的访问权）、联合国 **UN R155 / R156**（车辆网络安全管理体系 CSMS 与软件更新管理体系 SUMS）。这三者构成"授权与访问控制为什么必须做、做到什么程度"的合规底座。

但本次取证对三者的结果都不理想，必须逐条交代（对齐信源档案 §1.4 与审计计划 §3.2.3）：

- **GDPR**：欧盟法规编号为 Regulation (EU) 2016/679，EUR-Lex 官方页 `https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng`，本次返回 HTTP **202 异步状态，正文未取到** —— 来源：信源档案 §1.4 —— `docs/sources/source-dossier.md` —— [C]。因此本章**不引用 GDPR 任何条款号**，只能按"通行公开认知"描述其性质为"以同意（consent）为合法性基础之一的个人数据保护框架"，并标记 `[未验证]`。
- **欧盟 Data Act**：编号为 Regulation (EU) 2023/2854，EUR-Lex 页 `https://eur-lex.europa.eu/eli/reg/2023/2854/oj`，本次返回 HTTP **202**，正文未取到 —— 来源：信源档案 §1.4 —— 同上 —— [C]。其通行公开认知是"赋予互联产品用户对其所生成数据的访问权与可携权"，但**具体条款、适用范围、生效时间表本次均无一手来源**，一律标 `[未验证：依通行公开认知]`。
- **UN R155 / R156**：unece.org 被 Cloudflare 全站拦截，URL 结构需复核。R155 通行认知为"网络安全管理体系（CSMS）"，R156 为"软件更新管理体系（SUMS）" —— 来源：信源档案 §1.4 —— 同上 —— [未验证]。信源档案 §1.4 有明确写作纪律：**"涉及 R155/R156 的具体条款号、强制时间表、审核要求时，本次无一手来源。凡引用必须标注「[未验证] 依通行公开认知」或改为待补证陈述，不得给出条款编号。"**

**本节写作承诺**：下文凡涉及上述三者的"要求域"描述，均为**性质层面的通行公开认知**，不带条款号、不带时间表、不带具体审核要求；凡进入本节表格的每一行，均标 `[未验证]` 或 `未找到公开来源`。

### 17.1.2 GDPR 视角下的"授权同意"与车企同意的耦合

尽管 GDPR 正文未取到，**车企侧对 GDPR 的公开表态**却是一手可引的 [A] 级证据。Mercedes-Benz 开发者平台首页原文写明：**"The trust and consent of our vehicle customers are at the heart of our business – ensuring GDPR compliance and enabling secure, reliable data you can depend on."**（"我们车辆客户的信任与同意是我们业务的核心——确保 GDPR 合规，并提供您可以依赖的安全、可靠数据。"）—— 来源：Mercedes-Benz Developer Platform 首页 —— `https://developer.mercedes-benz.com/` —— [A]。

这句话的工程含义值得展开：它把"客户同意"与"GDPR 合规"绑定为同一件事，而 OAuth 授权码流程正承担了"采集并留存终端用户同意"的技术职责。Mercedes 文档对此的表述（意译）是：部分 API 提供燃油状态、车门锁状态等数据，**属 GDPR 意义上的个人数据，因此需要终端用户同意**，平台自称使用"standard OAuth 2.0" —— 来源：Mercedes-Benz 授权码流文档 —— `https://developer.mercedes-benz.com/get-started/oauth/authorization-code-flow` —— [A]。

由此可以抽出一条清晰的因果链（**本报告判断，见 §17.8**）：**GDPR 的"同意"要求 → 需要可撤回、可细粒度、可留痕的授权机制 → 车企被迫把 OAuth scope 设计与"车主同意界面"耦合起来 → 授权与访问控制从"技术实现"升格为"合规义务"**。这条链解释了为什么国际车企的公开 scope 文档普遍比国内车企厚——scope 不只是权限位，还是**向监管者与车主举证"我们取得了哪些同意"的凭证**。

### 17.1.3 欧盟 Data Act 对"车辆数据访问权"的通行认知与本报告的处理

Data Act 的通行公开认知是：赋予互联产品（connected products，含车辆）的使用者对其所产生数据获得访问与再使用的权利，并允许用户把数据直接分享给第三方。若该认知成立，它将在授权层产生一项硬性派生需求——**平台必须提供一个"用户主导、可由用户转授给第三方"的数据访问通道**，而这恰好对应 OAuth 授权码流程的 `authorization_code` 将"资源所有者"设为真人车主的设计。

但请注意本报告的取证纪律：**Data Act 正文本次返回 HTTP 202，未取到，故本条仅为通行认知，标 [未验证：依通行公开认知]** —— 来源：信源档案 §1.4 —— `docs/sources/source-dossier.md` —— [C/未验证]。**本报告不引用 Data Act 任何条款编号，也不引用其生效时间表。** 待补证动作见 §17.9。

值得记录的对照现象（**本报告判断，非事实**）：Tesla Fleet API 的"车主侧 revoke consent 端点"与 Mercedes 的"同意界面展示 scope 与 purpose URL"，在**功能形态上**与 Data Act 所描述的"用户主导数据访问"高度同构。但**这只能说两者形态相容，不能断言是 Data Act 的直接合规驱动**——因为 Data Act 正文未取证，因果归属无法证实。

### 17.1.4 UN R155/R156 的授权管理面（性质层面）

在无一手正文的前提下，本报告只能描述 R155/R156 与授权管理的**性质关联**，并全部标 `[未验证]`：

| 法规 | 通行认知的体系对象 | 与"授权与访问控制"的性质关联（本报告判断） | 证据等级 |
|---|---|---|---|
| UN R155 | 网络安全管理体系（CSMS） | 要求整车企业建立覆盖全生命周期的网络安全流程；授权/身份管理属其"访问控制"要求域的组成部分 | [未验证：依通行公开认知] |
| UN R156 | 软件更新管理体系（SUMS） | 要求软件更新过程的完整性、真实性与授权可追溯；OTA 下发权限属其"更新授权"要求域 | [未验证：依通行公开认知] |
| ISO/SAE 21434 | 道路车辆网络安全工程 | 提供威胁分析与风险评估（TARA）方法论，是 R155 的技术支撑标准之一 | [未验证：编号与年份为通行共识，正文未取到] |

来源：信源档案 §1.4 —— `docs/sources/source-dossier.md` —— [未验证]。

**本报告明确声明**：上述表格**不含任何条款号、时间表、审核要求**，因为本次无一手来源。信源档案 §1.4 与审计计划 §3.2.3 均禁止以记忆填补此类缺口。凡需引用 R155/R156 具体条款的场景，一律进入 §17.9 待补证清单。

### 17.1.5 合规底座小结

本节可安全输出的结论只有两条，且都可溯源：

1. **车企侧的公开表态确证"同意"与"合规"的耦合**：Mercedes-Benz 开发者平台首页原文把"信任与同意"与"GDPR 合规"并列为业务核心 —— 来源：Mercedes-Benz 开发者平台首页 —— `https://developer.mercedes-benz.com/` —— [A]。
2. **国际法规/标准的正文本次普遍未取到**：GDPR、Data Act、R155、R156、ISO/SAE 21434 均标 `[未验证]`／`[C]`，**不得作为条款级依据** —— 来源：信源档案 §1.4 —— 同上 —— [C/未验证]。

据此，本章后续各节的机制剖析**不依赖法规条款**，而全部建立在**车企一手开发者文档**这一 [A] 级证据之上。这也正是本章标题取"实践分析"而非"合规分析"的原因——合规映射交由 WF-6 的 `18-authz-80-compliance-audit.md` 处理。

---

## 17.2 Tesla Fleet API 深度剖析

> 本节为本章最重要的技术剖析，目标是把 Tesla Fleet API 拆到"可被其他车企逐条对标、可被工程团队复现"的粒度。
> 全部事实来自信源档案 §7.1（全部 [A]，来源 developer.tesla.com）—— 来源：信源档案 §7.1 —— `docs/sources/source-dossier.md` —— [A]。

### 17.2.1 三类令牌模型（third-party / partner / third-party-for-business）与信任边界

Tesla Fleet API 的第一层设计是**令牌分类**。文档要求所有请求携带请求头 `Authorization: Bearer <token>` —— 来源：Tesla Fleet API 认证总览 —— `https://developer.tesla.com/docs/fleet-api/authentication/overview` —— [A]。但其关键不在"Bearer"这一载体，而在于**同一个载体背后有三类语义完全不同的令牌**：

- **third-party token**（第三方令牌）：代表车主（resource owner）行事的令牌，语义上"这是某个车主授权某个第三方应用做的事"。
- **partner token**（合作伙伴令牌）：代表合作伙伴（通常是企业级/商业开发者）行事的令牌，**不绑定单个车主的逐次同意**。
- **third-party-for-business token**（面向企业业务的第三方令牌）：文档列为第三类令牌名称 —— 来源：同 `authentication/overview` 页 —— [A]。

**信任边界分析（本报告判断）**：三类令牌的价值在于把"谁在授权"与"能做什么"解耦成两个维度——

- 第一维度是**主体身份**：是"代车主行事的应用"（third-party）还是"企业自身身份"（partner）。
- 第二维度是**同意的取得方式**：third-party 令牌必须走车主同意的授权码流程；partner 令牌走的是企业契约路径，不进入逐车主同意模型。

这一解耦直接决定了**后续所有 scope 的可授予主体**（见 §17.2.2 表格的"可授予主体"列）。最典型的后果是 `vehicle_specs` 与 `vehicle_pricing_info` **仅 Partner Token 可用**，即这两类资源从设计上就**退出了"逐车主同意"模型** —— 来源：Tesla Fleet API 认证总览 —— `https://developer.tesla.com/docs/fleet-api/authentication/overview` —— [A]。

信任边界可以用 ASCII 图表达如下：

```
                      Tesla Fleet API 令牌信任边界（本报告整理）
  ┌─────────────────────────────────────────────────────────────────────┐
  │  资源所有者（车主）          合作伙伴/企业（Partner）                  │
  │       │                            │                                 │
  │       │ 授权码流程（/authorize）   │ 企业契约/注册（Partner Account） │
  │       ▼                            ▼                                 │
  │  ┌──────────────┐            ┌──────────────┐                        │
  │  │ third-party  │            │ partner       │                       │
  │  │ token        │            │ token         │                       │
  │  └──────┬───────┘            └───────┬───────┘                       │
  │         │                            │                               │
  │         │ 进入逐车主同意模型          │ 不进入逐车主同意模型           │
  │         │                            │（vehicle_specs /             │
  │         │                            │  vehicle_pricing_info 例外）  │
  │         └────────────┬───────────────┘                              │
  │                      ▼                                               │
  │              Fleet API 资源（车辆/能源/用户/企业）                    │
  └─────────────────────────────────────────────────────────────────────┘
        第三类：third-party-for-business token（面向企业业务的第三方令牌）
```

**工程含义**：这三类令牌的存在说明，一个成熟的"车-云第三方授权"实现**不能只有一条授权路径**。它必须至少同时支持：(1) 面向个人车主的"同意驱动"路径；(2) 面向企业客户的"契约驱动"路径。只做前者，企业级批量场景（车队、保险、充电计费）无法落地；只做后者，则违反 GDPR 意义上的"个人数据需终端用户同意"。Tesla 把两条路径**用令牌类型显式区分**，是本模型最值得对标的一点 —— [合理推测（本报告判断）]。

### 17.2.2 Scope 全清单与资源粒度（12 个 scope 逐个分析）

Tesla Fleet API 公开了 **12 个 scope**（scope 即 OAuth 权限范围；本报告首次出现处给中英对照）：`openid`、`offline_access`、`user_data`、`vehicle_device_data`、`vehicle_location`、`vehicle_cmds`、`vehicle_charging_cmds`、`vehicle_specs`、`vehicle_pricing_info`、`energy_device_data`、`energy_cmds`、`enterprise_management` —— 来源：Tesla Fleet API 认证总览 —— `https://developer.tesla.com/docs/fleet-api/authentication/overview` —— [A]。

下表逐个分析这 12 个 scope 的覆盖资源、可授予主体、是否需车主同意，以及粒度设计评价（评价栏为 **本报告判断**）：

| # | scope | 覆盖资源（文档明载） | 可授予主体 | 是否需车主同意 | 粒度设计评价（本报告判断） |
|---|---|---|---|---|---|
| 1 | `openid` | "Sign in with Tesla"——允许车主用 Tesla 凭证登录第三方应用 | 第三方应用（对车主） | 是（登录即同意动作） | 对应 OpenID Connect Core 1.0 的身份层，与授权分离，设计正确 —— [A] |
| 2 | `offline_access` | 获取刷新令牌，避免重复登录 | 第三方应用 | 是 | 对应 OIDC 离线访问语义，是把"会话"与"长期授权"分开的关键 scope |
| 3 | `user_data` | 联系方式、家庭住址、头像、推荐信息 | 第三方应用 | 是 | 粒度偏粗：把"联系方式"与"家庭住址"捆在一起，属于一类"账户画像"资源包 |
| 4 | `vehicle_device_data` | 实时数据、服务历史、服务预约、服务沟通、可升级项、附近超充、所有权信息 | 第三方应用 | 是 | 粒度偏粗且覆盖面广（从遥测到"所有权信息"），是位置之外最敏感的一包 |
| 5 | `vehicle_location` | 精确与粗略位置 | 第三方应用 | 是 | **双层收窄的典型**：即便授予，`hide_private` 共享车仍拒绝返回位置（见下） |
| 6 | `vehicle_cmds` | 添加/移除驾驶员、Live Camera 访问、解锁、唤醒、远程启动、预约软件更新 | 第三方应用 | 是 | 高风险 scope：含"添加/移除驾驶员"（可扩权）与"Live Camera"（可实时窥视） |
| 7 | `vehicle_charging_cmds` | 充电历史、计费金额、充电地点、预约/开始/停止充电 | 第三方应用 | 是 | 把"读充电历史/计费"与"写充电动作"合并在一个 scope，读写未分离 |
| 8 | `vehicle_specs` | 车辆规格 | **仅 Partner Token** | **否——对任意车辆无需车主授权** | **授权控制例外（High）**：退出逐车主同意模型，见 §17.2.10 |
| 9 | `vehicle_pricing_info` | 车辆定价信息 | **仅 Partner Token** | **否** | 同上，同属 High 级例外 |
| 10 | `energy_device_data` | 能源设备（Powerwall 等）数据 | 第三方应用 | 是 | 把授权域从"车"扩展到"能源产品"，是少见的跨产品线授权统一 |
| 11 | `energy_cmds` | 能源设备命令（如调度充放电） | 第三方应用 | 是 | 与 `energy_device_data` 读写分离处理恰当，注意与车侧 6/7 的不一致 |
| 12 | `enterprise_management` | 企业管理（车队级管理） | Partner/企业 | 否（契约路径） | 面向企业租户的"管理面" scope，是 B 端与 C 端授权分层的关键 |

来源：Tesla Fleet API 认证总览（scope 名称与覆盖资源为该页文档原文）—— `https://developer.tesla.com/docs/fleet-api/authentication/overview` —— [A]。表中"粒度设计评价"列为本报告判断 —— [合理推测（本报告判断）]。

**逐点机制分析：**

**(1) `openid` 与 `offline_access` 的定位。** 文档明确 `openid` = "Sign in with Tesla"（允许车主用 Tesla 凭证登录第三方应用）；`offline_access` = 获取刷新令牌以免重复登录 —— 来源：同上 —— [A]。这两个 scope 是 **OIDC（OpenID Connect）标准 scope**，与特斯拉自定义的 `vehicle_*` / `energy_*` / `user_data` / `enterprise_management` 形成清晰分层：**前两个管"身份与会话"，后十个管"资源与动作"**。这是"认证与授权分离"的良好落地（对齐 OpenID Connect Core 1.0 的 UserInfo 与授权分离设计）—— [合理推测（本报告判断）]。

**(2) `vehicle_location` 的双层收窄（本报告对标的正面案例）。** 文档明载：`vehicle_location` 覆盖**精确与粗略位置**；此外，**带 `granular_access.hide_private=true` 的车辆共享，即使被授予 `vehicle_location`，也拿不到任何位置，且无法流式传输位置字段** —— 来源：Tesla Fleet API 认证总览 —— `https://developer.tesla.com/docs/fleet-api/authentication/overview` —— [A]。

这是全章最值得对标的一处设计。它意味着**授权被授予（granted）不等于资源可访问（accessible）**，中间还叠了一层**资源级的策略收窄（granular access / hide_private）**。工程上，这一"第二层"必须独立于 OAuth 授权层实现——即在 API 网关/资源服务器侧，**每次取位置都要重新做一次"该车是否 hide_private"的判定**，而不能只信 token 里的 scope。审计计划 §3.3 已把此点归为 **Informational→正面控制案例**：**"双层授权控制"的良好实践，建议其他车企对标** —— 来源：审计计划 §3.3 —— `docs/00-engagement-plan.md` —— [A]。

从 STRIDE 视角（**本报告判断**）：`hide_private` 收窄的是 **Information Disclosure（信息泄露）** 与 **Elevation of Privilege（越权）** 两类威胁——它切断了"应用一旦拿到 `vehicle_location` 就能追踪所有共享车"的横向扩散路径。Fleet Telemetry 侧对应字段被拒返回 **HTTP 403 "location access not granted"**，见 §17.2.7 —— 来源：Tesla Fleet Telemetry 文档 —— `https://developer.tesla.com/docs/fleet-api/fleet-telemetry` —— [A]。

**(3) `vehicle_cmds` 的高风险内容。** 该 scope 覆盖**添加/移除驾驶员、Live Camera 访问、解锁、唤醒、远程启动、预约软件更新** —— 来源：Tesla Fleet API 认证总览 —— 同上 —— [A]。其中两点需要特别标注（**本报告判断**）：
- "**添加/移除驾驶员**"是一个**可扩权动作**——获此 scope 的应用理论上可通过"添加驾驶员"改变车辆的用户集合，其影响面大于单次解锁；
- "**Live Camera 访问**"是**实时视觉数据**，一旦泄露即场景级信息暴露，其敏感度高于普通遥测。

因此 `vehicle_cmds` 在风险分级上应高于"读类" scope。这提示一个通用设计原则：**scope 划分不应只按"资源对象"（vehicle），还应按"读/写"与"是否可扩权"细分层级**。Tesla 在此处把大量动作合并进一个 scope，属**粒度偏粗但以虚拟密钥二次校验补偿**的取舍（见 §17.2.6 与 §17.2.10）。

**(4) `vehicle_specs` / `vehicle_pricing_info` 的授权控制例外。** 文档明载这两个 scope **仅 Partner Token 可用**，且 `vehicle_specs` **对任意车辆可用、无需车主授权** —— 来源：Tesla Fleet API 认证总览 —— 同上 —— [A]。这是**唯一明确退出"逐车主同意"模型的车辆资源访问路径**。审计计划 §3.3 已将其判定为 **High 级授权控制例外**：**"需在报告中显式标注为'退出逐车主同意模型'的路径，并建议以契约与审计补偿"** —— 来源：审计计划 §3.3 —— `docs/00-engagement-plan.md` —— [A]。本报告在 §17.2.10 的 Trade-off 表中再次显式标注。

**(5) scope 粒度总评（本报告判断）。** Tesla 的 12 scope 覆盖了 **身份（openid）→ 会话（offline_access）→ 用户画像（user_data）→ 车辆数据（vehicle_device_data/vehicle_location）→ 车辆动作（vehicle_cmds/vehicle_charging_cmds）→ 规格价格（vehicle_specs/vehicle_pricing_info）→ 能源（energy_device_data/energy_cmds）→ 企业管理（enterprise_management）** 八个层级，覆盖完整；但**读/写分离不彻底**（`vehicle_device_data` 为纯读，而 `vehicle_cmds` / `vehicle_charging_cmds` 读写混装），且**存在两个可绕过车主同意的 Partner 专属 scope**。综合看，Tesla 的 scope 模型属"**覆盖广、粒度中、以密钥二次校验补强**"的工程取舍，而非学术意义上的最细粒度模型——若对齐 OAuth 2.0 Rich Authorization Requests（RFC 9396，`authorization_details` 结构化权限对象）所能表达的"资源级授权"粒度，Tesla 仍有细化空间 —— 来源：RFC 9396 —— `https://www.rfc-editor.org/rfc/rfc9396.txt` —— [A]。

### 17.2.3 授权码流程逐步剖析

#### 17.2.3.1 授权服务器元数据（Discovery）

Tesla 的授权服务器元数据发布于：
`https://fleet-auth.prd.vn.cloud.tesla.com/oauth2/v3/thirdparty/.well-known/openid-configuration`
—— 来源：Tesla Fleet API 认证总览 —— `https://developer.tesla.com/docs/fleet-api/authentication/overview` —— [A]。

这一条对应两项规范：**OIDC Discovery 1.0**（`/.well-known/openid-configuration`）与 **RFC 8414**（OAuth 2.0 Authorization Server Metadata，`/.well-known/oauth-authorization-server`）—— 来源：信源档案 §2.1 —— `docs/sources/source-dossier.md` —— [A]。其工程价值在于：**客户端无需硬编码端点，可通过一次 GET 自动发现 authorize/token 端点、支持的 scope、JWKS 公钥位置**。对第三方开发者而言，这降低了"对接出错到无法授权"的概率；对 Tesla 而言，这让**密钥轮换、端点迁移可以在不破坏既有集成的情况下完成**（**本报告判断**）。

注意元数据 URL 中的 `thirdparty` 路径段：它暗示**按令牌类型划分元数据命名空间**——thirdparty 的元数据独立于 partner/for-business —— [合理推测（本报告判断）]。

#### 17.2.3.2 授权端点与参数

文档给出的授权端点为 `https://auth.tesla.com/oauth2/v3/authorize` —— 来源：Tesla Fleet API 第三方令牌文档 —— `https://developer.tesla.com/docs/fleet-api/authentication/third-party-tokens` —— [A]。

**必填参数**（文档明载）：`response_type=code`、`client_id`、`redirect_uri`、`scope`、`state`（文档描述 `state` 为"用于校验的随机值"）—— 来源：同上 —— [A]。

**可选参数**：`nonce`（"用于防重放的随机值"）—— 来源：同上 —— [A]。

一个完整的授权请求报文（按文档参数拼装，实际值须以开发者注册信息为准）：

```
GET /oauth2/v3/authorize?
    response_type=code
    &client_id=$CLIENT_ID
    &redirect_uri=https%3A%2F%2Fdeveloper.example.com%2Fcallback
    &scope=openid%20offline_access%20vehicle_device_data%20vehicle_cmds
    &state=$RANDOM_STATE
    &nonce=$RANDOM_NONCE
    &audience=https%3A%2F%2Ffleet-api.prd.na.vn.cloud.tesla.com
Host: auth.tesla.com
```

（参数清单来源：Tesla Fleet API 第三方令牌文档 —— `https://developer.tesla.com/docs/fleet-api/authentication/third-party-tokens` —— [A]；`audience` 参数见 §17.2.3.4。）

**`state` 的作用剖析（本报告判断）**：`state` 是 OAuth 2.0 核心的 **CSRF（Cross-Site Request Forgery）防护**手段——客户端生成一个不可预测的随机值，授权服务器原样回传，客户端在回调时比对。若攻击者能构造一个"把受害者账号绑定到攻击者应用"的授权请求，`state` 不匹配即可拦截。文档仅描述为"用于校验的随机值"，未展开其威胁模型 —— [A]（文档）+ [合理推测（本报告判断）]（威胁模型）。

**`nonce` 的作用剖析（本报告判断）**：`nonce` 属 OIDC 层，绑定 `id_token` 与本次授权请求，防止 **ID Token 重放**。文档描述为"用于防重放的随机值"，与实际语义一致 —— 来源：Tesla Fleet API 第三方令牌文档 —— 同上 —— [A]。

#### 17.2.3.3 三个附加参数：授权流程的"可控性旋钮"

Tesla 在 `/authorize` 上提供了三个**非标准但极具工程价值**的可选参数 —— 来源：Tesla Fleet API 第三方令牌文档 —— `https://developer.tesla.com/docs/fleet-api/authentication/third-party-tokens` —— [A]：

- `prompt_missing_scopes=true`：**对尚未授权的 scope 再次提示**（即"增量授权"——车主此前已同意的 scope 不再重复展示，只对新增部分再次征求同意）。
- `require_requested_scopes=true`：**必须授权全部请求 scope 才放行**（即"全有或全无"——若车主只同意部分 scope，则整个授权失败，不颁发部分权限的令牌）。
- `show_keypair_step=true`：**预告虚拟密钥配对第二步**（即在授权 UI 中提前展示"稍后还需配对虚拟密钥"这一步，见 §17.2.6）。

**机制级分析（本报告判断）**：这三个参数把"授权流程的严格程度"变成客户端可控的旋钮，其价值如下：

1. `prompt_missing_scopes` 解决的是**增量授权体验**问题。若无此参数，每次应用新增一个 scope 都得让车主重新走完整同意界面（重复展示已授权项会造成"同意疲劳"，反而降低安全性）。Tesla 的取舍是：**默认精确到"缺什么补什么"**，把重复同意降到最低。
2. `require_requested_scopes` 解决的是**部分授权导致的运行期失败**问题。若允许部分授权，应用拿到"半套权限"后运行到某一步才发现缺少 `vehicle_cmds`，会产生难以诊断的失败；强制全量授权则把"权限不足"提前到授权时刻暴露。代价是**同意率下降**（车主必须全同意）。
3. `show_keypair_step` 解决的是**两步式安全流程的用户预期管理**问题。Tesla 车控需要"OAuth 授权 + 虚拟密钥配对"两步，若不预告，车主在第二步会困惑"为什么装个应用还要配对密钥"。提前预告可提升配对完成率。

**与 §17.2.5 的联动**：`require_requested_scopes` 的"全有或全无"语义，与"**scope 缩减对既有刷新令牌兼容、但新增 scope 必须用 `prompt_missing_scopes=true` 重新授权**"形成一对不对称策略——**收权限容易（当场生效对后续令牌）、加权限难（必须车主再次出面）**。这是安全的默认方向（**本报告判断**）：扩权必须经车主，缩权可自动进行。

#### 17.2.3.4 令牌端点、主机分离与 audience 绑定

**主机分离**：令牌端点与 API 端点**分属不同主机**——
- 令牌端点：`POST https://fleet-auth.prd.vn.cloud.tesla.com/oauth2/v3/token`；
- 授权端点：`https://auth.tesla.com/oauth2/v3/authorize`；
- API 端点：`https://fleet-api.prd.na.vn.cloud.tesla.com`（示例 base URL）。
—— 来源：Tesla Fleet API 第三方令牌文档 —— `https://developer.tesla.com/docs/fleet-api/authentication/third-party-tokens` —— [A]。

文档还特别说明：`/token` 调用"来自应用服务器、适用不同的限流" —— 来源：同上 —— [A]。

**主机分离的工程含义（本报告判断）**：把 `auth.tesla.com`（面向车主的身份/同意主机）、`fleet-auth.prd.vn.cloud.tesla.com`（面向应用服务器的令牌主机）、`fleet-api.prd.na.vn.cloud.tesla.com`（面向应用服务器的资源主机）分置于不同主机，带来三重收益：

1. **限流域隔离**：`/token` 是低频、高价值的调用（每次换码/刷新一次），与高频的 API 调用（60 次/分）天然不同频。分离后可独立限流，避免"刷新风暴"打垮 API 网关。
2. **攻击面收敛**：面向车主的 `auth.tesla.com` 需要渲染同意 UI、承载车主登录，其攻击面（XSS/CSRF）性质与纯 API 主机不同；分离后二者互不污染。
3. **信任域切分**：`fleet-auth` 属"授权服务器"信任域，`fleet-api` 属"资源服务器"信任域——这正对应 OAuth 2.0 架构中 AS（Authorization Server）与 RS（Resource Server）的角色分离（RFC 6749）—— 来源：RFC 6749 —— `https://www.rfc-editor.org/rfc/rfc6749.txt` —— [A]。

**audience 绑定**：`/token` 换码参数含 `grant_type=authorization_code`、`client_id`、`client_secret`、`audience`（**必须是 Fleet API base URL**，如 `https://fleet-api.prd.na.vn.cloud.tesla.com`）、`redirect_uri`、`scope` —— 来源：Tesla Fleet API 第三方令牌文档 —— `https://developer.tesla.com/docs/fleet-api/authentication/third-party-tokens` —— [A]。

**audience 绑定的机制意义（本报告判断）**：Requirement 是"audience 必须是 Fleet API base URL"，这把**签发出来的令牌在签发生成就钉死在某个资源服务器域上**。攻击者即使窃取令牌，也无法把该令牌重放到其他域（例如其他租户域或第三方伪造域），因为资源服务器会校验 `aud` 是否等于自己。这与 **RFC 9068（JWT Profile for OAuth 2.0 Access Tokens）中"必须校验 `aud`/`iss`/`exp`"的要求**同向 —— 来源：RFC 9068 —— `https://www.rfc-editor.org/rfc/rfc9068.txt` —— [A]。此外，Tesla 同时存在 `.na.`（北美）等区域段，说明 audience 实际承载了**区域绑定**语义——令牌跨区域不可用 —— [合理推测（本报告判断）]。

一个 `/token` 换码请求的例子（结构按文档参数拼装）：

```http
POST /oauth2/v3/token HTTP/1.1
Host: fleet-auth.prd.vn.cloud.tesla.com
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&client_id=$CLIENT_ID
&client_secret=$CLIENT_SECRET
&audience=https%3A%2F%2Ffleet-api.prd.na.vn.cloud.tesla.com
&redirect_uri=https%3A%2F%2Fdeveloper.example.com%2Fcallback
&scope=openid+offline_access+vehicle_device_data+vehicle_cmds
&code=$AUTHORIZATION_CODE
```

（参数清单来源：Tesla Fleet API 第三方令牌文档 —— 同上 —— [A]。）

**文档明确"认证端点不计费"**：文档陈述"authentication endpoints are not billed"（认证端点不计费）—— 来源：同上 —— [A]。这一条对开发者意义重大：它把"授权/换码/刷新"这类安全必需操作与"调用业务 API"的计费解耦，**避免了"因计费上限而让令牌刷新失败，导致应用被动断服"这一失败模式**——见 §17.2.8 的计费模型 —— [合理推测（本报告判断）]。
