import json
import xml.etree.ElementTree as ET

def convert_table_to_xml(table_data):
    root = ET.Element("table")
    
    for row in table_data:
        row_elem = ET.SubElement(root, "row")
        for key, value in row.items():
            cell_elem = ET.SubElement(row_elem, key)
            cell_elem.text = str(value)
    
    return ET.tostring(root, encoding='unicode')

def process_jsonl_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            data = json.loads(line)
            
            # Convert the table data to XML format
            table_data = data.get("input", {}).get("table", [])
            xml_table = convert_table_to_xml(table_data)
            
            # Update the data with the XML formatted table
            data["input"]["table_xml"] = xml_table
            
            # Remove the original table data
            if "table" in data["input"]:
                del data["input"]["table"]
            
            # Ensure the url data is removed
            if "metadata" in data["input"] and "url" in data["input"]["metadata"]:
                del data["input"]["metadata"]["url"]
            
            # Remove the id data
            if "id" in data:
                del data["id"]
            
            # Keep only the first element of the output list
            if isinstance(data.get("output"), list) and len(data["output"]) > 0:
                data["output"] = data["output"][0]
            
            # Write the modified data back to the output file
            outfile.write(json.dumps(data, ensure_ascii=False) + '\n')

input_file = 'nikluge-gtps-2023-test.jsonl'
output_file = 'test_full.jsonl'

# Process the file
process_jsonl_file(input_file, output_file)

print(f"Conversion completed. XML data saved in {output_file}")
