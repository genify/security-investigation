# 授权与访问控制 · 威胁模型与攻击面

> **文件编号**：`14-authz-40-threat-model.md`
> **所属工作流**：WF-3（授权与访问控制 · 威胁模型与工程实现）
> **覆盖验收标准**：AC-2（授权章节 ≥300K 字符的组成部分）、AC-7（信源可靠并标注等级）、AC-12（技术深度与可读性并重：架构图 / 表格 / 工程片段）
> **证据底座**：`docs/sources/source-dossier.md`（唯一事实底座，信源档案）
> **编制**：Trail of Bits Security · Reverse Engineering Lead
> **版本**：v1.0 · 生效 2026-09-28
> **阅读提示**：本章事实句后紧跟 `—— 来源名称 —— URL —— [等级]`。证据等级口径沿用审计计划 §3.1：`[A]` 一手官方文档、`[B]` 权威第三方、`[C]` 二手、`[未验证]` 站点可达但正文未取到、`[合理推测（本报告判断）]`、`未找到公开来源`。**本章是全报告推演占比最高的一章**，因此每一条推演都显式标注「**本报告判断**…（推测，非事实）」，并在"前置条件"字段写明该推演成立所依赖的条件；凡不能对应信源档案条目的断言，一律不写，或降级为待补证陈述。
> **写作红线遵守声明**：本章严格遵守审计计划 §3.2。特别地——（1）**不臆造任何车企的密码算法/硬件实现细节**（§3.2 范围外声明）；（2）不把「未找到公开来源」反向表述为「该企业不具备该能力」；（3）**不编造真实攻击事件**，本章所有攻击路径均为"结构化的假设性威胁条目"，不代表任何已发生的真实入侵。

---

## 14.0 本章方法与诚实性声明

### 14.0.1 为什么本章必须先声明"哪些是事实、哪些是推演"

威胁模型（threat model）这一文体的天然属性，是**对尚未发生之事的结构化枚举**。它回答的是"在给定系统结构下，哪些攻击路径在原理上可行、需要什么前置条件、有什么征兆、被哪些控制挡住"。这与前面的机制剖析章节（`11-authz-10-protocols.md`、`12-authz-20-tokens-keys.md`、`13-authz-30-resource-authz.md`）有本质差别：机制章节描述"文档明载了什么"，威胁模型章节描述"如果攻击者这样走，会发生什么"。

因此，本章的**事实密度天然低于机制章节，推演密度天然高于机制章节**。为避免读者把推演误读为事实，本章采取与审计计划 §4.4「证据分层写作法」一致的纪律：**先写"文档明载"部分，再写"合理推测"部分，两者物理分段**，且每条推演都带独立的标注与前置条件字段 —— 来源：审计计划 §4.4 —— `docs/00-engagement-plan.md` —— [A，本项目内部方法论文档]。

一句话概括本章的**事实/推演比例声明**：

- **本章的事实骨架**来自三块 `[A]` 级一手证据：① 车企开发者文档（Tesla `developer.tesla.com`、Mercedes-Benz `developer.mercedes-benz.com`，后者本报告对标基准）；② 授权/密码/OTA 协议规范（RFC Editor 与各规范库，HTTP 200 已取证）；③ 中国国标（openstd.samr.gov.cn 一手条目）。
- **本章的推演部分**全部以「**本报告判断**」显式开头，并逐条给出「前置条件」。
- **本章不做的事**：不声称任何一家车企存在某个具体漏洞；不引用任何真实漏洞编号（CVE）；不描述任何真实攻击事件；不臆造国内车企的密码算法与硬件实现。

### 14.0.2 采集条件与覆盖度偏置（决定本章结论的可信度边界）

本章写作所依赖的取证条件，必须显式声明。信源档案 §0 记载：采集日期 2026-09-28，执行方式为 `terminal + curl` 与浏览器直连权威站点；**检索工具 `web_search` / `web_extract` 全程返回额度耗尽（Firecrawl 402/429），本次调研无法做开放网络发现，只能"直取已知权威 URL"**；公开搜索引擎在本运行环境同样不可用（Bing 地理重定向至 cn.bing.com、Baidu/Sogou/360 验证码、Google 机器人墙、DuckDuckGo 验证码）；`bmw.com` / `bmwgroup.com` / `rivian.com` 被 Akamai/CloudFront 区域封锁（HTTP 000 / 403）；`unece.org`、`iso.org`、`autosar.org`、`trustedcomputinggroup.org` 被 Cloudflare 或超时拦截；`open.xiaopeng.com` 对所有请求返回 403（openresty）—— 来源：信源档案 §0 —— `docs/sources/source-dossier.md` —— [A，本项目内部采证记录]。

由此产生的**覆盖度偏置**是：证据密度向"文档公开可达"的企业倾斜，Tesla、Mercedes-Benz 证据最厚，BMW、Rivian、小鹏、极氪、零跑、理想、华为、奇瑞证据薄弱。信源档案 §0 对此有强制写作纪律：**「未找到公开来源」= 本次披露缺口，绝不等于能力缺口，不得反向推断为「该企业没有该能力」** —— 来源：信源档案 §0 —— 同上 —— [A]。

这条纪律在本章尤其关键：威胁模型的读者容易产生一种滑坡——"某家车企未公开某项控制，所以它的攻击面更大"。本章明确拒绝这种滑坡。**一位攻击者面对的攻击面，取决于系统真实实现，而不取决于厂商是否写了白皮书。** 本章凡涉及"某企业缺少某控制"的判断，一律改写为"该方向未找到公开来源，控制是否存在未知，需在实车/沙箱验证中确认"。这句话同时也是本章 §14.9 待补证清单的方法论动机。

### 14.0.3 本章不臆造车企密码实现细节（红线复述）

审计计划 §1「范围外」明确列出：**不臆造国内车企的密码算法/硬件实现细节；缺证据即写缺证据** —— 来源：审计计划 §1 —— `docs/00-engagement-plan.md` —— [A]。信源档案 §7.10 第 5 条进一步记载：**9 家国内车企本次全部未取得关于"国密 SM2/SM3/SM4"、"mTLS 双向证书"、"证书轮换"、"HSM/SE/TEE"的任何官方一手来源**，报告中这些方向的结论一律写为「未找到公开来源 / 待补证」，禁止以行业常识冒充车企事实 —— 来源：信源档案 §7.10 —— `docs/sources/source-dossier.md` —— [A]。

因此本章在讨论"密钥存储""令牌绑定""硬件根信任"等主题时，**只引用中立的国际规范与国标条目**（如 GB/T 32918 系列 SM2、RFC 8705 mTLS、GlobalPlatform TEE、CCC Digital Key 3.0 的 SE 存储），**不对任何具体车企断言其采用了哪种实现**。凡涉及具体车企者，均写"该企业是否采用未知"。

### 14.0.4 本章结构导航

| 小节 | 主题 | 主证据强度 | 推演占比 |
|---|---|---|---|
| 14.1 | 资产与主体清单、信任边界 | 资产分级为分析构造；边界图为结构构造 | 中（构造性） |
| 14.2 | STRIDE 逐层映射（≥20 行） | 控制列引 Tesla/Mercedes [A] | 中 |
| 14.3 | 攻击树 A–F（6 棵） | 叶节点控制引规范与车企文档 | 高 |
| 14.4 | 协议级威胁剖析（6 主题） | 规范 [A] 为骨架 | 中高 |
| 14.5 | 威胁 × 控制映射矩阵（≥25 行） | 控制列尽量落到 [A] | 中 |
| 14.6 | 严重度分类应用 | 判据引审计计划 §3.3 | 中 |
| 14.7 | 攻击可行性评估方法 | 方法构造 | 高（方法本身是构造） |
| 14.8 | 合规红线与威胁的对齐 | 国标条目 [A] | 中 |
| 14.9 | 待补证清单 | — | — |
| 14.10 | 本章小结 | — | — |

---

## 14.1 资产与主体清单

威胁模型的第一性工作，是**在写任何威胁之前先回答"我们要保护什么、保护谁免受谁的侵害"**。本节先列资产（被保护对象）、再列主体（可能与资产发生交互的实体）、最后画信任边界（哪些穿越点是控制点）。这三张清单是本章后续所有分析的公因子。

**方法声明**：本节的三张清单**属于本报告的结构化构造**，不是从某份文档抄录的目录。资产分级中的"机密性/完整性/可用性"影响评级是**本报告的安全工程判断**，其依据是资产的**功能后果**（例如：能否导致车辆物理动作、能否暴露个人行踪），而非任何企业的官方定级。凡资产与主体的具体取值可对应信源档案者，均给出标注；凡属构造者，均标「本报告构造」。

### 14.1.1 资产分级表

下表列出车云授权体系中需要保护的 15 类资产（≥12 行要求已满足）。"C/I/A" 分别指机密性（Confidentiality）/完整性（Integrity）/可用性（Availability）的**失陷后果等级**：H（高，可导致人身安全或大规模隐私后果）、M（中，可导致业务损失或定向隐私泄露）、L（低，影响有限）。"对应授权对象"指该资产在授权模型中由哪类主体持有或访问。

> 评级口径说明：本表的 C/I/A 等级为**本报告的安全工程判断（构造）**，不代表任何企业的官方定级。资产本身的定义可对应信源档案者，逐条标注。

| # | 资产 | 说明与可溯源依据 | C | I | A | 对应授权对象 | 证据/构造标注 |
|---|---|---|---|---|---|---|---|
| A1 | **车辆控制能力**（unlock / start / wake / 远程启动 / 预约更新） | Tesla `vehicle_cmds` scope 覆盖"添加/移除驾驶员、Live Camera 访问、解锁、唤醒、远程启动、预约软件更新"—— 来源：Tesla Fleet API 认证概览 —— `https://developer.tesla.com/docs/fleet-api/authentication/overview` —— [A] | M | **H** | H | 车主、被授权驾驶员、数字钥匙持有者、代客泊车员、第三方 App（经 `vehicle_cmds`） | 定义 [A]；评级本报告构造 |
| A2 | **精确位置与轨迹** | Tesla `vehicle_location` scope 覆盖"精确与粗略位置"；带 `granular_access.hide_private=true` 的共享车辆即使被授予该 scope 也拿不到任何位置—— 同上 —— [A]。Fleet Telemetry 中位置类字段（Location、OriginLocation、DestinationLocation、DestinationName、RouteLine、GpsState、GpsHeading）需要 `vehicle_location`—— 来源：Tesla Fleet Telemetry —— `https://developer.tesla.com/docs/fleet-api/fleet-telemetry` —— [A] | **H** | M | M | 车主、车队管理员（经 `vehicle_location`）、第三方 App | 定义 [A]；评级本报告构造 |
| A3 | **摄像头 / 麦克风（Live Camera 等座舱感知）** | `vehicle_cmds` 覆盖"Live Camera 访问"—— 来源：Tesla 认证概览 —— 同上 —— [A] | **H** | **H** | M | 车主、代客泊车员（受限）、车企内部服务 | 定义 [A]；评级本报告构造 |
| A4 | **充电与计费数据** | Tesla `vehicle_charging_cmds` 覆盖"充电历史、计费金额、充电地点、预约/开始/停止充电"—— 同上 —— [A]；充电侧协议族 OCPP 1.6 / 2.0.1 / 2.1 与 ISO 15118-2/-20（Plug & Charge，TLS + contract certificate）—— 来源：Open Charge Alliance 协议页 —— `https://www.openchargealliance.org/protocols/` —— [A]；ISO 15118 标准号 —— 信源档案 §6 —— [未验证：iso.org Cloudflare 拦截] | M | **H** | M | 车主、第三方 App（经 `vehicle_charging_cmds`）、充电运营商 | 定义 [A]；评级本报告构造 |
| A5 | **诊断与服务数据**（服务历史、服务预约、可升级项、所有权信息） | `vehicle_device_data` 覆盖"实时数据、服务历史、服务预约、服务沟通、可升级项、附近超充、所有权信息"—— 来源：Tesla 认证概览 —— 同上 —— [A] | M | M | L | 车主、服务技师（经服务渠道）、第三方 App | 定义 [A]；评级本报告构造 |
| A6 | **账户身份**（车主账号、`openid` 身份） | `openid` = "Sign in with Tesla"（允许车主用 Tesla 凭证登录第三方应用）—— 同上 —— [A]；OpenID Connect Core 1.0 —— `https://openid.net/specs/openid-connect-core-1_0.html` —— [A] | **H** | **H** | M | 车主、第三方 App（经 `openid`）、车企云身份服务 | 定义 [A]；评级本报告构造 |
| A7 | **虚拟密钥（Virtual Key，车端命令签名私钥）** | 虚拟密钥 = 公私钥对；公钥须由可信用户添加到车辆，私钥留在应用服务器；**车辆在执行命令前或接受 Fleet Telemetry 配置前验证载荷签名**；文档称虚拟密钥"甚至能阻止 Tesla 自己的后端访问这些能力"—— 来源：Tesla 虚拟密钥开发者指南 —— `https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide` —— [A] | **H** | **H** | M | 车主（配对者）、第三方 App 后端 | 定义 [A]；评级本报告构造 |
| A8 | **刷新令牌 / 访问令牌**（第三方令牌、partner token、third-party-for-business token） | 三种令牌 —— 来源：Tesla 认证概览 —— 同上 —— [A]；刷新令牌**一次性使用（single use only）且 3 个月后过期**，最近一次使用的刷新令牌在 **24 小时内仍有效**—— 来源：Tesla 第三方令牌文档 —— `https://developer.tesla.com/docs/fleet-api/authentication/third-party-tokens` —— [A] | **H** | **H** | M | 第三方 App 后端、车企授权服务器 | 定义 [A]；评级本报告构造 |
| A9 | **个人与联系数据**（联系方式、家庭住址、头像） | `user_data` 覆盖"联系方式、家庭住址、头像、推荐信息"—— 来源：Tesla 认证概览 —— 同上 —— [A] | **H** | M | L | 车主、第三方 App（经 `user_data`） | 定义 [A]；评级本报告构造 |
| A10 | **车辆规格与定价信息** | `vehicle_specs` **仅 Partner Token 可用**，且对**任意车辆**可用、**无需车主授权**；`vehicle_pricing_info` **仅 Partner Token 可用**—— 同上 —— [A]（**授权控制例外，详见 §14.6**） | M | M | L | Partner（合作伙伴） | 定义 [A]；评级本报告构造 |
| A11 | **车队管理权限**（多车批量操作） | Tesla 限流"同账号多应用**共享**限额"—— 来源：Tesla 计费与限流 —— `https://developer.tesla.com/docs/fleet-api/billing-and-limits` —— [A]；`enterprise_management` scope 在 Tesla scope 全清单中—— 来源：Tesla 认证概览 —— 同上 —— [A] | M | **H** | M | 车队管理员、企业客户 | 定义 [A]；评级本报告构造 |
| A12 | **OTA 更新通道**（固件与配置下发） | `vehicle_cmds` 覆盖"预约软件更新"—— 同上 —— [A]；Uptane Standard 2.1.0 双仓库模型（Director + Image）—— 来源：Uptane 标准页 —— `https://uptane.org/docs/latest/standard/uptane-standard` —— [A]；TUF 四角色 + 阈值签名 —— `https://theupdateframework.github.io/specification/latest/` —— [A] | **H** | **H** | **H** | 车企云 OTA 服务、供应链厂商 | 定义 [A]；评级本报告构造 |
| A13 | **遥测流配置**（Fleet Telemetry 推流配置） | 配置由应用私钥**签名**且"**Tesla 无法编辑**"；若所需 scope 被撤销导致配置失效，配置会被**从车辆移除**；单台车辆最多同时向 **5 个第三方应用**推流—— 来源：Tesla Fleet Telemetry —— 同上 —— [A] | M | **H** | M | 第三方 App（经已配对虚拟密钥） | 定义 [A]；评级本报告构造 |
| A14 | **共享车辆的隐私开关状态**（`granular_access.hide_private`） | 带 `hide_private=true` 的车辆共享，即使被授予 `vehicle_location` 也拿不到任何位置，且无法流式传输位置字段—— 来源：Tesla 认证概览 —— 同上 —— [A] | M | **H** | L | 车主（设置方）、共享接收方 | 定义 [A]；评级本报告构造 |
| A15 | **授权决策日志 / 审计记录** | 本次未取到任何车企公开的"授权决策日志格式"文档—— 来源：信源档案 §7（Tesla/Mercedes 已读页面均未见此文档）—— [未找到公开来源]（**不得据此推断其无日志能力**） | L | M | L | 车企安全运营、监管 | 未找到公开来源 |

