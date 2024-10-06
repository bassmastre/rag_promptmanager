import json
import csv
import os

# 1. diagnosisData_filtered.csv 파일에서 중국어-영어 매핑 데이터를 읽어 딕셔너리로 변환
mapping_dict = {}
with open('diagnoseData_filtered.csv', 'r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        zh_term = row['zh'].strip()  # 중국어 명칭
        eng_term = row['eng'].strip()  # 영어 명칭
        mapping_dict[zh_term] = eng_term

# 2. 텍스트에서 중국어 단어를 영어로 대체하는 함수
def replace_chinese_with_english(text, mapping_dict):
    for zh_term, eng_term in mapping_dict.items():
        if zh_term in text:
            text = text.replace(zh_term, eng_term)
    return text

# 3. JSON 데이터에서 문자열을 탐색하고, 중국어를 영어로 대체하는 함수
def replace_in_json(data, mapping_dict):
    if isinstance(data, dict):
        return {key: replace_in_json(value, mapping_dict) for key, value in data.items()}
    elif isinstance(data, list):
        return [replace_in_json(item, mapping_dict) for item in data]
    elif isinstance(data, str):
        return replace_chinese_with_english(data, mapping_dict)  # 문자열인 경우만 번역
    else:
        return data  # 다른 형식은 그대로 반환

# 4. 여러 JSON 파일 처리
for i in range(2, 11):  # file_part_2.json부터 file_part_10.json까지 처리
    input_file = f'file_part_{i}.json'
    output_file = f'translated_file_part_{i}.json'

    # 파일이 존재하는지 확인
    if os.path.exists(input_file):
        # JSON 파일 불러오기
        with open(input_file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # JSON 데이터에서 중국어를 영어로 대체
        translated_data = replace_in_json(data, mapping_dict)

        # 변환된 데이터를 새로운 JSON 파일로 저장
        with open(output_file, 'w', encoding='utf-8') as json_file:
            json.dump(translated_data, json_file, ensure_ascii=False, indent=4)

        print(f"중국어 단어가 영어로 대체된 파일이 {output_file}에 저장되었습니다.")
    else:
        print(f"파일 {input_file}이 존재하지 않습니다.")
