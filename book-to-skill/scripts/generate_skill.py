#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill 文件生成脚本

功能说明:
    基于 16 个问题的分析结果，生成标准化的 Skill 文件结构。
    包括 SKILL.md 主文件、必要的脚本目录和配置文件。

功能特性:
    - 根据分析结果生成 SKILL.md
    - 自动创建标准目录结构
    - 生成配套的配置文件
    - 支持自定义模板

参数说明:
    --analysis: 分析结果 JSON 文件路径（由 analyze_book.py 生成）
    --output: Skill 输出目录
    --template: 自定义模板文件（可选）

使用示例:
    python generate_skill.py --analysis ./analysis.json --output ./my-skill
    python generate_skill.py --analysis ./analysis.json --output ./my-skill --template ./custom_template.md
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List


def sanitize_skill_name(name: str) -> str:
    """
    清理并格式化 Skill 名称

    将书名转换为适合作为 Skill 名称的格式：
    - 中文书名自动转为拼音（需要 pinyin 库）
    - 转换为小写
    - 替换空格为连字符
    - 移除特殊字符

    参数:
        name: 原始书名（支持中文和英文）

    返回:
        格式化后的英文 Skill 名称

    使用示例:
        sanitize_skill_name("思考快与慢")       # => "si-kao-kuai-yu-man"
        sanitize_skill_name("The Art of War")   # => "art-war"
        sanitize_skill_name("Clean Code")        # => "clean-code"
    """
    # 检测是否包含中文字符，如果是则转为拼音
    if re.search(r'[\u4e00-\u9fff]', name):
        try:
            from xpinyin import Pinyin
            p = Pinyin()
            name = p.get_pinyin(name, splitter='-')
        except ImportError:
            # pinyin 未安装时的回退方案：使用 hash
            import hashlib
            short_hash = hashlib.md5(name.encode()).hexdigest()[:6]
            name = f"book-{short_hash}"
            print(f"  提示: 安装 xpinyin 库可获得更好的中文书名转换效果 (pip install xpinyin)")

    # 转换为小写
    name = name.lower()
    # 替换常见英文连接词
    name = re.sub(r'\s+(and|or|the|a|an|in|on|at|to|for|of|with)\s+', '-', name)
    # 替换空格和特殊字符为连字符
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '-', name)
    # 移除首尾连字符
    name = name.strip('-')
    return name


def _join_list(items: list, prefix: str = "- ", default: str = "*暂无*") -> str:
    """
    安全地连接列表项为字符串，空列表时返回默认值

    参数:
        items: 待连接的字符串列表
        prefix: 每项前缀（默认 "- "）
        default: 列表为空时的默认返回值（默认 "*暂无*"）

    返回:
        连接后的字符串，或默认值

    使用示例:
        _join_list(["a", "b"])  # => "- a\\n- b"
        _join_list([])          # => "*暂无*"
    """
    if not items:
        return default
    return "\n".join(prefix + str(item) for item in items)


def generate_skill_description(analysis: Dict[str, Any]) -> str:
    """
    生成 Skill 描述

    基于问题 1 和 16 的分析结果，生成 Skill 的 description 字段。

    参数:
        analysis: 包含 16 个问题答案的分析结果

    返回:
        格式化的描述字符串

    使用示例:
        analysis = {"q1_book_positioning": {...}, "q16_skill_usage": {...}, "book_title": "书名"}
        desc = generate_skill_description(analysis)
    """
    q1 = analysis.get("q1_book_positioning", {})
    q16 = analysis.get("q16_skill_usage", {})

    problem = q1.get("problem_solved", "")
    audience = q1.get("target_audience", "")
    scenarios = q16.get("typical_scenarios", [])

    # 将场景列表转为逗号分隔的内联文本
    scenarios_text = "；".join(scenarios[:5]) if scenarios else "待补充"

    description = (
        f"基于《{analysis.get('book_title', '未知书籍')}》的方法论 Skill。"
        f"解决核心问题：{problem}。"
        f"适合人群：{audience}。"
        f"典型使用场景：{scenarios_text}。"
    )

    return description



def render_template(template: str, analysis: Dict[str, Any]) -> str:
    """
    使用简单变量替换渲染模板
    
    支持 {{ variable }} 和 {{ variable|default }} 语法
    
    参数:
        template: 模板字符串
        analysis: 分析数据字典
        
    返回:
        渲染后的字符串
    """
    import re
    
    def replace_var(match):
        var_expr = match.group(1).strip()
        # 处理带默认值的语法: var|default
        if '|' in var_expr:
            var_name, default_val = var_expr.split('|', 1)
            var_name = var_name.strip()
            default_val = default_val.strip().strip('"').strip("'")
        else:
            var_name = var_expr
            default_val = ""
        
        # 支持嵌套访问，如 q1_book_positioning.problem_solved
        keys = var_name.split('.')
        value = analysis
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, default_val)
            else:
                value = default_val
                break
        
        return str(value) if value is not None else default_val
    
    # 替换 {{ variable }} 格式
    result = re.sub(r'\{\{\s*(.+?)\s*\}\}', replace_var, template)
    return result