**对 A10 的特别标注（贯穿全章的悬置项）**：`vehicle_specs` / `vehicle_pricing_info` **仅 Partner Token 可用且对任意车辆无需车主授权**，是信源档案中唯一被明文记载的"**退出逐车主同意模型**"的资源访问路径 —— 来源：Tesla 认证概览 —— 同上 —— [A]；审计计划 §3.3 的 CSO 判定示例已将其归为 **High** —— 来源：审计计划 §3.3 —— `docs/00-engagement-plan.md` —— [A]。本章在 §14.6 对该项做逐条判定与补偿控制建议。

### 14.1.2 主体清单

下表列出可能与上述资产发生交互的 10 类主体（≥9 类要求已满足）。"授权来源"指该主体的权限在授权模型中**从何而来**；"可信度假设"指威胁模型在建模时**默认是否信任该主体**（这是建模假设，不是对现实组织的评价）。

| # | 主体 | 角色描述 | 授权来源 | 建模时的可信度假设 | 证据/构造标注 |
|---|---|---|---|---|---|
| S1 | **车主（资源所有者）** | 车辆的合法所有者 / 主要使用者，是 OAuth 模型中的"资源所有者" | 天然（所有权） | 可信（但账号可能被攻陷） | 本报告构造 |
| S2 | **被授权驾驶员** | 车主通过车辆或 App 授予临时/长期驾驶权限者 | 车主转授（如 `vehicle_cmds` 覆盖"添加/移除驾驶员"）—— 来源：Tesla 认证概览 —— `https://developer.tesla.com/docs/fleet-api/authentication/overview` —— [A] | 有条件可信 | 定义 [A] |
| S3 | **数字钥匙持有者** | 通过 CCC Digital Key 或车企自有数字钥匙持有车辆近场进入/启动权者 | 车主分发 + 密钥配对；CCC Digital Key Release 3.0 用 **BLE + UWB** 实现被动进入与启动，NFC 为强制备用，密钥存于 **Secure Element** —— 来源：CCC 发布公告 —— `https://carconnectivity.org/car-connectivity-consortium-delivers-digital-key-release-3-0-specification-businesswire/` —— [A] | 有条件可信（中继/重放为关键威胁，见 §14.3.4） | 定义 [A] |
| S4 | **代客泊车员 / 服务代驾** | 临时取得车辆控制权的第三方人员 | 临时授权 / 物理移交 | 低可信（短时、弱追责） | 本报告构造 |
| S5 | **服务技师** | 授权服务中心的维修人员，可能访问诊断数据 | 服务渠道授权（企业侧） | 有条件可信 | 本报告构造 |
| S6 | **第三方开发者应用** | 通过车企开放平台接入的车主服务或车队服务 App | OAuth 授权码流；Tesla 要求"必须已配对虚拟密钥"才能使用 Fleet Telemetry—— 来源：Tesla Fleet Telemetry —— `https://developer.tesla.com/docs/fleet-api/fleet-telemetry` —— [A] | **不完全可信**（攻击面主体） | 定义 [A] |
| S7 | **车企内部微服务** | 车企云内部的账号、授权、车控、OTA、数据等微服务 | 服务间凭证（如 RFC 7523 服务账号 + 客户端断言）—— `https://www.rfc-editor.org/rfc/rfc7523.txt` —— [A] | 可信（但横向移动为关键威胁） | 本报告构造 + 规范 [A] |
| S8 | **车队管理员** | 企业客户侧管理多车的高级操作者 | 企业合同 + `enterprise_management` scope —— 来源：Tesla 认证概览 —— 同上 —— [A] | 有条件可信 | 定义 [A] |
| S9 | **监管 / 执法接口** | 依法请求车辆数据的政府侧接口 | 法定程序 + 车企合规流程 | 建模为"高权限外部主体" | 本报告构造 |
| S10 | **供应链厂商** | 提供 T-BOX、网关、OTA 包、SDK 的上游厂商 | 合同 + 构建/签名链（SLSA v1.0 L0–L3 —— `https://slsa.dev/spec/v1.0/levels` —— [A]；in-toto —— `https://in-toto.io/specs/` —— [B]） | 不完全可信（供应链攻击面） | 定义 [A] |

**主体清单的使用方式**：任何威胁条目都必须能写成主语—动词—宾语的形式（"某主体 对 某资产 做了某事"）。凡不能落到具体主体与资产的威胁，本章视为不成立的威胁，予以剔除。这条纪律用于防止威胁模型退化为"泛泛而谈的风险列表"。

### 14.1.3 信任边界图

下图把"手机 App / 车机 / 第三方云 / 车企云 / T-BOX / 网关 / ECU / SE·HU"逐层标注信任级别与穿越的控制点。**图的拓扑为授权与访问控制的一般化抽象（本报告构造），不代表任何具体车企的实车网络拓扑**；每一处"控制点"若可对应信源档案条目者，在下方表内逐条标注。

```
┌────────────────────────────────────────────────────────────────────────────┐
│  信任域 I：用户侧（Trust Level：低—中；物理在用户手上，可被完全控制）      │
│                                                                            │
│   ┌───────────────┐   ┌───────────────┐   ┌───────────────────────┐        │
│   │ 手机 App      │   │ 数字钥匙      │   │ 车机（HU）            │        │
│   │ (第三方/车企) │   │ (SE 内密钥)   │   │ (座舱系统)            │        │
│   └──────┬────────┘   └──────┬────────┘   └──────────┬────────────┘        │
│          │                   │                       │                     │
└──────────┼───────────────────┼───────────────────────┼─────────────────────┘
           │                   │                       │
     [CP-1]│授权码/PKCE        │[CP-2] BLE+UWB+NFC     │[CP-4]车机本地 API
           │+ 外部用户代理      │  测距 + SE 签名        │  授权（车机侧）
           ▼                   ▼                       ▼
┌────────────────────────────────────────────────────────────────────────────┐
│  信任域 II：近场与边缘（Trust Level：中；物理邻近但无物理保护）             │
│   ┌──────────────────────────────┐   ┌──────────────────────────────┐      │
│   │ [CP-2] 数字钥匙链路          │   │ [CP-3] T-BOX 蜂窝链路        │      │
│   │ BLE(测距初判)+UWB(精确测距)  │   │ TLS 1.3（RFC 8446）+ 证书     │      │
│   │ +NFC(强制备用)；SE 存密钥    │   │ + 双向认证（若启用）          │      │
│   └──────────────┬───────────────┘   └──────────────┬───────────────┘      │
└──────────────────┼──────────────────────────────────┼──────────────────────┘
                   │                                  │
                   │            ┌─────────────────────┘
                   ▼            ▼
┌────────────────────────────────────────────────────────────────────────────┐
│  信任域 III：云侧（Trust Level：高—中；多租户，横向移动风险在内部）        │
│                                                                            │
│   ┌────────────────────┐   ┌────────────────────┐   ┌──────────────────┐   │
│   │ 第三方云（App 后端）│   │ 车企云              │   │ 授权服务器        │   │
│   │ 持虚拟密钥私钥      │◄─►│ 授权/车控/OTA/数据  │◄─►│ (auth.<oem>.com)  │   │
│   │                    │   │ 微服务              │   │ 令牌/内省/吊销    │   │
│   └─────────┬──────────┘   └─────────┬──────────┘   └──────────────────┘   │
│             │  [CP-5] 令牌与密钥      │ [CP-6] 服务间凭证/令牌交换           │
│             │  交换、act/subject      │  (RFC 8693 / RFC 7523)               │
└─────────────┼────────────────────────┼────────────────────────────────────┘
              │                        │
              │                        ▼
              │        ┌───────────────────────────────────────────┐
              │        │ 信任域 IV：车端（Trust Level：分层的信任基）│
              │        │  ┌─────────┐   [CP-7] 网关策略        │
              │        │  │ T-BOX   │───►┌──────────┐          │
              │        │  │(外部通信)│    │ 中央网关 │          │
              │        │  └─────────┘    └────┬─────┘          │
              │        │        [CP-8] SecOC / 授权校验        │
              │        │           ┌─────────┴──────────┐       │
              │        │           ▼                    ▼       │
              │        │   ┌───────────────┐   ┌──────────────┐ │
              │        │   │ ECU 域（车控）│   │ SE / TEE /   │ │
              │        │   │               │   │ HSM（密钥）  │ │
              │        │   └───────────────┘   └──────────────┘ │
              │        └───────────────────────────────────────────┘
              │                        ▲
              └────────────────────────┘
                 [CP-9] 虚拟密钥签名校验：车辆在执行命令前或接受
                 Fleet Telemetry 配置前验证载荷签名（Tesla [A]）
```

**控制点（CP）清单与溯源**：

| CP | 边界 | 控制点内容 | 可溯源依据 | 证据等级 |
|---|---|---|---|---|
| CP-1 | 用户侧 → 车企云 | 授权码请求必须携带 `response_type=code`、`client_id`、`redirect_uri`、`scope`、`state`（"用于校验的随机值"），可选 `nonce`（"用于防重放的随机值"）—— 来源：Tesla 第三方令牌 —— `https://developer.tesla.com/docs/fleet-api/authentication/third-party-tokens` —— [A]；公共客户端须用 PKCE（RFC 7636）—— `https://www.rfc-editor.org/rfc/rfc7636.txt` —— [A]；原生 App 必须使用系统浏览器/外部用户代理（RFC 8252）—— `https://www.rfc-editor.org/rfc/rfc8252.txt` —— [A] | 定义 [A] | [A] |
| CP-2 | 用户侧 → 近场 → 车端 | CCC Digital Key 3.0 用 **BLE + UWB** 实现被动进入/启动，**NFC 为强制备用**，密钥存于 **Secure Element**；CCC 与 FiRa 就 UWB 合作 —— 来源：CCC 发布公告 —— `https://carconnectivity.org/car-connectivity-consortium-delivers-digital-key-release-3-0-specification-businesswire/` —— [A]；FiRa Core 3.0 / 4.0 规范 —— `https://www.firaconsortium.org news` —— [B] | 定义 [A/B] | [A/B] |
| CP-3 | T-BOX → 车企云 | TLS 1.3（RFC 8446）、X.509（RFC 5280）、OCSP（RFC 6960）；国密 TLS 落点 RFC 8998（SM2 签名 / AEAD_SM4_GCM / SM3）—— 各 RFC —— [A] | 规范 [A] | [A]（规范层） |
| CP-4 | 车机 → 车端域 | 车机本地 API 的授权（本报告构造：车机侧应存在与云侧一致的授权判定点）；本次未取到任何车企车机侧授权文档 —— 来源：信源档案 §7 —— [未找到公开来源] | 未找到公开来源 | [未找到公开来源] |
| CP-5 | 第三方云 ↔ 车企云 | 令牌与虚拟密钥交换；Tesla 令牌端点与 API 端点**分属不同主机**（`POST https://fleet-auth.prd.vn.cloud.tesla.com/oauth2/v3/token`）—— 来源：Tesla 第三方令牌 —— 同上 —— [A]；发送方约束令牌 RFC 8705（mTLS）/ RFC 9449（DPoP）—— [A] | 定义 [A] | [A] |
| CP-6 | 车企云内部服务 ↔ 服务 | 服务间凭证与代授权：RFC 7523（服务账号 + 客户端断言）、RFC 8693（`subject_token`/`actor_token` 令牌交换）—— [A] | 规范 [A] | [A]（规范层） |
| CP-7 | T-BOX → 网关 | 网关策略（本报告构造：应做域间访问控制与报文过滤）；GB/T 40857-2021《汽车网关信息安全技术要求及试验方法》—— 来源：国标全公开系统 —— `https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=2977F0AC1719BBEFB9649C0146B0FC55` —— [A] | 规范 [A] | [A]（标准存在性） |
| CP-8 | 网关 → ECU | SecOC / 授权校验（本报告构造）；AUTOSAR Classic Platform 含 Crypto Stack、SecOC、IdsM —— 来源：信源档案 §4 —— [未验证：autosar.org 超时] | 未验证 | [未验证] |
| CP-9 | 任意控制指令 → 车辆执行 | **虚拟密钥签名校验**：车辆在执行命令前或接受 Fleet Telemetry 配置前验证载荷签名—— 来源：Tesla 虚拟密钥开发者指南 —— `https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide` —— [A] | 定义 [A] | [A] |

**边界图的三点读法（本报告判断，非事实）**：

1. **CP-9 是唯一一个"由被保护方自己执行"的控制点**，也是 Tesla 文档中声称"甚至能阻止 Tesla 自己的后端访问这些能力"的依据 —— 来源：Tesla 虚拟密钥开发者指南 —— 同上 —— [A]。前置条件：车辆固件支持该签名校验、且公钥已由可信用户配对。若该前置条件不成立，CP-9 不生效。
2. **信任级别最高的域（车企云）恰恰是横向移动后果最重的域**，因为云侧同时持有授权、车控、OTA 与数据四类能力。这是 §14.3.5（云端授权服务攻陷）之所以被单列为一棵攻击树的原因。
3. **CP-4（车机侧授权）在本次取证中完全空缺**。本报告不推测车机侧是否存在授权判定，只指出：**这一空缺本身是待补证项，而不是已知缺陷**。

---

## 14.2 STRIDE 逐层映射

STRIDE 是威胁枚举的经典分类法：**S**poofing（仿冒）、**T**ampering（篡改）、**R**epudiation（抵赖）、**I**nformation Disclosure（信息泄露）、**D**enial of Service（拒绝服务）、**E**levation of Privilege（权限提升）。本节把 STRIDE 六类**逐信任边界**（取 §14.1.3 的 CP-1 至 CP-9）展开，共 24 行（≥20 行要求已满足）。

**方法声明**：下表"威胁"列为**结构化推演**（本报告构造的攻击假设），"现有控制"列尽量落到信源档案中的 `[A]` 级依据（Tesla / Mercedes 文档、RFC、国标）；"可观测征兆"列为**检测点的构造**（用于 §14.7 的验证方法）。凡控制列无法落到 `[A]` 者，标 `[未找到公开来源]`，**并禁止反向推断为"无控制"**。

