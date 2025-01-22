# Tabular-TX: Theme-Explanation Structure-based Table Summarization via In-Context Learning

(**논문 링크**)[https://arxiv.org/abs/2501.10487]

## Introduction
**Tabular-TX**는 **In-Context Learning(ICL)** 방식을 활용하여 테이블 데이터를 요약하는 **Theme-Explanation 구조** 기반 파이프라인입니다. 기존 테이블 요약 방법은 대규모 언어모델(LLM) 직접 학습(fine-tuning)이 필요하거나, 대화형 방식으로 정확한 맥락을 유지하기 어려운 문제가 있었습니다. Tabular-TX는 테이블에서 핵심 주제(Theme)와 설명(Explanation)을 분리해, **최소한의 자원**으로도 정확도 높은 문장을 생성할 수 있도록 돕습니다.

본 레포지토리는 Tabular-TX의 구현체와 실험 결과를 포함하고 있으며, 특히 **한국어 테이블 요약**에 대한 우수한 성능을 보입니다.


## Key Features
- **Theme-Explanation 구조**  
  - **Theme Part**: 테이블 제목 등을 활용해 요약 대상(주제)을 강조합니다.  
  - **Explanation Part**: 테이블의 주요 셀들을 분석 및 설명합니다.
- **In-Context Learning (ICL)**: 별도의 파인튜닝 없이 예시(프롬프트)만으로 LLM 활용이 가능합니다.
- **효율적인 전처리(Preprocessing)**: 테이블을 key-value 딕셔너리 형태로 변환하여 모델 이해도를 높입니다.
- **다양한 데이터 타입 지원**: 수치, 퍼센트, 텍스트 등 다양한 형식을 분석하여 정확한 요약을 생성합니다.


## Usage Example
간단한 예시를 통해 Tabular-TX가 어떤 식으로 데이터를 입력받고 요약문을 생성하는지 살펴볼 수 있습니다.

**Input (예시 테이블 JSON)**:
```json
{
  "title": "K-POP Albums Sales",
  "header": ["Artist", "Album", "Sales", "Release Date"],
  "data": [
    ["Group A", "Album X", "1,000,000", "2023-01-10"],
    ["Group B", "Album Y", "750,000", "2023-03-15"]
  ]
}
```

**Output (요약 결과)**:
```
Theme: "K-POP Albums Sales에 따르면"
Explanation: "올해 1월에 발매된 Group A의 Album X가 100만 장으로 가장 높은 판매량을 보이며, Group B는 약 75만 장을 판매했습니다."
```


## Repository Structure
- `src/`: Tabular-TX 파이프라인의 메인 소스 코드
  - `preprocess.py`: 테이블을 key-value 형태로 변환하는 전처리 스크립트
  - `run_tabular_tx.py`: 전처리된 데이터를 요약하는 메인 파이프라인
  - `evaluate.py`: 요약 결과를 평가하기 위한 스크립트 (ROUGE, BLEU 등)
- `data/`: 실험용 예시 데이터셋
- `notebooks/`: Jupyter 노트북 (추가 실험, 시각화 및 튜토리얼)
- `results/`: 실험 결과 및 평가 지표


## Installation
아래 단계대로 로컬 환경에서 프로젝트를 실행할 수 있습니다:

1. **레포지토리 클론**  
   ```bash
   git clone https://github.com/your-repo/Tabular-TX.git
   cd Tabular-TX
   ```

2. **의존성 패키지 설치**  
   ```bash
   pip install -r requirements.txt
   ```
   > Python 3.7 이상 환경을 권장합니다.


## Usage

### 1. Preprocess Tabular Data
```bash
python src/preprocess.py \
  --input data/sample_table.json \
  --output data/processed_table.json
```
- **input**: 원본 테이블 JSON 파일 경로  
- **output**: 전처리된 key-value 딕셔너리 파일 경로  

### 2. Run Tabular-TX
```bash
python src/run_tabular_tx.py \
  --input data/processed_table.json \
  --output results/summaries.json
```
- **input**: 전처리된 JSON 파일  
- **output**: 요약 결과가 기록될 JSON 파일  

### 3. Evaluate
```bash
python src/evaluate.py \
  --predictions results/summaries.json \
  --references data/ground_truth.json
```
- **predictions**: 모델이 생성한 요약 문서 경로  
- **references**: 정답(래퍼런스) 문서 경로  
- ROUGE 및 BLEU 스코어가 콘솔에 출력됩니다.


## Results
아래 표는 Tabular-TX가 달성한 핵심 평가 지표(ROUGE, BLEU)를 보여줍니다:

| Model                        | ROUGE-1 | ROUGE-L | BLEU | Average |
|------------------------------|---------|---------|------|---------|
| **Tabular-TX (EXAONE)**      | 0.51    | 0.39    | 0.44 | 0.45    |
| **Tabular-TX (Llama-Korean)**| 0.48    | 0.37    | 0.42 | 0.43    |
| Fine-tuned Baseline          | 0.37    | 0.28    | 0.35 | 0.33    |


## Contributing
Tabular-TX는 오픈 소스로 운영됩니다. 새로운 기능 제안이나 버그 리포트를 원하시면 [이슈](https://github.com/your-repo/Tabular-TX/issues)를 통해 남겨주세요.  
풀 리퀘스트(PR)도 언제나 환영합니다!


## HCLT-KACL2024
아래는 HCLT-KACL2024 관련 링크 모음입니다:
- 말평 제공 baseline GitHub: [링크](https://github.com/teddysum/korean_T2T_baseline/tree/main)
- KoBART 학습 코드: [링크](https://github.com/teddysum/korean_T2T_baseline/blob/main/run/train.py)
- 공식 scoring 코드: [링크](https://github.com/teddysum/korean_T2T_baseline/blob/main/run/scoring.py)


## Citation
이 프로젝트가 연구에 도움이 되었다면, 아래의 논문을 인용해주세요:
```
@inproceedings{kwack2024tabularTX,
  title={Tabular-TX: Theme-Explanation Structure-based Table Summarization via In-Context Learning},
  author={Kwack, TaeYoon and Kim, Jisoo and Jung, Ki Yong and Lee, DongGeon and Park, Heesun},
  booktitle={Proceedings of the 36th Korean Information Processing Conference},
  year={2024}
}
```


## License
이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [`LICENSE`](LICENSE) 파일을 참고하세요.


## Contact
프로젝트 관련 문의 사항은 아래 이메일로 연락 부탁드립니다:
- TaeYoon Kwack: [njj05043@g.skku.edu](mailto:njj05043@g.skku.edu)
- Jisoo Kim: [clrdln@g.skku.edu](mailto:clrdln@g.skku.edu)
- KiYong Jung: [wjdrldyd0213@g.skku.edu](mailto:wjdrldyd0213@g.skku.edu)
- Heesun Park: [hspark20@skku.edu](mailto:hspark20@skku.edu)
