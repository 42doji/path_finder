# mas_map.py

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

plt.style.use('default')

# 한글 폰트 설정
try:
    font_path = 'c:/Windows/Fonts/malgun.ttf'
    font_name = fm.FontProperties(fname=font_path, size=10).get_name()
    plt.rc('font', family=font_name)
except FileNotFoundError:
    try:
        font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'
        font_name = fm.FontProperties(fname=font_path, size=10).get_name()
        plt.rc('font', family=font_name)
    except FileNotFoundError:
        print("한글 폰트를 찾을 수 없어 기본 폰트를 사용합니다.")
        pass


def prepare_data():
    """데이터를 준비하는 함수"""
    area_category_df = pd.read_csv('area_category.csv')
    area_map_df = pd.read_csv('area_map.csv')
    area_struct_df = pd.read_csv('area_struct.csv')

    # 공백 제거
    area_category_df.columns = area_category_df.columns.str.strip()
    area_category_df['struct'] = area_category_df['struct'].str.strip()

    # 데이터 병합
    merged_df = pd.merge(area_map_df, area_struct_df, on=['x', 'y'])
    final_df = pd.merge(merged_df, area_category_df, on='category', how='left')

    return final_df


def draw_map_fixed(data):
    """처리된 데이터를 사용하여 지도를 시각화"""

    print("=== 데이터 분석 ===")
    print(f"전체 데이터 크기: {len(data)}")
    print(f"컬럼들: {list(data.columns)}")
    print("\n카테고리별 분포:")
    print(data['category'].value_counts().sort_index())
    print("\nstruct 값 분포:")
    print(data['struct'].value_counts(dropna=False))

    fig, ax = plt.subplots(figsize=(12, 12))
    max_x = data['x'].max()
    max_y = data['y'].max()

    ax.set_xlim(0.5, max_x + 0.5)
    ax.set_ylim(0.5, max_y + 0.5)
    ax.set_xticks(range(1, max_x + 1))
    ax.set_yticks(range(1, max_y + 1))
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.invert_yaxis()
    ax.set_aspect('equal', adjustable='box')
    plt.title('지역 지도 (색상 수정본)', fontsize=16)

    # 색상 매핑을 category 기반으로 직접 처리

    # 1. 아파트 (category = 1)
    apartments = data[data['category'] == 1]
    print(f"\n아파트 (category=1): {len(apartments)}개")
    if len(apartments) > 0:
        ax.scatter(apartments['x'], apartments['y'],
                   marker='o', color='saddlebrown', s=100,
                   label='아파트', zorder=3, alpha=0.9)

    # 2. 빌딩 (category = 2)
    buildings = data[data['category'] == 2]
    print(f"빌딩 (category=2): {len(buildings)}개")
    if len(buildings) > 0:
        ax.scatter(buildings['x'], buildings['y'],
                   marker='s', color='darkblue', s=100,
                   label='빌딩', zorder=3, alpha=0.9)

    # 3. 내 집 (category = 3)
    my_home = data[data['category'] == 3]
    print(f"내 집 (category=3): {len(my_home)}개")
    if len(my_home) > 0:
        ax.scatter(my_home['x'], my_home['y'],
                   marker='^', color='red', s=150,
                   label='내 집', zorder=4, alpha=1.0)

    # 4. 반달곰 커피 (category = 4)
    coffee_shops = data[data['category'] == 4]
    print(f"반달곰 커피 (category=4): {len(coffee_shops)}개")
    if len(coffee_shops) > 0:
        ax.scatter(coffee_shops['x'], coffee_shops['y'],
                   marker='s', color='green', s=120,
                   label='반달곰 커피', zorder=3, alpha=0.9)

    # 5. 건설 현장 (ConstructionSite = 1)
    construction_sites = data[data['ConstructionSite'] == 1]
    print(f"건설 현장 (ConstructionSite=1): {len(construction_sites)}개")
    if len(construction_sites) > 0:
        ax.scatter(construction_sites['x'], construction_sites['y'],
                   marker='X', color='orange', s=80,
                   label='건설 현장', zorder=2, alpha=0.7)

    # 6. 빈 공간 (category = 0, ConstructionSite = 0)
    empty_spaces = data[(data['category'] == 0) & (data['ConstructionSite'] == 0)]
    print(f"빈 공간: {len(empty_spaces)}개")
    if len(empty_spaces) > 0:
        ax.scatter(empty_spaces['x'], empty_spaces['y'],
                   marker='.', color='lightgray', s=30,
                   label='빈 공간', zorder=1, alpha=0.5)

    # 범례 추가
    ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1.02))

    # 파일로 저장
    plt.savefig('map_fixed.png', dpi=300, bbox_inches='tight')
    print("\n수정된 지도를 'map_fixed.png' 파일로 저장했습니다.")
    plt.show()


# 실행
if __name__ == "__main__":
    map_data = prepare_data()
    draw_map_fixed(map_data)