# 车云安全技术方案调研 — 信源档案（Source Dossier）

> 本文件是 TRA-1 全部写作工作流（§3 授权与访问控制、§2 通用分层方案、§4/§5 车企实践）的**唯一事实底座**。
> 规则：任何写入报告的断言，必须能在本文件中找到对应条目或明确标注为「合理推测 / 未找到公开来源」。
> 禁止新增未经检索证实的 URL 或数字。发现新来源时，**就地追加到本文件**，不另建文件。

## 0. 采集方法与局限（必读，影响全部结论的可信度断言）

- 采集日期：2026-09-28。执行方式：`terminal + curl` 与 `browser_navigate/browser_console` 直连权威站点取证。
- **检索工具不可用**：`web_search` / `web_extract` 全程返回 `Insufficient credits`（Firecrawl 402/429），额度耗尽且不自动恢复。因此本次调研**无法做开放网络发现**，只能"直取已知权威 URL"。
- 公开搜索引擎在本运行环境同样不可用：Bing 被地理重定向至 cn.bing.com 且对中文品牌词返回噪声结果；Baidu / Sogou / 360 触发验证码；Google 返回 `/sorry` 机器人墙或空结果；DuckDuckGo 验证码。
- 区域/网络封锁：`bmw.com` / `bmwgroup.com` / `rivian.com` 被 Akamai/CloudFront 区域封锁（HTTP 000 / 403）；`unece.org`、`iso.org`、`autosar.org`、`trustedcomputinggroup.org` 被 Cloudflare 或超时拦截；`open.xiaopeng.com` 对所有请求返回 403（openresty）。
- **覆盖度偏置**：证据密度向"文档公开可达"的企业倾斜（Tesla、Mercedes-Benz 证据最厚），对文档未公开的企业（BMW、Rivian、小鹏、极氪、零跑、理想、华为、奇瑞）证据薄弱。**「未找到公开来源」= 本次披露缺口，绝不等于能力缺口**，不得反向推断为"该企业没有该能力"。
- 凡标 `[未验证]` 者，URL 结构或站点可达性已确认但正文未取到，交付前须复核；不得作为事实断言使用。

---

## 1. 法规与标准（中国）

### 1.1 强制性国家标准（GB，A 级：国家标准全文公开系统一手）

- GB 44495-2024《汽车整车信息安全技术要求》—— 发布 2024-08-23，实施 2026-01-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=2DB552CAA58F589705C3DC7AD47AC2AB —— [A]
- GB 44496-2024《汽车软件升级通用技术要求》—— 发布 2024-08-23，实施 2026-01-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=8BC0D8B44DD4E71F9557BADE5175565A —— [A]
- GB 44495 / GB 44496 属**强制性**国标（"现行"状态），是中国车云与 OTA 安全的合规基线，2026-01-01 起对新车型强制适用。

### 1.2 推荐性国家标准（GB/T，A 级）

- GB/T 40855-2021《电动汽车远程服务与管理系统信息安全技术要求及试验方法》—— 发布 2021-10-11，实施 2022-05-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=AC47DD65376598FB44E0F24FBEBBF769 —— [A]
- GB/T 40856-2021《车载信息交互系统信息安全技术要求及试验方法》—— 发布 2021-10-11，实施 2022-05-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=9995D55CBCAE667570C36F6A6CD1712D —— [A]
- GB/T 40857-2021《汽车网关信息安全技术要求及试验方法》—— 发布 2021-10-11，实施 2022-05-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=2977F0AC1719BBEFB9649C0146B0FC55 —— [A]
- GB/T 38628-2020《信息安全技术 汽车电子系统网络安全指南》—— 发布 2020-04-28，实施 2020-11-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=59F8899E944C9ED52288FE5E0146C621 —— [A]
- GB/T 41871-2022《信息安全技术 汽车数据处理安全要求》—— 发布 2022-10-14，实施 2023-05-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=4D3C5BB193E079AD54294E5845749B8F —— [A]
- GB/T 44464-2024《汽车数据通用要求》—— 发布/实施 2024-08-23 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=D63AAC0203E9B169F74B10E547A3CBCE —— [A]
- GB/T 45112-2024《基于 LTE 的车联网无线通信技术 安全证书管理系统技术要求》—— 发布 2024-12-31，实施 2025-04-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=FB30FC033090F346D1B53E892DCD23BB —— [A]（中国 C-V2X 证书管理体系，是"车-云-车"证书体系的国家级规范）
- GB/T 45181-2024《车联网网络安全异常行为检测机制》—— 发布 2024-12-31，实施 2025-04-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=29740120554AA4DCB87A8FEAE106BA43 —— [A]
- GB/T 47324-2026《车联网平台网络安全防护要求》—— 发布 2026-03-31，实施 2026-10-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=90F36FFBED2E85627B648B837A522527 —— [A]（**直接命中本报告主题：车联网云平台侧的防护要求**）
- GB/T 47325-2026《车联网在线升级安全技术要求与测试方法》—— 发布 2026-03-31，实施 2026-10-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=8407225889D602060265D0ABB8D14AA7 —— [A]
- GB/T 47467-2026《车联网安全管理接口规范》—— 发布 2026-04-30，实施 2026-11-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=AC95A675E7B6E8E822E66B30BE14ED5C —— [A]（**接口层规范，与授权/访问控制的 API 治理直接相关**）
- GB/T 44402.1-2024《卡及身份识别安全设备 数字钥匙系统 第 1 部分：参考架构》—— 发布 2024-08-23，实施 2025-03-01 —— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=9CDE5F17C28F5332BA9CBEDD4618FD77 —— [A]（中国数字钥匙授权模型的国标参考架构）
- GB/T 32918.1~.5-2016/2017《SM2 椭圆曲线公钥密码算法（总则/数字签名/密钥交换/公钥加密/参数定义）》—— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=3EE2FD47B962578070541ED468497C5B 等 —— [A]
- GB/T 32905-2016《SM3 密码杂凑算法》—— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=45B1A67F20F3BF339211C391E9278F5E —— [A]
- GB/T 32907-2016《SM4 分组密码算法》—— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=7803DE42D3BC5E80B0C3E5D8E873D56A —— [A]
- GB/T 35275-2017《SM2 密码算法加密签名消息语法规范》—— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=A7B91213CC4862B31BE2C84665CB8F7E —— [A]
- GB/T 35276-2017《SM2 密码算法使用规范》—— https://openstd.samr.gov.cn/bzgk/gb/newGbInfo?hcno=2127A9F19CB5D7F20D17D334ECA63EE5 —— [A]

