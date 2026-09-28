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

### 17.2.4 Tesla 虚拟密钥与车端授权校验

§17.2.1–§17.2.3 拆解的是 Tesla Fleet API 的"云授权链"——令牌分类、scope 划分、授权码流程。但 Fleet API 的车控类能力（解锁、远程启动、Live Camera）与遥测下发，**并不止步于云侧的 OAuth 判定**：它们还要求应用在云之外再持有一把**由车辆本身校验的密钥**。这套机制就是 **虚拟密钥（Virtual Key）**。理解虚拟密钥，是理解 Tesla 授权模型"最后一道闸门"的关键。

本节按信源档案 §7.1 中"虚拟密钥（Virtual Key）——车端授权校验"条目的全部已取证事实，逐条以"**原文事实 / 工程含义 / 授权控制价值 / 残余风险**"四段式展开。凡涉及威胁推断与工程建议者，均标为**本报告判断**（推测，非事实）。

#### 17.2.4.1 虚拟密钥的本质：一对非对称密钥，而非一个共享秘密

**原文事实**：文档明载——虚拟密钥（Virtual Key）是一个**公私钥对**；其中**公钥须由一个"可信用户"（trusted user）添加到车辆**，而**私钥保留在应用服务器端**；车辆在**执行命令之前**或**接受 Fleet Telemetry 配置之前**会**验证载荷的签名** —— 来源：Tesla Fleet API 虚拟密钥开发者指南 —— `https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide` —— [A]。

**工程含义**：这一条把"应用是否有权做某动作"的**最终裁决点从云端移到了车端**。云端（Fleet API）负责"该应用是否被授权调用该端点"，车端（车辆计算单元）负责"这条载荷是否由持私钥的应用签发"。二者是 **AND 关系**：任一侧不通过，命令不执行。从工程实现看，这是一道典型的"非对称签名校验"——应用以私钥签名载荷，车辆用已配对公钥验签；**私钥不出应用服务器**，因此即使云侧令牌被窃，攻击者若拿不到应用私钥，也无法伪造能被车辆接受的载荷。

**授权控制价值**：极高。它把"凭证泄露"的后果从"可直接车控"降级为"还需再突破一次非对称签名"，即从**单因素**升级为**跨信任域的双因素**（云令牌 + 车端验签）。这直接对应审计计划 §3.3 中 **Critical 级**（授权链可被绕过导致任意车辆车控）的**缓解控制**——即使云授权链某一环被击穿，车端仍有一次独立校验兜底 —— 来源：审计计划 §3.3 —— `docs/00-engagement-plan.md` —— [A]。

**残余风险**（本报告判断，推测，非事实）：车端验签的强度取决于**公钥添加环节的"可信用户"判定**是否可靠。若"可信用户"的判定本身可被绕过（例如账户接管后冒充可信用户添加公钥），则车端这道闸门的**信任根**仍然落在云账户安全上——即虚拟密钥把风险**上移**而非消灭。文档已取证的内容未描述"可信用户"的判定细则，这一方向列入 §17.9 待补证。

#### 17.2.4.2 密钥规格：车辆仅支持 prime256v1（P-256）

**原文事实**：文档明确"**车辆仅支持 prime256v1 密钥**"（即 NIST P-256 椭圆曲线，对应 ECDSA）—— 来源：Tesla Fleet API 虚拟密钥开发者指南 —— `https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide` —— [A]。

**工程含义**：这把密钥算法**钉死为单一种类**，而不是让开发者自由选择 RSA/EC/Ed25519。P-256（prime256v1）是 NIST 曲线族中应用最广的一条，其在 X.509 中的表示规则见 RFC 5480（ECDSA/EC 公钥在 X.509 中的表示） —— 来源：RFC 5480 —— `https://www.rfc-editor.org/rfc/rfc5480.txt` —— [A]。单一算法带来的直接工程收益是：**车端只需实现并维护一套验签逻辑与一条曲线**，减少了把多种算法栈带上车所带来的攻击面与验证成本。

**授权控制价值**：中等偏正面。它把"密钥协商面"收窄，避免了"算法降级攻击"（攻击者诱导使用更弱算法）与"算法实现不完整导致验签可被绕过"的常见缺陷。同时，固定曲线让车端可以对该曲线实现做更严格的常量时间与侧信道加固 —— [合理推测（本报告判断）]。

**残余风险**（本报告判断，推测，非事实）：P-256 属经典（非抗量子）曲线，长期看存在"后量子迁移"压力；但截至本次取证，文档未提及抗量子算法或将虚拟密钥迁移至 PQC 的路线，属**未找到公开来源**方向，列入 §17.9。此外，文档未说明车端是否同时支持 **RFC 6090（ECDSA/ECC 基础）** 所描述的确定性签名变体（如 RFC 6979），故"签名是否可复现/是否引入随机数熵依赖"为待补证项。

#### 17.2.4.3 密钥生成命令：以 openssl 显式指定曲线

**原文事实**：文档给出的密钥生成命令为 `openssl ecparam -name prime256v1 -genkey -noout` —— 来源：Tesla Fleet API 虚拟密钥开发者指南 —— `https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide` —— [A]。

**工程含义**：这条命令有两个工程要点。其一是 **显式指定 `-name prime256v1`**，而非依赖 openssl 的默认曲线——这消除了"开发者本机 openssl 版本不同导致生成曲线不一致"的配置漂移。其二是 **`-noout` 抑制了人类可读的曲线参数输出**，使命令直接产出纯密钥文件（私钥），便于纳入后续签名与托管流程。对工程团队而言，这条命令可以**原样写入自动化脚本**，从而保证"生成—签名—注册"三步的密钥材料一致性。

**授权控制价值**：偏工程卫生（Informational）。它的价值在于**降低"人为选错曲线导致配对静默失败"的概率**——若开发者用了默认的其它曲线，车端验签会失败，表现为"授权成功但车控无效"的难诊断故障。把正确曲线写进文档命令，是一种低成本的**可复现性控制**。

**残余风险**（本报告判断，推测，非事实）：命令本身**不包含密钥保护措施**（如口令加密 `-aes256`、或直接生成于 HSM），因此若开发者把裸私钥落盘在本机，私钥即处于"文件系统级"风险下。文档是否建议将私钥存入 HSM/KMS，本次未取证，列入 §17.9。

#### 17.2.4.4 公钥托管路径：一个约定俗成的 .well-known 位置

**原文事实**：公钥**必须托管于** `https://developer-domain.com/.well-known/appspecific/com.tesla.3p.public-key.pem` 且**必须长期可用**；私钥 `private-key.pem` **绝不可托管于域名** —— 来源：Tesla Fleet API 虚拟密钥开发者指南 —— `https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide` —— [A]。

**工程含义**：这把公钥的发布位置**标准化为一条可预测的路径**，从而让"公钥发现"变成一次约定 URL 的 GET，而无需额外的带外交换。注意路径中的两段：`/.well-known/` 是 IANA 注册的"众所周知的 URI"前缀语义，`/appspecific/` 表示"应用私有子命名空间"，`com.tesla.3p.public-key.pem` 则把"发布方（Tesla）、第三方（3p）、对象（public-key）"编码进文件名。这与 OIDC Discovery 用 `/.well-known/openid-configuration` 做端点发现的思路同源（**本报告判断**）——把"元数据放哪儿"从协议外约定变成协议内约定。

**授权控制价值**：正面。其一，**公钥与私钥物理分离**（公钥在域名上，私钥在应用服务器内且明确禁止托管）是密钥管理的基本纪律，直接契合 NIST SP 800-57 对密钥生命周期"公钥可公开、私钥必须受控"的建议 —— 来源：NIST SP 800-57 Part 1 Rev.5 —— `https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final` —— [A]。其二，路径固定使 **Tesla 与车辆都能以确定性方式取到公钥**，降低了"公钥来源不可信"的供应链风险。

**残余风险**（本报告判断，推测，非事实）：公钥托管在**开发者自己的域名**下，意味着该域名的**可用性与完整性**成为配对链路的一环。若域名被劫持或 `.well-known` 路径被篡改（例如通过 DNS/证书层攻击），就可能出现"公钥替换"风险——这与 RFC 5280（X.509 PKI）所防范的证书链信任问题属同一类威胁面 —— 来源：RFC 5280 —— `https://www.rfc-editor.org/rfc/rfc5280.txt` —— [A]。文档要求"长期可用"正是对这一风险的工程对冲，但**"如何承担 TLS 与证书固定"本次未取证**，列入 §17.9。

#### 17.2.4.5 "长期可用"要求：把公钥可用性纳入授权链的持续性

**原文事实**：公钥**必须长期可用**（must be available long term）—— 来源：Tesla Fleet API 虚拟密钥开发者指南 —— `https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide` —— [A]。

**工程含义**：这是一条**持续性义务**，而非一次性动作。它意味着配对的"完成"不等于"结束"——只要应用仍要对已配对车辆生效，公钥就必须一直可被取回。工程上这要求开发者把 `.well-known` 端点纳入**可用性监控（SLA）**，并把它视作**生产依赖**而非"上线时临时放一下的静态文件"。

**授权控制价值**：中高。它把"授权链的持续性"从隐性变成显性——任何撤销/轮换动作，都必须以公钥仍可验证为前提。这实际上给"密钥生命周期"上了一道"可用性即授权条件"的耦合，防止出现"域还在、公钥没了、车控静默失效"的半失效状态 —— [合理推测（本报告判断）]。

**残余风险**（本报告判断，推测，非事实）：文档要求"长期可用"但**未给出公钥轮换的同时在线（dual-publishing）指引**——即新公钥与旧公钥如何并行张贴、过渡多久、旧公钥何时撤下。若开发者直接替换文件，可能造成"正在使用的车辆仍验旧公钥、而域名已只提供新公钥"的过渡窗口不一致。轮换细则列为待补证。

#### 17.2.4.6 私钥绝不可托管：一条明确的红线

**原文事实**：私钥 `private-key.pem` **绝不可托管于域名** —— 来源：Tesla Fleet API 虚拟密钥开发者指南 —— `https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide` —— [A]。

**工程含义**：这是一条**明示的安全红线**。若把私钥放在 Web 可访问的路径上，任何能取到该 URL 的人即获得"签发可被车辆接受载荷"的能力——车端验签将彻底失效。这条要求等价于：**密钥的公开可读性必须与密钥的用途严格对立**——能公开的只有公钥。

**授权控制价值**：极高（对整条车端授权链的存续是前提性的）。它把"虚拟密钥能提供车端级防护"成立的前提条件明确化：**只有当私钥确实只存在于应用服务器时，车端验签才具备独立于云端的裁决能力**。一旦私钥外泄，虚拟密钥机制就退化为"与纯云令牌等效甚至更弱"（因为它还多了一条固定路径可被探测）。

**残余风险**（本报告判断，推测，非事实）：文档给出的是**禁止性要求**，但**未给出私钥的存储标准**（例如是否强制 HSM/KMS、是否强制口令加密、是否强制最小权限的进程隔离）。"要求正确"与"实现正确"之间存在缺口；私钥的实际保护强度取决于开发者自行实现的工程水平，属**文档未覆盖**方向，列入 §17.9。

#### 17.2.4.7 Partner Account 注册端点：把密钥登记到 Tesla

**原文事实**：必须调用 **Partner Account 注册端点**把密钥登记到 Tesla —— 来源：Tesla Fleet API 虚拟密钥开发者指南 —— `https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide` —— [A]。

**工程含义**：这一步把"开发者自建的公钥"与"Tesla 侧的开发者身份"**建立绑定**。可以理解为一次"公钥备案"：Tesla 记录"这个域名的这把公钥，属于这个开发者/应用"，从而在后续配对深链、遥测配置下发时能够验证"公钥—应用"的一致性。文档未在本条目给出该端点的具体 URL（本节**不臆造该 URL**，遵循证据纪律）。

**授权控制价值**：正面且必要。它使"公钥发布"从"单方自建"变为"双方登记"，抑制了"任意域名随意张贴公钥即被视为合法应用"的滥用路径。这是把"授权主体的身份"纳入授权链的一环——与 OAuth 里"客户端必须先注册拿到 client_id"的逻辑同构 —— [合理推测（本报告判断）]。

**残余风险**（本报告判断，推测，非事实）：注册动作的**验真强度**（Tesla 如何确认该域名确属该开发者）本次未取证。若域名归属的核验较弱，则可能出现"冒名注册"。该方向列入 §17.9。

#### 17.2.4.8 配对深链：把"添加密钥"变成一次车主可控的动作

**原文事实**：配对深链为 `https://tesla.com/_ak/<developer-domain.com>`（可选带 `?vin=...` 参数）—— 来源：Tesla Fleet API 虚拟密钥开发者指南 —— `https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide` —— [A]。

**工程含义**：深链把"配对"这一动作**收敛到 Tesla 域内的一个统一入口**。参数中的 `<developer-domain.com>` 指明"要配对哪个应用的公钥"，可选的 `?vin=...` 则指明"针对哪台车"。这样的设计使配对可以：(1) 从应用内直接跳转（引导车主点击）；(2) 可指定单台车（vn 精确到车）。从工程看，这是"由 Tesla 托管配对 UI、由开发者提供上下文"的职责切分。

**授权控制价值**：中高。把配对入口放在 **Tesla 自己的域名**下（而非开发者域名），意味着车主是在**自己信任的品牌域**内完成"添加密钥"这一高风险动作，降低了钓鱼站点伪造配对界面的空间。这与 RFC 8252 对原生应用"必须使用系统浏览器/外部用户代理、禁止内嵌 WebView"的要求在精神上一致——都是为了**让用户能在可信 UI 中确认关键授权动作** —— 来源：RFC 8252 —— `https://www.rfc-editor.org/rfc/rfc8252.txt` —— [A]。

**残余风险**（本报告判断，推测，非事实）：`?vin=...` 的存在意味着**深链携带车辆标识**。若该深链被分享或记录，可能泄露"某车与某应用正在配对"的关联信息。文档未描述深链的时效性/一次性校验，属待补证。

#### 17.2.4.9 自动添加条件：已配对密钥少于 20 把

**原文事实**：B2B 项目车辆**可自动添加虚拟密钥**，条件为**已配对密钥少于 20 把**且**不需要车辆命令协议**；非 B2B 渠道购买的车辆**无法由 Tesla 远程添加密钥** —— 来源：Tesla Fleet API 虚拟密钥开发者指南 —— `https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide` —— [A]。

**工程含义**：这揭示了虚拟密钥配对的**两条路径**——"车主手动添加"与"B2B 自动添加"，且自动路径受**配额约束（<20 把）**。其中的"不需要车辆命令协议"是一个边界条件：对需要命令能力（车控）的场景，自动路径不适用，仍须手动添加。非 B2B 车辆则**被设计为不能远程添加**——即普通消费者车辆的公钥添加必须经车主本人动作。

**授权控制价值**：高。**把"密钥数量上限（<20）"作为影响范围控制手段**，是本章最值得对标的工程取舍之一。它直接对应审计计划 §3.3 中 **High 级**（单一凭证被攻破可横向影响同账号其他车辆）的控制思路——限制"一个账号/一台车能挂多少把密钥"，即限制单点失陷后的横向扩散面 —— 来源：审计计划 §3.3 —— `docs/00-engagement-plan.md` —— [A]。同时，"非 B2B 车辆不可远程添加"把消费者车辆配对锚定在**车主亲自动作**上，符合"个人数据/车控授权须得车主同意"的方向。

**残余风险**（本报告判断，推测，非事实）："<20 把"是一个**绝对数量阈值**，文档未说明其与"车辆所有权变更"的联动——例如车辆易主后，旧密钥是否自动失效。若易主后旧公钥仍在车辆信任集内，则存在"前车主/其应用仍可操作车辆"的残余风险。该方向列入 §17.9。

#### 17.2.4.10 配对的 scope 前置：不是任何令牌都能配对

