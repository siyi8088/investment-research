# 📈 机构级买方投资研究知识库 (Investment Research Hub)

> 专注于基本面深度投研、真实造血质量穿透、预期投资学逆向求解、严苛压力测试与非价格证伪的机构级买方投研体系。

---

## 🧭 投研体系与目录结构

```text
investment-research/
├── .agents/                # [机构买方投研智能体规范与技能中枢]
│   ├── skills/
│   │   ├── investment-analyst/     # [主中枢] 证券投研总揽协议与数据信披基石 (零幻觉政策、标准交付格式)
│   │   ├── financial-forensics/    # [排雷与穿透] 真实造血质量穿透 (CFO瀑布、SBC稀释、CCC飞轮、EV桥)
│   │   ├── valuation-engine/       # [估值引擎] 预期投资学逆向DCF求解器 (市价倒推隐含CAGR、三情景建模)
│   │   └── investment-memo/        # [风控决策] 买方投资备忘录 (事前验尸、非价格证伪红线、六维雷达量规)
│   └── rules/investment-rules.md  # 投研通用数据规范与财年对齐规则
├── README.md               # [全局索引] 覆盖标的看板与总览
├── companies/              # [个股深度主档案、历季财报与买方备忘录]
│   ├── NVDA/                 # 英伟达 (AI算力系统级垄断者 / 核心底仓 / 备忘录 55.0分)
│   ├── AMZN/                 # 亚马逊 (负CCC营运资本飞轮 / AWS盈利拐点 / 备忘录 50.5分)
│   ├── AXP/                  # 美国运通 (闭环高端会员生态 / 极低隐含增速 / 备忘录 53.0分)
│   ├── AVGO/                 # 博通 (定制ASIC与网络物理层垄断 / 45% FCF利润率 / 备忘录 47.5分)
│   ├── GLW/                  # 康宁 (AI高密光纤光互连 / 真实造血修复 / 备忘录 49.0分)
│   ├── VRT/                  # 维谛技术 (AI数据中心液冷绝对龙头 / 逢低击球区 / 备忘录 47.5分)
│   ├── NOK/                  # 诺基亚 ($30.8亿净现金 / Infinera整合与指数重返 / 备忘录 46.0分)
│   ├── QCOM/                 # 高通 (汽车数字底盘高增 / AI PC突破 / 备忘录 52.0分)
│   ├── BA/                   # 波音 (300天在制品积压 / 估值透支 / 观察池等待深度安全边际)
│   ├── INTC/                 # 英特尔 (重资产折旧承压 / IFS微利拐点 / 观察池等待击球区)
│   ├── VST/                  # Vistra (电力公用事业 / AI算力核电基建 / SOTP估值)
│   ├── GE/                   # GE Aerospace (航空航天动力 / 航发后市场维修SOTP)
│   ├── KLAC/                 # KLA Corp (半导体良率控制 / 过程控制SOTP)
│   └── FN/                   # Fabrinet (高端精密光学制造 / AI光互连SOTP)
│       ├── README.md         # 个股投研中枢主档案 (穿透财务质量、CCC、EV桥、逆向DCF预期差)
│       ├── earnings/         # 历季财报深度复盘 (FY2026-Q2.md 等)
│       └── research/         # 买方投资备忘录 (investment-memo.md、六维评估雷达图)
├── templates/              # [投研模板库]
│   ├── template-company.md   # 个股全景主档案模板
│   ├── template-earnings.md  # 季度财报追踪模板
│   └── template-research.md  # 深度专题与估值模型模板
├── industries/             # [行业研究] 上下游产业链与行业全景图
└── frameworks/             # [投资框架] 估值方法论、仓位管理、投资清单与心法
```

---

## 📊 覆盖标的看板 (Coverage Universe)

