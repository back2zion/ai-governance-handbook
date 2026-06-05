#!/usr/bin/env python3
"""Add citations to chapters that need more references."""
import re
import os

BASE = '/home/babelai/personal-dev/latex-book/chapters'

def count_citations(text):
    keys = set()
    for m in re.findall(r'\\cite\{([^}]+)\}', text):
        for k in m.split(','):
            keys.add(k.strip())
    return keys

def add_cite(content, search, cite, max_count=1):
    """Add cite after search string, only if cite not already present nearby."""
    if cite in content:
        return content
    if search in content:
        content = content.replace(search, search + cite, max_count)
    return content

def process_chapter(filename, citations_to_add):
    """Add citations to a chapter file."""
    path = os.path.join(BASE, filename)
    with open(path, 'r') as f:
        c = f.read()

    before = len(count_citations(c))

    for search, cite in citations_to_add:
        c = add_cite(c, search, cite)

    with open(path, 'w') as f:
        f.write(c)

    after = len(count_citations(c))
    print(f"{filename}: {before} -> {after} citations")

# ===== Ch04 Organization (currently 12, need 8+ more) =====
process_chapter('04_organization.tex', [
    ('조직 모델, 역할 정의, 프로세스 설계', '\\cite{mantymaki2022defining}'),
    ('분산형 사이에서', '\\cite{eitelporter2021beyond}'),
    ('비즈니스 가치를 창출', '\\cite{enholm2022artificial}'),
    ('AI 전략 수립', '\\cite{dafoe2018aigovernance}'),
    ('리스크 비례', '\\cite{iso23894}'),
    ('인재 양성', '\\cite{fountaine2019building}'),
    ('심리적 안전', '\\cite{rakova2021responsible}'),
    ('3선 방어', '\\cite{shneiderman2020bridging}'),
    ('이해관계자', '\\cite{winfield2018ethical}'),
    ('조직 문화', '\\cite{hagendorff2020ethics}'),
])

# ===== Ch05 Policy (currently 3, need 17+ more) =====
process_chapter('05_policy.tex', [
    ('정책 아키텍처', '\\cite{calo2017artificial}'),
    ('계층 구조', '\\cite{baldwin2012understanding}'),
    ('영향평가 체계', '\\cite{canada2019aia}'),
    ('AI 영향평가', '\\cite{raji2020closing}'),
    ('리스크 분류', '\\cite{nist2023airmf}'),
    ('NIST AI RMF', '\\cite{iso23894}'),
    ('리스크 매트릭스', '\\cite{iso42001}'),
    ('Policy-as-Code', '\\cite{hinrichs2019opa}'),
    ('OPA', '\\cite{stix2021actionable}'),
    ('인시던트 관리', '\\cite{brundage2020trustworthy}'),
    ('정책 준수', '\\cite{mokander2022conformity}'),
    ('정책 위반', '\\cite{shneiderman2020bridging}'),
    ('EU AI Act', '\\cite{eu2024aiact}'),
    ('기본법', '\\cite{cset2025korea_ai_act}'),
    ('투명성', '\\cite{arrieta2020explainable}'),
    ('공정성', '\\cite{mehrabi2021survey}'),
    ('모니터링', '\\cite{klaise2021monitoring}'),
    ('감사', '\\cite{falco2021governing}'),
])