**原文事实**：配对**要求用户已授予** `vehicle_device_data`、`vehicle_cmds` 或 `vehicle_location` **中至少一项** —— 来源：Tesla Fleet API 虚拟密钥开发者指南 —— `https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide` —— [A]。

**工程含义**：这把"配对"与"OAuth scope 授权"**在流程上串联**：车主必须先完成一次 OAuth 授权（拿到上述三类 scope 之一），才能进行密钥配对。换言之，配对不是独立于 OAuth 的旁路，而是**OAuth 授权的下游动作**——云授权是"准入条件"，车端密钥是"执行条件"。

**授权控制价值**：中高。它**阻断了"绕过 OAuth 直接配对密钥"的路径**。若配对不要求任何已授 scope，则攻击者可能通过配对获取车端能力而无需经云端同意；要求"至少一项相关 scope"把两条授权链耦合起来，使"云同意"成为"车端钥匙"的前置。

**残余风险**（本报告判断，推测，非事实）：这里用的是 **OR 语义（三者之一）**，而非"与车控能力相匹配的最小 scope"。理论上，车主可能为"读遥测"（`vehicle_device_data`）而授权，却由此获得了**进行车控配对**的资格——存在"以读权限换取写能力配对起点"的语义错配。是否在配对时进一步按最终能力收窄，文档未描述，列入待补证。

#### 17.2.4.11 吊销方式：车主在车辆 Locks 界面删除密钥

**原文事实**：虚拟密钥的**吊销由用户在车辆 Locks 界面删除密钥完成** —— 来源：Tesla Fleet API 虚拟密钥开发者指南 —— `https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide` —— [A]。

**工程含义**：吊销的**控制权掌握在车主（车端）手里**，而非仅由开发者或 Tesla 云侧发起。工程含义是：吊销动作直接在**信任集所在处**生效——公钥从车辆上删除，车辆此后不再接受由对应私钥签名的载荷。这与云端"撤销 OAuth consent"（`https://auth.tesla.com/user/revoke/consent?...`）形成**两个不同层面的吊销**：云侧撤销令牌，车端删除密钥。

**授权控制价值**：高。**在车端提供独立吊销入口**，意味着即使云侧某个环节失灵或开发者拒绝配合，车主仍能**直接、就地**切断应用的车控能力。这是"用户主导的授权收回"的强实现，符合 OAuth 2.0 Token Revocation（RFC 7009）"存在可用的吊销机制"的思路，并把吊销权下放到最贴近资源的终端 —— 来源：RFC 7009 —— `https://www.rfc-editor.org/rfc/rfc7009.txt` —— [A]。

**残余风险**（本报告判断，推测，非事实）：文档描述的是**手动**吊销路径（车主去 Locks 界面操作）。这带来两个问题：其一，**时效性依赖车主主动**——若车主不知情或不便操作，吊销不会自动发生；其二，"云侧撤销与车端删除是否自动联动"未在虚拟密钥条目中明说（但 Fleet Telemetry 条目有"scope 撤销→配置移除"的联动，见 §17.2.5）。该联动边界列待补证。

#### 17.2.4.12 "能阻止 Tesla 自己的后端"：一句值得展开的强表述

**原文事实**：文档称虚拟密钥"**甚至能阻止 Tesla 自己的后端访问这些能力**"（even Tesla's own backend cannot access these capabilities）—— 来源：Tesla Fleet API 虚拟密钥开发者指南 —— `https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide` —— [A]。

**工程含义**：这是一句**关于信任边界的强断言**。它暗示：对已启用虚拟密钥保护的能力，其签名校验锚点是**车辆上已配对的那把公钥**，而不论请求来自哪一侧——只要载荷未由对应私钥签名，车辆就拒绝。若成立，则 Tesla 云侧自身也**不构成一个可绕过该校验的万能主体**。

**授权控制价值**：高（潜在）。若该表述在实现上成立，它意味着虚拟密钥提供了**对"云侧超级权限"的约束**——即存在一类"连平台方也无法代签"的操作。这对授权治理是很有分量的性质：它把"平台信任"从"无限"收窄为"受限于车端已配对的公钥集"。

**残余风险**（本报告判断，推测，非事实）：该表述是**厂商自述**，本次未取到独立验证（如第三方研究或车端实现细节）。"能阻止 Tesla 后端"究竟指"后端也无法伪造签名"（密码学意义上的确如此，因为后端没有私钥）还是"后端也无法绕过配对流程"（需车端流程配合），二者强度不同。本报告**不将其作为已独立验证的事实**，仅作为**文档明载的自述口径**记录，并列入 §17.9。

#### 17.2.4.13 对 Fleet Telemetry 的前置依赖

**原文事实**：车辆在**接受 Fleet Telemetry 配置之前**也会**验证载荷签名**；Fleet Telemetry 的前置条件含"**必须已配对虚拟密钥**" —— 来源：Tesla Fleet API 虚拟密钥开发者指南 / Fleet Telemetry 文档 —— `https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide`、`https://developer.tesla.com/docs/fleet-api/fleet-telemetry` —— [A]。

**工程含义**：虚拟密钥不只是"车控"的闸门，也是"遥测下发"的闸门。这使**同一把密钥同时守护两条能力通道**（命令通道与数据流通道）。工程上这意味着"配对一次、双通道受控"，简化了开发者的密钥管理，但也意味着**这两条通道共享同一失效面**——私钥或公钥任一出问题，两条通道同时受影响。

**授权控制价值**：中高。它把"数据流的授权"不只在云端（scope + token）控制，还在**车端以签名控制**。这与"授权被授予 ≠ 资源可访问"的双层控制理念（见 §17.2.2 对 `hide_private` 的分析）一脉相承——通道的开启本身也要过一道车端校验。

**残余风险**（本报告判断，推测，非事实）：**共享失效面**是本节最需警惕的工程风险：密钥一旦泄露或被误删，车控与遥测**同时**受损，缺乏"降级保留其一"的余地。是否支持多密钥并行（如一把管命令、一把管遥测）以隔离失效面，文档未描述，列入 §17.9。

#### 17.2.4.14 虚拟密钥配对的整体数据流（本报告整理）

综合 §17.2.4.1–§17.2.4.13，可把虚拟密钥的"生成—发布—登记—配对—验签—吊销"全链路整理如下（示意图为依据上述已取证事实的**本报告整理**，非文档原图）：

```
                 虚拟密钥配对与车端验签（本报告整理）

  应用服务器                                 车辆（信任集）
  ┌────────────────┐                       ┌────────────────────────┐
  │ private-key.pem│                       │  已配对公钥            │
  │ （绝不可外置托管）│──── 签名载荷 ───────▶│  校验载荷签名           │
  │                │                       │  （仅 prime256v1）      │
  └────────────────┘                       └────────────────────────┘
        │ 生成：openssl ecparam -name                      ▲
        │        prime256v1 -genkey -noout                 │
        │                                                  │ 可信用户在车辆
        ▼ 公钥发布：https://<domain>/.well-known/          │ Locks 界面
          appspecific/com.tesla.3p.public-key.pem         │ 添加 / 删除（吊销）
        │                                                  │
        ▼ 备案：调用 Partner Account 注册端点 ──▶ Tesla 云侧
                                                   │
        配对深链：https://tesla.com/_ak/<developer-domain.com>（?vin=可选）
                                                   │
        配对前置：车主已授予 vehicle_device_data / vehicle_cmds /
                  vehicle_location 三者之一
                                                   │
        B2B 自动添加：已配对密钥 <20 把 且 不需要车辆命令协议
        非 B2B 车辆：无法由 Tesla 远程添加
```

**链路小结（本报告判断，推测，非事实）**：Tesla 的虚拟密钥把授权控制做了**三层叠加**——(1) 云层：OAuth scope + 令牌；(2) 配对层：车主在车端添加公钥、受"<20 把"与 scope 前置约束；(3) 校验层：车辆在执行/接受配置前逐条验签。三层缺一不可。这一设计对通用方案的直接启示是：**面向车控的授权，不应止步于"云端授权令牌"，还应包含"资源侧（车端）的独立凭证校验"**。该启示将在 §17.8 与通用方案逐条比对。

### 17.2.5 Tesla Fleet Telemetry 的授权链与数据流

虚拟密钥明确了"车端为何信你"，Fleet Telemetry 则回答"车端**把数据推给谁、推什么、推到什么程度**"。本节按信源档案 §7.1 中"Fleet Telemetry（车→云直连流）"条目的已取证事实逐条展开，重点分析其**授权链**（谁有权开启推流）与**数据流**（推什么、如何限流、断连怎么办）。

#### 17.2.5.1 定位：以"推送"取代"轮询"

**原文事实**：Fleet Telemetry 让**车辆直连开发者服务器**，取代**轮询 `vehicle_data` 端点**；客户端源码在 `https://github.com/teslamotors/fleet-telemetry`，命令代理在 `https://github.com/teslamotors/vehicle-command` —— 来源：Tesla Fleet Telemetry 文档 —— `https://developer.tesla.com/docs/fleet-api/fleet-telemetry` —— [A]。

**工程含义**：这是**数据获取范式**的转变——从"应用反复问车要数据"（pull/轮询）转为"车主动把数据推给应用"（push/流）。对授权而言，范式转变带来一个关键差异：轮询模式下，每次取数都是一次**独立的 API 调用**，可在调用点做鉴权与审计；推送模式下，数据是**持续流**，鉴权发生在**流建立时**（配置下发/连接建立），之后是一条长约的连接。因此推送模式对"授权撤销的联动"提出了更高要求——**若撤销不能传导到已建立的流，撤销就会滞后**。

**授权控制价值**：正面但需配套。推送降低了无效调用（省配额、省电、省带宽），但把"持续授权"的责任前移到"配置与连接管理"上。Tesla 对此的配套（scope 撤销→配置移除）见 §17.2.5.3。

**残余风险**（本报告判断，推测，非事实）：开放源码的客户端（`fleet-telemetry`）与命令代理（`vehicle-command`）属**可信第三方仓库**（审计计划 §3.1 的 [B] 级，官方 SDK 仓库）——但其**版本演进**本身构成供应链关注点，见 §17.2.5.7。

#### 17.2.5.2 前置条件：固件版本 + 虚拟密钥，双重门槛

**原文事实**：Fleet Telemetry 的前置条件为——车辆**固件 2024.26+**；**证书签名类应用需 2023.20.6+**；**Model S/X（Intel Atom）需 2025.20+**；且**必须已配对虚拟密钥** —— 来源：Tesla Fleet Telemetry 文档 —— `https://developer.tesla.com/docs/fleet-api/fleet-telemetry` —— [A]。

**工程含义**：这里的门槛是**双重的**——一条是**能力门槛**（固件版本必须支持遥测推流，且不同车型/不同应用类型要求不同版本），一条是**授权门槛**（必须已配对虚拟密钥，即 §17.2.4 的成果）。这意味着"开启遥测"不是单一开关，而是"**车辆能力达标 + 车端授权就位**"的合取条件。

**授权控制价值**：中高。把"固件版本"纳入前置，是一种**能力级的最小基线控制**：它确保只有具备相应安全能力的固件才能开启推流，避免老固件上以更弱的实现暴露数据。把"虚拟密钥"纳入前置，则把遥测与车端凭证绑定（见 §17.2.4.13）。

**残余风险**（本报告判断，推测，非事实）：文档明载 **2018 年前 Model S/X 且未做信息娱乐升级的车辆不支持 Fleet Telemetry，且无支持计划** —— 来源：同上 —— [A]。这类"永久不支持"的存量车辆，其数据获取只能回到"轮询 vehicle_data"或更早路径，形成**能力分级上的长期不均**。这不构成安全缺陷，但在车队治理上是需要登记的事实。

#### 17.2.5.3 配置由应用私钥签名，且"Tesla 无法编辑"

**原文事实**：遥测**配置由应用私钥签名**，且"**Tesla 无法编辑**"；若**所需 scope 被撤销导致配置失效，配置会被从车辆移除** —— 来源：Tesla Fleet Telemetry 文档 —— `https://developer.tesla.com/docs/fleet-api/fleet-telemetry` —— [A]。

**工程含义**：这两条把"配置的**完整性与**授权**绑定**。其一，配置由应用私钥签名，意味着**配置内容的来源可被车辆验证**（车辆能确认"这份配置确实是那个已配对应用签的"）；"Tesla 无法编辑"进一步说明**平台方也不能单方面改写要推什么字段**。其二，"scope 撤销→配置移除"意味着**云侧授权状态的变化会传导到车端配置**——授权一旦不在，推流配置即被回收。

**授权控制价值**：极高（本章最强的"撤销联动"案例之一）。"scope 撤销→配置自动移除"是**授权撤销的自动传导**，把"授权生命周期"与"数据流生命周期"耦合起来，避免了"授权已撤销、流还在跑"的常见失配。这与 OAuth 2.0 Token Revocation（RFC 7009）所期望的"撤销能真正生效"一脉相承，并把撤销**从令牌层延伸到车端配置层** —— 来源：RFC 7009 —— `https://www.rfc-editor.org/rfc/rfc7009.txt` —— [A]。"Tesla 无法编辑"则是一种**平台中立性**设计，抑制了"平台方利用特权窥探或改写用户数据流"的信任风险。

**残余风险**（本报告判断，推测，非事实）：其一，"**导致配置失效**"的触发条件被描述为"所需 scope 被撤销"，但"scope 部分撤销（如撤销 `vehicle_location` 但保留 `vehicle_device_data`）时，配置是整体移除还是按字段收窄"本次未取证——这直接关系到 §17.2.5.5 字段级控制的边界。其二，"Tesla 无法编辑"为自述口径，未取到独立验证。二者列入 §17.9。

#### 17.2.5.4 单车上限：最多同时向 5 个第三方应用推流

**原文事实**：**单台车辆最多同时向 5 个第三方应用推流** —— 来源：Tesla Fleet Telemetry 文档 —— `https://developer.tesla.com/docs/fleet-api/fleet-telemetry` —— [A]。

**工程含义**：这是 Fleet Telemetry 侧的一处**并发配额**。它与虚拟密钥的"<20 把"上限（§17.2.4.9）共同构成"**一台车的对外暴露面**"的双重量化约束：最多 20 把密钥、最多 5 条第三方推流。"5 个应用"这一上限，直接限制了单台车的数据被多少个不同第三方同时接收。

**授权控制价值**：高。这是"**影响范围控制**"在数据流维度的直接体现——把"一台车的数据可被多少方持续接收"钉死在 5 个，对应审计计划 §3.3 中 High 级的横向影响面控制（**本报告判断**）：即便多个应用被攻破，车辆对外推流的入口数量仍有硬上限。它与"<20 把密钥"形成"身份上限 + 通道上限"的双保险。

**残余风险**（本报告判断，推测，非事实）："5 个"是**绝对阈值**，文档未说明超限时的**行为语义**（第 6 个应用请求推流时是拒绝、还是替换最旧的）。拒绝对车主更安全，替换则可能造成"静默挤掉既有应用"。该行为语义列入 §17.9。

#### 17.2.5.5 位置类字段与 vehicle_location 的耦合，以及 hide_private 的 403

**原文事实**：位置类字段（**Location、OriginLocation、DestinationLocation、DestinationName、RouteLine、GpsState、GpsHeading**）**需要 `vehicle_location`**；`hide_private` 共享车辆尝试访问会被拒绝并返回 **HTTP 403 "location access not granted"** —— 来源：Tesla Fleet Telemetry 文档 —— `https://developer.tesla.com/docs/fleet-api/fleet-telemetry` —— [A]。

**工程含义**：这三个要点值得分开看。其一，**字段级授权**——遥测不是"全有或全无"，而是**按字段绑定 scope**：只有这 7 类位置字段需要 `vehicle_location`，其余字段由别的 scope 管辖。其二，**字段清单是显式枚举的**（7 个字段名被逐一列出），意味着位置语义被拆到了"起点/终点/名称/路径/状态/朝向"的粒度。其三，**`hide_private` 车在字段级仍被二次拒绝**，且拒绝有明确的 **HTTP 403 与错误语义 "location access not granted"**。

