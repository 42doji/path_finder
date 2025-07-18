import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 운영체제에 맞는 한글 폰트를 설정합니다.
# 폰트가 없는 경우 경고 메시지가 나타날 수 있으나, 실행에는 문제가 없습니다.
try:
    # Windows
    font_path = 'c:/Windows/Fonts/malgun.ttf'
    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rc('font', family=font_name)
except FileNotFoundError:
    try:
        # Mac / Linux
        font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
        font_name = fm.FontProperties(fname=font_path).get_name()
        plt.rc('font', family=font_name)
    except FileNotFoundError:
        print("경고: 맑은 고딕 또는 나눔고딕 폰트를 찾을 수 없습니다. 범례의 한글이 깨질 수 있습니다.")
        plt.rc('font', family='sans-serif')

# 1. 데이터 로드
area_map = pd.read_csv('area_map.csv')
area_struct = pd.read_csv('area_struct.csv')
area_category = pd.read_csv('area_category.csv')

# 2. 컬럼명 정리 및 변환
# area_category의 컬럼명에 숨어있는 공백을 제거합니다.
area_category.columns = [col.strip() for col in area_category.columns]
area_category.columns = ['Struct_id', 'Struct_nm']

# area_struct와 area_map의 'area' 컬럼명을 'Area_id'로 통일합니다.
# 이 부분이 가장 중요하며, 이전 오류의 원인이었습니다.
area_struct.rename(columns={'area': 'Area_id', 'category': 'Struct_id'}, inplace=True)
area_map.rename(columns={'area': 'Area_id'}, inplace=True)

# 3. 구조물 ID를 이름으로 변환
struct_id_to_name = pd.Series(area_category.Struct_nm.values, index=area_category.Struct_id).to_dict()
area_struct['Struct_nm'] = area_struct['Struct_id'].map(struct_id_to_name)


# --- ▼▼▼ 이 두 줄을 추가해주세요 ▼▼▼ ---
print("--- 디버깅 정보 ---")
print("area_map의 실제 컬럼명:", area_map.columns)
print("area_struct의 실제 컬럼명:", area_struct.columns)
print("--------------------")
# --- ▲▲▲ 여기까지 추가 ▲▲▲ ---
# 4. 데이터 병합 (Merge)
# 양쪽 DataFrame에 'Area_id'가 있으므로 정상적으로 병합됩니다.
merged_df = pd.merge(area_map, area_struct, on='Area_id')

# 5. 'Area_id' 기준으로 정렬
merged_df = merged_df.sort_values(by='Area_id')

# 6. area 1 데이터 필터링
area_1_df = merged_df[merged_df['Area_id'] == 1].copy()

# 7. 시각화
plt.figure(figsize=(10, 10))
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# 각 구조물 종류에 대한 핸들러를 저장하여 범례 중복을 방지합니다.
handles_labels = {}

# 건설 현장이 다른 구조물과 겹칠 때, 건설 현장이 아래에 그려지도록 zorder를 설정합니다.
for _, row in area_1_df.iterrows():
    x, y, struct_name = row['x'], row['y'], row['Struct_nm']
    
    if struct_name in ['아파트', '빌딩']:
        label, color, marker, size = '아파트/빌딩', 'saddlebrown', 'o', 100
        zorder = 5
    elif struct_name == '반달곰 커피':
        label, color, marker, size = '반달곰 커피', 'darkgreen', 's', 100
        zorder = 5
    elif struct_name == '내 집':
        label, color, marker, size = '내 집', 'blue', '^', 150
        zorder = 5
    elif struct_name == '건설 현장':
        label, color, marker, size = '건설 현장', 'gray', 's', 250
        zorder = 3 # 다른 마커들보다 아래에 위치
    else:
        continue

    # 범례에 라벨이 없으면 그리고, 핸들러 저장
    if label not in handles_labels:
        scatter = plt.scatter(x, y, c=color, marker=marker, s=size, label=label, zorder=zorder)
        handles_labels[label] = scatter
    else:
        plt.scatter(x, y, c=color, marker=marker, s=size, zorder=zorder)

# 축 설정
plt.xlabel('X 좌표')
plt.ylabel('Y 좌표')
plt.title('지역 1 지도 (Area 1 Map)')

# 범례를 그래프 바깥 오른쪽에 배치합니다.
plt.legend(handles=handles_labels.values(), labels=handles_labels.keys(), loc='upper left', bbox_to_anchor=(1, 1))

# 축 범위와 눈금을 설정하여 지도를 더 명확하게 만듭니다.
max_coord = max(area_1_df['x'].max(), area_1_df['y'].max()) + 2
plt.xticks(range(0, max_coord))
plt.yticks(range(0, max_coord))
plt.axis([0, max_coord, max_coord, 0]) # 좌측 상단이 (0,0) 근처가 되도록 설정
plt.gca().set_aspect('equal', adjustable='box')
plt.tight_layout(rect=[0, 0, 0.85, 1]) # 범례가 잘리지 않도록 레이아웃 조정

# 이미지 파일로 저장
plt.savefig('map.png', dpi=150)

print("성공적으로 'map.png' 파일을 생성했습니다.")