### 1.3 行政法规与部门规章（A 级）

- 《汽车数据安全管理若干规定（试行）》（网信办等五部门令第 7 号）—— 2021-08-16 成文，2021-10-01 施行，规定重要数据目录、境内存储、年度报送、出境评估等义务 —— https://www.gov.cn/zhengce/zhengceku/2021-09/12/content_5640023.htm —— [A]
- 同上，答记者问 —— http://www.gov.cn/zhengce/2021-08/20/content_5632437.htm —— [A]

### 1.4 国际标准与法规（覆盖度受限）

- ISO/SAE 21434:2021《Road vehicles — Cybersecurity engineering》—— SAE 收录页 https://www.sae.org/standards/content/iso21434/ ，ISO 官方页 https://www.iso.org/standard/70918.html 被 Cloudflare 拦截 —— [未验证：编号与年份为通行共识，正文未取到]
- SAE J3061《Cybersecurity Guidebook for Cyber-Physical Vehicle Systems》（21434 前身）—— https://www.sae.org/standards/j3061_201601-cybersecurity-guidebook-cyber-physical-vehicle-systems/ —— [B：HTTP 200]
- ISO 24089:2023《Road vehicles — Software update engineering》—— https://www.iso.org/standard/77796.html —— [未验证：iso.org Cloudflare 拦截]
- UN Regulation No.155（CSMS 网络安全管理体系）与 No.156（SUMS 软件更新管理体系）—— https://unece.org/transport/vehicle-regulations/wp29/grva —— [未验证：unece.org 被 Cloudflare 全站拦截，URL 结构需复核]
- 欧盟 GDPR Regulation (EU) 2016/679 —— https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng —— [C：EUR-Lex 返回 202 异步状态，正文未取到]
- 欧盟 Data Act Regulation (EU) 2023/2854（车辆数据可携权/互联产品数据访问权）—— https://eur-lex.europa.eu/eli/reg/2023/2854/oj —— [C：HTTP 202，正文未取到]

**写作纪律提示**：涉及 R155/R156 的**具体条款号、强制时间表、审核要求**时，本次无一手来源。凡引用必须标注「[未验证] 依通行公开认知」或改为待补证陈述，不得给出条款编号。

---

## 2. 授权与身份协议规范（全部经 RFC Editor / openid.net 取证，HTTP 200）

这是 §3 授权与访问控制章节的**规范底座**。每条均可直接引用，引用格式建议 `RFC 编号 §章节`。

### 2.1 OAuth 2.x 核心与扩展（A 级）

- RFC 6749 (2012) The OAuth 2.0 Authorization Framework（Obsoletes RFC 5849）—— https://www.rfc-editor.org/rfc/rfc6749.txt —— [A]
- RFC 6750 (2012) OAuth 2.0 Bearer Token Usage（Bearer 令牌在 HTTP 中的使用、`WWW-Authenticate` 错误语义）—— https://www.rfc-editor.org/rfc/rfc6750.txt —— [A]
- RFC 8252 (2017) OAuth 2.0 for Native Apps（原生 App 必须使用系统浏览器/外部用户代理，禁止内嵌 WebView）—— https://www.rfc-editor.org/rfc/rfc8252.txt —— [A]
- RFC 7636 (2015) PKCE（Proof Key for Code Exchange，公共客户端授权码拦截防护）—— https://www.rfc-editor.org/rfc/rfc7636.txt —— [A]
- RFC 9068 (2021) JWT Profile for OAuth 2.0 Access Tokens（`typ: at+jwt`、`aud`/`iss`/`exp` 校验要求）—— https://www.rfc-editor.org/rfc/rfc9068.txt —— [A]
- RFC 8705 (2020) OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens（mTLS 客户端认证 + 证书绑定令牌，即"持有的令牌不可被复制盗用"）—— https://www.rfc-editor.org/rfc/rfc8705.txt —— [A]（**车云链路最关键的授权规范**）
- RFC 9449 (2023) OAuth 2.0 Demonstrating Proof of Possession (DPoP)（发送方约束令牌，`DPoP` 头 + JWK 指纹绑定）—— https://www.rfc-editor.org/rfc/rfc9449.txt —— [A]
- RFC 9396 (2023) OAuth 2.0 Rich Authorization Requests（`authorization_details` 结构化权限对象，替代裸字符串 scope）—— https://www.rfc-editor.org/rfc/rfc9396.txt —— [A]（**车控场景"资源级授权"的规范依据**）
- RFC 8693 (2020) OAuth 2.0 Token Exchange（`subject_token`/`actor_token`，代理链授权）—— https://www.rfc-editor.org/rfc/rfc8693.txt —— [A]
- RFC 7523 (2015) JWT Profile for OAuth 2.0 Client Authentication and Authorization Grants（服务账号 + 客户端断言）—— https://www.rfc-editor.org/rfc/rfc7523.txt —— [A]
- RFC 7662 (2015) OAuth 2.0 Token Introspection（令牌内省，不透明令牌的实时校验）—— https://www.rfc-editor.org/rfc/rfc7662.txt —— [A]
- RFC 8414 (2018) OAuth 2.0 Authorization Server Metadata（`.well-known/oauth-authorization-server` 自动发现）—— https://www.rfc-editor.org/rfc/rfc8414.txt —— [A]
- RFC 7009 (2013) OAuth 2.0 Token Revocation（令牌吊销端点）—— https://www.rfc-editor.org/rfc/rfc7009.txt —— [A]
- RFC 9470 (2023) OAuth 2.0 Step Up Authentication Challenge Protocol（`acr`/`amr` 步进认证挑战）—— https://www.rfc-editor.org/rfc/rfc9470.txt —— [A]
- RFC 8628 (2019) OAuth 2.0 Device Authorization Grant（无浏览器设备授权，车机/受限 UI 场景适用）—— https://www.rfc-editor.org/rfc/rfc8628.txt —— [A]
- RFC 9635 (2024) Grant Negotiation and Authorization Protocol (GNAP)，Standards Track，2024-10 —— https://www.rfc-editor.org/rfc/rfc9635.txt —— [A]（**下一代授权协议，面向"细粒度 + 可协商"授权，代表演进方向**）
- OAuth 2.1 草案 draft-ietf-oauth-v2-1-16（强制 PKCE、废弃隐式流与密码模式、Bearer 令牌最小化）—— https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/ —— [A]
- OpenID Connect Core 1.0（`id_token`、UserInfo、认证与授权分离）—— https://openid.net/specs/openid-connect-core-1_0.html —— [A]
- OpenID Connect Discovery 1.0（`/.well-known/openid-configuration`）—— https://openid.net/specs/openid-connect-discovery-1_0.html —— [A]
- FIDO Alliance 规范（无密码/抗钓鱼凭证）—— https://fidoalliance.org/specifications/ —— [B]
- W3C WebAuthn Level 2 —— https://www.w3.org/TR/webauthn-2/ —— [A]
- UMA 2.0（User-Managed Access，用户自管授权）—— https://docs.kantarainitiative.org/uma/wg/rec-oauth-uma-grant-2.0.html —— [未验证：Kantara 站点 curl 超时]