**授权控制价值**：极高（与 §17.2.2 的双层收窄呼应）。这是"**scope 授权 + 资源级策略**"双层控制在**数据流**上的落地：即使应用持有 `vehicle_location`，`hide_private` 车的对应字段仍返回 403。明确的状态码（RFC 6750 定义了 Bearer 令牌使用中的 403 语义与错误码）让"被策略拒绝"与"令牌无效"可区分，便于审计与排障 —— 来源：RFC 6750 —— `https://www.rfc-editor.org/rfc/rfc6750.txt` —— [A]。审计计划 §3.3 已将此判为 **Informational→正面控制案例** —— 来源：审计计划 §3.3 —— `docs/00-engagement-plan.md` —— [A]。

**残余风险**（本报告判断，推测，非事实）：位置字段被枚举为 7 个，但**是否仍有其他字段可间接推断位置**（如通过充电地点、服务记录等非位置字段的组合）本次未取证。字段级的"最小必要"是否已做到完备，属待补证；同时，"hide_private 由谁设置、可否被应用影响"未取证，若可被应用侧影响则会削弱该控制。

#### 17.2.5.6 传输行为：500 ms 窗口、字段级 interval_seconds、变化触发

**原文事实**：遥测传输行为为——**500 ms 事件收集窗口**；**按字段 `interval_seconds` 与变化触发上报**；示例负载约 **15 信号/分钟 ≈ $0.0001/分钟 ≈ $0.006/行驶小时** —— 来源：Tesla Fleet Telemetry 文档 —— `https://developer.tesla.com/docs/fleet-api/fleet-telemetry` —— [A]。

**工程含义**：三点工程含义。其一，**500 ms 收集窗口**是一种**批处理节流**——事件先在车端聚合成窗口再发出，避免逐事件高频发包。其二，**字段级 `interval_seconds`** 允许对每个信号设定"最小上报间隔"，实现**按字段的采样率治理**。其三，**变化触发**（on-change）意味着"值没变就不报"，进一步降低冗余流量与计费。

**授权控制价值**：中（更偏"可用性与成本治理"而非"访问控制"）。但它有间接的授权价值：**降低数据密度即降低泄露面**——采样率越低、变化触发越多，单次泄露可暴露的时间序列越稀疏。它是"最小必要数据"原则在**时间维度**上的工程落地 —— [合理推测（本报告判断）]。

**残余风险**（本报告判断，推测，非事实）：字段级 `interval_seconds` 的**可设置范围与下限**未取证——若某字段允许被设为极小间隔（如 100 ms），可能反而**放大**数据密度与成本。该范围属待补证。

#### 17.2.5.7 断连处理：5000 条缓冲与最大 30 秒指数退避

**原文事实**：断连处理为——车辆**缓冲 5000 条消息（≥2500 秒数据）**；重连采用**指数退避，最大重试延迟 30 秒** —— 来源：Tesla Fleet Telemetry 文档 —— `https://developer.tesla.com/docs/fleet-api/fleet-telemetry` —— [A]。

**工程含义**：这两条是**可靠性工程**参数。**5000 条缓冲**（文档换算为 ≥2500 秒）意味着断连期间车端会暂存数据，重连后补发，避免网络抖动造成数据缺口。**指数退避、上限 30 秒**是经典的重连节流策略：失败越多次、等待越久，但封顶 30 秒以保证恢复速度。

**授权控制价值**：偏可用性（Informational/C）。但它对安全有间接影响：**缓冲的 5000 条数据在车端"待发"期间处于暂存态**，若缓冲内容涉及敏感字段，其车端存储本身成为一个小攻击面；指数退避则避免"断连→猛重连"造成的拒绝服务式自扰。

**残余风险**（本报告判断，推测，非事实）：缓冲数据在**车端的存储保护**（是否加密、是否随 scope 撤销而清除）未取证；"缓冲上限 5000 条"在长时间断连下会造成**数据截断**（超出即丢），这对需要完整时序的场景是隐性数据完整性问题。二者列入待补证。

#### 17.2.5.8 客户端版本与固件矩阵

**原文事实**：客户端版本变更记录含——**1.0.0**（固件 2025.2.6 / 2024.45.32.20，新增 `delivery_policy=latest` 要求服务端 ≥0.7.1）、**1.1.0**、**1.2.0**（固件 2025.44.25.5）、**1.3.0**（固件 2026.26.6，`include_fields`） —— 来源：Tesla Fleet Telemetry 文档 —— `https://developer.tesla.com/docs/fleet-api/fleet-telemetry` —— [A]。

**工程含义**：这揭示了 Fleet Telemetry 存在**客户端—固件—服务端三方版本矩阵**。每一次客户端升级往往**绑定**某个固件基线（如 1.2.0 对应固件 2025.44.25.5），并要求服务端达到某个最低版本（如 1.0.0 的 `delivery_policy=latest` 要求服务端 ≥0.7.1）。这意味着**授权/数据流的可用性依赖版本对齐**。

**授权控制价值**：中。版本矩阵的存在使"安全能力的升级"可以**随客户端版本推送**（如 1.3.0 带来的 `include_fields` 可视为字段级最小化的能力增强，见 §17.2.5.5 字段控制的呼应）——它是"能力可演进"的工程基础。

**残余风险**（本报告判断，推测，非事实）：**三方版本矩阵**是典型的"版本地狱"来源——固件落后、客户端过新、服务端过低，任一不匹配都可能导致推流异常。文档给出的版本对应是否**向下兼容**、旧客户端在新固件上的行为，未取证。列入待补证。

#### 17.2.5.9 服务端 TLS 指引：自建服务端的证书责任

**原文事实**：服务端 TLS 指引——开发者须用仓库内 `tools/check_server_cert.sh` 校验主机与 CA 兼容性 —— 来源：Tesla Fleet Telemetry 文档 —— `https://developer.tesla.com/docs/fleet-api/fleet-telemetry` —— [A]。

**工程含义**：因为 Fleet Telemetry 是"车**直连开发者服务器**"，所以**TLS 服务端证书的责任落在开发者身上**。Tesla 提供 `check_server_cert.sh` 作为工具，把"证书是否满足车端要求"变成一次可执行的预检。

**授权控制价值**：中高。车端与开发者服务器之间的 TLS，是这个直连链路的**通道鉴权基础**。若证书不合规，车端可能拒绝连接或降级。这属于"通信安全"层（见通用分层方案的通信安全章节），但在授权视角下，它是"**服务端身份被车端确认**"的前提——车端得先确认"对面确实是那个已授权应用的服务器"。

**残余风险**（本报告判断，推测，非事实）：文档只给出**证书兼容性预检工具**，是否要求**证书固定（pinning）**或**双向 TLS（mTLS，RFC 8705）**本次未在 Fleet Telemetry 条目中取证。考虑到车云链路的关键性，mTLS/证书固定是通用方案中推荐的控制（见 §17.8），但**Tesla 是否在遥测链路上采用，属未找到公开来源**，不得推断为"未采用"（红线 §3.2.4）——来源：RFC 8705 —— `https://www.rfc-editor.org/rfc/rfc8705.txt` —— [A]（规范存在性）。

### 17.2.6 Tesla 限流、计费与配额治理

授权控制的另一端是"**授权之外还有多少配额可被消耗**"。本节按信源档案 §7.1 中"限流与计费（影响范围控制的另一维度）"条目的已取证事实逐条分析其安全含义——重点不是"多少钱"，而是"**配额分池与暂停机制如何约束滥用与可用性**"。

#### 17.2.6.1 限流：按账号、按设备，且同账号多应用共享

**原文事实**：限流按**账号按设备**计——**实时数据 60 次/分**；**唤醒 3 次/分**；**设备命令 30 次/分**；**同账号多应用共享限额** —— 来源：Tesla Fleet API Billing and Limits —— `https://developer.tesla.com/docs/fleet-api/billing-and-limits` —— [A]。

**工程含义**：三个限额**按动作类型分层**（读数据 > 设备命令 > 唤醒），且**按"账号×设备"为维度**计量。最关键的机制是"**同账号多应用共享限额**"——即配额是**账号级分池**，而非"每个应用各拿一份"。这意味着一个账号下若有 N 个应用，它们**争抢同一池额度**。

**授权控制价值**：中高（针对"滥用与突破尝试"）。分层限额把"高破坏性动作用更小配额"来收窄——唤醒（3 次/分）与设备命令（30 次/分）是可能影响车辆状态的操作，配额远低于读取（60 次/分），本身就抑制了"高频轰炸式车控"。**共享分池**则防止了"通过注册多个应用来放大配额"的绕过路径 —— [合理推测（本报告判断）]。

**残余风险**（本报告判断，推测，非事实）：**共享分池**是双刃剑——它防止配额被多应用放大，但也引入**可用性耦合**：一个应用被滥用打满额度，**同账号其余应用一并受影响**（类似"吵闹的邻居"）。这在多租户/多应用共账号的 B2B 场景下是真实的**可用性风险**。是否存在"按应用分池"或"配额隔离"机制，本次未取证，列入 §17.9。

#### 17.2.6.2 计费：月度周期、默认上限 0、80%/100% 邮件、超限暂停且移除推流

**原文事实**：计费**按用量、月度周期（每月 1 日起算）**；**每账号计费上限默认 0**；**达 80% 与 100% 时发邮件**；**超限会暂停 API 使用并移除 Fleet Telemetry 推流配置（且不恢复）** —— 来源：Tesla Fleet API Billing and Limits —— `https://developer.tesla.com/docs/fleet-api/billing-and-limits` —— [A]。

**工程含义**：这四点构成一套**成本安全阀**。其一，**月度周期**给出稳定的结算窗口。其二，**默认上限 0** 表示"未经设置，账号的计费上限为零"——即**默认不允许多花**，是一种"默认拒绝"（default-deny）的财务姿态。其三，**80%/100% 邮件**是**渐进告警**。其四，**超限暂停 + 移除推流 + 不恢复**是最严厉的一档：超限不只是"停止继续调用"，而是**主动回收已有的推流配置，且不自动恢复**。

**授权控制价值**：高（针对"滥用成本与失控扩散"）。**默认上限 0** 的 default-deny 姿态，把"成本失控"的默认结果设为"不会发生"，与安全领域的"默认拒绝"原则同构。**超限即移除推流且不恢复**是一项**强制性的资源回收控制**——它把"财务超限"升级为"授权态变更"，使滥用/失控达到阈值时**自动切断数据通道**，而非仅停止计费。这对应审计计划 §3.3 中"**无吊销联动导致影响范围扩大**"（Medium 级）的**反向正面案例**：存在强制联动 —— 来源：审计计划 §3.3 —— `docs/00-engagement-plan.md` —— [A]。

**残余风险**（本报告判断，推测，非事实）：**"且不恢复"**是一处值得警惕的设计——它在安全上是"宁可停服不可失控"，但在**可用性**上是激进的：合法应用因偶发超限即被移除推流且不自动恢复，需要人工介入。对依赖持续遥测的安全监测类应用（如入侵检测相关的车辆状态监控），这可能造成**监测盲区**。此外，**认证端点不计费**（见 §17.2.3.4）缓解了"因计费导致令牌刷新失败"的失败模式，但**计费暂停是否连带影响刷新**的边界仍需确认，列入 §17.9。

#### 17.2.6.3 折扣与计费口径：$10 折扣、<500 计费 / ≥500 不计费、四舍五入到 $0.01

**原文事实**：**个人开发者/小应用每月 $10 折扣**；**响应码 <500 全部计费，≥500 不计费**；**费用四舍五入到 $0.01** —— 来源：Tesla Fleet API Billing and Limits —— `https://developer.tesla.com/docs/fleet-api/billing-and-limits` —— [A]。

**工程含义**：三条口径值得分开看。**$10 月度折扣**是面向个人/小开发者的扶持，降低了准入门槛。**"响应码 <500 全部计费，≥500 不计费"**是一条**按结果计费**规则——服务端错误（5xx）不计费，把"平台故障的成本"从开发者转移回平台。**四舍五入到 $0.01** 是结算精度规则。

**授权控制价值**：中（主要是治理与公平性）。"≥500 不计费"在**滥用经济学**上有直接含义：它降低了"攻击者**故意打爆服务端（诱发 5xx）以制造开发者账单**"的动机——因为 5xx 本就不计费。这消除了一个特定的**成本型拒绝服务**向量 —— [合理推测（本报告判断）]。

**残余风险**（本报告判断，推测，非事实）："<500 全部计费"意味着 **4xx（客户端错误）仍计费**——若攻击者以大量**无效请求（4xx）**轰炸 API，开发者仍要为其买单，构成一种"**计费层拒绝服务**"风险（攻击者低成本、受害者高成本）。这是配额治理下真实存在的滥用成本面，是否有限速/防重放抑制，列入 §17.9。

#### 17.2.6.4 过渡期硬日期：2024-02-01

**原文事实**：文档明确过渡日期——"**Application access will not be disabled during the payment transition period which ends February 1, 2024**"（第三方付费 API 的强制执行安排在 2024-02-01 前后）—— 来源：Tesla Fleet API Billing and Limits —— `https://developer.tesla.com/docs/fleet-api/billing-and-limits` —— [A]（**原文陈述与"2024-02-01"为该页一手引文**）。

**工程含义**：这是本章**极少数的硬日期之一**。它的工程含义是：在 2024-02-01 之前的过渡期内，即使未完成付费设置的账号**也不会被停用访问**；过渡期结束后，付费/配额规则正式生效（与 §17.2.6.2 的暂停机制衔接）。

**授权控制价值**：中（治理透明性）。一个**公开的过渡硬日期**让所有开发者有统一的时间表，减少"规则突变"带来的运营风险。这是"平台侧策略变更的**可预期性**"——本身不是访问控制，但影响授权治理的**确定性**。

**残余风险**（本报告判断，推测，非事实）：本报告**只采信该页的一手引文**。关于"2023 年 Tesla 收紧 API"与"2023 Toyota/Tesla 漏洞披露事件"的叙事版本，信源档案 §7.1 明确标注**未取到一手来源** —— 来源：信源档案 §7.1 —— `docs/sources/source-dossier.md` —— [A，记录]。故本报告**不采用**这些叙事，仅保留"2024-02-01"这一硬日期。这是证据纪律的直接体现（红线 §3.2.3）。

#### 17.2.6.5 限额与计费的三层治理结构（本报告整理）

综合 §17.2.6.1–§17.2.6.4，Tesla 的配额治理可整理为三层（**本报告整理**）：

| 层级 | 机制 | 已取证事实 | 安全含义（本报告判断） |
|---|---|---|---|
| 速率层 | 分层限流 | 实时 60/分、唤醒 3/分、命令 30/分；同账号多应用共享 | 抑制高频滥用与"多应用放大配额"绕过 |
| 成本层 | 计费与上限 | 月度周期；默认上限 0；80%/100% 邮件 | 默认拒绝的财务姿态，防成本失控 |
| 强制层 | 超限暂停 | 暂停 API + 移除推流配置 + 不恢复 | 强制吊销联动，切断失控数据通道 |

来源：Tesla Fleet API Billing and Limits —— `https://developer.tesla.com/docs/fleet-api/billing-and-limits` —— [A]；"安全含义"列为本报告判断 —— [合理推测（本报告判断）]。

**小结（本报告判断，推测，非事实）**：Tesla 把**配额治理当作授权治理的一部分**——超限不只是"经济事件"，还会**触发资源侧的授权回收**（推流配置被移除且不恢复）。这一"经济阈值 → 授权态变更"的联动，是通用方案中不一定显式提供的控制点，值得对标（见 §17.8）。

### 17.2.7 Tesla 漏洞披露生态

