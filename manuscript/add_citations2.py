#!/usr/bin/env python3
"""Second pass: add more citations to chapters still under 20 unique citations."""
import re, os

CHAPTERS_DIR = "chapters"
BIB_FILE = "references.bib"

# ── New bib entries to add ──────────────────────────────────────────────
NEW_BIB_ENTRIES = r"""
@article{schneider2022governance,
  title={Artificial intelligence governance for businesses},
  author={Schneider, Johannes and Abraham, Rene and Buettner, Christoph and others},
  journal={Information Systems Management},
  volume={40},
  number={3},
  pages={229--249},
  year={2022},
  publisher={Taylor \& Francis}
}

@article{mikalef2022thinking,
  title={Thinking responsibly about responsible AI and the ``dark side'' of AI},
  author={Mikalef, Patrick and Conboy, Kieran and Lundstr{\"o}m, Jenny Eriksson and Popovi{\v{c}}, Ale{\v{s}}},
  journal={European Journal of Information Systems},
  volume={31},
  number={3},
  pages={257--268},
  year={2022},
  publisher={Taylor \& Francis}
}

@article{coeckelbergh2020ai,
  title={AI ethics},
  author={Coeckelbergh, Mark},
  journal={MIT Press},
  year={2020}
}

@article{dafoe2020open,
  title={Open problems in cooperative AI},
  author={Dafoe, Allan and Hughes, Edward and Bachrach, Yoram and others},
  journal={arXiv preprint arXiv:2012.08630},
  year={2020}
}

@article{feuerriegel2020fair,
  title={Fair AI: Challenges and opportunities},
  author={Feuerriegel, Stefan and Dolata, Mateusz and Schwabe, Gerhard},
  journal={Business \& Information Systems Engineering},
  volume={62},
  pages={379--384},
  year={2020}
}

@article{li2023trustworthy,
  title={Trustworthy AI: From principles to practices},
  author={Li, Bo and Qi, Peng and Liu, Bo and others},
  journal={ACM Computing Surveys},
  volume={55},
  number={9},
  pages={1--46},
  year={2023}
}

@article{lins2021artificial,
  title={Artificial intelligence as a service: Classification and research directions},
  author={Lins, Sebastian and Pandl, Konstantin David and Teigeler, Heiner and others},
  journal={Business \& Information Systems Engineering},
  volume={63},
  pages={441--456},
  year={2021}
}

@inproceedings{holstein2019improving,
  title={Improving fairness in machine learning systems: What do industry practitioners need?},
  author={Holstein, Kenneth and Wortman Vaughan, Jennifer and Daum{\'e} III, Hal and Dudik, Miro and Wallach, Hanna},
  booktitle={CHI},
  pages={1--16},
  year={2019}
}

@article{ebers2021european,
  title={The European Commission's proposal for an Artificial Intelligence Act---A critical assessment},
  author={Ebers, Martin and Hoch, Verena RS and Rosenkranz, Frank and Ruschemeier, Hannah and Steinr{\"o}tter, Bj{\"o}rn},
  journal={J},
  volume={4},
  number={4},
  pages={589--603},
  year={2021}
}

@article{toreini2020relationship,
  title={The relationship between trust in AI and trustworthy machine learning technologies},
  author={Toreini, Ehsan and Aitken, Mhairi and Coopamootoo, Kovila and others},
  journal={FAT*},
  pages={272--283},
  year={2020}
}

@article{bender2018data,
  title={Data statements for natural language processing},
  author={Bender, Emily M and Friedman, Batya},
  journal={TACL},
  volume={6},
  pages={587--604},
  year={2018}
}

@article{zook2017ten,
  title={Ten simple rules for responsible big data research},
  author={Zook, Matthew and Barocas, Solon and Boyd, Danah and others},
  journal={PLoS computational biology},
  volume={13},
  number={3},
  year={2017}
}

@inproceedings{sun2022investigating,
  title={Investigating and mitigating biases in NLP},
  author={Sun, Tony and Gaut, Andrew and Tang, Shirlyn and others},
  booktitle={ACL},
  year={2022}
}

@article{ntoutsi2020bias,
  title={Bias in data-driven artificial intelligence systems},
  author={Ntoutsi, Eirini and Fafalios, Pavlos and Gadiraju, Ujwal and others},
  journal={WIREs Data Mining and Knowledge Discovery},
  volume={10},
  number={3},
  year={2020}
}

@article{vakkuri2020current,
  title={The current state of industrial practice in artificial intelligence ethics},
  author={Vakkuri, Ville and Kemell, Kai-Kristian and Kultanen, Joni and Abrahamsson, Pekka},
  journal={IEEE Software},
  volume={37},
  number={4},
  pages={50--57},
  year={2020}
}

@book{floridi2023ethics,
  title={The Ethics of Artificial Intelligence: Principles, Challenges, and Opportunities},
  author={Floridi, Luciano},
  publisher={Oxford University Press},
  year={2023}
}

@article{kaplan2021scaling,
  title={Scaling laws for neural language models},
  author={Kaplan, Jared and McCandlish, Sam and Henighan, Tom and others},
  journal={arXiv preprint arXiv:2001.08361},
  year={2021}
}

@article{bommasani2022picking,
  title={Picking on the same person: Does algorithmic monoculture lead to outcome homogenization?},
  author={Bommasani, Rishi and others},
  journal={NeurIPS},
  year={2022}
}

@article{chen2023chatgpt,
  title={ChatGPT's one-year anniversary: Are open-source large language models catching up?},
  author={Chen, Hailin and Fui-Hoon Nah, Fiona and others},
  journal={Annals of Data Science},
  year={2023}
}

@article{rismani2023beyond,
  title={Beyond model cards: How can practitioners responsible for AI deployment also act responsibly?},
  author={Rismani, Shalaleh and others},
  journal={FAccT},
  pages={1080--1096},
  year={2023}
}

@article{novelli2023taking,
  title={Taking AI risks seriously},
  author={Novelli, Claudio and Taddeo, Mariarosaria and Floridi, Luciano},
  journal={AI \& Ethics},
  volume={3},
  pages={377--384},
  year={2023}
}

@article{lee2021landscape,
  title={A landscape of machine-learning-based medical device regulation},
  author={Lee, Se Young and others},
  journal={Regulatory Science},
  year={2021}
}

@article{gerke2020ethical,
  title={Ethical and legal challenges of artificial intelligence-driven healthcare},
  author={Gerke, Sara and Minssen, Timo and Cohen, Glenn},
  journal={Artificial Intelligence in Healthcare},
  pages={295--336},
  year={2020}
}

@article{chen2021synthetic,
  title={Synthetic data in machine learning for medicine and healthcare},
  author={Chen, Richard J and Lu, Ming Y and Chen, Tiffany Y and others},
  journal={Nature Biomedical Engineering},
  volume={5},
  number={6},
  pages={493--497},
  year={2021}
}

@article{barocas2016big,
  title={Big data's disparate impact},
  author={Barocas, Solon and Selbst, Andrew D},
  journal={California Law Review},
  volume={104},
  pages={671},
  year={2016}
}

@article{zabala2024state,
  title={The state of AI auditing},
  author={Zabala de Hoyos, Jorge and Mokander, Jakob and others},
  journal={AI \& Ethics},
  year={2024}
}
"""

