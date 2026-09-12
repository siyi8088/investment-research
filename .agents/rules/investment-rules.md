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
