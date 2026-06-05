import os

chapters = {
    "01_concept": "AI 거버넌스의 개념과 필요성",
    "02_global_frameworks": "글로벌 AI 거버넌스 프레임워크 비교 분석",
    "03_ethics_operationalization": "AI 윤리 원칙의 운용화(Operationalization)",
    "04_organization": "AI 거버넌스 조직 설계",
    "05_policy": "AI 정책 체계 수립",
    "06_risk_management": "AI 리스크 관리 프레임워크",
    "07_roadmap": "AI 거버넌스 로드맵 수립",
    "08_usecase_discovery": "AI 유스케이스 발굴과 사전 승인",
    "09_data_governance": "데이터 거버넌스와 AI 거버넌스의 통합",
    "10_model_development": "모델 개발 단계의 거버넌스",
    "11_deployment_ops": "모델 배포 및 운영 단계의 거버넌스",
    "12_retirement": "모델 폐기와 아카이빙",
    "13_architecture": "AI 시스템 아키텍처와 거버넌스",
    "14_tools_platform": "거버넌스 도구와 플랫폼",
    "15_security_privacy": "보안과 프라이버시의 기술적 구현",
    "16_healthcare": "헬스케어 AI 거버넌스",
    "17_finance": "금융 AI 거버넌스",
    "18_public": "공공부문 AI 거버넌스",
    "19_manufacturing": "제조/산업 AI 거버넌스",
    "20_future": "AI 거버넌스의 미래와 지속적 진화"
}

base_path = "/home/babelai/personal-dev/latex-book/chapters"
os.makedirs(base_path, exist_ok=True)

for filename, title in chapters.items():
    file_path = os.path.join(base_path, f"{filename}.tex")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"\\chapter{{{title}}}\n\n")
        f.write("% 내용 작성 필요\n")
        
print("Chapters created successfully.")
