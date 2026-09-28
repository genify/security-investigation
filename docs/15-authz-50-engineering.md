# 授权与访问控制 · 工程实现参考架构

> **文件编号**：`15-authz-50-engineering.md`
> **所属工作流**：WF-3（授权与访问控制 · 威胁模型与工程实现）
> **覆盖验收标准**：AC-2（授权章节 ≥300K 字符的组成部分）、AC-7（信源可靠并标注等级）、AC-12（技术深度与可读性并重：架构图 / 表格 / 工程片段）
> **证据底座**：`docs/sources/source-dossier.md`（唯一事实底座，信源档案）
> **编制**：Trail of Bits Security · Reverse Engineering Lead
> **版本**：v1.0 · 生效 2026-09-28
>
> **阅读提示**：本章是「工程实现」章，与前一章 `14-authz-40-threat-model.md`（威胁模型与攻击面）互为镜像——威胁模型回答「攻击者能怎么走」，本章回答「防守方应当怎么搭」。本章事实句沿用全报告统一格式 `—— 来源名称 —— URL —— [等级]`。证据等级口径沿用审计计划 §3.1：`[A]` 一手官方文档、`[B]` 权威第三方、`[C]` 二手、`[未验证]` 站点可达但正文未取到、`[合理推测]`（以「**本报告判断**…（推测，非事实）」显式开头）、`未找到公开来源`。
>
> **本章最重要的写作纪律**：本章是「通用工程参考架构」——它描述的是**一类系统应当如何构造**，而**不是任何一家车企的实际实现**。除标注了 `[A]` 引用的对照基准（如 Tesla Fleet API 的已公开参数）之外，本章所有架构、代码、配置、数值均为**工程示意**。凡是示意代码/伪代码/配置片段/JSON，一律在代码块首行或紧随其后标注「**示意，非真实配置**」。凡无信源档案直接来源、由规范语义推导出的设计判断，一律以「**本报告判断**…（推测，非事实）」开头。

---

## 15.0 本章方法与边界

### 15.0.1 本章是什么、不是什么

本章的定位是「**工程实现参考架构**」（engineering reference architecture）。这一文体的核心不是「某家车企怎么做的」，而是「**如果由本报告的读者去搭建一套车云授权与访问控制平台，应当由哪些组件构成、沿着怎样的决策流水线运转、在哪些点会失败、失败时如何降级、如何度量它是否健康**」。

因此本章刻意采取「**与厂商无关**」（vendor-neutral）的写法。原因有三：

1. **信源档案 §0 已明确记录本次调研的覆盖度偏置**：「证据密度向『文档公开可达』的企业倾斜（Tesla、Mercedes-Benz 证据最厚），对文档未公开的企业（BMW、Rivian、小鹏、极氪、零跑、理想、华为、奇瑞）证据薄弱」，并且强制写作纪律「**『未找到公开来源』= 本次披露缺口，绝不等于能力缺口**」—— 来源：信源档案 §0 —— `docs/sources/source-dossier.md` —— [A]。
2. 若本章把「参考架构」写成「某厂商实现复刻」，就会违反红线③（不得把「未找到公开来源」反向写成「不具备该能力」）——因为一旦把参考架构等同于某家已公开的实现，读者自然会认为「未公开架构的车企 = 架构不成熟」。
3. 工程实现章的价值在于可迁移性：一套组件清单、一套决策流水线、一套失败处置预案，应当能被任意车企按其组织与合规约束裁剪使用。

**本章不是什么**：
- 不是 Tesla 或 Mercedes 的实现说明书（这两家的公开事实仅作为「对照基准」被引用）。
- 不是对任何在售车型的逆向工程结论（审计计划 §1「范围外」明确不做实车攻击与逆向）。
- 不是一份可直接上线的配置文件集合（所有片段均为结构示意，字段名与数值均非真实配置）。

### 15.0.2 本章的事实骨架与推演边界

**事实骨架**来自三块 `[A]` 级一手证据（均可在信源档案中逐条回溯）：

| 事实块 | 内容 | 信源档案位置 |
|---|---|---|
| 授权/身份协议规范 | RFC 6749、6750、7009、7523、7636、7662、8252、8414、8628、8693、8705、9068、9396、9449、9470、9635；OIDC Core 1.0 / Discovery 1.0；OAuth 2.1 草案 | 信源档案 §2.1 |
| 通信与 PKI 规范 | RFC 8446（TLS 1.3）、5280（X.509）、6960（OCSP）、3161（TSP）、8555（ACME）、5480、8017、6090、8998（国密 TLS 套件） | 信源档案 §3 |
| 硬件根信任与密钥管理 | FIPS 140-3、FIPS 186-5、FIPS 197、NIST SP 800-57 Part 1 Rev.5、SP 800-38D、SP 800-90A Rev.1、SP 800-133、GlobalPlatform TEE System Architecture v1.3（GPD_SPE_009） | 信源档案 §4 |
| 中国合规基线 | GB/T 47324-2026（车联网平台网络安全防护要求）、GB/T 47467-2026（车联网安全管理接口规范）、GB/T 45181-2024（车联网网络安全异常行为检测机制） | 信源档案 §1.2 |
| 车企对照基准 | Tesla Fleet API（令牌/虚拟密钥/Fleet Telemetry/限流计费）、Mercedes-Benz Developer Platform（客户端凭证与刷新令牌约束） | 信源档案 §7.1 / §7.2 |

**推演边界**：以下三类内容在本章被显式标记为「**本报告判断**…（推测，非事实）」，不进入事实层：

1. 由 RFC 规范语义推导、但档案无对应企业实现证据的工程建议（例如「授权决策流水线的检查顺序应当如何排列」）。
2. 由两处 `[A]` 事实组合出的、档案未直接陈述的行为推理（例如「由 Tesla 一次性刷新令牌 + 24 小时宽限，推导出并发刷新的工程处置」）。
3. 面向车云场景的分级、配额、阈值、容量建议——本章给出的**具体数值若未标 `[A]`，一律为「设计建议值 / 示意值」**，与「文档明载值」物理分隔，并在表格标题或脚注注明。

### 15.0.3 与相邻章节的分工（避免重复）

| 相邻章节 | 主题 | 本章与其边界 |
|---|---|---|
| `11-authz-10-protocols.md` | 协议族（授权码/PKCE/DPoP/mTLS 等协议流） | 本章不重述协议流，只把协议**当作流水线上的一个检查点** |
| `12-authz-20-tokens-keys.md` | 令牌谱系与密钥治理 | 本章不重述令牌类型对照，只讨论**令牌如何绑定到车辆**与**如何被工程化校验** |
| `13-authz-30-resource-authz.md` | 资源级授权 | 本章只做**资源级策略的落地位置与实现选型**，不展开策略语言本身 |
| `14-authz-40-threat-model.md` | 威胁模型与攻击面 | 本章的每个控制点都应能反向映射到威胁模型中的某条威胁；本章 §15.8 的故障场景是威胁模型的「运维化」版本 |
| `18-authz-80-compliance-audit.md` | 合规映射与审计 | 本章 §15.9 只写「工程需要产出哪些证据」，证据如何映射到条款由 18 章负责 |

### 15.0.4 术语约定

为减少歧义，本章统一使用下表术语。这些术语取自 IETF OAuth 术语体系（RFC 6749 §1.1 定义了资源服务器、授权服务器等核心角色，本章沿用其语义并做车云场景扩展）—— 来源：RFC 6749 —— https://www.rfc-editor.org/rfc/rfc6749.txt —— [A]。

| 术语 | 英文 | 本章含义 |
|---|---|---|
| IdP | Identity Provider | 身份提供方，负责认证（你是谁） |
| AS | Authorization Server | 授权服务器，负责签发令牌（你能做什么） |
| RS | Resource Server | 资源服务器，持有被保护资源（车控服务、数据服务） |
| PDP | Policy Decision Point | 策略决策点，输出「允许/拒绝/有条件」 |
| PEP | Policy Enforcement Point | 策略执行点，执行 PDP 的决策 |
| KMS/HSM | Key Management Service / Hardware Security Module | 密钥管理服务 / 硬件安全模块 |
| T-BOX | Telematics Box | 车联网终端，车辆侧云通信网关 |
| VIN | Vehicle Identification Number | 车辆识别号，车云场景中最稳定的资源标识 |
| 冻结/吊销 | revoke | 令牌或授权被主动失效 |
| 内省 | introspection | 资源服务器向授权服务器实时查询令牌状态（RFC 7662） |

---

## 15.1 车云授权平台的参考架构

### 15.1.1 逻辑组件清单

一套车云授权平台在工程上可拆解为 **10 个逻辑组件**。下表给出每个组件的定位与「一句话职责」。**本报告判断：这 10 个组件是构成完整授权链的最小集合**（推测，非事实）——任何车云平台若要覆盖「认证 → 授权 → 决策 → 执行 → 审计」的闭环，都必然包含这十类职能，即便其中若干类在实现上合并部署。

| # | 组件 | 缩写 | 一句话职责 | 典型技术归属 |
|---|---|---|---|---|
| 1 | 身份提供方 | IdP | 认证主体身份，输出认证断言（OIDC `id_token` / SAML 断言 / FIDO 凭证） | 车企统一身份平台 / 外部 IdP 联邦 |
| 2 | 授权服务器 | AS | 校验授权请求，签发访问令牌与刷新令牌，暴露 `.well-known` 元数据 | OAuth AS（自研或商用） |
| 3 | 资源服务器 | RS | 持有被保护资源（车控 API、遥测数据、账户数据），执行 PEP | 微服务 / API 网关 |
| 4 | 策略决策点 | PDP | 接收「主体×资源×动作×上下文」，输出决策 | 独立服务 / 策略引擎嵌入式 |
| 5 | 策略执行点 | PEP | 在请求路径上拦截、调用 PDP、执行决策、拒绝时返回标准错误 | API 网关 / 服务内中间件 / 车端代理 |
| 6 | 令牌内省服务 | Introspection | 接收不透明令牌，返回其活性与元数据（RFC 7662） | AS 的子端点 |
| 7 | 密钥管理服务 | KMS/HSM | 生成、存储、轮换签名密钥与加密密钥，执行密码运算 | 云 KMS / 网络 HSM / 云托管 HSM |
| 8 | 同意与授权记录库 | Consent Store | 持久化「谁在何时同意了什么 scope / 什么 `authorization_details`」 | 关系库 + 审计流 |
| 9 | 审计日志管道 | Audit Pipeline | 采集、富化、落盘、转发授权决策事件 | 日志总线 + 不可篡改存储 |
| 10 | 车端验签代理 | On-vehicle Verifier | 车辆内对下行载荷做签名验证与新鲜性校验的组件 | T-BOX / 网关 ECU 上的安全组件 |

**补充说明（对照基准）**：Tesla 的公开文档中，其授权服务器元数据发布在 `https://fleet-auth.prd.vn.cloud.tesla.com/oauth2/v3/thirdparty/.well-known/openid-configuration`，且**令牌端点与 API 端点分属不同主机**——`POST https://fleet-auth.prd.vn.cloud.tesla.com/oauth2/v3/token` 被文档说明为「来自应用服务器、适用不同的限流」—— 来源：Tesla Fleet API 开发者文档 —— https://developer.tesla.com/docs/fleet-api/authentication/third-party-tokens —— [A]。**本报告判断**：这种「授权面与数据面分域部署」是组件 2 与组件 3 解耦的公开实例，可作为参考架构中 AS 与 RS 分域的依据（推测，非事实）。

### 15.1.2 ASCII 全景部署图（示意，非真实部署）

下图展示一条从「客户端」到「T-BOX」的完整请求路径，标注了 10 个逻辑组件在链路上的位置。**示意，非真实部署**。

