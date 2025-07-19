import pandas as pd

area_category_df = pd.read_csv('area_category.csv')
area_map_df = pd.read_csv('area_map.csv')
area_struct_df = pd.read_csv('area_struct.csv')
area_category_df.rename(columns={' struct': 'struct'}, inplace=True)

merged_map_struct_df = pd.merge(area_map_df, area_struct_df, on=['x', 'y'])
final_df = pd.merge(merged_map_struct_df, area_category_df, on='category', how='left')
print(final_df)
final_df_sorted = final_df.sort_values(by='area')
area_1_data = final_df_sorted[final_df_sorted['area'] == 1]

print("area가 1인 데이터:")
print(area_1_data)