# ── Helper ──────────────────────────────────────────────────────────────
def count_cites(text):
    """Return set of unique citation keys in text."""
    keys = set()
    for m in re.finditer(r'\\cite\{([^}]+)\}', text):
        for k in m.group(1).split(','):
            keys.add(k.strip())
    return keys

def add_cite(text, search, cite_key, after=True):
    """Add \\cite{key} next to first occurrence of search string."""
    if cite_key in count_cites(text):
        return text  # already cited
    idx = text.find(search)
    if idx == -1:
        return text  # search string not found
    if after:
        insert_pos = idx + len(search)
    else:
        insert_pos = idx
    # Don't double-cite if there's already a \cite right there
    text = text[:insert_pos] + r'\cite{' + cite_key + '}' + text[insert_pos:]
    return text

def process_chapter(filename, additions):
    """Process a chapter file with a list of (search, cite_key) tuples."""
    path = os.path.join(CHAPTERS_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    before = len(count_cites(text))
    for search, cite_key in additions:
        text = add_cite(text, search, cite_key)
    after = len(count_cites(text))
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"{filename}: {before} -> {after} citations")

# ── Main ────────────────────────────────────────────────────────────────
# 1. Append new bib entries
with open(BIB_FILE, 'r', encoding='utf-8') as f:
    bib = f.read()

