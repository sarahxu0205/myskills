#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TXT 书籍内容提取脚本

功能说明:
    从 TXT 格式的电子书籍中提取文本内容、元数据和章节结构。
    输出格式与 extract_pdf.py 完全一致，便于后续流程无缝衔接。

功能特性:
    - 自动从文件开头或文件名提取书名和作者
    - 按固定字符数将全文切分为"虚拟页"，与 PDF 流程对齐
    - 复用与 extract_pdf.py 相同的章节检测正则模式
    - 文本清洗（移除页码噪声、压缩空行等）
    - 支持分块处理大文件
    - 支持 --max-chars 控制 full_text 长度

参数说明:
    txt_path: TXT 文件路径（位置参数）
    --output / -o: 输出目录路径（必填）
    --max-chars: full_text 最大字符数（默认 100000，0 表示不限制）
    --chapter-scan-depth: 章节检测每页扫描行数（默认 0 = 全部扫描）
    --page-size: 虚拟页字符数（默认 2000）
    --chunk: 分块编号（从 0 开始，默认 0）
    --chunk-total: 总块数（默认 1，不分块）

使用示例:
    python extract_txt.py book.txt --output ./output
    python extract_txt.py book.txt -o ./output --max-chars 50000
    python extract_txt.py book.txt -o ./output --chunk 0 --chunk-total 3
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def extract_txt_metadata(txt_path: str, head_text: str) -> Dict[str, Any]:
    """
    从 TXT 文件中提取元数据（书名、作者）

    功能说明:
        依次尝试以下策略提取书名和作者：
        1. 从文件开头匹配常见中文电子书格式（如"书名：xxx"、"标题：xxx"）
        2. 从文件开头匹配英文格式（如"Title: xxx"、"Author: xxx"）
        3. 无法识别时，从文件名（去掉扩展名）推断书名

    参数:
        txt_path: TXT 文件路径
        head_text: 文件开头的文本（前 2000 字符），用于匹配元数据

    返回:
        包含 title、author、subject、page_count 的元数据字典

    使用示例:
        metadata = extract_txt_metadata("book.txt", "书名：原子习惯\n作者：James Clear\n...")
    """
    metadata = {
        "title": None,
        "author": None,
        "subject": None,
        "page_count": 0  # 占位，后续由实际虚拟页数覆盖
    }

    # 策略 1：匹配中文电子书常见格式
    cn_title_patterns = [
        r'(?:书名|标题|作品名)[：:]\s*(.+)',
        r'(?:作者|著者|撰文)[：:]\s*(.+)',
    ]
    cn_author_patterns = [
        r'(?:作者|著者|撰文)[：:]\s*(.+)',
    ]

    lines = head_text.split('\n')
    for line in lines[:50]:  # 只扫描前 50 行
        line_stripped = line.strip()
        if not line_stripped:
            continue

        if metadata["title"] is None:
            match = re.search(cn_title_patterns[0], line_stripped)
            if match:
                metadata["title"] = match.group(1).strip()

        if metadata["author"] is None:
            match = re.search(cn_author_patterns[0], line_stripped)
            if match:
                metadata["author"] = match.group(1).strip()

    # 策略 2：匹配英文格式
    if metadata["title"] is None or metadata["author"] is None:
        for line in lines[:50]:
            line_stripped = line.strip()
            if not line_stripped:
                continue

            if metadata["title"] is None:
                match = re.search(r'Title[：:]\s*(.+)', line_stripped, re.IGNORECASE)
                if match:
                    metadata["title"] = match.group(1).strip()

            if metadata["author"] is None:
                match = re.search(r'Author[：:]\s*(.+)', line_stripped, re.IGNORECASE)
                if match:
                    metadata["author"] = match.group(1).strip()

    # 策略 3：从文件名推断书名
    if metadata["title"] is None:
        filename = Path(txt_path).stem
        # 去掉常见后缀（如 ".txt"、"_完整版"、"(精校版)" 等）
        clean_name = re.sub(r'[\(（\[【].*?[\)）\]】]', '', filename)
        clean_name = re.sub(r'[_\-—–]+', ' ', clean_name)
        clean_name = re.sub(r'(完整版|精校版|校对版|最终版|未删减|全本|珍藏版)', '', clean_name)
        metadata["title"] = clean_name.strip() or filename

    return metadata


