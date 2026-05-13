#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 内容提取脚本

功能说明:
    从 PDF 书籍文件中提取文本内容、元数据、章节结构等信息，
    为后续的 16 个问题分析提供基础数据。

功能特性:
    - 提取 PDF 元数据（书名、作者、出版信息等）
    - 提取完整文本内容
    - 识别章节结构和目录
    - 支持大文件分块处理
    - 输出结构化的 JSON 格式

参数说明:
    pdf_path: PDF 文件路径
    --output: 输出目录路径
    --max-pages: 最大处理页数（可选，用于测试）
    --chunk-size: 分块大小（默认 10000 字符）

使用示例:
    python extract_pdf.py /path/to/book.pdf --output ./output
    python extract_pdf.py /path/to/book.pdf --output ./output --max-pages 50
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def extract_pdf_metadata(pdf_path: str) -> Dict[str, Any]:
    """
    提取 PDF 元数据
    
    尝试从 PDF 中提取书名、作者、页数等信息
    
    参数:
        pdf_path: PDF 文件路径
        
    返回:
        包含元数据的字典
    """
    metadata = {
        "title": None,
        "author": None,
        "subject": None,
        "page_count": 0
    }
    
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(pdf_path)
        
        if reader.metadata:
            meta = reader.metadata
            metadata["title"] = meta.get("/Title", None)
            metadata["author"] = meta.get("/Author", None)
            metadata["subject"] = meta.get("/Subject", None)
        
        metadata["page_count"] = len(reader.pages)
        
    except ImportError:
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                metadata["page_count"] = len(pdf.pages)
                if pdf.metadata:
                    meta = pdf.metadata
                    metadata["title"] = meta.get("Title", None)
                    metadata["author"] = meta.get("Author", None)
        except ImportError:
            print("错误: 需要安装 PyPDF2 或 pdfplumber")
            sys.exit(1)
    
    return metadata


def extract_pdf_text(pdf_path: str, max_pages: Optional[int] = None,
                     chunk: int = 0, chunk_total: int = 1) -> List[Dict[str, Any]]:
    """
    提取 PDF 文本内容
    
    参数:
        pdf_path: PDF 文件路径
        max_pages: 最大提取页数（可选）
        
    返回:
        每页内容的列表
    """
    pages_content = []
    
    try:
        import pdfplumber
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)
                pages_to_extract = min(total_pages, max_pages) if max_pages else total_pages
                
                for i in range(pages_to_extract):
                    page = pdf.pages[i]
                    text = page.extract_text()
                    
                    if text:
                        text = clean_text(text)
                        pages_content.append({
                            "page_number": i + 1,
                            "text": text
                        })
        except Exception as e:
            # 密码保护 PDF 检测
            if "password" in str(e).lower() or "encrypted" in str(e).lower() or "decrypt" in str(e).lower():
                print("警告: 该 PDF 文件可能受密码保护，无法直接提取内容。请先解除密码保护后再试。")
            else:
                print(f"警告: 无法打开 PDF 文件: {e}")
            return pages_content
                    
    except ImportError:
        try:
            from PyPDF2 import PdfReader
            try:
                reader = PdfReader(pdf_path)
            except Exception as e:
                # 密码保护 PDF 检测
                if "password" in str(e).lower() or "encrypted" in str(e).lower() or "decrypt" in str(e).lower():
                    print("警告: 该 PDF 文件可能受密码保护，无法直接提取内容。请先解除密码保护后再试。")
                else:
                    print(f"警告: 无法打开 PDF 文件: {e}")
                return pages_content
            
            total_pages = len(reader.pages)
            pages_to_extract = min(total_pages, max_pages) if max_pages else total_pages
            
            for i in range(pages_to_extract):
                page = reader.pages[i]
                text = page.extract_text()
                
                if text:
                    text = clean_text(text)
                    pages_content.append({
                        "page_number": i + 1,
                        "text": text
                    })
        except ImportError:
            print("错误: 无法导入 PDF 处理库")
            sys.exit(1)
    
    # 扫描版 PDF 检测：检查提取结果是否为空或文本极短
    total_text_length = sum(len(page.get("text", "")) for page in pages_content)
    if not pages_content or total_text_length < 100:
        print("警告: 提取的文本内容极少（总长度 < 100 字符）。")
        print("  可能原因：该 PDF 为扫描版（图片型），需要 OCR 处理后才能提取文字。")
        print("  建议：使用 OCR 工具（如 Tesseract、Adobe Acrobat）将扫描版 PDF 转换为可搜索文本。")

    # 分块处理
    if chunk_total > 1 and len(pages_content) > 0:
        total = len(pages_content)
        chunk_size = total // chunk_total
        start = chunk * chunk_size
        end = start + chunk_size if chunk < chunk_total - 1 else total
        pages_content = pages_content[start:end]

    return pages_content