| 标的代码 (Ticker) | 公司名称 | 所属行业 | 覆盖状态 | 买方投资评级 | 现价基准 | Base Case 目标价 | 潜在空间 | 六维量规总分 | 最新财报 | 最近更新 |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| [**NVDA**](companies/NVDA/README.md) | NVIDIA Corporation | 半导体 / AI 算力系统 | **持仓** | **强烈看多 (核心底仓)** | **$217.00** | **$350.00** | **+61.3%** | **55.0 / 60.0** (PROCEED) | [FY27 Q2](companies/NVDA/earnings/FY2027-Q2.md) | 2026-10-04 |
| [**AXP**](companies/AXP/README.md) | American Express | 闭环支付网络 / 会员经济 | **重点跟踪** | **强烈看多 (核心底仓)** | **$275.50** | **$383.80** | **+39.3%** | **53.0 / 60.0** (PROCEED) | [FY26 Q2](companies/AXP/earnings/FY2026-Q2.md) | 2026-10-04 |
| [**AMZN**](companies/AMZN/README.md) | Amazon.com, Inc. | 云计算与AI / 零售 / 广告 | **重点跟踪** | **强烈看多 (核心底仓)** | **$256.78** | **$328.23** | **+27.8%** | **50.5 / 60.0** (PROCEED) | [FY26 Q2](companies/AMZN/earnings/FY2026-Q2.md) | 2026-10-04 |
| [**GLW**](companies/GLW/README.md) | Corning Incorporated | AI光通信互连 / 特种材料 | **重点跟踪** | **强烈看多 (稳健配置)** | **$149.79** | **$175.00** | **+16.8%** | **49.0 / 60.0** (PROCEED) | [FY26 Q2](companies/GLW/earnings/FY2026-Q2.md) | 2026-10-04 |
| [**AVGO**](companies/AVGO/README.md) | Broadcom Inc. | 定制半导体 / 企业级软件 | **重点跟踪** | **重点跟踪 (买入)** | **$378.00** | **$475.00** | **+25.7%** | **47.5 / 60.0** (PROCEED) | [FY26 Q3](companies/AVGO/earnings/FY2026-Q3.md) | 2026-10-04 |
| [**VRT**](companies/VRT/README.md) | Vertiv Holdings Co | AI算力温控 / 液冷与供电 | **重点跟踪** | **重点跟踪 (逢低布局)** | **$245.00** | **$289.49** | **+18.2%** | **47.5 / 60.0** (PROCEED) | [FY26 Q2](companies/VRT/earnings/FY2026-Q2.md) | 2026-10-04 |
| [**QCOM**](companies/QCOM/README.md) | Qualcomm Incorporated | 边缘AI计算 / 汽车底盘 / 专利池 | **重点跟踪** | **重点买入 (核心配置)** | **$184.87** | **$245.00** | **+32.5%** | **52.0 / 60.0** (PROCEED) | [FY26 Q3](companies/QCOM/earnings/FY2026-Q3.md) | 2026-10-05 |
| [**NOK**](companies/NOK/README.md) | Nokia Corporation | AI全光网基建 / 专利许可 | **重点跟踪** | **强烈看多 (稳健配置)** | **$8.82** | **$14.20** | **+61.0%** | **46.0 / 60.0** (PROCEED) | [FY26 Q2](companies/NOK/earnings/FY2026-Q2.md) | 2026-10-04 |
| [**BA**](companies/BA/README.md) | The Boeing Company | 商用大飞机 / 航空防务 | **观察池** | **观察 (等待安全边际)** | **$198.20** | **$217.80** | **+9.9%** | **38.5 / 60.0** (WAIT) | [FY26 Q2](companies/BA/earnings/FY2026-Q2.md) | 2026-10-04 |
| [**INTC**](companies/INTC/README.md) | Intel Corporation | x86芯片设计 / 晶圆代工 | **观察池** | **观察 (等待安全边际)** | **$105.00** | **$130.00** | **+23.8%** | **40.5 / 60.0** (WAIT) | [FY26 Q2](companies/INTC/earnings/FY2026-Q2.md) | 2026-10-04 |
| [**VST**](companies/VST/README.md) | Vistra Corp. | 电力公用事业 / AI算力基建 | **重点跟踪** | **强烈看多** | **$148.38** | **$186.04** | **+25.4%** | - | [FY26 Q2](companies/VST/earnings/FY2026-Q2.md) | 2026-09-13 |
| [**GE**](companies/GE/README.md) | GE Aerospace | 航空航天动力 / 后市场维修 | **重点跟踪** | **审慎看多** | **$323.66** | **$365.00** | **+12.8%** | - | [FY26 Q2](companies/GE/earnings/FY2026-Q2.md) | 2026-09-13 |
| [**KLAC**](companies/KLAC/README.md) | KLA Corporation | 半导体良率与过程控制设备 | **重点跟踪** | **审慎看多** | **$168.02** | **$180.67** | **+7.5%** | - | [FY26 Q4](companies/KLAC/earnings/FY2026-Q4.md) | 2026-09-16 |
| [**FN**](companies/FN/README.md) | Fabrinet | 高端精密光学与AI光互连制造 | **重点跟踪** | **强烈看多** | **$374.91** | **$442.08** | **+17.9%** | - | [FY26 Q4](companies/FN/earnings/FY2026-Q4.md) | 2026-09-17 |