---

## 3. 车云通信安全与 PKI（A 级为主）

- RFC 8446 (2018) TLS 1.3（1-RTT 握手、0-RTT 重放风险、前向保密）—— https://www.rfc-editor.org/rfc/rfc8446.txt —— [A]
- RFC 5280 (2008) X.509 PKI 证书与 CRL 规范（证书链、扩展、吊销列表）—— https://www.rfc-editor.org/rfc/rfc5280.txt —— [A]
- RFC 6960 (2013) OCSP（在线证书状态查询）—— https://www.rfc-editor.org/rfc/rfc6960.txt —— [A]
- RFC 3161 (2001) Time-Stamp Protocol（可信时间戳，**防重放的时间基准**）—— https://www.rfc-editor.org/rfc/rfc3161.txt —— [A]
- RFC 8555 (2019) ACME（自动化证书签发/轮换，短周期证书的工程前提）—— https://www.rfc-editor.org/rfc/rfc8555.txt —— [A]
- RFC 5480 (2009) ECDSA/EC 公钥在 X.509 中的表示 —— https://www.rfc-editor.org/rfc/rfc5480.txt —— [A]
- RFC 8017 (2016) PKCS #1 RSA —— https://www.rfc-editor.org/rfc/rfc8017.txt —— [A]
- RFC 6090 (2011) ECDSA/ECC 基础 —— https://www.rfc-editor.org/rfc/rfc6090.txt —— [A]
- RFC 8998 (2021) ShangMi (SM) Cipher Suites for TLS 1.3（SM2 签名、AEAD_SM4_GCM / AEAD_SM4_CCM、SM3）—— https://www.rfc-editor.org/rfc/rfc8998.txt —— [A]（**国密 TLS 在国际标准层面的唯一落点，国产车云链路合规的关键**）
- IEEE 1609.2（WAVE 安全服务 / 证书格式）—— https://standards.ieee.org/ieee/1609.2/6865/ —— [C：HTTP 200，正文未解析]
- 美国 SCMS（V2X 安全证书管理体系）—— [未验证：未取得可核验官方 URL]

---

## 4. 硬件根信任（TEE / SE / HSM）

- GlobalPlatform TEE System Architecture v1.3（规范号 GPD_SPE_009）—— https://globalplatform.org/specs-library/tee-system-architecture/ —— [A]
- GlobalPlatform 规范库 — Secure Element 分类 —— https://globalplatform.org/specs-library/?filter-committee=secure-element —— [A]
- OP-TEE（开源 TEE OS，TrustZone 之上的 TEE 实现）—— https://optee.readthedocs.io/en/latest/ —— [A]
- ARM TrustZone for Cortex-A —— https://www.arm.com/technologies/trustzone-for-cortex-a —— [B]
- ARM TrustZone for Cortex-M —— https://www.arm.com/technologies/trustzone-for-cortex-m —— [B]
- EVITA 项目（E-safety Vehicle Intrusion Protected Applications，定义车载 HSM 的 Full / Medium / Light 三级分级）—— https://www.evita-project.org/ —— [B]
- NIST FIPS 140-3（密码模块安全要求，HSM 认证基线）—— https://csrc.nist.gov/pubs/fips/140-3/final —— [A]
- NIST FIPS 186-5（数字签名标准 DSS）—— https://csrc.nist.gov/pubs/fips/186-5/final —— [A]
- NIST FIPS 197（AES）—— https://csrc.nist.gov/pubs/fips/197/final —— [A]
- NIST SP 800-57 Part 1 Rev.5（密钥管理建议：密钥生命周期、密码周期）—— https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final —— [A]
- NIST SP 800-38D（GCM 模式）—— https://csrc.nist.gov/pubs/sp/800/38/d/final —— [A]
- NIST SP 800-90A Rev.1（确定性随机比特发生器）—— https://csrc.nist.gov/pubs/sp/800/90/a/r1/final —— [A]
- NIST SP 800-133（密钥生成）—— https://csrc.nist.gov/pubs/sp/800/133/final —— [A]
- Infineon AURIX / TriCore 32 位汽车微控制器 —— https://www.infineon.com/cms/en/product/microcontroller/32-bit-tricore-microcontroller/ —— [C：HTTP 202，型号页未解析]
- NXP S32 汽车平台 —— https://www.nxp.com/products/processors-and-microcontrollers/s32-automotive-platform:S32 —— [未验证：curl 超时]
- Renesas 汽车产品线（RH850 系列）—— https://www.renesas.com/en/products/automotive-products —— [C]
- TI Jacinto TDA4VM —— https://www.ti.com/product/TDA4VM —— [C]
- AUTOSAR Classic Platform（Crypto Stack、SecOC、IdsM 入侵检测）—— https://www.autosar.org/standards/classic-platform/ —— [未验证：autosar.org 超时]
- TCG TPM 2.0 规范 —— https://trustedcomputinggroup.org/ —— [未验证：TCG 站点 403/超时]
- SHE（Secure Hardware Extension）规范 —— [未找到可核验公开一手 URL：成员制规范]

