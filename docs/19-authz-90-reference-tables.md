# 授权与访问控制 · 参考表与索引

> 所属工作流：WF-6（合规映射、审计与参考表）
> 覆盖验收标准：**AC-2（授权章节 ≥300K 字符的组成部分）、AC-7（信源可靠并标注等级）、AC-8（区分公开信息与合理推测）**；本章另为 AC-1 / AC-3 / AC-4 / AC-5 / AC-6 / AC-11 / AC-12 提供可核对索引。
> 唯一事实底座：`docs/sources/source-dossier.md`（下称「信源档案」）
> 采集日期：2026-09-28｜本章为**汇总层**，不新增任何一手取证。

---

## 19.1 说明与使用方式

### 19.1.1 本章的定位：工具箱，而非再论证

本章是全报告第 3 部分（授权与访问控制）的**工具箱层**。它不重新论证任何议题，只做一件事：把散落在第 2 章（`02-general-layered-security.md`）与第 3 部分各章（`11`–`17`）中的**已取证事实**，按「可比较参数 / 端点 / 规范 / 术语 / 证据台账 / 缺口台账」六种维度重新结构化，使读者可以**不翻正文而直接查表**。

因此本章的第一优先级是**准确性、可核对性、无重复论述**，而不是新增分析。凡一张表能表达的内容，本章不再写论述段落；凡一张表已覆盖的判断，本章不再重复理由。任何读者若在某行看到非表格内容，那一定是为了交代该表的**边界或口径**，而不是新的论证。

### 19.1.2 四条写作纪律（本章自我约束）

1. **可回溯**：本章任何条目必须能在信源档案 §1–§7 找到对应条目，或在被索引章节（02/11/12/13/14/16/17）正文中找到对应小节。新增而未取证的内容一律不写。
2. **不新增**：本章**不引入任何新的 URL、标准号、日期、数字**。表内出现的每一个 URL 均逐字复制自信源档案。
3. **不确定即标注**：凡本次未取证的方向，一律写「未找到公开来源」并保留在 19.11 缺口台账，**绝不填平**。
4. **中立**：「未找到公开来源」= **本次披露缺口**，绝不等于「该主体不具备该能力」（对齐 AC-11 与信源档案 §0 的「覆盖度偏置」声明）。

### 19.1.3 每张表的来源章节与更新规则

| 表号 | 表名 | 主数据来源 | 被索引章节 | 更新触发条件 |
|---|---|---|---|---|
| 19.2 | 规范索引表 | 信源档案 §1–§6 | 02、11、12、14 | 信源档案追加新规范条目时同步追加 |
| 19.3 | OAuth/身份协议速查表 | 信源档案 §2.1 | 11、12 | RFC/草案版本变化时更新「版本」列 |
| 19.4 | 车企与平台端点/凭证清单 | 信源档案 §7 | 13、16、17 | 某车企新披露开发者门户时追加行 |
| 19.5 | 令牌与密钥参数对照表 | 信源档案 §7.1、§7.2 | 12、13 | 实测补齐 Tesla `expires_in` 时更新 |
| 19.6 | Scope 命名与粒度对照表 | 信源档案 §7.1、§7.2 + 规范 | 13、17 | 新增车企 scope 清单时追加 |
| 19.7 | 国家标准与实施时间线表 | 信源档案 §1.1–§1.3 | 16 | 国标新发布/状态变化时更新 |
| 19.8 | 硬件与密码基元对照表 | 信源档案 §3–§5 | 02、12 | 新增密码规范条目时追加 |
| 19.9 | 威胁-控制交叉索引 | 章节 14 的 §14.2/§14.5/§14.6 | 14、12 | 章节 14 威胁编号变化时同步 |
| 19.10 | 证据等级台账 | 信源档案全篇 | 全部 | 每次补证后重算 |
| 19.11 | 缺口台账汇总 | 信源档案 §8 + 各章待补证清单 | 全部 | 每次补证后删除已闭合项 |
| 19.12 | 术语与缩写表 | 信源档案 + 各章 | 全部 | 新术语引入时追加 |
| 19.13 | 关键结论索引 | 各章小结段 | 全部 | 结论修订时同步 |
| 19.14 | 报告章节地图 | 审计计划 §2、§6.1 | 全部 | 新增文件时更新状态列 |

### 19.1.4 证据等级记号（沿用审计计划 §3.1，全报告统一口径）

| 记号 | 定义 | 本章用法 |
|---|---|---|
| `[A]` | 一手：标准正文（openstd.samr.gov.cn / RFC Editor / 官方规范库）、OEM 官方开发者文档、官方白皮书、官方漏洞政策 | 表内直接引用 |
| `[B]` | 权威第三方：学术论文、检测认证机构、权威媒体、官方 SDK 仓库、行业联盟规范页 | 表内标注 |
| `[C]` | 二手：自媒体、博客、论坛、聚合站 | 表内标注，不得单独立论 |
| `[未验证]` | 站点可达性已确认但正文未取到 | 表内标注，不得作事实断言 |
| `[合理推测]` | 由已知架构/规范推导 | 仅出现在 19.13 的「是否含推测成分」列 |
| `未找到公开来源` | 已检索指定对象无果 | 一律保留在 19.11 |

---

## 19.2 规范索引表

本表逐条覆盖信源档案 §1.1（强制性国标）、§1.2（推荐性国标）、§1.3（行政法规）、§1.4（国际标准与法规）、§2.1（OAuth 身份协议）、§3（通信与 PKI）、§4（硬件根信任）、§5（数字钥匙与近场）、§6（OTA 与供应链）的**全部条目**。「相关度」列的判定口径：直接规定授权/身份/访问控制机制者为「高」；为授权机制提供密码或通信底座者为「中」；与授权仅间接相关者为「低」。「引用章节」列指向本报告已完稿章节；「规划中」表示该章节写作时尚未完稿。

| 编号 | 名称 | 类型 | 版本或年份 | 相关度 | 引用章节 | 证据等级 |
|---|---|---|---|---|---|---|
| GB 44495-2024 | 汽车整车信息安全技术要求 | GB（强制） | 2024 | 高 | 16、02 | [A] |
| GB 44496-2024 | 汽车软件升级通用技术要求 | GB（强制） | 2024 | 中 | 16、02 | [A] |
| GB/T 40855-2021 | 电动汽车远程服务与管理系统信息安全技术要求及试验方法 | GB/T | 2021 | 高 | 16 | [A] |
| GB/T 40856-2021 | 车载信息交互系统信息安全技术要求及试验方法 | GB/T | 2021 | 中 | 16 | [A] |
| GB/T 40857-2021 | 汽车网关信息安全技术要求及试验方法 | GB/T | 2021 | 中 | 16、14（CP-7） | [A] |
| GB/T 38628-2020 | 信息安全技术 汽车电子系统网络安全指南 | GB/T | 2020 | 中 | 16、02 | [A] |
| GB/T 41871-2022 | 信息安全技术 汽车数据处理安全要求 | GB/T | 2022 | 高 | 16 | [A] |
| GB/T 44464-2024 | 汽车数据通用要求 | GB/T | 2024 | 中 | 16 | [A] |
| GB/T 45112-2024 | 基于 LTE 的车联网无线通信技术 安全证书管理系统技术要求 | GB/T | 2024 | 高 | 16、11 | [A] |
| GB/T 45181-2024 | 车联网网络安全异常行为检测机制 | GB/T | 2024 | 中 | 16、02 | [A] |
| GB/T 47324-2026 | 车联网平台网络安全防护要求 | GB/T | 2026 | 高 | 16 | [A] |
| GB/T 47325-2026 | 车联网在线升级安全技术要求与测试方法 | GB/T | 2026 | 中 | 16 | [A] |
| GB/T 47467-2026 | 车联网安全管理接口规范 | GB/T | 2026 | 高 | 16 | [A] |
| GB/T 44402.1-2024 | 卡及身份识别安全设备 数字钥匙系统 第 1 部分：参考架构 | GB/T | 2024 | 高 | 16、11、02 | [A] |
| GB/T 32918.1~.5-2016/2017 | SM2 椭圆曲线公钥密码算法（总则/数字签名/密钥交换/公钥加密/参数定义） | GB/T | 2016/2017 | 高 | 02、12 | [A] |
| GB/T 32905-2016 | SM3 密码杂凑算法 | GB/T | 2016 | 中 | 02、12 | [A] |
| GB/T 32907-2016 | SM4 分组密码算法 | GB/T | 2016 | 中 | 02、12 | [A] |
| GB/T 35275-2017 | SM2 密码算法加密签名消息语法规范 | GB/T | 2017 | 高 | 02、12 | [A] |
| GB/T 35276-2017 | SM2 密码算法使用规范 | GB/T | 2017 | 高 | 02、12 | [A] |
| 汽车数据安全管理若干规定（试行）（网信办等五部门令第 7 号） | 重要数据目录、境内存储、年度报送、出境评估 | 行政法规/部门规章 | 2021 | 高 | 16 | [A] |
| 汽车数据安全管理若干规定 答记者问 | 官方解读 | 行政法规配套 | 2021 | 低 | 16 | [A] |
| ISO/SAE 21434:2021 | Road vehicles — Cybersecurity engineering | ISO/SAE | 2021 | 高 | 02（规划中） | [未验证] |
| SAE J3061 | Cybersecurity Guidebook for Cyber-Physical Vehicle Systems | SAE（21434 前身） | 2016 | 中 | 02 | [B] |
| ISO 24089:2023 | Road vehicles — Software update engineering | ISO | 2023 | 中 | 02（规划中） | [未验证] |
| UN Regulation No.155 | CSMS 网络安全管理体系 | UN 法规 | — | 高 | 17（规划中） | [未验证] |
| UN Regulation No.156 | SUMS 软件更新管理体系 | UN 法规 | — | 中 | 17（规划中） | [未验证] |
| GDPR Regulation (EU) 2016/679 | 通用数据保护条例 | 欧盟法规 | 2016 | 高 | 17（规划中） | [C] |
| Data Act Regulation (EU) 2023/2854 | 车辆数据可携权/互联产品数据访问权 | 欧盟法规 | 2023 | 高 | 17（规划中） | [C] |
| RFC 6749 | The OAuth 2.0 Authorization Framework | RFC | 2012 | 高 | 11、12 | [A] |
| RFC 6750 | OAuth 2.0 Bearer Token Usage | RFC | 2012 | 高 | 11、12 | [A] |
| RFC 8252 | OAuth 2.0 for Native Apps | RFC | 2017 | 高 | 11、14 | [A] |
| RFC 7636 | PKCE（Proof Key for Code Exchange） | RFC | 2015 | 高 | 11、12、14 | [A] |
| RFC 9068 | JWT Profile for OAuth 2.0 Access Tokens | RFC | 2021 | 高 | 12、14 | [A] |
| RFC 8705 | OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens | RFC | 2020 | 高 | 11、12、14 | [A] |
| RFC 9449 | OAuth 2.0 Demonstrating Proof of Possession (DPoP) | RFC | 2023 | 高 | 11、12、14 | [A] |
| RFC 9396 | OAuth 2.0 Rich Authorization Requests | RFC | 2023 | 高 | 11、13、14 | [A] |
| RFC 8693 | OAuth 2.0 Token Exchange | RFC | 2020 | 高 | 11、12、14 | [A] |
| RFC 7523 | JWT Profile for OAuth 2.0 Client Authentication and Authorization Grants | RFC | 2015 | 高 | 11、12、14 | [A] |
| RFC 7662 | OAuth 2.0 Token Introspection | RFC | 2015 | 高 | 12、14 | [A] |
| RFC 8414 | OAuth 2.0 Authorization Server Metadata | RFC | 2018 | 高 | 11、12、17 | [A] |
| RFC 7009 | OAuth 2.0 Token Revocation | RFC | 2013 | 高 | 12 | [A] |
| RFC 9470 | OAuth 2.0 Step Up Authentication Challenge Protocol | RFC | 2023 | 中 | 11、12 | [A] |
| RFC 8628 | OAuth 2.0 Device Authorization Grant | RFC | 2019 | 中 | 11、12 | [A] |
| RFC 9635 | Grant Negotiation and Authorization Protocol (GNAP)，Standards Track | RFC | 2024-10 | 高 | 11、13 | [A] |
| OAuth 2.1 草案 draft-ietf-oauth-v2-1-16 | 强制 PKCE、废弃隐式流与密码模式 | IETF 草案 | 草案第 16 版 | 高 | 11、14 | [A] |
| OpenID Connect Core 1.0 | id_token、UserInfo、认证与授权分离 | OIDF 规范 | 1.0 | 高 | 11、17 | [A] |
| OpenID Connect Discovery 1.0 | /.well-known/openid-configuration | OIDF 规范 | 1.0 | 中 | 11、17 | [A] |
| FIDO Alliance 规范 | 无密码/抗钓鱼凭证 | 行业联盟规范 | — | 中 | 11 | [B] |
| W3C WebAuthn Level 2 | Web 认证 API | W3C 推荐 | Level 2 | 中 | 11 | [A] |
| UMA 2.0 | User-Managed Access，用户自管授权 | Kantara 规范 | 2.0 | 中 | 11（规划中） | [未验证] |
| RFC 8446 | TLS 1.3 | RFC | 2018 | 高 | 02、11、14 | [A] |
| RFC 5280 | X.509 PKI 证书与 CRL 规范 | RFC | 2008 | 高 | 02、11 | [A] |
| RFC 6960 | OCSP（在线证书状态查询） | RFC | 2013 | 中 | 02、11 | [A] |
| RFC 3161 | Time-Stamp Protocol（可信时间戳） | RFC | 2001 | 中 | 02、11、14 | [A] |
| RFC 8555 | ACME（自动化证书签发/轮换） | RFC | 2019 | 中 | 02、11 | [A] |
| RFC 5480 | ECDSA/EC 公钥在 X.509 中的表示 | RFC | 2009 | 中 | 02、12 | [A] |
| RFC 8017 | PKCS #1 RSA | RFC | 2016 | 中 | 12 | [A] |
| RFC 6090 | ECDSA/ECC 基础 | RFC | 2011 | 中 | 12 | [A] |
| RFC 8998 | ShangMi (SM) Cipher Suites for TLS 1.3 | RFC | 2021 | 高 | 02、12、16 | [A] |
| IEEE 1609.2 | WAVE 安全服务 / 证书格式 | IEEE 标准 | — | 中 | 11（规划中） | [C] |
| 美国 SCMS | V2X 安全证书管理体系 | 国家级体系 | — | 低 | 11（规划中） | [未验证] |
| GlobalPlatform TEE System Architecture | TEE 系统架构（规范号 GPD_SPE_009） | 规范 | v1.3 | 高 | 02、12 | [A] |
| GlobalPlatform Secure Element 规范库 | SE 分类 | 规范 | — | 高 | 02、12 | [A] |
| OP-TEE | 开源 TEE OS（TrustZone 之上的 TEE 实现） | 开源实现 | — | 中 | 02 | [A] |
| ARM TrustZone for Cortex-A | 应用处理器安全域 | 硬件技术 | — | 中 | 02 | [B] |
| ARM TrustZone for Cortex-M | 微控制器安全域 | 硬件技术 | — | 中 | 02 | [B] |
| EVITA 项目 | 车载 HSM Full / Medium / Light 三级分级 | 研究项目 | — | 中 | 02 | [B] |
| NIST FIPS 140-3 | 密码模块安全要求（HSM 认证基线） | FIPS | 140-3 | 高 | 02、12 | [A] |
| NIST FIPS 186-5 | 数字签名标准 DSS | FIPS | 186-5 | 中 | 02、12 | [A] |
| NIST FIPS 197 | AES | FIPS | 197 | 中 | 02、12 | [A] |
| NIST SP 800-57 Part 1 Rev.5 | 密钥管理建议：密钥生命周期、密码周期 | SP | Rev.5 | 高 | 12、14 | [A] |
| NIST SP 800-38D | GCM 模式 | SP | — | 中 | 02、12 | [A] |
| NIST SP 800-90A Rev.1 | 确定性随机比特发生器 | SP | Rev.1 | 中 | 12 | [A] |
| NIST SP 800-133 | 密钥生成 | SP | — | 中 | 12 | [A] |
| Infineon AURIX / TriCore | 32 位汽车微控制器 | 芯片 | — | 低 | 02 | [C] |
| NXP S32 | 汽车平台 | 芯片 | — | 低 | 02 | [未验证] |
| Renesas RH850 | 汽车产品线 | 芯片 | — | 低 | 02 | [C] |
| TI Jacinto TDA4VM | 车用 SoC | 芯片 | — | 低 | 02 | [C] |
| AUTOSAR Classic Platform | Crypto Stack、SecOC、IdsM 入侵检测 | 行业平台规范 | — | 中 | 02、14（CP-8） | [未验证] |
| TCG TPM 2.0 | 可信平台模块规范 | 行业规范 | 2.0 | 中 | 02 | [未验证] |
| SHE（Secure Hardware Extension） | 安全硬件扩展规范 | 成员制规范 | — | 中 | 02 | 未找到可核验公开一手 URL |
| CCC Digital Key Release 3.0 发布公告 | 新增 BLE + UWB，NFC 保留为强制备用，密钥存储于 Secure Element | 行业联盟公告 | Release 3.0，发布 2021-04-21 | 高 | 02、11、14 | [A] |
| CCC Digital Key 主页面 | 跨 OS 生态、认证计划 | 行业联盟页面 | — | 中 | 11 | [A] |
| CCC Digital Key Release 3 v1.1 规范开放 | 规范向公众开放 | 行业联盟公告 | v1.1 | 中 | 11 | [B] |
| CCC 与 FiRa 就 UWB 合作 | UWB 技术合作 | 行业联盟公告 | — | 中 | 11 | [B] |
| FiRa Consortium 2.0 技术规范 | UWB 技术规范 | 联盟规范 | 2023-11 | 中 | 11、14 | [B] |
| FiRa Core 3.0 规范与认证 | UWB 核心规范与认证 | 联盟规范 | 2025-01 | 中 | 11、14 | [B] |
| FiRa Core 4.0 规范与认证 | UWB 核心规范与认证 | 联盟规范 | 2025-12 | 低 | 11 | [B] |
| IEEE 802.15.4z | UWB 物理层增强 | IEEE 标准 | — | 中 | 11（规划中） | [未验证] |
| Uptane 框架官网 | 面向汽车、可抵御国家级攻击者的更新安全系统 | 开源框架 | — | 中 | 02 | [A] |
| Uptane Standard | Director 仓库 + Image 仓库双仓库模型 | 开源标准 | 2.1.0 | 高 | 02、14 | [A] |
| The Update Framework (TUF) 官网 | 阈值签名，防仓库/密钥泄露 | 开源框架 | — | 中 | 02 | [B] |
| TUF 规范 | Root / Targets / Snapshot / Timestamp 四角色 + 委托 + threshold/quorum | 开源规范 | latest | 高 | 02、14 | [A] |
| RFC 9019 | A Firmware Update Architecture for IoT Devices（SUIT 架构） | RFC | 2021 | 中 | 02 | [A] |
| RFC 9124 | A Manifest Information Model for Firmware Updates in IoT Devices | RFC | 2022 | 中 | 02 | [A] |
| IETF SUIT 工作组 | 固件更新标准工作组 | IETF 工作组 | — | 低 | 02 | [A] |
| SUIT Manifest 草案 draft-ietf-suit-manifest-27 | SUIT 清单信息模型草案 | IETF 草案 | 草案第 27 版 | 低 | 02 | [C] |
| SPDX 规范 | SBOM（对应 ISO/IEC 5962:2021） | 开放标准 | — | 低 | 02 | [A] |
| CycloneDX 规范 | SBOM | 开放标准 | — | 低 | 02 | [B] |
| SLSA v1.0 分级 | Build L0–L3，供应链构建完整性 | 开放规范 | v1.0 | 中 | 02、14 | [A] |
| in-toto 规范 | 供应链完整性元数据与签名链 | 开放规范 | — | 中 | 02 | [B] |
| OCPP 1.6 / 2.0.1 / 2.1 | 充电侧协议族，授权与计量 | 开放协议 | 1.6 / 2.0.1 / 2.1 | 中 | 11 | [A] |
| ISO 15118-2 / -20 | Plug & Charge，TLS + contract certificate | ISO 标准 | — | 中 | 11（规划中） | [未验证] |