漏洞披露政策是"授权与控制之外"的**最后一层治理**：它约束**研究者**如何进入、报告、以及**不得做什么**。本节按信源档案 §7.1 中"漏洞披露与赏金"条目逐条分析，重点是"披露政策作为安全治理的一部分"及其对研究者的**实际约束**。

#### 17.2.7.1 项目启动与状态

**原文事实**：Tesla 在 **Bugcrowd** 运营漏洞赏金项目，**启动于 2015-08-04**，状态 **in progress** —— 来源：Bugcrowd Tesla 项目页 —— `https://bugcrowd.com/engagements/tesla` —— [A/B]。

**工程含义**：**2015-08-04** 是本章又一处硬日期，说明 Tesla 的赏金项目是**长期运行**的（非临时活动），状态 in progress 表明持续接受报告。

**治理价值**：一个**长期、公开、第三方平台托管**的赏金项目，是"**外部研究可被有序吸纳**"的标志。把报告通道放在第三方（Bugcrowd）而非仅自建，提供了**流程透明度**与**研究者侧的可追溯性**。

**残余风险**（本报告判断，推测，非事实）：该条目在本档案中标为 **[A/B]**（Bugcrowd 页属权威第三方托管平台）。这暗示其**证据等级略低于** Tesla 官方开发者文档的纯 [A]——引用时应保留这一区分（对齐 §3.1）。

#### 17.2.7.2 四档赏金区间

**原文事实**：赏金档位为——**Critical $50,000–$100,000**；**High $20,000–$50,000**；**Moderate $10,000–$20,000**；**Low $500–$10,000** —— 来源：Bugcrowd Tesla 项目页 —— `https://bugcrowd.com/engagements/tesla` —— [B]。

**工程含义**：四档区间**呈阶梯**，且**最高档（Critical）达 5–10 万美元**。档位的存在把"漏洞严重性—经济激励"映射为公开契约。

**治理价值**：高。**赏金区间是安全投资意愿的公开信号**——尤其 Critical 档的高上限，说明厂商愿意为"最高危漏洞"支付高额对价，从而**减少研究者"私藏漏洞或卖给出价更高者"的动机**。这与"授权与访问控制"的关联在于：**赏金项目是发现"授权链被绕过"类漏洞（审计计划 §3.3 的 Critical 判据）的主要外部渠道** —— 来源：审计计划 §3.3 —— `docs/00-engagement-plan.md` —— [A]。

**残余风险**（本报告判断，推测，非事实）：档位为**区间**，具体定价规则未取证；"车辆/能源产品问题不走 Bugcrowd 网页表单"（见 §17.2.7.3）意味着**最高危的一类漏洞并不进入公开赏金的常规流程**，其定价与流程透明度相对更低。

#### 17.2.7.3 必须邮件报递并使用 GPG；硬件研究须先登记

**原文事实**：车辆/能源产品问题**须邮件报至 `vulnerabilityreporting@tesla.com` 并使用 Tesla GPG 公钥**，**不走 Bugcrowd 网页表单**；**硬件研究须先向 Tesla 登记车辆/Powerwall** —— 来源：Bugcrowd Tesla 项目页 —— `https://bugcrowd.com/engagements/tesla` —— [A/B]。

**工程含义**：这里有三条**流程分叉**。其一，**渠道分叉**：车辆/能源产品的发现**不走网页表单，走邮件**——对应最高危资产用更受控的通道。其二，**加密要求**：**必须使用 Tesla GPG 公钥**加密报告，保护报告内容的机密性。其三，**前置登记**：硬件研究**必须先登记**车辆/Powerwall，即"先声明、后研究"。

**治理价值**：高。**GPG 加密报告**确保"漏洞细节在传输中不被窃取"——这与漏洞本身的**机密性治理**一致。**硬件研究先登记**则把物理研究纳入**可追溯的授权范围**（登记即授权），避免"未授权物理测试"落入法律灰区——这是"研究授权的显式化"。

**残余风险**（本报告判断，推测，非事实）：**前置登记**对研究者是**实际约束**（增加了进入成本与可追溯性）；同时，登记机制也可能**抑制部分研究者的参与意愿**，从而在"可追溯"与"报告量"之间存在取舍。GPG 密钥的**轮换与公示**方式未取证。

#### 17.2.7.4 规则要点：24 小时停止、不得公开披露、超充不在范围、第三方库归属

**原文事实**：规则要点为——若**访问到不属于自己的数据须在 24 小时内停止并披露**；**未经 Tesla 批准不得公开披露已确认未修复漏洞**；**超级充电及相关基础设施不在范围内**；**涉及第三方库的漏洞可能被转给厂商而不通知研究者** —— 来源：Bugcrowd Tesla 项目页 —— `https://bugcrowd.com/engagements/tesla` —— [B]。

**工程含义与治理价值**：四条各自对应一个治理取舍——
1. **"访问到他人数据 24 小时内停止并披露"**：这是**对越界访问的止损义务**，把"研究过程中意外触达个人数据"的处理**时间盒化**。它把"数据保护"置于"研究完整性"之上，与 GDPR 式的数据保护取向一致（**本报告判断**）。
2. **"未修复漏洞不得公开披露"**：这是**披露协调（coordinated disclosure）**的强形态——把公开披露的**决定权归厂商**。治理上它保护了"修复窗口"，但对研究者是**强约束**（可能延长漏洞的隐蔽期）。
3. **"超充不在范围内"**：**范围边界**的明示，划清了"可研究"与"不可研究"的资产。
4. **"第三方库漏洞可能被转给厂商而不通知研究者"**：**归属与通知规则**——供应链漏洞的处置可能不经研究者，这对研究者的**回报预期**是负面因素。

**残余风险与对研究者的实际约束**（本报告判断，推测，非事实）：这四条共同构成对研究者的**实际约束集**——**范围有限（超充排除）、披露受限（需批准）、回报不确定（可能无通知）、且须自证合规（24 小时止损）**。对厂商而言这降低了法律与声誉风险；对研究者而言，参与前须**充分理解这些约束**，否则可能"做了研究却无法公开或获得回报"。

#### 17.2.7.5 披露政策作为"安全治理"的意义（本报告判断）

把 §17.2.7.1–§17.2.7.4 合起来看，Tesla 的披露生态具备**四要素**（**本报告判断，推测，非事实**）：

| 要素 | 对应机制 | 治理作用 |
|---|---|---|
| 长期通道 | Bugcrowd 项目（2015-08-04 起，in progress） | 研究可持续被吸纳 |
| 经济激励 | 四档赏金（Critical 至 Low） | 抑制私藏/黑市交易 |
| 渠道分级 | 车辆/能源走邮件 + GPG；硬件先登记 | 高危资产用受控通道 |
| 行为约束 | 24h 止损、未修复不公开、范围排除、无通知转交 | 厂商风险与合规优先 |

**与授权章节的关联（本报告判断）**：披露政策**不是**授权机制本身，但它是授权治理的**外部审计面**——授权链的 Critical 级缺陷（如可绕过车控授权）最可能由外部研究者经此渠道发现。因此，**披露生态的健全程度，间接决定了一个车企"授权缺陷被多快发现并修复"**。这也是本章把披露生态纳入"车企实践"分析的核心理由。

### 17.2.8 Tesla 授权模型小结

本节把 §17.2.1–§17.2.7 的已取证控制点收拢为一张**控制点对照表**，并按审计计划 §3.3 的严重度口径给出 **CSO 评估**，最后给出三条优劣分析。

#### 17.2.8.1 控制点 × 实现方式 × 证据等级 × CSO 评估

| # | 控制点 | 实现方式（已取证事实） | 证据等级 | CSO 评估（按审计计划 §3.3） |
|---|---|---|---|---|
| 1 | 令牌分类 | third-party / partner / third-party-for-business 三类令牌，语义分离 | [A] | Informational（架构观察） |
| 2 | scope 粒度 | 12 个 scope，覆盖身份→能源→企业八层 | [A] | Low（覆盖广但读写未彻底分离，属文档化观察） |
| 3 | 双层收窄 | `hide_private` 车即便授予 `vehicle_location` 亦拒绝位置（403） | [A] | **Informational→正面控制案例**（建议对标） |
| 4 | 授权控制例外 | `vehicle_specs`/`vehicle_pricing_info` 仅 Partner Token、对任意车辆无需车主授权 | [A] | **High**（退出逐车主同意模型，需契约与审计补偿） |
| 5 | 增量授权 | `prompt_missing_scopes` / `require_requested_scopes` | [A] | Informational（同意流程严格度可控） |
| 6 | 授权/资源主机分离 | auth.tesla.com / fleet-auth / fleet-api 分置 | [A] | Informational（AS/RS 分离落地） |
| 7 | audience 区域绑定 | `/token` 的 `audience` 必须为 Fleet API base URL | [A] | Low（抑制令牌跨域重放） |
| 8 | 刷新令牌轮换 | 刷新令牌一次性、3 个月过期、24 小时宽限 | [A] | Low（强轮换约束，正面） |
| 9 | 车端凭证校验 | 虚拟密钥（P-256）签名/验签，私钥不出服务器 | [A] | **Critical 级威胁的缓解控制**（车端独立兜底） |
| 10 | 密钥/通道上限 | 虚拟密钥 <20 把；Fleet Telemetry 单车 ≤5 应用 | [A] | High 级的**影响范围控制**手段 |
| 11 | 撤销自动联动 | scope 撤销→Fleet Telemetry 配置从车辆移除 | [A] | Medium 级的**反向正面案例**（存在联动） |
| 12 | 车主侧吊销 | Locks 界面删密钥；`auth.tesla.com/user/revoke/consent` | [A] | Informational→正面（用户主导收回） |
| 13 | 配额治理 | 分层限流；默认上限 0；超限暂停并移除推流且不恢复 | [A] | Informational（成本安全阀，但有可用性耦合） |
| 14 | 外部披露生态 | Bugcrowd（2015-08-04 起）；车辆/能源走邮件+GPG | [A/B] | Informational（外部审计面） |

来源：§17.2.1–§17.2.7 各条已标注的 developer.tesla.com / bugcrowd.com 一手或第三方页面；"CSO 评估"列依审计计划 §3.3 口径 —— 来源：审计计划 §3.3 —— `docs/00-engagement-plan.md` —— [A]。

#### 17.2.8.2 优劣分析（三条）

**优势一：车端独立校验（虚拟密钥）——把 Critical 级风险挡在车端。** Tesla 是本次取证中**唯一**在公开文档里把"车端凭证校验"讲清楚的车企：公钥上车上、私钥不出服务器、车辆逐条验签。这使"云授权链被绕过"（§3.3 的 Critical 判据）**不再等价于"车控被夺"**，因为还有车端这一道独立闸门 —— 来源：Tesla Fleet API 虚拟密钥开发者指南 —— 同上 —— [A]。**本报告判断**：这是本章最值得其他车企对标的控制点。

**优势二：撤销联动的多层贯通。** Tesla 在**三个层面**都提供了撤销——云侧撤销 consent、scope 撤销触发遥测配置移除（§17.2.5.3）、车端 Locks 界面删密钥（§17.2.4.11）。三层各自独立生效，使"授权收回"不一定依赖单点。这对应审计计划 §3.3 中 Medium 级（"无吊销联动"）的反面，是**正面实现** —— 来源：审计计划 §3.3 —— `docs/00-engagement-plan.md` —— [A]。

**待改进一（High）：存在退出逐车主同意模型的路径。** `vehicle_specs`/`vehicle_pricing_info` 仅 Partner Token 可用且对任意车辆无需车主授权 —— 来源：Tesla Fleet API 认证总览 —— 同上 —— [A]。这是**明确的 High 级授权控制例外**，须以**契约 + 审计补偿**（§3.3 建议）管理 —— 来源：审计计划 §3.3 —— 同上 —— [A]。**本报告判断**：该路径的正当性依赖"规格/定价不属个人数据"的假设，一旦未来规格数据被用于个体推断，该例外的影响面会上升。

**待改进二（Low/可用性）：配额共享与"超限不恢复"的耦合。** 同账号多应用共享限额（§17.2.6.1）与"超限移除推流且不恢复"（§17.2.6.2）在多应用/车队场景下可能造成**合规应用的连带停流**。它在安全上激进（宁可停服不可失控），在可用性上有代价 —— 来源：Tesla Fleet API Billing and Limits —— 同上 —— [A]。是否提供按应用分池或恢复宽限，本次未取证（待补证）。

#### 17.2.8.3 Tesla 节小结

Tesla 的授权模型可概括为"**三层叠加、双上限、多路撤销**"：云层（令牌 + scope + 增量授权）、配对层（虚拟密钥 + 车主动作 + <20 上限）、校验层（车端逐条验签）；双上限指密钥 <20 把与推流 ≤5 应用；多路撤销指云 consent、scope 联动、车端删钥。**本报告判断（推测，非事实）**：这一模型在"公开文档最完整的车-云第三方授权实现"中确属标杆，但**并非无缺口**——其 High 级例外（Partner 专属 scope）与**多层文档未覆盖的实现细节**（私钥存储标准、公钥轮换、缓冲保护等）构成对外部复现者的**主要不确定区**，均已在 §17.9 汇总。

---

## 17.3 Mercedes-Benz 完整实践剖析

Tesla 一节确立的是"公开文档最完整"的标尺。Mercedes-Benz 则是**第二条标尺**：它的公开文档在**OAuth 实现细节**与**scope 命名空间约定**两个方向上尤其具体，且其"同意——合规"耦合的表态最为直白。本节按信源档案 §7.2（全部 [A]，来源 developer.mercedes-benz.com）逐项剖析，并把与 Tesla 的**结构差异**随时点出，以便在 §17.7 横向对照时直接引用。

### 17.3.1 平台与产品结构

**原文事实**：Mercedes-Benz 开发者平台为 `https://developer.mercedes-benz.com`，其**运营主体为 Mercedes-Benz Connectivity Services GmbH**（页脚版权 "© 2026"）—— 来源：Mercedes-Benz Developer Platform —— `https://developer.mercedes-benz.com/` —— [A]。平台**产品分类为五类**：**Fleet Data、Smart Vehicle Data、Infrastructure Data、Vehicle Commerce Data、Repair & Maintenance Data** —— 来源：同上 —— [A]。

**结构剖析（本报告判断，推测，非事实）**：把这五类名称并置，可以读出一条**面向对象的分层逻辑**——

| 产品分类（文档原文） | 字面语义 | 本报告推测的数据对象 | 与授权的关联 |
|---|---|---|---|
| Fleet Data | 车队数据 | 面向企业车队运营的车辆集合数据 | 企业契约路径，可能对应 Client Credentials |
| Smart Vehicle Data | 智能车辆数据 | 面向单车主的车辆状态/感知数据 | 个人数据取向，可能对应授权码流 |
| Infrastructure Data | 基础设施数据 | 充电/停车等外部基础设施数据 | 可能不涉车主个人数据 |
| Vehicle Commerce Data | 车辆商业数据 | 车相关的交易/商务数据 | 商业化取向，需企业侧凭证 |
| Repair & Maintenance Data | 维修与保养数据 | 服务历史/维保数据 | 可能与所有者信息耦合（个人数据） |

**必须强调**：上表"数据对象"与"与授权的关联"两列均为**本报告推测**，因为信源档案 §7.2 **仅取证到五类产品的名称**，未取到各类产品的详细说明页。本报告**不臆造**任何一类产品的 scope 或端点——凡进入 §17.7 对照表的 Mercedes 行，均只使用已取证的 scope 与流程事实。

**运营主体的意义（本报告判断）**：运营主体是 **Mercedes-Benz Connectivity Services GmbH**（一家以"连接服务"命名的德国有限责任公司），而**不是**整车研发主体。这与 Tesla 由 developer.tesla.com（品牌直营域名）直接承载开发者文档形成对照。其工程含义是：**车云数据访问的对外接口，被放在一个专门的"连接服务"法人实体下**，这一实体划分本身即是一种**责任边界切分**——数据访问的合规与运营责任，落在连接服务实体上。这一点在 §17.4 分析 CARIAD（集团软件子公司）时会再次出现，构成国际车企"**集团—子公司—平台**"三级分层的一个共同特征。