```
                                 车云授权平台 · 全景部署参考（示意，非真实部署）

 ┌────────────────────┐        ┌─────────────────────────────────────────────────────────────────────┐
 │  客户端域           │        │  平台边界（云侧）                                                     │
 │                    │        │                                                                       │
 │ ┌────────────────┐ │        │   ┌─────────────┐   ┌───────────────────────────────────────────────┐  │
 │ │ 车主 App        │ │        │   │ (1) IdP     │   │ (2) 授权服务器 AS                              │  │
 │ │ (RFC 8252 外部  │ │        │   │  身份提供方  │◄──┤  /authorize  /token  /.well-known            │  │
 │ │  用户代理)      │ │        │   └──────┬──────┘   │  (RFC 6749 / 7636 PKCE / 9396 RAR)            │  │
 │ └───────┬────────┘ │        │          │          └───────────────┬───────────────────────────────┘  │
 │         │ ①授权码流 │        │          │ 认证断言                  │ 签发令牌 / 内省 / 吊销          │
 │ ┌───────▼────────┐ │        │          ▼                          ▼                                  │
 │ │ 第三方应用后端  │ │        │   ┌─────────────┐   ┌───────────────────────────────┐   ┌──────────┐  │
 │ │ (Mercedes 口径: │ │        │   │ (8) 同意与  │   │ (7) KMS / HSM                │   │ (6) 令牌 │  │
 │ │  凭证不下发客户端)│ │        │   │ 授权记录库  │   │ 签名密钥轮换 (SP 800-57)      │   │ 内省服务 │  │
 │ └───────┬────────┘ │        │   └─────────────┘   └───────────────────────────────┘   └────┬─────┘  │
 └─────────┼──────────┘        │                                                              │        │
           │ ②Bearer / mTLS(8705) / DPoP(9449)                                              │        │
           ▼                   │   ┌──────────────────────────────────────────────────────────▼─────┐  │
 ┌────────────────────┐        │   │ (3)(5) API 网关 = PEP                                         │  │
 │  互联网 (TLS 1.3)  │───────►│   │  拦截请求 → 组装上下文 → 调 PDP → 执行决策 → 拒绝返回标准错误   │  │
 │  RFC 8446          │        │   └───────────────┬───────────────────────────────────────────────┘  │
 └────────────────────┘        │                   │ 决策请求(subject,resource,action,context)             │
                               │                   ▼                                                       │
                               │   ┌──────────────────────────────┐    ┌────────────────────────────┐     │
                               │   │ (4) 策略决策点 PDP           │    │ (9) 审计日志管道            │     │
                               │   │  策略版本  policies@vX       │───►│  决策事件 / 原因码 / traceID │     │
                               │   └──────────────┬───────────────┘    └────────────────────────────┘     │
                               │                  │ 允许                                                  │
                               │                  ▼                                                      │
                               │   ┌──────────────────────────────┐   ┌───────────────────────────┐      │
                               │   │ 微服务（车控 / 数据 / 账户）  │   │ 速率/配额 计数器 (Redis等) │      │
                               │   └──────────────┬───────────────┘   └───────────────────────────┘      │
                               │                  │ 下行命令（签名载荷）                                    │
                               │                  ▼                                                      │
                               │   ┌──────────────────────────────┐                                      │
                               │   │ 车辆命令通道（长连接 / 推送）  │                                      │
                               │   └──────────────┬───────────────┘                                      │
                               └──────────────────┼──────────────────────────────────────────────────────┘
                                                  │  TLS / 私有协议
                                                  ▼
                               ┌───────────────────────────────────────────┐
                               │  车辆域                                     │
                               │  ┌─────────────────────────────────────┐  │
                               │  │ (10) T-BOX / 车端验签代理            │  │
                               │  │   验签载荷 → 校验新鲜性 → 校验授权     │  │
                               │  │   （Tesla 口径：车辆在执行命令前       │  │
                               │  │     验证载荷签名）                     │  │
                               │  └───────────────┬─────────────────────┘  │
                               │                  ▼                         │
                               │            ┌──────────────┐                │
                               │            │ 网关 ECU /   │                │
                               │            │ 车身控制器    │                │
                               │            └──────────────┘                │
                               └───────────────────────────────────────────┘

 图例：①~⑩ 为请求链路的时序编号；括号内数字对应 §15.1.1 的组件编号。
 说明：本图为结构示意，不代表任何厂商的真实部署拓扑。
```

**读图要点**（**本报告判断**，推测，非事实）：

1. **PEP 位于数据面、PDP 位于控制面**——网关（PEP）在请求热路径上，PDP 可独立伸缩；二者分离使「策略变更」不必重启网关。
2. **审计管道旁挂在 PDP 输出侧**——每一个决策（不论允许还是拒绝）都应产生一条审计事件，这是审计计划 §3.3 中「Low：文档与可观测性缺失、日志不含授权决策依据」该项的工程对策。
3. **车端验签代理是「第二道 PEP」**——云侧的 PEP 通过并不代表车端会执行；车端按本地信任锚独立校验，构成纵深防御。

### 15.1.3 组件「职责 / 失败模式 / 降级策略 / 监控指标」四列表

下表为每个逻辑组件列出四类信息。**「降级策略」一列中，凡涉及具体数值者均为设计建议值（示意），非文档明载值**。此表是本章的工程核心之一，可直接作为设计评审 checklist 使用。

| 组件 | 职责 | 主要失败模式 | 降级策略（建议，示意） | 监控指标（建议，示意） |
|---|---|---|---|---|
| (1) 身份提供方 IdP | 认证主体、输出认证断言、管理凭证（密码/OIDC/FIDO） | 认证服务不可用；凭证风暴；联邦 IdP 证书过期 | 缓存最近成功的会话断言（短 TTL）；只读模式下允许已认证会话续用；对高敏操作强制重认证 | 认证成功率、认证 P99 延迟、失败原因分布、活跃会话数 |
| (2) 授权服务器 AS | 校验授权请求、签发/刷新令牌、暴露元数据、执行内省与吊销 | 签名密钥不可用；令牌签发延迟；.well-known 不可达导致客户端无法发现端点 | 多副本 + 读写分离；签名走 HSM 但缓存「公钥 JWKS」供校验方本地验证；`.well-known` 静态化多节点部署 | 签发 QPS、签发 P99、刷新失败率、JWKS 拉取成功率、吊销处理延迟 |
| (3) 资源服务器 RS | 持有并保护资源、作为 PEP 执行决策 | 后端不可用；下游依赖（PDP/内省）超时；资源不存在误判为拒绝 | 内省结果短缓存 + 失败时对「已签名 JWT」走本地校验；对幂等读操作可返回陈旧数据并标注 | 请求 QPS、4xx/5xx 比例、鉴权失败率、下游超时率 |
| (4) 策略决策点 PDP | 评估策略、输出允许/拒绝/有条件 | 策略加载失败；策略版本漂移；评估超时 | 保留上一已知良好策略版本；评估超时按「默认拒绝」（fail-closed）对高危动作、按「允许但审计」对低危读操作 | PDP 评估 P50/P99、策略版本一致性、缓存命中率、评估错误率 |
| (5) 策略执行点 PEP | 拦截请求、组装上下文、执行决策、拒绝时返回标准错误 | 与 PDP 通信中断；上下文缺失导致误判；错误信息泄露内部细节 | PDP 不可达时按动作分级：车控=拒绝，遥测读=放行+审计；拒绝响应统一 RFC 6750 错误语义不泄露内部 | 决策执行 QPS、PEP-PDP 往返延迟、拒绝率、错误码分布 |
| (6) 令牌内省服务 | 实时校验不透明令牌活性与元数据（RFC 7662） | 成为单点瓶颈；高 QPS 下延迟上升；状态不一致 | 内省结果短 TTL 本地缓存（建议 ≤30 秒，示意值）；对已知 JWT 走本地签名校验免除内省 | 内省 QPS、P99 延迟、缓存命中率、失效令牌判定延迟 |
| (7) KMS/HSM | 生成/存储/轮换密钥、执行密码运算（FIPS 140-3 符合性） | 密钥轮换失败；HSM 连接中断；密钥用途误配 | 双密钥并行期（新旧公钥同时可验）；轮换失败自动回滚；HSM 主备切换 | 密钥年龄、轮换成功率、HSM 调用延迟、签名失败数 |
| (8) 同意与授权记录库 | 记录「谁同意了什么 scope/细节」、支撑撤销与合规举证 | 写入延迟导致同意状态不一致；跨库一致性问题 | 同意写入异步化但以事件溯源保证最终一致；撤销事件优先落盘 | 同意写入延迟、撤销可见延迟、记录完整性校验失败数 |
| (9) 审计日志管道 | 采集/富化/落盘/转发决策事件 | 日志丢失；时钟漂移导致时序错乱；存储写满 | 本地磁盘缓冲 + 背压；NTP 强制同步并记录时钟偏移；只读降级写入 | 日志投递成功率、端到端延迟、盘使用率、时钟偏移量 |
| (10) 车端验签代理 | 车端验证下行载荷签名与新鲜性 | 公钥过期；重放窗口；验签算力不足导致延迟 | 保留已配对公钥的过渡期；维护滑动重放窗口；验签失败即拒绝执行并记录 | 验签失败率、重放拒绝数、验签耗时、本地信任锚版本 |
| (11) 车辆命令通道 | 维护车云长连接、转发下行命令 | 连接风暴；断连堆积；消息乱序 | 指数退避重连；断连缓冲 + 上限截断；命令幂等去重 | 在线车辆数、命令投递成功率、端到端时延、断连缓冲水位 |

> **注（≥11 行已满足）**：本表含 11 行组件。其中组件 (11) 车辆命令通道在 §15.1.1 清单中属于组件 3/5 的运行时延伸，此处单列以覆盖「车云链路」特有的失败面。

**对照基准（`[A]` 事实）**：Tesla Fleet Telemetry 的断连处理为——车辆缓冲 **5000 条消息**（≥2500 秒数据）、重连采用**指数退避且最大重试延迟 30 秒** —— 来源：Tesla Fleet API 开发者文档 —— https://developer.tesla.com/docs/fleet-api/fleet-telemetry —— [A]。**本报告判断**：这一对参数（缓冲上限 + 退避上限）是组件 (11) 降级策略的公开参照；缓冲「有上限」本身就是一种降级策略（被截断的数据不无限占用车辆内存）（推测，非事实）。

---

## 15.2 授权决策流水线（PEP/PDP 拆分）

### 15.2.1 请求抵达后的逐级检查序列

车云授权决策的核心是一段**有序的检查序列**。顺序至关重要：先做廉价且能快速拒绝的检查（签名、受众），再做需要外部调用的检查（内省、策略评估），最后做需要写操作的检查（审计写入）。**本报告判断**：这个「由廉价到昂贵、由本地到远程」的排序原则是性能与安全性的公共最优点（推测，非事实）。

下面是决策流水线的伪代码。**示意，非真实配置**。