**读表要点**：

1. 本表共收录 **103 条**规范/标准/法规条目，全部来自信源档案，无一新增。
2. 「相关度=高」集中在三处：**国标中的车联网平台与接口规范**（GB/T 47324、47467、40855、44402.1）、**OAuth 2.x 协议族**（§2.1）、**发送方约束与资源级授权规范**（RFC 8705 / 9449 / 9396 / 8693）。这三处正是本报告第 3 部分的论证脊柱。
3. «[未验证]» 与 «[C]» 条目**不得作为事实断言使用**；其使用限制逐条列于 19.10。
4. 国际标准（ISO/UN/欧盟法规）在本表中**整体处于低取证状态**（多为 `[未验证]`/`[C]`），这是信源档案 §0 记载的区域封锁与检索工具额度耗尽的直接后果，**不是这些标准不存在**。

---

## 19.3 OAuth / 身份协议速查表

本表是 §2.1 协议规范的**可执行视图**：把每条 RFC 的关键词、车云用途、关键参数或头字段提取为一行，供工程选型时横向对照。「关键参数/头」列只列规范中**定义**的字段名，不对任何车企是否使用该字段作断言（车企采用情况见 19.4 与 19.6）。

| RFC 编号 | 标题 | 关键词 | 车云典型用途 | 关键参数/头 | 引用章节 |
|---|---|---|---|---|---|
| RFC 6749 | The OAuth 2.0 Authorization Framework | 授权码/隐式/密码/客户端凭证 | 第三方应用代表车主访问车云 API 的授权底座 | `response_type`、`client_id`、`redirect_uri`、`scope`、`state`、`grant_type` | 11、12、13 |
| RFC 6750 | OAuth 2.0 Bearer Token Usage | Bearer 令牌传输 | 车云 API 的默认令牌携带方式；错误语义统一 | `Authorization: Bearer`、`WWW-Authenticate` | 11、12 |
| RFC 7636 | PKCE | 授权码拦截防护 | 公共客户端（移动 App / 车机）必用 | `code_challenge`、`code_challenge_method`、`code_verifier` | 11、12、14 |
| RFC 8252 | OAuth 2.0 for Native Apps | 外部用户代理 | 车载/移动 App 禁内嵌 WebView，必须用系统浏览器 | 重定向 URI 策略、外部用户代理要求 | 11、14 |
| RFC 9068 | JWT Profile for OAuth 2.0 Access Tokens | 访问令牌 JWT Profile | 自校验访问令牌的格式与校验义务 | `typ: at+jwt`、`aud`、`iss`、`exp` | 12、14 |
| RFC 8705 | Mutual-TLS Client Authentication and Certificate-Bound Access Tokens | mTLS 证书绑定令牌 | 车云链路最关键：令牌与客户端证书绑定，复制即失效 | client certificate、`cnf`（证书指纹绑定） | 11、12、14 |
| RFC 9449 | OAuth 2.0 Demonstrating Proof of Possession (DPoP) | 发送方约束令牌 | 无 mTLS 时的令牌防复制替代方案 | `DPoP` 头、JWK 指纹绑定、DPoP nonce | 11、12、14 |
| RFC 9396 | OAuth 2.0 Rich Authorization Requests | 结构化权限对象 | 车控场景「资源级授权」的规范依据，替代裸字符串 scope | `authorization_details`（含 location/action/privilege 语义） | 11、13、14 |
| RFC 8693 | OAuth 2.0 Token Exchange | 代授权/代理链 | 表达「谁代表谁」执行，云内部越权可审计 | `subject_token`、`actor_token`、`act` 链 | 11、12、14 |
| RFC 7523 | JWT Profile for OAuth 2.0 Client Authentication and Authorization Grants | 客户端断言 | 服务账号（微服务身份）认证 | JWT client assertion、`grant_type` | 11、12、14 |
| RFC 7662 | OAuth 2.0 Token Introspection | 令牌内省 | 不透明令牌的实时校验；scope 缩减后的即时生效手段 | introspection endpoint、`active` | 12、14 |
| RFC 8414 | OAuth 2.0 Authorization Server Metadata | 元数据自动发现 | 客户端自动发现授权服务器端点 | `.well-known/oauth-authorization-server` | 11、12、17 |
| RFC 7009 | OAuth 2.0 Token Revocation | 令牌吊销 | 车主/企业主动吊销第三方令牌 | revocation endpoint、`token_type_hint` | 12 |
| RFC 9470 | OAuth 2.0 Step Up Authentication Challenge | 步进认证 | 高敏感车控操作要求二次强认证 | `acr`、`amr`、`WWW-Authenticate` 挑战 | 11、12 |
| RFC 8628 | OAuth 2.0 Device Authorization Grant | 设备授权 | 无浏览器/受限 UI 的车机授权场景 | `device_code`、`user_code`、轮询 `interval` | 11、12 |
| RFC 9635 | Grant Negotiation and Authorization Protocol (GNAP) | 可协商授权 | 下一代授权：细粒度 + 可协商，代表演进方向 | grant request/continue、access token 协商 | 11、13 |
| draft-ietf-oauth-v2-1-16 | OAuth 2.1 草案 | 强制 PKCE | 迁移目标：废弃隐式流与密码模式，Bearer 令牌最小化 | 强制 PKCE、移除 implicit/password | 11、14 |
| OpenID Connect Core 1.0 | OIDC 核心 | 认证与授权分离 | 车主身份认证；`id_token` 用于身份而非授权 | `id_token`、UserInfo、`nonce` | 11、17 |
| OpenID Connect Discovery 1.0 | OIDC 发现 | 配置发现 | 发现 OIDC 端点与密钥 | `/.well-known/openid-configuration` | 11、17 |
| FIDO Alliance 规范 | FIDO2 / 抗钓鱼凭证 | 无密码认证 | 车主账号强认证、抗钓鱼 | 公钥凭证、attestation | 11 |
| W3C WebAuthn Level 2 | WebAuthn | 浏览器/平台认证器 API | OIDC 的强认证凭据层 | PublicKeyCredential、challenge | 11 |
| UMA 2.0 | User-Managed Access | 用户自管授权 | 用户对数据共享的细粒度自管（本次未取证） | resource/authorization API（未取证） | 11（规划中） |

**读表要点**：

1. 「高相关度」的协议是 **RFC 8705 / 9449 / 9396 / 8693 / 7636**——它们分别解决「令牌不可复制」「资源级授权」「代授权可审计」「授权码不可拦截」四个车云授权最关键的问题。
2. 授权码流（RFC 6749）是**底座**而非终点：本表 22 条协议中的绝大多数是对它的**加固或扩展**。
3. 表中「关键参数/头」均为规范**定义**名，与任何车企的实际采用无关；实际采用证据见 19.4。

---

## 19.4 车企与平台端点 / 凭证清单

本表汇总信源档案 §7 中所有**已取证的 URL 与鉴权机制**。**严禁新增信源档案未载的 URL**；表内每一行均可在 §7 找到逐字对应的原条目。「证据等级」列区分「一手文档」与「直接观测」（如占位页、403、封锁）。凡信源档案标注为失败观测的行，其「已取证参数/scope 示例」列为空或记「无」。

