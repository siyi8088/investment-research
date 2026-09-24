# 📈 个人投资研究知识库 (Investment Research Hub)

> 专注于基本面深度投研、长期竞争壁垒追踪、财报预期差捕捉与估值定价的严谨投研体系。

---

## 🧭 投研体系与目录结构

```text
investment-research/
├── .agents/                # [投研智能体规范]
│   ├── skills/investment-analyst/SKILL.md  # 投研分析师规范（零幻觉政策、真实数据校验）
│   └── rules/investment-rules.md          # 投研通用数据与财年对齐规则
├── README.md               # [全局索引] 覆盖标的看板与总览
├── templates/              # [投研模板库]
│   ├── template-company.md   # 个股全景主档案模板
│   ├── template-earnings.md  # 季度财报追踪模板
│   └── template-research.md  # 深度专题与估值模型模板
├── companies/              # [个股深度档案与财报跟踪]
│   ├── NVDA/                 # 英伟达主档案与历季财报
│   ├── AVGO/                 # 博通主档案、Q3财报复盘与估值模型
│   ├── INTC/                 # 英特尔主档案、Q2财报复盘与SOTP分部估值模型
│   ├── VST/                  # Vistra 主档案、Q2财报复盘与核电SOTP估值模型
│   ├── AMZN/                 # 亚马逊主档案、Q2财报复盘与五大支柱SOTP估值模型
│   ├── GE/                   # GE Aerospace 主档案、Q2财报复盘与航发后市场SOTP估值模型
│   ├── KLAC/                 # KLA Corp 主档案、Q4全财年财报复盘与良率控制SOTP估值模型
│   ├── FN/                   # Fabrinet 主档案、Q4全财年财报复盘与AI光互连SOTP估值模型
│   ├── VRT/                  # Vertiv 主档案、Q2财报复盘与液冷温控/供电SOTP估值模型
│   ├── GLW/                  # Corning 主档案、Q2财报复盘与高密光通信/特种材料SOTP估值模型
│   ├── BA/                   # Boeing 主档案、Q2财报复盘与民航大飞机双寡头/防务SOTP估值模型
│   ├── NOK/                  # Nokia 主档案、Q2财报复盘与AI光网络/专利SOTP估值模型
│   └── AXP/                  # American Express 主档案、Q2财报复盘与闭环会员制估值模型
│       ├── README.md         # AXP 主档案 (闭环网络、客群年轻化65%、卡费增15.4%、ROE>30%)
│       ├── earnings/         # 历季财报复盘 (FY2026-Q2.md 等)
│       └── research/         # 深度专题与估值模型 (SOTP分部模型)
├── industries/             # [行业研究] 上下游产业链与行业全景图
└── frameworks/             # [投资框架] 估值方法论、仓位管理、投资清单与心法
```

---

## 📊 覆盖标的看板 (Coverage Universe)