| ID | STRIDE | 边界 | 具象威胁（构造） | 可观测征兆（构造） | 现有控制（尽量落到 [A]） | 证据等级 |
|---|---|---|---|---|---|---|
| T-01 | S 仿冒 | CP-1 | 攻击者伪造第三方 App 的 `client_id`/`redirect_uri`，冒充合法应用骗取授权码 | 授权请求中 `redirect_uri` 与注册值不一致会返回 "Invalid redirect URL"—— 来源：Mercedes 授权码流 —— `https://developer.mercedes-benz.com/get-started/oauth/authorization-code-flow` —— [A] | 注册 `redirect_uri` 精确匹配；`state` 校验（Tesla 文档描述 `state` 为"用于校验的随机值"） | [A]（控制依据）；推演为本报告构造 |
| T-02 | S 仿冒 | CP-1 | 原生 App 内嵌 WebView 冒充系统浏览器，截获授权码 | 授权页面在 WebView 中而非系统浏览器中渲染（终端侧可观测） | RFC 8252 强制原生 App 使用外部用户代理、禁止内嵌 WebView —— `https://www.rfc-editor.org/rfc/rfc8252.txt` —— [A] | [A] |
| T-03 | S 仿冒 | CP-1 | 攻击者用被盗的 `client_secret` 冒充第三方应用后端 | 令牌端点 `/token` 调用来源异常（如来自非应用服务器 IP）—— Tesla 文档说明 `/token` 调用"来自应用服务器、适用不同的限流"—— 来源：Tesla 第三方令牌 —— [A] | 客户端凭证须保存在后端（Mercedes 明确"应用不得向客户端暴露任何客户端凭证"）—— 来源：Mercedes 授权码流 —— 同上 —— [A] | [A] |
| T-04 | S 仿冒 | CP-5 | 攻击者仿冒第三方云调用车企 API（持被窃访问令牌） | 令牌使用的地理/时间模式异常（构造的检测点） | 发送方约束令牌：RFC 8705 mTLS 证书绑定、RFC 9449 DPoP —— [A]；Tesla 虚拟密钥让**载荷签名**由私钥完成 | [A]（规范）；车企是否启用未知 |
| T-05 | S 仿冒 | CP-2 | 数字钥匙中继：攻击者用中继设备在车主与车辆之间转发 BLE/UWB 信号，伪装"车主在场" | 测距距离与实际物理距离不符（UWB 精确测距可发现） | CCC Digital Key 3.0 用 BLE + UWB 实现被动进入，UWB 提供精确测距以抗中继 —— 来源：CCC 发布公告 —— `https://carconnectivity.org/...` —— [A]；FiRa UWB 规范 —— [B] | [A/B] |
| T-06 | T 篡改 | CP-1 | 攻击者篡改授权请求中的 `scope`，诱导车主同意超出应用实际需要的权限 | 同意界面上显示的 SCOPE 与应用声明的用途不符（Mercedes 同意界面展示 SCOPE 与 "purpose URL"）—— 来源：Mercedes 授权码流 —— 同上 —— [A] | 同意界面须展示 scope 与用途 URL；`require_requested_scopes=true` 强制全部 scope 授权 —— 来源：Tesla 第三方令牌 —— 同上 —— [A] | [A] |
| T-07 | T 篡改 | CP-5 | 中间人篡改云端下发的车控指令 | 指令载荷签名校验失败（CP-9 的观测点） | **虚拟密钥签名校验**：车辆在执行命令前验证载荷签名 —— 来源：Tesla 虚拟密钥指南 —— [A]；TLS 1.3（RFC 8446）防被动/主动篡改 —— [A] | [A] |
| T-08 | T 篡改 | CP-3 | 篡改 T-BOX 与车企云之间的通信 | 证书链校验失败、OCSP 状态异常（构造的检测点） | RFC 5280 证书链、RFC 6960 OCSP、RFC 8446 TLS 1.3 —— [A]；国密落点 RFC 8998 —— [A] | [A]（规范层） |
| T-09 | T 篡改 | CP-9 | 篡改虚拟密钥公钥托管位置的内容（`.well-known` 下的公钥文件） | 公钥指纹变化；文档要求公钥**必须长期可用**且私钥绝不可托管于域名 | 公钥托管于 `https://developer-domain.com/.well-known/appspecific/com.tesla.3p.public-key.pem`，私钥 `private-key.pem` 绝不可托管于域名 —— 来源：Tesla 虚拟密钥指南 —— [A] | [A] |
| T-10 | T 篡改 | CP-4 | 篡改车机侧授权判定逻辑或缓存（本报告构造） | 车机授权状态与云侧不一致（构造的检测点） | 本次未取到任何车企车机侧授权文档 —— 来源：信源档案 §7 —— [未找到公开来源] | [未找到公开来源] |
| T-11 | R 抵赖 | 全域 | 第三方应用否认执行过某次车控操作；车主否认授权过某 scope | 缺失"授权决策依据"的日志（构造的观测点） | 车主侧可撤销入口：Tesla `https://auth.tesla.com/user/revoke/consent?revoke_client_id=$CLIENT_ID&back_url=$RETURN_URL` —— 来源：Tesla 第三方令牌 —— [A]（提供"谁撤销了什么"的锚点） | [A]（部分）；日志内容 [未找到公开来源] |
| T-12 | R 抵赖 | CP-6 | 车企内部服务否认其代表某第三方应用代授权过某资源 | 令牌交换链 `act`/`subject` 记录缺失（RFC 8693 定义的代理链） | RFC 8693 Token Exchange（`subject_token`/`actor_token`）—— `https://www.rfc-editor.org/rfc/rfc8693.txt` —— [A] | [A]（规范）；车企是否启用未知 |
| T-13 | I 信息泄露 | CP-1 | 授权码被截获后换取令牌（公共客户端无 PKCE 时） | 同一授权码被多次使用 → "Invalid grant"（授权码无效或已被使用）—— 来源：Mercedes 授权码流 —— [A] | RFC 7636 PKCE；授权码一次性使用 | [A] |
| T-14 | I 信息泄露 | CP-5 | 访问令牌被复制到攻击者处后被重放 | 同一令牌来自多个地理位置/IP（构造的检测点） | 短 TTL（Mercedes 默认 `expires_in` 3599 秒 ≈ 1 小时）—— 来源：Mercedes 授权码流 —— [A]；令牌绑定（RFC 8705 / RFC 9449）—— [A] | [A]（TTL 依据）；绑定是否启用未知 |
| T-15 | I 信息泄露 | CP-5 | 位置字段被推流给未获授权的第三方应用 | 请求位置字段被拒 → 返回 HTTP 403 "location access not granted"—— 来源：Tesla Fleet Telemetry —— [A] | `granular_access.hide_private=true` 双层控制：即使授予 `vehicle_location` 也拿不到位置 —— 来源：Tesla 认证概览 —— [A] | [A] |
| T-16 | I 信息泄露 | CP-5 | `vehicle_specs` / `vehicle_pricing_info` 被 Partner 无车主授权读取 | Partner Token 对任意车辆访问 `vehicle_specs`/`vehicle_pricing_info`（**文档明载该路径无需车主授权**） | 该路径**为授权控制例外**，判为 High（见 §14.6）—— 来源：Tesla 认证概览 —— [A]；审计计划 §3.3 —— [A] | [A] |
| T-17 | I 信息泄露 | CP-6 | 车企云内部某微服务越权读取其他租户或全量车辆数据 | 跨租户数据访问（构造的检测点） | 本次未取到车企云内部租户隔离文档 —— 来源：信源档案 §7 —— [未找到公开来源]（**不得推断为无隔离**） | [未找到公开来源] |
| T-18 | D 拒绝服务 | CP-5 | 攻击者耗尽第三方应用的 API 限额，使正常服务不可用 | 限流触发计数（账号>设备维度） | 限流按账号按设备计：实时数据 60 次/分、唤醒 3 次/分、设备命令 30 次/分、同账号多应用**共享**限额 —— 来源：Tesla 计费与限流 —— `https://developer.tesla.com/docs/fleet-api/billing-and-limits` —— [A] | [A] |
| T-19 | D 拒绝服务 | CP-5 | 计费上限被触发导致 API 使用暂停且推流配置被移除（且不恢复） | 达 80% / 100% 上限发邮件；超限暂停 API 使用并移除 Fleet Telemetry 推流配置（且不恢复） | 每账号计费上限默认 0；邮件预警 —— 来源：Tesla 计费与限流 —— 同上 —— [A] | [A] |
| T-20 | D 拒绝服务 | CP-3 | 车队规模下 T-BOX 与云的连接被大量中断，遥测缓冲耗尽 | 断连后缓冲上限（构造的观测点） | 车辆缓冲 **5000 条消息（≥2500 秒数据）**；重连采用**指数退避，最大重试延迟 30 秒** —— 来源：Tesla Fleet Telemetry —— [A] | [A] |
| T-21 | D 拒绝服务 | CP-2 | 数字钥匙的 BLE/UWB/NFC 三种通道同时被干扰 | 三种通道均不可用（构造的观测点） | CCC Digital Key 3.0 保留 **NFC 为强制备用方案** —— 来源：CCC 发布公告 —— [A] | [A] |
| T-22 | E 权限提升 | CP-5 | 第三方应用借车企云的更高权限访问超出自身 scope 的资源（混淆代理） | 同一请求在授权服务器侧 `act` 链与资源侧判定不一致（构造的检测点） | RFC 8693 令牌交换的 `subject`/`act` 链路设计用于显式表达"谁代表谁" —— [A]；RFC 9396 富授权请求（`authorization_details`）用于资源级授权 —— `https://www.rfc-editor.org/rfc/rfc9396.txt` —— [A] | [A]（规范）；车企是否采用未知 |
| T-23 | E 权限提升 | CP-6 | 车企云内部服务被攻陷后提升到可签发任意令牌的角色 | 内部服务签发令牌的权限边界越界（构造的检测点） | RFC 7523 服务账号 + 客户端断言可约束服务身份 —— [A]；RFC 9068 `typ: at+jwt` / `aud`/`iss`/`exp` 校验 —— `https://www.rfc-editor.org/rfc/rfc9068.txt` —— [A] | [A]（规范）；车企是否采用未知 |
| T-24 | E 权限提升 | CP-9 | 攻击者获取虚拟密钥私钥后伪造任意车控指令 | 私钥托管位置被暴露（文档明确私钥绝不可托管于域名） | 私钥须留在应用服务器，绝不可托管于域名；公钥须长期可用 —— 来源：Tesla 虚拟密钥指南 —— [A]；密钥数量上限（B2B 自动添加条件为**已配对密钥少于 20 把**）作为影响范围控制 —— 同上 —— [A] | [A] |

**对 STRIDE 表的横向观察（本报告判断，非事实）**：

- **S 与 E 两类威胁的现有控制最厚**：Tesla 与 Mercedes 的公开文档提供了 `redirect_uri` 精确匹配、`state`、PKCE、外部用户代理、发送方约束令牌、虚拟密钥签名校验等一整套对应控制；这些控制的共同点是"**由规范预先定义、可被逐条对标**"（前置条件：规范被实际采用）。
- **R（抵赖）与 I（信息泄露）两类威胁的现有控制最薄**：本节 24 行中，R 类仅 2 行、I 类 5 行，且多行落在"日志/租户隔离未找到公开来源"。**这构成本章在 §14.10 提炼的"可观测性缺口"主题。**
- **D（拒绝服务）在车云场景有一个特殊性**：Tesla 的计费-限流机制把"配额耗尽"设计成一种**有意的（对业务方而言的）拒绝服务**，且"超限会暂停 API 使用并移除 Fleet Telemetry 推流配置（且不恢复）" —— 来源：Tesla 计费与限流 —— [A]。这意味着一次配额耗尽对第三方应用是可自伤也可被攻击者触发的可用性事件 —— **本报告判断，前置条件：攻击者已持有可用令牌且能持续消耗配额。**

---

## 14.3 攻击树

攻击树以"攻击者目标"为根节点、以"达成目标的子步骤"为中间节点、以"可由规范或文档验证的具体动作"为叶节点。本节给出 6 棵攻击树（A–F），每棵附 ASCII 树 + 节点说明 + 前置条件 + 检测点。

**总体方法声明**：**本节所有攻击树均为结构化的假设性推演，不代表任何已发生的真实攻击。** 叶节点中若引用规范或车企文档，则该叶节点的"控制对策"有 `[A]` 依据；若为纯构造，则标注「本报告构造（推测，非事实）」。前置条件字段写明"要让这棵树成立，攻击者必须先具备什么"。

### 14.3.1 攻击树 A：未授权车辆控制（目标：执行 unlock / start）

```
[A] 未授权执行 unlock / start
├── [A.1] 直接持有合法凭证
│   ├── [A.1.1] 窃取车主账号（钓鱼/撞库）→ 走授权码流拿 vehicle_cmds
│   ├── [A.1.2] 窃取第三方应用后端存储的刷新令牌
│   └── [A.1.3] 窃取虚拟密钥私钥（应用服务器被入侵）
├── [A.2] 不持凭证，绕过授权判定
│   ├── [A.2.1] 伪造/重放车控指令载荷（绕过 CP-9 签名校验）
│   ├── [A.2.2] 直接攻击车端总线（不经过云）
│   └── [A.2.3] 借用云侧代理的更宽权限（混淆代理，见攻击树 E）
└── [A.3] 取得合法但范围过宽的授权
    ├── [A.3.1] 诱导车主同意超出需要的 scope（consent phishing）
    └── [A.3.2] 利用"scope 缩减不影响既有刷新令牌"的窗口
```

**节点说明**：

- **A.1.1**：走标准授权码流。控制对策对应 CP-1（`state`、PKCE、外部用户代理）与 RFC 9470 步进认证挑战（`acr`/`amr`）—— `https://www.rfc-editor.org/rfc/rfc9470.txt` —— [A]。**前置条件**：车主账户凭证被攻陷，或授权页被钓鱼。
- **A.1.2**：刷新令牌一次性使用且在 3 个月后过期，最近一次使用的刷新令牌在 24 小时内仍有效 —— 来源：Tesla 第三方令牌 —— [A]。这条控制**同时**带来攻防两面：见 §14.4.3。**前置条件**：应用后端存储被入侵，或令牌在传输中被截获。
- **A.1.3**：私钥须留在应用服务器、绝不可托管于域名 —— 来源：Tesla 虚拟密钥指南 —— [A]。**前置条件**：应用服务器被入侵且私钥未受 HSM 保护。
- **A.2.1**：直接伪造载荷。控制对策为 CP-9（车辆在执行命令前验证载荷签名）—— 来源：Tesla 虚拟密钥指南 —— [A]。**前置条件**：攻击者需先获得可通过校验的签名，或车辆固件未启用签名校验（本次无证据可判断任何车企是否启用）。
- **A.2.2**：绕开云，攻击车端网络。控制对策为 GB/T 40857-2021（汽车网关信息安全）与 GB/T 40856-2021（车载信息交互系统信息安全）—— 来源：国标全公开系统 —— [A]（标准存在性）。**前置条件**：物理接触车辆或近场可用。
- **A.2.3**：见攻击树 E。
- **A.3.1**：见 §14.4.4。控制对策为同意界面展示 scope 与 purpose URL —— 来源：Mercedes 授权码流 —— [A]。**前置条件**：攻击者能诱导车主在诱导性界面点击同意。
- **A.3.2**：Tesla 文档明载"**scope 缩减与既有刷新令牌兼容，仅对新签发的访问令牌生效**"—— 来源：Tesla 第三方令牌 —— [A]。**前置条件**：车主先授权了过宽 scope，事后缩减；此时既有刷新令牌的**能力面**在旧访问令牌 TTL 内仍存在（见 §14.4.3 的窗口分析）。

**检测点（构造）**：(1) 同一 `client_id` 在短时间内请求多次 `/authorize`；(2) `prompt_missing_scopes=true` 的重复触发；(3) 车控指令来源 IP 与历史模式偏离；(4) 虚拟密钥签名校验失败率上升。

### 14.3.2 攻击树 B：位置与轨迹窃取（含 `granular_access.hide_private` 作为叶节点被拒的路径）