| 主体 | 端点或文档 URL | 鉴权方式 | 已取证的参数/scope 示例 | 证据等级 | 备注 |
|---|---|---|---|---|---|
| Tesla | `https://developer.tesla.com/docs/fleet-api/authentication/overview` | `Authorization: Bearer <token>` | 令牌类型：third-party token、partner token、third-party-for-business token；12 个 scope 全清单 | [A] | Fleet API 授权总览；scope 与令牌模型的一手源 |
| Tesla | `https://fleet-auth.prd.vn.cloud.tesla.com/oauth2/v3/thirdparty/.well-known/openid-configuration` | 公开元数据 | 授权服务器元数据（对应 RFC 8414 / OIDC Discovery） | [A] | 元数据端点，非调用端点 |
| Tesla | `https://auth.tesla.com/oauth2/v3/authorize` | 授权码流授权端点 | `response_type=code`、`client_id`、`redirect_uri`、`scope`、`state`；可选 `nonce` | [A] | 车主同意与授权码签发 |
| Tesla | `/authorize` 可选参数（同文档） | — | `prompt_missing_scopes=true`、`require_requested_scopes=true`、`show_keypair_step=true` | [A] | scope 增补与密钥配对预告 |
| Tesla | `POST https://fleet-auth.prd.vn.cloud.tesla.com/oauth2/v3/token` | 令牌端点（与应用服务器不同主机） | `grant_type=authorization_code`、`client_id`、`client_secret`、`audience`（须为 Fleet API base URL）、`redirect_uri`、`scope` | [A] | `/token` 调用来自应用服务器、适用不同限流 |
| Tesla | `https://auth.tesla.com/user/revoke/consent?revoke_client_id=$CLIENT_ID&back_url=$RETURN_URL` | 车主侧授权管理 | 撤销授权 / 管理授权范围 | [A] | 车主可撤销入口 |
| Tesla | `https://developer-domain.com/.well-known/appspecific/com.tesla.3p.public-key.pem` | 公钥托管（HTTPS） | 虚拟密钥公钥，必须长期可用 | [A] | 私钥 `private-key.pem` 绝不可托管于域名 |
| Tesla | 配对深链 `https://tesla.com/_ak/<developer-domain.com>`（可选 `?vin=...`） | 车辆侧密钥配对 | 深链触发车端加钥 | [A] | 需已授予 vehicle_device_data / vehicle_cmds / vehicle_location 之一 |
| Tesla | `https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide` | 虚拟密钥（车端验签） | 密钥生成命令 `openssl ecparam -name prime256v1 -genkey -noout`；车辆仅支持 prime256v1 | [A] | 车端执行命令前验签 |
| Tesla | `https://developer.tesla.com/docs/fleet-api/authentication/third-party-tokens` | 第三方令牌流程 | 刷新令牌一次性、3 个月过期、24 小时宽限 | [A] | 令牌轮换强约束的一手源 |
| Tesla | `https://developer.tesla.com/docs/fleet-api/fleet-telemetry` | Fleet Telemetry（车→云直连） | 单车最多 5 个第三方推流；500 ms 事件窗口；断连缓冲 5000 条 | [A] | 取代轮询 vehicle_data |
| Tesla | `https://developer.tesla.com/docs/fleet-api/billing-and-limits` | 限流与计费 | 限流 60/3/30 次每分；计费上限默认 0 | [A] | 影响范围控制的另一维度 |
| Tesla | `https://github.com/teslamotors/fleet-telemetry` | 官方 SDK 仓库 | 客户端源码 | [A] | 服务端 TLS 校验脚本 `tools/check_server_cert.sh` 在同仓库 |
| Tesla | `https://github.com/teslamotors/vehicle-command` | 官方仓库 | 命令代理 | [A] | 与虚拟密钥配合 |
| Tesla | `https://bugcrowd.com/engagements/tesla` | 漏洞赏金（Bugcrowd 运营） | 启动于 2015-08-04；赏金档位 Critical $50,000–$100,000 等 | [A/B] | 车辆/能源问题须走邮件而非网页表单 |
| Mercedes-Benz | `https://developer.mercedes-benz.com` | 开发者平台入口 | 运营主体 Mercedes-Benz Connectivity Services GmbH | [A] | 页脚版权 © 2026 |
| Mercedes-Benz | `https://developer.mercedes-benz.com/product-docs` | 文档页 | 两种鉴权集成模式：Authorization Code Flow 与 Client Credentials Flow | [A] | — |
| Mercedes-Benz | `https://developer.mercedes-benz.com/get-started/oauth/authorization-code-flow` | 授权码流 | `scope=openid offline_access mb:vehicle:mbdata:fuelstatus`；令牌端点用 HTTP Basic | [A] | 五步流程一手源 |
| Mercedes-Benz | `https://ssoalpha.dvb.corpinter.net/v1/auth?response_type=code&client_id=...&redirect_uri=...&scope=...&state=...` | 授权端点（文档给出的示例） | `response_type=code`、`client_id`、`redirect_uri`、`scope`、`state` | [A] | 示例端点，非生产地址 |
| Mercedes-Benz | `https://ssoalpha.dvb.corpinter.net/v1/token` | 令牌端点（文档给出的示例） | 客户端认证用 HTTP Basic（`clientId:clientSecret` BASE64） | [A] | `expires_in` 默认 3599 秒 |
| Mercedes-Benz | 同意界面语义（同文档） | 用户同意 | 展示所请求 SCOPE 与 purpose URL；`openid` 与 `offline_access` 各自必要性 | [A] | 知情同意设计样本 |
| BYD（i迪桥） | `https://open.byd.com/` | API Key（appKey） | 首页显示「12 已上线服务 / 60 服务总系统 / 53.8 亿+ 累计服务请求数」；© 2025 | [A] | 企业级 ESB/API 网关，非车控开放平台 |
| BYD（i迪桥） | `https://open.byd.com/platform?id=1848412878248345602` | API Key（appKey） | `x-Gateway-APIKey`：应用的 appKey，传入 Header 头；文档发布 2024-01-23 | [A] | 接口调用文档一手源 |
| BYD（i迪桥） | `https://esb.byd.com.cn/tong/restful/api/mdm07670/package_1` | 网关示例域名 | 文档注明「以上示例只作为参考不可实际调用」 | [A] | 示例 URL，不可实际调用 |
| BYD（i迪桥） | `https://open.byd.com/notices-details?id=1994268247284723713&toB=1` | 平台版本公告 | 「i迪桥平台 3.3.4 版本全面升级」含 API 在线导出等 | [A] | — |
| 蔚来 NIO（Open NSC） | `https://developer.nio.com/` | 平台入口 | GitBook 托管；站点自述「正在建设中」 | [A] | — |
| 蔚来 NIO（Open NSC） | `https://developer.nio.com/docs/open-nsc/spec/integration-process.html` | app-id + secret 双凭证（非 OAuth） | 「app-id 和 secret 是系统对接调用的唯一凭证……通过商务渠道获取」 | [A] | 双凭证非 scope 模型 |
| 蔚来 NIO（Open NSC） | `https://developer.nio.com/docs/open-nsc/spec/env.html` | 环境说明 | stg `https://open-stg.nio.com`；prod `https://open.nio.com` | [A] | — |
| 蔚来 NIO（Open NSC） | `https://developer.nio.com/docs/open-nsc/spec/interface.html` | 文档访问本身受 token 保护 | 「请联系文档提供人获取文档访问 token」 | [A] | 平台侧把文档访问也纳入授权控制 |
| 小米 | `https://iot.mi.com/` | 面向硬件模组厂商的开发者平台 | 接入流程「成为开发者 → 创建产品 → 研发配置 → 认证发布」 | [A] | 非车企车云 API 开放平台 |
| 小米 | `https://iot.mi.com/v2/new/doc/home` | 文档中心 | 标题「小米IoT文档与资源中心」 | [A] | HTTP 200 |
| 小米（信任中心） | `https://trust.mi.com/zh-CN/compliance` | 合规章页 | ISO/IEC 27001 认证（编号 IS 831552） | [A] | 范围含小米科技 IT 运维与云服务 |
| BMW | `https://developer.bmwgroup.com/` | 占位页（无内容） | Apache 占位页「no content deployed」，Last-Modified 2026-04-27 | [A，直接观测] | 未提供 CarData / OAuth 文档 |
| BMW | `https://crd.bmwgroup.com/` / `https://b2b-developer.bmwgroup.com/` | 不可达 | 前者无法解析；后者超时 | [A，直接观测] | — |
| BMW | `https://b2b.bmw.com` | 供应商采购门户 | purchasing/logistics 登录 | [A，直接观测] | 非车辆数据开发者 API 门户 |
| Rivian | `https://rivian.com` | CloudFront 区域封锁 | 「The CloudFront distribution is configured to block access from your country」 | [A，直接观测] | — |
| Rivian | `developer.rivian.com` / `api.rivian.com` | 前者无 DNS；后者为 App 后端 | `api.rivian.com` 可解析（13.35.190.19） | [A，直接观测] | 非公开开发者门户 |
| 小鹏 | `https://open.xiaopeng.com/dev/` | 全请求 403（openresty） | 无法核实鉴权机制/scope/令牌有效期 | [A 站点存在，内容不可验证] | — |
| 小鹏 | `https://login.xiaopeng.com/policy.html` | 用户协议 | 主体广州智鹏车联网科技有限公司 | [A] | — |
| 理想 | `https://www.lixiang.com/agreement/privacy.html` | 隐私政策 | 生效 2026-01-22；主体北京车励行信息技术有限公司、北京罗克维尔斯科技有限公司 | [A] | `open.lixiang.com`、`developer.lixiang.com` 均无 DNS |
| 极氪 | `https://open.zeekrlife.com` | 返回 HTTP 500 空页 | 无可用信息 | [A 站点存在，无可用信息] | — |
| 零跑 | `https://cn.leapmotor.com` | 可达但无开放平台入口 | `developer./dev./open.leapmotor.com` 均无 DNS | 未找到公开来源 | — |
| 奇瑞 | `https://www.chery.cn/others/networksecurity/` | 官网「网络产品安全漏洞」专栏 | 页面可达 | [A] | `developer.chery.cn`、`open.chery.cn` 无 DNS |
| 华为 | `https://developer.huawei.com/consumer/cn/` | 开发者联盟统一入口 | Wallet Kit 数字车钥匙文档返回 JS 空壳页（1749 字节） | 未找到可验证公开来源 | — |
| 蔚来（二手） | `https://auto.sina.cn/2026-07-18/detail-iniicyyt8275101.d.html` | 二手报道 | 「UWB+蓝牙+NFC 三合一数字钥匙」 | [C] | 蔚来官方未取得技术说明 |
| Volkswagen / CARIAD | `https://cariad.technology/de/en/solutions/automotive-cloud-connectivity.html` | 官方自述页 | 「45 million connected vehicles」「90 markets connected」 | [A，公司自述口径] | 营销口径，非技术规范 |
| Volkswagen / CARIAD | `https://cariad.technology/` | 官方站点 | 「We are the Volkswagen Group's automotive software company…」 | [A] | 未取到安全白皮书 |

**读表要点**：

1. 表中**唯一可完整对照的「逐车主授权 + 令牌 + 密钥」实现是 Tesla Fleet API**；Mercedes-Benz 是第二完整的样本（令牌与同意模型，字段级策略未载）。
2. 国内车企中，BYD / 蔚来 / 小米 的公开接入均为**非车控平台**（ESB、服务云、IoT 模组平台）；**不得据此归纳「国内车企车云授权 = APIKey」**（信源档案 §7.10 第 3 条）。
3. 表中所有失败观测（403、占位页、区域封锁、无 DNS）均为**披露缺口**，在 19.11 逐条登记。

---

## 19.5 令牌与密钥参数对照表

本表把信源档案中所有**离散的数值/规则**集中为可比较参数。凡单位为「分」「秒」「毫秒」「条」「把」者，均按信源档案原文语义标注。本表是 19.6（scope 粒度）与 19.13（结论）的数值依据。