# ===== Ch06 Governance Tools (currently 0, need 20+) =====
process_chapter('06_governance_tools.tex', [
    ('거버넌스 기술 스택', '\\cite{morley2020from}'),
    ('공정성 평가', '\\cite{bellamy2019ai}'),
    ('Fairlearn', '\\cite{mehrabi2021survey}'),
    ('AIF360', '\\cite{saleiro2018aequitas}'),
    ('SHAP', '\\cite{lundberg2017unified}'),
    ('설명가능성', '\\cite{arrieta2020explainable}'),
    ('설명가능한 AI', '\\cite{ribeiro2016why}'),
    ('Captum', '\\cite{sokol2020explainability}'),
    ('MLflow', '\\cite{zaharia2018accelerating}'),
    ('MLOps', '\\cite{kreuzberger2023machine}'),
    ('CI/CD', '\\cite{sato2019continuous}'),
    ('모니터링', '\\cite{klaise2021monitoring}'),
    ('Evidently', '\\cite{sculley2015hidden}'),
    ('드리프트', '\\cite{paleyes2022challenges}'),
    ('모델 카드', '\\cite{mitchell2019model}'),
    ('Model Card', '\\cite{gebru2021datasheets}'),
    ('문서화', '\\cite{arnold2019factsheets}'),
    ('편향 완화', '\\cite{madaio2020co}'),
    ('데이터시트', '\\cite{holland2018dataset}'),
    ('도구 선정', '\\cite{amershi2019software}'),
    ('관측성', '\\cite{shankar2022operationalizing}'),
])

# ===== Ch07 Case Studies (currently 0, need 20+) =====
process_chapter('07_case_studies.tex', [
    ('신용평가', '\\cite{fuster2022predictably}'),
    ('공정성 관리', '\\cite{mehrabi2021survey}'),
    ('편향', '\\cite{buolamwini2018gender}'),
    ('의료 AI', '\\cite{topol2019high}'),
    ('임상 검증', '\\cite{kelly2019key}'),
    ('진단 보조', '\\cite{rajpurkar2022ai}'),
    ('모니터링', '\\cite{klaise2021monitoring}'),
    ('설명가능성', '\\cite{arrieta2020explainable}'),
    ('AI 행정', '\\cite{wirtz2019artificial}'),
    ('공공기관', '\\cite{kuziemski2020ai}'),
    ('시민 신뢰', '\\cite{zuiderwijk2021implications}'),
    ('데이터 거버넌스', '\\cite{janssen2020data}'),
    ('모델 카드', '\\cite{mitchell2019model}'),
    ('영향평가', '\\cite{raji2020closing}'),
    ('품질 관리', '\\cite{wuest2016machine}'),
    ('제조 AI', '\\cite{li2017applications}'),
    ('SHAP', '\\cite{lundberg2017unified}'),
    ('ISO/IEC 42001', '\\cite{iso42001}'),
    ('EU AI Act', '\\cite{eu2024aiact}'),
    ('AI 기본법', '\\cite{cset2025korea_ai_act}'),
    ('드리프트', '\\cite{paleyes2022challenges}'),
])

# ===== Ch08 Usecase Discovery (currently 5, need 15+) =====
process_chapter('08_usecase_discovery.tex', [
    ('ROI 분석', '\\cite{brynjolfsson2017business}'),
    ('기술적 실현가능성', '\\cite{amershi2019software}'),
    ('데이터 준비도', '\\cite{sambasivan2021everyone}'),
    ('조직 준비도', '\\cite{fountaine2019building}'),
    ('유스케이스', '\\cite{ransbotham2017reshaping}'),
    ('포트폴리오', '\\cite{iansiti2020competing}'),
    ('다기준 의사결정', '\\cite{barbosa2023mcdm}'),
    ('심의위원회', '\\cite{raji2020closing}'),
    ('윤리 스크리닝', '\\cite{morley2020from}'),
    ('EU AI Act', '\\cite{eu2024aiact}'),
    ('기본법', '\\cite{cset2025korea_ai_act}'),
    ('리소스 배분', '\\cite{bughin2018notes}'),
    ('AI 프로젝트', '\\cite{davenport2018advantage}'),
    ('비즈니스 가치', '\\cite{enholm2022artificial}'),
    ('위험 분류', '\\cite{nist2023airmf}'),
    ('투명성', '\\cite{arrieta2020explainable}'),
])