**GDPR 同意表述原文**：平台首页写明——"**The trust and consent of our vehicle customers are at the heart of our business – ensuring GDPR compliance and enabling secure, reliable data you can depend on.**"（"我们车辆客户的信任与同意是我们业务的核心——确保 GDPR 合规，并提供您可以依赖的安全、可靠数据。"）—— 来源：Mercedes-Benz Developer Platform 首页 —— `https://developer.mercedes-benz.com/` —— [A]。

这句原文已在 §17.1.2 作为"合规底座"的一手证据引用。在 §17.3 的语境下，它还有一层**产品结构层面的含义**：它把"**客户同意**"提升为业务的"核心"（at the heart of our business），而不是只在法务条款里一笔带过。**本报告判断（推测，非事实）**：这种"把同意写进首页价值主张"的做法，与"五类产品中至少 Smart Vehicle Data / Repair & Maintenance Data 涉及车主个人数据"这一（推测的）产品现实是自洽的——因为一旦产品线中有人数据取向的 API，同意机制就不再是可选项，而必须被公开承诺。

### 17.3.2 两种鉴权模式的适用边界

**原文事实**：Mercedes 文档页**明确列出两种鉴权集成模式**——OAuth **Authorization Code Flow** 与 **Client Credentials Flow** —— 来源：Mercedes-Benz 产品文档 —— `https://developer.mercedes-benz.com/product-docs` —— [A]；采用授权码流的理由（原文意译）："**部分 API 提供燃油状态、车门锁状态等数据，属 GDPR 意义上的个人数据，因此需要终端用户同意**"，平台自称使用 "**standard OAuth 2.0**" —— 来源：Mercedes-Benz 授权码流文档 —— `https://developer.mercedes-benz.com/get-started/oauth/authorization-code-flow` —— [A]。

**两种模式的规范定位**（依据 RFC 6749，[A]）：**Authorization Code Flow** 是 OAuth 2.0 中"**代表资源所有者（真人用户）行事**"的标准模式——它要求资源所有者（车主）在授权服务器上认证并同意，授权服务器再下发授权码，客户端以码换令牌。**Client Credentials Flow** 则是"**客户端以自己的身份行事**"的模式——没有终端用户参与，客户端直接用自己注册的凭证换令牌 —— 来源：RFC 6749 —— `https://www.rfc-editor.org/rfc/rfc6749.txt` —— [A]。

**适用边界的推演（本报告判断，推测，非事实）**：把 Mercedes 已取证的表述与 RFC 6749 的两种模式定义合起来，可以推演出如下**适用边界**（请注意：以下为推演，Mercedes 文档**未逐产品明示**哪一类产品对应哪一流）：

1. **Authorization Code Flow 用于"涉及车主个人数据"的 API**。文档已给出判据——"燃油状态、车门锁状态等属 GDPR 意义上的个人数据，因此需要终端用户同意"。**顺着这条判据推演**：凡访问"某个具体车主的车"的数据（状态、位置、命令），逻辑上都落在需要**逐车主同意**的一侧，因而应走授权码流。这与 Tesla 的 third-party token（代车主行事）在**架构角色上对应**（**本报告判断**）。
2. **Client Credentials Flow 用于"不涉及终端用户、或由企业以自身身份访问"的 API**。典型如：车队运营方以企业身份读取其名下车辆的聚合数据、或访问与个人无关的基础设施/商务数据。这条路径**没有"车主在场"的同意采集**，其授权基础是**企业契约**——与 Tesla 的 partner token（退出逐车主同意模型）在**架构角色上对应**（**本报告判断**）。

**为什么必须提供两种模式（本报告判断，推测，非事实）**：这与 §17.2.1 对 Tesla 三类令牌的分析**同构**。只做授权码流，则企业级批量场景（车队、维保网络、基础设施）无法落地；只做 Client Credentials，则违反"个人数据需终端用户同意"。因此**成熟的车云开放平台往往同时提供两条鉴权路径**，并把"是否涉及终端用户"作为模式选择的**分界判据**。Mercedes 把这条分界**写在文档的鉴权模式层**（而非令牌类型层），而 Tesla 把它**写在令牌类型层**（third-party vs partner）——两者是**同一治理问题的两种工程表达**。这一对照将在 §17.7 的横向表中作为一列（"同意模型"）体现。

**残余风险（本报告判断，推测，非事实）**：模式选择若**仅由开发者自律**（即文档告知"哪类数据该用哪种流"，但技术上不强制），则存在**误用风险**——开发者可能以 Client Credentials 去访问本应逐车主同意的数据。文档是否在**服务端强制**"某类 scope 只接受某类流"，本次未取证（信源档案 §7.2 只取到两种模式的存在与授权码流的理由），列入 §17.9。

### 17.3.3 授权码五步流程的逐步剖析

**原文事实**：Mercedes 的授权码流程为**五步**——**① 重定向浏览器至授权端点；② 用户认证并采集同意；③ 携带授权码回调；④ 用授权码换取访问令牌；⑤ 以令牌代表终端用户调用 API** —— 来源：Mercedes-Benz 授权码流文档 —— `https://developer.mercedes-benz.com/get-started/oauth/authorization-code-flow` —— [A]。文档给出的**授权端点示例**为 `https://ssoalpha.dvb.corpinter.net/v1/auth?response_type=code&client_id=...&redirect_uri=...&scope=...&state=...`；**令牌端点**为 `https://ssoalpha.dvb.corpinter.net/v1/token` —— 来源：同上 —— [A]。

下面逐步剖析，并给出参数表与错误语义。**注意**：参数表依据 RFC 6749（[A]）与文档已取证参数拼装；凡文档未明示者，本报告标注为"RFC 标准参数，文档未显式列举"。

#### 17.3.3.1 第一步：重定向浏览器至授权端点

**原文事实**：第一步为"**重定向浏览器至授权端点**" —— 来源：同上 —— [A]。授权端点示例含 `response_type=code`、`client_id`、`redirect_uri`、`scope`、`state` —— 来源：同上 —— [A]。

| 参数 | 文档是否显式出现 | 语义 | 工程含义 |
|---|---|---|---|
| `response_type=code` | 是（示例含） | 声明用授权码模式 | 排除隐式流，令牌不经浏览器前置通道（对齐 OAuth 2.1 草案废弃隐式流方向，[A]） |
| `client_id` | 是 | 客户端标识 | 用于定位注册的 redirect_uri 与 scope 白名单 |
| `redirect_uri` | 是 | 回调地址 | 必须与注册值一致，否则触发 "Invalid redirect URL" |
| `scope` | 是 | 请求权限 | 例：`openid offline_access mb:vehicle:mbdata:fuelstatus` |
| `state` | 是 | 防 CSRF 的随机值 | 回调时比对，阻断授权请求伪造（RFC 6749 定义） |

**错误语义**：若请求的 scope 未在客户端注册，报 **`invalid_scope` → "No registered scope value for this client has been requested"**；若 redirect_uri 与注册值不一致，报 **"Invalid redirect URL"** —— 来源：同上 —— [A]。

**工程含义（本报告判断）**：`invalid_scope` 报错文案中的关键词是"**No registered scope value for this client**"——它揭示 Mercedes 的 scope 是**按客户端注册**的（即每个客户端有各自的 scope 白名单），而非"平台全部 scope 向所有客户端开放"。这是一个**默认最小权限**的姿态：客户端只能请求自己被批准的那部分 scope。这与 §17.2.6.3 中 Tesla 的"分层限额"思路不同——Tesla 限制的是**速率**，Mercedes 限制的是**权限面**。

#### 17.3.3.2 第二步：用户认证并采集同意

**原文事实**：第二步为"**用户认证并采集同意**" —— 来源：同上 —— [A]；同意界面**展示所请求的 SCOPE 与 "purpose URL"**，便于终端用户知情决策 —— 来源：同上 —— [A]。

**工程含义（本报告判断）**：这一步是**授权码流与 Client Credentials 流的根本分界**——只有授权码流有"用户在授权服务器上认证并当面同意"这一环节。工程上它意味着 Mercedes 的授权服务器**必须承载一套同意 UI**，且该 UI 要能渲染 scope 与 purpose URL。这一步的存在，使"用户同意"成为**可留痕、可举证**的一手记录——这正是 §17.1.2 所述"车企侧把同意作为合规义务"的**技术落点**。

**与 §17.3.4 的衔接**：同意界面的设计质量（是否清楚展示 scope 与 purpose）直接决定"同意是否有效"，见 §17.3.4。

#### 17.3.3.3 第三步：携带授权码回调

**原文事实**：第三步为"**携带授权码回调**"（即授权服务器把 `code` 回传到 `redirect_uri`）—— 来源：同上 —— [A]。

**工程含义（本报告判断）**：这一步把"授权结果"从授权服务器送回**客户端后端**。安全要点有二：其一，`code` 是**短期、一次性**的中间凭证，其价值窗口很短；其二，`state` 必须在此比对。第三，回调地址**必须受客户端后端控制**——这也是 "Invalid redirect URL" 错误存在的原因：**redirect_uri 的严格校验**是防止授权码被投递到攻击者地址的关键控制（对齐 RFC 6749 对 redirect_uri 的强制校验要求）。

#### 17.3.3.4 第四步：用授权码换取访问令牌

**原文事实**：第四步为"**用授权码换取访问令牌**"；令牌端点为 `https://ssoalpha.dvb.corpinter.net/v1/token`；**客户端认证采用 HTTP Basic**（`clientId:clientSecret` BASE64 编码置于 Authorization 头）；**访问令牌有效期以响应 `expires_in` 字段为秒数，默认 3599 秒**（≈1 小时）；示例 JSON 含 `access_token`、`refresh_token`、`id_token` —— 来源：同上 —— [A]。

**错误语义**：**"Invalid grant"** 用于**授权码无效或已被使用** —— 来源：同上 —— [A]。

**工程含义**：这一步的安全细节密集，逐条解析——
- **HTTP Basic 客户端认证**：意味着客户端在换码时须以 `client_id` + `client_secret` 证明身份。RFC 6749 将 HTTP Basic（`client_secret_basic`）列为标准客户端认证方式之一 —— 来源：RFC 6749 —— `https://www.rfc-editor.org/rfc/rfc6749.txt` —— [A]。它的前提是**客户端是机密客户端（confidential client）**，即能安全保存 secret——因此文档强制"**客户端凭证必须保存在后端服务器**"（见 §17.3.6）。
- **`expires_in` 默认 3599 秒**：这是一个**约 1 小时**的短生命周期访问令牌。它与 §17.2 中 Tesla 的刷新令牌"3 个月 + 一次性"形成**不同侧重**——Mercedes 强调**访问令牌短寿**，Tesla 强调**刷新令牌一次性**。
- **"Invalid grant" 覆盖"授权码已被使用"**：这揭示授权码是**一次性**的（同一 code 二次换码报 Invalid grant），与 RFC 6749 一致（授权码必须一次性使用，重复使用应使已发令牌失效）。

#### 17.3.3.5 第五步：以令牌代表终端用户调用 API

**原文事实**：第五步为"**以令牌代表终端用户调用 API**"；客户端指引为——在**服务端应用缓存访问令牌与刷新令牌**；访问令牌**有效期内直接使用**，失效后由**缓存的刷新令牌换取** —— 来源：同上 —— [A]。

**工程含义（本报告判断）**：这一步明确了**令牌生命周期管理的工程范式**：访问令牌短寿（3599 秒）、刷新令牌长存（缓存在服务端）、过期即刷。其安全收益是：**即使访问令牌泄露，攻击窗口也只有约 1 小时**；而刷新令牌始终留在服务端，不暴露给客户端设备。这与 RFC 6749 的"短期访问令牌 + 长期刷新令牌"范式一致。**本报告判断**：Mercedes 把"缓存与刷新"的职责**明确压到服务端**，与其"客户端凭证不得下发"的强制要求共同构成**机密客户端模型**（confidential client）的完整落地。

### 17.3.4 同意界面与 purpose URL 的授权透明度设计

**原文事实**：同意界面的语义为——**展示所请求的 SCOPE 与 "purpose URL"**，便于终端用户知情决策；且 **`openid` scope 为获得有效令牌所必需，`offline_access` 为获得刷新令牌所必需** —— 来源：Mercedes-Benz 授权码流文档 —— `https://developer.mercedes-benz.com/get-started/oauth/authorization-code-flow` —— [A]。

**三方剖析**：

**(1) 为何展示 scope？** scope 是"应用将要获取哪些权限"的**机器可读清单**。把它展示给车主，是把授权决策的**信息基础**交给决策者。**本报告判断**：若同意界面只显示"某某应用请求访问你的车辆"而不列 scope，车主无法判断"是只读状态还是能远程开车门"——同意将沦为**盲目同意**。因此"**展示 scope**"是同意质量的第一关。

**(2) 为何展示 purpose URL？** 这是 Mercedes 相对特殊的做法——除了 scope 清单，还提供一个 "purpose URL"。**本报告判断（推测，非事实）**：purpose URL 的作用是**把"为什么需要这项权限"以人类可读的方式外链说明**——车主可以点进去看该应用声明的数据用途。这与 GDPR 的"目的限制（purpose limitation）与透明性"精神一致（**本报告判断**）；它把"数据处理目的"从法务文书**前置到同意界面**，从而提升同意的**知情度**。

**(3) 为何 `openid`/`offline_access` 是"必需"？** 文档明载二者是获得令牌/刷新令牌的**前提**。**本报告判断**：这实质是把 OIDC 的身份层（`openid`）与离线访问（`offline_access`）设为**平台的技术前置**——没有 `openid` 就没有有效令牌，没有 `offline_access` 就没有刷新令牌。这带来一个授权治理上的含义：**Mercedes 平台把"身份认证"作为"资源授权"的强制入口**，与 §17.2.2 中 Tesla 把 `openid`/`offline_access` 与资源 scope 分层但并列的做法**略有差异**——Tesla 是"分层可选"，Mercedes 在此处是"必需前置"。

**"同意质量"作为授权控制的关键（本报告判断，推测，非事实）**：把 §17.3.4 与 §17.3.3.2 合起来看，可以得到一条通用原则——**授权系统的实际安全性，很大程度取决于同意界面的质量**：因为"用户同意"是整个授权码流的**信任起点**，若起点就是盲目点击，则后续所有技术控制（令牌绑定、短寿、轮换）都建立在"用户其实没看懂"的沙地上。因此 **"展示 scope + purpose"是把同意从形式变为实质的关键一锤**。这一原则将在 §17.8 作为"通用方案应吸收的实践"之一列出。

**残余风险（本报告判断，推测，非事实）**：purpose URL 的**内容标准**（是否由平台审核、是否可能指向失效或误导页面）本次未取证；若 purpose URL 可被开发者任意填写且无审核，则"透明度设计"可能被反向利用（用看似正当的目的页骗取同意）。列入 §17.9。

### 17.3.5 scope 命名空间 `mb:vehicle:mbdata:fuelstatus` 的逐段拆解与治理价值

**原文事实**：Mercedes 的示例 scope 字符串（Fuel Status 产品）为 `scope=openid offline_access mb:vehicle:mbdata:fuelstatus` —— 来源：Mercedes-Benz 授权码流文档 —— `https://developer.mercedes-benz.com/get-started/oauth/authorization-code-flow` —— [A]。信源档案 §7.2 对这一约定的概括是：**"`mb:` 命名空间式 scope 约定：产品-域-资源三段式，是车企资源级 scope 设计的典型样本"** —— 来源：信源档案 §7.2 —— `docs/sources/source-dossier.md` —— [A]。

**逐段拆解（本报告判断，推测，非事实）**：把 `mb:vehicle:mbdata:fuelstatus` 按 `:` 切分，可读作四段：