def clean_text(text: str) -> str:
    """
    清洗提取的文本，移除常见的页眉页脚噪声

    功能说明:
        过滤 PDF 提取文本中常见的噪声模式，如：
        - 独立的页码（如 "1", "- 2 -", "第3页"）
        - 重复的书名/章节标题（页眉）
        - 过多的连续空行

    参数:
        text: 原始提取文本

    返回:
        清洗后的文本
    """
    import re
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
    
    通过分析文本内容，尝试识别书籍的章节结构
    
    参数:
        pages_content: 页面内容列表
        scan_depth: 每页扫描行数（默认0表示扫描整页）
        
    返回:
        章节列表
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
    保存提取结果
    
    参数:
        output_dir: 输出目录
        metadata: 元数据
        pages_content: 页面内容
        chapters: 章节信息
        max_chars: full_text 最大字符数（默认100000，0表示不限制）
        
    返回:
        输出文件的路径
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
    """主函数"""
    parser = argparse.ArgumentParser(description='从 PDF 书籍中提取内容')
    parser.add_argument('pdf_path', help='PDF 文件路径')
    parser.add_argument('--output', '-o', required=True, help='输出目录路径')
    parser.add_argument('--max-pages', type=int, help='最大处理页数')
    parser.add_argument('--max-chars', type=int, default=100000,
                        help='full_text 最大字符数（默认100000，0表示不限制）')
    parser.add_argument('--chapter-scan-depth', type=int, default=0,
                        help='章节检测每页扫描行数（默认0表示扫描整页）')
    parser.add_argument('--chunk', type=int, default=0,
                        help='分块编号（从0开始），配合 --chunk-total 使用')
    parser.add_argument('--chunk-total', type=int, default=1,
                        help='总块数（默认1，不分块）')

    args = parser.parse_args()
    
    if not os.path.exists(args.pdf_path):
        print(f"错误: 文件不存在: {args.pdf_path}")
        sys.exit(1)
    
    print(f"开始处理 PDF: {args.pdf_path}")
    
    print("提取元数据...")
    metadata = extract_pdf_metadata(args.pdf_path)
    print(f"  书名: {metadata.get('title', '未知')}")
    print(f"  作者: {metadata.get('author', '未知')}")
    print(f"  页数: {metadata.get('page_count', 0)}")
    
    print("提取文本内容...")
    pages_content = extract_pdf_text(args.pdf_path, args.max_pages, args.chunk, args.chunk_total)
    print(f"  成功提取 {len(pages_content)} 页")
    if args.chunk_total > 1:
        print(f"  分块: {args.chunk + 1}/{args.chunk_total}")

    print("识别章节结构...")
    chapters = detect_chapters(pages_content, args.chapter_scan_depth)
    print(f"  发现 {len(chapters)} 个章节")
    
    print("保存提取结果...")
    output_file = save_extraction_results(args.output, metadata, pages_content, chapters, args.max_chars)
    
    print(f"\n完成！结果保存在: {output_file}")


if __name__ == '__main__':
    main()
