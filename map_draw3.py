import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import heapq
import math

plt.style.use('default')

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


class AStar:
    def __init__(self, grid_data):
        self.data = grid_data
        self.max_x = grid_data['x'].max()
        self.max_y = grid_data['y'].max()

        construction_sites = grid_data[grid_data['ConstructionSite'] == 1]
        self.blocked = set(zip(construction_sites['x'], construction_sites['y']))

    def heuristic(self, a, b):
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx <= self.max_x and 1 <= ny <= self.max_y:
                if (nx, ny) not in self.blocked:
                    neighbors.append((nx, ny))

        return neighbors

    def find_path(self, start, goal):
        """A* 알고리즘으로 최단 경로 찾기"""

        # 우선순위 큐: (f_score, g_score, position, path)
        open_set = [(0, 0, start, [start])]

        # 방문한 노드와 최소 비용 저장
        visited = {}

        while open_set:
            f_score, g_score, current, path = heapq.heappop(open_set)

            # 이미 더 좋은 경로로 방문한 경우 스킵
            if current in visited and visited[current] <= g_score:
                continue

            visited[current] = g_score

            # 목표 도달
            if current == goal:
                return path

            # 이웃 노드 탐색
            for neighbor in self.get_neighbors(current):
                new_g_score = g_score + 1

                # 이미 더 좋은 경로로 방문한 경우 스킵
                if neighbor in visited and visited[neighbor] <= new_g_score:
                    continue

                h_score = self.heuristic(neighbor, goal)
                new_f_score = new_g_score + h_score
                new_path = path + [neighbor]

                heapq.heappush(open_set, (new_f_score, new_g_score, neighbor, new_path))

        return None



def prepare_data():
    area_category_df = pd.read_csv('area_category.csv')
    area_map_df = pd.read_csv('area_map.csv')
    area_struct_df = pd.read_csv('area_struct.csv')

    area_category_df.columns = area_category_df.columns.str.strip()
    area_category_df['struct'] = area_category_df['struct'].str.strip()

    merged_df = pd.merge(area_map_df, area_struct_df, on=['x', 'y'])
    final_df = pd.merge(merged_df, area_category_df, on='category', how='left')

    return final_df


def find_key_locations(data):
    locations = {}

    # 내 집 (category = 3)
    my_home = data[data['category'] == 3]
    if not my_home.empty:
        locations['home'] = (int(my_home.iloc[0]['x']), int(my_home.iloc[0]['y']))

    # 반달곰 커피 (category = 4)
    coffee_shops = data[data['category'] == 4]
    locations['cafes'] = [(int(row['x']), int(row['y'])) for _, row in coffee_shops.iterrows()]

    # 아파트 (category = 1)
    apartments = data[data['category'] == 1]
    locations['apartments'] = [(int(row['x']), int(row['y'])) for _, row in apartments.iterrows()]

    # 빌딩 (category = 2)
    buildings = data[data['category'] == 2]
    locations['buildings'] = [(int(row['x']), int(row['y'])) for _, row in buildings.iterrows()]

    return locations


def save_path_to_csv(path, filename):
    if path:
        path_df = pd.DataFrame(path, columns=['x', 'y'])
        path_df.to_csv(filename, index=False)
        print(f"경로가 '{filename}' 파일로 저장되었습니다. (총 {len(path)}개 지점)")
    else:
        print(f"저장할 경로가 없습니다.")