---

## 5. 数字钥匙与近场授权

- CCC Digital Key Release 3.0 发布公告（2021-04-21）：新增 **BLE + UWB** 实现被动无钥匙进入与启动，NFC 保留为强制备用方案，密钥存储于 **Secure Element** —— Car Connectivity Consortium —— https://carconnectivity.org/car-connectivity-consortium-delivers-digital-key-release-3-0-specification-businesswire/ —— [A]
- CCC Digital Key 主页面（跨 OS 生态、认证计划）—— https://carconnectivity.org/digital-key/ —— [A]
- CCC Digital Key Release 3 v1.1 规范向公众开放 —— https://carconnectivity.org/car-connectivity-consortium-makes-digital-key-release-3-v1-1-specification-available-to-the-public/ —— [B]
- CCC 与 FiRa Consortium 就 UWB 技术合作 —— https://carconnectivity.org/car-connectivity-consortium-and-fira-consortium-partner-on-uwb-technology-used-in-the-ccc-digital-key/ —— [B]
- FiRa Consortium 2.0 技术规范（2023-11）—— https://www.firaconsortium.org/news/press-releases/2023/11/fira-consortium-publishes-fira-2-0-technical-specifications —— [B]
- FiRa Core 3.0 规范与认证（2025-01）—— https://www.firaconsortium.org/news/press-releases/2025/01/fira-consortium-unveils-fira-core-3-0-specifications-and-certification —— [B]
- FiRa Core 4.0 规范与认证（2025-12）—— https://www.firaconsortium.org/news/press-releases/2025/12/fira-consortium-unveils-fira-core-4-0-specifications-and-certification —— [B]
- GB/T 44402.1-2024 数字钥匙系统参考架构（见 §1.2）
- IEEE 802.15.4z（UWB 物理层增强）—— [未验证：未取得可核验官方 URL]

---

## 6. OTA 与供应链安全

- Uptane 框架官网（首个面向汽车、面向"可抵御国家级攻击者"设计的软件更新安全系统；Linux Foundation Joint Development Foundation 项目）—— https://uptane.org/ —— [A]
- Uptane Standard 最新版 **2.1.0**（Director 仓库 + Image 仓库双仓库模型）—— https://uptane.org/docs/latest/standard/uptane-standard —— [A]
- The Update Framework (TUF) 官网（阈值签名，防仓库/密钥泄露）—— https://theupdateframework.io/ —— [B]
- TUF 规范（Root / Targets / Snapshot / Timestamp 四角色 + 委托 + threshold/quorum 阈值模型）—— https://theupdateframework.github.io/specification/latest/ —— [A]
- RFC 9019 (2021) A Firmware Update Architecture for IoT Devices（SUIT 架构）—— https://www.rfc-editor.org/rfc/rfc9019.txt —— [A]
- RFC 9124 (2022) A Manifest Information Model for Firmware Updates in IoT Devices（SUIT Manifest 信息模型）—— https://www.rfc-editor.org/rfc/rfc9124.txt —— [A]
- IETF SUIT 工作组 —— https://datatracker.ietf.org/wg/suit/about/ —— [A]
- SUIT Manifest 草案 draft-ietf-suit-manifest-27 —— https://www.ietf.org/archive/id/draft-ietf-suit-manifest-27.html —— [C]
- GB 44496-2024 / GB/T 47325-2026（中国 OTA 强制与推荐国标，见 §1.1/§1.2）
- SPDX 规范（SBOM；对应国际标准 ISO/IEC 5962:2021）—— https://spdx.dev/use/specifications/ —— [A]
- CycloneDX 规范概览（SBOM）—— https://cyclonedx.org/specification/overview/ —— [B]
- SLSA v1.0 分级（Build L0–L3，供应链构建完整性）—— https://slsa.dev/spec/v1.0/levels —— [A]
- in-toto 规范（供应链完整性元数据与签名链）—— https://in-toto.io/specs/ —— [B]
- OCPP 1.6 / 2.0.1 / 2.1（充电侧协议族，授权与计量）—— Open Charge Alliance —— https://www.openchargealliance.org/protocols/ —— [A]
- ISO 15118-2 / -20（Plug & Charge，TLS + contract certificate，充电授权的证书模型）—— https://www.iso.org/standard/55366.html —— [未验证：iso.org Cloudflare 拦截，标准号需复核]

---

## 7. 车企一手证据（授权与访问控制为主）

### 7.1 Tesla（证据最厚，全部来自 developer.tesla.com，[A]）

Tesla Fleet API 是**目前公开文档中最完整的"车-云第三方授权"实现范例**，其 scope 模型、令牌模型、密钥模型可直接作为行业标尺。

**令牌类型与鉴权头**
- Fleet API 要求请求头 `Authorization: Bearer <token>`；文档定义**三类令牌**：third-party token（代表车主行事的第三方令牌）、partner token（合作伙伴令牌）、third-party-for-business token —— https://developer.tesla.com/docs/fleet-api/authentication/overview —— [A]

