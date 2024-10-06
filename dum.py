#%%
import json

target_file = 'file_part_1.json'
output_file = 'onlydoc.json'

# 파일 읽기
with open(target_file, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Doctor 항목만 남기고 필터링하는 함수
def filter_doctor_entries(nested_list):
    filtered_data = []
    for session in nested_list:
        # 'id'가 'Doctor'인 항목만 필터링
        filtered_session = [entry for entry in session if entry.get('id') == 'Doctor']
        if filtered_session:
            filtered_data.append(filtered_session)
    return filtered_data

# 필터링 수행
filtered_data = filter_doctor_entries(data)

for session in filtered_data:
    for i, entry in enumerate(session):
        entry['index'] = i

# 세션을 세는 함수
def count_sessions(nested_list):
    return len(nested_list)

# 필터링된 세션 개수 계산
session_count = count_sessions(filtered_data)
print("Session Count:", session_count)

# 필터링된 데이터를 새로운 파일에 저장
with open(output_file, 'w', encoding='utf-8') as json_out:
    json.dump(filtered_data, json_out, ensure_ascii=False, indent=4)


# %%
import json

# 'onlydoc.json' 파일을 불러오기
input_file = 'onlydoc.json'
output_file = 'traindata_5.json'


with open(input_file, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Disease 값이 있는 항목까지의 인덱스에서 Sentence를 저장하고 Class:1을 부여하는 함수
def store_sentences_with_class(session):
    sentences = []
    for entry in session:
        sentences.append(entry['Sentence'])
        if entry['Disease']:  # Disease 값이 있는 경우
            sentence_combined=' '.join(sentences)
            return {'Sentences': sentence_combined, 'Class': 1}
    return None  # Disease 값이 없는 경우

# 모든 세션에 대해 같은 작업을 수행, Disease 값이 있는 세션만 저장
all_stored_sentences = [store_sentences_with_class(session) for session in data if store_sentences_with_class(session)]

# 'onlydoc_classified.json' 파일로 저장

with open(output_file, 'w', encoding='utf-8') as json_out:
    json.dump(all_stored_sentences, json_out, ensure_ascii=False, indent=4)
# %%


import json

# 'onlydoc.json' 파일을 불러오기
input_file = 'onlydoc.json'
output_file = 'traindata_10.json'

with open(input_file, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Disease 값이 있는 항목까지의 인덱스에서 그 직전까지 Sentence를 저장하고 Class:0을 부여하는 함수
def store_sentences_with_class(session):
    sentences = []
    for entry in session:
        if entry['Disease']:  # Disease 값이 있는 경우
            sentence_combined = ' '.join(sentences)  # Disease 값이 있기 직전까지의 문장 결합
            return {'Sentences': sentence_combined, 'Class': 0}
        sentences.append(entry['Sentence'])
    return None  # Disease 값이 없는 경우

# 모든 세션에 대해 같은 작업을 수행, Disease 값이 있는 세션만 저장
all_stored_sentences = [store_sentences_with_class(session) for session in data if store_sentences_with_class(session)]

# 결과를 출력 파일로 저장
with open(output_file, 'w', encoding='utf-8') as json_out:
    json.dump(all_stored_sentences, json_out, ensure_ascii=False, indent=4)
# %%
import json

# 파일들을 처리하는 함수
def merge_files(file_list, output_file):
    all_data = []

    # 각 파일에 대해 처리
    for target_file in file_list:
        # 파일 읽기
        with open(target_file, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            all_data.extend(data)

    # 모든 데이터를 하나의 파일에 저장
    with open(output_file, 'w', encoding='utf-8') as json_out:
        json.dump(all_data, json_out, ensure_ascii=False, indent=4)

# 처리할 파일 목록과 출력 파일
file_list = ['traindata_3.json', 'traindata_8.json', 'traindata_4.json', 'traindata_9.json', 'traindata_5.json', 'traindata_10.json']
output_file = 'train_set2.json'

# 파일 처리 실행
merge_files(file_list, output_file)

# %%
import json
import matplotlib.pyplot as plt

# 'onlydoc.json' 파일을 불러오기
input_file = 'onlydoc.json'

with open(input_file, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Disease 값이 있는 항목의 인덱스 번호를 저장하는 함수
# Disease 값이 없는 경우 index 번호 0으로 저장
def get_disease_indices(nested_list):
    indices = []
    for session_index, session in enumerate(nested_list):
        has_disease = False
        for entry in session:
            if entry['Disease']:  # Disease 값이 있는 경우
                indices.append(session_index)
                has_disease = True
                break
        if not has_disease:  # Disease 값이 없는 경우
            indices.append(0)
    return indices

# Disease 값이 있는 세션의 인덱스 번호 얻기
disease_indices = get_disease_indices(data)

# 인덱스 번호와 해당 번호의 빈도수를 계산
max_index = max(disease_indices)  # 최대 인덱스 값
index_counts = [disease_indices.count(i) for i in range(max_index + 1)]  # 각 인덱스의 빈도수를 리스트로 저장

# x축: 인덱스 번호, y축: 빈도수를 꺾은선 그래프로 시각화
plt.plot(range(max_index + 1), index_counts, marker='o', linestyle='-', color='b')
plt.title('Frequency of Index Numbers with Disease')
plt.xlabel('Index Number')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# %%
max_index = max([max([entry['index'] for entry in session]) for session in data])
max_index