| 段序 | 取值 | 本报告推测的语义 | 治理作用 |
|---|---|---|---|
| 1 | `mb` | 品牌/平台命名空间前缀（Mercedes-Benz） | 避免与其它厂商 scope 命名冲突；一眼可辨归属 |
| 2 | `vehicle` | 域（domain）：车辆域 | 把权限按**业务域**分层（区别于 `user`/`fleet` 等） |
| 3 | `mbdata` | 数据类型层（推测：Mercedes-Benz 车辆数据） | 区分"元数据层"与"具体资源" |
| 4 | `fuelstatus` | 具体资源（燃油状态） | **资源级**最细粒度，绑定单个数据类型 |

**治理价值（本报告判断）**：这种"**命名空间化 scope**"相对"裸字符串 scope"（如 `vehicle_cmds`）的核心优势有三：

1. **可扩展而不冲突**。新增资源只需追加一段（如 `mb:vehicle:mbdata:<新资源>`），不会与既有 scope 撞名，也不需要集中式注册数字编号。
2. **可解释性强**。命名本身携带层级语义，人（与审计工具）都能从字符串推断其所属域与资源，降低"scope 名不达意"导致的误授权。
3. **支持按前缀批量治理**。理论上平台可对 `mb:vehicle:*` 做**通配式策略**（例如"车辆域下的所有 scope 都需车主同意"），把治理规则**按命名空间**施加，而非逐个枚举（**本报告判断**）。

**与 RFC 9396（Rich Authorization Requests）的关系（本报告判断，推测，非事实）**：命名空间化 scope 是**在裸字符串 scope 之上做结构化**的一种轻量手段，但它在**表达力上仍弱于** RFC 9396 的 `authorization_details`——后者可表达"资源 + 动作 + 约束（如金额上限、时间窗）"的**结构化权限对象** —— 来源：RFC 9396 —— `https://www.rfc-editor.org/rfc/rfc9396.txt` —— [A]。命名空间 scope 只能表达"**是哪一类资源**"，无法表达"**对这类资源能做哪些具体动作/有何约束**"。因此，若未来车控需要"资源级 + 动作级 + 约束级"的三维授权，命名空间 scope 将遇到表达力天花板，需要向 `authorization_details` 演进——这是通用方案在车控场景下值得前瞻的一点（见 §17.8）。

**残余风险（本报告判断，推测，非事实）**：命名空间 scope 的**粒度精细化程度**取决于平台的**注册与审核**——若平台把过粗的命名空间（如 `mb:vehicle:mbdata:*`）当作单一 scope 授予，则名义上结构化、实际上仍是**粗粒度授权**。Mercedes 实际授予的 scope 粒度分布（是否已细化到 `fuelstatus` 单资源一级）本次只取证到**一个示例**，不足以概括全平台，列入 §17.9。

### 17.3.6 令牌端点与客户端认证

**原文事实**：Mercedes 令牌端点客户端认证采用 **HTTP Basic**（`clientId:clientSecret` BASE64 编码置于 Authorization 头）；**对开发者的安全要求**为——客户端凭证必须保存在**后端服务器**，应用"**不得**向客户端暴露任何客户端凭证（client id、client secret、访问令牌）"；**访问令牌有效期 `expires_in` 默认 3599 秒**；**刷新**为 `grant_type=refresh_token`，**刷新令牌一次性使用**，授权服务器返回**新的访问令牌与新的刷新令牌**；已用/无效刷新令牌报错 **"The given refresh token is not valid or was already used"**；客户端引导为**在服务端缓存访问令牌与刷新令牌** —— 来源：Mercedes-Benz 授权码流文档 —— `https://developer.mercedes-benz.com/get-started/oauth/authorization-code-flow` —— [A]。

逐条剖析：

**(1) HTTP Basic 客户端认证。** RFC 6749 将 HTTP Basic（`client_secret_basic`）列为标准客户端认证方式 —— 来源：RFC 6749 —— `https://www.rfc-editor.org/rfc/rfc6749.txt` —— [A]。**工程含义**：它把"客户端身份"与"用户身份"在换码请求中**分离**——Bearer 令牌代表用户，Basic 头代表客户端。**授权控制价值**：否定"仅凭 client_id 即可换码"的弱模型，要求客户端证明持有 secret（机密客户端模型）。

**(2) 凭证不得下发客户端——机密客户端模型的强制。** 文档要求凭证只存后端，且**明确禁止**把 client id/secret/access token 暴露给客户端设备。**工程含义**：这是把 OAuth 的"**机密客户端 vs 公共客户端**"划分**强制**在"机密"一侧。**授权控制价值**：高。若凭证下发到终端设备（移动 App/车机），则可被逆向提取，进而伪造客户端身份。强制后端保存，消除了"从设备中抠出 secret"这一常见攻击面。**本报告判断**：这也解释了为什么 Mercedes 未在公开文档中强调 PKCE（RFC 7636，面向公共客户端的授权码拦截防护）——因为在其强制机密客户端的模型里，PKCE 的核心场景被 secret 认证覆盖 —— 来源：RFC 7636 —— `https://www.rfc-editor.org/rfc/rfc7636.txt` —— [A]（规范存在性）。**但请注意**：这只是一种**推测**（本报告判断，非事实），Mercedes 是否支持 PKCE 本次未取证。

**(3) `expires_in` 默认 3599 秒。** 约 1 小时。**工程含义**：访问令牌短寿，使泄露窗口被压缩到 ≤1 小时。与 Tesla 的刷新令牌"3 个月"形成对照——**Mercedes 的核心令牌 TTL 是"短访问、长刷新"，Tesla 的核心约束是"刷新一次性"**。

**(4) 刷新令牌一次性 + 新令牌对。** 文档明载刷新返回**新的访问令牌与新的刷新令牌**，且**已用刷新令牌报错** "The given refresh token is not valid or was already used"。**工程含义**：这是**刷新令牌轮换（refresh token rotation）**的实现——每次刷新都换发新刷新令牌，旧令牌作废。**授权控制价值**：极高。它使"**刷新令牌被盗用**"可被**检测**——若攻击者用了旧刷新令牌，合法客户端下次刷新会失败（因为令牌已被轮换），从而暴露令牌泄露。这与 §17.2 中 Tesla"刷新令牌一次性 + 24 小时宽限"是**同一控制思想**（一次性轮换），只是 Mercedes 未取证到"宽限期"机制。

**(5) 错误语义 "The given refresh token is not valid or was already used"。** **工程含义**：该文案**同时覆盖**"无效"与"已被使用"两种情形——这对开发者是**排障友好**（明确告知可能是重复使用导致），但也意味着从错误文案无法区分"令牌过期"与"重放"（**本报告判断**）。审计视角下，若日志能记录"因已使用而失败"的事件，则该事件是**刷新令牌泄露的强指示信号**。

### 17.3.7 未取证方向逐项与补证方式

信源档案 §7.2 末尾明确列出 Mercedes 的**未取到方向**：**数字钥匙（CCC）、mTLS/证书固定、TEE/安全元件、OTA 安全、2024–2025 车辆数据 API 政策文档、MBition、Mercedes Pay** —— 来源：信源档案 §7.2 —— `docs/sources/source-dossier.md` —— [A，记录]。

**逐项补证方式（本报告建议）**：

| 未取证方向 | 为何重要（与授权的关系） | 补证方式 |
|---|---|---|
| 数字钥匙（CCC） | 近场授权（BLE/UWB/NFC）与云授权是两条平行授权链，缺一不能全貌 | 查 CCC 认证名单、Mercedes 车钥匙 App 技术说明、专利 |
| mTLS / 证书固定 | 车-云链路是否双向证书认证，决定"通道鉴权"强度 | 抓取车机流量（合规前提下）、查 TLS 握手、官方安全白皮书 |
| TEE / 安全元件 | 密钥与凭证是否受硬件保护，决定"私钥不可提取"是否成立 | 器件选型、FCC 拆解、芯片厂 design win |
| OTA 安全 | 更新授权的完整性（R156/SUMS 取向） | 官方 OTA 白皮书、固件签名验证研究 |
| 2024–2025 车辆数据 API 政策文档 | 授权策略的时间演进（scope/同意模型是否变化） | developer 站点的 changelog / 政策归档页 |
| MBition | 该子公司是否承担车云/授权平台研发，影响架构溯源 | 公司官网、招聘页、技术演讲 |
| Mercedes Pay | 车载支付涉及的令牌化与授权（金融级授权） | 官方产品页、PCI/令牌化文档 |

**必须强调（对齐红线 §3.2.4）**：以上七项**全部为"本次未找到公开来源"，绝不等于"Mercedes 不具备相应能力"**。本报告对 Mercedes 的授权与访问控制**只下已取证范围内的结论**（两条鉴权模式、五步流程、scope 命名空间、令牌端点细节），**不对未取证方向作任何否定性推断**。

---

## 17.4 Volkswagen Group / CARIAD：已取证自述口径逐条解读

与 Tesla、Mercedes 不同，大众集团（Volkswagen Group）及其软件子公司 **CARIAD** 在本次取证中**未取到任何开发者 API 文档**，只取到**企业自述的营销口径**（信源档案 §7.3 标注为 **[A，公司自述口径]**）。因此本节的写作纪律格外重要：**把"自述口径"与"技术事实"严格分开**，只解读口径本身的含义，不从中推断技术实现——凡属推断一律标**本报告判断（推测，非事实）**。

### 17.4.1 已取证自述口径逐条解读

**口径 1：CARIAD 的自我定位。** 原文——"**We are the Volkswagen Group's automotive software company... for iconic car brands, including Audi, Volkswagen and Porsche**"（"我们是大众集团的汽车软件公司……服务于包括奥迪、大众和保时捷在内的标志性汽车品牌"）—— 来源：CARIAD 官网 —— `https://cariad.technology/` —— [A，公司自述口径]。

**解读**：这条口径确立了 CARIAD 的**法律与组织定位**——它是**集团级的软件公司**，统辖多个品牌（Audi / Volkswagen / Porsche）的软件。**本报告判断（推测，非事实）**：这意味着大众集团的"车云授权"很可能**不是按品牌各自为政**，而是一个**集团级共享平台**（因为软件公司是统一主体）。这与 Mercedes 由"Connectivity Services GmbH"单品牌实体承载、Tesla 由品牌直营域承载，形成三种不同的**治理主体形态**（单品牌实体 / 品牌直营 / 集团软件子公司）。三种形态的对照见 §17.7。

**口径 2：Automotive Cloud 的定位。** 原文——"**Our cloud ecosystem connects the Volkswagen Group's vehicles, markets and services via a central platform**"（"我们的云生态通过一个中央平台连接大众集团的车辆、市场与服务"）—— 来源：CARIAD Automotive Cloud 页 —— `https://cariad.technology/de/en/solutions/automotive-cloud-connectivity.html` —— [A，公司自述口径]。

**解读**：关键词是"**central platform**（中央平台）"。**本报告判断（推测，非事实）**：若一个中央平台同时连接"车辆、市场、服务"三类对象，则其授权模型必然面临**多租户、多角色**的复杂性——车辆（资源）、市场（区域/业务）、服务（第三方服务商）各自需要不同的令牌类型与 scope 域。这与 Tesla 用"三类令牌 + 12 scope"覆盖"车/能源/用户/企业"四类资源是**同类复杂度问题**。**但必须强调**：本报告**未取到** CARIAD 的任何令牌类型、scope 或端点文档，因此**不能**说 CARIAD"采用"了任何具体授权模型——只能指出其自述的架构定位**蕴含**了多角色授权的需求（**本报告判断**）。

**口径 3：规模指标。** 指标条原文——"**1 ecosystem for all VW brands**"、"**45 million connected vehicles**"、"**90 markets connected**"、"**365 days global support**"；正文另称"**超过 4500 万辆网联车**"、"**全球最大的汽车云基础设施**" —— 来源：同上 —— [A，公司自述口径]。

**解读**：**4500 万辆、90 个市场**是**规模自述**（非第三方审计数据，标记为自述口径）。**本报告判断（推测，非事实）**：如此规模下的"授权与访问控制"面临**两个放大效应**——其一，**横向影响面放大**：任一漏洞的潜在影响车辆数可能达千万级（对应审计计划 §3.3 中 Critical/High 的判据在超大规模下的严峻性）；其二，**治理一致性压力**：90 个市场涉及不同司法辖区（欧盟 GDPR、各地数据法），授权模型必须**可配置地适配多辖区**。这两点是"大规模平台授权"相对"小规模平台"的**结构性差异**。

**口径 4：数据平台与 OTA。** 原文——同页称数据平台是"**所有车辆相关 AI 创新的关键使能器**"，云支持"**安全关键更新**"的 OTA 下发 —— 来源：同上 —— [A，公司自述口径]。

**解读**：这条把"数据平台"与"AI 创新"绑定，并明确云承担"**安全关键更新**"的 OTA 下发。**本报告判断（推测，非事实）**：把"安全关键更新（safety-critical updates）"的 OTA 下发放在云侧，意味着该下发的**授权与完整性**控制成为安全关键项——对应联合国 UN R156（SUMS 软件更新管理体系）与 OTA 侧标准（如 Uptane/TUF 的更新授权模型）所关注的"更新授权"领域。**但请注意**：CARIAD 自述中**未出现** R155/R156 的合规声明（见 §17.4.2 未取证项），因此本报告**不把**"自述的 OTA 能力"与"R156 合规"相等同——这是**红线 §3.2.3（不得以记忆填补）** 的直接要求。

**口径 5：站点产品分类。** 原文——站点产品分类为 **Infotainment、Automated Driving、Connectivity & Cloud、Motion & Energy** —— 来源：同上 —— [A，公司自述口径]。

**解读**：这四类中，**"Connectivity & Cloud"** 是与本节主题（授权与访问控制）最相关的一类。**本报告判断（推测，非事实）**：把"连接与云"与"信息娱乐""自动驾驶""运动与能量"并列为四大产品域，说明"云/连接"在 CARIAD 的产品结构中**是一等公民**，而非附属功能。这与其"中央平台"定位自洽。

### 17.4.2 未取证方向逐项

信源档案 §7.3 明确列出 VW/CARIAD 的**未取到项**：**E3 架构、VW.OS、ID 系列 OTA 细节、UN R155 集团合规声明、与 Mobileye/Bosch 的合作、任何 CARIAD 安全白皮书**；并且 **VW Newsroom 对 `R155` 的站内检索返回零结果项** —— 来源：信源档案 §7.3 —— `docs/sources/source-dossier.md` —— [A，记录]。

| 未取证方向 | 与授权/访问控制的关系 | 补证方式 |
|---|---|---|
| E3 架构 | 决定车云分层的硬件/软件底座（服务导向架构） | 技术演讲、专利、车型拆解 |
| VW.OS | 车端操作系统，是车端授权校验的落地处 | 官方发布材料、开发者报道 |
| ID 系列 OTA 细节 | OTA 的下发授权与完整性 | 车型 OTA 说明、固件分析研究 |
| UN R155 集团合规声明 | CSMS 合规是"授权/访问控制"的合规底座 | 官方合规公告、型式认证记录 |
| 与 Mobileye/Bosch 的合作 | 第三方在车云/感知链中的授权边界 | 官方新闻稿、合作公告 |
| CARIAD 安全白皮书 | 最直接的授权架构一手来源 | 官网安全页、投资者材料 |

**"VW Newsroom 对 R155 检索零结果"这一观察的含义（本报告判断）**：它**只说明**"本次在该站内检索未命中 R155"，**不等于**"大众集团未开展 R155 合规工作"。按 **红线 §3.2.4**，"未找到公开来源"**绝不等于能力缺失**。本报告对 VW/CARIAD 的授权与访问控制**不下任何否定性结论**。

### 17.4.3 本报告判断（推测）：集团架构对车云授权治理的含义

