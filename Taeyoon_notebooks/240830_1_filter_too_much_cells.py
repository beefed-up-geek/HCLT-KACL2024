import json

def process_jsonl_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            data = json.loads(line)
            
            # table에서 셀의 개수를 계산
            table = data['input']['table']
            cell_count = len(table)
            
            # 셀의 개수가 75개 초과하는지 확인
            if cell_count > 75:
                highlighted_cells = data['input']['metadata']['highlighted_cells']
                highlighted_indices = {(col, row) for col, row in highlighted_cells}
                
                # highlighted_cells에 포함되지 않은 셀들을 필터링
                filtered_table = [cell for cell in table if (cell['col'], cell['row']) in highlighted_indices]
                
                # table을 필터링된 테이블로 교체
                data['input']['table'] = filtered_table
            
            # 수정된 데이터를 출력 파일에 기록
            outfile.write(json.dumps(data, ensure_ascii=False) + '\n')

# 사용 예시
input_file = '240829_2_remove_redundancy.jsonl'
output_file = '240830_final_data.jsonl'
process_jsonl_file(input_file, output_file)
