---
name: interview-prep
description: 生成预测面试题库、答题话术策略、打磨自我介绍。触发词：面试会问什么、准备面试题、面试话术、怎么回答离职原因、自我介绍、STAR、面试重点、面试前准备什么、行为题、压力面。
version: 2.0.0
---

# 面试备战 Interview Prep

## 输入
- 优化后的简历 / JD（来自 `resume-optimizer` 最佳）
- 目标岗位、级别、公司类型
- 用户自评薄弱点

## 共享口径（必读）
- 表达框架：`references/star-framework.md`
- 行业题型/重点：`references/industry-templates.md`
- 薪资参考（期望薪资题用）：`references/salary-bands.md`
- 诚信红线：`references/redlines.md`

## 模块一：题库预测
按岗位+级别生成 3 类题（题型侧重见 industry-templates）：
- 技术/专业题：基于 JD 能力模型推导。
- 行为题：STAR 考察软技能（冲突/失败/领导力/优先级）。
- HR/老板题：动机/规划/期望薪资/为什么是我们/管理商业思维。
分层：高频必考 / 进阶 / 压力。

## 模块二：话术策略
- STAR/STAR-L 框架（见 star-framework），给"回答结构"而非背稿。
- 刁钻题结构：
  - 离职原因：聚焦发展，不贬前司。
  - 缺点：真实+已改进，形成闭环。
  - 空窗期：正面叙事。
  - 期望薪资：先反问区间，给薪资参考（salary-bands），留弹性。
  - 没做过的项目：邻近经验迁移+学习力。
- 红线（redlines）：不造假、不泄密、不贬低。

## 模块三：自我介绍
按角色出 3 版（结构见 star-framework）：
- 技术面：技术深度+项目复杂度（1–2 分钟）
- HR 面：稳定性+动机+成长（1 分钟）
- 老板/终面：业务理解+ownership+商业结果（2–3 分钟）
每版给「结构+范例片段」。

## 输出格式
```
【预测题库】分层（技术/行为/HR）
【话术策略】框架 + 刁钻题结构
【自我介绍】3 版（技术/HR/老板）
【下一步】调用 mock-interview 实战演练
```

## 关联
- 上游：`resume-optimizer` / `company-research`
- 下游：`mock-interview`