```text
# ============================================================
# 车云授权决策流水线（伪代码 · 示意，非真实配置）
# 输入: HTTP 请求 (含 Authorization 头) + 路由元数据
# 输出: 决策 D ∈ {ALLOW, DENY(reason), CHALLENGE}
# 原则: fail-closed（高危动作）、deny-by-default、逐级短路
# ============================================================

function authorize(request, route_meta):
    ctx = new_context()
    ctx.trace_id = gen_trace_id(request.headers["traceparent"])   # 分布式追踪
    ctx.received_at = now_utc()

    # ---------- 步骤 1：客户端认证 ----------
    # 判定「发起方是谁」——可能是公共客户端(手机App)或机密客户端(后端服务)
    client = authenticate_client(request)
    if client is None:
        return DENY("invalid_client")           # RFC 6749 §5.2
    ctx.client_id = client.id
    ctx.client_type = client.type               # public / confidential

    # ---------- 步骤 2：令牌签名 / 发行方 / 受众校验 ----------
    # 若为 JWT（RFC 9068 建议 typ=at+jwt），做本地签名校验
    token = extract_token(request)
    if token is None:
        return CHALLENGE("invalid_token")        # 缺令牌 → 401 + WWW-Authenticate
    if token.is_jwt:
        if not verify_signature(token, jwks_cache):     # 用 IdP/AS 公钥
            return DENY("invalid_signature")
        if token.iss not in TRUSTED_ISSUERS:
            return DENY("invalid_issuer")                # 发行方不在信任列表
        if token.aud not in expected_audiences(route_meta):  # 受众必匹配
            return DENY("invalid_audience")
        if token.exp <= now_utc():
            return DENY("token_expired")
        if token.nbf > now_utc() + CLOCK_SKEW:
            return DENY("token_not_yet_valid")           # 时钟偏移容忍
        ctx.token_fingerprint = sha256(token.raw)[:16]

    # ---------- 步骤 3：令牌活性（内省 或 本地缓存 + 撤销流）----------
    # 不透明令牌 → 必须内省（RFC 7662）；JWT → 优先生效缓存 + 检查撤销黑名单
    if not token.is_jwt:
        intro = introspect(token, timeout=INTROSPECT_TIMEOUT)  # RFC 7662
        if intro is None:
            return DENY("introspection_unavailable")   # fail-closed
        if not intro.active:
            return DENY("token_inactive")
        ctx.subject = intro.sub
        ctx.scopes = intro.scope
        ctx.claims = intro.extra
    else:
        if is_revoked(token.jti, cached_revocation_list):   # 撤销传播
            return DENY("token_revoked")
        ctx.subject = token.sub
        ctx.scopes = token.scope
        ctx.claims = token.authorization_details          # RFC 9396

    # ---------- 步骤 4：主体-资源绑定 ----------
    # 令牌是否被授权「代表这个主体」「作用于这个资源」
    resource = resolve_resource(route_meta, request)      # 通常是 VIN
    binding = check_binding(ctx.subject, ctx.claims, resource)
    if not binding.ok:
        return DENY("subject_resource_binding_mismatch")   # 跨 VIN 越权在此拦截

    # ---------- 步骤 5：动作权限（粗粒度 scope）----------
    action = route_meta.action                             # 如 vehicle_cmds:unlock
    if action.required_scope not in ctx.scopes:
        return DENY("insufficient_scope")                  # RFC 6750 §3.1
    # 命令域级绑定（vehicle_cmds / vehicle_charging_cmds 等）

    # ---------- 步骤 6：资源级策略（细粒度，集中到 PDP）----------
    policy_input = {
        "subject": ctx.subject, "client": ctx.client_id,
        "resource": resource, "action": action,
        "context": {
            "ip": request.ip, "geo": request.geo,
            "time": ctx.received_at, "granular": ctx.claims.granular_access,
            "consent": consent_store.get(ctx.subject, resource, action),
        }
    }
    decision = pdp.evaluate(policy_input, policy_version=CURRENT_POLICY_VERSION)
    if decision.effect == "DENY":
        # 典型：granular_access.hide_private=true 且请求位置字段
        return DENY(decision.reason)                        # 对应 HTTP 403
    if decision.effect == "CHALLENGE":
        return CHALLENGE(decision.acr)                      # RFC 9470 步进认证

    # ---------- 步骤 7：速率 / 配额 ----------
    quota = quota_limiter.check(ctx.client_id, ctx.subject, resource, action)
    if not quota.allowed:
        return DENY("rate_limit_exceeded")                  # HTTP 429
    # 注意：配额按「账号+设备」或「租户」维度，见 §15.6

    # ---------- 步骤 8：审计写入（先写后放行，防止「做了没记」）----------
    audit_event = build_audit_event(
        ts=ctx.received_at, subject=ctx.subject, client=ctx.client_id,
        token_id=ctx.token_fingerprint, resource=resource, action=action,
        decision="ALLOW", reason="policy_allow", policy_version=CURRENT_POLICY_VERSION,
        trace_id=ctx.trace_id, quota_remaining=quota.remaining)
    audit_pipeline.emit(audit_event)                        # 异步但保证至少一次

    return ALLOW
```

**流水线的关键设计取舍**（**本报告判断**，推测，非事实）：

1. **短路方向**：步骤 1–4 任一失败即短路，不再进入昂贵的外部调用。这既省资源，也避免「一个明显无效的令牌被送进 PDP 评估」产生的信息泄漏面。
2. **步骤 3 的双路径**：JWT 走「本地校验 + 撤销黑名单」，不透明令牌走「内省」。这是一条带宽—实时性的经典权衡（详见 §15.2.3）。
3. **步骤 6 的 `granular_access` 体现了「双层控制」**：Tesla 文档明载，带 `granular_access.hide_private=true` 的共享车辆即使被授予 `vehicle_location`，也拿不到任何位置、且无法流式传输位置字段；`hide_private` 共享车辆尝试访问位置字段会被拒绝并返回 **HTTP 403 "location access not granted"** —— 来源：Tesla Fleet API 开发者文档 —— https://developer.tesla.com/docs/fleet-api/authentication/overview —— [A]。这正是「授权被授予（scope 通过）但资源级策略进一步收窄」的公开实例，也是流水线必须区分步骤 5（粗）与步骤 6（细）的理由。
4. **步骤 7 与步骤 8 的位置关系**：配额检查位于策略评估之后，以避免对已被策略拒绝的请求消耗配额；审计写入位于放行之前，以保证「决策必有记录」。

### 15.2.2 策略决策的三种实现选型对比

「PDP 用什么实现」是车云平台最重大的架构决策之一。下表对比三种主流选型。**表内延迟与维护性评分为本报告相对评估（示意），非实测数值**。

| 维度 | 选型 A：硬编码 if-else | 选型 B：声明式策略引擎 | 选型 C：外部授权服务 |
|---|---|---|---|
| 典型形态 | 在 RS 代码里直接写权限判断分支 | 嵌入式策略引擎（策略以声明式语言编写） | 独立部署的授权微服务（如集中式决策中心） |
| 可维护性 | 低：策略散落各处，改动需改代码与发版 | 中—高：策略集中为文件，改动走配置发布 | 高：策略与业务彻底解耦，可独立版本化 |
| 可测试性 | 中：可用单元测试，但覆盖组合爆炸 | 高：策略可被单独喂输入、断言输出 | 高：可作为黑盒服务做契约测试与差分测试 |
| 延迟（相对） | 最低（纯内存判断，纳秒—微秒级） | 低—中（内存中解释策略，微秒—毫秒级） | 中—高（一次网络往返，毫秒级） |
| 审计友好度 | 低：决策「为什么」隐含在代码里，难输出原因码 | 高：策略可返回命中规则与原因 | 高：决策服务本身即审计源，可集中记录 |
| 策略版本治理 | 差：版本即代码版本 | 中：策略文件可版本化 | 好：策略版本独立于服务版本 |
| 车云适用场景 | 极少数永不变化的判断（如「令牌过期则拒」） | 车辆资源级授权、租户隔离等主体规则 | 多租户、多产品线、跨团队统一治理的大型平台 |
| 主要风险 | 策略漂移、难以响应合规变更 | 策略语言能力不足时被迫外溢到代码 | 成为单点与延迟瓶颈；故障时全平台不可决策 |
| 与 PDP/PEP 拆分契合度 | 低（PEP 与 PDP 混为一体） | 高（PEP 内嵌引擎调用） | 最高（PEP 与 PDP 物理分离） |

**本报告判断**：车云平台现实中的最优解往往是**混合式**——「令牌形式校验、主体-资源绑定」用选型 A（因为是稳定且高频的检查），「资源级细粒度授权」用选型 B 或 C（因为策略会随合规与产品持续变化）（推测，非事实）。选择 C 时，必须配套 §15.1.3 中 PDP 的降级策略（缓存策略决策、fail-closed 分级），否则授权服务本身会成为可用性单点。

**与合规的关系**：GB/T 47467-2026《车联网安全管理接口规范》（发布 2026-04-30，实施 2026-11-01）是接口层规范，与授权/访问控制的 API 治理直接相关 —— 来源：信源档案 §1.2 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=AC95A675E7B6E8E822E66B30BE14ED5C —— [A]。**本报告判断**：接口层的规范化意味着「策略决策不应以不可审计的硬编码形式散落在各接口实现中」，因此选型 B/C 在需要接受管理接口合规审计的场景中更易举证（推测，非事实）。本章不对该标准的具体条款作任何断言（未取证）。

### 15.2.3 策略缓存与撤销传播的权衡

这是授权工程中最容易被低估的一处权衡：**为了性能而缓存决策，就会引入撤销的传播延迟**。

#### 两条技术路线

| 路线 | 机制 | 优点 | 代价 |
|---|---|---|---|
| 本地 JWT 自校验 | RS 用 AS 公钥（JWKS）本地验签，不查 AS | 无网络往返、可水平扩展、AS 压力低 | 令牌签发即「有效直到过期」；撤销需额外的黑名单/版本机制 |
| 实时内省 | 每个请求查 AS 内省端点（RFC 7662） | 撤销即时生效（近实时） | 每请求一次往返；内省成为瓶颈与单点 |

OAuth 2.0 Token Introspection（RFC 7662）定义的正是后者：资源服务器通过向授权服务器查询，获得令牌的实时活性与元数据 —— 来源：RFC 7662 —— https://www.rfc-editor.org/rfc/rfc7662.txt —— [A]。而 OAuth 2.0 Token Revocation（RFC 7009）定义了令牌的吊销端点 —— 来源：RFC 7009 —— https://www.rfc-editor.org/rfc/rfc7009.txt —— [A]。**本报告判断**：RFC 7009 只规定「如何发起吊销」，不规定「吊销后多快在所有 RS 生效」——传播延迟是部署问题，不是协议问题（推测，非事实）。

#### 缓存 TTL 与吊销延迟的量化权衡（示意）

设：
- `T_cache` = RS 本地缓存内省结果或决策的 TTL；
- `T_prop` = 撤销事件从 AS 产生到所有 RS 可见的最大延迟；
- `T_revoke_effective` = 撤销生效的总时延。

**最坏情况下 `T_revoke_effective ≈ T_cache + T_prop`**（**本报告判断**，推测，非事实）。下表给出示例取值与后果（**全部为设计建议值，示意**）。

| 方案 | `T_cache`（示意） | `T_prop`（示意） | 最坏撤销生效时延（示意） | 内省 QPS 估算（示意，按 10k 请求/秒） | 适用场景（建议） |
|---|---|---|---|---|---|
| 无缓存（全内省） | 0 秒 | 近 0 | ≈ 秒级 | 10,000 / 秒 | 极高敏动作（车控写）、低频 |
| 短缓存 | 5 秒 | ≤2 秒 | ≈ 7 秒 | ≈ 2,000 / 秒（按 5s 窗口摊薄） | 车控读 + 中敏写 |
| 中缓存 | 30 秒 | ≤5 秒 | ≈ 35 秒 | ≈ 333 / 秒 | 常规数据读 |
| 长缓存 | 300 秒 | ≤5 秒 | ≈ 305 秒 | ≈ 33 / 秒 | 低敏、大批量遥测查询 |
| 纯 JWT 本地校验 | 至令牌过期 | 取决于黑名单轮询 | 可长达令牌剩余寿命 | 0（不查 AS） | 极高频、低敏；须配黑名单 |

> 上表 QPS 估算按「请求量 ÷ 缓存 TTL」简化，未考虑命中率分布，仅用于量级对比。**全部为示意，非真实配置。**

#### 撤销传播的工程手段（**本报告判断**，推测，非事实）

1. **黑名单式（deny-list）**：AS 维护「已撤销 `jti`」集合，RS 定期拉取增量。适合撤销量小的场景；缺点是集合持久化与增量同步复杂。
2. **版本号式（epoch/version）**：为主体或会话维护一个「版本号」，令牌内嵌版本，主体版本递增即令旧令牌失效。适合「用户重置密码即全失效」类需求。Tesla 文档明载刷新失败返回 `401 login_required` 的场景之一是「**用户已重置密码**」—— 来源：Tesla Fleet API 开发者文档 —— https://developer.tesla.com/docs/fleet-api/authentication/third-party-tokens —— [A]。**本报告判断**：这是「按主体一次性失效全部令牌」需求的公开实例，工程上可用版本号或吊销族实现（推测，非事实）。
3. **推送式（pub/sub）**：AS 撤销时主动向 RS 广播撤销事件。传播快，但需可靠的扇出通道与去重。

