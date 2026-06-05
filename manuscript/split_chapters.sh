#!/bin/bash
cd /home/babelai/personal-dev/latex-book
mkdir -p chapters_pdf

split_chapter() {
    local name=$1 start=$2 end=$3
    pdfseparate -f $start -l $end main.pdf "chapters_pdf/tmp_${name}_%d.pdf"
    pdfunite chapters_pdf/tmp_${name}_*.pdf "chapters_pdf/${name}.pdf" 2>/dev/null
    rm -f chapters_pdf/tmp_${name}_*.pdf
    echo "${name}.pdf done"
}

split_chapter "00_preface" 1 1
split_chapter "01_concept" 2 34
split_chapter "02_global_frameworks" 35 60
split_chapter "03_ethics" 61 80
split_chapter "04_organization" 81 104
split_chapter "05_policy" 105 137
split_chapter "06_governance_tools" 138 170
split_chapter "07_case_studies" 171 200
split_chapter "08_usecase_discovery" 201 231
split_chapter "09_data_governance" 232 257
split_chapter "10_model_development" 258 291
split_chapter "11_audit_certification" 292 318
split_chapter "12_operation_lifecycle" 319 348
split_chapter "13_generative_ai" 349 377
split_chapter "14_architecture" 378 406
split_chapter "15_tools_platform" 407 432
split_chapter "16_security_privacy" 433 461
split_chapter "17_healthcare" 462 490
split_chapter "18_finance" 491 519
split_chapter "19_public" 520 546
split_chapter "20_industrial" 547 571
split_chapter "21_future" 572 599
split_chapter "appendix_a" 600 605
split_chapter "appendix_b" 606 608
split_chapter "appendix_c" 609 610
split_chapter "appendix_d" 611 613
split_chapter "appendix_e" 614 620
split_chapter "bibliography" 621 642

echo "=== ALL DONE ==="
ls -lh chapters_pdf/*.pdf | awk '{print $5, $9}'