def extract_txt_text(
    txt_path: str,
    page_size: int = 2000,
    chunk: int = 0,
    chunk_total: int = 1
) -> List[Dict[str, Any]]:
    """
    从 TXT 文件中提取文本并按虚拟页切分

    功能说明:
        读取 TXT 文件全文，按固定字符数切分为"虚拟页"，
        模拟 PDF 的逐页结构，便于后续章节检测等流程复用。

    参数:
        txt_path: TXT 文件路径
        page_size: 每页字符数（默认 2000）
        chunk: 分块编号（从 0 开始）
        chunk_total: 总块数（默认 1）

    返回:
        虚拟页内容列表，每项包含 page_number 和 text 字段

    使用示例:
        pages = extract_txt_text("book.txt", page_size=2000)
        pages = extract_txt_text("big_book.txt", chunk=0, chunk_total=3)
    """
    # 尝试多种编码
    encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5', 'utf-16']
    text = None
    for encoding in encodings:
        try:
            with open(txt_path, 'r', encoding=encoding) as f:
                text = f.read()
            print(f"  使用编码: {encoding}")
            break
        except (UnicodeDecodeError, UnicodeError):
            continue

    if text is None:
        print(f"错误: 无法解码文件 {txt_path}，尝试过的编码: {encodings}")
        sys.exit(1)

    # 清洗全文
    text = clean_text(text)

    if not text:
        print(f"警告: 文件 {txt_path} 内容为空或无法提取有效文本")
        return []

    # 按字符数切分为虚拟页（尽量在段落边界切分）
    pages = []
    paragraphs = text.split('\n')
    current_page_text = ""
    page_number = 1

    for para in paragraphs:
        if len(current_page_text) + len(para) + 1 > page_size and current_page_text:
            pages.append({
                "page_number": page_number,
                "text": current_page_text.strip()
            })
            page_number += 1
            current_page_text = para + "\n"
        else:
            current_page_text += para + "\n"

    # 添加最后一页
    if current_page_text.strip():
        pages.append({
            "page_number": page_number,
            "text": current_page_text.strip()
        })

    # 分块处理
    if chunk_total > 1:
        total = len(pages)
        chunk_size = max(1, total // chunk_total)
        start = chunk * chunk_size
        end = start + chunk_size if chunk < chunk_total - 1 else total
        pages = pages[start:end]
        print(f"  分块处理: 第 {chunk + 1}/{chunk_total} 块 (页 {start + 1}-{end})")

    print(f"  共提取 {len(pages)} 个虚拟页")
    return pages


def clean_text(text: str) -> str:
    """
    清洗提取的文本，移除常见的页眉页脚噪声

    功能说明:
        过滤文本中常见的噪声模式，如：
        - 独立的页码（如 "1", "- 2 -", "第3页"）
        - 重复的书名/章节标题（页眉）
        - 过多的连续空行
        - BOM 头标记
        - 全角空格

    参数:
        text: 原始提取文本

    返回:
        清洗后的文本

    使用示例:
        cleaned = clean_text(raw_text)
    """
    import re
    # 移除 BOM 头
    text = text.lstrip('\ufeff')
    # 移除全角空格
    text = text.replace('\u3000', ' ')
    # 移除独立页码行
    text = re.sub(r'^\s*[-‐]?\s*\d+\s*[-‐]?\s*$', '', text, flags=re.MULTILINE)
    # 移除"第X页"模式
    text = re.sub(r'^\s*第\d+页\s*$', '', text, flags=re.MULTILINE)
    # 压缩连续空行为最多两个
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def detect_chapters(pages_content: List[Dict[str, Any]], scan_depth: int = 0) -> List[Dict[str, Any]]:
    """
    识别章节结构

    功能说明:
        通过正则匹配分析文本内容，识别书籍的章节结构。
        支持中文"第X章"、英文"Chapter X"、数字编号等多种格式。

    参数:
        pages_content: 虚拟页内容列表
        scan_depth: 每页扫描行数（默认 0 表示扫描整页）

    返回:
        章节列表，每项包含 title、clean_title、page_number、level 字段

    使用示例:
        chapters = detect_chapters(pages, scan_depth=10)
    """
    chapters = []

    chapter_patterns = [
        r'^第[一二三四五六七八九十百千万零\d]+章[\s\.]*(.+)$',
        r'^Chapter\s+\d+[\s\.:]*(.+)$',
        r'^(\d+\.\d*(?:\.\d+)*)\s+(.+)$',
        r'^(引言|前言|序言|导论|结论|总结|附录)[\s\.]*(.+)?$',
    ]

    for page in pages_content:
        page_num = page["page_number"]
        text = page["text"]
        lines = text.split('\n')

        # 根据 scan_depth 决定扫描范围
        lines_to_scan = lines[:scan_depth] if scan_depth > 0 else lines
        for line in lines_to_scan:
            line = line.strip()
            if not line:
                continue

            for pattern in chapter_patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    level = 1
                    if 'Chapter' in line or '第' in line:
                        level = 1
                    elif re.match(r'^\d+\.\d+\.\d+', line):
                        level = 3
                    elif re.match(r'^\d+\.\d+', line):
                        level = 2

                    title = match.group(1) if match.group(1) else line

                    chapters.append({
                        "title": line,
                        "clean_title": title.strip(),
                        "page_number": page_num,
                        "level": level
                    })
                    break

    return chapters


def save_extraction_results(
    output_dir: str,
    metadata: Dict[str, Any],
    pages_content: List[Dict[str, Any]],
    chapters: List[Dict[str, Any]],
    max_chars: int = 100000
) -> str:
    """
    保存提取结果为 JSON 和 TXT 文件

    功能说明:
        将提取结果保存为与 extract_pdf.py 完全一致的格式：
        - extraction_result.json: 结构化数据（含受 max_chars 截断的 full_text）
        - full_text.txt: 完整纯文本（不截断）

    参数:
        output_dir: 输出目录
        metadata: 元数据字典
        pages_content: 虚拟页内容列表
        chapters: 章节信息列表
        max_chars: full_text 最大字符数（默认 100000，0 表示不限制）

    返回:
        extraction_result.json 的文件路径

    使用示例:
        path = save_extraction_results("./output", metadata, pages, chapters)
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    full_text = "\n\n".join([page["text"] for page in pages_content])

    full_text_for_json = full_text[:max_chars] if max_chars > 0 else full_text

    result = {
        "metadata": metadata,
        "chapters": chapters,
        "page_count": len(pages_content),
        "full_text": full_text_for_json,
        "pages": pages_content[:5]
    }

    output_file = output_path / "extraction_result.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    text_file = output_path / "full_text.txt"
    with open(text_file, 'w', encoding='utf-8') as f:
        f.write(full_text)

    return str(output_file)


def main():
    """
    主函数

    功能说明:
        解析命令行参数，执行 TXT 文本提取、章节检测和结果保存。

    使用示例:
        python extract_txt.py book.txt --output ./output
        python extract_txt.py book.txt -o ./output --max-chars 50000
        python extract_txt.py book.txt -o ./output --chunk 0 --chunk-total 3
    """
    parser = argparse.ArgumentParser(description='从 TXT 书籍中提取文本内容')
    parser.add_argument('txt_path', help='TXT 文件路径')
    parser.add_argument('--output', '-o', required=True, help='输出目录路径')
    parser.add_argument('--max-chars', type=int, default=100000,
                        help='full_text 最大字符数（默认 100000，0 表示不限制）')
    parser.add_argument('--chapter-scan-depth', type=int, default=0,
                        help='章节检测每页扫描行数（默认 0 = 全部扫描）')
    parser.add_argument('--page-size', type=int, default=2000,
                        help='虚拟页字符数（默认 2000）')
    parser.add_argument('--chunk', type=int, default=0,
                        help='分块编号（从 0 开始）')
    parser.add_argument('--chunk-total', type=int, default=1,
                        help='总块数（默认 1，不分块）')

    args = parser.parse_args()

    # 验证输入文件
    if not os.path.exists(args.txt_path):
        print(f"错误: 文件不存在: {args.txt_path}")
        sys.exit(1)

    print(f"读取 TXT 文件: {args.txt_path}")

    # 读取文件开头用于元数据提取
    encodings = ['utf-8', 'gbk', 'gb2312', 'gb18030', 'big5', 'utf-16']
    head_text = ""
    for encoding in encodings:
        try:
            with open(args.txt_path, 'r', encoding=encoding) as f:
                head_text = f.read(2000)
            break
        except (UnicodeDecodeError, UnicodeError):
            continue

    # 步骤 1: 提取元数据
    print("提取元数据...")
    metadata = extract_txt_metadata(args.txt_path, head_text)
    print(f"  书名: {metadata.get('title', '未识别')}")
    print(f"  作者: {metadata.get('author', '未识别')}")

    # 步骤 2: 提取文本
    print("提取文本内容...")
    pages_content = extract_txt_text(
        args.txt_path,
        page_size=args.page_size,
        chunk=args.chunk,
        chunk_total=args.chunk_total
    )

    if not pages_content:
        print("错误: 未能提取到任何文本内容")
        sys.exit(1)

    # 更新元数据中的页数
    metadata["page_count"] = len(pages_content)

    # 步骤 3: 检测章节
    print("检测章节结构...")
    chapters = detect_chapters(pages_content, args.chapter_scan_depth)
    print(f"  检测到 {len(chapters)} 个章节")

    # 步骤 4: 保存结果
    print("保存提取结果...")
    output_file = save_extraction_results(
        args.output, metadata, pages_content, chapters, args.max_chars
    )

    print(f"\n提取完成！结果保存在: {output_file}")
    print(f"  - extraction_result.json (结构化数据)")
    print(f"  - full_text.txt (完整文本)")


if __name__ == '__main__':
    main()
