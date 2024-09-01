import json

# .jsonl 파일 경로
file_path = r'./240831_prompt_results.jsonl'

# average_score 값을 저장할 리스트 초기화
average_scores = []

# .jsonl 파일 읽기 및 average_score 값 추출
with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        average_scores.append(data['analysis']['average_score'])

# average_score의 평균 계산
overall_average_score = sum(average_scores) / len(average_scores)

# 결과 출력
print(f'전체 average_score의 평균: {overall_average_score}')
