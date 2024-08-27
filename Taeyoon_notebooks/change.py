import json
import xml.etree.ElementTree as ET


# 입력 파일과 출력 파일 경로
input_file_path = 'nikluge-gtps-2023-train.jsonl'
output_file_path = 'output1.jsonl'

def filter_and_convert_table(input_data):
    # 'table'과 'highlighted_cells' 추출
    table = input_data.get('table', [])
    highlighted_cells = input_data['metadata'].get('highlighted_cells', [])

    # 새로운 테이블 필터링
    filtered_table = []
    for cell in highlighted_cells:
        row_idx, col_idx = cell
        for item in table:
            if item['row'] == col_idx and item['col'] == row_idx:
                filtered_table.append(item)
    
    # XML 변환
    root = ET.Element('table')
    if filtered_table:
        for item in filtered_table:
            cell_element = ET.SubElement(root, 'cell')
            cell_element.set('row', str(item['row']))
            cell_element.set('col', str(item['col']))
            cell_element.text = item['value']
    
    # XML 문자열 생성
    xml_string = ET.tostring(root, encoding='unicode')
    
    return xml_string

# 파일을 줄 단위로 읽고 처리하여 다시 저장
with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
    for line in infile:
        try:
            # JSON 라인 파싱
            data = json.loads(line)
            input_data = data['input']  # 'input' 키의 데이터 추출

            # 테이블 필터링 및 XML 변환
            xml_table = filter_and_convert_table(input_data)

            # 빈 테이블인지 확인
            if xml_table.strip() != "<table />":  # 빈 테이블이 아니면 저장
                data['input']['table'] = xml_table
                outfile.write(json.dumps(data, ensure_ascii=False) + '\n')
            else:
                print(f"Skipping empty table for id: {data['id']}")
        
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