**Scope 全清单（文档原文名称）**
- `openid`、`offline_access`、`user_data`、`vehicle_device_data`、`vehicle_location`、`vehicle_cmds`、`vehicle_charging_cmds`、`vehicle_specs`、`vehicle_pricing_info`、`energy_device_data`、`energy_cmds`、`enterprise_management` —— https://developer.tesla.com/docs/fleet-api/authentication/overview —— [A]
- `openid` = "Sign in with Tesla"（允许车主用 Tesla 凭证登录第三方应用）；`offline_access` = 获取刷新令牌以免重复登录 —— 同上 —— [A]
- `user_data` 覆盖联系方式、家庭住址、头像、推荐信息；`vehicle_device_data` 覆盖实时数据、服务历史、服务预约、服务沟通、可升级项、附近超充、所有权信息 —— 同上 —— [A]
- `vehicle_location` 覆盖精确与粗略位置；**带 `granular_access.hide_private=true` 的车辆共享即使被授予 `vehicle_location` 也拿不到任何位置，且无法流式传输位置字段** —— 同上 —— [A]（**"授权被授予但资源级策略进一步收窄"的双层控制实例**）
- `vehicle_cmds` 覆盖添加/移除驾驶员、Live Camera 访问、解锁、唤醒、远程启动、预约软件更新 —— 同上 —— [A]
- `vehicle_charging_cmds` 覆盖充电历史、计费金额、充电地点、预约/开始/停止充电 —— 同上 —— [A]
- `vehicle_specs` **仅 Partner Token 可用**，且对**任意车辆**可用、**无需车主授权** —— 同上 —— [A]（**重要的授权控制例外：存在不进入"逐车主同意"模型的资源访问路径**）
- `vehicle_pricing_info` **仅 Partner Token 可用** —— 同上 —— [A]
- 授权服务器元数据发布在 https://fleet-auth.prd.vn.cloud.tesla.com/oauth2/v3/thirdparty/.well-known/openid-configuration —— 同上 —— [A]（对应 RFC 8414 / OIDC Discovery）

**授权码流程细节**
- 第三方令牌使用 OAuth `authorization_code` 授权流代表车主行事；文档明确"认证端点不计费" —— https://developer.tesla.com/docs/fleet-api/authentication/third-party-tokens —— [A]
- 授权端点 `https://auth.tesla.com/oauth2/v3/authorize`，必填参数 `response_type=code`、`client_id`、`redirect_uri`、`scope`、`state`（文档描述为"用于校验的随机值"）；可选 `nonce`（"用于防重放的随机值"） —— 同上 —— [A]
- `/authorize` 附加可选参数：`prompt_missing_scopes=true`（对尚未授权的 scope 再次提示）、`require_requested_scopes=true`（必须授权**全部**请求 scope 才放行）、`show_keypair_step=true`（预告虚拟密钥配对第二步） —— 同上 —— [A]
- 令牌端点与 API 端点**分属不同主机**：`POST https://fleet-auth.prd.vn.cloud.tesla.com/oauth2/v3/token`（文档说明 `/token` 调用"来自应用服务器、适用不同的限流"） —— 同上 —— [A]
- `/token` 换码参数含 `grant_type=authorization_code`、`client_id`、`client_secret`、`audience`（**必须是 Fleet API base URL**，如 `https://fleet-api.prd.na.vn.cloud.tesla.com`）、`redirect_uri`、`scope` —— 同上 —— [A]
- **刷新令牌一次性使用（single use only）且在 3 个月后过期** —— 同上 —— [A]（令牌轮换的强约束实现）
- **宽限期：最近一次使用的刷新令牌在 24 小时内仍有效**（用于覆盖"应用未能持久化轮换后令牌"的失败场景） —— 同上 —— [A]
- 刷新失败返回 `401 login_required` 的两种场景：刷新令牌过期/被更新令牌挤出，或**用户已重置密码** —— 同上 —— [A]
- 用户可通过 `https://auth.tesla.com/user/revoke/consent?revoke_client_id=$CLIENT_ID&back_url=$RETURN_URL` 管理授权范围或撤销授权 —— 同上 —— [A]（车主侧可撤销入口）
- **Scope 缩减与既有刷新令牌兼容**，仅对新签发的访问令牌生效；**新增 scope 需以 `prompt_missing_scopes=true` 重新发起 `/authorize`** —— 同上 —— [A]

**虚拟密钥（Virtual Key）——车端授权校验**
- 虚拟密钥 = 公私钥对；公钥须由**可信用户**添加到车辆，私钥留在应用服务器；**车辆在执行命令前或接受 Fleet Telemetry 配置前验证载荷签名** —— https://developer.tesla.com/docs/fleet-api/virtual-keys/developer-guide —— [A]
- 文档称虚拟密钥"**甚至能阻止 Tesla 自己的后端访问这些能力**"；吊销由用户在车辆 Locks 界面删除密钥完成 —— 同上 —— [A]
- 密钥生成命令 `openssl ecparam -name prime256v1 -genkey -noout`；文档明确"车辆仅支持 prime256v1 密钥"（即 P-256 ECDSA） —— 同上 —— [A]
- 公钥必须托管于 `https://developer-domain.com/.well-known/appspecific/com.tesla.3p.public-key.pem` 且**必须长期可用**；私钥 `private-key.pem` 绝不可托管于域名 —— 同上 —— [A]
- 必须调用 Partner Account 注册端点把密钥登记到 Tesla；配对深链 `https://tesla.com/_ak/<developer-domain.com>`（可选 `?vin=...`） —— 同上 —— [A]
- B2B 项目车辆可自动添加虚拟密钥，条件为**已配对密钥少于 20 把**且不需要车辆命令协议；非 B2B 渠道购买的车辆无法由 Tesla 远程添加密钥 —— 同上 —— [A]（**密钥数量上限作为"影响范围控制"的工程手段**）
- 配对要求用户已授予 `vehicle_device_data`、`vehicle_cmds` 或 `vehicle_location` 中至少一项 —— 同上 —— [A]

**Fleet Telemetry（车→云直连流）**
- Fleet Telemetry 让车辆直连开发者服务器，取代轮询 `vehicle_data` 端点；客户端源码 https://github.com/teslamotors/fleet-telemetry ，命令代理 https://github.com/teslamotors/vehicle-command —— https://developer.tesla.com/docs/fleet-api/fleet-telemetry —— [A]
- 前置条件：车辆固件 2024.26+；证书签名类应用需 2023.20.6+；Model S/X（Intel Atom）需 2025.20+；必须已配对虚拟密钥 —— 同上 —— [A]
- 配置由应用私钥**签名**且"**Tesla 无法编辑**"；若所需 scope 被撤销导致配置失效，配置会被**从车辆移除** —— 同上 —— [A]（授权撤销→配置自动回收的联动控制）
- **单台车辆最多同时向 5 个第三方应用推流** —— 同上 —— [A]
- 服务端 TLS 指引：开发者须用仓库内 `tools/check_server_cert.sh` 校验主机与 CA 兼容性 —— 同上 —— [A]
- 位置类字段（Location、OriginLocation、DestinationLocation、DestinationName、RouteLine、GpsState、GpsHeading）需要 `vehicle_location`；`hide_private` 共享车辆尝试访问会被拒绝并返回 **HTTP 403 "location access not granted"** —— 同上 —— [A]
- 遥测传输行为：500 ms 事件收集窗口；按字段 `interval_seconds` 与变化触发上报；示例负载约 15 信号/分钟 ≈ $0.0001/分钟 ≈ $0.006/行驶小时 —— 同上 —— [A]
- 断连处理：车辆缓冲 5000 条消息（≥2500 秒数据）；重连采用指数退避，最大重试延迟 30 秒 —— 同上 —— [A]
- 客户端版本变更记录含 1.0.0（固件 2025.2.6 / 2024.45.32.20，新增 `delivery_policy=latest` 要求服务端 ≥0.7.1）、1.1.0、1.2.0（固件 2025.44.25.5）、1.3.0（固件 2026.26.6，`include_fields`） —— 同上 —— [A]