| 来源 | 参数项 | 已取证值或规则 | 单位/语义 | 引用章节 | 证据等级 |
|---|---|---|---|---|---|
| Tesla | 刷新令牌使用次数 | 一次性使用（single use only） | 次数 | 12、13、17 | [A] |
| Tesla | 刷新令牌过期 | 3 个月后过期 | 时间 | 12、13、17 | [A] |
| Tesla | 刷新令牌宽限期 | 最近一次使用的刷新令牌在 24 小时内仍有效 | 时间（覆盖持久化失败场景） | 12、14、17 | [A] |
| Tesla | 刷新失败返回 | `401 login_required`（刷新令牌过期/被更新令牌挤出，或用户已重置密码） | HTTP 状态/错误码 | 12、17 | [A] |
| Tesla | 访问令牌 TTL | **未获证实**（已证实的仅为刷新令牌 3 个月 + 24h 宽限） | 时间 | 12、13 | 未找到公开来源 |
| Mercedes-Benz | 访问令牌有效期 | 响应 `expires_in` 默认 3599 秒（≈1 小时） | 秒 | 12、14、17 | [A] |
| Mercedes-Benz | 刷新令牌使用次数 | 一次性使用；刷新返回新的访问令牌与新的刷新令牌 | 次数 | 12、17 | [A] |
| Mercedes-Benz | 已用/无效刷新令牌报错 | 「The given refresh token is not valid or was already used」 | 错误语义 | 12、17 | [A] |
| Mercedes-Benz | invalid_scope 报错 | 「No registered scope value for this client has been requested」 | 错误语义 | 12、17 | [A] |
| Mercedes-Benz | 令牌端点客户端认证 | HTTP Basic（`clientId:clientSecret` BASE64 置于 Authorization 头） | 认证方式 | 12、17 | [A] |
| Tesla | 虚拟密钥曲线 | 车辆仅支持 prime256v1（P-256 ECDSA） | 曲线 | 12、13、17 | [A] |
| Tesla | 虚拟密钥生成命令 | `openssl ecparam -name prime256v1 -genkey -noout` | 命令 | 12、17 | [A] |
| Tesla | 密钥数量上限 | B2B 项目自动添加虚拟密钥条件为「已配对密钥少于 20 把」 | 把 | 13、14、17 | [A] |
| Tesla | 单车推流上限 | 单台车辆最多同时向 5 个第三方应用推流 | 个 | 13、14、17 | [A] |
| Tesla | 限流（实时数据） | 60 次/分 | 次每分（按账号按设备计） | 13、14、17 | [A] |
| Tesla | 限流（唤醒） | 3 次/分 | 次每分 | 13、14、17 | [A] |
| Tesla | 限流（设备命令） | 30 次/分 | 次每分 | 13、14、17 | [A] |
| Tesla | 限流共享语义 | 同账号多应用**共享**限额 | 语义 | 13、14、17 | [A] |
| Tesla | 遥测断连缓冲 | 车辆缓冲 5000 条消息（≥2500 秒数据） | 条 / 秒 | 12、14、17 | [A] |
| Tesla | 遥测重连退避 | 指数退避，最大重试延迟 30 秒 | 秒 | 12、14、17 | [A] |
| Tesla | 遥测事件窗口 | 500 ms 事件收集窗口 | 毫秒 | 13、17 | [A] |
| Tesla | 遥测上报触发 | 按字段 `interval_seconds` 与变化触发上报 | 秒 | 13、17 | [A] |
| Tesla | 遥测示例负载成本 | 约 15 信号/分钟 ≈ $0.0001/分钟 ≈ $0.006/行驶小时 | 信号 / 美元 | 13、17 | [A] |
| Tesla | 计费周期与上限 | 按用量、月度周期（每月 1 日起算）；每账号计费上限**默认 0** | 美元 | 13、17 | [A] |
| Tesla | 计费预警 | 达 80% 与 100% 时发邮件 | 阈值 | 13、17 | [A] |
| Tesla | 超限后果 | 暂停 API 使用并移除 Fleet Telemetry 推流配置（且不恢复） | 语义 | 13、14、17 | [A] |
| Tesla | 计费判定 | 响应码 <500 全部计费，≥500 不计费 | 规则 | 17 | [A] |
| Tesla | 计费取整 | 费用四舍五入到 $0.01 | 美元 | 17 | [A] |
| Tesla | 开发者折扣 | 个人开发者/小应用每月 $10 折扣 | 美元 | 17 | [A] |
| Tesla | 付费 API 过渡日期 | 「Application access will not be disabled during the payment transition period which ends February 1, 2024」 | 日期（一手引文） | 17 | [A] |
| Tesla | Fleet Telemetry 前置条件 | 车辆固件 2024.26+；证书签名类应用 2023.20.6+；Model S/X（Intel Atom）2025.20+ | 固件版本 | 17 | [A] |
| Tesla | Fleet Telemetry 客户端版本 | 1.0.0 / 1.1.0 / 1.2.0 / 1.3.0（对应固件 2025.2.6、2025.44.25.5、2026.26.6 等） | 版本 | 17 | [A] |
| Tesla | 位置拒绝响应 | hide_private 共享车辆访问位置字段返回 HTTP 403 「location access not granted」 | HTTP 状态 | 13、14、17 | [A] |
| CCC | 数字钥匙通道 | BLE + UWB 实现被动进入与启动；NFC 保留为强制备用 | 通道 | 11、14 | [A] |
| CCC | 数字钥匙密钥存储 | 存储于 Secure Element | 载体 | 11、14 | [A] |
| Tesla | 漏洞赏金档位 | Critical $50,000–$100,000；High $20,000–$50,000；Moderate $10,000–$20,000；Low $500–$10,000 | 美元 | 17 | [B] |
| Tesla | 漏洞报告时限 | 若访问到不属于自己的数据须在 24 小时内停止并披露 | 小时 | 17 | [B] |

**读表要点**：

1. 表中**唯一的空缺是 Tesla 访问令牌 TTL**——信源档案明确记载该值「未获证实」，并标记为待补证（对齐 AC-8）。
2. Tesla 的参数密度远高于其他主体，这**直接源于文档公开度**，不代表其他车企缺少同等机制。
3. 「一次性刷新令牌 + 24 小时宽限」「默认 `expires_in` 3599 秒」「prime256v1」「<20 把密钥」「≤5 推流」「60/3/30 次每分」「5000 条缓冲」「30 秒退避上限」「500 ms 窗口」这九个数值，是本章后续所有量化对照的公共基准。

---

## 19.6 Scope 命名与粒度对照表

本表把 Tesla 的 12 个 scope、Mercedes 的 3 个已取证 scope，以及两个**非字符串 scope 的结构化替代方案**（RFC 9396 RAR、RFC 9635 GNAP）并列对照。「粒度层级」列区分：账号级（覆盖账号下全部车辆）、类别级（覆盖某类资源）、资源级（可细到单资源/单字段）、协商级（运行时协商）。「是否可收窄」列记录信源档案中关于**收窄行为**的一手陈述。

| 平台 | scope 字符串 | 覆盖资源 | 粒度层级 | 是否可收窄 | 同意主体 | 引用章节 |
|---|---|---|---|---|---|---|
| Tesla | `openid` | 「Sign in with Tesla」：允许车主用 Tesla 凭证登录第三方应用 | 账号级 | 不适用 | 车主 | 13、17 |
| Tesla | `offline_access` | 获取刷新令牌以免重复登录 | 账号级 | 不适用 | 车主 | 13、17 |
| Tesla | `user_data` | 联系方式、家庭住址、头像、推荐信息 | 类别级 | 未载 | 车主 | 13、17 |
| Tesla | `vehicle_device_data` | 实时数据、服务历史、服务预约、服务沟通、可升级项、附近超充、所有权信息 | 类别级 | 未载 | 车主 | 13、17 |
| Tesla | `vehicle_location` | 精确与粗略位置 | 类别级（受双层控制进一步收窄） | **可收窄**：`granular_access.hide_private=true` 下即使授予也拿不到任何位置，且无法流式传输位置字段 | 车主 | 13、14、17 |
| Tesla | `vehicle_cmds` | 添加/移除驾驶员、Live Camera 访问、解锁、唤醒、远程启动、预约软件更新 | 类别级 | 未载 | 车主 | 13、17 |
| Tesla | `vehicle_charging_cmds` | 充电历史、计费金额、充电地点、预约/开始/停止充电 | 类别级 | 未载 | 车主 | 13、17 |
| Tesla | `vehicle_specs` | 车辆规格 | 类别级 | **仅 Partner Token 可用**，对任意车辆可用、无需车主授权 | 无（Partner 路径） | 13、14、17 |
| Tesla | `vehicle_pricing_info` | 车辆定价信息 | 类别级 | **仅 Partner Token 可用** | 无（Partner 路径） | 13、17 |
| Tesla | `energy_device_data` | 能源设备数据 | 类别级 | 未载 | 车主 | 13、17 |
| Tesla | `energy_cmds` | 能源设备命令 | 类别级 | 未载 | 车主 | 13、17 |
| Tesla | `enterprise_management` | 企业管理能力 | 账号/组织级 | 未载（内部细粒度定义未取证） | 企业（B 端） | 13、17 |
| Mercedes-Benz | `openid` | 获得有效令牌所必需 | 账号级 | 不适用 | 车主 | 17 |
| Mercedes-Benz | `offline_access` | 获得刷新令牌所必需 | 账号级 | 不适用 | 车主 | 17 |
| Mercedes-Benz | `mb:vehicle:mbdata:fuelstatus` | 燃油状态（Fuel Status 产品示例） | **资源级**（`mb:` 命名空间式，产品-域-资源三段式） | 未载 | 车主（含 purpose URL 知情同意） | 17 |
| 通用（RFC 9396） | `authorization_details`（结构化权限对象，非字符串 scope） | 资源/动作/时限的组合 | **资源级**（locations/actions/privileges 参与判定） | 机制内建（结构化收窄） | 由部署方定义 | 11、13 |
| 通用（RFC 9635） | GNAP access（可协商权限，非字符串 scope） | 运行时协商的细粒度权限 | **协商级** | 机制内建（协商式） | 由部署方定义 | 11、13 |

**读表要点**：

1. **两种 scope 命名范式并存**：Tesla 用**扁平英文枚举**（`vehicle_cmds`），Mercedes 用**冒号分隔命名空间**（`mb:vehicle:mbdata:fuelstatus`）。后者在语义上更接近「产品-域-资源」三段式，是资源级 scope 设计的典型样本。
2. **粒度与收窄是两个独立维度**：Tesla 的 scope 是类别级，但通过 `granular_access.hide_private` 实现了**字段级收窄**——这是「授权被授予但资源级策略进一步收窄」的双层控制实例（判为 Informational 正面案例）。
3. **授权控制例外**：`vehicle_specs` / `vehicle_pricing_info` 仅 Partner Token 可用且无需车主授权，**跳出了「逐车主同意」模型**，在章节 14 判为 **High**（对齐审计计划 §3.3）。
4. 表中**没有任何车企公开采用 RFC 9396 RAR 或 RFC 9635 GNAP 的一手证据**——这两行是规范层能力，不是落地事实（见 19.11）。

---

## 19.7 国家标准与实施时间线表

本表严格使用信源档案 §1.1–§1.3 载明的发布日期与实施日期，**不补全任何未载日期**。「状态」列区分强制（GB）与推荐（GB/T）；「对车云授权的影响方向」列给出该标准对授权/访问控制议题的**作用面**（方向性描述，非条款引用）。

| 编号 | 名称 | 状态 | 发布日期 | 实施日期 | 对车云授权的影响方向 |
|---|---|---|---|---|---|
| GB 44495-2024 | 汽车整车信息安全技术要求 | 强制 | 2024-08-23 | 2026-01-01 | 整车信息安全基线；2026-01-01 起对新车型强制适用，是车云授权的合规上限约束 |
| GB 44496-2024 | 汽车软件升级通用技术要求 | 强制 | 2024-08-23 | 2026-01-01 | OTA 安全基线，约束升级授权与签名链 |
| GB/T 40855-2021 | 电动汽车远程服务与管理系统信息安全技术要求及试验方法 | 推荐 | 2021-10-11 | 2022-05-01 | 直接约束「车-云远程服务」的访问控制与身份 |
| GB/T 40856-2021 | 车载信息交互系统信息安全技术要求及试验方法 | 推荐 | 2021-10-11 | 2022-05-01 | 车载信息交互侧的授权与隔离要求 |
| GB/T 40857-2021 | 汽车网关信息安全技术要求及试验方法 | 推荐 | 2021-10-11 | 2022-05-01 | 网关域间访问控制（对应章节 14 的 CP-7） |
| GB/T 38628-2020 | 信息安全技术 汽车电子系统网络安全指南 | 推荐 | 2020-04-28 | 2020-11-01 | 汽车电子系统网络安全的方法论指南，含访问控制原则 |
| GB/T 41871-2022 | 信息安全技术 汽车数据处理安全要求 | 推荐 | 2022-10-14 | 2023-05-01 | 数据处理的授权与最小化要求 |
| GB/T 44464-2024 | 汽车数据通用要求 | 推荐 | 2024-08-23 | 2024-08-23 | 汽车数据通用规则（发布与实施同日） |
| GB/T 45112-2024 | 基于 LTE 的车联网无线通信技术 安全证书管理系统技术要求 | 推荐 | 2024-12-31 | 2025-04-01 | 车-云-车证书体系的国家级规范 |
| GB/T 45181-2024 | 车联网网络安全异常行为检测机制 | 推荐 | 2024-12-31 | 2025-04-01 | 异常行为检测，支撑授权滥用的发现能力 |
| GB/T 47324-2026 | 车联网平台网络安全防护要求 | 推荐 | 2026-03-31 | 2026-10-01 | **直接命中本报告主题：车联网云平台侧的防护要求** |
| GB/T 47325-2026 | 车联网在线升级安全技术要求与测试方法 | 推荐 | 2026-03-31 | 2026-10-01 | OTA 在线升级安全的技术要求与测试方法 |
| GB/T 47467-2026 | 车联网安全管理接口规范 | 推荐 | 2026-04-30 | 2026-11-01 | **接口层规范，与授权/访问控制的 API 治理直接相关** |
| GB/T 44402.1-2024 | 卡及身份识别安全设备 数字钥匙系统 第 1 部分：参考架构 | 推荐 | 2024-08-23 | 2025-03-01 | 中国数字钥匙授权模型的国标参考架构 |
| GB/T 32918.1~.5-2016/2017 | SM2 椭圆曲线公钥密码算法 | 推荐 | 未载（分部分年份见编号） | 未载 | 国密公钥算法基线，支撑国密授权签名 |
| GB/T 32905-2016 | SM3 密码杂凑算法 | 推荐 | 未载 | 未载 | 国密杂凑算法基线 |
| GB/T 32907-2016 | SM4 分组密码算法 | 推荐 | 未载 | 未载 | 国密对称算法基线 |
| GB/T 35275-2017 | SM2 密码算法加密签名消息语法规范 | 推荐 | 未载 | 未载 | SM2 加密签名消息语法，授权报文的国密编码 |
| GB/T 35276-2017 | SM2 密码算法使用规范 | 推荐 | 未载 | 未载 | SM2 使用规范，授权签名实现依据 |
| 汽车数据安全管理若干规定（试行） | 网信办等五部门令第 7 号 | 强制（部门规章） | 2021-08-16 成文 | 2021-10-01 施行 | 重要数据目录、境内存储、年度报送、出境评估等义务 |
| 汽车数据安全管理若干规定 答记者问 | 官方解读 | — | 2021-08-20 | — | 官方问答，辅助理解上述规定 |

**读表要点**：

