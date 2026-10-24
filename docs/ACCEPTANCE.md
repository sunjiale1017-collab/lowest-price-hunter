# 实际验收与状态

验收产品：AEG TR738AT2B，8 kg 热泵烘干机，EAN 7333394036762。核验日期：2026-10-24，准确 UTC 采集时间见 reports/live/report.json。

## 四种状态

| 状态 | 结果 |
|---|---|
| 代码已生成 | 是。模块化标准库 CLI，README、SKILL、配置、测试、手动工作流和 ZIP。 |
| 程序已测试 | 是。25 项自动测试通过；实际网络调用实际执行；JSON/CSV/HTML/SQLite 已生成。 |
| 真实网站已验证 | 部分。取得真实商品报价/库存字段与公开促销线索；未完成所有费用及购物车验证，无可认定的最低确定到手价。 |
| 持续监控已部署 | 否。未创建远程仓库、未运行远程 Actions、无定时任务。 |

## 商品网页交叉检查

- Bemmel en Kroon：https://www.bemmelenkroon.nl/merken/aeg/tr738at2b-aego/ 。实际 JSON-LD 为 EUR 645、InStoreOnly。可见商品主体为 Showroommodel。按展示机及门店库存处理，不能当全新可送货的最低价。
- Keukenloods：https://www.keukenloods.nl/product/aeg-tr738at2b-wasdroger-aego/ 。实际 EUR 645，JSON-LD Discontinued，主体 Nooit meer leverbaar。排除。配件/其他型号的“有货”不计入目标商品。
- EP：旧 URL 返回301，第一次脚本按策略停止。通过公开网页查得最终产品 URL https://www.ep.nl/product/aeg-tr738at2b-1429265 ，网页读取显示 EUR 849；这是网页观察而非已确认完整到手价。已更新配置后重新运行，脚本确实取得第三条真实报价；费用/配送未齐全，仍未列入确定排名。
- AEG 官网目标旧 URL 返回301，脚本未追踪；搜索/网页核对确认产品为热泵机，不将官方规格页视为可下单库存证明。

## 优惠与返现

- 官方 https://www.aeg.nl/local/promotions/laundry-cashback/ 有参与型号返现活动；没有确认这个具体 EAN、具体商家和展示机条件符合，因此未分配确定返现。
- https://www.cashbackxl.nl/webshops/aeg 读取到 AEG 返现页面，公开网页标明上限7%、计价不含 VAT/运费等条件；未确认这次订单、外部码及商家资格，未计算确定收益。
- ShopBuddies 实际被 robots 拒绝，未绕过。
- Pepper/mydealz 所试 AEG 链接返回410，未声称查遍两站。
- https://www.vouchercodes.nl/aeg.nl 公开页面有会员、Newsletter和代码线索；均第三方 C，未购物车测试，**没有 A 级已验证优惠**。
- Reddit：https://www.reddit.com/r/BIFLNL/comments/1r7x2fr/wasdroger_gezocht/ ，网页显示约8个月前发布，只有购买讨论，不是价格、库存或有效优惠证明。发布时间未取得精确日。
- 对小红书、YouTube、TikTok 进行了带域名的公开搜索，没有取得可核实、适用荷兰目标 SKU 的优惠内容；未虚构博主推荐或发布时间。CLI 无这些平台的专项适配器。

## 程序实际使用的数据来源

Python 通过 urllib 的公开 HTTPS + robots 检查，解析真实商品 JSON-LD 与可见 HTML，采集公开优惠线索。没有接通付费 API、官方价格 API、私人 Feed、第三方价格历史 API或大模型 API。没有 Playwright 运行或购物车操作。所有上游审计材料只读取。

网络报告分别为 reports/live 与 reports/europe；原始命令日志 live-run.log、europe-run.log；测试输出 tests.txt。数据失败日志里包含实际错误及时间。商家搜索结果不完整时，不声称该国无货。

## 仍未完成

完整自动购物车优惠验证、JS 动态商家专用适配器、自动合法配送/VAT/服务条款判断、多渠道用户资格/优惠叠加判定、自动 SKU 关联返现、可靠的跨站发现和商家信誉核验仍需后续实现。现阶段不是完整的无人值守“全欧洲最低价 Agent”。严格验证门槛使本次**确定到手价排名为空**，不会输出虚构最低价。

GitHub 账号连接存在，当前工具清单无 create repository，shell 无 gh；未获得可创建私人仓库的 API 凭证或端点，不能声称已部署。没有检查 GitHub 账单/分钟数，不启用计时任务。ZIP 是完整交付方式。