#### 一致性 vs 可用性（决策建议，示意）

| 动作敏感度 | 建议 `T_cache` | 建议撤销机制 | 一致性取向 |
|---|---|---|---|
| 车控写（解锁/启动/空调） | 0—5 秒 | 推送 + 黑名单双保险 | 偏一致性（宁可多查） |
| 位置/隐私数据读 | ≤30 秒 | 黑名单 | 平衡 |
| 遥测批量读 | ≤300 秒 | 黑名单 | 偏可用性（宁可缓存） |

**本报告判断**：把「动作敏感度」作为缓存 TTL 的分级依据，比「按接口路径」分级更稳定，因为敏感度与合规风险直接相关（推测，非事实）。

---

## 15.3 车辆-令牌绑定的工程实现

### 15.3.1 绑定层级：账号级 / 车辆级 / 命令域级 / 会话级

车云授权区别于普通 Web 授权的本质，在于**令牌必须被绑定到「哪辆车」「哪类命令」**。本章提出四层绑定模型（**本报告判断**，推测，非事实）。四层由外到内逐级收窄。

| 层级 | 绑定对象 | 表达方式 | 存储模型 | 校验位置 | 典型越权风险 |
|---|---|---|---|---|---|
| L1 账号级 | 主体账号（车主/企业） | 令牌 `sub` = 账号 ID | AS 用户库 | 步骤 4 | 一个账号下的多车之间「应隔离未隔离」 |
| L2 车辆级 | 具体车辆 VIN | scope 限定 + 令牌声明 `vin`/资源参数 | 同意记录库（账号→VIN 授权关系） | 步骤 4 + PDP | 跨 VIN 越权：拿 A 车令牌控 B 车 |
| L3 命令域级 | 命令类别（车控/充电/数据/位置） | scope 命名空间（`vehicle_cmds` 等） | 令牌 `scope` 或 `authorization_details` | 步骤 5 | 过度授权：能读数据却也能发命令 |
| L4 会话级 | 单次会话/单条命令 | 令牌 `jti` + 短 TTL + 重放窗口 | RS 缓存 + 车端重放窗口 | 步骤 2/3 + 车端 | 令牌重放：同一条命令被多次执行 |

#### L1 账号级

账号级绑定是最外层。OAuth 的 `sub`（subject）在访问令牌中标识主体 —— 来源：RFC 9068 —— https://www.rfc-editor.org/rfc/rfc9068.txt —— [A]。**本报告判断**：账号级绑定本身不提供车辆隔离，必须叠加 L2（推测，非事实）。

#### L2 车辆级（VIN）

车辆级绑定是车云的「资源级授权」核心。规范上可用两种表达：

- **scope 内嵌资源**：如 Mercedes-Benz 示例 scope 字符串 `scope=openid offline_access mb:vehicle:mbdata:fuelstatus` —— 来源：Mercedes-Benz Developer Platform —— https://developer.mercedes-benz.com/get-started/oauth/authorization-code-flow —— [A]。这是「产品-域-资源」三段式命名空间，资源以类别而非具体 VIN 表达，VIN 另有资源路径或参数承载。
- **`authorization_details` 结构化表达**：RFC 9396 定义 `authorization_details`，用结构化对象替代裸字符串 scope —— 来源：RFC 9396 —— https://www.rfc-editor.org/rfc/rfc9396.txt —— [A]。**本报告判断**：车控场景「资源级授权」的规范依据即在此——可把「哪辆车、哪类命令、什么条件」编码进 `authorization_details` 的元素（推测，非事实）。

**存储模型（示意）**：

```text
# 账号 → 车辆 授权关系（关系模型 · 示意，非真实 schema）
consent(
    subject_id      TEXT,     -- L1 账号
    vin             TEXT,     -- L2 车辆
    client_id       TEXT,     -- 哪个第三方应用
    scopes          TEXT,     -- 授予的 scope 集合
    authz_details   JSON,     -- RFC 9396 结构化细节（可选）
    granular        JSON,     -- 如 {hide_private: true}
    granted_at      TIMESTAMP,
    revoked_at      TIMESTAMP NULL,
    PRIMARY KEY (subject_id, vin, client_id)
)
```

#### L3 命令域级

命令域级绑定把「读取」与「控制」分开。Tesla Fleet API 的 scope 全清单以文档原文名称列出，包含 `user_data`、`vehicle_device_data`、`vehicle_location`、`vehicle_cmds`、`vehicle_charging_cmds`、`vehicle_specs`、`vehicle_pricing_info`、`energy_device_data`、`energy_cmds`、`enterprise_management` 等 —— 来源：Tesla Fleet API 开发者文档 —— https://developer.tesla.com/docs/fleet-api/authentication/overview —— [A]。其中 `vehicle_cmds` 覆盖「添加/移除驾驶员、Live Camera 访问、解锁、唤醒、远程启动、预约软件更新」，`vehicle_charging_cmds` 覆盖「充电历史、计费金额、充电地点、预约/开始/停止充电」—— 同上 —— [A]。**本报告判断**：把「数据读取」与「命令下发」分为不同 scope 域，是命令域级绑定的工程范式（推测，非事实）。

值得注意的是，`vehicle_specs` **仅 Partner Token 可用**，且对**任意车辆**可用、**无需车主授权** —— 来源：同上 —— [A]。**本报告判断**：这属于「不进入逐车主同意模型」的资源访问路径，工程上必须以契约与审计补偿（对应审计计划 §3.3 将该点判为 High 的处理）（推测，非事实）。

#### L4 会话级

会话级绑定面向单条命令或单次会话，主要防重放。手段包括：短 TTL 的访问令牌、令牌唯一标识 `jti` 的去重、以及服务端滑动重放窗口。**本报告判断**：会话级绑定是唯一能约束「已授权但被重放的命令」的层级（推测，非事实）。

### 15.3.2 请求体/令牌声明的示意 JSON（三份）

以下三份 JSON 均为**示意，非真实令牌**。字段命名遵循 RFC 9068（访问令牌 JWT 声明）、RFC 9396（`authorization_details`）、RFC 8705（证书绑定 `cnf`）的语义。

#### 示意一：粗粒度 scope 令牌

```json
{
  "typ": "at+jwt",
  "alg": "ES256",
  "kid": "as-signing-key-2026-09",
  "iss": "https://as.example-oem.invalid/oauth2",
  "sub": "owner:acct_9f2b",
  "aud": "https://fleet-api.example-oem.invalid",
  "exp": 1767225600,
  "iat": 1767222000,
  "jti": "6f1c2d3e-4a5b-6c7d-8e9f-0123456789ab",
  "scope": "openid vehicle_device_data vehicle_cmds",
  "client_id": "third_party_app_42"
}
```

> 说明：这是最简形态——scope 是裸字符串集合，资源（VIN）不体现在令牌中，而在请求路径/参数中携带。**示意，非真实令牌。**
> 对照：RFC 9068 要求校验 `iss`/`aud`/`exp`，推荐 `typ: at+jwt` —— 来源：RFC 9068 —— https://www.rfc-editor.org/rfc/rfc9068.txt —— [A]。

#### 示意二：RFC 9396 `authorization_details` 令牌

```json
{
  "typ": "at+jwt",
  "alg": "ES256",
  "kid": "as-signing-key-2026-09",
  "iss": "https://as.example-oem.invalid/oauth2",
  "sub": "owner:acct_9f2b",
  "aud": "https://fleet-api.example-oem.invalid",
  "exp": 1767225600,
  "iat": 1767222000,
  "jti": "7a2b3c4d-5e6f-7081-92a3-b4c5d6e7f809",
  "authorization_details": [
    {
      "type": "vehicle_command",
      "identifier": "VIN_DEMO_0000000000",
      "locations": ["https://fleet-api.example-oem.invalid/api/1/vehicles/*/command/*"],
      "actions": ["unlock", "climate_on"],
      "constraints": {
        "not_before": "08:00",
        "not_after": "20:00",
        "max_uses": 5
      }
    },
    {
      "type": "vehicle_data",
      "identifier": "VIN_DEMO_0000000000",
      "privileges": ["battery_level", "odometer"]
    }
  ]
}
```

> 说明：`authorization_details` 以数组承载「结构化权限对象」，每项含 `type`、资源标识与可执行动作，并可带约束。这是把 L2（车辆）+ L3（命令域）编码进单枚令牌的方式。**示意，非真实令牌。**
> 对照：RFC 9396 定义 `authorization_details` 用结构化权限对象替代裸字符串 scope —— 来源：RFC 9396 —— https://www.rfc-editor.org/rfc/rfc9396.txt —— [A]。

#### 示意三：证书绑定令牌（含 `cnf`）

```json
{
  "typ": "at+jwt",
  "alg": "ES256",
  "kid": "as-signing-key-2026-09",
  "iss": "https://as.example-oem.invalid/oauth2",
  "sub": "enterprise:fleet_op_7",
  "aud": "https://fleet-api.example-oem.invalid",
  "exp": 1767225600,
  "iat": 1767222000,
  "jti": "8b3c4d5e-6f70-8192-a3b4-c5d6e7f8091a",
  "scope": "vehicle_cmds vehicle_charging_cmds",
  "cnf": {
    "x5t#S256": "b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3"
  }
}
```

> 说明：`cnf.x5t#S256` 是客户端证书的 SHA-256 指纹（thumbprint）。资源服务器在 TLS 层取客户端证书，计算指纹并与 `cnf` 比对——不匹配即拒。这样即使令牌被复制，攻击者没有对应私钥也无法使用。**示意，非真实令牌。**
> 对照：RFC 8705 定义 mTLS 客户端认证与证书绑定访问令牌（持有人约束令牌不可被复制盗用） —— 来源：RFC 8705 —— https://www.rfc-editor.org/rfc/rfc8705.txt —— [A]。DPoP 则是等价思路的「无证书」变体，用 `DPoP` 头 + JWK 指纹绑定 —— 来源：RFC 9449 —— https://www.rfc-editor.org/rfc/rfc9449.txt —— [A]。

#### 三份 JSON 的对照

| 维度 | 示意一（裸 scope） | 示意二（`authorization_details`） | 示意三（`cnf` 证书绑定） |
|---|---|---|---|
| 资源表达 | 无（在请求路径） | 令牌内 `identifier` | 无（依赖客户端证书） |
| 命令域表达 | `scope` 字符串 | `type` + `actions` | `scope` 字符串 |
| 抗令牌复制 | 无（Bearer 默认可复制） | 无 | 强（需私钥） |
| 粒度 | 粗 | 细（含约束） | 取决于 scope |
| 规范依据 | RFC 6749 / 6750 / 9068 | RFC 9396 | RFC 8705 / 9449 |
| 适用 | 简单数据读 | 车控细粒度授权 | 企业服务账号 / 高风险命令 |

**本报告判断**：现实中三者常叠加——`cnf` 抗复制 + `authorization_details` 提粒度 + `sub`/`vin` 定归属，可同时满足「不可复制」「细粒度」「可归因」三目标（推测，非事实）。

### 15.3.3 车端二次校验

云侧 PEP 放行**不等于**车辆会执行。Tesla 文档明载虚拟密钥机制：虚拟密钥 = 公私钥对；公钥须由**可信用户**添加到车辆，私钥留在应用服务器；**车辆在执行命令前或接受 Fleet Telemetry 配置前验证载荷签名** —— 来源：Tesla Fleet API 虚拟密钥开发者指南 —— https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide —— [A]。文档进一步称虚拟密钥「**甚至能阻止 Tesla 自己的后端访问这些能力**」—— 同上 —— [A]。

这构成了「车端二次校验」的公开范式。其验签顺序可工程化为如下伪代码。**示意，非真实实现**。

