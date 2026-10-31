# 投资研究工作区通用行为规则（Investment Research Rules）

1. **真实数据第一原则（Ground Truth First）**：
   - 严禁在财务报表、分部数据、营收、净利润、EPS、毛利率等关键指标中使用未经核实的幻觉数据。
   - 在进行估值或撰写投资评级时，必须基于标的**当前最新真实交易价格（Current Market Price）**进行推演，不得使用过时的历史价格。
2. **信披“双轨制”穿透原则（SEC Filings + Call Transcripts）**：
   - 历史客观财务数据（如分部营收、现金流、资产负债表）必须穿透至 **SEC 官方文件（Form 8-K / 10-Q / 10-K）**；
   - 重大前瞻指引、行业景气度及潜在超预期变量，必须穿透至 **官方电话会实录（Earnings Call Transcript，如 Q4/FactSet 官方纪要）** 的管理层口头陈述与分析师 Q&A，严禁单纯依赖新闻摘要或通用大模型二道贩运。
3. **财年（Fiscal Year）规范**：
   - 对于非自然年结算的公司（如 NVDA、MSFT、AAPL 等），必须在财报与研报中显式注明 Fiscal Period 与自然日历区间的对应关系。
4. **结构完整性与证伪约束**：
   - 每份研报必须遵循 `templates/` 中的标准框架，必须包含明确的「核心投资 Thesis」、「反向证伪条件」与「三情景估值（Bear/Base/Bull）」。
5. **微信公众号与墨滴排版规范（WeChat & mdnice Compliance）**：
   - 凡涉及输出至微信公众号或使用墨滴 (mdnice) 排版的内容（包括专栏文章及个股实战附录），必须 100% 遵守 [.agents/rules/wechat-publishing-rules.md](file:///Users/siyi/Documents/code/investment-research/.agents/rules/wechat-publishing-rules.md) 与全局母版 [articles/WECHAT_MDNICE_STYLEGUIDE.md](file:///Users/siyi/Documents/code/investment-research/articles/WECHAT_MDNICE_STYLEGUIDE.md)，严格执行加粗防崩四大军规与零 LaTeX 原则。
6. **研报语言风格规范（客观、克制、事实驱动，杜绝说教与情绪化强调）**：
   - **全面保持客观、克制、事实驱动的专业研报风格**，以第三方审慎评估视角陈述事实与逻辑，绝不充当狂热多头或情绪化宣泄者；
   - **严禁作者自我辩白与说教式过渡**：如“一旦这个...确立，全部迎刃而解且极度直观”、“买方最忌讳...”、“买方分析必须保持清醒”等，直接以客观事实与计算清单陈述；
   - **杜绝主观强调词与情绪化词汇**：如“唯一”、“唯一合成”、“终审买方合成”、“爆发式产生”、“极其/极度”、“牢不可破”、“绝对”等。估值体系统一使用“公允目标价”或“综合公允目标价”，盈亏比使用“基准风险收益比”；
   - **数据指标必须溯源清晰、前后勾稽一致**：盈亏比计算中的“悲观防御底（Downside Floor）”必须显式标注其来源（即第五幕正向推演中的 Bear Case 熊市情景内在价值底线），严禁凭空出现未在上下文推导的价格。