def generate_skill_md(analysis: Dict[str, Any], template_content: str = None) -> str:
    """
    生成 SKILL.md 内容

    基于 16 个问题的分析结果，生成完整的 SKILL.md 文件内容。
    包含 YAML frontmatter、概述、快速上手、核心方法、使用指南等区块。

    参数:
        analysis: 包含 16 个问题答案的分析结果

    返回:
        SKILL.md 文件内容

    使用示例:
        analysis = json.load(open("analysis.json"))
        md_content = generate_skill_md(analysis)
    """
    # 如果提供了自定义模板，使用模板渲染
    if template_content:
        return render_template(template_content, analysis)
    
    skill_name = analysis.get("skill_name", "book-method")
    book_title = analysis.get("book_title", "未知书籍")
    book_author = analysis.get("book_author", "未知作者")

    description = generate_skill_description(analysis)

    # 获取各个问题的答案
    q1 = analysis.get("q1_book_positioning", {})
    q2 = analysis.get("q2_method_steps", {})
    q3 = analysis.get("q3_core_rules", {})
    q4 = analysis.get("q4_warnings", {})
    q5 = analysis.get("q5_key_questions", {})
    q6 = analysis.get("q6_applicable_scenarios", {})
    q7 = analysis.get("q7_prerequisites", {})
    q8 = analysis.get("q8_expected_output", {})
    q9 = analysis.get("q9_validation", {})
    q10 = analysis.get("q10_core_principles", {})
    q11 = analysis.get("q11_resources", {})
    q12 = analysis.get("q12_learning_path", {})
    q13 = analysis.get("q13_variations", {})
    q14 = analysis.get("q14_advanced_tips", {})
    q15 = analysis.get("q15_ai_assistance", {})
    q16 = analysis.get("q16_skill_usage", {})

    # --- 快速上手区块 ---
    quick_steps = q2.get('steps', [])
    quick_steps_text = ""
    if quick_steps:
        quick_lines = []
        for i, step in enumerate(quick_steps[:5], 1):
            quick_lines.append(f"{i}. **{step.get('name', f'步骤 {i}')}**")
        quick_steps_text = "\n".join(quick_lines)
    else:
        quick_steps_text = "1. 准备好必要工具\n2. 按照下方核心方法的步骤执行"

    top_rules = q3.get('core_rules', [])[:3]
    top_rules_text = ("\n".join('- ' + rule for rule in top_rules)) or '*暂无*'

    skill_md = f"""---
name: {skill_name}
description: {description}
---

# {book_title} - 方法论 Skill

> 基于 {book_author} 的《{book_title}》
>
> 本 Skill 仅供个人学习使用

## 概述

### 解决什么问题
{q1.get('problem_solved', '待补充')}

### 目标受众
{q1.get('target_audience', '待补充')}

### 核心收益
{_join_list(q1.get('key_benefits', []))}

---

## 快速上手

> 一句话概括：{q1.get('problem_solved', '待补充')}

**最简使用流程：**
{quick_steps_text}

**核心原则速记：**
{top_rules_text}

---

## 核心方法

### 方法步骤

"""

    # 添加步骤
    steps = q2.get('steps', [])
    for i, step in enumerate(steps, 1):
        skill_md += f"""#### 步骤 {i}: {step.get('name', f'步骤 {i}')}

{step.get('description', '待补充')}

**具体操作：**
{_join_list(step.get('actions', []))}

**依赖关系：** {step.get('dependencies', '无')}

---

"""

    # 预计算含有特殊前缀的列表文本（避免 f-string 内使用反斜杠）
    _nl = "\n"
    core_rules_text = (_nl.join('- **' + rule + '**' for rule in q3.get('core_rules', []))) or '*暂无*'
    warnings_text = (_nl.join('- ⚠️ ' + warning for warning in q4.get('warnings', []))) or '*暂无*'
    checklist_text = (_nl.join('- [ ] ' + item for item in q9.get('checklist', []))) or '*暂无*'
    key_questions_text = (_nl.join(str(i+1) + '. ' + q for i, q in enumerate(q5.get('key_questions', [])))) or '*暂无*'
    advanced_tips_text = (_nl.join('- **' + tip.get('name', '技巧') + '**: ' + tip.get('description', '') for tip in q14.get('advanced_techniques', []))) or '*暂无*'
    ai_steps_text = (_nl.join('- **' + step + '**: 可由 AI 协助完成' for step in q15.get('ai_suitable_steps', []))) or '*暂无*'

    skill_md += f"""### 核心原则

{core_rules_text}

### 注意事项与警告

{warnings_text}

**避坑指南：**
{_join_list(q4.get('avoidance_tips', []))}

---

## 使用指南

### 适用场景

✅ **推荐使用：**
{_join_list(q6.get('applicable_scenarios', []))}

❌ **不推荐使用：**
{_join_list(q6.get('inapplicable_scenarios', []))}

### 前置准备

**知识准备：**
{_join_list(q7.get('knowledge_prep', []))}

**工具准备：**
{_join_list(q7.get('tools_prep', []))}

**环境准备：**
{_join_list(q7.get('environment_prep', []))}

### 预期产出

**直接产出：**
{q8.get('direct_output', '待补充')}

**阶段性产出：**
{_join_list(q8.get('milestone_outputs', []))}

**成功标准：**
{_join_list(q8.get('success_criteria', []))}

### 检验标准

{q9.get('validation_description', '待补充')}

**自测清单：**
{checklist_text}

---

## 深入理解

### 核心原理

{q10.get('theoretical_basis', '待补充')}

**为什么有效：**
{q10.get('why_it_works', '待补充')}

### 关键提问

在使用此方法时，请思考以下问题：

{key_questions_text}

---

## 实践资源

### 配套工具与模板

**工具清单：**
{_join_list(q11.get('tools', []))}

**模板：**
{_join_list(q11.get('templates', []))}

**参考案例：**
{_join_list(q11.get('cases', []))}

### 学习路径

**入门阶段：**
{_join_list(q12.get('beginner_steps', []))}

**进阶路径：**
{_join_list(q12.get('advanced_steps', []))}

**关键里程碑：**
{_join_list(q12.get('milestones', []))}

### 方法变体

**常见变体：**
{_join_list(q13.get('common_variations', []))}

**场景调整：**
{_join_list(q13.get('scenario_adjustments', []))}

### 进阶技巧

{advanced_tips_text}

---

## AI 辅助建议

### 适合 AI 辅助的步骤

{ai_steps_text}

### 人机协作模式

{q15.get('human_ai_collaboration', '待补充')}

### 自动化机会

{_join_list(q15.get('automation_opportunities', []))}

---

## Skill 使用说明

### 典型调用场景

{_join_list(q16.get('typical_scenarios', []))}

### 触发条件

当用户出现以下情况时，触发此 Skill：
{_join_list(q16.get('trigger_conditions', []))}

### 输入参数

{_join_list(q16.get('input_parameters', []))}

### 输出格式

{q16.get('output_format', '根据具体场景提供相应的输出')}

---

## 参考资料

- 原书：《{book_title}》
- 作者：{book_author}
- 免责声明：本 Skill 基于原书内容提炼，仅供个人学习使用
"""

    return skill_md


