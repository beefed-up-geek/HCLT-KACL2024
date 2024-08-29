import json

def expand_cells(table):
    expanded_table = []
    for cell in table:
        rowspan = cell.get('rowspan', 1)
        colspan = cell.get('colspan', 1)
        row = cell['row']
        col = cell['col']
        value = cell['value']
        
        # If a cell has rowspan or colspan > 1, we need to expand it
        if rowspan > 1 or colspan > 1:
            for r in range(rowspan):
                for c in range(colspan):
                    new_cell = {
                        'value': value,
                        'is_header': cell.get('is_header', False),
                        'col': col + c,
                        'colspan': 1,
                        'row': row + r,
                        'rowspan': 1,
                        'is_replicated': 1  # Mark this cell as replicated
                    }
                    expanded_table.append(new_cell)
            # Mark the original cell's replicated status as true
            cell['is_replicated'] = 0
        else:
            cell['is_replicated'] = 0
            expanded_table.append(cell)
    
    return expanded_table

def process_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            record = json.loads(line)
            table = record.get('input', {}).get('table', [])
            if table:
                record['input']['table'] = expand_cells(table)
            json.dump(record, outfile, ensure_ascii=False)
            outfile.write('\n')

# 입력 파일 경로와 출력 파일 경로
input_file = 'nikluge-gtps-2023-train.jsonl'
output_file = '240829_1_replicate_colrowspan.jsonl'

# JSONL 파일 처리
process_jsonl(input_file, output_file)