# ===== Ch09 Data Governance (currently 4, need 16+) =====
process_chapter('09_data_governance.tex', [
    ('데이터 요구사항', '\\cite{janssen2020data}'),
    ('데이터 패브릭', '\\cite{gartner2021datafabric}'),
    ('데이터 품질', '\\cite{redman2008data}'),
    ('데이터시트', '\\cite{gebru2021datasheets}'),
    ('편향의 유형', '\\cite{mehrabi2021survey}'),
    ('피처 스토어', '\\cite{delarua2024hopsworks}'),
    ('계보', '\\cite{wilkinson2016fair}'),
    ('메타데이터', '\\cite{holland2018dataset}'),
    ('접근 제어', '\\cite{abadi2016deep}'),
    ('차분 프라이버시', '\\cite{dwork2014algorithmic}'),
    ('연합학습', '\\cite{mcmahan2017communication}'),
    ('머신 언러닝', '\\cite{bourtoule2021unlearning}'),
    ('사전 학습 모델', '\\cite{bommasani2021opportunities}'),
    ('오픈소스', '\\cite{paullada2021data}'),
    ('CDO', '\\cite{ladley2019data}'),
    ('FAIR', '\\cite{wilkinson2016fair}'),
    ('데이터 카드', '\\cite{breck2019data}'),
])

# ===== Ch10 Model Development (currently 5, need 15+) =====
process_chapter('10_model_development.tex', [
    ('모델 카드(Model Card)', '\\cite{mitchell2019model}'),
    ('데이터시트', '\\cite{gebru2021datasheets}'),
    ('실험 추적', '\\cite{zaharia2018accelerating}'),
    ('재현성', '\\cite{studer2021towards}'),
    ('공정성 지표', '\\cite{mehrabi2021survey}'),
    ('편향 완화', '\\cite{bellamy2019ai}'),
    ('적대적 공격', '\\cite{goodfellow2014explaining}'),
    ('SHAP', '\\cite{lundberg2017unified}'),
    ('LIME', '\\cite{ribeiro2016why}'),
    ('모델 승인', '\\cite{brundage2020trustworthy}'),
    ('소프트웨어 공학', '\\cite{amershi2019software}'),
    ('생명주기', '\\cite{ashmore2021assuring}'),
    ('강건성', '\\cite{madry2018towards}'),
    ('배포 전 체크리스트', '\\cite{shneiderman2020bridging}'),
    ('개발 환경', '\\cite{kreuzberger2023machine}'),
    ('코드 리뷰', '\\cite{sculley2015hidden}'),
])

# ===== Ch11 Audit Certification (currently 3, need 17+) =====
process_chapter('11_audit_certification.tex', [
    ('감사의 목적', '\\cite{mokander2023auditing}'),
    ('감사 유형', '\\cite{koshiyama2022algorithm}'),
    ('내부 감사', '\\cite{raji2020closing}'),
    ('외부 감사', '\\cite{falco2021governing}'),
    ('알고리즘 감사', '\\cite{metaxa2021auditing}'),
    ('ISO/IEC 42001', '\\cite{iso42001}'),
    ('적합성 평가', '\\cite{mokander2022conformity}'),
    ('감사 체크리스트', '\\cite{brundage2020trustworthy}'),
    ('투명성', '\\cite{arrieta2020explainable}'),
    ('공정성', '\\cite{bellamy2019ai}'),
    ('설명가능성', '\\cite{sokol2020explainability}'),
    ('NIST', '\\cite{nist2023airmf}'),
    ('EU AI Act', '\\cite{eu2024aiact}'),
    ('지속적 감사', '\\cite{shneiderman2020bridging}'),
    ('모니터링', '\\cite{klaise2021monitoring}'),
    ('지적사항', '\\cite{cobbe2021reviewable}'),
    ('개선 계획', '\\cite{batool2025ai_governance}'),
    ('위험관리', '\\cite{iso23894}'),
])