```text
# ============================================================
# 车端验签代理 · 下行载荷校验顺序（伪代码 · 示意，非真实实现）
# 触发: T-BOX 收到一条下行命令载荷
# 原则: 默认拒绝；任一校验失败即丢弃并记录；不得「校验失败仍执行」
# ============================================================

function on_vehicle_verify(payload, transport_ctx):
    # ---------- 0. 传输层信任 ----------
    if not transport_ctx.tls_authenticated:
        return REJECT("transport_not_authenticated")   # TLS 1.3 (RFC 8446)

    # ---------- 1. 载荷结构校验（先廉价检查）----------
    if not payload.has_fields(["vin", "command", "issued_at", "nonce", "signature"]):
        return REJECT("malformed_payload")

    # ---------- 2. 归属校验：载荷是否针对本车 ----------
    if payload.vin != local_vin:
        return REJECT("vin_mismatch")                  # 防跨车投递

    # ---------- 3. 签名校验：用本地信任锚 ----------
    # 信任锚 = 车主/可信用户在车辆 Locks 界面添加的虚拟密钥公钥
    pubkey = local_key_store.get(payload.signer_fingerprint)
    if pubkey is None:
        return REJECT("unknown_signer")                # 未配对密钥一律拒绝
    if not verify_ecdsa_p256(pubkey, payload.body, payload.signature):
        return REJECT("bad_signature")                 # 签名不匹配
    # 说明: Tesla 文档明载密钥生成用 prime256v1(P-256)、车辆仅支持 prime256v1
    #       —— developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide [A]

    # ---------- 4. 新鲜性 / 重放校验 ----------
    now = vehicle_clock.now_utc()
    if payload.issued_at > now + MAX_CLOCK_SKEW:
        return REJECT("issued_in_future")              # 时钟偏移容忍
    if now - payload.issued_at > REPLAY_WINDOW:
        return REJECT("expired_payload")               # 超出重放窗口
    if nonce_cache.contains(payload.nonce):            # 滑动窗口去重
        return REJECT("replay_detected")
    nonce_cache.insert(payload.nonce, ttl=REPLAY_WINDOW)

    # ---------- 5. 授权状态校验（本地缓存的授权视图）----------
    if not local_authz_cache.allows(payload.signer_fingerprint, payload.command):
        return REJECT("authorization_not_present")     # 授权已被收回 / 未授予

    # ---------- 6. 命令合法性 ----------
    if payload.command not in ALLOWED_COMMANDS:
        return REJECT("command_not_allowed")

    # ---------- 7. 审计与执行 ----------
    audit_log.append({ts: now, vin: local_vin, signer: payload.signer_fingerprint,
                      command: payload.command, nonce: payload.nonce, result: "ALLOW"})
    return EXECUTE(payload.command)
```

**车端二次校验的工程要点**（**本报告判断**，推测，非事实）：

1. **信任锚的删除即吊销**：Tesla 文档明载「吊销由用户在车辆 Locks 界面删除密钥完成」—— 来源：https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide —— [A]。这意味着车端「本地密钥存储」本身就是授权状态的一部分——删除密钥即切断该密钥签发的一切后续载荷。
2. **密钥数量上限作为影响范围控制**：Tesla 文档明载 B2B 项目车辆可自动添加虚拟密钥的条件之一是「**已配对密钥少于 20 把**」—— 同上 —— [A]。**本报告判断**：这是一个「以数量上限约束单车辆影响面」的工程手段（推测，非事实）。
3. **公钥必须长期可用**：Tesla 文档明载公钥必须托管于 `https://developer-domain.com/.well-known/appspecific/com.tesla.3p.public-key.pem` 且**必须长期可用**，私钥 `private-key.pem` 绝不可托管于域名 —— 同上 —— [A]。**本报告判断**：这要求「公钥发布」成为一项带长期可用性 SLA 的运维职责，而非一次性动作（推测，非事实）。

---

## 15.4 多租户与 B/C 端隔离（车队/企业 vs 车主）

车云平台同时服务两类主体：**C 端车主**（个人，其车辆是其私产）与 **B 端车队/企业**（企业拥有或管理一批车辆，代表企业行事）。这两类主体的授权模型、数据可见性、审计要求都不同，必须做租户隔离。Tesla Fleet API 中出现 `enterprise_management` scope —— 来源：Tesla Fleet API 开发者文档 —— https://developer.tesla.com/docs/fleet-api/authentication/overview —— [A] —— 并区分「partner token / third-party token / third-party-for-business token」等令牌 —— 来源：同上 —— [A]，**本报告判断**：这类令牌分类反映了 B 端（企业管理）与 C 端（车主代表）在授权模型上的分野（推测，非事实）。

### 15.4.1 租户模型与数据隔离策略

| 隔离策略 | 机制 | 隔离强度 | 成本 | 密钥管理 | 适用 |
|---|---|---|---|---|---|
| 行级隔离 | 所有租户共用库/表，用 `tenant_id` 列区分，查询强制带租户谓词 | 中（依赖代码正确性） | 低 | 共享密钥 + 租户标签 | 大量小租户、统一演进 |
| 库级/实例级隔离 | 每租户独立库或独立实例 | 高（物理分隔） | 高 | 每租户独立密钥 | 少量大租户、强合规 |
| 密钥隔离 | 隔离不体现在数据行，而体现为「每租户独立签名/加密密钥」 | 高（密码学隔离） | 中 | 每租户独立 KMS 密钥 | 跨租户数据共享仍敏感的场景 |
| 混合（推荐示意） | 行级隔离 + 每租户密钥 + 租户级策略作用域 | 高 | 中 | 每租户密钥 | 车云常见配置（本报告建议） |

**本报告判断**：车云场景中，单纯的行级隔离不足以防护「跨租户越权」——因为一旦某条查询漏了租户谓词，数据即跨租户泄漏；而「行级 + 每租户密钥 + 策略强制作用域」三重叠加后，即使逻辑隔离被绕过，攻击者也无法解密他租户的数据（推测，非事实）。密钥隔离的规范依据来自 NIST SP 800-57 Part 1 Rev.5 的密钥生命周期管理建议 —— 来源：https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final —— [A]。

**租户模型（示意，非真实 schema）**：

```text
# 租户模型（关系模型 · 示意，非真实 schema）
tenant(
    tenant_id     TEXT PRIMARY KEY,
    tenant_type   TEXT,      -- 'individual' | 'fleet' | 'enterprise'
    kms_key_id    TEXT,      -- 该租户的独立密钥标识
    policy_scope  TEXT,      -- 策略作用域（限制策略评估范围）
    created_at    TIMESTAMP
)
# 每个请求的鉴权上下文必须携带 tenant_id，且由令牌声明而非请求参数推导，
# 以防「客户端自报租户」造成的租户伪造。   ← 本报告判断（推测，非事实）
```

### 15.4.2 跨租户越权防护的控制清单

以下 10 条控制构成「跨租户越权防护」的检查清单（**本报告判断**，推测，非事实；条目为主要控制点，可据组织裁剪）。

| # | 控制 | 说明 | 失败时的后果 |
|---|---|---|---|
| 1 | 租户由令牌声明推导，不由请求参数自报 | `tenant_id` 来自令牌 claim，任何请求体/查询参数中的租户字段一律忽略 | 客户端可自报他租户 → 越权 |
| 2 | 全查询强制带租户谓词 | 数据访问层强制注入 `tenant_id = :ctx_tenant`，禁止裸查询 | 漏谓词即跨租户泄漏 |
| 3 | 每租户独立密钥 | KMS 按租户派生密钥，跨租户密文不可解 | 逻辑绕过仍可解密 |
| 4 | 策略作用域限定 | PDP 评估时以租户作用域加载策略，禁止跨租户规则命中 | 策略误命中他租户 |
| 5 | 资源归属双校验 | 不仅校验「资源属于租户」，还校验「主体有权对该资源执行该动作」 | 同租户内横向越权 |
| 6 | IDOR 防护 | 所有资源标识（VIN、订单号）做归属校验，禁止直接按 ID 取 | 枚举 ID 遍历他人资源 |
| 7 | 跨租户操作显式授权 | 如企业代管车主车辆，需车主显式授权记录（同意库） | 企业越权控制车主车辆 |
| 8 | 审计含租户维度 | 每条授权事件记录 `tenant_id`，可做租户维度回溯 | 事后无法定位越权范围 |
| 9 | 负向测试常态化 | 自动化测试持续验证「A 租户令牌访问 B 租户资源必被拒」 | 回归引入越权无人察觉 |
| 10 | 令牌绑定租户不可转移 | 令牌或绑定 `tenant_id`，跨租户复用被拒 | 令牌泄漏即跨租户 |

**B/C 端分野的工程注记**（**本报告判断**，推测，非事实）：

- **C 端**：授权粒度以「车主 × 车辆 × 第三方应用」三元组为主，撤销入口在车主侧（Tesla 提供车主撤销入口 `https://auth.tesla.com/user/revoke/consent?...` —— 来源：https://developer.tesla.com/docs/fleet-api/authentication/third-party-tokens —— [A]）。
- **B 端**：授权粒度以「企业 × 车队 × 角色 × 车辆集合」为主，需支持批量授权与角色继承；但**企业代管车主车辆仍须车主同意记录**（否则构成对 C 端权利的覆盖）。
- **B/C 冲突**：当同一车辆同时被车主（C）与企业（B）主张控制权时，需明确的仲裁策略——例如「车主撤销优先，撤销即令企业侧授权失效」。Tesla 文档明载「若所需 scope 被撤销导致配置失效，配置会被**从车辆移除**」—— 来源：https://developer.tesla.com/docs/fleet-api/fleet-telemetry —— [A]。**本报告判断**：这体现了「撤销即联动回收配置」的联动控制思想（推测，非事实）。

---

## 15.5 运维与可观测性

### 15.5.1 授权决策的审计事件模型

审计计划 §3.3 将「文档与可观测性缺失、日志不含授权决策依据」判为 Low 级发现，并要求归入合规映射章节 —— 来源：审计计划 §3.3 —— `docs/00-engagement-plan.md` —— [A]。其工程对策是**结构化审计事件模型**：每条授权决策都必须产出一条字段化的、可机读的事件。下表为字段模型（**本报告判断**，字段设计为工程建议，非任何标准条款）。

| 字段 | 类型 | 含义 | 是否必填 | 敏感度处理 |
|---|---|---|---|---|
| `event_id` | UUID | 事件唯一标识 | 是 | — |
| `ts_utc` | RFC 3339 | 事件时间（UTC，NTP 同步） | 是 | 记录时钟偏移量 |
| `event_type` | enum | `authorization_decision` / `token_issued` / `token_revoked` | 是 | — |
| `subject` | string | 主体标识（账号，可哈希） | 是 | 按需假名化 |
| `client_id` | string | 发起方客户端 | 是 | — |
| `token_id` | string | 令牌指纹（`jti` 或其哈希，不记原文） | 是 | 不记明文令牌 |
| `token_type` | enum | bearer / mtls_bound / dpop_bound | 是 | — |
| `resource` | string | 被访问资源（VIN 等，可部分掩码） | 是 | VIN 可掩码 |
| `action` | string | 请求动作 | 是 | — |
| `decision` | enum | `ALLOW` / `DENY` / `CHALLENGE` | 是 | — |
| `reason_code` | string | 拒绝/挑战原因码（如 `insufficient_scope`） | 是 | — |
| `policy_version` | string | 生效的策略版本 | 是 | 支撑举证 |
| `trace_id` | string | 分布式追踪 ID | 是 | — |
| `quota_remaining` | int | 决策时剩余配额 | 否 | — |
| `consent_ref` | string | 关联的同意记录 ID | 否 | — |
| `decided_ms` | int | 决策耗时（毫秒） | 否 | 性能 |

**关键纪律**（**本报告判断**，推测，非事实）：

1. **`reason_code` 必填**——「拒绝但不知为何拒」的日志对合规举证无价值；这正对应审计计划 §3.3 的 Low 级判据。
2. **`policy_version` 必填**——能回答「当时生效的是哪版策略」，是差分测试（§15.7.2）与事后复盘的前提。
3. **不记明文令牌**——审计日志仅记令牌指纹，防止日志成为「令牌仓库」这一新攻击面。
4. **时钟统一**——审计事件时间必须 NTP 同步并记录偏移，否则跨服务时序不可信。

