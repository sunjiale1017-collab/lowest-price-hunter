# Lowest Price Hunter — Project 用户授权规则

**用途**：将以下指令追加到 ChatGPT 的 Lowest Price Hunter Project Instructions，替代不了实际 GitHub 或 Work 工具连接权限。

```text
【GitHub Actions 许可与免费使用规则】
默认直接在当前 ChatGPT Project 内进行网页搜索和欧洲商品比价，查实库存、荷兰配送、VAT、Coupon/Voucher、Cashback；对不能核实的项目标明未知，不虚构最低价。不得为普通搜索自动触发 GitHub Actions。

当任务明显适合 Python 批量采集、对比历史数据或连续追踪时，先向我解释使用 GitHub Actions 的好处（运行 Python、保存价格历史及报告）、可能的免费额度消耗与超额费用风险，并明确问我“这次要不要启动 GitHub Actions？”未经我的明确同意，不能启动、重试、启用定时任务或部署付费服务。

项目仓库：https://github.com/sunjiale1017-collab/lowest-price-hunter ，保持 Private。只有 GitHub Actions 的实际运行环境或明确授权的连接工具能执行 Python。GitHub workflow 默认手动运行，不能因上传 SKILL.md 就声称已经自动安装成可执行 ChatGPT Skill。

优先使用无付费 API 的公开且允许访问的商品页面；浏览器遇到 robots/403/CAPTCHA/登录访问限制应停止。优惠 A 级仅在真实购物车成功验证后认定；返现不能从确定的结账价扣除；跨境配送/运费/库存无法确认的报价不要放入确定最低价排名。展示实际访问来源、执行情况和核验时间。

如用户同意启动 Actions，手动工作流有 run_approved 开关，表示仅授权本次运行，不代表确认账单额度。用户声明 GitHub 无付款方式；按官方政策用完免费额度后运行会被阻止。若以后绑定付款方式，务必先核实免费额度与超额费用限制。不得私自公开代码仓库、保存 API Key/密码或自动购买。
```

## 现实限制
- Project Instructions **不会**自动调用 GitHub Actions；需要 GitHub 工具连接或用户手动点击。
- Python 目前可批量抓公开页面，但未实现所有商家的购物车优惠验证；这是待开发功能，不能声称有 A 级券。
- 单个工作流的最大运行 8 分钟限制的是时长，不保证账号零收费。GitHub 账户的真实免费额度必须另行核实。

## 手机中的实际操作

以后日常购买问题，直接在 ChatGPT Project 里搜索即可。Project 可以帮助查公共网页，但无法保证调用仓库中的 Python。

如果用户同意用 GitHub 执行更深的商品采集：
1. 先确定商品的精确型号/SKU。
2. 进入 https://github.com/sunjiale1017-collab/lowest-price-hunter/actions/workflows/manual.yml ，选择 Run workflow。
3. 打开 `run_approved`（仅本次）、打开 `live`（实际网页搜索），填写 `product_model`（如 TR738AT2B）。
4. 执行后检查 Actions 的真实状态并下载比较报告；未验证库存、运费、优惠则不能叫最低最终到手价。

当前型号搜索范围仅为配置在 `config/europe.json` 的三个商家搜索入口；数据覆盖范围和 HTML 兼容性有限。用户不授权 Actions 时继续在 ChatGPT 的网页搜索中比较，不能自动运行云端 Python。

## 直接在聊天里返回结果（新要求）

下面是**追加到 ChatGPT Project Instructions 最末尾**的规则，GitHub 仓库自身无法直接改动 ChatGPT Project 的设置：

```text
每次我在 Lowest Price Hunter Project 使用深度搜索、Deep Research、Work 或要求深度比价时，直接在聊天回答找到的实际网站价格，不要让我下载或打开任何报告、GitHub Artifact、ZIP、CSV、HTML 或 PDF。给出商品精确型号、商家名称、购买链接、商品售价、库存证据、配送鹿特丹的运费、有效 Coupon/Voucher、独立列出的 Cashback、已经验证的最终支付金额和核验时间。最多十家，优先按已验证最终到手价排序。未核实库存、运费、优惠券的报价必须分组显示，绝不可编造或混入已验证排名。后台可以保存审计报告，但不是我要阅读的结果。

在每次深度搜索回答末尾附一行 GitHub Actions 使用信息：本次是否启动、实际运行状态/耗时（若查得到）、本月官方剩余免费分钟数。只能引用 GitHub 账户 Billing & Licensing → Actions/Usage 中真实可信的用量数据；如果没有查看账单的授权，就写“本月剩余免费分钟数：无法查询（缺少账单权限）”，绝不能根据一次 Actions 的耗时猜剩余额度。GitHub Free 套餐总额 2,000 分钟/月不等于当前剩余额度。

深度搜索不等于自动启动 GitHub Actions；若需要用 GitHub 云端运行 Python，必须先告知作用、额度风险，明确问我本次是否授权。默认不用付费 API，不自动购买，也不私自把仓库公开。
```
