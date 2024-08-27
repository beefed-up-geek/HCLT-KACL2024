import json
import xml.etree.ElementTree as ET

def filter_table_by_highlighted_cells(table, highlighted_cells):
    filtered_table = []
    for row, col in highlighted_cells:
        for cell in table:
            if (cell['row'] == col and cell['col'] == row) or \
               (cell['row'] == 0 and cell['col'] == row) or \
               (cell['row'] == col and cell['col'] == 0) or \
               (cell['row'] == col and cell.get('rowspan', 0) != 0) or \
               (cell['row'] == col and cell.get('colspan', 0) != 0) or \
               (cell['col'] == row and cell.get('colspan', 0) != 0) or \
               (cell['col'] == row and cell.get('rowspan', 0) != 0):
                filtered_table.append(cell)
    return filtered_table

def convert_table_to_xml(table_data):
    root = ET.Element("table")
    for cell in table_data:
        row_elem = ET.SubElement(root, "row")
        for key, value in cell.items():
            cell_elem = ET.SubElement(row_elem, key)
            cell_elem.text = str(value)
    return ET.tostring(root, encoding='unicode')

def process_jsonl_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            data = json.loads(line)
            
            # Filter table by highlighted cells
            table_data = data.get("input", {}).get("table", [])
            highlighted_cells = data.get("input", {}).get("metadata", {}).get("highlighted_cells", [])
            filtered_table = filter_table_by_highlighted_cells(table_data, highlighted_cells)
            
            # Convert the filtered table data to XML format
            xml_table = convert_table_to_xml(filtered_table)
            data["input"]["table_xml"] = xml_table
            
            # Remove the original table data, url, highlighted_cells, and id
            if "table" in data["input"]:
                del data["input"]["table"]
            if "url" in data["input"]["metadata"]:
                del data["input"]["metadata"]["url"]
            if "highlighted_cells" in data["input"]["metadata"]:
                del data["input"]["metadata"]["highlighted_cells"]
            if "id" in data:
                del data["id"]
            
            # Keep only the first element of the output list and convert to string
            if isinstance(data.get("output"), list) and len(data["output"]) > 0:
                data["output"] = data["output"][0]
            
            # Write the modified data back to the output file
            outfile.write(json.dumps(data, ensure_ascii=False) + '\n')

# Input and Output file paths
input_file = 'nikluge-gtps-2023-train.jsonl'
output_file = 'train_only_highlight_.jsonl'

# Process the file
process_jsonl_file(input_file, output_file)

print(f"Processing completed. Data saved in {output_file}")