# ===== Ch12 Operation Lifecycle (currently 6, need 14+) =====
process_chapter('12_operation_lifecycle.tex', [
    ('Retire 기준', '\\cite{klaise2021monitoring}'),
    ('좀비 모델', '\\cite{tamburri2020sustainable}'),
    ('아카이브', '\\cite{huyen2022designing}'),
    ('머신 언러닝', '\\cite{bourtoule2021unlearning}'),
    ('Retire 프로세스', '\\cite{ashmore2021assuring}'),
    ('기술 부채', '\\cite{sculley2015hidden}'),
    ('LLM', '\\cite{bommasani2021opportunities}'),
    ('RAG', '\\cite{lewis2020retrieval}'),
    ('프롬프트', '\\cite{openai2023gpt4}'),
    ('계보', '\\cite{wilkinson2016fair}'),
    ('지식 보존', '\\cite{sato2019continuous}'),
    ('드리프트', '\\cite{paleyes2022challenges}'),
    ('모니터링', '\\cite{shankar2022operationalizing}'),
    ('리소스 최적화', '\\cite{amershi2019software}'),
])

# ===== Ch12b Generative AI (currently 0, need 20+) =====
process_chapter('12b_generative_ai.tex', [
    ('환각(Hallucination)', '\\cite{ji2023survey}'),
    ('저작권', '\\cite{bommasani2021opportunities}'),
    ('딥페이크', '\\cite{weidinger2021ethical}'),
    ('프롬프트 인젝션', '\\cite{carlini2021extracting}'),
    ('도입 전 평가', '\\cite{liang2022holistic}'),
    ('사용 정책', '\\cite{taeihagh2025governing}'),
    ('RAG', '\\cite{lewis2020retrieval}'),
    ('벤치마크', '\\cite{openai2023gpt4}'),
    ('인간 평가', '\\cite{ouyang2022training}'),
    ('LLM-as-Judge', '\\cite{brown2020language}'),
    ('RLHF', '\\cite{anthropic2023constitutional}'),
    ('DPO', '\\cite{touvron2023llama}'),
    ('에이전트', '\\cite{wei2022emergent}'),
    ('도구 사용', '\\cite{kaplan2020scaling}'),
    ('토큰 관리', '\\cite{bender2021stochastic}'),
    ('가드레일', '\\cite{casper2023explore}'),
    ('레드팀', '\\cite{brundage2020trustworthy}'),
    ('모니터링', '\\cite{klaise2021monitoring}'),
    ('EU AI Act', '\\cite{eu2024aiact}'),
    ('AI 기본법', '\\cite{cset2025korea_ai_act}'),
    ('데이터 거버넌스', '\\cite{paullada2021data}'),
])

# ===== Ch13 Architecture (currently 5, need 15+) =====
process_chapter('13_architecture.tex', [
    ('설계 원칙', '\\cite{amershi2019software}'),
    ('MLOps 참조', '\\cite{kreuzberger2023machine}'),
    ('Feature Store', '\\cite{delarua2024hopsworks}'),
    ('Model 레지스트리', '\\cite{zaharia2018accelerating}'),
    ('마이크로서비스', '\\cite{baylor2017tfx}'),
    ('벡터 임베딩', '\\cite{carlini2021extracting}'),
    ('RAG 품질', '\\cite{lewis2020retrieval}'),
    ('프롬프트 거버넌스', '\\cite{openai2023gpt4}'),
    ('가드레일', '\\cite{casper2023explore}'),
    ('에이전트', '\\cite{wei2022emergent}'),
    ('CI/CD', '\\cite{sato2019continuous}'),
    ('Policy as Code', '\\cite{hinrichs2019opa}'),
    ('거버넌스 자동화', '\\cite{sculley2015hidden}'),
    ('OWASP', '\\cite{biggio2018wild}'),
    ('기술 부채', '\\cite{paleyes2022challenges}'),
    ('Data Fabric', '\\cite{gartner2021datafabric}'),
])

