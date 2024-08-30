import json

def filter_table(table, highlighted_cells):
    filtered_table = []
    highlighted_cols = {col for col, row in highlighted_cells}
    highlighted_rows = {row for col, row in highlighted_cells}

    for cell in table:
        col = cell['col']
        row = cell['row']
        is_replicated = cell.get('is_replicated', 0)

        if (
            (col, row) in highlighted_cells or  # Condition 1
            (col in highlighted_cols and row == 0) or  # Condition 2
            (row in highlighted_rows and col == 0) or  # Condition 3
            (col in highlighted_cols and is_replicated == 1) or  # Condition 4
            (row in highlighted_rows and is_replicated == 1)  # Condition 5
        ):
            # Remove 'is_replicated' key from each cell before appending
            cell.pop('is_replicated', None)
            filtered_table.append(cell)

    return filtered_table

def process_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            record = json.loads(line)
            metadata = record.get('input', {}).get('metadata', {})
            table = record.get('input', {}).get('table', [])
            highlighted_cells = metadata.get('highlighted_cells', [])
            
            # Convert highlighted_cells list of lists to a list of tuples
            highlighted_cells = [tuple(cell) for cell in highlighted_cells]

            if table:
                record['input']['table'] = filter_table(table, highlighted_cells)
            
            
            metadata.pop('url', None)
            metadata.pop('publisher', None)
            metadata.pop('date', None)
            
            json.dump(record, outfile, ensure_ascii=False)
            outfile.write('\n')

# 입력 파일 경로와 출력 파일 경로
input_file = '240829_1_replicate_colrowspan.jsonl'
output_file = '240829_2_remove_redundancy_with_title.jsonl'

# JSONL 파일 처리
process_jsonl(input_file, output_file)