**事件示例（示意，非真实事件）**：

```json
{
  "event_id": "e1f2a3b4-c5d6-7890-abcd-ef1234567890",
  "ts_utc": "2026-09-28T23:59:12.345Z",
  "event_type": "authorization_decision",
  "subject": "owner:acct_9f2b",
  "client_id": "third_party_app_42",
  "token_id": "fp:sha256:6f1c2d3e…",
  "token_type": "mtls_bound",
  "resource": "VIN_DEMO_0000000000",
  "action": "vehicle_cmds:unlock",
  "decision": "DENY",
  "reason_code": "policy_denied_location_not_granted",
  "policy_version": "authz-policies@v37",
  "trace_id": "00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01",
  "quota_remaining": 27,
  "decided_ms": 4
}
```

> 说明：仅用于演示字段结构。`reason_code` 的取值（如 `policy_denied_location_not_granted`）为示意原因码，非任何产品的真实错误码。**示意，非真实事件。**

### 15.5.2 关键指标体系与告警阈值设计

下表为车云授权平台的核心指标体系。**阈值列为设计建议值（示意），非文档明载值**；实际取值应基于自身基线与容量测试确定。

| 指标 | 定义 | 单位 | 建议告警阈值（示意） | 可能根因 |
|---|---|---|---|---|
| 授权拒绝率 | DENY 数 ÷ 决策总数 | % | 突增 > 基线 3 倍（15 分钟窗口） | 策略误配、密钥轮换失败、攻击探测 |
| 令牌刷新失败率 | 刷新失败 ÷ 刷新请求 | % | > 2%（5 分钟窗口） | 刷新令牌一次性问题、竞态、时钟 |
| 内省延迟 P99 | 内省端点 99 分位延迟 | ms | > 200 ms | 内省瓶颈、AS 压力过高 |
| 撤销传播延迟 | 撤销产生到全 RS 可见 | s | > 60 s | 黑名单/推送通道滞后 |
| 单车主异常命令率 | 单车主单位时间命令数与基线偏离 | 倍 | > 基线 5 倍 | 令牌泄漏、账号被盗、脚本化攻击 |
| 决策 P99 延迟 | PEP 端到端决策耗时 | ms | > 50 ms（热路径） | PDP 慢、下游超时 |
| 签名验证失败率 | 验签失败 ÷ 验签总数 | % | > 0.5% | 密钥轮换不同步、伪造尝试 |
| 配额耗尽账号数 | 触发限流的账号数 | 个 | 突增 > 基线 3 倍 | 滥用、配额误配、攻击 |
| 在线车辆占比 | 在线 ÷ 应在线 | % | 骤降 > 10% | 车云通道故障 |
| 同意写入延迟 | 同意事件落盘延迟 | ms | > 500 ms | 同意库压力、一致性冲突 |

**「单车主异常命令率」的工程价值**（**本报告判断**，推测，非事实）：这是把安全信号（令牌泄漏/账号被盗）转化为可告警指标的典型手段。它与 §15.5.3 的异常行为检测自然衔接——GB/T 45181-2024《车联网网络安全异常行为检测机制》正是这一方向的国标 —— 来源：信源档案 §1.2 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=29740120554AA4DCB87A8FEAE106BA43 —— [A]。

### 15.5.3 异常行为检测的工程接入

GB/T 45181-2024《车联网网络安全异常行为检测机制》与 GB/T 47324-2026《车联网平台网络安全防护要求》为异常行为检测与平台防护提供了国标定位 —— 来源：信源档案 §1.2 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=29740120554AA4DCB87A8FEAE106BA43 、https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=90F36FFBED2E85627B648B837A522527 —— [A]。**本章不对这两个标准的任何条款号或具体技术要求作断言**（未取证，信源档案仅记录了标准编号、名称与发布/实施日期）。

**本报告判断**：工程上把异常行为检测接入授权平台的可行位点如下（推测，非事实）：

| 位点 | 数据来源 | 可检出行为 | 处置动作（示意） |
|---|---|---|---|
| 授权请求侧 | 授权/决策事件流 | 单主体短时高频授权；异常地域；异常客户端 | 步进认证（RFC 9470）/ 限流 / 拒绝 |
| 令牌使用侧 | 令牌使用审计 | 同令牌跨地域并发；同一 `jti` 多 IP 使用 | 令牌吊销 + 主体全域失效 |
| 命令侧 | 车控命令流 | 单车主异常命令率飙升；非常规时段的敏感命令 | 二次确认 / 暂缓执行 / 人工复核 |
| 车辆侧 | 车端验签日志 | 大量验签失败；未知签名者；重放尝试 | 拒绝执行 + 回传告警 |
| 配额侧 | 配额计数器 | 单账号配额异常消耗曲线 | 配额分池 / 临时冻结 |

**接入原则**（**本报告判断**，推测，非事实）：

1. **检测位点应覆盖「认证后」而非仅「认证前」**——取证显示，攻击者多数在拿到合法令牌后才有实质行为。
2. **检测输出必须可行动**（detect → decide → act）——只报警不处置的检测在工程上不产生安全收益。
3. **检测规则本身要版本化与审计**——与策略版本一致地纳入审计事件模型（`policy_version` 字段族）。
4. **检测与授权决策解耦**——检测系统异常不应导致授权决策不可用（避免检测系统成为新的可用性单点）。

---

## 15.6 容量、成本与限流工程

### 15.6.1 已取证限流/计费参数作为对照基准

Tesla Fleet API 的公开限流与计费参数是本章可用的 `[A]` 对照基准 —— 来源：Tesla Fleet API Billing and Limits —— https://developer.tesla.com/docs/fleet-api/billing-and-limits —— [A]。逐条列出如下（**均为文档明载值**）：

| 类别 | 参数 | 文档明载值 |
|---|---|---|
| 实时数据 | 请求频率上限 | 60 次/分（按账号按设备计） |
| 唤醒 | 请求频率上限 | 3 次/分 |
| 设备命令 | 请求频率上限 | 30 次/分 |
| 账号维度 | 同账号多应用 | **共享**限额 |
| 计费周期 | 周期 | 按用量，月度周期（每月 1 日起算） |
| 计费上限 | 每账号默认上限 | 0 |
| 告警点 | 用量百分比 | 达 80% 与 100% 时发邮件 |
| 超限后果 | 处置 | **暂停 API 使用并移除 Fleet Telemetry 推流配置（且不恢复）** |
| 折扣 | 个人开发者/小应用 | 每月 $10 折扣 |
| 计费规则 | 响应码 | **<500 全部计费，≥500 不计费** |
| 计费精度 | 舍入 | 费用四舍五入到 $0.01 |
| 推流上限 | 单车第三方应用数 | 最多同时向 **5 个**第三方应用推流 |
| 密钥上限 | 单车辆已配对虚拟密钥 | 少于 **20** 把（B2B 自动添加条件） |
| 遥测样例 | 示例负载 | 约 15 信号/分钟 ≈ $0.0001/分钟 ≈ $0.006/行驶小时 |
| 断连缓冲 | 车辆缓冲上限 | 5000 条消息（≥2500 秒数据） |
| 重连退避 | 最大重试延迟 | 30 秒（指数退避，最大 30 秒） |
| 事件窗口 | 遥测收集窗口 | 500 ms |

> 数据来源：Tesla Fleet API Billing and Limits 页与 Fleet Telemetry 页 —— https://developer.tesla.com/docs/fleet-api/billing-and-limits 、https://developer.tesla.com/docs/fleet-api/fleet-telemetry —— [A]。上表为文档明载值，非本报告推算。

### 15.6.2 容量规划表（示意）

下表以「某中型车云平台」为假想规模做容量规划示例。**规模假设与容量数值均为示意，非真实配置**；读者应以自身规模替换。

| 维度 | 假设（示意） | 计算 | 结论（示意） |
|---|---|---|---|
| 联网车辆数 | 1,000,000 | — | — |
| 在线比例 | 5% 同时在线 | 1,000,000 × 5% | 50,000 在线连接 |
| 命令频率 | 每车 30 次/分上限（对照 Tesla 参数） | 50,000 × 30 | 峰值 1,500,000 命令/分（≈25k QPS） |
| 实时数据 | 每车 60 次/分上限 | 50,000 × 60 | 3,000,000 请求/分（≈50k QPS） |
| 决策耗时预算 | 端到端 | — | 热路径 ≤ 50 ms |
| 内省容量 | 若 10% 请求走内省 | 80k QPS × 10% | 8,000 内省/秒 |
| 审计事件量 | 每决策 1 事件 | 80k QPS | 80,000 事件/秒 |
| 审计存储 | 单事件 ≈ 1 KB，保留 180 天 | 80k × 86400 × 180 × 1KB | ≈ 1.24 PB（示意） |

**容量规划要点**（**本报告判断**，推测，非事实）：

1. **决策吞吐必须与命令吞吐解耦**——命令通道的长连接数与授权决策的 QPS 是两个独立的容量维度。
2. **审计存储往往是被低估的成本项**——上表显示审计量级可达 PB 级；需冷热分层与采样策略（但**授权拒绝事件不建议采样**，因其是安全信号）。
3. **内省是成本放大器**——若每个请求都内省，QPS 直接翻倍于决策量；因此 §15.2.3 的缓存策略在容量层面是刚需。

### 15.6.3 「配额耗尽作为可用性攻击面」的工程缓解

**威胁**（**本报告判断**，推测，非事实）：配额机制本意是控制成本，但它同时是一个**可用性攻击面**——攻击者若能用少量请求把目标账号的配额「烧光」，就能让合法用户失效。Tesla 文档明载超限后果是「**暂停 API 使用并移除 Fleet Telemetry 推流配置（且不恢复）**」—— 来源：https://developer.tesla.com/docs/fleet-api/billing-and-limits —— [A]。**本报告判断**：这是配额耗尽的极端后果（不仅是暂停，且推流配置不恢复），需要专门的工程缓解（推测，非事实）。

三类缓解手段（**本报告判断**，推测，非事实）：

| 手段 | 机制 | 缓解的攻击 | 代价 |
|---|---|---|---|
| 服务端削峰 | 对入站请求做令牌桶/漏桶，超限请求快速拒绝而非排队 | 突发洪峰烧配额 | 合法突发也可能被拒 |
| 客户端退避 | 客户端遇 429 后指数退避重试（对齐 Tesla 重连退避「最大 30 秒」范式） | 重试风暴加重配额消耗 | 需客户端配合；退避参数需统一下发 |
| 配额分池 | 把总配额按「应用/功能/时段」拆分为独立子池 | 单应用耗尽拖垮全账号 | 池划分与再平衡复杂 |
| 配额与身份分层 | 不同信任级别（正式合作方 vs 新注册应用）给不同配额 | 恶意应用烧光共享配额 | 需信任分级治理 |
| 异常配额消耗告警 | 监测消耗曲线，突增即告警并可临时冻结 | 隐蔽的慢速耗尽 | 误报需调参 |

**关键设计原则**（**本报告判断**，推测，非事实）：**配额耗尽不得触发「不可恢复」的副作用**。Tesla 文档明载「移除 Fleet Telemetry 推流配置（且不恢复）」是供给侧的选择；从可用性工程角度，更稳妥的做法是「暂停但可恢复」，把「永久移除配置」限制在明确的合规/安全场景。此处的判断仅为工程建议，**不构成对 Tesla 处置策略的评价**。

---

## 15.7 测试与验证工程

### 15.7.1 授权逻辑的单元/属性测试清单

授权逻辑是「默认拒绝」型系统的典型代表——它的正确性很难靠人工审查，必须靠**属性测试**（property-based testing）：不是逐个用例断言，而是断言「对所有输入都满足某性质」。下表列出 12 条必测属性（**本报告判断**，推测，非事实；条目为工程建议）。