1. **两个关键节点**：**2026-01-01**（GB 44495 / 44496 强制适用）与 **2026-10-01 / 2026-11-01**（GB/T 47324 / 47325 / 47467 实施）。前者是合规硬门槛，后者直接覆盖平台侧与接口侧授权。
2. 表中「未载日期」的五项（SM 系列国标）因信源档案未记录发布/实施日期而留空——**不补全**（对齐 AC-7）。
3. 强制 vs 推荐：仅 GB 44495 / GB 44496 为强制，其余为推荐性（企业自愿采用，但常被合同/认证引用）。

---

## 19.8 硬件与密码基元对照表

本表汇总信源档案 §3–§5 中的硬件根信任与密码基元。「提供的保证 / 不提供的保证」两列用于防止把单一机制过度解读——每一项只在其**规定的作用域内**提供保证。

| 机制 | 规范依据 | 作用位置 | 提供的保证 | 不提供的保证 | 引用章节 |
|---|---|---|---|---|---|
| TEE（可信执行环境） | GlobalPlatform TEE System Architecture v1.3（GPD_SPE_009） | 主控芯片上的隔离执行环境 | 与富执行环境（REE）隔离的代码/数据执行 | 不保证抗物理提取；不保证 REE 侧不泄露 | 02、12 |
| OP-TEE | 开源 TEE OS | TrustZone 之上的 TEE 实现 | 开源可审计的 TEE 实现 | 不提供芯片级抗攻击 | 02 |
| ARM TrustZone for Cortex-A | ARM 硬件技术 | 应用处理器安全域划分 | 硬件级安全/非安全世界隔离 | 不提供密钥不可导出保证 | 02 |
| ARM TrustZone for Cortex-M | ARM 硬件技术 | 微控制器安全域划分 | 微控制器级隔离 | 同上 | 02 |
| 车载 HSM（EVITA Full/Medium/Light） | EVITA 项目分级 | 车载安全硬件模块 | 分级的安全功能与密钥运算 | 分级不同则不保证同等抗攻击能力 | 02 |
| Secure Element（SE） | GlobalPlatform SE 规范库 | 独立安全芯片 | 密钥存储与运算的强隔离（CCC 数字钥匙密钥即存于 SE） | 不保证应用层逻辑正确 | 02、11 |
| FIPS 140-3 | NIST FIPS 140-3 | 密码模块认证 | 密码模块安全等级认证（HSM 认证基线） | 不保证系统级授权逻辑 | 02、12 |
| FIPS 186-5 | NIST FIPS 186-5 | 数字签名 | DSS 数字签名标准 | 不约束密钥生命周期管理与吊销 | 02、12 |
| FIPS 197 | NIST FIPS 197 | AES | 对称加密标准 | 不约束模式与密钥派生 | 02、12 |
| SP 800-57 Part 1 Rev.5 | NIST SP 800-57 Pt.1 R5 | 密钥生命周期 | 密钥生命周期与密码周期建议 | 不规定具体实现 | 12、14 |
| SP 800-38D | NIST SP 800-38D | GCM 模式 | AEAD 加密模式规范 | 不防 nonce 重用（实现责任） | 02、12 |
| SP 800-90A Rev.1 | NIST SP 800-90A R1 | 随机数生成 | 确定性随机比特发生器 | 不保证熵源质量（实现责任） | 12 |
| SP 800-133 | NIST SP 800-133 | 密钥生成 | 密钥生成建议 | 不规定存储方式 | 12 |
| TPM 2.0 | TCG TPM 2.0 规范 | 平台可信模块 | 平台度量与绑定密钥 | 规范正文本次未取证 | 02 |
| SHE（Secure Hardware Extension） | 成员制规范 | 车载安全硬件扩展 | 局域网内的安全通信与密钥 | 本次未找到可核验公开一手 URL | 02 |
| SM2 | GB/T 32918.1~.5 | 公钥密码（签名/交换/加密） | 国密公钥算法，国产车云授权签名基线 | 不约束协议集成方式 | 02、12 |
| SM3 | GB/T 32905-2016 | 杂凑 | 国密杂凑算法 | 不提供加密能力 | 02、12 |
| SM4 | GB/T 32907-2016 | 分组密码 | 国密对称算法 | 不约束模式选择 | 02、12 |
| SM2 消息语法 | GB/T 35275-2017 / GB/T 35276-2017 | 报文编码与使用规范 | SM2 加密签名消息语法与使用规范 | 不覆盖协议层 | 02、12 |
| 国密 TLS 套件 | RFC 8998 | TLS 1.3 密码套件 | SM2 签名 + AEAD_SM4_GCM / AEAD_SM4_CCM + SM3 | 是国际标准层唯一落点，但不保证车企已启用 | 02、12、16 |
| ECDSA/EC 公钥表示 | RFC 5480 | X.509 证书 | EC 公钥在证书中的表示 | 不约束曲线选择安全 | 02、12 |
| ECDSA/ECC 基础 | RFC 6090 | 椭圆曲线密码 | ECC/ECDSA 基础规范 | 不规定参数集 | 12 |
| RSA（PKCS #1） | RFC 8017 | 非对称加密/签名 | RSA 标准用法 | 与 ECC 并存但不是车端主流 | 12 |
| X.509 PKI | RFC 5280 | 证书与 CRL | 证书链、扩展、吊销列表 | 不保证 OCSP 可达性 | 02、11 |
| OCSP | RFC 6960 | 在线证书状态 | 实时吊销状态查询 | 不保证软失败策略正确 | 02、11 |
| 可信时间戳 | RFC 3161 | 时间基准 | 防重放的时间基准 | 不保证车端时钟同步 | 02、11、14 |
| ACME | RFC 8555 | 证书自动化 | 自动化签发/轮换（短周期证书的工程前提） | 不规定轮换灰度策略 | 02、11 |
| prime256v1（P-256） | Tesla 虚拟密钥文档 | 车端密钥曲线 | 车辆仅支持该曲线（Tesla 文档明载） | 不适用于其他车企（未取证） | 12、13、17 |
| SE 存数字钥匙密钥 | CCC Digital Key Release 3.0 | 手机/设备侧密钥载体 | 密钥存储于 Secure Element | 不保证车端撤销同步时延 | 11、14 |

**读表要点**：

1. **「提供的保证」与「不提供的保证」必须成对阅读**：例如 FIPS 140-3 只保证密码模块等级，不保证授权逻辑；TEE 只保证隔离，不保证抗物理提取。
2. **国密三件套（SM2/SM3/SM4）+ RFC 8998** 构成国产车云链路的规范基础，但**本次 9 家国内车企均未取得其采用的一手证据**（信源档案 §7.10 第 5 条），因此相关行只可作为「规范层能力」引用。
3. prime256v1 是表中**唯一由车企文档直接明载的曲线约束**，其余曲线/算法对车企而言均为规范层选项。

---

## 19.9 威胁-控制交叉索引

本表交叉引用章节 14 的威胁编号（§14.2 的 `T-01`…`T-24`，§14.5 的 `TH-01`…`TH-28`）与缓解控制。「控制所在章节」列指向控制的论述位置；「残余风险」列记录该控制在本次取证条件下的**未闭合部分**。「严重度」列沿用章节 14 §14.6 与审计计划 §3.3 的分类。

| 威胁 ID | 威胁名 | 缓解控制 | 控制所在章节 | 残余风险 | 严重度 |
|---|---|---|---|---|---|
| T-01 | 伪造 client_id/redirect_uri 骗取授权码 | 注册 redirect_uri 精确匹配；`state` 校验 | 11、14 | 子域接管未覆盖 | High |
| T-02 | 原生 App 内嵌 WebView 截获授权码 | RFC 8252 强制外部用户代理、禁内嵌 WebView | 11、14 | 车企移动端实现未知 | High |
| T-03 | 用被盗 client_secret 冒充应用后端 | 客户端凭证须保存在后端（Mercedes 明载） | 11、14 | 后端失陷即失效 | High |
| T-04 | 仿冒第三方云持被窃令牌调用 API | RFC 8705 mTLS / RFC 9449 DPoP；Tesla 虚拟密钥载荷签名 | 12、14 | 车企是否启用发送方约束未知 | High |
| T-05 | 数字钥匙 BLE/UWB 中继伪装在场 | CCC DK3.0 BLE+UWB 精确测距 | 11、14 | 车企实现与 CCC 版本未知 | High |
| T-06 | 篡改授权请求 scope 诱导过度授权 | 同意界面展示 scope 与 purpose URL；`require_requested_scopes=true` | 11、13、14 | 「全部 scope 才放行」可能降低授权率 | Medium |
| T-07 | 中间人篡改云端车控指令 | 虚拟密钥签名校验（车端验签）；TLS 1.3 | 12、14 | 依赖车端固件与公钥配对 | Critical/High |
| T-08 | 篡改 T-BOX 与车企云通信 | RFC 5280 证书链、RFC 6960 OCSP、TLS 1.3、RFC 8998 国密 | 02、11、14 | 车企启用情况未知 | High |
| T-09 | 篡改 .well-known 公钥文件 | 公钥须长期可用；私钥不入域名 | 12、14 | 公钥指纹固定机制未知 | High |
| T-10 | 篡改车机侧授权判定逻辑或缓存 | 无（本次未取到车机侧授权文档） | 14（CP-4） | 完全未取证领域 | 未找到公开来源 |
| T-11 | 第三方否认执行过车控操作 | 车主侧撤销端点（Tesla） | 12、14 | 授权决策日志内容未找到公开来源 | Low |
| T-12 | 内部服务否认代授权过某资源 | RFC 8693 令牌交换 `act`/`subject` 链 | 12、14 | 车企是否启用未知 | Low |
| T-13 | 授权码被截获后换码 | RFC 7636 PKCE；授权码一次性使用 | 11、12、14 | 车企是否强制 PKCE 未知 | High |
| T-14 | 访问令牌被复制后重放 | 短 TTL（Mercedes 3599 秒）；令牌绑定 RFC 8705 / 9449 | 12、14 | 绑定是否启用未知；Tesla TTL 未取证 | High |
| T-15 | 位置字段被推流给未授权应用 | `granular_access.hide_private=true` 双层控制（403） | 13、14 | 间接推断风险 | Informational（正面案例） |
| T-16 | vehicle_specs/pricing 被 Partner 无车主授权读取 | 该路径为授权控制例外；建议契约约束 + 逐次审计 | 13、14 | 无车主同意路径仍存在 | High |
| T-17 | 内部微服务越权读其他租户/全量数据 | 无（租户隔离文档未取证） | 14 | 不得推断为无隔离 | 未找到公开来源 |
| T-18 | 攻击者耗尽 API 限额致服务不可用 | 限流 60/3/30 次每分；同账号共享限额 | 13、14 | 共享限额放大单应用影响 | Medium |
| T-19 | 计费上限触发致 API 暂停且推流被移除不恢复 | 计费上限默认 0；80%/100% 邮件预警 | 13、14 | 无自动恢复 | Medium |
| T-20 | 车队规模下遥测缓冲耗尽 | 缓冲 5000 条；指数退避最大 30 秒 | 12、14 | 无持久队列 | Medium |
| T-21 | 数字钥匙三通道同时被干扰 | CCC DK3.0 保留 NFC 为强制备用 | 11、14 | 三通道同时失效场景 | Low |
| T-22 | 混淆代理：应用借更高权限越权 | RFC 8693 act/subject 链；RFC 9396 authorization_details | 12、13、14 | 车企是否采用未知 | High |
| T-23 | 内部服务被攻陷提升到签发任意令牌 | RFC 7523 客户端断言；RFC 9068 aud/iss/exp 校验 | 12、14 | 内部权限边界未知 | High |
| T-24 | 获取虚拟密钥私钥伪造任意车控指令 | 私钥不得托管域名；车端验签；密钥上限 <20 把 | 12、13、14 | 私钥是否受 HSM 保护未知 | Critical |
| TH-05 | 刷新令牌被窃且落在 24 小时宽限期内 | 一次性刷新 + 3 个月过期 + 24h 宽限 | 12、14 | 宽限期的安全窗口 | Medium |
| TH-06 | 并发刷新竞赛导致可用性抖动 | 宽限期用于覆盖持久化失败 | 12、14 | 应用侧串行化未规定 | Medium |
| TH-07 | 旧访问令牌在 scope 缩减后仍带旧能力 | 文档明载「仅对新签发访问令牌生效」 | 13、14 | Tesla TTL 未取证 | Medium |
| TH-15 | 数字钥匙撤销未在车端生效 | Tesla 虚拟密钥车端删除生效 | 12、14 | 数字钥匙撤销同步未知 | Medium |
| TH-16 | 云端混淆代理越权 | 强制令牌交换 + act/subject 审计 | 12、14 | 车企是否启用未知 | High |
| TH-17 | 服务账号凭证过宽可签发任意令牌 | 最小权限服务账号 + aud 强校验 | 12、14 | 内部权限边界未知 | High |
| TH-18 | 多租户越界（车队 A 读 B） | 租户维度强制隔离 + 审计 | 14 | 无公开证据 | Critical（若成立） |
| TH-19 | 授权服务器签名密钥泄露 | HSM + 密钥轮换 + 双人控制；SP 800-57 | 12、14 | 密钥保护与轮换未知 | Critical |
| TH-23 | 撤销后残留窗口（断连缓冲 + 重连语义） | scope 撤销 → 配置从车辆移除 | 12、14 | 时延未取证；重连是否重校验未知 | Medium（需验证） |
| TH-28 | 授权决策日志缺失导致不可追责 | 记录决策依据（谁/何 scope/何时/何策略） | 12、14 | 日志内容未找到公开来源 | Low |

**读表要点**：

1. 本表共 34 行，覆盖章节 14 中**全部 Critical 项**（T-24 / TH-18 / TH-19 及 T-07 相关的签名根）与多数 High 项。
2. **两行「未找到公开来源」**（T-10、T-17）代表本次**完全未取证的领域**（车机侧授权、云内租户隔离），不得反向解读为「无控制」。
3. 表中「残余风险」列的措辞刻意区分**「未知」与「缺失」**：绝大多数残余风险是「车企是否启用未知」，即披露缺口，而非控制缺失。