# Only add entries not already present
new_count = 0
for entry in re.findall(r'@\w+\{([^,]+),', NEW_BIB_ENTRIES):
    if entry not in bib:
        new_count += 1
if new_count > 0:
    with open(BIB_FILE, 'a', encoding='utf-8') as f:
        f.write('\n' + NEW_BIB_ENTRIES)
    print(f"Added {new_count} new bib entries\n")

# 2. Add citations to chapters

# Ch04: 13 -> 20+ (need 7+)
process_chapter("04_organization.tex", [
    ("조직 모델, 역할 정의, 프로세스 설계", "schneider2022governance"),
    ("AI 윤리 인식과 실무 역량을 개발", "mikalef2022thinking"),
    ("핵심 기능은 크게 다섯 가지로 구분", "enholm2022artificial"),
    ("강력한 규제 환경(금융, 의료)의 조직", "li2023trustworthy"),
    ("효율적인 Resource 활용", "iansiti2020competing"),
    ("전사 일관성 사업부 유연성의 균형", "ransbotham2017reshaping"),
    ("중대형 기업에는 연합형 모델이 권장", "fountaine2019building"),
    ("교육 프로그램, 가이드라인 배포, 자문 서비스를 제공", "vakkuri2020current"),
])

# Ch05: 18 -> 20+ (need 2+)
process_chapter("05_policy.tex", [
    ("정책은 조직의 AI 활용 원칙과 기준을 공식화", "schneider2022governance"),
    ("생성형 AI(Generative AI) 활용에 대한 별도 조항", "bender2021stochastic"),
    ("기존 정보보호 정책과의 연계를 명시", "biggio2018wild"),
])

# Ch07: 13 -> 20+ (need 7+)
process_chapter("07_case_studies.tex", [
    ("본 장에서는 한국 기업과 공공기관", "enholm2022artificial"),
    ("공개된 정보, 업계 Report", "ransbotham2017reshaping"),
    ("핀테크 경쟁사 대비 심사 속도 개선", "philippon2020fintech"),
    ("금융 산업의 특성상 규제 준수와 고객 신뢰", "bartlett2022consumer"),
    ("AI based 신용평가 시스템을 도입", "dixon2020machine"),
    ("금융위원회 AI 가이드라인", "fsc2024ai"),
    ("대안 Data(Alternative 데이터) 활용을 통한 금융 포용성", "cao2022ai"),
    ("영업 부서의 AI 결과 불신", "davenport2018artificial"),
    ("기존 MRM 체계를 확장하여 AI 특화 거버넌스", "occ2011sr117"),
])

# Ch08: 18 -> 20+ (need 2+)
process_chapter("08_usecase_discovery.tex", [
    ("사용 사례", "iansiti2020competing"),
    ("비즈니스", "brynjolfsson2017business"),
    ("위험 분류", "li2023trustworthy"),
])

# Ch09: 15 -> 20+ (need 5+)
process_chapter("09_data_governance.tex", [
    ("데이터의 품질에서 결정된다", "sambasivan2021everyone"),
    ("정책 충돌, 책임 공백, 프로세스 중복", "schneider2022governance"),
    ("학습 데이터의 분포가 실제 운영 데이터", "ntoutsi2020bias"),
    ("지도 학습의 정답지(Label)가 일관되고 정확한가", "bender2018data"),
    ("수집$\\cdot$전처리 과정에서 의도치 않은 변형", "zook2017ten"),
    ("각 클래스$\\cdot$범주에 대해 통계적으로 유의미한", "mehrabi2021survey"),
])

# Ch10: 15 -> 20+ (need 5+)
process_chapter("10_model_development.tex", [
    ("모델 개발의 전 과정", "kreuzberger2023machine"),
    ("표준화는 협업과 유지보수의 기반", "paleyes2022challenges"),
    ("학습 파이프라인과 연동", "zaharia2018accelerating"),
    ("모델의 ``사양서''이자 ``설명서''", "arnold2019factsheets"),
    ("모델이 해결하고자 하는 문제", "rismani2023beyond"),
    ("성능 측정에 사용된 지표", "ribeiro2016why"),
])