| 标的代码 (Ticker) | 公司名称 | 所属行业 | 覆盖状态 | 当前观点 | 现价基准 | Base Case 目标价 | 潜在空间 | 最新财报 | 最近更新 |
|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [**NVDA**](companies/NVDA/README.md) | NVIDIA Corporation | 半导体 / AI 算力系统 | **持仓** | **强烈看多** | **$217.00** | **$350.00** | **+61.3%** | [FY27 Q2](companies/NVDA/earnings/FY2027-Q2.md) | 2026-09-12 |
| [**AVGO**](companies/AVGO/README.md) | Broadcom Inc. | 半导体定制算力 / 软件 | **重点跟踪** | **强烈看多** | **$361.99** | **$475.00** | **+31.2%** | [FY26 Q3](companies/AVGO/earnings/FY2026-Q3.md) | 2026-09-12 |
| [**INTC**](companies/INTC/README.md) | Intel Corporation | x86 芯片设计 / 晶圆代工 | **重点跟踪** | **审慎看多** | **$102.94** | **$130.00** | **+26.3%** | [FY26 Q2](companies/INTC/earnings/FY2026-Q2.md) | 2026-09-12 |
| [**VST**](companies/VST/README.md) | Vistra Corp. | 电力公用事业 / AI算力基建 | **重点跟踪** | **强力看多** | **$148.38** | **$186.04** | **+25.4%** | [FY26 Q2](companies/VST/earnings/FY2026-Q2.md) | 2026-09-13 |
| [**AMZN**](companies/AMZN/README.md) | Amazon.com, Inc. | 云计算与AI / 零售 / 广告 | **重点跟踪** | **强烈看多** | **$256.78** | **$328.23** | **+27.8%** | [FY26 Q2](companies/AMZN/earnings/FY2026-Q2.md) | 2026-09-13 |
| [**GE**](companies/GE/README.md) | GE Aerospace | 航空航天动力 / 后市场维修 | **重点跟踪** | **审慎看多** | **$323.66** | **$365.00** | **+12.8%** | [FY26 Q2](companies/GE/earnings/FY2026-Q2.md) | 2026-09-13 |
| [**KLAC**](companies/KLAC/README.md) | KLA Corporation | 半导体制造良率与过程控制 | **重点跟踪** | **审慎看多** | **$168.02** | **$180.67** | **+7.5%** | [FY26 Q4](companies/KLAC/earnings/FY2026-Q4.md) | 2026-09-16 |
| [**FN**](companies/FN/README.md) | Fabrinet | 高端精密光学与AI光互连制造 | **重点跟踪** | **强烈看多** | **$374.91** | **$442.08** | **+17.9%** | [FY26 Q4](companies/FN/earnings/FY2026-Q4.md) | 2026-09-17 |
| [**VRT**](companies/VRT/README.md) | Vertiv Holdings Co | AI算力基建 / 液冷温控与供电 | **重点跟踪** | **强烈看多** | **$239.41** | **$289.49** | **+20.9%** | [FY26 Q2](companies/VRT/earnings/FY2026-Q2.md) | 2026-09-17 |
| [**GLW**](companies/GLW/README.md) | Corning Incorporated | AI光通信高密互连 / 特种材料 | **重点跟踪** | **强烈看多** | **$149.79** | **$175.00** | **+16.8%** | [FY26 Q2](companies/GLW/earnings/FY2026-Q2.md) | 2026-09-19 |
| [**BA**](companies/BA/README.md) | The Boeing Company | 商用大飞机制造 / 航空防务军工 | **重点跟踪** | **审慎看多** | **$198.20** | **$217.80** | **+9.9%** | [FY26 Q2](companies/BA/earnings/FY2026-Q2.md) | 2026-09-20 |
| [**NOK**](companies/NOK/README.md) | Nokia Corporation | AI全光网基建 / 移动网 / 专利池 | **重点跟踪** | **强烈看多** | **$10.68** | **$14.20** | **+33.0%** | [FY26 Q2](companies/NOK/earnings/FY2026-Q2.md) | 2026-09-21 |
| [**AXP**](companies/AXP/README.md) | American Express | 闭环支付网络 / 高净值会员经济 | **重点跟踪** | **强烈看多** | **$301.96** | **$383.80** | **+27.1%** | [FY26 Q2](companies/AXP/earnings/FY2026-Q2.md) | 2026-09-24 |

> **状态说明**：`重点跟踪` (深度调研中) / `持仓` (已有头寸) / `观察` (列入 Watchlist) / `已清仓` / `暂不关注`

---

## 🛠️ 投研核心原则与工作流

1. **真实数据为本（Zero-Hallucination Policy）**：所有财务数据与股价必须经由真实财报与行情核实，绝不使用虚假/过时数字。
2. **Thesis 驱动**：每一次投资都必须有清晰的书面 Thesis（为什么买、看多什么变量）。
3. **反向证伪思维**：明确列出 *“发生什么情况代表我错了”*，不盲目沉没成本。
4. **预期差捕捉**：区分公司基本面的“好与坏”和市场预期的“高与低”，赚取预期差修复的钱。
5. **动态演变复盘**：每个季度财报追踪核心变量验证情况，记录 Thesis 的迭代轨迹。

---

## 📑 常用模板快捷入口

- 📄 [个股主档案模板 (template-company.md)](templates/template-company.md)
- 📊 [季度财报追踪模板 (template-earnings.md)](templates/template-earnings.md)
- 🔬 [深度专题研究模板 (template-research.md)](templates/template-research.md)