**限流与计费（影响范围控制的另一维度）**
- 限流按账号按设备计：实时数据 60 次/分；唤醒 3 次/分；设备命令 30 次/分；同账号多应用**共享**限额 —— https://developer.tesla.com/docs/fleet-api/billing-and-limits —— [A]
- 计费按用量、月度周期（每月 1 日起算）；每账号计费上限默认 0；达 80% 与 100% 时发邮件；**超限会暂停 API 使用并移除 Fleet Telemetry 推流配置（且不恢复）** —— 同上 —— [A]
- 个人开发者/小应用每月 $10 折扣；**响应码 <500 全部计费，≥500 不计费**；费用四舍五入到 $0.01 —— 同上 —— [A]
- 明确过渡日期："Application access will not be disabled during the payment transition period which ends February 1, 2024"（第三方付费 API 的强制执行安排在 2024-02-01 前后） —— 同上 —— [A]（**说明：原文陈述与"2024-02-01"为该页一手引文**）
- 2018 年前 Model S/X 且未做信息娱乐升级的车辆**不支持** Fleet Telemetry，且无支持计划 —— 同上 —— [A]

**漏洞披露与赏金**
- Tesla 在 Bugcrowd 运营漏洞赏金项目，启动于 2015-08-04，状态 in progress —— https://bugcrowd.com/engagements/tesla —— [A/B]
- 赏金档位：Critical $50,000–$100,000；High $20,000–$50,000；Moderate $10,000–$20,000；Low $500–$10,000 —— 同上 —— [B]
- 车辆/能源产品问题须邮件报至 `vulnerabilityreporting@tesla.com` 并使用 Tesla GPG 公钥，**不走 Bugcrowd 网页表单**；硬件研究须先向 Tesla 登记车辆/Powerwall —— 同上 —— [A/B]
- 规则要点：若访问到不属于自己的数据须在 24 小时内停止并披露；未经 Tesla 批准不得公开披露已确认未修复漏洞；超级充电及相关基础设施**不在范围内**；涉及第三方库的漏洞可能被转给厂商而不通知研究者 —— 同上 —— [B]

**Tesla 未能证实项（禁止当作事实写入）**
- "访问令牌有效期约 8 小时"：在已读页面中**未获证实**。已证实的是**刷新令牌**一次性且 3 个月有效、以及 24 小时复用宽限。访问令牌 TTL 标记为待补证。
- "2023 年 Toyota/Tesla 漏洞披露事件"与"Tesla 2023 年 API 收紧"的叙事版本：未取到一手来源，仅有 "2024-02-01 计费过渡结束"这一硬日期。标记为待补证。

### 7.2 Mercedes-Benz（全部来自 developer.mercedes-benz.com，[A]）

- 开发者平台 https://developer.mercedes-benz.com ，运营主体 Mercedes-Benz Connectivity Services GmbH（页脚版权 "© 2026"） —— [A]
- 产品分类：Fleet Data、Smart Vehicle Data、Infrastructure Data、Vehicle Commerce Data、Repair & Maintenance Data —— https://developer.mercedes-benz.com/ —— [A]
- 数据处理主张（原文）："The trust and consent of our vehicle customers are at the heart of our business – ensuring GDPR compliance and enabling secure, reliable data you can depend on." —— 同上 —— [A]
- 文档页明确列出两种鉴权集成模式：OAuth **Authorization Code Flow** 与 **Client Credentials Flow** —— https://developer.mercedes-benz.com/product-docs —— [A]
- 采用授权码流的理由（原文意译）："部分 API 提供燃油状态、车门锁状态等数据，属 GDPR 意义上的个人数据，因此需要终端用户同意"；平台自称使用"standard OAuth 2.0" —— https://developer.mercedes-benz.com/get-started/oauth/authorization-code-flow —— [A]
- 对开发者的安全要求：客户端凭证必须保存在后端服务器，应用"**不得**向客户端暴露任何客户端凭证（client id、client secret、访问令牌）" —— 同上 —— [A]
- 五步流程：重定向浏览器至授权端点 → 用户认证并采集同意 → 携带授权码回调 → 用授权码换取访问令牌 → 以令牌代表终端用户调用 API —— 同上 —— [A]
- 同意界面语义：展示所请求的 SCOPE 与"purpose URL"，便于终端用户知情决策；**`openid` scope 为获得有效令牌所必需，`offline_access` 为获得刷新令牌所必需** —— 同上 —— [A]
- 文档给出的授权端点示例：`https://ssoalpha.dvb.corpinter.net/v1/auth?response_type=code&client_id=...&redirect_uri=...&scope=...&state=...`；令牌端点 `https://ssoalpha.dvb.corpinter.net/v1/token` —— 同上 —— [A]
- 示例 scope 字符串（Fuel Status 产品）：`scope=openid offline_access mb:vehicle:mbdata:fuelstatus` —— 同上 —— [A]（**`mb:` 命名空间式 scope 约定：产品-域-资源三段式，是车企资源级 scope 设计的典型样本**）
- 令牌端点客户端认证采用 **HTTP Basic**（`clientId:clientSecret` BASE64 编码置于 Authorization 头） —— 同上 —— [A]
- 访问令牌有效期：响应 `expires_in` 字段为秒数，"**默认 3599 秒**"（≈1 小时）；示例 JSON 含 `access_token`、`refresh_token`、`id_token` —— 同上 —— [A]
- 刷新：`grant_type=refresh_token`，刷新令牌**一次性使用**，授权服务器返回**新的访问令牌与新的刷新令牌**；已用/无效刷新令牌报错 "The given refresh token is not valid or was already used" —— 同上 —— [A]
- 错误语义：`invalid_scope` → "No registered scope value for this client has been requested"；"Invalid grant" 用于授权码无效或已被使用；"Invalid redirect URL" 用于 redirect_uri 与注册值不一致 —— 同上 —— [A]
- 客户端指引：在服务端应用缓存访问令牌与刷新令牌；访问令牌有效期内直接使用，失效后由缓存的刷新令牌换取 —— 同上 —— [A]

