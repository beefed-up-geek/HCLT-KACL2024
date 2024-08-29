import json
import re

# 파일 경로 설정
file_path = 'train_full_for_prompt.jsonl'

matching_line_numbers = []

# 숫자 패턴
number_pattern = r'<value>\d+</value>'

# 파일을 줄 단위로 읽기
with open(file_path, 'r', encoding='utf-8') as file:
    for line_number, line in enumerate(file, 1):
        data = json.loads(line)
        
        table_xml = data['input']['table_xml']
        output_text = ' '.join(data['output'])
        
        # table_xml에서 <value>태그 내의 숫자 찾기
        numbers_in_table = re.findall(number_pattern, table_xml)
        
        # 조건 체크
        if len(numbers_in_table) >= 20 and "만 원" not in table_xml and "만원" not in table_xml:
            if "만 원" in output_text or "만원" in output_text:
                matching_line_numbers.append(line_number)

# 결과 출력
print(f"조건에 맞는 줄번호: {matching_line_numbers}")