---

## 19.10 证据等级台账

### 19.10.1 统计表

下表按信源档案 §1–§6 的**规范类条目**逐条统计证据等级（口径：以信源档案中带方括号标注的独立条目为一条）。§7 的车企证据因条目结构为长 bullet 段落，单列定性说明。

| 等级 | 条目数（§1–§6） | 计数口径 | 说明 |
|---|---|---|---|
| `[A]` 一手 | 71 | 信源档案 §1.1–§6 中带 `[A]` 标注的独立条目 | 集中于国标全文公开系统、RFC Editor、NIST、GlobalPlatform、OAuth/OIDC 官方规范 |
| `[B]` 权威第三方 | 13 | 同上，带 `[B]` 标注者 | 含 SAE J3061、FIDO、ARM TrustZone、EVITA、CCC v1.1/FiRa 系列、TUF 官网、CycloneDX、in-toto |
| `[C]` 二手 | 7 | 同上，带 `[C]` 标注者 | 逐条列于 19.10.2 |
| `[未验证]` | 11 | 同上，带 `[未验证]` 标注者 | 逐条列于 19.10.2 |
| 未找到公开来源 | 1 | §4 中 SHE 规范 | 成员制规范，无一手 URL |
| `[合理推测]` | 0 | 信源档案自身不含推测条目 | 推测一律由各章正文显式标注，见 19.13 的「是否含推测成分」列 |

| 数据域 | 主要证据等级构成 | 定性说明 |
|---|---|---|
| §7.1 Tesla | [A] 为主，个别 [A/B]（Bugcrowd 合作）、[B]（赏金档位） | 全部来自 `developer.tesla.com` 与 Bugcrowd 官方页 |
| §7.2 Mercedes-Benz | [A] | 全部来自 `developer.mercedes-benz.com` |
| §7.3 VW/CARIAD | [A]，但为**公司自述营销口径** | 指标数字不可作为技术架构断言 |
| §7.4 BMW / §7.5 Rivian | [A，直接观测]（占位页/封锁/无 DNS） | 是**观测事实**，不是能力结论 |
| §7.6 BYD / §7.7 蔚来 / §7.8 小米 | [A] | 平台均为非车控平台 |
| §7.9 理想/小鹏/极氪/零跑/奇瑞/华为 | [A] 与「未找到公开来源」混合 | 开放平台入口缺失或拒绝服务 |
| §7.10 矛盾与不确定项 | 含 [C]（新浪汽车二手报道） | 不得单独立论 |

### 19.10.2 全部 `[C]` 与 `[未验证]` 条目及其使用限制

下表逐条列出信源档案中全部 `[C]` 与 `[未验证]` / 「未找到公开来源」条目。**使用限制**列为该条目在报告中允许的最强表述。

| # | 条目 | 等级 | 使用限制 |
|---|---|---|---|
| 1 | ISO/SAE 21434:2021《Road vehicles — Cybersecurity engineering》 | [未验证] | 编号与年份为通行共识，正文未取到；不得引用具体条款号 |
| 2 | ISO 24089:2023《Road vehicles — Software update engineering》 | [未验证] | iso.org Cloudflare 拦截；不得引用条款 |
| 3 | UN Regulation No.155（CSMS） | [未验证] | unece.org 全站拦截，URL 结构待复核；**不得给出强制时间表与审核要求** |
| 4 | UN Regulation No.156（SUMS） | [未验证] | 同上；不得给出条款编号 |
| 5 | GDPR Regulation (EU) 2016/679 | [C] | EUR-Lex 返回 202 异步状态，正文未取到；不得逐条引用 |
| 6 | EU Data Act Regulation (EU) 2023/2854 | [C] | HTTP 202，正文未取到；「车辆数据可携权」为通行认知 |
| 7 | SAE J3061 | [B] | HTTP 200，可作 21434 前身引用 |
| 8 | IEEE 1609.2（WAVE 安全服务/证书格式） | [C] | HTTP 200 但正文未解析；不得引条款 |
| 9 | 美国 SCMS（V2X 安全证书管理体系） | [未验证] | 未取得可核验官方 URL |
| 10 | UMA 2.0 | [未验证] | Kantara 站点 curl 超时；不得引机制细节 |
| 11 | NXP S32 汽车平台 | [未验证] | curl 超时；仅可陈述「站点存在」 |
| 12 | AUTOSAR Classic Platform（Crypto Stack/SecOC/IdsM） | [未验证] | autosar.org 超时；不得引规范条款 |
| 13 | TCG TPM 2.0 规范 | [未验证] | 站点 403/超时；不得引规范条款 |
| 14 | SHE（Secure Hardware Extension）规范 | 未找到公开一手 URL | 成员制规范；仅可作为「存在此类规范」的一般陈述 |
| 15 | IEEE 802.15.4z（UWB 物理层增强） | [未验证] | 未取得可核验官方 URL |
| 16 | ISO 15118-2 / -20（Plug & Charge） | [未验证] | iso.org 拦截，标准号需复核；不得引机制细节 |
| 17 | Infineon AURIX / TriCore | [C] | HTTP 202，型号页未解析；仅可陈述「站点存在」 |
| 18 | Renesas RH850 | [C] | 同上，仅可陈述「站点存在」 |
| 19 | TI Jacinto TDA4VM | [C] | 同上，仅可陈述「站点存在」 |
| 20 | SUIT Manifest 草案 draft-ietf-suit-manifest-27 | [C] | 草案；不得作为已发布标准引用 |
| 21 | 蔚来「UWB+蓝牙+NFC 三合一数字钥匙」（新浪汽车） | [C] | 二手报道；无法确认是否 CCC 3.0、是否有 SE 保护 |
| 22 | 小鹏 UWB 钥匙（论坛/短视频） | [C] | 官方未证实具体车型与安全实现 |
| 23 | 小鹏 `open.xiaopeng.com/dev/` 鉴权细节 | [A 站点存在，内容不可验证] | 全请求 403；不得陈述其鉴权机制 |
| 24 | 小鹏 `xmart.xiaopeng.com` | 未找到可验证公开来源 | 有 DNS（47.96.221.177）但证书无效（ERR_CERT_AUTHORITY_INVALID） |
| 25 | 极氪 `open.zeekrlife.com` | [A 站点存在，无可用信息] | HTTP 500 空页；不得陈述其能力 |
| 26 | 理想 `open.lixiang.com` / `developer.lixiang.com` | 未找到公开来源 | 均无 DNS |
| 27 | 零跑 `developer./dev./open.leapmotor.com` | 未找到公开来源 | 均无 DNS |
| 28 | 奇瑞 `developer.chery.cn` / `open.chery.cn` | 未找到公开来源 | 均无 DNS |
| 29 | 华为 Wallet Kit 数字车钥匙文档 | 未找到可验证公开来源 | JS 空壳页（1749 字节） |
| 30 | BMW `https://crd.bmwgroup.com/` / `https://b2b-developer.bmwgroup.com/` | [A，直接观测] | 前者无法解析、后者超时；仅记录观测事实 |
| 31 | Rivian `developer.rivian.com` | [A，直接观测] | 无 DNS 解析 |
| 32 | 蔚来隐私政策 `https://www.nio.cn/privacy-policy` | [A，JS 渲染，正文未取到] | 不得引其中条款 |
| 33 | VW/CARIAD 指标数字（45 million / 90 markets） | [A，公司自述口径] | 营销口径，不得作为技术架构断言 |
| 34 | Tesla 访问令牌 TTL | 未找到公开来源 | 仅已证实刷新令牌 3 个月 + 24h 宽限；TTL 待实测 |

**读表要点**：

1. 本表共 34 行 `[C]` / `[未验证]` / 「未找到公开来源」条目，**全部不得作为事实断言使用**。
2. 其中第 3–4 行（R155/R156）是**风险最高的一类**：它们是国际合规讨论的高频引用对象，但本次**完全无一手来源**，因此报告中凡涉及条款号、时间表、审核要求的表述一律禁止。
3. 第 23–32 行（国内车企 + BMW/Rivian 站点观测）**只能陈述观测事实**（403、无 DNS、占位页），**不得反向推断企业能力**（AC-11）。

---

## 19.11 缺口台账汇总

本表汇总信源档案 §8（覆盖度局限）、§7.10（矛盾与不确定项）与各已完成章节的「待补证清单」。缺口 ID 格式 `G-xx`。「优先级」判定口径：**高** = 直接影响授权章节核心结论；**中** = 影响某车企或某层的完整性；**低** = 影响背景信息完备度。

| 缺口 ID | 方向 | 已检索对象 | 结果 | 影响章节 | 补证动作 | 优先级 |
|---|---|---|---|---|---|---|
| G-01 | 国内 9 家车企车云通信安全（mTLS/国密） | 官网、开放平台、隐私政策、SRC 页 | 未找到公开一手来源 | 16 | 向车企发起 RFI / 采购安全白皮书 / 查专利与招标文件 | 高 |
| G-02 | 国内车企 TEE/SE/HSM 实现 | 开发者门户、安全页 | 未找到公开一手来源 | 16、02 | 器件选型逆向、T-BOX 拆解、芯片厂 Design Win 公告 | 高 |
| G-03 | 国内车企资源级（字段级）授权策略 | 开放平台文档 | 未找到公开来源 | 16、13 | RFI / 采购白皮书 / 沙箱申请 | 高 |
| G-04 | 国内车企同意界面设计（是否有 purpose URL 式知情同意） | 开发者文档 | 未找到公开来源 | 16、13 | 商务渠道获取接入文档截图 | 中 |
| G-05 | 小鹏开放平台鉴权与 scope 详情 | `open.xiaopeng.com` | HTTP 403 拒绝服务 | 16 | 商务渠道申请沙箱账号 | 高 |
| G-06 | 华为鸿蒙座舱安全与数字车钥匙 | `developer.huawei.com` 文档 | JS 空壳，正文不可取 | 16 | 用带 JS 渲染的抓取（须登录） | 高 |
| G-07 | BMW CarData / OAuth | `developer.bmwgroup.com` | 占位页「no content deployed」 | 17 | 换出口 IP 或代理后重跑 | 高 |
| G-08 | Rivian Fleet API | `rivian.com` / `developer.rivian.com` | CloudFront 区域封锁 | 17 | 换出口 IP | 高 |
| G-09 | VW/CARIAD 的 E3 架构、VW.OS、ID 系列 OTA 细节 | CARIAD 官网、VW Newsroom | 未取得技术文档（R155 站内检索零结果） | 17 | 采购白皮书 / 供应商资料 | 中 |
| G-10 | R155 / R156 条款与时间表 | unece.org | Cloudflare 拦截 | 17、16 | 恢复检索额度或用官方 PDF 直链 | 高 |
| G-11 | ISO 21434 正文 | iso.org | Cloudflare 拦截 | 02 | 通过标准购买渠道或 SAE 页面补 | 中 |
| G-12 | ISO 24089 正文 | iso.org | Cloudflare 拦截 | 02 | 同上 | 低 |
| G-13 | ISO 15118-2 / -20 正文 | iso.org | Cloudflare 拦截，标准号需复核 | 11 | 同上 | 低 |
| G-14 | Tesla 访问令牌 TTL | `developer.tesla.com` 已读页面 | 仅有刷新令牌 3 个月 + 24h 宽限 | 12、13 | 实机走一遍 token 响应读取 `expires_in` | 高 |
| G-15 | `enterprise_management` scope 的内部细粒度定义 | Tesla 文档 | 仅知其为企业管理能力 scope | 13、17 | 查 developer.tesla.com 企业管理文档 | 中 |
| G-16 | B 端企业授权与 C 端车主隐私偏好（如 `hide_private`）的优先级 | Tesla 文档 | 未找到公开说明 | 13 | 查 Tesla Fleet API 企业条款或向 Tesla 求证 | 中 |
| G-17 | 配额耗尽的恢复路径是否确实「不恢复」 | Tesla 文档 | 明载超限会移除配置且不恢复 [A]，但未载恢复流程 | 13、14 | 查 Tesla 支持文档或实际测试 | 中 |
| G-18 | UMA 2.0 规范正文 | Kantara 站点 | curl 超时 | 11 | 会员渠道获取规范正文 | 低 |
| G-19 | AUTOSAR Classic Platform 规范 | autosar.org | 超时 | 02、14 | 会员渠道获取 | 中 |
| G-20 | TCG TPM 2.0 规范 | trustedcomputinggroup.org | 403/超时 | 02 | 会员渠道获取 | 低 |
| G-21 | SHE 规范 | 厂商资料 | 成员制，未找到可核验公开一手 URL | 02 | 会员渠道获取 | 低 |
| G-22 | IEEE 802.15.4z 标准 | IEEE | 未取得可核验官方 URL | 11 | 通过 IEEE 标准渠道补齐 | 低 |
| G-23 | 美国 SCMS 体系 | — | 未取得可核验官方 URL | 11 | 检索 NHTSA / USDOT 官方页 | 低 |
| G-24 | IEEE 1609.2 正文 | standards.ieee.org | HTTP 200 但正文未解析 | 11 | 购买标准或从公开摘要补 | 低 |
| G-25 | 任何车企对 RFC 9396 RAR / RFC 9635 GNAP 的采用情况 | IETF 实现清单、授权服务器元数据 | 未找到公开来源 | 13、11 | 检索实现清单、查 `.well-known` 元数据 | 中 |
| G-26 | Mercedes 数字钥匙（CCC） | developer.mercedes-benz.com | 未取到 | 17、11 | 检索 Mercedes 数字钥匙公开资料 | 中 |
| G-27 | Mercedes mTLS / 证书固定 | developer.mercedes-benz.com | 未取到 | 17、02 | 检索开发者文档深度页 | 中 |
| G-28 | Mercedes TEE / 安全元件 | developer.mercedes-benz.com | 未取到 | 17、02 | 同上 | 中 |
| G-29 | Mercedes OTA 安全 | developer.mercedes-benz.com | 未取到 | 17 | 同上 | 中 |
| G-30 | Mercedes 2024–2025 车辆数据 API 政策文档 | developer.mercedes-benz.com | 未取到 | 17 | 检索平台政策页 | 中 |
| G-31 | MBition 与 Mercedes Pay 的车云授权角色 | 公开资料 | 未取到 | 17 | 检索子公司公开资料 | 低 |
| G-32 | 蔚来「UWB+蓝牙+NFC 三合一数字钥匙」真实性 | 蔚来官方 | 仅有二手报道（新浪汽车） | 16 | 蔚来官方技术说明或 RFI | 中 |
| G-33 | 小鹏 UWB 钥匙的具体车型与安全实现 | 小鹏官方 | 未证实 | 16 | RFI | 低 |
| G-34 | 比亚迪是否存在车控开放平台 | `open.byd.com` 全站 | i迪桥定位为企业级 ESB，**非车控平台**；未见 OAuth/数字钥匙 | 16 | RFI / 商务渠道 | 高 |
| G-35 | 小米汽车专属开放平台与车控 API | xiaomiev.com、iot.mi.com | 小米汽车官网无开发者入口 | 16 | RFI | 中 |
| G-36 | GDPR 正文与逐条适用性 | EUR-Lex | 202 异步状态，正文未取到 | 17 | 用 EUR-Lex 直链或官方 PDF | 中 |
| G-37 | EU Data Act 正文与逐条适用性 | EUR-Lex | HTTP 202，正文未取到 | 17 | 同上 | 中 |
| G-38 | 充电侧 OCPP / ISO 15118 的授权细节 | Open Charge Alliance、iso.org | OCPP 页 [A]；ISO 15118 未验证 | 11 | 补 ISO 15118 正文 | 低 |
| G-39 | 车企授权决策日志内容（谁/何 scope/何时/何策略） | 各车企文档 | 未找到公开来源 | 12、14 | RFI / 采购审计材料模板 | 中 |
| G-40 | 车企云内部多租户隔离实现 | 各车企文档 | 未找到公开来源 | 14 | RFI / 采购安全白皮书 | 中 |
| G-41 | 车机侧授权判定（CP-4） | 各车企文档 | 完全空缺 | 14、12 | RFI / 车机系统拆解研究 | 中 |
| G-42 | 数字钥匙撤销在车端的同步时延 | 各车企文档 | 未取证 | 14、12 | RFI / 实测 | 中 |
| G-43 | 车企 OTA 签名角色配置（TUF 阈值/quorum 设置） | 各车企文档 | 未取证 | 02、14 | RFI / 采购白皮书 | 中 |
| G-44 | 车企 SLSA 构建等级 | 各车企文档 | 未取证 | 02 | RG 采购 / 供应链问卷 | 低 |
| G-45 | 车企 SBOM 交付格式与频率 | 各车企文档 | 未取证 | 02 | 合同条款核查 | 低 |
| G-46 | 数字钥匙撤销与 Fleet Telemetry 配置回收的时延一致性 | Tesla 文档 | scope 撤销 → 配置从车辆移除 [A]，但时延未载 | 14、13 | 实测 / Tesla 支持文档 | 中 |

