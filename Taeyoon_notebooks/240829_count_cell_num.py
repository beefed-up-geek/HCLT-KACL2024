import json
import matplotlib.pyplot as plt

# JSONL 파일 경로
input_file = '240829_2_remove_redundancy.jsonl'

# 셀 갯수 리스트
cell_counts = []

# 파일 읽기 및 셀 갯수 계산
with open(input_file, 'r', encoding='utf-8') as infile:
    for line_number, line in enumerate(infile, start=1):
        record = json.loads(line)
        table = record.get('input', {}).get('table', [])
        cell_count = len(table)
        
        # 50개 이상의 셀을 가진 표는 제외
        if cell_count < 50:
            cell_counts.append(cell_count)

# 셀 갯수의 분포를 시각화
plt.figure(figsize=(10, 6))
plt.hist(cell_counts, bins=range(min(cell_counts), max(cell_counts) + 1), color='skyblue', edgecolor='black')
plt.title('Distribution of Cell Counts in Tables (Excluding 50+ cells)')
plt.xlabel('Number of Cells in Table')
plt.ylabel('Frequency')
plt.grid(axis='y')

# 이미지 저장
plt.savefig('240829_cell_count_distribution_filtered.png')

# 시각화 완료 메시지
print("The distribution plot has been saved as 'cell_count_distribution_filtered.png'.")
