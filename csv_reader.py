import pandas as pd

# 파일 경로 설정
directory = './csvs/'
main_file = 'area_struct.csv'
category_file = 'area_category.csv'

# CSV 파일 두 개를 각각 읽어오기
# strip() 함수는 ' struct' 처럼 이름 앞뒤의 공백을 제거해줘요.
df_main = pd.read_csv(directory + main_file)
df_category = pd.read_csv(directory + category_file)
df_category.columns = [col.strip() for col in df_category.columns]


# 1. 두 데이터를 'category' 기준으로 합치기 (merge)
# how='left'는 df_main의 모든 데이터를 유지해요.
merged_df = pd.merge(df_main, df_category, on='category', how='left')

# 2. 필요 없는 열은 지우고, 열 이름 바꾸기
merged_df = merged_df.drop('category', axis=1) # 숫자 category 열 삭제
merged_df = merged_df.rename(columns={'struct': 'category'}) # struct 열을 category로 이름 변경

# 3. 매칭되지 않은 데이터(NaN)를 'N/A'로 채우기
merged_df['category'] = merged_df['category'].fillna('N/A')

# 4. 최종 결과 확인하기
print(merged_df)
