"""
aigov CLI — AI 거버넌스 커맨드라인 도구

사용법:
  python -m aigov check  --data data.csv --sensitive gender
  python -m aigov drift  --baseline train.csv --current prod.csv
  python -m aigov audit  --output report.json
"""
import argparse
import sys


def cmd_check(args):
    """공정성 진단 실행."""
    import pandas as pd
    import numpy as np
    from core.fairness import FairnessAuditor

    print(f"\n[aigov check] 공정성 진단 시작")
    print(f"  데이터: {args.data}")
    print(f"  민감 속성: {args.sensitive}\n")

    try:
        df = pd.read_csv(args.data)
    except FileNotFoundError:
        print(f"오류: '{args.data}' 파일을 찾을 수 없습니다.")
        sys.exit(1)

    if args.target not in df.columns or args.pred not in df.columns:
        print(f"오류: '{args.target}' 또는 '{args.pred}' 컬럼이 없습니다.")
        sys.exit(1)

    y_true = df[args.target].values
    y_pred = df[args.pred].values

    auditor = FairnessAuditor(sensitive_attribute=args.sensitive,
                              model_name=args.model_name or args.data)
    report = auditor.audit(df, y_true, y_pred)
    print(report.summary())

    if args.output:
        import json
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump({
                "model": report.model_name,
                "sensitive_attr": report.sensitive_attr,
                "dpr": report.demographic_parity_ratio,
                "eod": report.equal_opportunity_diff,
                "risk_level": report.risk_level,
                "recommendations": report.recommendations,
            }, f, ensure_ascii=False, indent=2)
        print(f"\n결과 저장: {args.output}")

    sys.exit(0 if report.risk_level == "LOW" else 1)


def cmd_drift(args):
    """드리프트 감지 실행."""
    import pandas as pd
    from core.drift import DriftDetector

    print(f"\n[aigov drift] 드리프트 감지 시작")
    print(f"  기준 데이터: {args.baseline}")
    print(f"  현재 데이터: {args.current}\n")

    try:
        baseline = pd.read_csv(args.baseline)
        current = pd.read_csv(args.current)
    except FileNotFoundError as e:
        print(f"오류: {e}")
        sys.exit(1)

    detector = DriftDetector(baseline)
    reports = detector.detect(current)
    detector.print_summary(reports)

    drifted = [r for r in reports if r.status == "drift"]
    sys.exit(1 if drifted else 0)


def cmd_audit(args):
    """거버넌스 감사 리포트 생성."""
    from core.audit import GovernanceAuditor

    print(f"\n[aigov audit] 거버넌스 감사 시작")
    model_name = args.model_name or "Unknown"
    auditor = GovernanceAuditor(model_name, auditor_name="aigov-cli")

    manual = {}
    if args.checklist:
        import json
        with open(args.checklist) as f:
            manual = json.load(f)

    record = auditor.audit(manual_checks=manual)

    print(f"  감사 ID   : {record.audit_id}")
    print(f"  모델명    : {record.model_name}")
    print(f"  점수      : {record.score:.1%}")
    print(f"  위험 등급 : {record.risk_level}")
    if record.findings:
        print(f"\n미충족 항목 ({len(record.findings)}개):")
        for f in record.findings:
            print(f"  ✗ {f}")
    if record.recommendations:
        print(f"\n권고 사항:")
        for r in record.recommendations:
            print(f"  → {r}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(record.to_json())
        print(f"\n리포트 저장: {args.output}")

    sys.exit(0 if record.passed() else 1)


def main():
    parser = argparse.ArgumentParser(
        prog="aigov",
        description="AI Governance Handbook CLI — 공정성·드리프트·감사 도구"
    )
    sub = parser.add_subparsers(dest="command")

    # check 서브커맨드
    p_check = sub.add_parser("check", help="공정성 진단 (Fairness Audit)")
    p_check.add_argument("--data", required=True, help="데이터 CSV 경로")
    p_check.add_argument("--sensitive", default="gender", help="민감 속성 컬럼명")
    p_check.add_argument("--target", default="label", help="정답 레이블 컬럼명")
    p_check.add_argument("--pred", default="prediction", help="예측값 컬럼명")
    p_check.add_argument("--model-name", help="모델 이름 (보고서용)")
    p_check.add_argument("--output", help="결과 JSON 저장 경로")

    # drift 서브커맨드
    p_drift = sub.add_parser("drift", help="드리프트 감지 (Data Drift Detection)")
    p_drift.add_argument("--baseline", required=True, help="기준 데이터 CSV")
    p_drift.add_argument("--current", required=True, help="현재 데이터 CSV")

    # audit 서브커맨드
    p_audit = sub.add_parser("audit", help="거버넌스 종합 감사 리포트")
    p_audit.add_argument("--model-name", help="모델 이름")
    p_audit.add_argument("--checklist", help="수동 체크리스트 JSON 파일")
    p_audit.add_argument("--output", help="감사 리포트 저장 경로")

    args = parser.parse_args()

    if args.command == "check":
        cmd_check(args)
    elif args.command == "drift":
        cmd_drift(args)
    elif args.command == "audit":
        cmd_audit(args)
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
