import json

# Function to extract titles from a JSONL file
def extract_titles(jsonl_file):
    titles = set()
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            titles.add(data['input']['metadata']['title'])
    return titles

# Load titles from the first and second JSONL files
titles_first_file = extract_titles('nikluge-gtps-2023-train.jsonl')
titles_second_file = extract_titles('nikluge-gtps-2023-test.jsonl')

# Find titles in the second file that are not in the first file
unique_titles = titles_second_file - titles_first_file

# Output the result
if unique_titles:
    print("Titles in the second file that are not in the first file:")
    for title in unique_titles:
        print(title)
else:
    print("All titles in the second file are present in the first file.")
