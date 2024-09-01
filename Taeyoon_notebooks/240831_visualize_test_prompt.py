import json
import os
from pathlib import Path

# Create the visualized directory if it doesn't exist
output_dir = Path("visualized")
output_dir.mkdir(exist_ok=True)

# Function to create HTML table with highlighted cells
def create_html_table(table_data, highlighted_cells):
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
                
                # Check if this cell should be highlighted
                if [col_index, row_index] in highlighted_cells:
                    cell_html = f'    <td colspan="{colspan}" rowspan="{rowspan}" style="background-color: yellow;">{value}</td>\n'
                else:
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
input_file = '240831_sorted_output_file.jsonl'
with open(input_file, 'r', encoding='utf-8') as f:
    for index, line in enumerate(f):
        entry = json.loads(line)
        table_data = entry['input']['table']
        highlighted_cells = entry['input']['metadata']['highlighted_cells']
        outputs = entry['output']
        analysis = entry['analysis']

        # Generate HTML content
        html_content = f"<html>\n<head><title>{index}</title></head>\n<body>\n"
        html_content += f"<h1>{entry['input']['metadata']['title']}</h1>\n"
        html_content += f"<h2>{entry['input']['metadata']['table_title']}</h2>\n"
        html_content += f"<h3>ID: {entry['id']}</h3>\n"
        html_content += create_html_table(table_data, highlighted_cells)

        # Add highlighted_cells info below the table
        html_content += "<div>\n"
        html_content += f"<p><strong>Highlighted Cells:</strong> {highlighted_cells}</p>\n"
        html_content += "</div>\n"

        # Add analysis scores table below the highlighted cells info
        html_content += "<div>\n"
        html_content += "<h2>분석 점수</h2>\n"
        html_content += "<table border='1' cellpadding='5' cellspacing='0'>\n"
        for key, value in analysis.items():
            if key != 'ai_output' and key != 'best_output':
                html_content += f"<tr><td><strong>{key}</strong></td><td>{value:.3f}</td></tr>\n"
        html_content += "</table>\n"
        html_content += "</div>\n"

        # Add AI output below the scores table
        html_content += "<div>\n"
        html_content += f"<h2>인공지능 대답:</h2>\n<p>{analysis['ai_output']}</p>\n"
        html_content += "</div>\n"
        
        # Add output values below the AI output
        html_content += "<div>\n"
        html_content += "<h2>정답들</h2>\n"
        for idx, output in enumerate(outputs, 1):
            html_content += f"<p>{idx}. {output}</p>\n"
        html_content += "</div>\n"
        
        html_content += "\n</body>\n</html>"

        # Write to an HTML file with the index as the file name
        output_file = output_dir / f"{index}.html"
        with open(output_file, 'w', encoding='utf-8') as output_f:
            output_f.write(html_content)

print(f"HTML files have been saved in the '{output_dir}' directory.")