> **本节整节均为"本报告判断（推测，非事实）"**，依据是 §17.4.1 的企业自述口径与 §17.3.1 对 Mercedes 运营主体的观察，**不含任何已取证的技术事实**。写作目的是**提出待验证的假设**，供补证后修正。

**（一）"集团软件子公司"形态如何改变授权治理的责任结构。** 把大众（CARIAD 统辖 Audi/VW/Porsche）与 Mercedes（Connectivity Services GmbH 单品牌）并置，可以看到**治理主体的两种切法**：一种是**跨品牌共享一个软件公司**（集团内集中），一种是**单品牌一个连接服务实体**（品牌内集中）。**本报告判断（推测，非事实）**：这两种切法对授权治理各有含义——

- **集团内集中**（如推测的大众形态）的潜在收益是**一次投入、多品牌复用**——scope 命名空间、令牌模型、同意机制可跨品牌统一，避免"每个品牌各自造一套 OAuth"。其潜在代价是**单点性与一致性难题**：一个集团平台的授权缺陷会**同时影响多个品牌**（呼应 §17.4.1 口径 3 的横向放大）；且不同品牌可能有不同的隐私定位（如保时捷与大众的用户预期不同），统一模型未必处处合宜。
- **单品牌集中**（如 Mercedes 形态）的收益是**边界清晰、责任单品牌可界定**；代价是**跨品牌协同时需跨实体对接**（例如集团内多品牌共享数据的场景）。

**（二）"中央平台连接车辆、市场、服务"隐含的三类授权主体。** 若 CARIAD 自述的"中央平台"确实同时承载"车辆—市场—服务"，那么逻辑上它需要**至少三类授权主体**：**车辆（资源所有者侧，如车主/车队）、市场（区域业务侧）、服务（第三方服务商）**。**本报告判断（推测，非事实）**：这与 Tesla 的"三类令牌"（third-party / partner / for-business）在**功能维度上同构**，但组织维度更复杂（多了"市场/区域"这一轴）。若未来车控授权要跨 90 个市场适配不同辖区规则，则**授权策略必须在"主体×资源×辖区"三维上可配置**。这是一个**仅凭自述口径提出的结构性假设**，**未取到任何 CARIAD 文档佐证**。

**（三）"安全关键更新的 OTA 下发"提示的授权控制点。** 自述明确云承担"安全关键更新"的 OTA 下发。**本报告判断（推测，非事实）**：从授权视角看，OTA 下发的控制点至少包括——**下发的授权对象**（谁能触发一次更新）、**下发的完整性**（更新包是否被授权与签名）、**下发的可追溯**（谁在何时批准了这次更新）。这三者分别对应"授权—完整性—审计"三条线，也是 Uptane/TUF 一类更新安全框架的核心关注 —— 来源：Uptane Standard —— `https://uptane.org/docs/latest/standard/uptane-standard` —— [A]。**但本报告未取到 CARIAD 采用任何具体 OTA 安全框架的证据**，故此处**仅指出"授权控制点在哪"，不指认"它用了什么"**。

**（四）对通用方案复现者的含义。** 综合以上三点，**本报告判断（推测，非事实）**：面向大型集团车企的通用车云授权方案，应至少满足三条**结构性要求**——(1) **多品牌/多实体可共用一套授权基础设施**（scope 命名空间与客户端注册需支持多租户隔离）；(2) **授权策略在"主体×资源×辖区"上可配置**（而非硬编码单辖区规则）；(3) **OTA 等"安全关键下发"独立于普通 API 的授权链**（避免普通数据 API 的授权缺陷波及更新下发）。这三条**均为推断**，其成立性依赖对 CARIAD 实际架构的补证。

---

## 17.5 BMW：取证失败全记录与中立性声明

按审计计划 §3.1 与信源档案 §0 的纪律，BMW 一节**不写"BMW 的授权模型如何"，只写"本次取证为何失败、失败到什么程度、以及不因此做什么推断"**。

### 17.5.1 取证失败全记录（逐条观测）

以下每一条均为**直接观测**（[A，直接观测]），来源：信源档案 §7.4 —— `docs/sources/source-dossier.md` —— [A]：

| # | 目标 | 观测结果 | 性质 |
|---|---|---|---|
| 1 | `https://developer.bmwgroup.com/` | DNS 可解析（160.46.244.54），但返回 **Apache 占位页**："BMW Group – no content deployed … This project didn't deploy any content yet"；`Last-Modified` 头为 **2026-04-27**；**未提供 CarData / OAuth 任何文档** | 站点可达，但无内容 |
| 2 | `https://crd.bmwgroup.com/` | **无法解析**（DNS 失败） | 不可达 |
| 3 | `https://b2b-developer.bmwgroup.com/` | **超时** | 不可达 |
| 4 | `www.bmw.com` / `www.bmwgroup.com` | 从本网络**被区域封锁**（HTTP 000 / 边缘封锁） | 区域封锁 |
| 5 | `www.bmwgroup.com/en/innovation/vehicle-data.html` | 经浏览器返回**站点自身 404** | 页面不存在 |
| 6 | `https://b2b.bmw.com` | **可达**，但为**供应商采购门户**（purchasing / logistics 登录），**并非**车辆数据开发者 API 门户 | 可达但非目标门户 |

### 17.5.2 不得据此做出的推断（中立性声明）

**声明（对齐红线 §3.2.4 / AC-11）**：上表六条**只证明"本次未能取到 BMW 的授权与访问控制文档"**，**不证明**以下任何一项：

- **不**证明 BMW 没有 CarData / OAuth / 数字钥匙 / 安全白皮书；
- **不**证明 BMW 的授权控制弱于 Tesla 或 Mercedes；
- **不**证明 `developer.bmwgroup.com` 的占位页代表 BMW 长期不提供开发者门户（`Last-Modified 2026-04-27` 只说明该占位页**当时**的状态）。

信源档案 §7.4 已明确：**"未取到：BMW CarData OAuth scope 清单、令牌有效期、CCC 数字钥匙、BMW 安全白皮书。原因是网络/检索封锁，不得据此推断 BMW 无相应方案。"** 本报告严格遵循该纪律。**BMW 在本章属于"披露缺口"，不是"能力缺口"** —— 这一区分是本章中立性的核心。

### 17.5.3 补证动作清单

| 动作 | 具体做法 | 预期产出 |
|---|---|---|
| 换出口 IP | 从非区域封锁网络重跑 `curl`/浏览器直取 | 验证 `bmwgroup.com` / `bmw.com` 是否可达 |
| 代理重跑 | 经合规代理访问占位页与 CarData 页 | 确认是否有内容或跳转 |
| 重新探测开发者域 | 复核 `crd.bmwgroup.com` / `b2b-developer.bmwgroup.com` 的 DNS 与路由 | 排除 DNS 临时故障 |
| 抓取采购门户说明 | 从 `b2b.bmw.com` 公开帮助页读取接入流程 | 了解 B2B 数据接入是否有 OAuth |
| RFI（信息征询） | 通过正式渠道向 BMW 索取 CarData 技术概览 | 一手 scope / 令牌文档 |
| 恢复检索额度 | `web_search` / `web_extract` 恢复后做开放发现 | 定位 CarData 文档与安全白皮书 |

**再次声明**：在完成上述补证并取得一手证据之前，本报告**不为 BMW 的授权与访问控制能力做任何推断**（无论正面或负面）。

---

## 17.6 Rivian：取证失败全记录与中立性声明

Rivian 一节的结构与 BMW 相同——**只记录取证失败与不做的推断**。

### 17.6.1 取证失败全记录

以下每一条均为**直接观测**（[A，直接观测]），来源：信源档案 §7.5 —— `docs/sources/source-dossier.md` —— [A]：

| # | 目标 | 观测结果 | 性质 |
|---|---|---|---|
| 1 | `https://rivian.com` | 从本出口返回 **Amazon CloudFront 403**，正文为："**The CloudFront distribution is configured to block access from your country**" | 区域封锁 |
| 2 | `developer.rivian.com` | **无 DNS 解析** | 不可达 |
| 3 | `api.rivian.com` | **可解析**（13.35.190.19），但为 **App 后端**（非公开开发者门户） | 可达但非门户 |

### 17.6.2 不得据此做出的推断（中立性声明）

**声明（对齐红线 §3.2.4 / AC-11）**：上表三条**只证明"本次未能取到 Rivian 的车云授权文档"**，**不证明**：

- **不**证明 Rivian 没有 Fleet API / OAuth / 数字钥匙文档；
- **不**证明 `api.rivian.com` 的 App 后端属性代表 Rivian 无开发者平台（`developer.rivian.com` 无解析可能是**域名未启用**而非"不打算提供"）；
- **不**证明 Rivian 的授权控制弱于任何车企。

信源档案 §7.5 已明确：**"未取到：Rivian Fleet API、OAuth 支持、数字钥匙文档。原因同上。"** 本报告严格遵循。**Rivian 在本章属于"披露缺口"，不是"能力缺口"。**

### 17.6.3 补证动作清单

| 动作 | 具体做法 | 预期产出 |
|---|---|---|
| 换出口 IP | 从非封锁网络访问 `rivian.com` | 确认站点正文与开发者入口 |
| 探测子域 | 复核 `developer.rivian.com` 等子域的 DNS 记录变更 | 判断是否为临时未启用 |
| 恢复检索额度 | 检索 Rivian 开发者/车联文档 | 定位 Fleet API 或 OAuth 文档 |
| RFI | 通过正式渠道向 Rivian 索取车云接入资料 | 一手文档 |
| 第三方交叉 | 从权威第三方（认证机构/媒体）间接了解 | [B]/[C] 级线索 |

**再次声明**：补证完成前，本报告**不为 Rivian 的授权与访问控制能力做任何推断**。

---

## 17.7 国际车企授权与访问控制的横向对照

本节把 §17.2–§17.6 的已取证事实压入**一张 14 行 × 7 列**的对照表（满足 AC-12 的"对照表"要求）。列的选取对齐审计计划 §4.5"对标基准法"约定的量化维度：**令牌类型、scope 粒度、同意模型、资源级策略、轮换机制**，另加"主体"与"证据等级"两列以保证可溯源。**凡未取证处一律写"未找到公开来源"，绝不推断为"无"。**

| 主体 | 令牌类型 | scope 粒度 | 同意模型 | 资源级策略 | 轮换机制 | 证据等级 |
|---|---|---|---|---|---|---|
| Tesla · third-party token | Bearer；代车主行事 | 12 scope 之一部（vehicle_device_data / vehicle_location / vehicle_cmds / vehicle_charging_cmds / energy_* / user_data 等） | **逐车主同意**（授权码流） | `hide_private` 车即使持 `vehicle_location` 亦拒位置（403） | 刷新令牌一次性 + 3 个月过期 + 24h 宽限 | [A] |
| Tesla · partner token | Bearer；企业契约 | `vehicle_specs` / `vehicle_pricing_info` **仅此路径** | **不进逐车主同意模型** | 无逐车主资源级策略（对任意车辆可访问） | 同上 | [A] |
| Tesla · third-party-for-business token | Bearer（文档列为第三类） | 文档未展开细则 | 文档未展开 | 文档未展开 | 同上 | [A，仅名称] |
| Tesla · 虚拟密钥（车端） | 非令牌：P-256 公私钥对 | 绑定"命令/遥测配置"两类载荷 | 反方向：车主在车端**添加公钥** | 车辆在执行/接受配置前**逐条验签** | **车主在 Locks 界面删密钥**吊销 | [A] |
| Tesla · Fleet Telemetry 流 | 签名配置 + 已配对密钥 | 字段级（7 个位置字段绑 `vehicle_location`；`include_fields`） | scope 授权为前置 | `hide_private` → 403 "location access not granted" | **scope 撤销→配置从车辆移除**；单车 ≤5 应用 | [A] |
| Mercedes · Authorization Code Flow | 访问令牌 + 刷新令牌 + id_token | 命名空间式（`mb:vehicle:mbdata:fuelstatus`） | **逐终端用户同意**（展示 scope + purpose URL） | scope 按客户端注册（白名单） | `expires_in` 默认 3599 秒；刷新一次性换新令牌对 | [A] |
| Mercedes · Client Credentials Flow | 客户端自身身份令牌 | 文档未展开 | **无终端用户参与**（企业契约） | 文档未逐产品展开 | 文档未展开 | [A，仅模式存在] |
| Mercedes · 令牌端点认证 | HTTP Basic（clientId:clientSecret） | — | — | 强制凭证仅存后端、**不得下发客户端** | 刷新令牌一次性；已用报错 | [A] |
| Volkswagen Group / CARIAD | **未找到公开来源** | **未找到公开来源** | 自述"中央平台连接车辆/市场/服务"（不构成同意模型证据） | **未找到公开来源** | **未找到公开来源** | [A，仅自述口径] |
| BMW | **未找到公开来源** | **未找到公开来源** | **未找到公开来源** | **未找到公开来源** | **未找到公开来源** | [A，直接观测：占位页/封锁] |
| Rivian | **未找到公开来源** | **未找到公开来源** | **未找到公开来源** | **未找到公开来源** | **未找到公开来源** | [A，直接观测：CloudFront 封锁] |
| 通用方案基线（RFC 系） | 承载无关；定义 Bearer / JWT / mTLS / DPoP 等 | 裸字符串 scope（RFC 6749）→ 结构化 `authorization_details`（RFC 9396） | 授权码流（RFC 6749）为基准；公共客户端强制 PKCE（RFC 7636） | 资源级由 RS 自行实现（无强制规范） | 刷新令牌轮换为最佳实践；吊销端点 RFC 7009；发送方约束 RFC 9449 | [A] |
| 数字钥匙生态（近场） | 非 OAuth：SE 内密钥 + BLE/UWB/NFC | 车端本地权限（非云 scope） | 近场配对与本地授权 | 由 CCC 规范与 SE 实现 | 密钥生命周期由数字钥匙体系管理 | [A（CCC 3.0 发布公告）/ 未验证（规范正文）] |
| 中国数字钥匙参考（对照） | 国标 GB/T 44402.1 数字钥匙系统参考架构 | 国标定义 | 国标定义 | 国标定义 | 国标定义 | [A] |

来源：Tesla 各行为 §17.2 已标注的 developer.tesla.com 页面；Mercedes 各行为 §17.3 已标注的 developer.mercedes-benz.com 页面；CARIAD 为 §17.4 的 cariad.technology 自述口径；BMW/Rivian 为 §17.5/§17.6 的直接观测；通用方案基线为 `docs/sources/source-dossier.md` §2.1 所列 RFC；数字钥匙生态为 dossier §5（CCC）；中国数字钥匙为 dossier §1.2（GB/T 44402.1-2024）—— [A]。

### 17.7.1 差异归因（三点）

**归因一：文档公开度决定"证据密度"，而非"技术强弱"。** 表中 Tesla / Mercedes 行填满，BMW / Rivian / CARIAD 大片"未找到公开来源"。**本报告判断**：这一差异的**直接原因是本次取证的区域封锁与检索受限**（信源档案 §0），**不是**车企技术能力的排序。**任何把"空白行"读成"能力弱"的解读都违反红线 §3.2.4。** 表中之所以保留空白而非省略行，正是为了**显式化披露缺口**（对齐 AC-8）。

**归因二：同一治理问题有两种工程表达。** Tesla 把"是否需要逐车主同意"写在**令牌类型层**（third-party vs partner），Mercedes 把同一分界写在**鉴权模式层**（Authorization Code vs Client Credentials）。**本报告判断**：二者**同构**——都是用"两条路径"的显式分离来避免"企业批量场景无路可走、或人数据被非同意访问"的两难（见 §17.2.1、§17.3.2）。这说明"**双路径授权**"是国际车企的**收敛做法**，值得通用方案吸收。

