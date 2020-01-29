import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import itertools
import re

train = pd.read_csv("./train.csv")
train.head(4)

shape = train.shape
print(shape)

pct_nans = round(train.isnull().sum()/shape[0]*100,1).to_frame().sort_values(by=[0], ascending=False)
plt.figure(figsize=(20,8))
sns.barplot(x=pct_nans.index, y=pct_nans[0])
plt.xticks(rotation=90)
plt.title("Percentage of missing values")
plt.ylabel("Missing values [%]")
# plt.show()

def clean_dates(row):
    '''
    This function cleans release_date row.
    '''
    text = row["release_date"]
    yr = re.findall(r"\d+/\d+/(\d+)",text)

    if int(yr[0]) >= 18:
        return(text[:-2] + "19" + yr[0])
    else:
        return(text[:-2] + "20" + yr[0])

train["release_date"] = train.apply(clean_dates, axis=1)  # applying cleaning function
train["release_date"] = pd.to_datetime(train["release_date"])  # converting release_date column to datetime type
train[["id", "title", "release_date", "runtime", "budget", "revenue"]].head()

first_date = train["release_date"].min()
last_date = train["release_date"].max()

first_movie = train[train["release_date"]==first_date]
first_movie[["id","title","release_date","runtime","budget","revenue","poster_path"]]

last_movie = train[train["release_date"]==last_date]
last_movie[["id","title","release_date","runtime","budget","revenue","poster_path"]]

train.loc[:,"release_year"] = train.loc[:,"release_date"].dt.year
train.loc[:,"release_month"] = train.loc[:,"release_date"].dt.month
movies_2017 = train[train["release_year"]==2017]
movies_2017[["id","title","release_date","runtime","budget","revenue"]].head(10)

movies_2018 = train[train["release_year"]==2018]
movies_2018[["id","title","release_date","runtime","budget","revenue"]].head(10)

plt.figure(figsize=(25,10))
sns.countplot(x="release_year", data=TS)
plt.xticks(rotation=70)
plt.show()