```
[B] 窃取车辆位置与轨迹
├── [B.1] 经授权但资源级策略拒绝（被阻断路径，正面案例）
│   ├── [B.1.1] 请求 vehicle_location scope 成功，但共享车辆 hide_private=true
│   │   └── [B.1.1.1] 查询位置 → HTTP 403 "location access not granted"（被拒）
│   └── [B.1.2] 尝试流式传输位置字段 → 同样无法流式传输（被拒）
├── [B.2] 经授权且未被 hide_private 拒绝
│   ├── [B.2.1] 合法获得 vehicle_location 后持续采集轨迹
│   └── [B.2.2] 通过 Fleet Telemetry 推流（须已配对虚拟密钥，≤5 应用）
├── [B.3] 绕过位置授权
│   ├── [B.3.1] 用车控类的间接推断（如车辆状态变化推测位置）［构造］
│   └── [B.3.2] 从 vehicle_device_data 的"附近超充"字段间接推断 ［构造］
└── [B.4] 从 Partner 路径读取非位置车辆数据（vehicle_specs）［不构成位置窃取］
```

**节点说明**：

- **B.1.1.1**：这是本章最重要的**正面控制案例**。Tesla 文档明载：带 `granular_access.hide_private=true` 的车辆共享即使被授予 `vehicle_location` 也拿不到任何位置，且无法流式传输位置字段 —— 来源：Tesla 认证概览 —— `https://developer.tesla.com/docs/fleet-api/authentication/overview` —— [A]。Fleet Telemetry 中"`hide_private` 共享车辆尝试访问会被拒绝并返回 **HTTP 403 'location access not granted'**"—— 来源：Tesla Fleet Telemetry —— `https://developer.tesla.com/docs/fleet-api/fleet-telemetry` —— [A]。审计计划 §3.3 已将其归为 **Informational→正面控制案例**（双层授权控制的良好实践，建议其他车企对标）—— 来源：审计计划 §3.3 —— [A]。
- **B.2.2**：Fleet Telemetry 前置条件为车辆固件 2024.26+、已配对虚拟密钥，且单台车辆最多同时向 5 个第三方应用推流 —— 来源：Tesla Fleet Telemetry —— 同上 —— [A]。**前置条件**：攻击者已持有已配对虚拟密钥的第三方应用后端。
- **B.3.1 / B.3.2**：**本报告构造的间接推断路径（推测，非事实）**。前置条件：攻击者已持有 `vehicle_device_data`（其覆盖"实时数据""附近超充""所有权信息"）—— 来源：Tesla 认证概览 —— 同上 —— [A]。**本报告判断**：若某资源的字段集合足够丰富，则即使位置字段被策略拒绝，仍可能从非位置字段的时间序列间接推断行踪（推测，非事实）。**这是"资源级策略只按字段拒绝、但未做推断抗性的可能缺口"，需要实测验证其可推断性；本报告不做任何断言其确实可推断。**

**检测点（构造）**：(1) 对 `hide_private` 车辆的 403 响应计数（异常高可能意味着试探）；(2) 同一应用在 `vehicle_location` 被拒后转而高频拉取 `vehicle_device_data`（本报告构造的侧信道迹象）。

### 14.3.3 攻击树 C：第三方应用令牌窃取与滥用

```
[C] 窃取并滥用第三方应用令牌
├── [C.1] 窃取授权码
│   ├── [C.1.1] 重定向劫持（redirect_uri 通配/子域接管）
│   ├── [C.1.2] 内嵌 WebView 截获（RFC 8252 禁止）
│   └── [C.1.3] 浏览器历史/日志泄漏
├── [C.2] 窃取令牌
│   ├── [C.2.1] 从应用后端数据库/日志读取访问令牌与刷新令牌
│   ├── [C.2.2] 从客户端侧读取（Mercedes：应用不得向客户端暴露任何凭证）
│   └── [C.2.3] 网络中间人（TLS 降级/证书劫持）
├── [C.3] 滥用窃得的令牌
│   ├── [C.3.1] 重放访问令牌（有效期内，最多 ≈1 小时，Mercedes 3599s）
│   ├── [C.3.2] 重放刷新令牌（一次性 + 24 小时宽限期，两者叠加）
│   └── [C.3.3] 并发刷新竞赛（两进程同时用同一刷新令牌）
└── [C.4] 维持访问
    ├── [C.4.1] 车主未主动撤销 → 依赖令牌自然过期（3 个月）
    └── [C.4.2] 若失效则回退到 A.1.1 重新钓鱼
```

**节点说明与"刷新令牌一次性 + 24 小时宽限期"的攻防含义**：

- **C.2.1**：控制对策为"客户端凭证必须保存在后端服务器，应用不得向客户端暴露任何客户端凭证（client id、client secret、访问令牌）"—— 来源：Mercedes 授权码流 —— `https://developer.mercedes-benz.com/get-started/oauth/authorization-code-flow` —— [A]。
- **C.3.1**：访问令牌 TTL 越短，重放窗口越小。Mercedes 明载默认 `expires_in` 为 **3599 秒**（≈1 小时）—— 来源：Mercedes 授权码流 —— 同上 —— [A]。
- **C.3.2**：Tesla 刷新令牌**一次性使用（single use only）且 3 个月后过期**，**最近一次使用的刷新令牌在 24 小时内仍有效** —— 来源：Tesla 第三方令牌 —— `https://developer.tesla.com/docs/fleet-api/authentication/third-party-tokens` —— [A]。**攻防两面性见 §14.4.3。**
- **C.3.3**：并发竞态 —— Tesla 明确刷新令牌一次性使用，而 24 小时宽限期正是用于覆盖"应用未能持久化轮换后令牌"的失败场景 —— 来源：Tesla 第三方令牌 —— 同上 —— [A]。**本报告判断（推测，非事实）**：宽限期在缓解"应用崩溃导致锁死"的同时，也把"旧刷新令牌被窃取"的有效窗口从"秒级"扩大到"24 小时级"。前置条件：攻击者在 24 小时内窃得旧刷新令牌，且真正的应用尚未完成下一轮轮换。
- **C.4.1**：车主侧可主动撤销 —— Tesla `https://auth.tesla.com/user/revoke/consent?revoke_client_id=$CLIENT_ID&back_url=$RETURN_URL` —— 来源：Tesla 第三方令牌 —— 同上 —— [A]；令牌吊销端点 RFC 7009 —— `https://www.rfc-editor.org/rfc/rfc7009.txt` —— [A]。

**检测点（构造）**：(1) 同一刷新令牌被多次使用（正常应一次性）；(2) 同一 `client_id` 的刷新请求来自多个 IP；(3) `prompt_missing_scopes=true` 与撤销事件的时间相关性。

### 14.3.4 攻击树 D：数字钥匙中继 / 重放

```
[D] 数字钥匙中继或重放
├── [D.1] 中继攻击
│   ├── [D.1.1] BLE 层中继（转发广播/连接）
│   ├── [D.1.2] UWB 测距中继（伪造飞行时间）
│   └── [D.1.3] NFC 层中继（近场转发）
├── [D.2] 重放攻击
│   ├── [D.2.1] 重放上一次进入/启动的认证报文
│   └── [D.2.2] 重放 SE 输出的签名（若挑战不含新鲜随机数）
├── [D.3] 密钥提取
│   ├── [D.3.1] 从手机侧提取数字钥匙私钥（应受 SE 保护）
│   └── [D.3.2] 从车辆侧提取配对密钥（应受车载 SE/HSM 保护）
└── [D.4] 授权模型缺陷
    ├── [D.4.1] 共享数字钥匙无有效期/无次数限制
    └── [D.4.2] 撤销（车主删除钥匙）未在车辆侧生效
```

**节点说明（以公开规范为"防中继设计的公开依据"）**：

- **D.1**：CCC Digital Key Release 3.0 发布会公告（2021-04-21）明载：新增 **BLE + UWB** 实现被动无钥匙进入与启动，**NFC 保留为强制备用方案**，密钥存储于 **Secure Element** —— 来源：Car Connectivity Consortium 发布公告 —— `https://carconnectivity.org/car-connectivity-consortium-delivers-digital-key-release-3-0-specification-businesswire/` —— [A]。其中 **UWB 的精确测距（基于飞行时间）是抗中继的核心机制**：中继会引入额外时延，从而被距离判定识别。CCC 与 FiRa Consortium 就 UWB 技术合作 —— 来源：CCC 与 FiRa 合作公告 —— `https://carconnectivity.org/car-connectivity-consortium-and-fira-consortium-partner-on-uwb-technology-used-in-the-ccc-digital-key/` —— [B]；FiRa 技术规范 2.0（2023-11）、Core 3.0（2025-01）、Core 4.0（2025-12）—— 来源：FiRa Consortium 新闻页 —— `https://www.firaconsortium.org/news/press-releases/...` —— [B]。
- **D.3.1 / D.3.2**：控制对策为 SE 存储（CCC 明载），以及国际硬件根信任规范：GlobalPlatform TEE System Architecture v1.3（规范号 GPD_SPE_009）—— `https://globalplatform.org/specs-library/tee-system-architecture/` —— [A]；GlobalPlatform Secure Element 分类 —— `https://globalplatform.org/specs-library/?filter-committee=secure-element` —— [A]；NIST FIPS 140-3（密码模块安全要求）—— `https://csrc.nist.gov/pubs/fips/140-3/final` —— [A]；EVITA 定义车载 HSM 的 Full/Medium/Light 三级 —— `https://www.evita-project.org/` —— [B]。**中国侧**：GB/T 44402.1-2024《卡及身份识别安全设备 数字钥匙系统 第 1 部分：参考架构》（发布 2024-08-23，实施 2025-03-01）—— 来源：国标全公开系统 —— `https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=9CDE5F17C28F5332BA9CBEDD4618FD77` —— [A]。
- **D.4.1 / D.4.2**：**本报告构造的授权模型缺陷（推测，非事实）**。前置条件：车企的数字钥匙分享未绑定有效期/次数，或撤销事件未同步到车辆侧。可对照的**已取证类比**是 Tesla 虚拟密钥的撤销机制："吊销由用户在车辆 Locks 界面删除密钥完成"—— 来源：Tesla 虚拟密钥指南 —— `https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide` —— [A]，即撤销**在车端生效**。**本报告判断**：数字钥匙若把撤销只做在云侧/手机侧而不同步车端，则车主"已删除钥匙"的直觉可能与车辆实际状态不一致（推测，非事实；需实测验证任何具体车企）。

**检测点（构造）**：(1) 数字钥匙认证的测距值异常（UWB 距离与实际不符）；(2) 同一钥匙凭证在异地的进入尝试；(3) 车辆侧已删除的密钥仍能触发进入。

**写作纪律提示**：信源档案 §7.10 第 1 条明载——「蔚来 UWB+蓝牙+NFC 三合一数字钥匙」仅见新浪汽车等二手报道 —— `https://auto.sina.cn/2026-07-18/detail-iniicyyt8275101.d.html` —— [C]，**蔚来官方未取得技术说明；无法确认是否 CCC 3.0、是否有 SE 保护** —— 来源：信源档案 §7.10 —— [A，采证记录]。因此本章**不对任何中国车企的数字钥匙实现做断言**，只以 CCC/FiRa 规范作为"防中继设计的公开依据"提供对标框架。

### 14.3.5 攻击树 E：云端授权服务攻陷（混淆代理、越权代理、租户越界）

```
[E] 攻陷或滥用车企云端授权服务
├── [E.1] 混淆代理（confused deputy）
│   ├── [E.1.1] 第三方应用用低权限令牌调用云代理接口，代理以自身高权限访问资源
│   ├── [E.1.2] 代理未校验"最终代表谁"（缺 act/subject 链）
│   └── [E.1.3] 代理的 audience/scope 校验缺失（未校验 aud）
├── [E.2] 越权代理
│   ├── [E.2.1] 服务间凭证过宽（服务账号可签发任意令牌）
│   └── [E.2.2] 令牌交换未限制目标资源
├── [E.3] 租户越界
│   ├── [E.3.1] 车队客户的 A 车数据被 B 客户读取（多租户隔离失效）
│   └── [E.3.2] Partner Token 路径跨客户读取 vehicle_specs（无车主授权的例外路径）
└── [E.4] 授权服务器本体攻陷
    ├── [E.4.1] 签名密钥泄露 → 伪造任意令牌
    └── [E.4.2] 元数据端点被篡改 → 客户端指向恶意授权服务器
```

**节点说明**：

- **E.1**：混淆代理是"代理拥有的权限高于请求者"时的经典漏洞类。控制对策为 **RFC 8693 OAuth 2.0 Token Exchange**：用 `subject_token`（代表谁）+ `actor_token`（谁在代表）显式表达代授权链 —— `https://www.rfc-editor.org/rfc/rfc8693.txt` —— [A]。**本报告判断（推测，非事实）**：若车企云以"独立微服务的自有凭证"代第三方应用访问资源，而不在令牌中携带 `act`/`subject` 链，则资源侧无法区分"是应用自己越权"还是"云代理代为越权"。前置条件：云侧存在代理模式的服务间调用，且未采用令牌交换链路。**这是架构层面的判定，本次无任何车企证据，故仅作为检查项列入 §14.7。**
- **E.1.3**：control 依据 RFC 9068（JWT Profile for Access Tokens：`typ: at+jwt`、`aud`/`iss`/`exp` 校验要求）—— `https://www.rfc-editor.org/rfc/rfc9068.txt` —— [A]；Tesla `/token` 换码的 `audience` 参数**必须是 Fleet API base URL**（如 `https://fleet-api.prd.na.vn.cloud.tesla.com`）—— 来源：Tesla 第三方令牌 —— [A]。这是"令牌受众被显式约束"的 `[A]` 级实例。
- **E.2.1**：控制对策为 RFC 7523（服务账号 + 客户端断言）—— `https://www.rfc-editor.org/rfc/rfc7523.txt` —— [A]；RFC 7662 令牌内省可用于不透明令牌的实时校验 —— `https://www.rfc-editor.org/rfc/rfc7662.txt` —— [A]。
- **E.3.2**：此叶节点**直接对应 A10 的授权控制例外**：`vehicle_specs`/`vehicle_pricing_info` 仅 Partner Token 可用且对任意车辆无需车主授权 —— 来源：Tesla 认证概览 —— [A]。**本报告判断（推测，非事实）**：若 Partner 侧的客户边界（哪个 partner 可读哪些车辆）未在契约与审计层收紧，则该路径从"平台能力"退化为"横向读取面"。前置条件：Partner 凭证被滥用或跨客户授权缺失。**该判定在 §14.6 定为 High（授权控制例外 + 补偿控制建议）。**
- **E.4.1**：控制对策为阈值签名思想（TUF 四角色 + threshold/quorum 阈值模型 —— `https://theupdateframework.github.io/specification/latest/` —— [A]）在授权服务器签名密钥上的类比应用；以及 NIST SP 800-57 Part 1 Rev.5 密钥生命周期建议 —— `https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final` —— [A]。**本报告判断**：授权服务器的签名密钥是"签发任意令牌"的单一根，应按 HSMs / FIPS 140-3 保护并做密钥轮换（推测，非事实；前置条件：车企云侧密钥管理未采用 HSM 或未轮换）。
- **E.4.2**：控制对策为 RFC 8414（授权服务器元数据 `.well-known/oauth-authorization-server`）与 OIDC Discovery —— `https://www.rfc-editor.org/rfc/rfc8414.txt` —— [A]；Tesla 的元数据发布在 `https://fleet-auth.prd.vn.cloud.tesla.com/oauth2/v3/thirdparty/.well-known/openid-configuration` —— 来源：Tesla 认证概览 —— [A]。**本报告判断**：元数据端点若被 DNS/证书层劫持，客户端可能被引导到恶意授权服务器；缓解是证书固定与应用侧硬编码（推测，非事实）。

