# Lowest Price Hunter

可重复运行的欧洲比价 CLI，Python 3.11+，零运行依赖、零付费 API。当前为 **可运行的证据优先研究工具 v0.1**，不是已覆盖欧洲全站的自主购物 Agent。AI Agent 可以按 SKILL.md 使用 CLI；程序自身不调用收费模型。

## 启动（在解压后的项目目录）

```bash
python -m unittest discover -s tests -v
python -m hunter.cli --config config/aeg.json --out reports/live
python -m hunter.cli --config config/europe.json --out reports/europe
```

Windows 可把 `python` 换为 `py -3`。无需 pip 安装。查看 `reports/live/report.html`，机器数据为 JSON / CSV，历史在 SQLite。重复运行追加历史，不覆盖历史数据库。HTML/JSON/CSV 是当前快照。网络失败仍输出报告；零结果绝不代表不存在商品。所有时间为 UTC ISO 8601。

## 已实现

- JSON-LD Product/Offer 的型号、EAN、SKU、币种、价格、库存解析；拒绝 AggregateOffer 低价和型号后缀误配。
- 配置驱动的 NL/DE/BE 商家搜索页候选发现（同域、精确型号 URL、最多3个候选）；可增加欧洲其他国家商家。
- 公开 JSON/CSV 商品 Feed 适配器；必须提供合法 Feed URL，不声称已连接未获授权的 Feed。
- HTML 可见文本的停售/展示机冲突保护；避免从配件和推荐商品借用库存。
- 官方促销、优惠网站、返现和社会媒体公开页面线索收集，含 URL、时间、片段、候选代码及未验证状态。
- 优惠等级 A/B/C/D 数据契约，A 需要对应商品、真实购物车证据、4小时内时间、资格和前后总额一致；只采用单个已验证优惠组合，不假设叠加。
- Cashback 潜在成本辅助计算，只有资格和兼容性都显式确认才输出，绝不从结账价扣除。
- 运费、荷兰配送、VAT、手续费、退货、保修、安装、回收字段和带来源的证据导入；未知费用保留空值，禁止进入确定排名。
- 精确报价去重、Decimal 计算、前10确定报价及未核实报价分组、SQLite 价格/失败运行历史。
- robots fail-closed、明确 UA、每域至少2秒、超时、最多2次重试、响应体大小限制、CAPTCHA/403/429/重定向停止、日志。
- 25项离线自动化测试与手动 GitHub Actions 工作流；没有 schedule。

## 配置与证据

`config/aeg.json` 是真实验收目标。`config/europe.json` 是 NL/DE/BE 搜索入口，访问成功不等于能取得报价。新商家提供 `merchant`, `country`, `url`；可选 `search_url` 内以 `{query}` 占位。Feed 需 `adapter: feed`, `format: json` 或 `csv`，字段见 `scrapers/feed.py`。

配送/VAT 等不能由国家后缀推断。浏览器或人工实际读到条件后，在配置的 `evidence` 列表添加对象：`offer_url`, `model`, `source_url`, `quote`, `checked_at`, `destination_country: NL`, `facts`。`facts` 可包含 `shipping`, `fees`, `delivery_nl`, `vat_included`, `warranty`, `returns`, `installation`, `old_appliance`。证据在4小时内且精确匹配报价才应用。不自动填0；必须确认没有其他必要费用后才记录 `fees: 0`。真实用户地址不应放进代码仓库。

实际购物车观察可放入 config 的 `coupons` 列表：`offer_url`, `model`, `source_url`, `checked_at`, `grade`, `cart_evidence`, `currency`, `eligibility_confirmed`, `before`, `after`。程序只校验记录完整性/时间/金额，不能替代真实浏览器操作或鉴定记录真伪。`cashback` 列表同样需要精确 offer、model、来源、时间；潜在净成本还要求 `eligible: true`, `compatible: true`, `terms_url`, `amount`，只采用单个方案，绝不自动叠加。

这是本地单用户 CLI，不是允许陌生 URL 输入的公网抓取服务。域名 DNS 可由环境代理解析，不验证代理上游 IP；不要部署为公开 HTTP 接口。重定向目前停止并报告，人工审核最终公开 URL 后更新配置。robots 允许不代表商家条款授权，启用新商家前应人工审核条款；明确禁止的来源应移除。

## 尚未自动化的部分

- 没有安装或执行第三方购物 Skills；只审阅，不采用它们的收费后端、隐身代理或购买流程。
- 没有运行 Playwright 购物车测试、提交订单、付款、登录、注册 Newsletter 或激活返现。因而本次没有 A 级优惠。
- 自动收集优惠**线索**不等于自动验证适用商品、用户资格、有效期、叠加关系。
- 没有将返现记录自动关联到 SKU；目前是线索和独立计算函数。没有自动判断复杂法律/税费/保修条款。
- DE/BE 是通用候选发现和解析能力，尚无成功取得报价的站点专项认证；JS页面、反爬、改版可产生覆盖缺口。
- 尚无小红书/YouTube/TikTok 平台专用适配器；本次公开搜索未取得可核实优惠内容。Reddit 仅为讨论线索，不证明价格/库存。
- 没有接通搜索引擎 API 或付费历史服务；历史从自己的实际观测开始，不伪造既往最低价。

## GitHub 已部署与费用保护

源代码已上传至私人仓库 [sunjiale1017-collab/lowest-price-hunter](https://github.com/sunjiale1017-collab/lowest-price-hunter)，包含手动触发的 GitHub Actions `.github/workflows/manual.yml`。**代码上传成功不等于云端运行通过**；截至本次文档修订，尚无 GitHub Actions 成功运行的证据。

运行工作流在 GitHub 仓库的 **Actions → Manual comparison → Run workflow**。开关 `run_approved` 默认 false，只有用户明确同意本次运行才设为 true；若为 false，check job 不会执行。用户表示账户未绑定有效付款方式，GitHub 官方文档说明免费额度用完后会阻止继续使用；如以后添加付款方式，必须重新核实账单和超额费用限制。开启 `live` 表示允许尝试公开商家网页，不下单；默认 false 只运行 25 项离线测试。工作流最长 8 分钟；这是超时上限，**不是金钱费用上限**。

GitHub Actions 私人仓库消耗免费额度；如账户有有效付款方式，超过配额可能收费。请勿将用户口头提供的付款信息状态当成已独立验证的账户配置；有付款方式时应在 Billing 设置费用限制。仓库保持 Private，无自动 schedule、无付费 API、无登录 Cookie。项目不会自动弹出 GitHub Actions 授权；ChatGPT Project 的询问规则需要在其 Project Instructions 中另行配置，见 [docs/PROJECT_USAGE.md](docs/PROJECT_USAGE.md)。

## 测试证据

`reports/tests.txt` 为实际 unittest 输出；`reports/live/` 和 `reports/europe/` 为真实网络运行结果；`docs/ACCEPTANCE.md` 区分程序测试与网站验收。测试 fixture 是明确的合成测试数据，从未作为真实商品报价输出。

## 许可

本项目代码 MIT，见 LICENSE。`docs/audit/` 保存公开上游审阅材料及各自许可证；这些文件仍适用各原作者许可，不被本项目许可替换。审查范围及失败详见 docs/REPOSITORY_REVIEW.md。
