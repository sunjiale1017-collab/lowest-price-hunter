---
name: lowest-price-hunter
description: 使用免费公开来源研究欧洲商品真实到手价；以 Python CLI 输出证据、库存、优惠和失败报告。
---

# Lowest Price Hunter V4

默认中文、EUR、配送荷兰。以真实性优先，不使用任何付费 API、代理、试用计费或收费模型。先确认精确型号/EAN和商品状态。只比较相同 SKU/版本与状态。

1. 阅读 README 和目标 config。执行 `python -m unittest discover -s tests -v`。
2. 审核商家公开条款、robots、商品 URL；未知来源不执行脚本。按需调整配置。不要运行下载的审计文件。
3. 执行 `python -m hunter.cli --config config/aeg.json --out reports/live`；记录执行结果，失败或空结果不补造。
4. 对最便宜候选再次打开真实商品页，核对库存、卖家、VAT、荷兰配送、运费、必须费用、保修、退货及家电上楼/安装/旧机回收。
5. 搜索官方、Newsletter、App、首单、会员、学生、满减、免运费优惠，以及 Pepper/mydealz/Dealabs 和可公开访问社交媒体。区分独立讨论与广告。
6. 优惠 A=真实购物车验证；B=官方公开未测；C=第三方未测；D=失效。真实购物车仅在许可内操作，停止于付款前。不要用第三方“verified”字样冒充自己已验证。仅单个真实测试过的组合可扣减。
7. CashbackXL/ShopBuddies/品牌返利单列，确认 SKU、资格、返现入口、追踪、上限、时限和外部优惠码兼容性。不将未来返现计入确定总价。
8. 通过 evidence 导入实际读到的配送费用等事实，不设置无证据默认值。报告里未知项继续保留空值。
9. 报告最多10个确定报价，未核实报价分组。最便宜是**已核实可比报价中的最低**，不是全网最低。列来源、时间、实际脚本、失败及未尝试渠道。
10. CAPTCHA、访问限制、登录、禁止自动访问时停止，不换后端绕过。定时任务需用户同意并检查免费额度，成功部署前不声称监控已启动。

本项目不包含自主付款功能。程序能力与人工/Agent证据核验须明确区分。

## ChatGPT Project 运行政策（用户明确要求）

- 默认只在 ChatGPT 当前会话使用可用的网页搜索与分析工具回答商品比价，不运行 GitHub Actions。Project 本身不具备直接执行任意 Python/GitHub Actions 的能力。
- 在准备启动、重新运行、定时运行任何 GitHub Actions 之前，先向用户用中文解释本次 Actions 的作用（代码测试、AEG 实时采集或 NL/DE/BE 采集）、会生成什么报告、潜在 GitHub Actions 分钟/存储费用，并明确问用户是否授权本次运行。没有明确同意，不触发。不可把用户的一次许可视为永久授权。
- 必须保持 Private 仓库、手动 workflow_dispatch、无 schedule、无付费 API、无代理服务、无自动采购。不得为了节省费用自行把仓库设为 Public。
- 运行工作流中的 run_approved 默认 false，仅当用户明确同意一次运行时才能设为 true。用户表示未绑定付款方式，依据 GitHub 官方政策，缺少有效付款方式且免费配额耗尽时使用会被阻止。此付款状态尚未从账户账单中独立核实；若将来绑定付款方式，先核实剩余额度与费用限制。timeout-minutes 是运行时长上限，不是费用上限。
- 告知用户：GitHub Actions 免费配额与 GitHub 自身账单设置有关；Project 无法在缺少连接权限时自动触发工作流或读取其产物。不得称项目指令中的运行策略已安装到 ChatGPT Project，只能要求用户将说明复制进 Project Instructions。
- 通过 GitHub Actions 运行成功、程序采集得到候选报价、购物车验证、找到确定最低到手价，是四种不同状态；报告须分别标记。不要将 25 项离线测试通过等同于电商网站实时验证通过。

## 按商品型号进行新的 Python 搜索

当用户想查其他商品时，先从公开商品资料确定精确英文数字 SKU/型号（如 `TR738AT2B`）。仅在得到用户同意后，才可以让其通过 GitHub Actions 手动运行；不能将 ChatGPT Project 当作 Python 执行环境。

执行示例：

```bash
python -m hunter.cli --config config/europe.json --model TR738AT2B --out reports/custom
```

这只会查询配置好的 NL/DE/BE 三个搜索入口，尚无全欧动态商品发现器，也没有自动购物车优惠验证。若只有品牌或模糊描述，先在聊天中搜索并确认型号，不要将自然语言直接作为 `--model`。结果为 0 或费用未核实时应说明是覆盖不足，不能说明欧洲无货。

Actions 工作流手动输入：`run_approved` = 本次明确授权；`live` = 允许尝试公开商品网页；`product_model` = 目标精确型号。每次运行都要单独授权；不能将一次授权复用，也不得开启自动计费服务。
