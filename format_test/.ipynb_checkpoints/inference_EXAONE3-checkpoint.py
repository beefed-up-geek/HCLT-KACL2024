# +
# # !pip install transformers==4.41.0 
# # !pip install huggingface_hub
# -

import os
os.environ['HF_HOME'] = '~/temp/.cache'
# os.environ['HF_HUB_CACHE'] = '~/temp/.cache'

import transformers
print(transformers.__version__)

import os
import json
from multiprocessing import Pool, set_start_method
from tqdm import tqdm
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login

login("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")
model = AutoModelForCausalLM.from_pretrained(
    "LGAI-EXAONE/EXAONE-3.0-7.8B-Instruct",
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("LGAI-EXAONE/EXAONE-3.0-7.8B-Instruct")

# +
# prompt="""다음 표의 highlighted_cell을 한 문장으로 요약해주세요. 표와 메타정보 : 
# {'input': {'metadata': {'title': '4차 산업혁명에 따른 조세환경 변화와 정책 과제',
#    'table_title': '영국의 우회이익세(DPT) 과세실적',
#    'date': '2020-06-09',
#    'publisher': '국회예산정책처',
#    'highlighted_cells': [[0, 3], [1, 3], [3, 3]]},
#   'table_xml': '<table><row><value /><is_header>True</is_header><col>0</col><colspan>1</colspan><row>0</row><rowspan>1</rowspan></row><row><value>2015/16</value><is_header>True</is_header><col>1</col><colspan>1</colspan><row>0</row><rowspan>1</rowspan></row><row><value>2016/17</value><is_header>True</is_header><col>2</col><colspan>1</colspan><row>0</row><rowspan>1</rowspan></row><row><value>2017/18</value><is_header>True</is_header><col>3</col><colspan>1</colspan><row>0</row><rowspan>1</rowspan></row><row><value>해외이전소득신고건수(건)1)</value><is_header>False</is_header><col>0</col><colspan>1</colspan><row>1</row><rowspan>1</rowspan></row><row><value>48</value><is_header>False</is_header><col>1</col><colspan>1</colspan><row>1</row><rowspan>1</rowspan></row><row><value>145</value><is_header>False</is_header><col>2</col><colspan>1</colspan><row>1</row><rowspan>1</rowspan></row><row><value>220</value><is_header>False</is_header><col>3</col><colspan>1</colspan><row>1</row><rowspan>1</rowspan></row><row><value>당초예상세수(백만파운드)</value><is_header>False</is_header><col>0</col><colspan>1</colspan><row>2</row><rowspan>1</rowspan></row><row><value>25</value><is_header>False</is_header><col>1</col><colspan>1</colspan><row>2</row><rowspan>1</rowspan></row><row><value>270</value><is_header>False</is_header><col>2</col><colspan>1</colspan><row>2</row><rowspan>1</rowspan></row><row><value>360</value><is_header>False</is_header><col>3</col><colspan>1</colspan><row>2</row><rowspan>1</rowspan></row><row><value>총세수(백만파운드)2)</value><is_header>False</is_header><col>0</col><colspan>1</colspan><row>3</row><rowspan>1</rowspan></row><row><value>31</value><is_header>False</is_header><col>1</col><colspan>1</colspan><row>3</row><rowspan>1</rowspan></row><row><value>281</value><is_header>False</is_header><col>2</col><colspan>1</colspan><row>3</row><rowspan>1</rowspan></row><row><value>388</value><is_header>False</is_header><col>3</col><colspan>1</colspan><row>3</row><rowspan>1</rowspan></row></table>'}"""

# messages = [
#     {"role": "system", 
#      "content": "You are EXAONE model from LG AI Research, a helpful assistant."},
#     {"role": "user", "content": prompt}
# ]

# input_ids = tokenizer.apply_chat_template(
#     messages,
#     tokenize=True,
#     add_generation_prompt=True,
#     return_tensors="pt"
# )

# output = model.generate(
#     input_ids.to("cuda"),
#     eos_token_id=tokenizer.eos_token_id,
#     max_new_tokens=512
# )
# print(tokenizer.decode(output[0]))

# -
# # 데이터셋


# +
import os
import json

# 현재 폴더의 모든 파일 중 .jsonl 파일을 찾기
current_folder = os.getcwd()  # 현재 작업 디렉토리 경로 가져오기
jsonl_files = [f for f in os.listdir(current_folder) if f.endswith('.jsonl')]

# 각 파일의 내용을 저장할 딕셔너리
all_jsonl_data = {}

# 각 JSONL 파일 읽기
for file_name in jsonl_files:
    file_path = os.path.join(current_folder, file_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        jsonl_data = [json.loads(line) for line in file]
        all_jsonl_data[file_name] = jsonl_data


# +
# all_jsonl_data.keys()

# +
# all_jsonl_data['trans_xml.jsonl'][0]
# -

def inference(data):
    messages = [
        {"role": "system", 
         "content": "당신은 표 요약 봇입니다."},
        {"role": "user", "content": f"다음 표의 highlighted_cell을 한 문장으로 요약해주세요. 표와 메타정보 : {str(data['input'])}"}
    ]

    input_ids = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt"
    )

    output = model.generate(
        input_ids.to("cuda"),
        eos_token_id=tokenizer.eos_token_id,
        max_new_tokens=1024
    )
    
    text = tokenizer.decode(output[0])
    del input_ids
    return text


all_jsonl_data.keys()

# +
from tqdm import tqdm
import json

inferences = {}

json_file = 'trans_xml.jsonl'

inferences[json_file] = []
# tqdm 적용
for data in tqdm(all_jsonl_data[json_file], desc=f"Processing {json_file}"):
    inferences[json_file].append(inference(data))

# 결과를 각각의 파일로 저장
output_file = f"{json_file}_inference2.jsonl"
with open(output_file, 'w') as f:
    for item in inferences[json_file]:
        f.write(json.dumps(item) + '\n')

# -
# # --


# +
# import json
# file_path = 'trans_mkdw2.jsonl_inference.jsonl'

# with open(file_path, 'r', encoding='utf-8') as file:
#     jsonl_data = [json.loads(line) for line in file]

# +
# print(jsonl_data[0])
