import json
import xml.etree.ElementTree as ET

def table_to_xml(table):
    root = ET.Element("table")
    for cell in table:
        cell_element = ET.SubElement(root, "cell")
        for key, value in cell.items():
            if key != "is_replicated":  # Exclude 'is_replicated' if present
                child = ET.SubElement(cell_element, key)
                child.text = str(value)
    return ET.tostring(root, encoding="unicode")

def process_jsonl(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            record = json.loads(line)
            table = record.get('input', {}).get('table', [])

            if table:
                # Convert table to XML
                table_xml = table_to_xml(table)
                # Replace the original table with its XML representation
                record['input']['table'] = table_xml
            
            # Save the modified record back to the JSONL file
            json.dump(record, outfile, ensure_ascii=False)
            outfile.write('\n')

# 입력 파일 경로와 출력 파일 경로
input_file = '240829_2_remove_redundancy.jsonl'
output_file = '240829_3_to_xml.jsonl'

# JSONL 파일 처리
process_jsonl(input_file, output_file)