def create_skill_structure(output_dir: str, skill_name: str, skill_md_content: str):
    """
    创建 Skill 目录结构

    只创建核心的 SKILL.md 文件。
    子目录（scripts/、references/、assets/）仅在 skill 实际包含对应文件时按需创建。

    参数:
        output_dir: 输出目录
        skill_name: Skill 名称
        skill_md_content: SKILL.md 内容

    使用示例:
        create_skill_structure("./output", "my-skill", md_content)
    """
    skill_dir = Path(output_dir) / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)

    # 只写入 SKILL.md（核心文件）
    skill_md_path = skill_dir / "SKILL.md"
    with open(skill_md_path, 'w', encoding='utf-8') as f:
        f.write(skill_md_content)

    print(f"已创建 Skill: {skill_dir}/SKILL.md")


def main():
    """
    主函数

    解析命令行参数，读取分析结果 JSON 文件，生成 Skill 目录结构和 SKILL.md 文件。

    使用示例:
        python generate_skill.py --analysis ./analysis.json --output ./my-skill
        python generate_skill.py -a ./analysis.json -o ./my-skill -t ./template.md
    """
    parser = argparse.ArgumentParser(description='基于分析结果生成 Skill 文件')
    parser.add_argument('--analysis', '-a', required=True, help='分析结果 JSON 文件路径')
    parser.add_argument('--output', '-o', required=True, help='Skill 输出目录')
    parser.add_argument('--template', '-t', help='自定义模板文件（可选）')

    args = parser.parse_args()

    # 验证输入文件
    if not os.path.exists(args.analysis):
        print(f"错误: 分析文件不存在: {args.analysis}")
        sys.exit(1)

    # 读取分析结果
    print(f"读取分析结果: {args.analysis}")
    with open(args.analysis, 'r', encoding='utf-8') as f:
        analysis = json.load(f)

    # 生成 Skill 名称
    book_title = analysis.get('book_title', 'book-method')
    skill_name = sanitize_skill_name(book_title)
    analysis['skill_name'] = skill_name

    print(f"书籍: {book_title}")
    print(f"Skill 名称: {skill_name}")

    # 读取自定义模板（如果提供）
    template_content = None
    if args.template:
        if not os.path.exists(args.template):
            print(f"错误: 模板文件不存在: {args.template}")
            sys.exit(1)
        with open(args.template, 'r', encoding='utf-8') as f:
            template_content = f.read()
        print(f"使用自定义模板: {args.template}")
    
    # 生成 SKILL.md 内容
    print("生成 SKILL.md 内容...")
    skill_md_content = generate_skill_md(analysis, template_content)

    # 创建 Skill 结构
    print("创建 Skill 目录结构...")
    create_skill_structure(args.output, skill_name, skill_md_content)

    print(f"\n完成！Skill 已生成在: {Path(args.output) / skill_name}")


if __name__ == '__main__':
    main()