**读表要点**：

1. 本表共 46 个缺口，其中**优先级高者 10 个**（G-01、G-02、G-03、G-05、G-06、G-07、G-08、G-10、G-14、G-34——含授权核心结论的取证缺口）。
2. 每一条缺口都**只陈述「未找到公开来源」，不陈述「不具备能力」**（AC-11）。
3. 补证动作分为四类：**换出口 IP / 代理重跑**（区域封锁类）、**商务渠道 / RFI**（未公开类）、**会员渠道**（成员制规范类）、**实测**（可复现验证类）。

---

## 19.12 术语与缩写表

| 缩写/术语 | 全称 | 中文 | 一句话说明 | 首次出现章节 |
|---|---|---|---|---|
| OAuth 2.0 | Open Authorization 2.0 | 开放授权 2.0 | 第三方应用代表用户访问资源的授权框架（RFC 6749） | 11 |
| OAuth 2.1 | OAuth 2.1（草案） | — | 强制 PKCE、废弃隐式流与密码模式的演进版 | 11 |
| OIDC | OpenID Connect | 开放身份连接 | 在 OAuth 2.0 之上的身份认证层（id_token） | 11 |
| PKCE | Proof Key for Code Exchange | 授权码交换证明密钥 | 防授权码拦截的公共客户端强制机制（RFC 7636） | 11 |
| mTLS | mutual TLS | 双向 TLS | 客户端与服务器互验证书的链路认证 | 02 |
| DPoP | Demonstrating Proof of Possession | 拥有证明 | 用 JWK 指纹把令牌绑定到发送方的机制（RFC 9449） | 11 |
| RAR | Rich Authorization Requests | 富授权请求 | 用结构化 authorization_details 替代裸 scope（RFC 9396） | 11 |
| GNAP | Grant Negotiation and Authorization Protocol | 授权协商协议 | 细粒度 + 可协商的下一代授权协议（RFC 9635） | 11 |
| JWT | JSON Web Token | JSON 网络令牌 | 自包含的令牌格式；RFC 9068 定义访问令牌 profile | 12 |
| Bearer Token | — | 持有者令牌 | 持有即可使用的令牌（RFC 6750） | 11 |
| Token Introspection | — | 令牌内省 | 实时校验不透明令牌状态（RFC 7662） | 12 |
| Token Exchange | — | 令牌交换 | 用 subject/actor 表达代授权链（RFC 8693） | 11 |
| Refresh Token | — | 刷新令牌 | 换取新访问令牌的长效凭证 | 12 |
| Token Rotation | — | 令牌轮换 | 每次刷新签发新刷新令牌、旧令牌失效 | 12 |
| Grace Period | — | 宽限期 | 轮换后旧令牌仍可用的时间窗（Tesla 24 小时） | 12 |
| Scope | — | 授权范围 | 授权请求中声明的权限集合 | 11 |
| Consent | — | 同意 | 资源所有者对授权请求的批准行为 | 13 |
| Granular Access | — | 粒度化访问 | Tesla 的资源级收窄机制（hide_private） | 13 |
| Virtual Key | — | 虚拟密钥 | 车端验签用的公私钥对 | 12 |
| Partner Token | — | 合作伙伴令牌 | Tesla 面向 B 端、部分能力无需车主授权的令牌 | 13 |
| third-party token | — | 第三方令牌 | Tesla 代表车主行事的令牌 | 13 |
| TEE | Trusted Execution Environment | 可信执行环境 | 与 REE 隔离的安全执行环境 | 02 |
| SE | Secure Element | 安全元件 | 独立安全芯片，数字钥匙密钥的存储载体 | 02 |
| HSM | Hardware Security Module | 硬件安全模块 | 密码运算与密钥托管的专用硬件 | 02 |
| TPM | Trusted Platform Module | 可信平台模块 | 平台度量与绑定密钥模块（TCG 规范） | 02 |
| SHE | Secure Hardware Extension | 安全硬件扩展 | 车载安全硬件扩展规范（成员制） | 02 |
| EVITA | E-safety Vehicle Intrusion Protected Applications | 车载入侵防护应用项目 | 定义车载 HSM Full/Medium/Light 三级分级 | 02 |
| OP-TEE | Open Portable TEE | 开源可移植 TEE | TrustZone 之上的开源 TEE 实现 | 02 |
| TrustZone | ARM TrustZone | ARM 可信区 | ARM 的硬件安全/非安全世界隔离技术 | 02 |
| SM2 | ShangMi 2 | 国密椭圆曲线公钥算法 | 国密公钥算法（GB/T 32918） | 02 |
| SM3 | ShangMi 3 | 国密杂凑算法 | 国密杂凑算法（GB/T 32905） | 02 |
| SM4 | ShangMi 4 | 国密分组密码 | 国密对称算法（GB/T 32907） | 02 |
| ECDSA | Elliptic Curve Digital Signature Algorithm | 椭圆曲线数字签名算法 | 车端签名的主流算法族 | 12 |
| ECC | Elliptic Curve Cryptography | 椭圆曲线密码 | 公钥密码体制 | 12 |
| AEAD | Authenticated Encryption with Associated Data | 带关联数据的认证加密 | 同时提供机密性与完整性 | 02 |
| GCM | Galois/Counter Mode | 伽罗瓦/计数器模式 | AEAD 的一种模式（SP 800-38D） | 02 |
| PKI | Public Key Infrastructure | 公钥基础设施 | 证书签发与信任链体系 | 02 |
| X.509 | — | X.509 证书 | 公钥证书格式标准（RFC 5280） | 02 |
| CRL | Certificate Revocation List | 证书吊销列表 | 批量吊销清单 | 02 |
| OCSP | Online Certificate Status Protocol | 在线证书状态协议 | 实时吊销查询（RFC 6960） | 02 |
| ACME | Automatic Certificate Management Environment | 自动化证书管理环境 | 证书自动签发/轮换（RFC 8555） | 02 |
| TLS 1.3 | Transport Layer Security 1.3 | 传输层安全 1.3 | 车云链路通信加密协议（RFC 8446） | 02 |
| 0-RTT | Zero Round Trip Time | 零往返 | TLS 1.3 的快速重连（可重放风险） | 02 |
| TUF | The Update Framework | 更新框架 | 阈值签名 + 四角色防仓库/密钥泄露 | 02 |
| Uptane | — | Uptane | 面向汽车的更新安全框架（Director + Image 双仓库） | 02 |
| Director Repository | — | 导演仓库 | Uptane 中面向车辆定向的元数据仓库 | 02 |
| Image Repository | — | 镜像仓库 | Uptane 中面向镜像的元数据仓库 | 02 |
| SUIT | Software Updates for Internet of Things | 物联网固件更新 | IETF 的固件更新标准（RFC 9019/9124） | 02 |
| SBOM | Software Bill of Materials | 软件物料清单 | 供应链成分清单（SPDX / CycloneDX） | 02 |
| SPDX | Software Package Data Exchange | 软件包数据交换 | SBOM 开放标准（对应 ISO/IEC 5962:2021） | 02 |
| CycloneDX | — | CycloneDX | SBOM 开放标准 | 02 |
| SLSA | Supply-chain Levels for Software Artifacts | 供应链等级 | 构建完整性分级 L0–L3 | 02 |
| in-toto | — | in-toto | 供应链完整性元数据与签名链 | 02 |
| SecOC | Secure Onboard Communication | 车载安全通信 | AUTOSAR 的车内报文认证机制 | 02 |
| IdsM | Intrusion Detection System Manager | 入侵检测系统管理器 | AUTOSAR 的入侵检测管理组件 | 02 |
| Crypto Stack | — | 密码栈 | AUTOSAR 的密码服务层 | 02 |
| CCC | Car Connectivity Consortium | 车联网联盟 | 数字钥匙规范制定者（Digital Key Release 3.0） | 11 |
| FiRa | FiRa Consortium | FiRa 联盟 | UWB 技术规范与认证制定者 | 11 |
| UWB | Ultra-Wideband | 超宽带 | 精确测距的近场技术（抗中继） | 11 |
| BLE | Bluetooth Low Energy | 低功耗蓝牙 | 近场通信通道 | 11 |
| NFC | Near Field Communication | 近场通信 | 数字钥匙的强制备用通道 | 11 |
| C-V2X | Cellular V2X | 蜂窝车联网 | 车-车/车-路通信（GB/T 45112 证书体系） | 11 |
| V2X | Vehicle-to-Everything | 车联万物 | 车辆与外部通信的统称 | 11 |
| SCMS | Security Credential Management System | 安全凭证管理系统 | V2X 证书管理体系（美国方案，未取证） | 11 |
| OTA | Over-the-Air | 空中下载 | 车辆软件的远程升级 | 02 |
| Plug & Charge | — | 即插即充 | ISO 15118 的充电授权模型（TLS + contract certificate） | 11 |
| OCPP | Open Charge Point Protocol | 开放充电点协议 | 充电侧协议族，含授权与计量 | 11 |
| GDPR | General Data Protection Regulation | 通用数据保护条例 | 欧盟数据保护法规 | 17 |
| Purpose URL | — | 用途链接 | Mercedes 同意界面展示的目的说明链接 | 17 |
| ESB | Enterprise Service Bus | 企业服务总线 | 企业级 API 网关（BYD i迪桥定位） | 16 |
| API Key | — | API 密钥 | 以 appKey 为代表的网关鉴权凭证 | 16 |
| app-id / secret | — | 应用 ID 与密钥 | 蔚来 Open NSC 的双凭证鉴权 | 16 |
| RBAC | Role-Based Access Control | 基于角色的访问控制 | 以角色为中心的授权模型 | 13 |
| ABAC | Attribute-Based Access Control | 基于属性的访问控制 | 以属性（含资源、环境）为中心的授权模型 | 13 |
| ReBAC | Relationship-Based Access Control | 基于关系的访问控制 | 以主体-资源关系为中心的授权模型 | 13 |
| Confused Deputy | — | 混淆代理 | 高权限中间方被诱导越权 | 14 |
| STRIDE | Spoofing/Tampering/Repudiation/Information Disclosure/DoS/Elevation | 威胁分类法 | 六类威胁枚举框架 | 14 |
| CP | Control Point | 控制点 | 章节 14 定义的 9 个信任边界控制点 | 14 |
| Blast Radius | — | 影响范围 | 单一凭证失陷的横向影响面积 | 13 |
| Secretless / Least Privilege | — | 最小权限 | 仅授予完成任务所必需的权限 | 13 |
| RFI | Request for Information | 信息征询 | 向车企索证的标准动作 | 19 |
| AC | Acceptance Criteria | 验收标准 | 审计计划 §1 冻结的 12 条验收标准 | 00 |
| WF | Workflow | 工作流 | 审计计划 §2 的 7 条工作流 | 00 |
| CSO | Chief Security Officer | 首席安全官 | 本委托终审签署人 | 00 |

