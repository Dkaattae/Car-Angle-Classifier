import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("labels.csv")

df_first = df[df['split']!='dealer']
df_second = df[df['split']=='dealer']

df_full_train, df_test = train_test_split(df_second, test_size=0.1, random_state=42)
df_train, df_val = train_test_split(df_full_train, test_size=0.2, random_state=42)

df_train['split'] = 'train'
df_val['split'] = 'val'
df_test['split'] = 'test'

final_second_df = pd.concat([df_train, df_val, df_test], axis=0)

final_second_df = final_second_df.sort_values("image_id").reset_index(drop=True)

final_df = pd.concat([df_first, final_second_df], axis=0)
final_df = final_df.sort_values("image_id").reset_index(drop=True)
final_df.to_csv("labels.csv", index=False)