**Mercedes 未取到**：数字钥匙（CCC）、mTLS/证书固定、TEE/安全元件、OTA 安全、2024–2025 车辆数据 API 政策文档、MBition、Mercedes Pay。全部标记待补证。

### 7.3 Volkswagen Group / CARIAD（[A]，但为自述营销口径）

- CARIAD 将 Automotive Cloud 定位为集团中央车云平台："Our cloud ecosystem connects the Volkswagen Group's vehicles, markets and services via a central platform"；自称"超过 4500 万辆网联车"、"全球最大的汽车云基础设施" —— https://cariad.technology/de/en/solutions/automotive-cloud-connectivity.html —— [A，公司自述口径]
- 同页指标条："1 ecosystem for all VW brands"、"45 million connected vehicles"、"90 markets connected"、"365 days global support" —— 同上 —— [A]
- 同页称数据平台是"所有车辆相关 AI 创新的关键使能器"，云支持"安全关键更新"的 OTA 下发 —— 同上 —— [A]
- CARIAD 自我定位："We are the Volkswagen Group's automotive software company... for iconic car brands, including Audi, Volkswagen and Porsche" —— https://cariad.technology/ —— [A]
- 站点产品分类：Infotainment、Automated Driving、Connectivity & Cloud、Motion & Energy —— 同上 —— [A]

**VW/CARIAD 未取到**：E3 架构、VW.OS、ID 系列 OTA 细节、UN R155 集团合规声明、与 Mobileye/Bosch 的合作、任何 CARIAD 安全白皮书。VW Newsroom 对 `R155` 的站内检索返回零结果项。全部标记待补证。

### 7.4 BMW（本次网络封锁，未取到）

- `https://developer.bmwgroup.com/` DNS 可解析（160.46.244.54）但返回 Apache 占位页："BMW Group – no content deployed … This project didn't deploy any content yet"（Last-Modified 2026-04-27），未提供 CarData / OAuth 文档 —— [A，直接观测]
- `https://crd.bmwgroup.com/` 无法解析；`https://b2b-developer.bmwgroup.com/` 超时 —— [A，直接观测]
- `www.bmw.com` / `www.bmwgroup.com` 从本网络被区域封锁（HTTP 000 / 边缘封锁）；`www.bmwgroup.com/en/innovation/vehicle-data.html` 经浏览器返回站点自身 404 —— [A，直接观测]
- `https://b2b.bmw.com` 可达，但为**供应商采购门户**（purchasing/logistics 登录），非车辆数据开发者 API 门户 —— [A]
- **未取到**：BMW CarData OAuth scope 清单、令牌有效期、CCC 数字钥匙、BMW 安全白皮书。原因是网络/检索封锁，**不得据此推断 BMW 无相应方案**。

### 7.5 Rivian（本次区域封锁，未取到）

- `https://rivian.com` 从本出口返回 Amazon CloudFront 403："The CloudFront distribution is configured to block access from your country" —— [A，直接观测]
- `developer.rivian.com` 无 DNS 解析；`api.rivian.com` 可解析（13.35.190.19）但为 App 后端，非公开开发者门户 —— [A，直接观测]
- **未取到**：Rivian Fleet API、OAuth 支持、数字钥匙文档。原因同上。

### 7.6 比亚迪 BYD（i迪桥开放平台，[A]）

- 官方开放平台名为「**i迪桥**」，站点 https://open.byd.com/ ，首页显示"12 已上线服务 / 60 服务总系统 / 53.8 亿+ 累计服务请求数"，© 2025 比亚迪提供计算服务，粤 ICP 备 10216027 号 —— [A]
- **鉴权方式为 API Key（appKey）而非 OAuth**：接口调用文档明确"用户创建应用 → 审核后生成 appKey 作为调用者身份识别"、"`x-Gateway-APIKey`：应用的 appKey，用于调用接口鉴权，传入 Header 头" —— https://open.byd.com/platform?id=1848412878248345602 （文档发布 2024-01-23） —— [A]
- 网关示例域名 `esb.byd.com.cn`（示例 URL `https://esb.byd.com.cn/tong/restful/api/mdm07670/package_1`），文档注明"以上示例只作为参考不可实际调用" —— 同上 —— [A]
- 接入五步流程：登录平台 → 用户认证（公司/组织认证）→ 应用创建（获取调用 API 唯一凭证）→ 注册/订阅 → 服务访问授权后调试 —— https://open.byd.com/ —— [A]
- 平台版本公告「i迪桥平台 3.3.4 版本全面升级」含 API 在线导出、API 提供者信息、API 注册暂存 —— https://open.byd.com/notices-details?id=1994268247284723713&toB=1 —— [A]
- 对接邮箱 `openapi@byd.com` —— https://open.byd.com/ —— [A]
- 定位判断：i迪桥为企业级 ESB/API 网关（覆盖供应链/研发/智造/营销/物流/品质/财务七大领域），**非车控开放平台**；未见 mTLS / 国密 / 数字钥匙 / OAuth scope 文档 —— [A，依据平台自述]

### 7.7 蔚来 NIO（Open NSC，[A] 但文档陈旧）

