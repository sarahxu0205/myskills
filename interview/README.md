# 简历优化 · 面试辅导 Skill 集合

本目录是一套面向「求职/面试」场景的协同 Skill 集合，由 1 个总控编排 Skill + 6 个专项 Skill 组成，覆盖面试全生命周期 **12 个能力点**。

## 总控（编排）
- `interview-coach`：按"投递前 → 面试前 → 面试后"生命周期路由到专项 Skill，保证环节闭环。

## 专项 Skill 与能力点映射
| 生命周期 | 能力点 | 专项 Skill |
|----------|--------|-----------|
| 投递前 | JD 诊断 / 简历优化 / 项目补全 | `resume-optimizer` |
| 投递前 | 公司背调 | `company-research` |
| 面试前 | 题库预测 / 话术策略 / 自我介绍 | `interview-prep` |
| 面试前 | 模拟面试 | `mock-interview` |
| 面试后 | 复盘 / 反向提问 | `interview-review` |
| 面试后 | Offer 谈判 / 进度追踪 | `offer-negotiation` |

## 各 Skill 自带 `references/`
为支持单 Skill 独立使用，每个 Skill 现已自带其所需的 `references/` 文件（不再是统一共享目录），避免重复定义、保证口径一致：
- `redlines.md`：诚信与边界红线（不造假、不泄密、不贬低、样例标注）。
- `star-framework.md`：STAR/STAR-L 表达与评分框架。
- `salary-bands.md`：薪资行情参考框架（结构 + 示例锚点）。
- `industry-templates.md`：按岗位（技术/产品/运营/数据/设计）的题型与重点。
- `ats-keywords.md`：ATS 关键词对齐指南。

各 Skill 实际携带的文件如下：
| Skill | 自带 references |
|-------|----------------|
| company-research | industry-templates, salary-bands |
| interview-coach | redlines, industry-templates, ats-keywords, salary-bands |
| interview-prep | industry-templates, redlines, salary-bands, star-framework |
| interview-review | redlines, star-framework |
| mock-interview | redlines, star-framework |
| offer-negotiation | redlines, salary-bands |
| resume-optimizer | ats-keywords, redlines, star-framework |

## 使用约定
- 专项 Skill 经 `interview-coach` 路由触发，也可由用户直接触发。
- 涉及 STAR/薪资/行业/ATS/红线时，由对应专项 Skill 读取其自身 `references/` 目录下的文件，不要重新定义。
- 任一环节产出后，按上表指向下一环，形成闭环。
