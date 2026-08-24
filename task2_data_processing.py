import pandas as pd

#converts the json(which is produced in task1) into DataFrame
df = pd.read_json("data/trends_20260823.json")
print(f"No. of stories == {len(df)} ")
#removing duplicate rows with same post_d
df = df.drop_duplicates(subset="post_id")
print(f"removing dupes: {len(df)}")
#removing null value containing rows 
df = df.dropna(subset=["post_id", "title", "score"])
print(f"removing nulls: {len(df)}") 
#checking datatype of each cloumn
print(df.dtypes)
print(df["num_comments"].isna().sum())
#since one null value present in num_comments row we filled it with zero and converted column into integer
df["num_comments"] = df["num_comments"].fillna(0).astype(int)

print(df["num_comments"].isna().sum())

print(df.dtypes)
#removing the rows which have low rating
df = df[df["score"]>=5]
print(f"removed low scores: {len(df)}")
#removing the white spaces at staring and ending of title
df["title"] = df["title"].str.strip()

df.to_csv("data/trends_clean.csv", index=False)
print(f"\n{len(df)} rows saved to data/trends_clean.csv")

print("\nstories per category")
print(df["category"].value_counts())