| # | 测试/属性 | 断言（性质） | 案例来源 |
|---|---|---|---|
| 1 | 跨 VIN 必拒 | ∀ 令牌绑定 VIN_A、请求资源 VIN_B（A≠B）：决策=DENY | L2 绑定 |
| 2 | scope 少写必拒 | ∀ 请求动作动作要求 scope S，令牌不含 S → 必拒 | RFC 6750 §3.1 |
| 3 | 过度授权检测 | 令牌 scope ⊋ 请求动作用域 → 标记为过度授权风险 | 最小权限原则 |
| 4 | 令牌重放 | 同一 `jti` + 同一载荷在重放窗口内第二次请求 → 必拒（会话级绑定） | L4 绑定 |
| 5 | 并发刷新 | 同一刷新令牌并发两次刷新 → 至多一个成功（一次性） | Tesla 一次性刷新[对照] |
| 6 | 时钟偏移 | `iat` 略早/略晚（在偏移容忍内）→ 允许；超出容忍 → 拒绝 | RFC 9068 `exp/nbf` |
| 7 | `aud` 不匹配 | 令牌 `aud` ≠ 目标资源服务器 → 必拒 | RFC 9068 |
| 8 | `iss` 不在信任列表 | 令牌由非信任发行方签发 → 必拒 | RFC 9068 |
| 9 | 签名伪造 | 篡改载荷或签名 → 验签必失败 | RFC 8705/9449 |
| 10 | 撤销后必拒 | 令牌被撤销（RFC 7009）后，在传播延迟内最终必拒 | RFC 7009 |
| 11 | `cnf` 指纹不匹配 | 证书指纹 ≠ 令牌 `cnf.x5t#S256` → 必拒 | RFC 8705 |
| 12 | `authorization_details` 约束 | 超出 `constraints`（时间窗/次数）→ 必拒 | RFC 9396 |

**属性测试实现建议（示意，非真实实现）**：

```python
# ============================================================
# 授权属性测试骨架（示意，非真实实现）
# 依赖: hypothesis 风格属性测试 + 被测 authorize() 决策函数
# ============================================================
from hypothesis import given, strategies as st

@given(
    token_vin = st.sampled_from(["VIN_A", "VIN_B", "VIN_C"]),
    req_vin   = st.sampled_from(["VIN_A", "VIN_B", "VIN_C"]),
)
def test_cross_vin_always_denied(token_vin, req_vin):
    token = make_token(vin=token_vin)
    req   = make_request(resource=req_vin, action="unlock")
    d = authorize(req, jwt=token)
    if token_vin != req_vin:
        assert d == DENY("subject_resource_binding_mismatch")
    # 性质: 跨 VIN 恒拒，与其它字段无关

@given(scopes = st.sets(st.sampled_from(
        ["vehicle_device_data","vehicle_cmds","vehicle_location"])))
def test_missing_scope_always_denied(scopes):
    token = make_token(scopes=scopes)
    req   = make_request(action="unlock")   # 要求 vehicle_cmds
    d = authorize(req, jwt=token)
    assert (d == ALLOW) == ("vehicle_cmds" in scopes)   # 充要条件
```

> **示意，非真实实现。** `make_token` / `make_request` / `authorize` / `DENY` / `ALLOW` 均为占位符。

### 15.7.2 集成与回归

| 类别 | 内容 | 目的 |
|---|---|---|
| 沙箱环境搭建 | 独立 IdP/AS/RS/KMS 沙箱；合成车辆（虚拟 VIN）；可注入故障的内省/推送通道 | 在无真实车辆风险下验证授权链 |
| 差分测试 | 同一策略引擎两版本（A/B）对同一输入集合回放，逐条比对决策差异 | 发现策略变更的意外中断（regression） |
| 模糊测试 | 模糊字段：`scope` 字符串、`authorization_details` 结构、`aud`/`iss`、`cnf` 指纹、VIN 格式、`jti` | 发现解析器崩溃/绕过 |
| 契约测试 | PEP↔PDP、RS↔内省端点的接口契约 | 防跨服务接口漂移 |
| 故障注入 | 内省超时、PDP 不可用、KMS 轮换中断、推送通道断连 | 验证降级策略真的有效 |
| 回放测试 | 用真实审计事件回放，验证新策略不误拒历史合法请求 | 上线前防止误伤 |
| 权限矩阵测试 | 生成「主体×资源×动作」全矩阵，断言与期望策略一致 | 系统化覆盖越权面 |

**差分测试的工程价值**（**本报告判断**，推测，非事实）：策略引擎换代或策略大改时，**差分测试是唯一能在上线前发现「意外放行」的手段**——因为「意外拒绝」会立即被用户投诉发现，而「意外放行」往往数月无人察觉。差分测试的输入应包含历史审计事件（§15.5.1）。

**模糊测试字段建议**（**本报告判断**，推测，非事实）：

| 字段 | 模糊策略 | 目标 |
|---|---|---|
| `scope` | 注入空格/逗号/超长/大小写变体/命名空间边界 | 发现 scope 解析绕过 |
| `authorization_details` | 深层嵌套、超长数组、类型混淆 | 发现结构解析绕过 |
| `aud`/`iss` | 相似域名、尾随点、大小写、Unicode 同形字 | 发现受众/发行方匹配绕过 |
| `cnf.x5t#S256` | 长度错误、非十六进制、大小写 | 发现指纹比对绕过 |
| VIN | 长度/字符集/大小写/相似 VIN | 发现跨 VIN 校验绕过 |
| `jti` | 重复、空、超长 | 发现去重失效 |

### 15.7.3 上线前安全检查表（≥15 项，可勾选）

以下 18 项为上线前检查清单（**本报告判断**，工程建议，非标准条款）。

- [ ] 1. 所有授权路径默认拒绝（deny-by-default），未显式允许的一律拒绝
- [ ] 2. 令牌签名校验使用受管密钥（KMS/HSM），公钥通过 JWKS 发布且可轮换
- [ ] 3. `iss` 白名单、`aud` 严格匹配、`exp`/`nbf` 校验均已实现并有测试
- [ ] 4. 所有车控/位置资源访问均做主体-资源绑定校验（跨 VIN 必拒有测试）
- [ ] 5. 资源级策略集中到 PDP，且有策略版本与原因码输出
- [ ] 6. 撤销传播路径已实现并测得最坏传播延迟（对照 §15.5.2 阈值）
- [ ] 7. 密钥轮换演练通过（双密钥并行期、回滚、批量 401 预案）
- [ ] 8. 内省/PDP 不可用时的降级策略已按动作分级实现（fail-closed 分级）
- [ ] 9. 审计事件包含全部必填字段（含 `reason_code`、`policy_version`、`trace_id`）
- [ ] 10. 审计日志不含明文令牌/密钥/客户端凭证
- [ ] 11. 配额/限流已按账号（或租户）维度实现，且不触发不可恢复副作用
- [ ] 12. 客户端凭证不下发到客户端（对齐 Mercedes 文档要求）
- [ ] 13. 多租户隔离三重叠加（行级 + 每租户密钥 + 策略作用域）已验证
- [ ] 14. 跨租户越权负向测试常态化并通过
- [ ] 15. 车端二次校验（验签 + 新鲜性 + 授权状态）已验证，且失败一律不执行
- [ ] 16. 差分测试对策略新版本全绿，无意外放行
- [ ] 17. 异常行为检测接入授权事件流，且检测输出可行动
- [ ] 18. 待补证清单已复核，无「未找到公开来源」被反向写成「不具备能力」的表述

> 第 12 项依据：Mercedes-Benz 开发者文档明载应用「**不得**向客户端暴露任何客户端凭证（client id、client secret、访问令牌）」—— 来源：Mercedes-Benz Developer Platform —— https://developer.mercedes-benz.com/get-started/oauth/authorization-code-flow —— [A]。**本报告判断**：这条要求本身是通用工程原则，不限于任何一家（推测，非事实）。

---

## 15.8 四类典型故障与处置

本节给出四类在车云授权平台中「高概率、高影响」的典型故障。每个故障按「症状 / 根因 / 影响面 / 处置步骤 / 预防」五段式展开。**本节场景为工程推演（示意），不代表任何已发生的真实事故**。

### 15.8.1 故障一：密钥轮换失败导致批量 401

| 维度 | 内容 |
|---|---|
| **症状** | 大面积 401/`invalid_token`；日志显示验签失败集中于某一批资源服务器；JWKS 端点新旧公钥不一致 |
| **根因** | 签名密钥轮换时，RS 的 JWKS 缓存过期时间过长（或推送失败），AS 已切到新私钥签发，RS 仍只认旧公钥；或轮换未被「双密钥并行期」覆盖 |
| **影响面** | 所有依赖该 AS 签发令牌的 RS 全量拒绝；车控、数据、账户全链路不可用 |
| **处置步骤** | ①立即回滚到旧签名密钥（若 AS 仍持有）；②或立即刷新全 RS 的 JWKS 缓存；③冻结轮换流程；④确认「新公钥已全量可见」后再切私钥；⑤审计受影响时段的拒绝事件 |
| **预防** | 轮换必须走「先发布新公钥 → 观察 ≥ 最长缓存 TTL → 再切私钥」的两阶段；JWKS 缓存 TTL 应短于轮换观察窗（示意：JWKS 缓存建议 ≤5 分钟）；轮换前后自动化校验「AS 签名可用新公钥验证」 |

**规范依据**：RFC 8555 定义 ACME 自动化证书签发/轮换，是「短周期证书的工程前提」—— 来源：RFC 8555 —— https://www.rfc-editor.org/rfc/rfc8555.txt —— [A]。NIST SP 800-57 Part 1 Rev.5 提供密钥生命周期管理建议（含密码周期）—— 来源：https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final —— [A]。**本报告判断**：密钥轮换的自动化程度决定了此类故障的概率——手工轮换的出错率远高于自动化（推测，非事实）。

### 15.8.2 故障二：授权服务器不可用导致车控不可用

| 维度 | 内容 |
|---|---|
| **症状** | 车控命令全面失败；客户端无法刷新令牌；`.well-known` 端点不可达 |
| **根因** | AS 单点故障；或 AS 依赖的 KMS/HSM 不可用导致无法签发；或 AS 过载（令牌风暴） |
| **影响面** | 所有需要新令牌/刷新的操作用户无法获得授权；已持有效令牌且 RS 走本地 JWT 校验的读操作可能仍可用 |
| **处置步骤** | ①切 AS 多副本/灾备；②检查 KMS 连通性；③若短期无法恢复，启用「已签发令牌延长使用」的应急模式（须有明确时限与审批）；④对高危动作仍强制走 AS，不接受降级；⑤恢复后收紧 |
| **预防** | AS 多活部署；令牌签发与校验分离（校验方依赖公钥而非 AS 在线）；对高频低敏读操作允许本地 JWT 校验（§15.2.3）；容量预置与过载保护 |

**关键权衡**（**本报告判断**，推测，非事实）：AS 不可用时「延长已签发令牌使用」是一种**可用性与安全性的显式权衡**——它让车控可用，但延长了「已撤销主体」的窗口。因此应急模式必须有**时限、审批、且对高危动作不生效**。

### 15.8.3 故障三：刷新令牌并发竞态导致会话丢失

| 维度 | 内容 |
|---|---|
| **症状** | 用户频繁被迫重新登录；刷新返回 `invalid_grant`；日志显示同一刷新令牌被使用两次 |
| **根因** | 刷新令牌**一次性使用**（Tesla 文档明载 single use only；Mercedes 文档明载刷新令牌一次性使用），但客户端多进程/多标签页并发刷新，第二个请求使用了已被「用掉」的旧刷新令牌 |
| **影响面** | 单用户会话丢失（可恢复但体验差）；严重时若客户端逻辑不当，可能进入刷新死循环 |
| **处置步骤** | ①客户端序列化刷新（全局单飞/互斥）；②利用「宽限期」机制（Tesla 文档明载最近一次使用的刷新令牌在 **24 小时内仍有效**）覆盖持久化失败场景；③服务端对同一刷新令牌的并发请求做「幂等返回同一新令牌对」或「明确区分重放与竞态」 |
| **预防** | 客户端实现「单飞刷新」（single-flight）；服务端宽限期窗口；对并发刷新做去重与可观测 |