def visualize_map(data, path=None, bonus_path=None):
    fig, ax = plt.subplots(figsize=(14, 14))
    max_x = data['x'].max()
    max_y = data['y'].max()

    ax.set_xlim(0.5, max_x + 0.5)
    ax.set_ylim(0.5, max_y + 0.5)
    ax.set_xticks(range(1, max_x + 1))
    ax.set_yticks(range(1, max_y + 1))
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.invert_yaxis()
    ax.set_aspect('equal', adjustable='box')
    plt.title('최단 경로 지도', fontsize=16)

    # 빈 공간
    empty_spaces = data[(data['category'] == 0) & (data['ConstructionSite'] == 0)]
    if len(empty_spaces) > 0:
        ax.scatter(empty_spaces['x'], empty_spaces['y'],
                   marker='.', color='lightgray', s=30,
                   label='빈 공간', zorder=1, alpha=0.5)

    # 건설 현장
    construction_sites = data[data['ConstructionSite'] == 1]
    if len(construction_sites) > 0:
        ax.scatter(construction_sites['x'], construction_sites['y'],
                   marker='X', color='orange', s=80,
                   label='건설 현장', zorder=2, alpha=0.7)

    # 아파트
    apartments = data[data['category'] == 1]
    if len(apartments) > 0:
        ax.scatter(apartments['x'], apartments['y'],
                   marker='o', color='saddlebrown', s=100,
                   label='아파트', zorder=3, alpha=0.9)

    # 빌딩
    buildings = data[data['category'] == 2]
    if len(buildings) > 0:
        ax.scatter(buildings['x'], buildings['y'],
                   marker='s', color='darkblue', s=100,
                   label='빌딩', zorder=3, alpha=0.9)

    # 반달곰 커피
    coffee_shops = data[data['category'] == 4]
    if len(coffee_shops) > 0:
        ax.scatter(coffee_shops['x'], coffee_shops['y'],
                   marker='s', color='green', s=120,
                   label='반달곰 커피', zorder=3, alpha=0.9)

    # 내 집
    my_home = data[data['category'] == 3]
    if len(my_home) > 0:
        ax.scatter(my_home['x'], my_home['y'],
                   marker='^', color='red', s=150,
                   label='내 집', zorder=4, alpha=1.0)

    # 기본 최단 경로 (집 → 가장 가까운 커피숍)
    if path:
        path_x = [p[0] for p in path]
        path_y = [p[1] for p in path]
        ax.plot(path_x, path_y, 'r-', linewidth=3,
                label=f'최단경로 (거리: {len(path) - 1})', zorder=5, alpha=0.8)


    ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1.02))

    try:
        plt.savefig('map_final.png', dpi=300, bbox_inches='tight')
        print("지도가 'map_final.png'로 저장되었습니다.")
    except Exception as e:
        print(f"이미지 저장 실패: {e}")

    try:
        plt.show()
    except Exception as e:
        print(f"이미지 표시 실패: {e}")
        print("GUI 환경이 아니거나 디스플레이에 문제가 있을 수 있습니다.")


def main():
    print("=== 지도 데이터 분석 및 최단경로 계산 ===")

    data = prepare_data()
    locations = find_key_locations(data)

    print(f"내 집: {locations.get('home')}")
    print(f"반달곰 커피: {locations['cafes']}")
    print(f"아파트: {locations['apartments']}")
    print(f"빌딩: {locations['buildings']}")

    astar = AStar(data)

    home = locations['home']
    cafes = locations['cafes']

    shortest_path = None
    if home and cafes:
        # 가장 가까운 커피숍 찾기
        shortest_distance = float('inf')
        target_cafe = None

        for cafe in cafes:
            path = astar.find_path(home, cafe)
            if path and len(path) - 1 < shortest_distance:
                shortest_distance = len(path) - 1
                shortest_path = path
                target_cafe = cafe

        if shortest_path:
            print(f"\n=== 최단 경로 (집 → 커피숍) ===")
            print(f"시작점: {home}")
            print(f"도착점: {target_cafe}")
            print(f"경로 거리: {len(shortest_path) - 1}")

            # 4. CSV 저장
            save_path_to_csv(shortest_path, 'home_to_cafe.csv')
        else:
            print("집에서 커피숍까지의 경로를 찾을 수 없습니다.")

    print(f"\n=== 지도 시각화 ===")
    try:
        visualize_map(data, shortest_path)
    except Exception as e:
        print(f"시각화 오류: {e}")
        print("CSV 파일은 정상적으로 저장되었습니다.")

    print("\n=== 완료 ===")
    print("생성된 파일:")
    if shortest_path:
        print("- 최단경로: home_to_cafe.csv")



if __name__ == "__main__":
    main()