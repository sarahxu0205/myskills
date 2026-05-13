#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
book-to-skill 统一 Pipeline 入口

一键执行完整流程：
1. 提取 PDF 内容
2. AI 分析（提示用户生成 analysis.json）
3. 生成 Skill

功能特性:
    - 自动串联 extract → analyze → generate 三步
    - 支持跳过已完成的步骤
    - 提供详细的进度输出和错误处理
    - 支持自定义参数传递给各步骤

参数说明:
    input_path: 输入文件路径（PDF 或已有的 extraction_result.json）
    --output: 输出目录（默认 ./output）
    --skip-extract: 跳过提取步骤（输入为 extraction_result.json 时）
    --skip-generate: 跳过生成步骤（仅提取和分析）
    --max-pages: 最大处理页数
    --max-chars: full_text 最大字符数
    --chapter-scan-depth: 章节检测扫描行数
    --template: 自定义 SKILL.md 模板

使用示例:
    python run_pipeline.py book.pdf --output ./my-skill
    python run_pipeline.py book.pdf --output ./my-skill --max-chars 0
    python run_pipeline.py extraction_result.json --output ./my-skill --skip-extract
    python run_pipeline.py book.pdf --output ./my-skill --skip-generate  # 只提取
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def run_extract(file_path: str, output_dir: str, max_pages: int = None,
                max_chars: int = None, chapter_scan_depth: int = None) -> str:
    """
    运行书籍内容提取步骤（支持 PDF 和 TXT 格式）

    功能说明:
        根据文件扩展名自动选择对应的提取脚本：
        - .pdf → extract_pdf.py
        - .txt → extract_txt.py

    参数:
        file_path: 书籍文件路径（PDF 或 TXT）
        output_dir: 输出目录
        max_pages: 最大处理页数（仅 PDF 有效）
        max_chars: full_text 最大字符数
        chapter_scan_depth: 章节检测扫描行数

    返回:
        extraction_result.json 的路径
    """
    # 根据扩展名选择提取脚本
    ext = Path(file_path).suffix.lower()
    if ext == '.pdf':
        script_name = "extract_pdf.py"
        format_label = "PDF"
    elif ext == '.txt':
        script_name = "extract_txt.py"
        format_label = "TXT"
    else:
        print(f"错误: 不支持的文件格式 '{ext}'，仅支持 .pdf 和 .txt")
        sys.exit(1)

    print("=" * 60)
    print(f"步骤 1/3: 提取 {format_label} 内容")
    print("=" * 60)

    script_path = Path(__file__).parent / "scripts" / script_name
    cmd = [
        "python3", str(script_path),
        file_path,
        "--output", output_dir
    ]

    # PDF 特有参数
    if max_pages is not None and ext == '.pdf':
        cmd.extend(["--max-pages", str(max_pages)])
    # 通用参数
    if max_chars is not None:
        cmd.extend(["--max-chars", str(max_chars)])
    if chapter_scan_depth is not None:
        cmd.extend(["--chapter-scan-depth", str(chapter_scan_depth)])

    print(f"执行: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"错误: {format_label} 提取失败")
        print(result.stderr)
        sys.exit(1)

    print(result.stdout)

    extraction_result = Path(output_dir) / "extraction_result.json"
    if not extraction_result.exists():
        print(f"错误: 未找到提取结果文件: {extraction_result}")
        sys.exit(1)

    print(f"✓ 提取完成: {extraction_result}")
    return str(extraction_result)



def prompt_analysis(extraction_result: str, output_dir: str) -> str:
    """
    提示用户进行 AI 分析步骤
    
    参数:
        extraction_result: extraction_result.json 的路径
        output_dir: 输出目录
        
    返回:
        analysis.json 的路径
    """
    print("\n" + "=" * 60)
    print("步骤 2/3: AI 分析（需要手动完成）")
    print("=" * 60)
    
    # 读取提取结果获取书名
    with open(extraction_result, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    book_title = data.get('metadata', {}).get('title', '未知书籍')
    book_author = data.get('metadata', {}).get('author', '未知作者')
    
    print(f"\n已提取书籍: 《{book_title}》 by {book_author}")
    print(f"提取结果保存在: {extraction_result}")
    
    analysis_path = Path(output_dir) / "analysis.json"
    
    print(f"\n请完成以下操作:")
    print(f"1. 读取提取结果: {extraction_result}")
    print(f"2. 参考 references/analysis_framework.md 中的 16 个问题框架")
    print(f"3. 参考 references/analysis_template.json 了解输出格式")
    print(f"4. 将分析结果保存为: {analysis_path}")
    
    print(f"\n提示: 你也可以直接运行 generate_skill.py 使用已有的 analysis.json")
    
    if analysis_path.exists():
        print(f"\n✓ 检测到已存在的 analysis.json: {analysis_path}")
        response = input("是否使用现有文件继续? (y/n): ").strip().lower()
        if response == 'y':
            return str(analysis_path)
    
    print(f"\n请按 Enter 键继续（生成 Skill 步骤）...")
    input()
    
    if not analysis_path.exists():
        print(f"错误: 未找到 analysis.json: {analysis_path}")
        print("请完成 AI 分析步骤后再继续")
        sys.exit(1)
    
    return str(analysis_path)


def run_generate(analysis_path: str, output_dir: str, template: str = None) -> str:
    """
    运行 Skill 生成步骤
    
    参数:
        analysis_path: analysis.json 的路径
        output_dir: 输出目录
        template: 自定义模板路径（可选）
        
    返回:
        生成的 Skill 目录路径
    """
    print("\n" + "=" * 60)
    print("步骤 3/3: 生成 Skill")
    print("=" * 60)
    
    script_path = Path(__file__).parent / "scripts" / "generate_skill.py"
    cmd = [
        "python3", str(script_path),
        "--analysis", analysis_path,
        "--output", output_dir
    ]
    
    if template:
        cmd.extend(["--template", template])
    
    print(f"执行: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"错误: Skill 生成失败")
        print(result.stderr)
        sys.exit(1)
    
    print(result.stdout)
    
    # 从 generate_skill.py 的输出中解析 Skill 名称
    output_path = Path(output_dir)
    skill_dir = None
    
    # 方法1: 从 stdout 中解析 "已创建 Skill 结构: <path>" 
    import re
    match = re.search(r'已创建 Skill 结构:\s*(\S+)', result.stdout)
    if match:
        skill_dir = match.group(1)
    
    # 方法2: 回退到查找包含 SKILL.md 的子目录
    if not skill_dir or not Path(skill_dir).exists():
        skill_dirs = [d for d in output_path.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
        if skill_dirs:
            # 如果有多个，选择最近修改的
            skill_dir = str(max(skill_dirs, key=lambda d: d.stat().st_mtime))
    
    if skill_dir:
        print(f"✓ Skill 生成完成: {skill_dir}")
        return skill_dir
    
    print(f"提示: 未找到生成的 Skill 目录，请检查 {output_path}")
    return str(output_path)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='book-to-skill 统一 Pipeline 入口',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
    %(prog)s book.pdf --output ./my-skill
    %(prog)s book.pdf --output ./my-skill --max-chars 0 --chapter-scan-depth 50
    %(prog)s extraction_result.json --output ./my-skill --skip-extract
    %(prog)s book.pdf --output ./my-skill --skip-generate  # 只提取
        """
    )
    
    parser.add_argument('input_path', help='输入文件路径（PDF 或 extraction_result.json）')
    parser.add_argument('--output', '-o', default='./output', help='输出目录（默认 ./output）')
    parser.add_argument('--skip-extract', action='store_true', help='跳过提取步骤（输入为 extraction_result.json 时）')
    parser.add_argument('--skip-generate', action='store_true', help='跳过生成步骤（仅提取和分析）')
    parser.add_argument('--max-pages', type=int, help='最大处理页数')
    parser.add_argument('--max-chars', type=int, help='full_text 最大字符数（0表示不限制）')
    parser.add_argument('--chapter-scan-depth', type=int, help='章节检测每页扫描行数（0表示扫描整页）')
    parser.add_argument('--template', '-t', help='自定义 SKILL.md 模板文件')
    
    args = parser.parse_args()
    
    # 验证输入文件
    if not os.path.exists(args.input_path):
        print(f"错误: 输入文件不存在: {args.input_path}")
        sys.exit(1)
    
    # 创建输出目录
    output_path = Path(args.output)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 判断输入类型
    input_path = Path(args.input_path)
    is_extraction_result = input_path.name == "extraction_result.json" or args.skip_extract
    
    # 步骤 1: 提取（如果需要）
    if is_extraction_result:
        extraction_result = str(input_path)
        print(f"跳过提取步骤，使用现有文件: {extraction_result}")
    else:
        extraction_result = run_extract(
            args.input_path,
            str(output_path),
            args.max_pages,
            args.max_chars,
            args.chapter_scan_depth
        )
    
    # 步骤 2: 分析（提示用户）
    if args.skip_generate:
        print("\n跳过生成步骤，Pipeline 完成")
        print(f"提取结果: {extraction_result}")
        print("\n下一步:")
        print(f"1. 进行 AI 分析，生成 {output_path / 'analysis.json'}")
        print(f"2. 运行: python scripts/generate_skill.py --analysis {output_path / 'analysis.json'} --output {output_path}")
        return
    
    analysis_path = prompt_analysis(extraction_result, str(output_path))
    
    # 步骤 3: 生成 Skill
    skill_dir = run_generate(analysis_path, str(output_path), args.template)
    
    # 完成
    print("\n" + "=" * 60)
    print("Pipeline 完成!")
    print("=" * 60)
    print(f"生成的 Skill 目录: {skill_dir}")
    print(f"\n你可以:")
    print(f"1. 查看生成的 SKILL.md")
    print(f"2. 根据需要调整 analysis.json 并重新运行生成")
    print(f"3. 将 Skill 目录复制到你的 skills 文件夹中使用")


if __name__ == '__main__':
    main()
