import pandas as pd
import matplotlib.pyplot as plt

# 1. 데이터 로드
area_map = pd.read_csv('area_map.csv')
area_struct = pd.read_csv('area_struct.csv')
area_category = pd.read_csv('area_category.csv')

# 2. 컬럼명 정리 및 변환
area_category.columns = ['Struct_id', 'Struct_nm']
area_struct.rename(columns={'area': 'Area_id', 'category': 'Struct_id'}, inplace=True)
area_map.rename(columns={'area': 'Area_id'}, inplace=True)

# 3. 구조물 ID를 이름으로 변환
struct_id_to_name = pd.Series(area_category.Struct_nm.values, index=area_category.Struct_id).to_dict()
area_struct['Struct_nm'] = area_struct['Struct_id'].map(struct_id_to_name)

# 4. 데이터 병합
merged_df = pd.merge(area_map, area_struct, on='Area_id')

# 5. 'Area_id' 기준으로 정렬
merged_df = merged_df.sort_values(by='Area_id')

# 6. area 1 데이터 필터링
area_1_df = merged_df[merged_df['Area_id'] == 1].copy()

# 7. 시각화
plt.figure(figsize=(10, 10))
plt.grid(True)

# 범례 중복을 피하기 위해 이미 추가된 라벨을 추적합니다.
handles, labels = plt.gca().get_legend_handles_labels()
for _, row in area_1_df.iterrows():
    x, y, struct_name = row['x'], row['y'], row['Struct_nm']
    if struct_name in ['아파트', '빌딩']:
        if '아파트/빌딩' not in labels:
            plt.scatter(x, y, c='brown', marker='o', s=100, label='아파트/빌딩')
            handles, labels = plt.gca().get_legend_handles_labels()
        else:
            plt.scatter(x, y, c='brown', marker='o', s=100)
    elif struct_name == '반달곰 커피':
        if '반달곰 커피' not in labels:
            plt.scatter(x, y, c='green', marker='s', s=100, label='반달곰 커피')
            handles, labels = plt.gca().get_legend_handles_labels()
        else:
            plt.scatter(x, y, c='green', marker='s', s=100)
    elif struct_name == '내 집':
        if '내 집' not in labels:
            plt.scatter(x, y, c='green', marker='^', s=100, label='내 집')
            handles, labels = plt.gca().get_legend_handles_labels()
        else:
            plt.scatter(x, y, c='green', marker='^', s=100)
    elif struct_name == '건설 현장':
        if '건설 현장' not in labels:
            plt.scatter(x, y, c='gray', marker='s', s=200, label='건설 현장')
            handles, labels = plt.gca().get_legend_handles_labels()
        else:
            plt.scatter(x, y, c='gray', marker='s', s=200)

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Area 1 Map')
plt.legend()
plt.axis('equal')
plt.gca().invert_yaxis()
plt.savefig('map.png')
