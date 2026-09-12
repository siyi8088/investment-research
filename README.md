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
├── companies/              # [公司研究] (以 Ticker 命名)
│   └── NVDA/
│       ├── README.md         # NVDA 主档案 (商业模式、全栈壁垒、三情景估值)
│       ├── earnings/         # 历季财报追踪 (FY2027-Q2.md / FY2026-Q2.md 等)
│       ├── research/         # 深度专题与估值模型 (DCF 模型、算力敏感性推演)
│       └── notes/            # 调研随手记、电话会速记
├── industries/             # [行业研究] 上下游产业链与行业全景图
└── frameworks/             # [投资框架] 估值方法论、仓位管理、投资清单与心法
```

---

## 📊 覆盖标的看板 (Coverage Universe)

| 标的代码 (Ticker) | 公司名称 | 所属行业 | 覆盖状态 | 当前观点 | 现价基准 | Base Case 目标价 | 潜在空间 | 最新财报 | 最近更新 |
|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [**NVDA**](companies/NVDA/README.md) | NVIDIA Corporation | 半导体 / AI 算力系统 | **持仓** | **看多** | **$217.00** | **$270.00** | **+24.4%** | [FY27 Q2](companies/NVDA/earnings/FY2027-Q2.md) | 2026-08-30 |

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