**检测点（构造）**：(1) 代理调用中缺少 `act`/`subject` 的令牌占比；(2) 服务的出站调用量与其自身 scope 不匹配；(3) 跨租户的数据读取（按 tenant 维度审计）；(4) 授权服务器签名密钥的使用频率与轮换记录。

### 14.3.6 攻击树 F：OTA 供应链

```
[F] 通过 OTA 供应链实现未授权代码/配置下发
├── [F.1] 攻陷更新仓库
│   ├── [F.1.1] 攻陷 Director 仓库元数据
│   ├── [F.1.2] 攻陷 Image 仓库产物
│   └── [F.1.3] 攻陷时间戳/快照角色（冻结攻击）
├── [F.2] 攻陷签名密钥
│   ├── [F.2.1] 单个签名密钥泄露（阈值签名可缓解）
│   └── [F.2.2] 阈值不足时伪造元数据
├── [F.3] 攻陷构建链
│   ├── [F.3.1] 构建环境被污染（SLSA 分级暴露）
│   └── [F.3.2] 依赖投毒（SBOM 缺失导致不可见）
├── [F.4] 滥用下发通道的授权
│   ├── [F.4.1] 用 vehicle_cmds 的"预约软件更新"权限触发非预期更新
│   └── [F.4.2] 通过遥测配置签名权下发恶意遥测配置
└── [F.5] 降级/回滚攻击
    └── [F.5.1] 回滚到已知有漏洞的旧固件版本
```

**节点说明（控制依据全部来自公开规范）**：

- **F.1 / F.2**：控制依据为 **Uptane**——"首个面向汽车、面向'可抵御国家级攻击者'设计的软件更新安全系统"，Linux Foundation Joint Development Foundation 项目，最新标准 **2.1.0**，采用 **Director 仓库 + Image 仓库双仓库模型** —— 来源：Uptane 官网与标准页 —— `https://uptane.org/` / `https://uptane.org/docs/latest/standard/uptane-standard` —— [A]；**TUF（The Update Framework）** 的 Root / Targets / Snapshot / Timestamp 四角色 + 委托 + **threshold/quorum 阈值模型**用于防仓库/密钥泄露 —— `https://theupdateframework.io/` —— [B] / `https://theupdateframework.github.io/specification/latest/` —— [A]。
- **F.1.3**：冻结攻击（freeze attack）通过让客户端停留在旧元数据上实现"看不到新撤销/新版本"。控制对策为 **Timestamp 角色**（TUF）—— 同上 —— [A]；以及可信时间戳 RFC 3161 —— `https://www.rfc-editor.org/rfc/rfc3161.txt` —— [A]。
- **F.3.1**：控制依据为 **SLSA v1.0 分级（Build L0–L3，供应链构建完整性）** —— `https://slsa.dev/spec/v1.0/levels` —— [A]；in-toto 规范（供应链完整性元数据与签名链）—— `https://in-toto.io/specs/` —— [B]。
- **F.3.2**：控制依据为 **SBOM**：SPDX 规范（对应国际标准 ISO/IEC 5962:2021）—— `https://spdx.dev/use/specifications/` —— [A]；CycloneDX 规范概览 —— `https://cyclonedx.org/specification/overview/` —— [B]。
- **F.4.1**：`vehicle_cmds` 覆盖"预约软件更新"—— 来源：Tesla 认证概览 —— `https://developer.tesla.com/docs/fleet-api/authentication/overview` —— [A]。**本报告判断（推测，非事实）**：若"预约软件更新"权限与"实际批准并安装某版本"权限未分离，则一个持有 `vehicle_cmds` 的应用可能触发超出车主预期的更新时序。前置条件：更新触发与更新批准在授权模型上未被拆成两个 scope。
- **F.4.2**：**已取证的强控制实例**：Fleet Telemetry 配置由应用私钥**签名**且"**Tesla 无法编辑**"；若所需 scope 被撤销导致配置失效，配置会被**从车辆移除** —— 来源：Tesla Fleet Telemetry —— `https://developer.tesla.com/docs/fleet-api/fleet-telemetry` —— [A]。车辆在**接受 Fleet Telemetry 配置前验证载荷签名** —— 来源：Tesla 虚拟密钥指南 —— [A]。
- **F.5.1**：控制依据为**版本单调性/反回滚**：Uptane 与 TUF 的元数据版本单调递增设计用于阻断降级 —— 同上 —— [A]；中国侧对应 GB 44496-2024《汽车软件升级通用技术要求》（发布 2024-08-23，实施 2026-01-01，强制性）—— 来源：国标全公开系统 —— `https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=8BC0D8B44DD4E71F9557BADE5175565A` —— [A]；GB/T 47325-2026《车联网在线升级安全技术要求与测试方法》（发布 2026-03-31，实施 2026-10-01）—— `https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=8407225889D602060265D0ABB8D14AA7` —— [A]。
- **SUIT 族**：RFC 9019（A Firmware Update Architecture for IoT Devices，SUIT 架构）—— `https://www.rfc-editor.org/rfc/rfc9019.txt` —— [A]；RFC 9124（A Manifest Information Model for Firmware Updates in IoT Devices，SUIT Manifest 信息模型）—— `https://www.rfc-editor.org/rfc/rfc9124.txt` —— [A]；IETF SUIT 工作组 —— `https://datatracker.ietf.org/wg/suit/about/` —— [A]；SUIT Manifest 草案 draft-ietf-suit-manifest-27 —— [C]。

**检测点（构造）**：(1) 客户端固件版本与元数据版本不单调（疑似降级）；(2) Timestamp 元数据过期未更新（疑似冻结）；(3) 构建产物的 SLSA provenance 缺失；(4) 更新触发与批准在日志上没有成对出现。

**对攻击树 F 的总体判断（本报告判断，非事实）**：OTA 供应链是本章"**控制依据最成熟但工程落地最不透明**"的一棵。**公开规范（Uptane/TUF/SLSA/SUIT/SBOM）已经把"应该怎么防"写得相当完整，但本次取证中，没有任何一家车企公开了其 OTA 的签名角色配置、阈值、SBOM 交付方式。** 这构成 §14.9 待补证清单的核心条目。前置条件与风险：这些控制的有效性依赖于车企实际部署的阈值与角色分离，而非规范存在本身。

---

## 14.4 协议级威胁剖析

本节从"协议原语"粒度过一遍最容易被工程实现忽略的威胁。与 §14.3 的攻击树不同，本节每一小节都**先给规范依据（[A]），再给攻击推演（标注），最后给控制映射**。

### 14.4.1 授权码拦截与 PKCE、原生 App 的重定向劫持与外部用户代理

**规范依据**：RFC 7636 (2015) PKCE 用于"公共客户端授权码拦截防护"—— `https://www.rfc-editor.org/rfc/rfc7636.txt` —— [A]；RFC 8252 (2017)《OAuth 2.0 for Native Apps》要求原生 App "必须使用系统浏览器/外部用户代理，禁止内嵌 WebView"—— `https://www.rfc-editor.org/rfc/rfc8252.txt` —— [A]；RFC 6749 (2012) 是 OAuth 2.0 授权框架本体 —— `https://www.rfc-editor.org/rfc/rfc6749.txt` —— [A]。

**车企实现侧的可引用锚点**：Tesla `/authorize` 的必填参数含 `response_type=code`、`client_id`、`redirect_uri`、`scope`、`state`（"用于校验的随机值"），可选 `nonce`（"用于防重放的随机值"）—— 来源：Tesla 第三方令牌 —— [A]。Mercedes 的错误语义含 "Invalid redirect URL"（redirect_uri 与注册值不一致）—— 来源：Mercedes 授权码流 —— [A]。

**威胁推演（本报告构造）**：

- **授权码拦截**：在公共客户端（无 `client_secret`）场景下，授权码若被中间人截获，攻击者可直接换取令牌。**PKCE 通过"授权请求时提交 `code_challenge`、换码时提交 `code_verifier`"** 使截获者无法完成换码（因为不知道 `code_verifier`）。前置条件：客户端**未启用 PKCE**。控制对策：强制 PKCE（RFC 7636；OAuth 2.1 草案 draft-ietf-oauth-v2-1-16 已把 PKCE 从"可选"改为"强制"—— `https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/` —— [A]）。
- **重定向劫持**：攻击者注册通配子域或接管应用声明的回调域名，把授权码重定向到自己。控制对策：`redirect_uri` 精确匹配（Mercedes 已实现 "Invalid redirect URL"）；应用侧对 `state` 做一次性校验。
- **WebView 截获**：若应用内嵌 WebView 呈现授权页，应用自身（或 WebView 中的恶意脚本）可读取用户在授权页的输入与 URL 上的授权码。控制对策：RFC 8252 的外部用户代理（系统浏览器）。**本报告判断（推测，非事实）**：这条控制的违反在移动端工程中并不罕见，但**本次取证没有任何车企公开文档可判定其是否遵守**，故列为 §14.7 的检查项而非结论。

**控制映射**：CP-1。严重度：若缺失 PKCE 且为公共客户端 → 授权码可被拦截 → 可换取 `vehicle_cmds` → 本报告判为 **High**（单一凭证被攻破可影响同账号车辆；对照 §14.6 判据）。

### 14.4.2 令牌重放的三条防线：短 TTL、发送方约束、时间戳与 nonce

**规范依据**：RFC 6750 (2012) OAuth 2.0 Bearer Token Usage（Bearer 令牌在 HTTP 中的使用、`WWW-Authenticate` 错误语义）—— `https://www.rfc-editor.org/rfc/rfc6750.txt` —— [A]；**发送方约束**：RFC 8705 (2020) Mutual-TLS Client Authentication and Certificate-Bound Access Tokens（"持有的令牌不可被复制盗用"）—— `https://www.rfc-editor.org/rfc/rfc8705.txt` —— [A]；RFC 9449 (2023) DPoP（`DPoP` 头 + JWK 指纹绑定）—— `https://www.rfc-editor.org/rfc/rfc9449.txt` —— [A]；**时间基准**：RFC 3161 (2001) Time-Stamp Protocol —— `https://www.rfc-editor.org/rfc/rfc3161.txt` —— [A]。

**三条防线的工程含义**：

1. **短 TTL**：Bearer 令牌是"持有即有权"的凭证（RFC 6750），一旦泄露即可被重放。缩短 TTL 缩小重放窗口。可对照的 `[A]` 级数值：Mercedes 默认 `expires_in` **3599 秒**（≈1 小时）—— 来源：Mercedes 授权码流 —— [A]。**本报告特别声明**：Tesla 访问令牌 TTL 在本次取证中**未获证实**，信源档案 §7.1 已将其列为待补证（"访问令牌 TTL 标记为待补证"）—— 来源：信源档案 §7.1 —— [A，采证记录]。**本章不给 Tesla 访问令牌 TTL 任何数值。**
2. **发送方约束（Sender-Constrained / Proof-of-Possession）**：把令牌与"持有某私钥"绑定，使被复制的令牌无法使用。RFC 8705 用 mTLS 证书绑定（令牌绑定到客户端证书的指纹），RFC 9449 用 DPoP（每次请求用 `DPoP` 头携带用私钥签的证明，绑定到令牌中的 JWK 指纹）。**这是车云链路最关键的授权规范**——信源档案 §2.1 对 RFC 8705 的标注即为此 —— 来源：信源档案 §2.1 —— [A]。
3. **时间戳与 nonce**：`nonce`（Tesla 文档描述为"用于防重放的随机值"）提供一次性的挑战值；RFC 3161 可信时间戳为"防重放的时间基准"提供可信时钟，避免依赖客户端本地时钟。

**攻击推演（本报告构造）**：

- 若仅有短 TTL 而无发送方约束，则"令牌泄露 → 攻击者在 TTL 内重放"仍然是完整的攻击路径。前置条件：令牌在 TTL 内被截获。
- 若仅有发送方约束而无短 TTL，则"持有私钥的攻击者"在令牌长时间有效时影响更大。三防线需**叠加**而非择一。
- **本报告判断（推测，非事实）**：车云场景中，`vehicle_cmds` 类令牌若只做 Bearer 而无线程绑定，则一次后端日志泄漏即可在 TTL 内执行真实车控。前置条件：**车企是否启用 mTLS/DPoP 未知**——本次无任何车企的此项公开证据（信源档案 §7.10 第 5 条明载 9 家国内车企的 mTLS 方向未找到公开来源）。**因此本报告不做"某车企未绑定"的断言，只将其列为验证项。**

**检测点（构造）**：(1) 同一令牌指纹出现在多个客户端证书/JWK 下（绑定应使其不可能）；(2) 令牌使用时刻的服务器时钟与 `iat`/`exp` 的偏离。

### 14.4.3 刷新令牌轮换的并发竞态与宽限期被滥用

**已取证事实（Tesla [A]）**：刷新令牌**一次性使用（single use only）且 3 个月后过期**；**最近一次使用的刷新令牌在 24 小时内仍有效**（用于覆盖"应用未能持久化轮换后令牌"的失败场景）；刷新失败返回 `401 login_required` 的两种场景为——刷新令牌过期/被更新令牌挤出，或**用户已重置密码** —— 来源：Tesla 第三方令牌 —— `https://developer.tesla.com/docs/fleet-api/authentication/third-party-tokens` —— [A]。此外，Tesla 文档明载 **scope 缩减与既有刷新令牌兼容，仅对新签发的访问令牌生效**；新增 scope 需以 `prompt_missing_scopes=true` 重新发起 `/authorize` —— 同上 —— [A]。

**Mercedes 的对照实现**：`grant_type=refresh_token` 时刷新令牌**一次性使用**，授权服务器返回**新的访问令牌与新的刷新令牌**；已用/无效刷新令牌报错 "The given refresh token is not valid or was already used"—— 来源：Mercedes 授权码流 —— [A]。

**并发竞态（本报告构造）**：多进程/多实例的应用若同时用同一刷新令牌发起刷新，则**只有一个能成功**，另一个会因"已被使用"失败。这会造成两类后果：（a）**可用性**：应用若未做串行化与失败重试，会陷入"两个实例互相把对方挤出"的抖动；（b）**安全**：轮换使旧令牌失效，理论上缩短了"旧令牌被窃"的窗口。**24 小时宽限期**正是为缓解（a）而设。

**宽限期被滥用（本报告判断，推测，非事实）**：24 小时宽限期把"上一次使用的刷新令牌"的失效时刻**延后了 24 小时**。若攻击者在应用完成下一轮轮换之前窃得旧刷新令牌，则其在宽限期内仍可用旧令牌换取新令牌，**并可能由此把合法应用挤出**（因为轮换是"你用一次，我就作废"的语义）。前置条件：①攻击者在 24 小时内窃得旧刷新令牌；②攻击者抢在合法应用轮换之前使用。**这是"可用性缓解措施引入安全窗口"的典型权衡**——本报告判断，非事实。

**scope 缩减的窗口（本报告判断，推测，非事实）**：文档明载 scope 缩减"仅对新签发的访问令牌生效"—— 来源：Tesla 第三方令牌 —— 同上 —— [A]。这意味着：车主在 `revoke/consent` 端点缩减 scope 后，**已签发的旧访问令牌在其 TTL 内仍携带旧 scope 的能力**。前置条件：旧访问令牌尚未过期。**缓解**：缩短访问令牌 TTL（但 Tesla 访问令牌 TTL 未取证，见 §14.4.2）或对车控类高影响 scope 采用"每次实时内省"（RFC 7662）—— **本报告判断**。