> **状态说明**：`持仓` (核心底仓头寸) / `重点跟踪` (进入深度买入或加仓击球区) / `观察池` (等待估值出清或右侧催化) / `已清仓` / `暂不关注`

---

## 🛠️ 买方投研四大核心基石与标准化工作流

本知识库全面遵循升级后的 **4-Skill 机构买方投研标准体系**：

### 1. 真实财务排雷与造血穿透（`financial-forensics`）
- **CFO 转化率审计**：剔除 GAAP/Non-GAAP 水分，强制核算过去 5 年连续经营现金流（CFO）对净利润（NI）的转化率；
- **SBC 股权稀释穿透**：将股权激励视为真实人力成本，比对回购消耗量与股本净变化；
- **CCC 营运资本飞轮**：计算存货天数（DSI）、应收天数（DSO）与应付天数（DPO），甄别无息商业浮存金与存货积压；
- **Pro Forma EV 桥**：核算完全稀释总股本、市场价、净负债/净现金与企业价值。

### 2. 估值与预期投资学引擎（`valuation-engine`）
- **逆向 DCF 求解器**：绝不盲目套用正向估值，首先从当前市价倒推市场隐含的未来 10 年自由现金流复合年化增速（10-Yr FCF CAGR）；
- **预期差四象限归类**：比对隐含增速与历史业绩、管理层军令状的剪刀差，锁定处于“低预期/低估值”的不对称资产；
- **正向三情景建模**：严格区分 Bear（悲观防御）、Base（基准中枢）、Bull（乐观爆发）三种情景，避免单一孤立预测。

### 3. 买方决策与严苛风控备忘录（`investment-memo`）
- **双变量敏感性压力测试**：计算 WACC × 永续增长率 g，以及 EPS × P/E 倍数网格，探寻极端环境下的底线价值；
- **事前验尸（Pre-Mortem）**：在买入前强制推演标的未来的 **4 大致命死因**；
- **前置非价格客观证伪红线**：确立 3-4 条基于运营与财务数据的前置证伪指标，一旦触发坚决减仓清仓，杜绝沉没成本纠缠；
- **客观六维量规自查**：从真实造血、商业壁垒、资本分配、安全边际、非对称盈亏比、前置证伪度六大维度进行量化评分（及格线 45.0/60.0），并生成雷达评估图。

### 4. 证券投研总览与信披中枢（`investment-analyst`）
- **零幻觉政策（Zero-Hallucination Policy）**：所有财务数据与股价必须源自真实 SEC 财报与真实行情核实；
- **标准交付物规范（Standard Option A）**：每个个股研究统一形成：
  1. `companies/<TICKER>/README.md`：个股投研中枢主档案
  2. `companies/<TICKER>/earnings/`：历季财报复盘
  3. `companies/<TICKER>/research/investment-memo.md`：标准 7 步买方投资备忘录与六维雷达评估图

---

## 📑 常用模板快捷入口

- 📄 [个股主档案模板 (template-company.md)](templates/template-company.md)
- 📊 [季度财报追踪模板 (template-earnings.md)](templates/template-earnings.md)
- 🔬 [深度专题研究模板 (template-research.md)](templates/template-research.md)
