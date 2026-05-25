#!/usr/bin/env python3
"""
Generate LaTeX report from BaoCao_ParallelComputing.md
"""

INPUT_FILE = "BaoCao_ParallelComputing.md"
OUTPUT_FILE = "BaoCao_ParallelComputing.tex"

def escape_latex(text):
    """Escape special LaTeX characters."""
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}',
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text


def process_inline_formatting(text):
    """Handle **bold** and *italic* inline formatting in LaTeX."""
    result = []
    i = 0
    while i < len(text):
        if text[i:i+2] == '**':
            end = text.find('**', i+2)
            if end != -1:
                result.append(r'\textbf{' + text[i+2:end] + '}')
                i = end + 2
            else:
                result.append(text[i:])
                break
        elif text[i] == '*' and (i == 0 or text[i-1] != '*'):
            end = text.find('*', i+1)
            if end != -1:
                result.append(r'\textit{' + text[i+1:end] + '}')
                i = end + 1
            else:
                result.append(text[i:])
                break
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)


def write_latex(doc, lines):
    i = 0
    in_table = False
    table_headers = []
    col_count = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # End table
        if in_table and not stripped.startswith('|'):
            doc.write(r'\end{tabular}\n\n')
            in_table = False
            table_headers = []
            continue

        # Skip table separator
        if in_table and '---' in stripped:
            i += 1
            continue

        # H1
        if stripped.startswith('# ') and not stripped.startswith('## '):
            doc.write(r'\section*{' + escape_latex(stripped[2:]) + '}\n')
            doc.write(r'\addcontentsline{toc}{section}{' + escape_latex(stripped[2:]) + '}\n\n')
            i += 1

        # H2
        elif stripped.startswith('## ') and not stripped.startswith('### '):
            doc.write(r'\section{' + escape_latex(stripped[3:]) + '}\n\n')
            i += 1

        # H3
        elif stripped.startswith('### ') and not stripped.startswith('#### '):
            doc.write(r'\subsection{' + escape_latex(stripped[4:]) + '}\n\n')
            i += 1

        # H4
        elif stripped.startswith('#### '):
            doc.write(r'\subsubsection{' + escape_latex(stripped[5:]) + '}\n\n')
            i += 1

        # Table
        elif stripped.startswith('|') and stripped.endswith('|'):
            if not in_table:
                cells = [c.strip() for c in stripped.split('|')[1:-1]]
                col_count = len(cells)
                table_headers = cells

                col_spec = '|' + '|'.join(['c'] * col_count) + '|'
                doc.write(r'\begin{tabular}{' + col_spec + r'}\n')
                doc.write(r'\hline\n')

                # Header row
                header_cells = ' & '.join([r'\textbf{' + escape_latex(c) + '}' for c in cells])
                doc.write(header_cells + r' \\' + '\n')
                doc.write(r'\hline' + '\n')
                in_table = True
                i += 1
                continue

            # Data row
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            if len(cells) == col_count:
                row_cells = ' & '.join([escape_latex(c) for c in cells])
                doc.write(row_cells + r' \\' + '\n')
            i += 1

        # Code block
        elif stripped.startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i].rstrip('\n'))
                i += 1
            i += 1  # skip closing ```

            code_text = '\n'.join(code_lines)
            doc.write(r'\begin{verbatim}' + '\n')
            doc.write(code_text + '\n')
            doc.write(r'\end{verbatim}' + '\n\n')

        # Bullet list
        elif stripped.startswith('- ') or stripped.startswith('* '):
            text = stripped[2:].strip()
            doc.write(r'\item ' + process_inline_formatting(text) + '\n')
            i += 1

        # Numbered list start
        elif stripped.startswith(('1. ', '2. ', '3. ', '4. ', '5. ', '6. ', '7. ', '8. ', '9. ')):
            # Check if we need to start an enumerate
            if not (i > 0 and lines[i-1].strip().startswith(('1. ', '2. ', '3. ', '4. ', '5. ', '6. ', '7. ', '8. ', '9. '))):
                doc.write(r'\begin{enumerate}' + '\n')
            doc.write(r'\item ' + process_inline_formatting(stripped.split('. ', 1)[1]) + '\n')
            i += 1

        # Empty line
        elif not stripped:
            # Close enumerate if we just ended a numbered list
            doc.write('\n')
            i += 1

        # Regular paragraph (skip TOC links)
        else:
            if not (stripped.startswith('[') and '](#' in stripped):
                doc.write(process_inline_formatting(stripped) + '\n\n')
            i += 1


def main():
    print(f"Reading {INPUT_FILE}...")
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print("Creating LaTeX document...")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as doc:
        # Preamble
        doc.write(r'\documentclass[14pt,a4paper]{article}' + '\n')
        doc.write(r'\usepackage[utf8]{inputenc}' + '\n')
        doc.write(r'\usepackage[vietnamese]{babel}' + '\n')
        doc.write(r'\usepackage{graphicx}' + '\n')
        doc.write(r'\usepackage{hyperref}' + '\n')
        doc.write(r'\usepackage{xcolor}' + '\n')
        doc.write(r'\usepackage{listings}' + '\n')
        doc.write(r'\usepackage{geometry}' + '\n')
        doc.write(r'\usepackage{tocbibind}' + '\n')
        doc.write(r'\geometry{margin=2.5cm}' + '\n')
        doc.write(r'\lstset{basicstyle=\ttfamily,columns=fullflexible}' + '\n')
        doc.write(r'\hypersetup{colorlinks=true,linkcolor=blue}' + '\n')
        doc.write('\n')

        doc.write(r'\title{\textbf{BÁO CÁO THỰC HÀNH}\\ \Large Giải thuật xử lý song song và phân bổ}' + '\n')
        doc.write(r'\author{\begin{itemize}\item Môn: Giải thuật xử lý song song và phân bổ \item GVHD: Lê Minh Khánh Hội, Lê Phạm Hoàng Trung \item Ngày: 31 tháng 3 năm 2026\end{itemize}}' + '\n')
        doc.write(r'\date{}' + '\n')
        doc.write('\n')

        doc.write(r'\begin{document}' + '\n')
        doc.write(r'\maketitle' + '\n')
        doc.write(r'\newpage' + '\n')
        doc.write(r'\tableofcontents' + '\n')
        doc.write(r'\newpage' + '\n\n')

        # Process content
        write_latex(doc, lines)

        doc.write(r'\end{document}' + '\n')

    print(f"Done! LaTeX saved to {OUTPUT_FILE}")
    print("Compile with: pdflatex BaoCao_ParallelComputing.tex")


if __name__ == "__main__":
    main()