**检测点（构造）**：(1) 同一刷新令牌族出现"两个不同客户端在宽限期内各换出一次令牌"；(2) `revoke/consent` 事件后，旧访问令牌仍在被使用；(3) `401 login_required` 的异常集中爆发（可能是被挤出）。

### 14.4.4 consent phishing 与过度授权

**已取证事实**：Mercedes 的同意界面"展示所请求的 SCOPE 与 'purpose URL'，便于终端用户知情决策"；**`openid` scope 为获得有效令牌所必需，`offline_access` 为获得刷新令牌所必需** —— 来源：Mercedes 授权码流 —— [A]。Tesla 的 `/authorize` 提供 `prompt_missing_scopes=true`（对尚未授权的 scope 再次提示）与 `require_requested_scopes=true`（必须授权**全部**请求 scope 才放行）—— 来源：Tesla 第三方令牌 —— [A]。Tesla 的 `offline_access` = "获取刷新令牌以免重复登录"；`openid` = "Sign in with Tesla"—— 来源：Tesla 认证概览 —— [A]。

**威胁模式（consent phishing，本报告构造）**：攻击者不窃取凭证，而是**诱使车主自愿授权**一个看起来正当的应用，该应用申请了远超其功能所需的 scope（如仅仅需要读里程，却申请 `vehicle_cmds` + `vehicle_location`）。一次"同意"即长期放大：`offline_access` 换来刷新令牌（Tesla 3 个月；Mercedes 一次性轮换），此后攻击者可持续访问，直至车主主动撤销（Tesla 撤销入口见 §14.3.3 C.4.1）。

**"过度授权"的结构性成因（本报告判断，推测，非事实）**：

- ① **scope 粒度过粗**：Tesla 的 `vehicle_cmds` 是**一个 scope 覆盖**"添加/移除驾驶员、Live Camera 访问、解锁、唤醒、远程启动、预约软件更新"—— 来源：Tesla 认证概览 —— [A]。**本报告判断**：单个 scope 覆盖了从"读取性较低的操作（唤醒）"到"高影响操作（解锁/远程启动/Live Camera）"的整条光谱，意味着"想唤醒车辆"的应用不得不一并取得"解锁"的能力。前置条件：平台未对高影响操作拆分 sub-scope。
- ② **同意疲劳**：`prompt_missing_scopes=true` 若被应用在每次新增 scope 时反复触发，用户可能形成"一路同意"的习惯。前置条件：应用可自主发起新增 scope 的授权请求。
- ③ **缺少"用途绑定"的可验证性**：Mercedes 展示 purpose URL，但**purpose URL 的声明是否与 scope 匹配，规范与文档均未定义可验证机制**（本报告判断，推测，非事实）。

**控制映射**：RFC 9396 富授权请求（`authorization_details` 结构化权限对象，替代裸字符串 scope）是**资源级授权**的规范依据，被认为可缓解"scope 过宽"—— 来源：信源档案 §2.1 —— `https://www.rfc-editor.org/rfc/rfc9396.txt` —— [A]；RFC 9470 步进认证可用于在敏感操作前要求更强认证 —— [A]。严重度：本报告判为 **Medium**（令牌生命周期与授权范围管理不当导致影响范围扩大，对照审计计划 §3.3）。

**检测点（构造）**：(1) 应用声明的 purpose 与其请求 scope 的交集为空/极小；(2) 单次授权请求的 scope 数量异常；(3) 车主侧撤销率在特定应用上偏高。

### 14.4.5 混淆代理（confused deputy）与 RFC 8693 的 act/subject 链路设计

（本节与 §14.3.5 E.1 呼应，此处展开设计层面。）

**问题定义**：当车企云（或第三方云）作为**代理**替请求者访问下游资源时，下游若只校验"代理是否有权"，而不校验"代理此刻代表谁"，则任何能把请求交给代理的客户端都能**借用代理的更高权限**。这就是混淆代理。

**RFC 8693 的缓解设计**：Token Exchange 用 `subject_token`（代表的主体，如车主/车辆）+ `actor_token`（执行者，如第三方应用）表达代授权链，使**资源侧能同时看到"为谁做"与"谁在做"** —— `https://www.rfc-editor.org/rfc/rfc8693.txt` —— [A]。**本报告判断（推测，非事实）**：若车企云内部的令牌交换保留 `act`/`subject` 链，则越权调用会在资源侧留下可审计的"代授权路径"，从而把 §14.2 的 T-12（抵赖）与 T-22（权限提升）一并缓解；若缺失，则两者同时暴露。前置条件：云侧采用令牌交换而非"服务自有凭证直连"。

**控制映射**：RFC 8693（令牌交换）；RFC 9068（`aud` 校验，防令牌跨服务滥用）；RFC 9396（结构化授权详情）；RFC 7662（内省，为不支持 JWT 的不透明令牌提供实时校验）。**检查清单（构造）**：①授权服务器是否签发带 `act`/`subject` 的令牌；②资源服务是否强制校验 `aud`；③代理是否对下游请求带上请求者的 `subject` 而不仅是自身服务身份。

**检测点（构造）**：代理发起的调用中，源令牌与目标令牌的 `act`/`subject` 关系是否成对；同一服务身份对不同 `subject` 的调用是否在其自身权限内。

### 14.4.6 长连接（Fleet Telemetry 类推流）在授权撤销后的残留窗口分析

**已取证事实（Tesla [A]）**：Fleet Telemetry 让车辆**直连开发者服务器**，取代轮询 `vehicle_data` 端点 —— 来源：Tesla Fleet Telemetry —— `https://developer.tesla.com/docs/fleet-api/fleet-telemetry` —— [A]。前置条件：车辆固件 2024.26+（证书签名类应用需 2023.20.6+；Model S/X Intel Atom 需 2025.20+）；必须已配对虚拟密钥。配置由应用私钥**签名**且"**Tesla 无法编辑**"；若所需 scope 被撤销导致配置失效，配置会被**从车辆移除**。**单台车辆最多同时向 5 个第三方应用推流**。位置类字段需要 `vehicle_location`；`hide_private` 共享车辆访问位置会返回 **HTTP 403 "location access not granted"**。遥测传输：**500 ms 事件收集窗口**；按字段 `interval_seconds` 与变化触发上报。**断连处理：车辆缓冲 5000 条消息（≥2500 秒数据）；重连采用指数退避，最大重试延迟 30 秒** —— 来源：同上 —— [A]。

**授权撤销后的残留窗口分析（本报告判断，推测，非事实）**：

本节要回答的问题是：**当车主撤销 scope 后，"车辆→第三方服务器"的这条长连接在多久之内才真正停止泄露数据？** 这涉及三个时间量：

1. **撤销传播时延**：从 `revoke/consent` 到"配置失效并被从车辆移除"的传播时间。文档明载配置会被**从车辆移除**，但**未给出时延数值**——来源：Tesla Fleet Telemetry —— 同上 —— [A]（数值未取到）。
2. **断连缓冲**：车辆侧缓冲 **5000 条消息（≥2500 秒）** —— 来源：同上 —— [A]。**本报告判断**：若撤销发生在该缓冲已经积累数据、且连接恰好中断的时刻，则**在重连语义下，缓冲中"撤销前采集"的 5000 条消息是否仍会被推送给已撤销的应用？**——这是**残留窗口的核心问题**。前置条件：①撤销与连接中断几乎同时发生；②缓冲中的消息在重连后仍按原配置推流（而非在重连时重新校验授权）。**本报告不做"Tesla 存在该残留"的断言**，只指出：**"断连缓冲 + 授权撤销"的交互语义需要兜底说明，而本次文档未取到该说明，故列为待补证。**
3. **重连退避**：**指数退避，最大重试延迟 30 秒** —— 来源：同上 —— [A]。**本报告判断**：退避上限 30 秒意味着，一旦连接恢复，数据流将以最多 30 秒的探测间隔尝试恢复；**若撤销后的第一轮重连前的授权重校验缺失，则残留窗口与退避时延同阶（数十秒级）**。前置条件：重连时不重新校验授权。

**建议的兜底设计（本报告构造）**：①在重连握手时强制重新校验授权（"重连接=重新授权"）；②在撤销事件后主动令车辆侧丢弃/隔离缓冲区中未发送的消息；③对遥测流配置引入"授权有效期"字段（到期即自动回收，而非只在 scope 撤销时回收）；④推流侧（开发者服务器）在收到撤销通知后立即停止落库。这些建议是**构造**，不对应任何企业的已公开实现。

**检测点（构造）**：(1) `revoke/consent` 事件与车辆侧配置移除的时间差；(2) 撤销后来自同一车辆的入站连接仍在建立（异常）；(3) 缓冲消息的采集时刻与送达时刻跨越撤销事件的计数。

---

## 14.5 威胁 × 控制映射矩阵

本节把前述威胁条目汇总为一张 ≥25 行的矩阵（实际 28 行），列含义：**威胁 ID / 威胁描述 / STRIDE / 受影响层 / 已取证的现有控制 / 控制缺口 / 建议控制 / 严重度**。

**严重度判据**沿用审计计划 §3.3（Critical/High/Medium/Low/Informational），下文"严重度"列即按该口径判定；"控制缺口"列中标注 `未找到公开来源` 者 **不等于**"该企业无此控制"，而是"本次未取到可核验证据"。

| 威胁 ID | 威胁描述 | STRIDE | 受影响层 | 已取证的现有控制 | 控制缺口 | 建议控制（本报告构造） | 严重度 |
|---|---|---|---|---|---|---|---|
| TH-01 | 授权码在公共客户端被截获换取令牌 | S/I | CP-1 | PKCE（RFC 7636）；OAuth 2.1 草案强制 PKCE | 车企是否强制 PKCE 未知 | 强制 PKCE + 短授权码 TTL + 一次性授权码 | High |
| TH-02 | 原生 App 内嵌 WebView 截获授权码 | S/I | CP-1 | RFC 8252 强制外部用户代理 | 车企移动端实现未知 | 系统浏览器 + 应用侧回调校验 | High |
| TH-03 | redirect_uri 通配/子域接管导致重定向劫持 | S | CP-1 | Mercedes "Invalid redirect URL" 精确匹配 | 通用：子域接管未覆盖 | 精确匹配 + 禁止通配 + 回调域名监控 | High |
| TH-04 | 访问令牌被复制重放 | S/I | CP-5 | RFC 8705 mTLS / RFC 9449 DPoP（规范） | 车企是否启用发送方约束未知 | 高影响 scope 强制发送方约束 | High |
| TH-05 | 刷新令牌被窃且落在 24 小时宽限期内 | S/I | CP-5 | Tesla 一次性刷新 + 3 个月过期 + 24h 宽限 | 宽限期的安全窗口 | 延迟使用旧令牌时告警 + 绑定客户端 | Medium |
| TH-06 | 并发刷新竞赛导致可用性抖动 | D | CP-5 | 宽限期用于覆盖持久化失败 | 应用侧串行化未规定 | 应用侧刷新互斥 + 幂等重试 | Medium |
| TH-07 | 旧访问令牌在 scope 缩减后仍带旧能力 | E | CP-5 | 文档明载"仅对新签发访问令牌生效" | TTL 未取证（Tesla） | 高影响 scope 实时内省（RFC 7662） | Medium |
| TH-08 | 虚拟密钥私钥泄露 → 伪造任意车控指令 | T/E | CP-9 | 私钥不得托管域名；车辆校验载荷签名 | 私钥是否受 HSM 保护未知 | HSM 托管私钥 + 密钥轮换 | Critical |
| TH-09 | `.well-known` 公钥被替换 | T | CP-9 | 公钥须长期可用；私钥不入域名 | 公钥指纹固定机制未知 | 证书固定 + 指纹监控告警 | High |
| TH-10 | Partner Token 路径无车主授权读取 vehicle_specs | I | CP-5 | 文档明载"仅 Partner Token + 任意车辆 + 无需车主授权" | **授权控制例外路径** | 契约约束 + 逐次审计 + 归属可见性 | High |
| TH-11 | hide_private 车辆的位置被绕过 | I | CP-5 | hide_private=true → 403 "location access not granted" | 间接推断（构造） | 字段级最小化 + 推断抗性评估 | Informational（正面案例） |
| TH-12 | 位置经非位置字段间接推断 | I | CP-5 | 无公开证据 | 数据最小化程度未知 | 对高敏字段做聚合/降采样 | Low（未验证） |
| TH-13 | 数字钥匙 BLE/UWB 中继 | S | CP-2 | CCC DK3.0：BLE+UWB 精确测距；NFC 强制备用；SE 存密钥 | 车企实现与 CCC 版本未知 | UWB 距离绑定 + 中继检测 | High |
| TH-14 | SE 提取数字钥匙私钥 | I/E | CP-2 | SE 存储（CCC [A]）；GlobalPlatform SE/TEE [A]；FIPS 140-3 | 车企是否用 SE 未知 | 抗提取 SE + 密钥不可导出 | High |
| TH-15 | 数字钥匙撤销未在车端生效 | E | CP-2/CP-9 | Tesla 虚拟密钥车端删除生效 | 数字钥匙撤销同步未知 | 撤销原子同步 + 车端兜底 TTL | Medium |
| TH-16 | 云端混淆代理越权 | E | CP-6 | RFC 8693 act/subject 链（规范） | 车企是否启用未知 | 强制令牌交换 + act/subject 审计 | High |
| TH-17 | 服务账号凭证过宽，可签发任意令牌 | E | CP-6 | RFC 7523 客户端断言；RFC 9068 aud 校验 | 内部权限边界未知 | 最小权限服务账号 + aud 强校验 | High |
| TH-18 | 多租户越界（车队 A 读 B） | I/E | CP-6 | 无公开证据 | 租户隔离实现未知 | 租户维度强制隔离 + 审计 | Critical（若成立） |
| TH-19 | 授权服务器签名密钥泄露 | E | CP-6 | TUF 阈值签名思想（规范）；SP 800-57 密钥生命周期 | 密钥保护与轮换未知 | HSM + 密钥轮换 + 双人控制 | Critical |
| TH-20 | 授权服务器元数据端点被劫持 | S | CP-5 | RFC 8414 / OIDC Discovery | 固定机制未知 | 元数据证书固定 | Medium |
| TH-21 | API 配额被耗尽 → 服务暂停且推流移除不恢复 | D | CP-5 | 限流 60/3/30 次每分；计费上限默认 0；80%/100% 邮件 | 无自动恢复 | 配额告警 + 自动恢复策略 | Medium |
| TH-22 | 车队规模下遥测缓冲耗尽 | D | CP-3 | 缓冲 5000 条（≥2500 秒）；指数退避最大 30 秒 | 无持久队列 | 服务端持久队列 + 背压 | Medium |
| TH-23 | 撤销后残留窗口（断连缓冲 + 重连语义） | I | CP-3 | scope 撤销 → 配置从车辆移除 | 时延未取证；重连是否重校验未知 | 重连接=重新授权 + 撤销即清缓冲 | Medium（需验证） |
| TH-24 | OTA 仓库元数据被攻陷 | T | CP-7 | Uptane 2.1.0 双仓库；TUF 四角色阈值 | 车企签名角色配置未知 | 阈值签名 + 角色分离 | Critical |
| TH-25 | OTA 冻结/降级攻击 | T | CP-7 | TUF Timestamp 角色；RFC 3161 可信时间戳 | 反回滚实现未知 | 版本单调 + 时间戳校验 | High |
| TH-26 | OTA 构建链污染 | T | CP-7 | SLSA v1.0 L0–L3；in-toto | 车企 SLSA 等级未知 | 构建证明 + 可复现构建 | High |
| TH-27 | 依赖投毒且 SBOM 缺失导致不可见 | T | CP-7 | SPDX / CycloneDX SBOM | 车企 SBOM 交付未知 | 强制 SBOM + 依赖监控 | Medium |
| TH-28 | 授权决策日志缺失导致不可追责 | R | 全域 | 车主侧撤销端点（Tesla [A]） | 日志内容未找到公开来源 | 记录决策依据（谁/何scope/何时/何策略） | Low |

