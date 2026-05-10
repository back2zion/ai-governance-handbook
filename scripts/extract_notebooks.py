"""Extract Python code blocks from LaTeX chapters and create Jupyter notebooks."""
import re
import json
import os

CHAPTERS_DIR = "/home/babelai/personal-dev/latex/latex-book/chapters"
OUTPUT_DIR = "/home/babelai/personal-dev/ai-governance-handbook/notebooks"
REPO = "back2zion/ai-governance-handbook"

CHAPTER_MAP = [
    ("01_concept.tex",             "ch01", "제1장: AI 거버넌스 개념과 필요성"),
    ("02_global_frameworks.tex",   "ch02", "제2장: 글로벌 AI 거버넌스 프레임워크"),
    ("03_ethics_operationalization.tex", "ch03", "제3장: AI 윤리 실무화"),
    ("04_organization.tex",        "ch04", "제4장: AI 거버넌스 조직 체계"),
    ("05_policy.tex",              "ch05a", "제5장: AI 정책 설계"),
    ("05_industry_applications.tex","ch05b", "제5장(b): 산업별 AI 적용"),
    ("06_governance_tools.tex",    "ch06", "제6장: 거버넌스 도구와 플랫폼"),
    ("07_case_studies.tex",        "ch07", "제7장: 사례 연구"),
    ("08_usecase_discovery.tex",   "ch08", "제8장: 유즈케이스 발굴"),
    ("09_data_governance.tex",     "ch09", "제9장: 데이터 거버넌스"),
    ("10_model_development.tex",   "ch10", "제10장: 모델 개발 거버넌스"),
    ("11_audit_certification.tex", "ch11", "제11장: 알고리즘 감사와 인증"),
    ("12_operation_lifecycle.tex", "ch12", "제12장: 운영 및 생명주기 관리"),
    ("12b_generative_ai.tex",      "ch12b", "제12장(b): 생성 AI 거버넌스"),
    ("13_architecture.tex",        "ch13", "제13장: 거버넌스 아키텍처"),
    ("14_tools_platform.tex",      "ch14", "제14장: 도구 및 플랫폼"),
    ("15_security_privacy.tex",    "ch15", "제15장: 보안과 프라이버시"),
    ("16_healthcare.tex",          "ch16", "제16장: 의료 AI 거버넌스"),
    ("17_finance.tex",             "ch17", "제17장: 금융 AI 거버넌스"),
    ("18_public.tex",              "ch18", "제18장: 공공 AI 거버넌스"),
    ("19_industrial.tex",          "ch19", "제19장: 산업 AI 거버넌스"),
    ("20_future.tex",              "ch20", "제20장: AI 거버넌스의 미래"),
]

INSTALL_PACKAGES = [
    "fairlearn",
    "shap",
    "mlflow",
    "diffprivlib",
    "alibi",
    "alibi-detect",
    "evidently",
    "pandas",
    "scikit-learn",
    "matplotlib",
    "seaborn",
    "numpy",
]

def strip_latex(text):
    """Remove common LaTeX commands from text."""
    text = re.sub(r'\\textbf\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\textit\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\emph\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\text\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\cite\{[^}]*\}', '', text)
    text = re.sub(r'\\label\{[^}]*\}', '', text)
    text = re.sub(r'\\ref\{[^}]*\}', '', text)
    text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_caption(options_str):
    """Extract caption from lstlisting options like [language=Python, caption={...}]"""
    m = re.search(r'caption=\{([^}]*)\}', options_str)
    if m:
        return strip_latex(m.group(1))
    return None

def parse_chapter(filepath):
    """Return list of (type, content) tuples: ('section', title) or ('code', (caption, code))."""
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    items = []

    # Collect sections and code blocks with their positions
    section_pattern = re.compile(
        r'\\(chapter|section|subsection)\*?\{([^}]+)\}', re.MULTILINE)
    code_pattern = re.compile(
        r'\\begin\{lstlisting\}(\[[^\]]*\])?(.*?)\\end\{lstlisting\}',
        re.DOTALL)

    events = []
    for m in section_pattern.finditer(content):
        events.append((m.start(), 'section', m.group(1), strip_latex(m.group(2))))
    for m in code_pattern.finditer(content):
        opts = m.group(1) or ''
        code = m.group(2).strip()
        caption = extract_caption(opts)
        # Only Python code
        if 'python' in opts.lower() or 'Python' in opts:
            events.append((m.start(), 'code', caption, code))

    events.sort(key=lambda x: x[0])

    for ev in events:
        if ev[1] == 'section':
            items.append(('section', ev[2], ev[3]))  # level, title
        else:
            items.append(('code', ev[2], ev[3]))  # caption, code

    return items

def make_notebook(chapter_id, title, items, repo):
    """Build a Jupyter notebook dict."""
    colab_url = f"https://colab.research.google.com/github/{repo}/blob/main/notebooks/{chapter_id}.ipynb"
    badge = f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_url})"

    cells = []

    # Header cell
    header_md = f"# {title}\n\n{badge}\n\n> **『AI 거버넌스 실무 지침서』** (곽두일) 실습 코드\n>\n> 이 노트북의 모든 코드는 Google Colab에서 바로 실행할 수 있습니다."
    cells.append(md_cell(header_md))

    # Install cell
    install_code = "# 필요 패키지 설치 (최초 1회)\n!pip install -q " + " ".join(INSTALL_PACKAGES)
    cells.append(code_cell(install_code))

    # Content cells
    for item in items:
        if item[0] == 'section':
            level, sec_title = item[1], item[2]
            prefix = "##" if level in ('section',) else "###"
            cells.append(md_cell(f"{prefix} {sec_title}"))
        elif item[0] == 'code':
            caption, code = item[1], item[2]
            if caption:
                cells.append(md_cell(f"**{caption}**"))
            cells.append(code_cell(code))

    nb = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            },
            "colab": {
                "provenance": [],
                "name": f"{chapter_id}.ipynb"
            }
        },
        "cells": cells
    }
    return nb

def md_cell(source):
    return {
        "cell_type": "markdown",
        "id": os.urandom(4).hex(),
        "metadata": {},
        "source": source
    }

def code_cell(source):
    return {
        "cell_type": "code",
        "id": os.urandom(4).hex(),
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": source
    }

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    created = []
    skipped = []

    for tex_file, chapter_id, title in CHAPTER_MAP:
        filepath = os.path.join(CHAPTERS_DIR, tex_file)
        if not os.path.exists(filepath):
            skipped.append(tex_file)
            continue

        items = parse_chapter(filepath)
        code_items = [i for i in items if i[0] == 'code']

        if not code_items:
            skipped.append(f"{tex_file} (코드 없음)")
            continue

        nb = make_notebook(chapter_id, title, items, REPO)
        out_path = os.path.join(OUTPUT_DIR, f"{chapter_id}.ipynb")
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, ensure_ascii=False, indent=2)

        created.append(f"{chapter_id}.ipynb ({len(code_items)}개 코드블록)")

    print("생성된 노트북:")
    for c in created:
        print(f"  ✓ {c}")
    if skipped:
        print("건너뜀:")
        for s in skipped:
            print(f"  - {s}")
    print(f"\n총 {len(created)}개 노트북 → {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
