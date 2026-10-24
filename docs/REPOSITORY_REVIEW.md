# GitHub 来源审核（2026-10-24）

审核方式：实际打开六个 GitHub 仓库，读取 GitHub 元数据、README、许可证及可获得的 SKILL.md/依赖清单。原始读取得到的文件保存在 docs/audit；ACCESS_FAILED 内容是失败记录，不是源码。未执行任何上游安装器、脚本或陌生代码，未复制上游实现代码进入运行模块。本项目采用独立标准库实现，只参考流程设计。

| 仓库 | 许可证（实际读取） | 技能/依赖检查 | 采用与拒绝 |
|---|---|---|---|
| https://github.com/OmarSaleh506/skills | MIT | 读取 skills/shop-scout/SKILL.md；依赖 Agent 搜索/读取能力，推荐 Firecrawl；README 与许可证已读。tree API 403，猜测的 backends.md 和 package.json 404，未视为真实存在。 | 采用含运费比较、无数据降级和商家信任证据思想；拒绝 cloud Firecrawl/stealth 后端、未经购物车验证就扣减优惠、按店铺优先而非到手价排序。未安装此技能。 |
| https://github.com/kirvahe/claude-buy-skill | MIT | 读取根 SKILL.md、README、LICENSE 和 tree。技能依赖 Playwright MCP；允许工具列表还含 Firecrawl、Exa、Telegram。配置/安全模式和购物流程是 Agent 指令，不是独立 Python 采集库。 | 采用研究/购物车/付款边界、配送总成本和审计思想；不启用 FULL checkout、Telegram、收费服务或自动注册。 |
| https://github.com/DaizeDong/shopping-aggregator | MIT | 读取 skills/shopping-aggregator/SKILL.md、README、LICENSE 和 tree。依赖宿主研究工具、外部配置/companion、fleet_guards 的账本验证等工作流；不是安装即可抓遍欧洲的网站服务。引用来源包括历史和优惠工具，免费资格须逐一验证。 | 采用证据分级、同版本、缺口报告、返现单列；不执行脚本、不使用 Keepa 等未经确认免费的接口、不移植个人配置或付款行为。 |
| https://github.com/microsoft/playwright-python | Apache-2.0 | README/LICENSE/pyproject/requirements/setup.py 和两个维护用 SKILL.md 已读；核心依赖 pyee 和 greenlet，浏览器二进制另装。维护 Skills 是发行/roll 工作流，不是购物技能。 | 合适的未来购物车浏览器方案；本次不安装，避免把未测试的浏览器能力说成已实现。 |
| https://github.com/scrapy/scrapy | BSD-3-Clause | README/LICENSE/pyproject 已读；tree API 403，未证明完整树无 SKILL.md。依赖 Twisted、cryptography、lxml、parsel、protego、w3lib 等。 | 借鉴模块化采集、robots、重试与限速设计；小规模 CLI 不引入此依赖树。 |
| https://github.com/apify/crawlee-python | Apache-2.0 | README/LICENSE/pyproject/tree 已读；核心含 pydantic、impit、protego 等；Playwright/BeautifulSoup 是可选依赖，存在付费平台及指纹相关可选模块。没有取得购物专用 SKILL.md。 | 借鉴适配器与可靠性结构；不启用 Apify 云、代理、指纹伪装或额外依赖。 |

审核范围是所列文件的许可证、声明依赖和工作流风险，**不是所有仓库全量代码安全审计，也不是全部传递依赖供应链审计**。未执行上游软件，所以无上游安装或运行成功主张。未额外选用其他未知仓库。公开仓库是存在性证据，不是其价格/库存能力真实有效的证明。

本项目原创运行代码仅用 Python 标准库，避免付费 API、模型、代理及第三方安装脚本。上游资料遵守各自原始许可证；audit 中含原 LICENSE。