- 官方开放平台为 GitBook 托管的「**Open NSC（NIO Service Cloud）**」，入口 https://developer.nio.com/ —— [A]
- **鉴权为 app-id + secret 双凭证，非 OAuth**："app-id 和 secret 是系统对接调用的唯一凭证……通过商务渠道获取" —— https://developer.nio.com/docs/open-nsc/spec/integration-process.html —— [A]
- 环境：stg `https://open-stg.nio.com`，prod `https://open.nio.com` —— https://developer.nio.com/docs/open-nsc/spec/env.html —— [A]
- 接口规范正文受 token 保护："请联系文档提供人获取文档访问 token" —— https://developer.nio.com/docs/open-nsc/spec/interface.html —— [A]（**平台侧把文档访问本身也纳入授权控制**）
- 文档首页标注"文档最后更新于: 2019-08-13，字段后续还有可能微调"，站点自述"正在建设中" —— https://developer.nio.com/ —— [A]
- 平台业务范围为服务云（一键加电/维保/拖车/租车/代泊/航班），**不含车控/数字钥匙 API** —— 同上 —— [A]
- NIO 隐私政策页 https://www.nio.cn/privacy-policy —— [A，JS 渲染，正文未取到]

### 7.8 小米（小米 IoT 开发者平台 / 信任中心，[A]）

- 官方开发者平台为「小米 IoT 开发者平台」https://iot.mi.com/ ，2026 年品牌为「小米澎湃智联」，与 Xiaomi HyperOS Connect 联动，宣称"人车家全生态" —— [A]
- 文档中心 https://iot.mi.com/v2/new/doc/home （HTTP 200，标题「小米IoT文档与资源中心」） —— [A]
- 合规与安全入口：小米信任中心 https://trust.mi.com/zh-CN/compliance ，载明 ISO/IEC 27001 认证（编号 IS 831552，范围含小米科技 IT 运维与云服务），并自述定期发布安全与隐私白皮书 —— [A]
- 平台接入流程"成为开发者 → 创建产品 → 研发配置 → 认证发布"面向**硬件模组厂商**，非面向车企的车云 API 开放平台 —— https://iot.mi.com/ —— [A]
- **未取到**：小米汽车（xiaomiev.com）专属开放平台、车控 API、OAuth scope、数字钥匙官方技术文档。小米汽车官网可达但无开发者入口。

### 7.9 理想 / 小鹏 / 极氪 / 零跑 / 奇瑞（覆盖度薄弱）

- 理想：官方用户隐私政策（生效 2026-01-22，主体北京车励行信息技术有限公司、北京罗克维尔斯科技有限公司；覆盖官网/App/小程序/车机端）—— https://www.lixiang.com/agreement/privacy.html —— [A]。**`open.lixiang.com`、`developer.lixiang.com` 均无 DNS 解析** —— [未找到公开来源]
- 小鹏：`open.xiaopeng.com/dev/` 站点存在但对所有请求（curl 常规 UA、浏览器）返回 **403 Forbidden（openresty）**，无法核实鉴权机制/scope/令牌有效期 —— [A 站点存在，内容不可验证]。`xmart.xiaopeng.com` 有 DNS 解析（47.96.221.177）但证书无效（ERR_CERT_AUTHORITY_INVALID）—— [未找到可验证公开来源]。小鹏用户协议 https://login.xiaopeng.com/policy.html （主体广州智鹏车联网科技有限公司）—— [A]
- 极氪：`open.zeekrlife.com` 返回 HTTP 500 空页；`www.zeekrlife.com` 为官网但未发现开发者/开放平台入口 —— [A 站点存在，无可用信息]
- 零跑：`cn.leapmotor.com` 可达但无开放平台入口；`developer./dev./open.leapmotor.com` 均无 DNS —— [未找到公开来源]
- 奇瑞：官网设「网络产品安全漏洞」专栏 https://www.chery.cn/others/networksecurity/ —— [A，页面可达]。`developer.chery.cn`、`open.chery.cn` 无 DNS —— [未找到公开来源]
- 华为：开发者联盟统一入口 https://developer.huawei.com/consumer/cn/ —— [A]。尝试抓取 Wallet Kit 数字车钥匙文档（`/doc/harmonyos-guides/wallet-kit-*`）与安全文档均返回 JS 空壳页（标题仅「文档中心」，1749 字节），正文无法取证 —— [未找到可验证公开来源]

### 7.10 车企侧矛盾与不确定项（写作时必须处理）

1. 「蔚来 UWB+蓝牙+NFC 三合一数字钥匙」仅见新浪汽车等二手报道（https://auto.sina.cn/2026-07-18/detail-iniicyyt8275101.d.html ，[C]），蔚来官方未取得技术说明；无法确认是否 CCC 3.0、是否有 SE 保护。
2. 小鹏 UWB 钥匙为论坛/短视频内容，官方未证实具体车型与安全实现；`open.xiaopeng.com` 403 使"小鹏开放座舱 API"一说无法向一手文档求证。
3. 比亚迪 i迪桥是**企业级 ESB 网关**（供应链/研发/智造），与"车控开放平台 / 车主 API"不是同一事物；未见其 OAuth 与数字钥匙能力。报告中必须区分，避免误导向"比亚迪车云授权=APIKey"的过度归纳。
4. 蔚来 Open NSC 文档停留在 2019 年且站点自述"建设中"，**不能代表蔚来当前车云安全架构**。
5. **9 家国内车企本次全部未取得关于"国密 SM2/SM3/SM4"、"mTLS 双向证书"、"证书轮换"、"HSM/SE/TEE"的任何官方一手来源** —— 报告中这些方向的结论一律写为"未找到公开来源 / 待补证"，禁止以行业常识冒充车企事实。
6. Xiaomi HyperOS Connect 宣称覆盖"人车家"，但 iot.mi.com 文档面向硬件模组厂商，未见小米汽车车云 API/鉴权细节。

---

## 8. 覆盖度局限（必须在报告 §7.2 或等价章节逐项列出）

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

**方法论声明（写入报告正文）**：本次调研因检索工具额度耗尽，采用"权威 URL 直取 + 逐条标注证据等级"的方法。凡 `[A]` 条目为官方一手页面直接取证；`[B]` 为权威第三方；`[C]` 为二手；`[未验证]` 表示站点可达性确认但正文未取到。报告中另设"待补证清单"，明确区分"公开信息缺失"与"能力缺失"。
