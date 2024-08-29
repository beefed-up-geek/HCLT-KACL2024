import json
import os
from pathlib import Path

# Create the visualized directory if it doesn't exist
output_dir = Path("visualized")
output_dir.mkdir(exist_ok=True)

# Function to create HTML table
def create_html_table(table_data):
    table_html = '<table border="1" cellpadding="5" cellspacing="0">\n'
    max_col = max(cell['col'] + cell.get('colspan', 1) - 1 for cell in table_data)
    max_row = max(cell['row'] + cell.get('rowspan', 1) - 1 for cell in table_data)
    
    for row_index in range(max_row + 1):
        row_html = "  <tr>\n"
        for col_index in range(max_col + 1):
            # Find the cell data for this position
            cell_data = next((cell for cell in table_data if cell['row'] == row_index and cell['col'] == col_index), None)
            if cell_data:
                colspan = cell_data.get('colspan', 1)
                rowspan = cell_data.get('rowspan', 1)
                value = cell_data['value']
                
                cell_html = f'    <td colspan="{colspan}" rowspan="{rowspan}">{value}</td>\n'
                row_html += cell_html
                
                # Skip over columns occupied by colspan
                for _ in range(1, colspan):
                    col_index += 1
        row_html += "  </tr>\n"
        table_html += row_html
    table_html += "</table>\n"
    return table_html

# Read the .jsonl file
input_file = 'nikluge-gtps-2023-train.jsonl'
with open(input_file, 'r', encoding='utf-8') as f:
    for line in f:
        entry = json.loads(line)
        entry_id = entry['id']
        table_data = entry['input']['table']
        highlighted_cells = entry['input']['metadata']['highlighted_cells']
        outputs = entry['output']

        # Generate HTML content
        html_content = f"<html>\n<head><title>{entry_id}</title></head>\n<body>\n"
        html_content += f"<h1>{entry['input']['metadata']['title']}</h1>\n"
        html_content += create_html_table(table_data)

        # Add highlighted_cells info below the table
        html_content += "<div>\n"
        html_content += f"<p><strong>Highlighted Cells:</strong> {highlighted_cells}</p>\n"
        html_content += "</div>\n"

        # Add output values below the table under "정답들"
        html_content += "<div>\n"
        html_content += "<h2>정답들</h2>\n"
        for idx, output in enumerate(outputs, 1):
            html_content += f"<p>{idx}. {output}</p>\n"
        html_content += "</div>\n"
        
        html_content += "\n</body>\n</html>"

        # Write to an HTML file
        output_file = output_dir / f"{entry_id}.html"
        with open(output_file, 'w', encoding='utf-8') as output_f:
            output_f.write(html_content)

print(f"HTML files have been saved in the '{output_dir}' directory.")