**对照依据**：Tesla 文档明载刷新令牌**一次性使用（single use only）且在 3 个月后过期**，且**宽限期：最近一次使用的刷新令牌在 24 小时内仍有效**（用于覆盖「应用未能持久化轮换后令牌」的失败场景）；刷新失败返回 `401 login_required` 的场景包括刷新令牌过期/被挤出、或用户已重置密码 —— 来源：Tesla Fleet API 开发者文档 —— https://developer.tesla.com/docs/fleet-api/authentication/third-party-tokens —— [A]。Mercedes 文档明载刷新令牌一次性使用，授权服务器返回**新的访问令牌与新的刷新令牌**，已用/无效刷新令牌报错 "The given refresh token is not valid or was already used" —— 来源：Mercedes-Benz Developer Platform —— https://developer.mercedes-benz.com/get-started/oauth/authorization-code-flow —— [A]。**本报告判断**：两家的公开口径共同证明「一次性刷新 + 竞态」是行业共性工程问题，宽限期是 Tesla 的公开对策（推测，非事实）。

### 15.8.4 故障四：撤销传播延迟导致已离职人员仍可控制车辆

| 维度 | 内容 |
|---|---|
| **症状** | 离职员工/被移除合作方的令牌在撤销后仍可用；短期出现「本应无权者发起车控」；撤销事件与 RS 拒绝日志之间存在时间差 |
| **根因** | 撤销事件传播延迟（§15.2.3）；RS 缓存 TTL 过长；或 RS 走本地 JWT 校验而无撤销黑名单 |
| **影响面** | 高：企业人员离职后仍可能控制车队车辆，属审计计划 §3.3 中「授权链可被绕过」类风险的运维版本 |
| **处置步骤** | ①立即执行「主体全域失效」（版本号式/吊销族），而非仅吊销单个令牌；②推送撤销事件到全部 RS；③对涉事主体的近期命令做告警回溯；④缩短该类主体的缓存 TTL |
| **预防** | 对 B 端主体采用「版本号 + 短缓存」；离职/移除流程与撤销流程强绑定（HR/IdP 事件 → 授权撤销）；定期演练撤销传播并度量延迟 |

**关键纪律**（**本报告判断**，推测，非事实）：**人员/合作关系变更必须触发授权撤销，且撤销必须可验证**。工程上应把「IdP 的账号停用事件」作为撤销的**触发源**，而非依赖人工操作——因为人工撤销在离职高峰期必然遗漏。

---

## 15.9 与合规审计的接口

本章不展开合规条款映射（由 `18-authz-80-compliance-audit.md` 负责），只回答一个工程问题：**为了支撑审计，工程侧必须产出哪些证据**。以下证据清单为工程建议（**本报告判断**，推测，非事实），供 18 章映射使用。

| 证据类别 | 工程产出 | 来源组件 | 支撑的审计问题 |
|---|---|---|---|
| 决策日志 | 结构化授权事件（§15.5.1 全字段） | 审计管道 (9) | 「当时为何允许/拒绝」 |
| 策略版本 | 策略文件的版本号与变更历史 | PDP (4) | 「当时生效的是哪版策略」 |
| 变更记录 | 策略/密钥/角色的变更审批记录 | 变更管理系统 | 「谁在何时改了什么」 |
| 密钥轮换记录 | 轮换时间、新旧密钥指纹、影响范围 | KMS/HSM (7) | 「密钥生命周期是否受控」 |
| 同意记录 | 车主/企业同意的 scope 与细节、撤销记录 | 同意库 (8) | 「是否取得合法授权」 |
| 撤销记录 | 撤销事件、传播时间戳、生效确认 | AS (2) + 管道 (9) | 「撤销是否及时生效」 |
| 配额/限流记录 | 配额消耗与限流触发记录 | 配额计数器 | 「是否滥用/是否被滥用」 |
| 异常检测记录 | 检测规则版本、命中记录、处置动作 | 检测系统 | 「异常行为是否被检出与处置」 |
| 权限矩阵快照 | 定期导出的「主体×资源×动作」授权矩阵 | 同意库 + PDP | 「权限是否最小化」 |
| 测试报告 | 属性测试、差分测试、故障注入结果 | CI 系统 | 「控制是否被验证有效」 |

**与国标的接口注记**（**本报告判断**，推测，非事实）：GB/T 47324-2026《车联网平台网络安全防护要求》面向平台侧防护、GB/T 47467-2026《车联网安全管理接口规范》面向管理接口 —— 来源：信源档案 §1.2 —— [A]。**本章不对这两个标准的条款内容作任何断言**（未取证）；仅指出：**管理接口类规范通常会要求「管理操作可审计、可追溯、可授权」**，因此上表证据清单中「变更记录」「权限矩阵快照」「策略版本」三类尤为重要（推测，非事实）。

**证据保留建议**（**本报告判断**，推测，非事实）：授权决策日志建议保留周期覆盖「合规要求的追诉期」；密钥轮换记录建议保留「密钥全生命周期」；同意与撤销记录建议保留至关系终止后再加合规缓冲期。具体周期须由法务与合规确定，本章不给出数值结论。

---

## 15.10 本章待补证清单

本章作为「通用工程参考架构」，其补证需求集中在「把示意参数替换为真实工程参数」与「确认公开事实的完整性」。以下清单记录本章的待补证项。**所有「未找到公开来源」项均为本次披露缺口，不等同于能力缺失。**

| # | 待补证项 | 现状 | 补证方式 |
|---|---|---|---|
| 1 | Tesla 访问令牌 TTL | 信源档案仅证实刷新令牌 3 个月 + 24 小时宽限；访问令牌 TTL 未获证实 | 实机走一遍 token 响应读取 `expires_in` |
| 2 | 各车企的内省/撤销传播实测延迟 | 无公开来源 | 沙箱申请 + 实测 |
| 3 | 各车企配额/限流的具体维度 | 仅 Tesla 公开（账号+设备） | 沙箱申请;平台文档 |
| 4 | 各车企多租户隔离的具体实现 | 无公开来源 | 采购安全白皮书 / RFI |
| 5 | 各车企审计事件的字段模型 | 无公开来源（Tesla 无公开字段表） | RFI / 合规审计报告 |
| 6 | 本章所有容量/阈值建议值的生产校验 | 全部为示意值 | 结合自身基线与压测确定 |
| 7 | 国标 GB/T 47324 / 47467 / 45181 的条款级要求 | 信源档案仅有编号、名称、日期 | 通过标准购买渠道获取正文 |
| 8 | 车端二次校验的行业普遍性 | 仅 Tesla 虚拟密钥机制有公开描述 | 逐家 RFI；不得以 Tesla 类推他厂 |
| 9 | R155/R156 对授权的具体要求 | 信源档案标注 [未验证]（unece.org 被拦截） | 恢复检索额度或官方 PDF 直链 |
| 10 | 国内 9 家车企的 mTLS/国密/HSM 实现 | 信源档案 §7.10 第 5 条：全部未取得官方一手来源 | 向车企发起 RFI / 查专利与招标 |

**补证纪律复述**：本章任何「某厂商未公开 X」的表述，**一律不得**被解读或改写为「某厂商不具备 X」。信源档案 §0 已明确：「未找到公开来源 = 本次披露缺口，绝不等于能力缺口，不得反向推断为『该企业没有该能力』」—— 来源：信源档案 §0 —— `docs/sources/source-dossier.md` —— [A]。

---

## 15.11 本章小结

本章给出了一套**与厂商无关**的车云授权与访问控制工程参考架构。核心结论与主张归纳如下。

**1. 架构层面**：车云授权平台可拆为 10 个逻辑组件（IdP / AS / RS / PDP / PEP / 内省 / KMS-HSM / 同意库 / 审计管道 / 车端验签代理），其关键架构特征是 **PDP 与 PEP 分离**（控制面与数据面解耦）与 **车端验签代理作为第二道 PEP**（纵深防御）。两者的落点均可在公开证据中找到对照：Tesla Fleet API 的 AS/RS 分域部署、以及虚拟密钥「车辆在执行命令前验证载荷签名」的公开描述 —— 来源：https://developer.tesla.com/docs/fleet-api/authentication/third-party-tokens 、https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide —— [A]。

**2. 决策层面**：授权决策应实现为**有序的逐级检查流水线**（客户端认证 → 令牌校验 → 活性 → 主体-资源绑定 → 动作权限 → 资源级策略 → 速率配额 → 审计），遵循「由廉价到昂贵、由本地到远程、默认拒绝、fail-closed 分级」原则。**本报告判断**：这是性能与安全性的公共最优点（推测，非事实）。

**3. 绑定层面**：车云令牌必须实现**四层绑定**（账号级 / 车辆级 / 命令域级 / 会话级），其中车辆级（VIN）绑定是资源级授权的核心，命令域级绑定是「读取与控制」分野的核心，会话级绑定是防重放的核心。规范工具为 RFC 9396（`authorization_details`）、RFC 8705（`cnf` 证书绑定）、RFC 9449（DPoP）—— 来源：信源档案 §2.1 —— [A]。

**4. 隔离层面**：B/C 端共平台时，多租户隔离应三重叠加（行级 + 每租户密钥 + 策略作用域），且租户必须由令牌声明推导而非请求参数自报。跨租户越权防护需 10 条控制（§15.4.2）。

**5. 运维层面**：授权可观测性的基石是**结构化审计事件模型**（含 `reason_code`、`policy_version`、`trace_id`），直接对应审计计划 §3.3 将「日志不含授权决策依据」判为 Low 级发现的工程对策。异常行为检测接入应覆盖「认证后」位点（对齐 GB/T 45181-2024 方向）。

**6. 容量层面**：Tesla 公开的限流/计费参数（实时数据 60 次/分、唤醒 3 次/分、设备命令 30 次/分、同账号共享、超限暂停并移除推流配置不恢复；单车 5 个第三方应用；虚拟密钥 <20 把）可作为容量与配额设计的对照基准 —— 来源：https://developer.tesla.com/docs/fleet-api/billing-and-limits 、https://developer.tesla.com/docs/fleet-api/fleet-telemetry —— [A]。工程上须把「配额耗尽」显式当作可用性攻击面，以服务端削峰、客户端退避、配额分池缓解，并避免不可恢复副作用。

**7. 验证层面**：授权逻辑的正确性只能靠**属性测试**（12 条必测属性）与**差分测试**（策略版本 A/B 回放）保证；上线前应通过 18 项安全检查表。

**8. 故障处置**：四类高频故障（密钥轮换失败批量 401、AS 不可用车控不可用、刷新令牌并发竞态、撤销传播延迟）各有明确的症状-根因-处置-预防路径；其中撤销售后必须可验证，且人员/关系变更必须以 IdP 事件为触发源。

**最后重申本章边界**：本章是**通用工程参考**，其中的架构、代码、配置、数值凡未标 `[A]` 者为工程示意，不代表任何车企的真实实现；凡涉及具体厂商者均标注证据等级或写为「未找到公开来源 / 待补证」，且**绝不反向推断为能力缺失**。本章的每一处推演均以「**本报告判断**…（推测，非事实）」显式标注，供后续章节（尤其 `18-authz-80-compliance-audit.md` 与 `19-authz-90-reference-tables.md`）引用时保持证据分层。

---

> **本章字符与覆盖度自检**：本章覆盖信源档案 §1.2（GB/T 47324-2026、GB/T 47467-2026、GB/T 45181-2024）、§2.1（RFC 6749/6750/7009/7523/7636/7662/8252/8414/8628/8693/8705/9068/9396/9449/9470）、§3（RFC 8446/5280/6960/3161/8555/5480/8017/6090/8998）、§4（FIPS 140-3、FIPS 186-5、NIST SP 800-57）、§7.1（Tesla Fleet Telemetry 推流参数、虚拟密钥托管、限流与计费、断连缓冲 5000 条 / 退避 30 秒 / 500ms 窗口）、§7.2（Mercedes 客户端凭证不得下发、刷新令牌一次性）。全部代码/配置/JSON 均标注「示意，非真实配置」。待补证项见 §15.10。