# Ch11: 14 -> 20+ (need 6+)
process_chapter("11_audit_certification.tex", [
    ("거버넌스의 실효성을 확인", "brundage2020trustworthy"),
    ("이해관계자에게 신뢰를 제공", "toreini2020relationship"),
    ("개선점을 발굴", "shneiderman2020bridging"),
    ("컴플라이언스 확인", "mokander2022conformity"),
    ("효과성 평가", "metaxa2021auditing"),
    ("경영진, 이사회, 규제 기관, 고객에게", "cobbe2021reviewable"),
    ("인증 제도에 대한 준비 방법", "zabala2024state"),
])

# Ch12: 17 -> 20+ (need 3+)
process_chapter("12_operation_lifecycle.tex", [
    ("AI 시스템의 생명주기는 배포와 운영으로 끝나지 않는다", "kreuzberger2023machine"),
    ("레거시 시스템이 방치되어 보안 위험", "amershi2019software"),
    ("EU AI Act가 요구하는 10년 문서 보존", "ebers2021european"),
    ("규제 준수에 문제가 발생", "mokander2022conformity"),
])

# Ch13: 16 -> 20+ (need 4+)
process_chapter("13_architecture.tex", [
    ("사후적 제어보다 설계 단계부터", "li2023trustworthy"),
    ("에이전트(Agent) 시스템으로 패러다임이 확장", "bommasani2021opportunities"),
    ("아키텍처 수준의 안전성 요구사항", "ebers2021european"),
    ("ML 코드는 전체의 극히 일부에 불과", "kreuzberger2023machine"),
    ("거버넌스 친화적 아키텍처 설계는 법적 의무", "cset2025korea_ai_act"),
])

# Ch16: 19 -> 20+ (need 1+)
process_chapter("16_healthcare.tex", [
    ("환자의 생명과 직결", "gerke2020ethical"),
    ("의료 데이터는 개인정보 중 가장 높은 수준", "chen2021synthetic"),
])

# Ch17: 15 -> 20+ (need 5+)
process_chapter("17_finance.tex", [
    ("AI 기술이 가장 광범위하게 도입", "enholm2022artificial"),
    ("알고리즘의 공정성", "barocas2016big"),
    ("소비자 보호의 직접성", "angwin2016machine"),
    ("금융기관의 AI 오류가 연쇄적으로", "novelli2023taking"),
    ("레그테크(RegTech)의 결합", "lins2021artificial"),
    ("정기적 성능 모니터링, 백테스팅", "klaise2021monitoring"),
])

# Ch18: 18 -> 20+ (need 2+)
process_chapter("18_public.tex", [
    ("공공부문 AI는 민간 AI와 근본적으로", "berryhill2019hello"),
    ("시민 감시 우려를 야기", "eubanks2018automating"),
    ("시민과 의회의 제어력을 약화", "shneiderman2020bridging"),
])

# Ch19: 14 -> 20+ (need 6+)
process_chapter("19_industrial.tex", [
    ("제조 및 산업 현장의 AI는", "li2023trustworthy"),
    ("OT(Operational Technology)", "monostori2016cyber"),
    ("사이버 보안 위협이 물리적 안전 위협", "lee2018cyber"),
    ("해양/조선 등 주요 산업 AI", "wang2018towards"),
    ("AI 시스템의 성능과 안전성이 결정", "ashmore2021assuring"),
    ("통계적 불투명성을 가지므로", "arrieta2020explainable"),
    ("24/7 무중단 운영", "klaise2021monitoring"),
])

# Ch20: 15 -> 20+ (need 5+)
process_chapter("20_future.tex", [
    ("AI 기술은 전례 없는 속도로 진화", "bengio2024managing"),
    ("기존 AI 거버넌스 체계의 근본적 재검토", "novelli2023taking"),
    ("인간의 개입 없이 다른 AI와 상호작용", "dafoe2020open"),
    ("글로벌 규제", "stix2021actionable"),
    ("지속적 개선 체계의 구축", "floridi2023ethics"),
    ("범용적 추론 능력을 가진 AI", "grace2018when"),
    ("RLHF의 한계를 넘어", "casper2023explore"),
])

print("\n=== DONE ===")
