import pandas as pd

area_map = pd.read_csv('csvs/area_map.csv')
area_struct = pd.read_csv('csvs/area_struct.csv')
area_category = pd.read_csv('csvs/area_category.csv')

# 2. 컬럼명 정리 및 변환
# area_category의 컬럼명이 'category', ' struct' 임을 확인. ' struct'의 선행 공백에 유의.
# 컬럼명을 각각 'Struct_id', 'Struct_nm'으로 변경
area_category.columns = ['Struct_id', 'Struct_nm']

# area_struct의 'area' 컬럼명을 'Area_id'로 변경
area_struct.rename(columns={'area': 'Area_id', 'category': 'Struct_id'}, inplace=True)

# 3. 구조물 ID를 이름으로 변환
struct_id_to_name = pd.Series(area_category.Struct_nm.values, index=area_category.Struct_id).to_dict()
area_struct['Struct_nm'] = area_struct['Struct_id'].map(struct_id_to_name)


# 4. 데이터 병합
# 'Area_id'를 기준으로 area_map과 area_struct를 병합합니다.
# area_map에는 Area_id가 없으므로, area_struct 데이터프레임을 기반으로 합니다.
merged_df = area_struct

# 5. 'Area_id' 기준으로 정렬
merged_df = merged_df.sort_values(by='Area_id')


# 6. area 1 데이터 필터링
area_1_df = merged_df[merged_df['Area_id'] == 1].copy()

print("--- Area 1 데이터 ---")
print(area_1_df)


# (보너스) 구조물 종류별 요약 통계
struct_summary = area_1_df.groupby('Struct_nm').describe()

print("\n--- 구조물 종류별 요약 통계 (Area 1) ---")
print(struct_summary)
