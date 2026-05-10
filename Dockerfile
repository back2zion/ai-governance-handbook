FROM python:3.10-slim

LABEL maintainer="곽두일 <babel.ai.dub@gmail.com>"
LABEL description="AI Governance Handbook — 완전 통제된 거버넌스 실습 환경"

WORKDIR /workspace

# 시스템 의존성
RUN apt-get update && apt-get install -y --no-install-recommends \
    git curl build-essential \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 (핵심만, torch 제외 — 용량 절약)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 복사
COPY . .

# Jupyter 설정
EXPOSE 8888
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--notebook-dir=/workspace/notebooks"]