# ===== Ch14 Tools Platform (currently 12, need 8+) =====
process_chapter('14_tools_platform.tex', [
    ('모델 레지스트리', '\\cite{amershi2019software}'),
    ('재현성의 중요성', '\\cite{studer2021towards}'),
    ('Silent Failure', '\\cite{klaise2021monitoring}'),
    ('관측성', '\\cite{shankar2022operationalizing}'),
    ('GenAI 모니터링', '\\cite{ji2023survey}'),
    ('Policy-as-Code', '\\cite{stix2021actionable}'),
    ('통합 거버넌스 플랫폼', '\\cite{batool2025ai_governance}'),
    ('자동화된 모델 검증', '\\cite{brundage2020trustworthy}'),
    ('규정 준수', '\\cite{mokander2022conformity}'),
])

# ===== Ch15 Security Privacy (currently 18, need 2+) =====
process_chapter('15_security_privacy.tex', [
    ('멤버십 추론', '\\cite{shokri2017membership}'),
    ('연합 학습', '\\cite{kairouz2021advances}'),
    ('동형 암호', '\\cite{abadi2016deep}'),
])

# ===== Ch16 Healthcare (currently 3, need 17+) =====
process_chapter('16_healthcare.tex', [
    ('SaMD', '\\cite{fda2021ai}'),
    ('규제 기관별', '\\cite{kelly2019key}'),
    ('설명가능성', '\\cite{arrieta2020explainable}'),
    ('건강 불평등', '\\cite{obermeyer2019dissecting}'),
    ('데이터 편향', '\\cite{mehrabi2021survey}'),
    ('자동화 편향', '\\cite{sendak2020real}'),
    ('데이터 비식별화', '\\cite{dwork2014algorithmic}'),
    ('연합학습', '\\cite{mcmahan2017communication}'),
    ('합성 데이터', '\\cite{ghassemi2020review}'),
    ('FHIR', '\\cite{char2018implementing}'),
    ('CDSS', '\\cite{wiens2019do}'),
    ('원격의료', '\\cite{davenport2019potential}'),
    ('사이버보안', '\\cite{biggio2018wild}'),
    ('영상의학', '\\cite{esteva2017dermatologist}'),
    ('당뇨', '\\cite{gulshan2016development}'),
    ('유방암', '\\cite{mckinney2020international}'),
    ('AI 통합', '\\cite{rajpurkar2022ai}'),
    ('임상 워크플로우', '\\cite{topol2019high}'),
])

# ===== Ch17 Finance (currently 5, need 15+) =====
process_chapter('17_finance.tex', [
    ('국내 금융', '\\cite{fsc2024ai}'),
    ('글로벌 금융', '\\cite{oecd2024regulatory_ai_finance}'),
    ('모델 리스크', '\\cite{occ2011sr117}'),
    ('공정 대출', '\\cite{bartlett2022consumer}'),
    ('이상거래탐지', '\\cite{cao2022ai}'),
    ('로보어드바이저', '\\cite{dixon2020machine}'),
    ('레그테크', '\\cite{arner2017fintech}'),
    ('3선 방어', '\\cite{falco2021governing}'),
    ('설명가능성', '\\cite{bracke2019machine}'),
    ('핀테크', '\\cite{philippon2020fintech}'),
    ('EU', '\\cite{eba2020big}'),
    ('편향', '\\cite{fuster2022predictably}'),
    ('FINRA', '\\cite{finra_2026_report}'),
    ('금융위원회', '\\cite{fsc_genai_2025}'),
    ('FSB', '\\cite{fsb2017crypto}'),
    ('신용평가', '\\cite{oecd2021ai}'),
])