**归因三：资源级策略是"第二层"，且形态各异。** Tesla 的第二层是 `hide_private`（对位置字段），Mercedes 的第二层是"scope 按客户端注册 + purpose URL"。**本报告判断**：两者都体现"**授权被授予 ≠ 资源可访问**"——真正的访问性由**独立于 OAuth 授权的资源级策略**再次裁量（见 §17.2.2）。这是本章反复出现的核心模式。

---

## 17.8 国际实践对通用方案的验证与修正

本节回答审计计划 §4 的"对标基准法"要求：用 §17.2–§17.7 的国际实践，**验证哪些通用控制已被实际落地**，并**指出哪些通用方案未在公开实现中出现**。凡"未出现"一律按"本次未找到公开来源"处理，**不得读作"车企未采用"**。

### 17.8.1 已被国际实践实际落地验证的通用控制

| 通用控制（规范来源） | 落地证据（本报告已取证） | 验证结论 |
|---|---|---|
| OAuth 授权码流代表资源所有者行事（RFC 6749） | Tesla third-party token；Mercedes Authorization Code Flow | **已验证**：两大标尺均以授权码流承载"逐车主同意" |
| 授权服务器元数据自动发现（RFC 8414 / OIDC Discovery 1.0） | Tesla `/.well-known/openid-configuration` | **已验证**：Tesla 公开元数据端点 |
| 身份与会话分层（OIDC Core 1.0：`openid`/`offline_access`） | Tesla 12 scope 含二者；Mercedes 明载二者"必需" | **已验证** |
| 刷新令牌轮换（最佳实践） | Tesla 刷新一次性 + 3 个月 + 24h 宽限；Mercedes 刷新一次性换新令牌对 | **已验证**（两家均实现一次性轮换） |
| 令牌吊销机制（RFC 7009） | Tesla 云 consent 撤销 + 车端删钥 + scope 联动移除配置 | **已验证**，且 Tesla 把吊销**延伸至车端与配置层** |
| 授权/资源服务器分离（RFC 6749 架构角色） | Tesla auth / fleet-auth / fleet-api 主机分离 | **已验证** |
| 受众绑定抑制令牌重放（RFC 9068 的 `aud` 校验取向） | Tesla `/token` 的 `audience` 必须为 Fleet API base URL | **已验证**（含区域绑定） |
| 资源级策略与授权解耦（"授权≠可访问"） | Tesla `hide_private`（位置字段 403） | **已验证**，审计计划判为正面案例 |
| 短生命周期访问令牌 | Mercedes `expires_in` 默认 3599 秒 | **已验证** |
| 机密客户端与凭证不下发 | Mercedes 强制凭证仅存后端 | **已验证** |
| 同意界面透明化（展示 scope 与用途） | Mercedes 展示 scope + purpose URL | **已验证** |
| 影响范围量化上限 | Tesla 密钥 <20 把、推流 ≤5 应用 | **已验证**（作为工程控制手段） |

**本报告判断（推测，非事实）**：上表说明**通用授权方案的"骨干"（授权码流、发现、轮换、吊销、受众绑定、资源级二次裁量）在国际实践中已被实际采用**。因此，通用方案若有"只讲理论不落地"的顾虑，可据此**增强信心**——至少 Tesla 与 Mercedes 两个标尺把骨干落了地。

**一条超出通用方案的控制：车端凭证校验。** Tesla 的虚拟密钥（§17.2.4）**不属于**经典 OAuth 通用方案的常规部分——通用 OAuth 把"资源服务器校验令牌"作为终点，而 Tesla **在资源（车辆）内部再加一道非对称验签**。**本报告判断**：这是本章对通用方案的**最重要修正建议**——**面向车控的授权，应在"云端令牌"之外，增加"资源侧（车端）独立凭证校验"**，以抵御"云授权链被绕过"的 Critical 级风险。通用方案若不包含此层，则在车控场景下存在**结构性缺口**。

### 17.8.2 未在公开实现中出现的通用方案（缺证据，不作反向推断）

| 通用方案（规范来源） | 已检索对象 | 结果 | 说明 |
|---|---|---|---|
| mTLS 客户端认证 + 证书绑定令牌（RFC 8705） | Tesla / Mercedes 开发者文档 | **未找到公开来源** | **不等于**两家未用 mTLS；Fleet Telemetry 仅见证书兼容性预检工具 |
| DPoP 发送方约束令牌（RFC 9449） | Tesla / Mercedes 开发者文档 | **未找到公开来源** | — |
| 富授权请求 `authorization_details`（RFC 9396） | Tesla / Mercedes 开发者文档 | **未找到公开来源** | 两家均用裸字符串/命名空间 scope，未见 RAR |
| Token Exchange 代理链（RFC 8693） | Tesla / Mercedes 开发者文档 | **未找到公开来源** | — |
| Step-up 认证挑战（RFC 9470） | Tesla / Mercedes 开发者文档 | **未找到公开来源** | — |
| 设备授权授予（RFC 8628，车机场景） | Tesla / Mercedes 开发者文档 | **未找到公开来源** | — |
| GNAP 授权协商（RFC 9635） | Tesla / Mercedes 开发者文档 | **未找到公开来源** | 属下一代方向，尚未见车云落地 |
| UMA 2.0 用户自管授权 | Kantara 站点 | **未验证**（站点 curl 超时） | 规范正文未取到 |

**关键纪律声明**：上表**不得**读作"国际车企未采用这些控制"。**它们只是"本次未在公开开发者文档中取证到"** —— 可能因文档未公开、或因该控制处于私有实现层。按红线 §3.2.4，"未找到公开来源 ≠ 不具备"。这些方向**全部进入 §17.9 待补证清单**。

### 17.8.3 对通用方案的三条"修正建议"（本报告判断）

**修正一：把"资源级二次裁量"从可选升级为必需。** 基于 Tesla `hide_private`（§17.2.2）与 Mercedes scope 白名单（§17.3.3.1），**本报告判断**：通用方案不应把"授权通过即放行"当作终点，而应在资源服务器侧**强制**执行"授权之上还有资源策略"的第二层判定（如车辆级 hide_private、字段级最小化、客户端级 scope 白名单）。

**修正二：为车控场景补上"车端凭证校验"层。** 基于 Tesla 虚拟密钥（§17.2.4），**本报告判断**：通用方案的"令牌 → 资源"链路在车控场景下应扩展为"令牌 → 车端凭证 → 资源动作"，由车端对载荷独立验签，以对抗云端单点失陷。

**修正三：把"撤销"做成端到端联动，而非仅令牌层。** 基于 Tesla 的"scope 撤销→遥测配置移除"（§17.2.5.3）与"超限→移除推流"（§17.2.6.2），**本报告判断**：通用方案的撤销应实现"**授权态变化 → 车端配置/数据流回收**"的端到端联动，避免"撤销了令牌、流还在跑"的失配。

---

## 17.9 本章待补证清单

本节汇总全章"未找到公开来源"与"待补证"项，供补证后修正结论（对齐 AC-8）。**所有条目均按"披露缺口 ≠ 能力缺口"处理。**

| # | 待补证项 | 归属主体 | 现状 | 补证方式 |
|---|---|---|---|---|
| 1 | GDPR 正文（条款级） | 通用/合规 | EUR-Lex 返回 HTTP 202，正文未取到 | 恢复后直取 EUR-Lex 或官方 PDF |
| 2 | 欧盟 Data Act 正文 | 通用/合规 | HTTP 202，正文未取到 | 同上 |
| 3 | UN R155/R156 条款与时间表 | 通用/合规 | unece.org Cloudflare 拦截 | 官方 PDF 直链 / 换出口 |
| 4 | ISO 21434 / 24089 / 15118 正文 | 通用/合规 | iso.org Cloudflare 拦截 | 标准购买渠道 / SAE 页 |
| 5 | Tesla 访问令牌 TTL | Tesla | 仅有刷新令牌 3 个月 + 24h 宽限 | 实机走一遍 token 响应读 `expires_in` |
| 6 | Tesla 虚拟密钥"可信用户"判定细则 | Tesla | 文档未描述 | 车端实现研究 / 官方补充文档 |
| 7 | Tesla 私钥存储标准（HSM/KMS 强制？） | Tesla | 文档仅有禁止性要求 | 官方安全白皮书 / 开发者问答 |
| 8 | Tesla 公钥轮换（dual-publishing）指引 | Tesla | 未见 | 开发者论坛 / 官方更新 |
| 9 | Tesla scope 部分撤销时的配置行为 | Tesla | 仅知"scope 撤销→配置移除"，未细分 | 文档或实测 |
| 10 | Tesla "能阻止 Tesla 后端"的独立验证 | Tesla | 仅厂商自述 | 第三方研究 / 车端实现 |
| 11 | Tesla 计费暂停是否影响令牌刷新 | Tesla | 未说明 | 官方计费文档 / 实测 |
| 12 | Tesla 4xx 计费的滥用防护 | Tesla | 未说明 | 官方文档 |
| 13 | Tesla 车端缓冲数据的存储保护 | Tesla | 未说明 | 车端实现研究 |
| 14 | Mercedes 是否服务端强制"某类 scope 只受某类流" | Mercedes | 未取证 | 官方文档 / 实测 |
| 15 | Mercedes purpose URL 的内容标准与审核 | Mercedes | 未取证 | 官方文档 |
| 16 | Mercedes scope 粒度分布（是否单资源级） | Mercedes | 仅一个示例 | 产品文档 |
| 17 | Mercedes 数字钥匙（CCC） | Mercedes | 未找到公开来源 | CCC 认证名单 / 技术说明 |
| 18 | Mercedes mTLS / 证书固定 | Mercedes | 未找到公开来源 | 抓包 / 白皮书 |
| 19 | Mercedes TEE/SE、OTA 安全 | Mercedes | 未找到公开来源 | 器件选型 / OTA 文档 |
| 20 | Mercedes 2024–2025 车辆数据 API 政策文档 | Mercedes | 未找到公开来源 | developer 站 changelog |
| 21 | Mercedes MBition / Mercedes Pay | Mercedes | 未找到公开来源 | 官网 / 产品页 |
| 22 | CARIAD E3 架构 / VW.OS / ID OTA 细节 | VW/CARIAD | 未取到 | 技术演讲 / 专利 / 拆解 |
| 23 | VW 集团 UN R155 合规声明 | VW/CARIAD | 站内检索零结果 | 官方合规公告 / 型式认证 |
| 24 | CARIAD 安全白皮书 | VW/CARIAD | 未找到公开来源 | 官网安全页 / 投资者材料 |
| 25 | BMW CarData OAuth 全量文档 | BMW | 占位页 + 区域封锁 | 换出口 IP / 代理 / RFI |
| 26 | BMW 数字钥匙 / 安全白皮书 | BMW | 未取到 | 同上 |
| 27 | Rivian Fleet API / OAuth / 数字钥匙文档 | Rivian | CloudFront 区域封锁 | 换出口 IP / RFI |
| 28 | 各国际车企 mTLS / DPoP / RAR / Token Exchange 落地情况 | 通用 | 未在公开文档取证 | 安全白皮书 / 抓包 / RFI |
| 29 | 数字钥匙规范正文（CCC 3 v1.1、FiRa、IEEE 802.15.4z） | 生态 | 发布公告 [A]/[B]，正文部分未取 | 联盟规范下载 / 成员渠道 |
| 30 | Tesla 漏洞项目定价细则与 GPG 轮换 | Tesla | 区间 [B]，细则未取 | Bugcrowd 政策页 / 官方公示 |

---

## 17.10 本章小结

### 17.10.1 本章的六个可溯源结论

1. **两家标尺的"骨干"由授权码流承载，且辅以"双路径"设计。** Tesla 以三类令牌、Mercedes 以两种鉴权模式，都把"是否需要逐车主同意"显式分离 —— 来源：§17.2.1、§17.3.2（developer.tesla.com / developer.mercedes-benz.com，[A]）。
2. **"授权被授予 ≠ 资源可访问"是国际实践的共同模式。** Tesla 的 `hide_private` 双层收窄与 Mercedes 的客户端 scope 白名单，都把资源级策略独立于 OAuth 授权 —— 来源：§17.2.2、§17.3.3.1（[A]）。
3. **Tesla 在车控链路上叠加了"车端凭证校验"（虚拟密钥），这是通用方案之外的关键控制** —— 来源：§17.2.4（[A]）。
4. **撤销与配额均可触发"授权态变更"，形成端到端联动**：scope 撤销→遥测配置移除；超限→移除推流且不恢复 —— 来源：§17.2.5.3、§17.2.6.2（[A]）。
5. **国际车企的约束性资源有两处明确的量化上限**：虚拟密钥 <20 把、单车推流 ≤5 应用，构成"影响范围控制" —— 来源：§17.2.4.9、§17.2.5.4（[A]）。
6. **BMW / Rivian / CARIAD 属"披露缺口"而非"能力缺口"**：本次因区域封锁与检索受限未取到其一手文档，**不得据此推断其能力** —— 来源：§17.4–§17.6、信源档案 §0（[A，直接观测/自述]）。

### 17.10.2 本章对通用方案的净贡献（三条）

- **验证**：通用授权方案的骨干（授权码流、发现、轮换、吊销、受众绑定、资源级二次裁量）已被国际标尺实际落地（§17.8.1）。
- **修正**：车控场景应在通用方案外补"车端凭证校验"层，并把"资源级二次裁量"从可选升为必需（§17.8.3）。
- **填补缺口**：把"候选但未取证"的通用控制（mTLS/DPoP/RAR/Token Exchange 等）显式列入待补证，**避免以"未出现"冒充"未采用"**（§17.8.2、§17.9）。

### 17.10.3 与全书其它章节的接口

- **合规映射**：GDPR / Data Act / R155 / R156 的条款级映射交由 WF-6 的 `18-authz-80-compliance-audit.md`（本章仅到"性质层面"，见 §17.1）。
- **国内对照**：本章（国际 5 家）与 `16-authz-60-cn-oem.md`（国内 9 家）的差异对比，交由 WF-0 的 `30-comparison.md`（AC-6）处理；本章仅在 §17.7 提供国际侧的对照矩阵。
- **规范底座**：本章引用的 RFC / OIDC / CCC / 国标，均取自信源档案 §2、§5、§1.2，未引入档案之外来源。

### 17.10.4 编号衔接说明（勘误）

为避免读者导航失误，此处对本章**扩写前的若干前向引用**作一致性说明（**本章未改动任何既有正文，仅在此登记实际归属**）：

- 正文 §17.2.2（第 8/9 行 scope 备注）与 §17.2.3.3（`show_keypair_step` 说明）中出现的"**见 §17.2.6**"，实际对应本版的"**§17.2.4 虚拟密钥**"；
- 正文 §17.2 表格 `vehicle_specs` 行与 §17.2.2 第 (4) 点中出现的"**见 §17.2.10**"，实际对应本版的"**§17.2.8 Tesla 授权模型小结**"（§17.2.8.1 的控制点对照表即其"Trade-off 表"）；
- 正文 §17.2.2 第 (2) 点中出现的"**见 §17.2.7**"，实际对应本版的"**§17.2.5 Fleet Telemetry**"（其中 §17.2.5.5 给出 `hide_private` 的 403 语义）；
- 正文 §17.2.3.4 末尾出现的"**见 §17.2.8 的计费模型**"，实际对应本版的"**§17.2.6 限流、计费与配额治理**"；
- 正文 §17.2.3.3 中"**与 §17.2.5 的联动**"，对应本版"**§17.2.5 Fleet Telemetry 授权链**"（scope 撤销→配置移除见 §17.2.5.3）。

> 说明：上述仅为**阅读导航的一致性登记**；本章既有正文**一字未改**（除本扩写在文件末尾追加内容外，未触碰任何原有段落）。若后续版本允许改稿，建议将上述前向引用直接订正为实际小节号。

**（本章结束。全章事实均来自 `docs/sources/source-dossier.md` §1–§7；凡推测均已标注"本报告判断（推测，非事实）"；凡未取证均已标注"未找到公开来源"，不代表能力缺失。）**