**矩阵的三点说明（本报告判断，非事实）**：

1. **Critical 类（TH-08、TH-18、TH-19、TH-24）全部是"根级信任被攻陷"**：虚拟密钥私钥、多租户隔离、授权服务器签名密钥、OTA 签名根。它们共同的特征是：**一旦失陷，下游所有控制形同虚设**。这与审计计划 §3.3 对 Critical 的判据（"授权链可被绕过，导致任意车辆车控/位置被未授权访问；或根密钥可被远程提取"）一致 —— 来源：审计计划 §3.3 —— [A]。
2. **"控制缺口"列中大量为"未知"而非"缺失"**：这是本次取证条件的直接后果。把"未知"当"缺失"会违反中立性红线（审计计划 §3.2.4）。
3. **建议控制列全部为本报告构造**，其中一部分有规范依据（括号内的 RFC/标准），一部分为工程惯例构造。

---

## 14.6 严重度分类应用

本节严格沿用审计计划 §3.3 的判据与报告处理要求，逐条判定。判据原文（信源档案与审计计划均已固定）—— 来源：审计计划 §3.3 —— `docs/00-engagement-plan.md` —— [A]：

| 等级 | 判据（满足其一） | 报告中的处理 |
|---|---|---|
| **Critical** | 授权链可被绕过，导致任意车辆车控/位置被未授权访问；或根密钥可被远程提取 | 必须在"对比与差异"中作为行业级风险单列，并给出缓解控制 |
| **High** | 单一应用/单一凭证被攻破可横向影响同账号其他车辆或平台其他租户 | 单列控制建议（最小权限、令牌绑定） |
| **Medium** | 令牌生命周期管理不当（长效令牌、无轮换、无吊销联动）导致影响范围扩大 | 归入"工程实现参考"的控制清单 |
| **Low** | 文档与可观测性缺失、日志不含授权决策依据 | 归入合规映射章节 |
| **Informational** | 架构观察、行业趋势判断 | 归入"总结与趋势" |

### 14.6.1 [High] `vehicle_specs` / `vehicle_pricing_info` 的 Partner 路径（授权控制例外）

**事实**：Tesla 文档明载 `vehicle_specs` **仅 Partner Token 可用**，且对**任意车辆**可用、**无需车主授权**；`vehicle_pricing_info` **仅 Partner Token 可用** —— 来源：Tesla 认证概览 —— `https://developer.tesla.com/docs/fleet-api/authentication/overview` —— [A]。审计计划 §3.3 的 CSO 判定示例已将其归为 **High**（"授权控制例外，需在报告中显式标注为'退出逐车主同意模型'的路径，并建议以契约与审计补偿"）—— 来源：审计计划 §3.3 —— [A]。

**判定理由**：该路径满足 High 的判据"单一应用/单一凭证被攻破可横向影响同账号其他车辆或平台其他租户"——更准确地说，**它绕过的是"逐车主同意"这一整个授权模型**：Partner Token 一旦被滥用（或 Partner 滥用其凭证），可对**任意车辆**读取这两类数据，而车主既未被征询、也（据公开文档）无直接的同意记录可追索。**本报告判断（推测，非事实）**：该路径的合法商业用途（二手车估值、保险定价、车队分析）需要跨车辆批量读取，因此"退出逐车主同意"在业务上有其合理性；**问题不在路径存在，而在缺少可归因的审计与契约边界**。前置条件：Partner 凭证被滥用，或 Partner 侧的客户/车辆范围边界未在契约层收紧。

**补偿控制建议（本报告构造）**：①对该路径的**每次访问**记录请求者、车辆 VIN 哈希、时刻、字段集合（可归因审计）；②在车主侧提供"数据使用通知/退出"的可观测入口（即使不逐次同意，也让车主可见）；③对 Partner 侧做客户边界限定（某 partner 仅能读其契约范围内的车辆）；④对读取频率做异常检测（GB/T 45181-2024 异常行为检测的适用方向 —— 来源：国标全公开系统 —— `https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=29740120554AA4DCB87A8FEAE106BA43` —— [A]）。

### 14.6.2 [Informational → 正面控制案例] `granular_access.hide_private` 的 403 行为

**事实**：Tesla 文档明载带 `granular_access.hide_private=true` 的车辆共享，即使被授予 `vehicle_location` 也拿不到任何位置，且无法流式传输位置字段 —— 来源：Tesla 认证概览 —— 同上 —— [A]；Fleet Telemetry 中"`hide_private` 共享车辆尝试访问会被拒绝并返回 **HTTP 403 'location access not granted'**"—— 来源：Tesla Fleet Telemetry —— `https://developer.tesla.com/docs/fleet-api/fleet-telemetry` —— [A]。

**判定理由与处理**：审计计划 §3.3 的 CSO 判定示例已将其归为 **Informational→正面控制案例**（"双层授权控制"的良好实践，建议其他车企对标）—— 来源：审计计划 §3.3 —— [A]。**本报告判断（推测，非事实）**：该设计的意义在于它区分了"**授权层**（scope 是否授予）"与"**资源策略层**（该资源此刻是否允许该字段）"这两个判定，并在**资源策略层做了更严的收窄**。这正对应 RFC 9396 富授权请求所倡导的"资源级授权"方向 —— `https://www.rfc-editor.org/rfc/rfc9396.txt` —— [A]。前置条件：车企在资源侧实际实现了第二层判定（而非仅靠文档承诺）。**该案例应作为"对标正向"写入 §14.10 与对比章节。**

### 14.6.3 [Medium] 长效令牌 / 无轮换 / 无吊销联动类缺陷

**判据**：Medium 判据为"令牌生命周期管理不当（长效令牌、无轮换、无吊销联动）导致影响范围扩大"—— 来源：审计计划 §3.3 —— [A]。

**逐项对照（本报告判定）**：

- **长效令牌**：Tesla 刷新令牌 3 个月有效、Mercedes 刷新令牌一次性轮换（返回新访问令牌与新刷新令牌）—— 来源：Tesla 第三方令牌 / Mercedes 授权码流 —— [A]。**本报告判断**：3 个月的有效期本身是"长效"的，但被"一次性使用 + 24h 宽限"部分抵消。若某实现既不轮换又有长有效期，则直接落入 Medium。**车企是否如此未知。**
- **无轮换**：无法从公开文档判定任何车企"无轮换"；Mercedes 与 Tesla 均有轮换。**故本项对中国车企标"未找到公开来源"，不下判定。**
- **无吊销联动**：**正面证据**——Tesla 有 scope 撤销 → 配置从车辆移除的联动（Fleet Telemetry）—— 来源：Tesla Fleet Telemetry —— [A]；车主侧撤销入口 —— 来源：Tesla 第三方令牌 —— [A]。**反面检查点**——§14.4.6 的残留窗口未取到时延说明。**本报告判断**：残留窗口若成立则属 Medium，但**需实测验证，不构成对任何车企的缺陷断言**。
- **吊销端点的规范要求**：RFC 7009 OAuth 2.0 Token Revocation —— `https://www.rfc-editor.org/rfc/rfc7009.txt` —— [A]；RFC 7662 内省 —— [A]。

**处理**：归入"工程实现参考"的控制清单（审计计划 §3.3 对 Medium 的要求）—— 建议清单见 §14.5 矩阵中 TH-05/TH-06/TH-07/TH-15/TH-20/TH-21/TH-22/TH-23/TH-27。

### 14.6.4 [Low] 日志缺少授权决策依据

**判据**：Low 判据为"文档与可观测性缺失、日志不含授权决策依据"—— 来源：审计计划 §3.3 —— [A]。

**事实与判定**：本次取证中，**未取到任何车企公开的授权决策日志格式文档**（Tesla/Mercedes 已读页面均未见此文档）—— 来源：信源档案 §7 —— [未找到公开来源]。**本报告明确声明：这属于"披露缺口"，不构成"该企业日志不含决策依据"的断言。** 但作为**检查项**，授权决策日志应至少包含：主体（sub/act）、资源（车辆/字段）、动作、决策结果、命中的策略 ID、时刻（可信时钟 RFC 3161）—— 本报告构造的清单。

**处理**：归入合规章节（审计计划 §3.3 对 Low 的要求），即由 WF-6 的 `18-authz-80-compliance-audit.md` 承接。

### 14.6.5 [Informational] 架构观察与行业趋势

**判据**：Informational 判据为"架构观察、行业趋势判断"—— 来源：审计计划 §3.3 —— [A]。本报告归入此类的观察（均为**判断**，标注如下）：

- **观察一（本报告判断，推测，非事实）**：授权模型正从"裸字符串 scope"向"资源级 / 结构化授权"演进，规范依据为 **RFC 9396 富授权请求**（`authorization_details`）与 **RFC 9635 GNAP**（Grant Negotiation and Authorization Protocol，2024-10，面向"细粒度 + 可协商"授权）—— 来源：信源档案 §2.1 —— `https://www.rfc-editor.org/rfc/rfc9635.txt` —— [A]。前置条件：企业实际采纳这些新规范。
- **观察二（本报告判断，推测，非事实）**：车控类高影响操作与读取类操作**尚未在 scope 层充分拆分**（Tesla `vehicle_cmds` 覆盖从唤醒到解锁的整条光谱 —— 来源：Tesla 认证概览 —— [A]）。趋势应是把高影响动作拆为独立 scope 并配合步进认证（RFC 9470）—— [A]。
- **观察三（本报告判断，推测，非事实）**：中国侧标准已把"车联网平台侧防护"与"接口治理"显式化（GB/T 47324-2026《车联网平台网络安全防护要求》发布 2026-03-31 实施 2026-10-01 —— `https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=90F36FFBED2E85627B648B837A522527` —— [A]；GB/T 47467-2026《车联网安全管理接口规范》发布 2026-04-30 实施 2026-11-01 —— `https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=AC95A675E7B6E8E822E66B30BE14ED5C` —— [A]），趋势是"授权与访问控制从企业自主走向国标约束"。

**处理**：归入"总结与趋势"（审计计划 §3.3 对 Informational 的要求）。

---

## 14.7 攻击可行性评估方法（可复现）

本节给出一套"**检测点 → 观测数据 → 判定规则**"的可复现清单，供后续**实车/沙箱验证**使用。**必须显式声明的边界：本次为公开信息调研，未做任何实车测试、未做任何渗透、未做任何逆向** —— 来源：审计计划 §1 范围外声明 —— `docs/00-engagement-plan.md` —— [A]。本节给出的方法本身是**本报告构造**，不对应任何已执行的测试。

### 14.7.1 方法总则

1. **只做授权行为观测，不做漏洞利用**：所有观测应在**合法授权的沙箱账号**上进行（如申请官方开发者沙箱，Tesla 的限流与计费机制天然限制了滥用面 —— 来源：Tesla 计费与限流 —— [A]）。
2. **以"文档声明的控制"为假说，以"观测结果"为证据**：例如"文档称 hide_private 车辆返回 403"是一个可证伪的假说；观测该响应即完成一次验证。
3. **不作能力反推**：任一检测点"未观测到异常"**不能**推出"该车企安全"；"无法观测"**不能**推出"该车企不安全"。

### 14.7.2 检测点清单

| DP | 检测点 | 观测数据 | 判定规则（构造） | 关联威胁 |
|---|---|---|---|---|
| DP-01 | PKCE 强制 | `/authorize` 是否接受无 `code_challenge` 的请求 | 若接受 → 未强制 PKCE | TH-01 |
| DP-02 | 外部用户代理 | 授权页能否在系统浏览器打开 | 若仅 WebView 可用 → 违反 RFC 8252 | TH-02 |
| DP-03 | redirect_uri 精确匹配 | 用未注册的 redirect_uri 请求 | 应返回 "Invalid redirect URL" 类错误 | TH-03 |
| DP-04 | 授权码一次性 | 同一 code 二次换码 | 应返回 "Invalid grant" 类错误 | TH-01 |
| DP-05 | 刷新令牌一次性 | 同一 refresh_token 二次刷新 | 应报 "already used" 类错误 | TH-05/TH-06 |
| DP-06 | 24h 宽限期行为 | 轮换后旧刷新令牌在 24h 内是否可用 | 可用即印证宽限语义 | TH-05 |
| DP-07 | 令牌 TTL 读取 | `/token` 响应的 `expires_in` | 记录数值（Tesla 未取证项，**实测可补**） | TH-04 |
| DP-08 | 发送方约束 | 换机/换 IP 后令牌是否仍可用 | 仍可用 → 未启用 mTLS/DPoP 绑定 | TH-04 |
| DP-09 | scope 缩减生效点 | 缩减 scope 后旧访问令牌是否仍可用旧能力 | 仍可用 → 印证"仅对新令牌生效" | TH-07 |
| DP-10 | hide_private 拒绝 | 对 hide_private 车辆请求位置字段 | 应返回 403 "location access not granted" | TH-11 |
| DP-11 | 推流上限 | 同车第 6 个应用请求推流 | 应因 5 应用上限被拒 | TH-22 |
| DP-12 | 撤销联动时延 | 撤销 scope 到车辆配置移除的时间差 | 记录时延（未取证项，**实测可补**） | TH-23 |
| DP-13 | 断连缓冲语义 | 断连→撤销→重连，观察缓冲消息是否推送 | 若推送撤销前消息 → 残留窗口成立 | TH-23 |
| DP-14 | 内省支持 | 是否存在 RFC 7662 内省端点 | 存在则可做实时校验 | TH-07 |
| DP-15 | 元数据端点 | `.well-known/openid-configuration` 内容 | 记录 issuer/端点，核对与文档一致 | TH-20 |
| DP-16 | 虚拟密钥配对前置 | 未授予三类 scope 之一时能否配对 | 应被拒（Tesla 明载需至少一项） | TH-08 |
| DP-17 | 密钥数量上限 | B2B 自动配对的已配对密钥数 | 应为 <20 把 | TH-08 |
| DP-18 | 配额耗尽行为 | 达计费上限后的 API 行为 | 记录是否暂停且推流移除不恢复 | TH-21 |
| DP-19 | 限流维度 | 同账号多应用是否共享限额 | 记录是否共享 | TH-21 |
| DP-20 | 日志可得性 | 是否可导出"授权决策"日志 | 不可得 → 观测性缺口（非缺陷） | TH-28 |

### 14.7.3 使用边界

- **DP-07 / DP-12 是本章明确的"可补证空位"**：Tesla 访问令牌 TTL 与撤销联动时延在本次取证中均未取到（信源档案 §7.1 明载 TTL 待补证；§8 覆盖度表给出"实机走一遍 token 响应读取 `expires_in`"的补证动作）—— 来源：信源档案 §7.1 / §8 —— [A]。
- **DP-01 至 DP-06 可在沙箱静默完成，不触及车控**；DP-10 至 DP-13 需要 **hide_private 共享车辆**与**已配对虚拟密钥**，属高门槛验证。
- **DP-08 的"换机"测试必须在授权范围内进行**（不得对未授权车辆执行）。
- **所有测试必须遵守沙箱条款与车企漏洞政策**：例如 Tesla 车辆/能源产品问题须邮件报至 `vulnerabilityreporting@tesla.com` 并使用 Tesla GPG 公钥、不走 Bugcrowd 网页表单；硬件研究须先向 Tesla 登记车辆 —— 来源：Tesla 漏洞披露与赏金 —— `https://bugcrowd.com/engagements/tesla` —— [A/B]。规则要点：若访问到不属于自己的数据须在 24 小时内停止并披露；未经批准不得公开披露已确认未修复漏洞 —— 来源：同上 —— [B]。

