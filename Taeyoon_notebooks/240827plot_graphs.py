import json
import matplotlib.pyplot as plt
from matplotlib.table import Table
from matplotlib.font_manager import FontProperties
import os

# Set up the font properties
font_path = 'malgun.ttf'  # Ensure this path is correct
font_prop = FontProperties(fname=font_path, size=10)  # Adjust font size here

def draw_table_with_highlights(table_data, highlighted_cells, output_file):
    fig, ax = plt.subplots(figsize=(8, 6))  # Adjust figure size as needed
    ax.set_axis_off()
    
    # Create table
    tbl = Table(ax, bbox=[0, 0, 1, 1])

    nrows = max([cell['row'] for cell in table_data]) + 1
    ncols = max([cell['col'] for cell in table_data]) + 1

    # Add cells to the table
    for cell in table_data:
        color = 'yellow' if [cell['col'], cell['row']] in highlighted_cells else 'white'
        tbl.add_cell(cell['row'], cell['col'], width=1/ncols, height=1/nrows, 
                     text=cell['value'], loc='center', facecolor=color, 
                     fontproperties=font_prop)

    # Row and Column Labels
    for row in range(nrows):
        tbl.add_cell(row, -1, width=1/ncols, height=1/nrows, text=str(row), loc='right', 
                     edgecolor='none', fontproperties=font_prop)
    
    for col in range(ncols):
        tbl.add_cell(-1, col, width=1/ncols, height=1/nrows, text=str(col), loc='center', 
                     edgecolor='none', fontproperties=font_prop)

    ax.add_table(tbl)
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()

def process_jsonl_file(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(input_file, 'r', encoding='utf-8') as infile:
        for index, line in enumerate(infile):
            data = json.loads(line)
            
            # Extract table data and highlighted cells
            table_data = data.get("input", {}).get("table", [])
            highlighted_cells = data.get("input", {}).get("metadata", {}).get("highlighted_cells", [])
            
            # Prepare output file name
            output_file = os.path.join(output_dir, f'{index}.png')
            
            # Draw table with highlighted cells
            draw_table_with_highlights(table_data, highlighted_cells, output_file)

input_file = 'nikluge-gtps-2023-train.jsonl'
output_dir = 'graphs_visualized'

# Process the file
process_jsonl_file(input_file, output_dir)

print(f"Processing completed. Images saved in {output_dir}")
