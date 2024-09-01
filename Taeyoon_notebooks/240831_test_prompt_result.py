import json

# 첫 번째 파일 (analysis 포함)을 읽어옵니다.
with open('240831_prompt_results.jsonl', 'r', encoding='utf-8') as file1:
    first_file_data = [json.loads(line) for line in file1]

# 두 번째 파일 (analysis 미포함)을 읽어옵니다.
with open('nikluge-gtps-2023-train.jsonl', 'r', encoding='utf-8') as file2:
    second_file_data = [json.loads(line) for line in file2]

# 두 번째 파일의 첫 7097개 항목에 첫 번째 파일의 "analysis" 항목을 추가합니다.
for idx in range(7097):
    second_file_data[idx]['analysis'] = first_file_data[idx]['analysis']

# 결과를 새로운 .jsonl 파일로 저장합니다.
with open('240831_combined_file.jsonl', 'w', encoding='utf-8') as outfile:
    for entry in second_file_data:
        outfile.write(json.dumps(entry, ensure_ascii=False) + '\n')