**读表要点**：本表共收录 84 条术语/缩写，「首次出现章节」列指向本报告中该术语的首个实质使用位置（`00` 表示审计计划）。术语的**定义均为一句话**，深度解释见对应章节正文，本章不重复。

---

## 19.13 关键结论索引

本表把散落在各章小结中的**核心结论**索引为可检索条目。结论 ID 格式 `K-xx`。「是否含推测成分」列严格区分事实层结论与判断层结论（对齐 AC-8 与审计计划 §3.2）。「置信度」判定口径：**高** = 全部依赖 `[A]` 一手事实；**中** = 依赖规范推理或存在取证边界；**低** = 主要依赖二手来源。

| 结论 ID | 结论一句话 | 事实依据章节 | 是否含推测成分 | 置信度 |
|---|---|---|---|---|
| K-01 | OAuth 2.0 授权码流是车云第三方授权的通行底座（Tesla、Mercedes 文档均明载） | 11、13、17 | 否 | 高 |
| K-02 | 「刷新令牌一次性 + 轮换」是公开证据中最强的令牌生命周期约束（Tesla 3 个月 + 24h 宽限；Mercedes 一次性） | 12、13 | 否 | 高 |
| K-03 | Tesla Fleet API 是公开文档中最完整的车云第三方授权实现范例 | 13、17 | 否 | 高 |
| K-04 | Mercedes 采用 `mb:` 三段式命名空间 scope，粒度可细到单资源 | 13、17 | 否 | 高 |
| K-05 | 资源级（字段级）策略的公开证据本次仅 Tesla 一家（`hide_private` 403） | 13、17 | 否（但「其他车企没有」不可推断） | 中 |
| K-06 | 发送方约束令牌（RFC 8705/9449）是规范层的关键对策 | 12、11 | 是（车企启用情况为推测） | 中 |
| K-07 | 虚拟密钥把授权校验下沉到车端，是车云特有能力（Tesla 文档明载） | 12、13、17 | 否 | 高 |
| K-08 | `vehicle_specs` / `vehicle_pricing_info` 仅 Partner Token 且无需车主授权，构成授权控制例外（High） | 13、14、17 | 否 | 高 |
| K-09 | 国内车企公开授权模型证据集中于非车控平台（BYD ESB、蔚来服务云、小米 IoT） | 13、16 | 否 | 高 |
| K-10 | 不得把国内车企车云授权归纳为「APIKey 模型」 | 13、16、17 | 否（纪律陈述） | 高 |
| K-11 | 9 家国内车企未取得国密 / mTLS / 证书轮换 / HSM 的任何官方一手来源 | 16 | 否 | 高 |
| K-12 | GB 44495 / 44496 于 2026-01-01 起对新车型强制适用，是中国车云合规基线 | 16、02 | 否 | 高 |
| K-13 | GB/T 47324-2026 直接命中车联网云平台侧防护，2026-10-01 实施 | 16 | 否 | 高 |
| K-14 | GB/T 47467-2026 是接口层规范，与授权/访问控制的 API 治理直接相关 | 16 | 否 | 高 |
| K-15 | 国密在 TLS 1.3 国际标准层的唯一落点是 RFC 8998 | 02、12 | 否 | 高 |
| K-16 | 数字钥匙近场三通道由 CCC DK3.0 定义，NFC 强制备用，密钥存于 SE | 11、14 | 否 | 高 |
| K-17 | Tesla 的计费-限流机制使配额耗尽成为可被攻击者触发的可用性事件 | 13、14、17 | 是（前置条件为推测） | 中 |
| K-18 | 授权决策日志与云内租户隔离构成本次全局可观测性缺口 | 12、14 | 否（缺口陈述） | 高 |
| K-19 | R155/R156 的具体条款、时间表、审核要求本次无一手来源 | 17、16 | 否 | 高 |
| K-20 | 规范层存在 RSA/ECC 与 SM 双轨（RFC 8017/5480/6090 ↔ GB/T 32918/32905/32907 + RFC 8998） | 02、12 | 否 | 高 |
| K-21 | 密钥数量上限（<20 把）与推流上限（≤5）是「影响范围控制」的工程手段 | 13、14、17 | 否 | 高 |
| K-22 | 国际 OTA 安全的主参照是 Uptane 2.1.0 双仓库与 TUF 四角色阈值签名 | 02 | 否 | 高 |
| K-23 | 车云授权模型应以 ABAC + ReBAC 为主、RBAC 为辅 | 13 | 是（选型判断） | 中 |
| K-24 | BMW 与 Rivian 属「披露缺口」而非「能力缺口」 | 17 | 否 | 高 |
| K-25 | 本次调研因检索工具额度耗尽无开放网络发现能力，覆盖度向文档公开可达的企业倾斜 | 00 §8、信源档案 §0 | 否 | 高 |
| K-26 | 蔚来「UWB+蓝牙+NFC 三合一数字钥匙」仅有二手报道，无法确认是否 CCC 3.0 / 有 SE 保护 | 16 | 是（真实性待证） | 低 |

**读表要点**：

1. 本表共 26 条结论，其中**含推测成分 4 条**（K-06、K-17、K-23、K-26），**其余 22 条为事实层或缺口层陈述**。
2. **置信度高者 18 条**，全部可回溯至 `[A]` 一手条目；**置信度中者 7 条**（K-05、K-06、K-17、K-23 及规范推理类）；**置信度低者 1 条**（K-26，依赖二手报道）。
3. 凡「含推测成分 = 是」的结论，在报告正文中一律以「本报告判断」措辞出现，**不得写成陈述句事实**（对齐审计计划 §3.2 红线第 1 条）。

---

## 19.14 报告章节地图

本表把审计计划 §6.1 定义的全部文件与它们覆盖的验收标准（AC-1…AC-12）对应起来。「状态」列的取值：**已完稿** = 本章写作时文件已存在于 `docs/` 且含实质内容；**规划中** = 审计计划已定义但本章写作时尚未完稿。

| 文件 | 标题/主题 | 归属工作流 | 覆盖 AC | 状态 |
|---|---|---|---|---|
| `README.md` | 索引：章节、AC 对照、证据分级、覆盖度 | WF-0 | AC-1、AC-7、AC-9 | 规划中 |
| `docs/00-engagement-plan.md` | 审计计划与方法论 | WF-0 | AC-1、AC-6、AC-8、AC-11 | 已完稿 |
| `docs/01-overview.md` | 概述 | WF-0 | AC-1、AC-12 | 规划中 |
| `docs/02-general-layered-security.md` | 通用车云安全技术方案（分层解构） | WF-1 | AC-3、AC-7、AC-12 | 已完稿 |
| `docs/10-authz-00-intro.md` | 授权与访问控制 · 总论 | WF-2 | AC-2、AC-3、AC-7、AC-12 | 规划中 |
| `docs/11-authz-10-protocols.md` | 授权与访问控制 · 协议族与消息流程 | WF-2 | AC-2、AC-3、AC-7、AC-12 | 已完稿 |
| `docs/12-authz-20-tokens-keys.md` | 授权与访问控制 · 令牌与密钥治理 | WF-2 | AC-2、AC-3、AC-7、AC-12 | 已完稿 |
| `docs/13-authz-30-resource-authz.md` | 授权与访问控制 · 资源级授权 | WF-2 | AC-2、AC-3、AC-7、AC-12 | 已完稿 |
| `docs/14-authz-40-threat-model.md` | 授权与访问控制 · 威胁模型与攻击面 | WF-3 | AC-2、AC-7、AC-12 | 已完稿 |
| `docs/15-authz-50-engineering.md` | 授权与访问控制 · 工程实现 | WF-3 | AC-2、AC-7、AC-12 | 规划中 |
| `docs/16-authz-60-cn-oem.md` | 授权与访问控制 · 国内车企实践（9 家） | WF-4 | AC-2、AC-4、AC-7、AC-8、AC-11、AC-12 | 已完稿 |
| `docs/17-authz-70-global-oem.md` | 授权与访问控制 · 国际车企实践（5 家） | WF-5 | AC-2、AC-5、AC-7、AC-11 | 已完稿 |
| `docs/18-authz-80-compliance-audit.md` | 授权与访问控制 · 合规映射与审计 | WF-6 | AC-2、AC-7、AC-8 | 规划中 |
| `docs/19-authz-90-reference-tables.md` | 授权与访问控制 · 参考表与索引（本文件） | WF-6 | AC-2、AC-7、AC-8 | 已完稿（本文件） |
| `docs/20-cn-oem-security.md` | 国内车企应用与平台安全 | WF-4 | AC-3、AC-4、AC-7、AC-11 | 规划中 |
| `docs/21-global-oem-security.md` | 国际车企应用与平台安全 | WF-5 | AC-3、AC-5、AC-7、AC-11 | 规划中 |
| `docs/30-comparison.md` | 对比与差异分析 | WF-0 | AC-1、AC-6、AC-11 | 规划中 |
| `docs/31-summary-trends.md` | 总结与趋势 | WF-0 | AC-1、AC-6、AC-12 | 规划中 |
| `docs/90-references.md` | 参考资料 | WF-0 | AC-7 | 规划中 |
| `docs/sources/source-dossier.md` | 信源档案（唯一事实底座） | WF-0 | AC-7、AC-8 | 已完稿（持续就地追加） |
| `docs/html/*.html` | CARIAD 风格 HTML（每个 md 对应一个） | 全工作流 | AC-9、AC-10 | 逐文件生成 |
| `scripts/md2cariad.py` | 确定性 MD→CARIAD HTML 转换器 | WF-0 | AC-10 | 规划中 |

### 19.14.1 AC 覆盖反查表

| AC | 判定要求 | 主要承载文件 | 本章贡献 |
|---|---|---|---|
| AC-1 | 报告含 6 个规定结构 | 01 / 02 / 16 / 17 / 30 / 31 | 本章 §19.14 提供文件级索引与状态 |
| AC-2 | 授权章节 ≥300K 字符 | 10–19 共 10 个文件 | 本章自身为配额 35K 的组成部分 |
| AC-3 | 覆盖 5 层分析框架 | 02（各层）、11–17 | 本章 §19.8 覆盖硬件与密码层，19.2 覆盖全层规范 |
| AC-4 | 国内 ≥9 家逐家拆解 | 16、20 | 本章 §19.4、§19.11 索引国内车企证据与缺口 |
| AC-5 | 国际 ≥5 家逐家拆解 | 17、21 | 本章 §19.4、§19.5 索引国际车企证据与参数 |
| AC-6 | 国内外技术路线差异对比 | 30、00 | 本章 §19.13 索引对比类结论（K-09 等） |
| AC-7 | 信源可靠并标注等级 + URL | 全部 | 本章 §19.2/§19.4/§19.10 为等级与 URL 审计入口 |
| AC-8 | 区分公开信息与合理推测 | 14、18、本章 | 本章 §19.10/§19.11/§19.13 为推测与缺口的集中台账 |
| AC-9 | 输出 MD 与 HTML 两种格式 | 全部 `docs/*.md` | 本章 HTML 由 `md2cariad.py` 确定性生成 |
| AC-10 | HTML 为 CARIAD 风格 | 全部 HTML | 由脚本保证；本章不手写 HTML |
| AC-11 | 客观中立，不夸大不贬低 | 全部 | 本章 §19.1.2/§19.10/§19.11 反复声明「未找到公开来源 ≠ 能力缺失」 |
| AC-12 | 技术深度与可读性并重 | 全部 | 本章由 14 张结构化表构成，满足「含对照表」要求 |

**地图读法**：

1. **第 3 部分（授权与访问控制）的完整文件集为 10–19 共 10 个文件**，本章为其中末位（90 号），承担汇总与索引职能。
2. 本章写作时已完稿的文件为：`00`、`02`、`11`、`12`、`13`、`14`、`16`、`17`、`19`、`sources/source-dossier.md`。其余标记为「规划中」，其覆盖的 AC 由审计计划 §2 的工作流派工单保证。
3. **AC-2 的对账**必须在全部 10 个文件完稿后进行（审计计划 §5 的 G5 门）；本章作为其中之一，按配额提供 35K 字符。

---

## 19.15 本章小结

**本章做了什么**：把第 2 章与第 3 部分各章散落的**已取证事实**，重新结构化为 14 张可查询的表——规范索引（103 条）、协议速查（22 条）、端点凭证清单（47 行）、令牌密钥参数（37 行）、scope 对照（17 行）、国标时间线（21 行）、硬件密码基元（29 行）、威胁控制交叉索引（34 行）、证据等级台账（统计 + 34 条受限条目）、缺口台账（46 条）、术语表（84 条）、结论索引（26 条）、章节地图（22 行）。

**本章未做什么**：不重新论证任何议题；不新增任何 URL、标准号、日期、数字；不为凑体量重复正文内容。所有体量均来自真实的对照表与索引条目。

**三条使用纪律（再次强调）**：

1. 凡 `[C]` / `[未验证]` / 「未找到公开来源」条目，**一律不得作为事实断言使用**（见 19.10.2）。
2. 凡出现在 19.11 的缺口，**只陈述「未找到公开来源」，不陈述「不具备能力」**（AC-11）。
3. 凡在 19.13 标注「含推测成分 = 是」的结论，在报告正文中**必须以「本报告判断」措辞出现**（审计计划 §3.2 红线第 1 条）。

*（本章完。文件：`docs/19-authz-90-reference-tables.md`；工作流：WF-6；覆盖 AC-2 / AC-7 / AC-8。）*
