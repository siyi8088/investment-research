# 《买方估值实战案例》专栏案例库 (Case Studies Library)

> 本目录为《买方级估值修炼手册》专栏的**买方个股深度实战案例演练库**。  
> 理论依托专栏全套 14 篇方法论，数据依托 `companies/<TICKER>/` 个股深度研究底稿，以生成案例当天的实时股价为定价锚点，通过“标准七幕剧”深度解剖全球标杆巨头。

---

## 📘 生产与写作规范指南
* 📐 **标准化生产规程 (SOP)**：[CASE_STUDY_STANDARDS.md](file:///Users/siyi/Documents/code/investment-research/articles/valuation_guide/case_studies/CASE_STUDY_STANDARDS.md)
  * 包含：4 步快速生产流、实时股价获取与模型联动、爆款标题公式、正文“标准七幕剧”全息模板、微信 ＋ 墨滴排版格式红线、视觉资产规格与 10 项终检清单。

---

## 🗂️ 现有实战案例索引

| 序号 | 标的名称 (Ticker) | 案例文章与核心主题 | 核心商业模式与估值焦点 | 配套资产状态 |
| :---: | :--- | :--- | :--- | :---: |
| **01** | **台积电 (NYSE: TSM)** | [01_台积电TSM_买方估值与预期投资学实战.md](file:///Users/siyi/Documents/code/investment-research/articles/valuation_guide/case_studies/01_台积电TSM_买方估值与预期投资学实战.md) | 半导体物理垄断、不可退预付款护城河、反向 DCF 隐含 +10.4% 增速、**显性扣除 20% 地缘折价**、双网格承压测试。 | 2.35:1 封面 ✅<br>六维雷达图 ✅ |
| **02** | **通用电气航天 (NYSE: GE)** | [02_通用电气航天GE_买方估值与后市场商业模式实战.md](file:///Users/siyi/Documents/code/investment-research/articles/valuation_guide/case_studies/02_通用电气航天GE_买方估值与后市场商业模式实战.md) | “剃刀与刀片”后市场商业模式、CSA 协议 $180 亿无息客户 Float、反向 DCF 逆向求解、商用与防务 **SOTP 分部加总**、4 大死因事前验尸。 | 2.35:1 封面 ✅<br>六维雷达图 ✅ |
| **03** | **诺基亚 (NYSE: NOK)** | [03_诺基亚NOK_买方估值与AI光通信周期逆向实战.md](file:///Users/siyi/Documents/code/investment-research/articles/valuation_guide/case_studies/03_诺基亚NOK_买方估值与AI光通信周期逆向实战.md) | Q3 现金流由正转负“会计视错觉”硬核穿透（€4 亿战略备货垫资）、€25.8 亿净现金底牌、三大业务 SOTP 分部加总、非对称赔率 **4.64:1**。 | 2.35:1 封面 ✅<br>六维雷达图 ✅ |
| **04** | **波音 (NYSE: BA)** | [04_波音BA_买方估值与大飞机双寡头困境反转实战.md](file:///Users/siyi/Documents/code/investment-research/articles/valuation_guide/case_studies/04_波音BA_买方估值与大飞机双寡头困境反转实战.md) | 单日暴跌 -10.7% 利空出清与质量重置（新 CEO 铁腕“拒绝工序漂移”）、$7,450 亿天量在手积压、737-7/10 认证落地、三大军团 SOTP、一级击球区触发。 | 2.35:1 封面 ✅<br>六维雷达图 ✅ |

---

## 🛠️ 快速生产工作流速览
1. **信源定位**：打开 `companies/<TICKER>/research/investment-memo.md` 与季报纪要；
2. **实时市价**：采集当天最新收盘价，重新计算 EV Bridge、反向 DCF、三情景收益分布与盈亏比；
3. **视觉生成**：出图 2.35:1 宽屏封面至 `assets/cover_case{XX}_{ticker}_2.35x1.jpg`，准备雷达图 `assets/{ticker}_radar.png`；
4. **规范行文**：按照 [CASE_STUDY_STANDARDS.md](file:///Users/siyi/Documents/code/investment-research/articles/valuation_guide/case_studies/CASE_STUDY_STANDARDS.md) 七幕剧模板填入数据并进行买方哲学升华。

