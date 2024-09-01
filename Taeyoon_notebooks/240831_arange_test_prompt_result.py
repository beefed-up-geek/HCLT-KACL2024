import json

# 원본 파일 경로
input_file_path = '240831_combined_file.jsonl'

# 결과 파일 경로
output_file_path = '240831_sorted_output_file.jsonl'

# JSONL 파일 읽기
with open(input_file_path, 'r', encoding='utf-8') as infile:
    data = [json.loads(line) for line in infile]

# 'analysis' 항목이 있는 데이터만 필터링 및 정렬
filtered_sorted_data = sorted(
    [item for item in data if 'analysis' in item], 
    key=lambda x: x['analysis']['average_score']
)

# 필터링 및 정렬된 데이터를 새로운 JSONL 파일로 저장
with open(output_file_path, 'w', encoding='utf-8') as outfile:
    for entry in filtered_sorted_data:
        outfile.write(json.dumps(entry, ensure_ascii=False) + '\n')