# ===== Ch18 Public (currently 4, need 16+) =====
process_chapter('18_public.tex', [
    ('공공성', '\\cite{wirtz2019artificial}'),
    ('시민 신뢰', '\\cite{zuiderwijk2021implications}'),
    ('행정기본법', '\\cite{korea2021admin}'),
    ('지능정보화', '\\cite{korea2020intel}'),
    ('시민 참여', '\\cite{sun2019mapping}'),
    ('AI 조달', '\\cite{kuziemski2020ai}'),
    ('민주적 책임성', '\\cite{coglianese2017regulating}'),
    ('알고리즘', '\\cite{veale2019administration}'),
    ('공공데이터', '\\cite{janssen2020data}'),
    ('가이드라인', '\\cite{nia2024quality}'),
    ('TTA', '\\cite{tta2024trust}'),
    ('투명성', '\\cite{arrieta2020explainable}'),
    ('편향', '\\cite{mehrabi2021survey}'),
    ('EU AI Act', '\\cite{eu2024aiact}'),
    ('기본법', '\\cite{cset2025korea_ai_act}'),
    ('성숙도', '\\cite{batool2025ai_governance}'),
    ('영향평가', '\\cite{raji2020closing}'),
])

# ===== Ch19 Industrial (currently 4, need 16+) =====
process_chapter('19_industrial.tex', [
    ('안전 중심', '\\cite{amodei2016concrete}'),
    ('OT-IT 융합', '\\cite{monostori2016cyber}'),
    ('IEC 61508', '\\cite{iec61508}'),
    ('ISO 13849', '\\cite{iso13849}'),
    ('UL 4600', '\\cite{ul4600}'),
    ('예지보전', '\\cite{wuest2016machine}'),
    ('품질 검사', '\\cite{zhong2017intelligent}'),
    ('디지털 트윈', '\\cite{tao2018digital}'),
    ('Industry 4.0', '\\cite{wang2018towards}'),
    ('CPS', '\\cite{lee2018cyber}'),
    ('모델 변경', '\\cite{kreuzberger2023machine}'),
    ('드리프트', '\\cite{paleyes2022challenges}'),
    ('AI 거버넌스 조직', '\\cite{mantymaki2022defining}'),
    ('에너지', '\\cite{windmann2024artificial}'),
    ('ISO/IEC 42001', '\\cite{iso42001}'),
    ('설명가능성', '\\cite{arrieta2020explainable}'),
    ('안전성 평가', '\\cite{ashmore2021assuring}'),
])

# ===== Ch20 Future (currently 1, need 19+) =====
process_chapter('20_future.tex', [
    ('AGI', '\\cite{bostrom2014superintelligence}'),
    ('초지능', '\\cite{russell2019human}'),
    ('멀티에이전트', '\\cite{wei2022emergent}'),
    ('뉴로심볼릭', '\\cite{arrieta2020explainable}'),
    ('글로벌 규제', '\\cite{bradford2020brussels}'),
    ('브뤼셀 효과', '\\cite{smuha2021race}'),
    ('AI 기본법', '\\cite{cset2025korea_ai_act}'),
    ('ESG', '\\cite{vinuesa2020role}'),
    ('성숙도 모델', '\\cite{batool2025ai_governance}'),
    ('인재 양성', '\\cite{fountaine2019building}'),
    ('PDCA', '\\cite{iso42001}'),
    ('KPI', '\\cite{shankar2022operationalizing}'),
    ('극단적 리스크', '\\cite{bengio2024managing}'),
    ('인간 성능', '\\cite{grace2018when}'),
    ('사회적 계약', '\\cite{rahwan2018society}'),
    ('SDGs', '\\cite{vinuesa2020role}'),
    ('AI 안전', '\\cite{hendrycks2021unsolved}'),
    ('구체적 문제', '\\cite{amodei2016concrete}'),
    ('표준', '\\cite{cihon2019standards}'),
    ('협력', '\\cite{askell2019role}'),
    ('절벽', '\\cite{ord2020precipice}'),
])

print("\n=== DONE ===")