---

## 14.8 合规红线与威胁的对齐

本节把前述威胁条目与中国已取证的标准条目对齐。**纪律：只引用信源档案中已取证的条目；不给条款号；凡标准正文未取到者标 [未验证]。**

### 14.8.1 已取证的标准条目（[A]）

| 标准/法规 | 名称 | 发布/实施 | 与威胁模型的对齐点（本报告判断） | 等级 |
|---|---|---|---|---|
| GB 44495-2024 | 汽车整车信息安全技术要求（**强制性**） | 发布 2024-08-23，实施 2026-01-01 | 整车信息安全基线，2026-01-01 起对新车型强制适用；授权/访问控制属其要求域之一 | [A] |
| GB 44496-2024 | 汽车软件升级通用技术要求（**强制性**） | 发布 2024-08-23，实施 2026-01-01 | OTA 通道（攻击树 F）的强制合规基线 | [A] |
| GB/T 47324-2026 | 车联网平台网络安全防护要求 | 发布 2026-03-31，实施 2026-10-01 | **直接命中本报告主题：车联网云平台侧的防护要求**（授权服务、租户隔离、越权防护） | [A] |
| GB/T 47325-2026 | 车联网在线升级安全技术要求与测试方法 | 发布 2026-03-31，实施 2026-10-01 | OTA（攻击树 F）的测试方法依据 | [A] |
| GB/T 47467-2026 | 车联网安全管理接口规范 | 发布 2026-04-30，实施 2026-11-01 | **接口层规范，与授权/访问控制的 API 治理直接相关** | [A] |
| GB/T 45181-2024 | 车联网网络安全异常行为检测机制 | 发布 2024-12-31，实施 2025-04-01 | 对应 §14.7 的检测点（异常行为）与 TH-10/TH-18 的审计方向 | [A] |
| GB/T 44402.1-2024 | 卡及身份识别安全设备 数字钥匙系统 第 1 部分：参考架构 | 发布 2024-08-23，实施 2025-03-01 | 数字钥匙授权模型（攻击树 D）的国标参考架构 | [A] |
| GB/T 45112-2024 | 基于 LTE 的车联网无线通信技术 安全证书管理系统技术要求 | 发布 2024-12-31，实施 2025-04-01 | "车-云-车"证书体系的国家级规范（CP-3） | [A] |
| GB/T 41871-2022 | 信息安全技术 汽车数据处理安全要求 | 发布 2022-10-14，实施 2023-05-01 | 数据资产（A1–A9）处理合规基线 | [A] |
| GB/T 44464-2024 | 汽车数据通用要求 | 发布/实施 2024-08-23 | 同上 | [A] |
| GB/T 40857-2021 | 汽车网关信息安全技术要求及试验方法 | 发布 2021-10-11，实施 2022-05-01 | 网关访问控制（CP-7） | [A] |
| GB/T 40856-2021 | 车载信息交互系统信息安全技术要求及试验方法 | 发布 2021-10-11，实施 2022-05-01 | 车机侧（CP-4）与信息交互 | [A] |
| GB/T 40855-2021 | 电动汽车远程服务与管理系统信息安全技术要求及试验方法 | 发布 2021-10-11，实施 2022-05-01 | 车云远程服务的授权与访问控制 | [A] |
| GB/T 38628-2020 | 信息安全技术 汽车电子系统网络安全指南 | 发布 2020-04-28，实施 2020-11-01 | 方法论层（TARA 类） | [A] |
| 《汽车数据安全管理若干规定（试行）》 | 网信办等五部门令第 7 号 | 2021-08-16 成文，2021-10-01 施行 | 重要数据目录、境内存储、年度报送、出境评估义务 | [A] |
| GB/T 32918.1~.5、GB/T 32905、GB/T 32907、GB/T 35275、GB/T 35276 | SM2 / SM3 / SM4 及使用规范 | — | 中国密码算法的国标底座（**但 9 家国内车企是否采用未找到公开来源**） | [A] |
| RFC 8998 (2021) | ShangMi (SM) Cipher Suites for TLS 1.3 | — | 国密 TLS 在国际标准层面的唯一落点，国产车云链路合规的关键 | [A] |

### 14.8.2 未取证条目（不得给条款号）

以下方向本次**未取得一手正文**，一律标 `[未验证]`，**不得作为条款级依据，不得给出条款编号**：

| 条目 | 本次状态 | 证据等级 |
|---|---|---|
| UN R155（CSMS）/ R156（SUMS） | unece.org 被 Cloudflare 全站拦截，URL 结构需复核 | [未验证：依通行公开认知] |
| ISO/SAE 21434:2021 | SAE 收录页可达；ISO 官方页被 Cloudflare 拦截 | [未验证：编号与年份为通行共识，正文未取到] |
| ISO 24089:2023 | iso.org Cloudflare 拦截 | [未验证] |
| ISO 15118-2 / -20（Plug & Charge） | iso.org Cloudflare 拦截，标准号需复核 | [未验证] |
| IEEE 1609.2 | HTTP 200，正文未解析 | [C] |
| IEEE 802.15.4z | 未取得可核验官方 URL | [未验证] |
| 美国 SCMS | 未取得可核验官方 URL | [未验证] |
| SHE（Secure Hardware Extension）规范 | 成员制规范，未找到可核验公开一手 URL | [未找到公开来源] |
| UMA 2.0 | Kantara 站点 curl 超时 | [未验证] |
| AUTOSAR Classic Platform（Crypto Stack / SecOC / IdsM） | autosar.org 超时 | [未验证] |
| TCG TPM 2.0 规范 | TCG 站点 403/超时 | [未验证] |
| 欧盟 GDPR / Data Act | EUR-Lex 返回 202 HTTP 异步，正文未取到 | [C] |

**信源档案 §1.4 的写作纪律提示在此完整适用**：涉及 R155/R156 的**具体条款号、强制时间表、审核要求**时本次无一手来源；凡引用必须标注「[未验证] 依通行公开认知」或改为待补证陈述，**不得给出条款编号** —— 来源：信源档案 §1.4 —— [A]。

### 14.8.3 合规红线与威胁的对齐结论（本报告判断，非事实）

- **中国监管已把"车联网平台侧防护"与"接口治理"从企业自主升级为国标约束**（GB/T 47324-2026、GB/T 47467-2026）—— 来源：国标全公开系统 —— [A]。**本报告判断**：§14.5 中 TH-16（混淆代理）、TH-17（服务账号过宽）、TH-18（租户越界）这三类"云侧授权内部威胁"将日益落入 GB/T 47324 的要求域。前置条件：该标准在 2026-10-01 实施后对企业产生实际约束（实施日期为 `[A]` 已取证）。
- **异常行为检测已有国标**（GB/T 45181-2024）—— 来源：同上 —— [A]，它恰好补上了 §14.2 中"R 与 I 两类控制最薄"的观测缺口方向。
- **数字钥匙有国标参考架构**（GB/T 44402.1-2024）—— 来源：同上 —— [A]，为攻击树 D 的中立对标提供依据（避免只参照 CCC 这一国际来源）。

---

## 14.9 本章待补证清单

| # | 待补证项 | 当前状态 | 关联章节 | 建议补证方式 |
|---|---|---|---|---|
| G-01 | Tesla 访问令牌 TTL（`expires_in`） | 未获证实（信源档案 §7.1 明载待补证） | §14.4.2、§14.6.3 | 实机走一遍 `/token` 读取响应 |
| G-02 | Tesla 撤销 → 车辆配置移除的时延 | 未取到 | §14.4.6、§14.7.2 DP-12 | 沙箱观测撤销事件与配置消失时间差 |
| G-03 | 断连缓冲在撤销后的推送语义 | 文档未说明 | §14.4.6、§14.7.2 DP-13 | 断连→撤销→重连的实测 |
| G-04 | 各车企授权决策日志的字段与可得性 | 未找到公开来源 | §14.6.4 | RFI / 安全白皮书索取 |
| G-05 | 各车企授权服务器元数据端点与 `aud` 校验 | 未取到（Tesla 元数据 URL 已取证） | §14.3.5 E.1.3 | 直取 `.well-known` 并核对 |
| G-06 | 各车企云内部令牌交换的 `act`/`subject` 链 | 无任何证据 | §14.4.5 | 内部架构文档 / 安全评审材料 |
| G-07 | 9 家国内车企的 mTLS / 国密 / HSM / SE / TEE 实现 | **全部未找到公开来源**（信源档案 §7.10 第 5 条） | §14.3.4、§14.3.6 | RFI / 采购白皮书 / 器件选型 / 拆解 |
| G-08 | 小鹏开放平台鉴权细节 | `open.xiaopeng.com` HTTP 403 拒绝服务 | §14.1.3 CP-1 | 商务渠道申请沙箱账号 |
| G-09 | 华为鸿蒙座舱安全与数字车钥匙 | developer.huawei.com 文档 JS 空壳 | §14.3.4 | 带 JS 渲染的抓取（须登录） |
| G-10 | BMW CarData / OAuth | developer.bmwgroup.com 占位页 | §14.1.3 | 换出口 IP 或代理后重跑 |
| G-11 | Rivian Fleet API | CloudFront 区域封锁 | §14.1.3 | 换出口 IP |
| G-12 | R155/R156 条款与时间表 | unece.org Cloudflare 拦截 | §14.8.2 | 恢复检索额度或用官方 PDF 直链 |
| G-13 | ISO 21434 / 24089 / 15118 正文 | iso.org Cloudflare 拦截 | §14.8.2 | 标准购买渠道或 SAE 页面 |
| G-14 | UMA 2.0 / AUTOSAR / TPM 2.0 / SHE / IEEE 802.15.4z | 站点不可达或成员制 | §14.8.2 | 会员渠道获取规范正文 |
| G-15 | 各车企 OTA 的签名角色配置、阈值、SBOM 交付方式 | 无任何车企公开 | §14.3.6 | 采购白皮书 / 供应链问卷 |
| G-16 | 数字钥匙撤销的车端同步语义 | 仅 Tesla 虚拟密钥有车端删除证据 | §14.3.4 D.4.2 | 实车验证（须授权） |
| G-17 | `vehicle_specs` Partner 路径的契约与审计边界 | 仅知"仅 Partner Token + 无需车主授权" | §14.6.1 | Partner 协议文本 / 商务问询 |

**方法论声明（写入正文）**：本次调研因检索工具额度耗尽，采用"权威 URL 直取 + 逐条标注证据等级"的方法。**本章所有"未找到公开来源"均为本次披露缺口，绝不等于能力缺口；不得反向推断为"该企业不具备该能力"** —— 来源：信源档案 §0 / 审计计划 §3.2.4 —— [A]。

---

## 14.10 本章小结

### 14.10.1 本章产出回顾

本章在"授权与访问控制"专题的第 5 个切面上，完成了四类结构化产物：

1. **资产与主体清单**（15 类资产 + 10 类主体 + 9 个控制点的信任边界图），为后续所有分析提供公因子。
2. **STRIDE 逐层映射 24 行**，覆盖 CP-1 至 CP-9 九个穿越点 × 六类威胁。
3. **6 棵攻击树**（未授权车控 / 位置轨迹窃取 / 令牌窃取滥用 / 数字钥匙中继重放 / 云端授权服务攻陷 / OTA 供应链），每棵含 ASCII 树、前置条件、检测点。
4. **28 行威胁 × 控制映射矩阵** 与**逐条严重度判定**（§14.6）。

### 14.10.2 最高优先级的三类结构性风险（本报告提炼）

**风险一：根级信任的单点化（Critical 类，对应 TH-08 / TH-18 / TH-19 / TH-24）。**
虚拟密钥私钥、多租户隔离、授权服务器签名密钥、OTA 签名根，四者一旦失陷，下游所有控制形同虚设。**本报告判断（推测，非事实）**：这四者的共同缓解方向是**阈值化与分离**——TUF/Uptane 的 threshold/quorum 阈值模型（`https://theupdateframework.github.io/specification/latest/` —— [A]）已经在 OTA 侧给出了成熟范本，授权服务器签名密钥与虚拟密钥托管应借鉴同一思想。前置条件：企业在实际部署中采用阈值签名、HSM 保护与密钥轮换（本次无任何车企的部署证据）。

**风险二：授权模型中的"例外路径"缺乏可归因审计（High 类，对应 TH-10）。**
`vehicle_specs` / `vehicle_pricing_info` 仅 Partner Token 可用且对任意车辆无需车主授权，这是信源档案中唯一被明文记载的"退出逐车主同意模型"的路径 —— 来源：Tesla 认证概览 —— [A]；审计计划 §3.3 已判为 High —— [A]。**本报告判断（推测，非事实）**：例外路径本身有商业合理性，但**必须在契约层限定客户边界、在审计层做逐次可归因记录**，否则一次 Partner 凭证滥用即可横向读取大量车辆的非公开数据。前置条件：企业未对该路径做逐次审计。

**风险三：可观测性缺口（Low 类转系统性风险，对应 TH-28 与 §14.2 的 R/I 薄弱带）。**
本章 24 行 STRIDE 中，R（抵赖）类仅 2 行、I（信息泄露）类 5 行，且多行落在"日志/租户隔离未找到公开来源"。**本报告判断（推测，非事实）**：授权与访问控制的有效性**最终取决于能否回答"谁在何时基于哪条策略做了什么"**；当授权决策日志缺失时，前述所有控制都退化为"不可验证的承诺"。缓解方向：按 GB/T 45181-2024（车联网网络安全异常行为检测机制 —— [A]）建立异常行为基线，并对每一条授权决策记录主体（`sub`/`act`）、资源、动作、结果、策略 ID 与可信时刻（RFC 3161 —— [A]）。

### 14.10.3 本章的诚实性边界（再次声明）

- **本章的攻击树与威胁条目全部为结构化推演，不代表任何已发生的真实攻击。** 凡叶节点引用规范或车企文档者，其"控制对策"有 `[A]` 依据；凡为构造者，均标注「本报告构造（推测，非事实）」并给出前置条件。
- **本章未对任何车企的密码算法、硬件实现、是否启用 mTLS/DPoP/HSM/SE 做任何断言。** 信源档案 §7.10 第 5 条明载 9 家国内车企在这些方向全部未找到公开一手来源 —— 来源：信源档案 §7.10 —— [A]。
- **本章未编造任何 URL、标准编号、条款号、数字、日期、CVE 编号或事件细节。** 全部事实可对应 `docs/sources/source-dossier.md` 条目；凡 `[C]` 二手者均写"有报道称"；凡 `[A]` 一手者写"文档明载"。
- **本报告不把"未找到公开来源"表述为"该企业不具备该能力"**（审计计划 §3.2.4 中立性红线）。

### 14.10.4 与后续章节的衔接

- **工程实现**（`15-authz-50-engineering.md`）：承接本章 §14.5 矩阵的"建议控制"列，展开为可落地的工程实现。
- **国内车企实践**（`16-authz-60-cn-oem.md`）与**国际车企实践**（`17-authz-70-global-oem.md`）：用本章的攻击树与检测点清单，逐家对照"已公开的控制"与"未取证的检查项"。
- **合规映射**（`18-authz-80-compliance-audit.md`）：承接 §14.6.4（Low 类）与 §14.8 的标准对齐。
- **对比与趋势**（`30-comparison.md` / `31-summary-trends.md`）：承接 §14.6.5（Informational 类）和 §14.10.2 的三类结构性风险。

（本章完）
