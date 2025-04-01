# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 17:20:40 2025

@author: Andycyca

Simple exploration of the statistics behind the popular TikTok series
"Roll for Sandwich", by @AdventuresInAardia

The dataset was listed on reddit at: https://www.reddit.com/r/RollforSandwich/comments/1144pvt/spreadsheet_of_rfs_stats_from_the_discord/

Dataset: https://docs.google.com/spreadsheets/d/11fjXIUbUae35AFNlp-f10t3hSjbq5tiBykLA_IbUojs/edit?usp=share_link

I don't see who is the curator of the dataset, and there's no explicit 
license for it, so I will play it safe and not upload it to Github just in
case. If you're the curator and/or can shine light on the permission for this
dataset, please get in contact with me.

Latest version: 2025-03-31
385 data points
"""

import pandas as pd
import matplotlib.pyplot as plt
from palettable.cartocolors.sequential import SunsetDark_7 as my_cmap

# Raw data
filename = "RFS Sandwiches - Master List.csv"

# Fow now, I won't analyze anything having to do with rolls and dice
my_cols = [
    "Season",
    "Episode",
    "Bread",
    "Main",
    "Cheese",
    "Roughage",
    "Wild Magic",
    "Sauce",
    "Spells Used",
    "Rating",
    "Date",
    "Name",
]

# Create main DF
df = pd.read_csv(filename, usecols=my_cols, parse_dates=["Date"])

# TODO: split columns with more than one ingredient (roughage, sauce)

# %% Group 1: Per season
group_season = df.groupby("Season")

season_breads = group_season["Bread"].value_counts(sort=True, ascending=False)
season_mains = group_season["Main"].value_counts(sort=True, ascending=False)
season_cheeses = group_season["Cheese"].value_counts(
    sort=True, ascending=False
)
season_roughages = group_season["Roughage"].value_counts(
    sort=True, ascending=False
)
season_magics = group_season["Wild Magic"].value_counts(
    sort=True, ascending=False
)
season_sauces = group_season["Sauce"].value_counts(sort=True, ascending=False)
season_ratings = group_season["Rating"].value_counts(
    sort=True, ascending=False
)
season_scores = group_season["Rating"].agg(["min", "max", "mean"])

colors = my_cmap.mpl_colormap(df["Rating"] / df["Rating"].max())

# df["Rating"].plot(
#     kind="hist",
#     title="Rating distribution",
#     bins=10,
# )

# plt.figure()

# season_ratings.plot(kind="bar")

# %% Group 2: Extreme scores

df_perfect = df[df["Rating"] == 10.0]
df_worst = df[df["Rating"] == 0.0]

# %% Group 3: Descriptive stats
#
# Let's assume that, in order to be statistically significant, an ingredient
# must appear more than 5 times in the overall table. This is 100% arbitrary.

# Arbitrary choice, 5 seems like a good middle ground
appear_thresh = 5

# Get common stats
bread_corr = df.groupby("Bread")["Rating"].agg(["describe", "median"])

# Filter by those appearing enough times per the arbitrary threshold
bread_desc = bread_corr[bread_corr["describe", "count"] >= appear_thresh]

# Which ones are the most consistent?
bread_by_std = bread_desc.sort_values(by=("describe", "std"))

# Same will go for other groups, starting with main...
main_corr = df.groupby("Main")["Rating"].agg(["describe", "median"])
main_desc = main_corr[main_corr["describe", "count"] >= appear_thresh]
main_by_std = main_desc.sort_values(by=("describe", "std"))

# cheese ...
cheese_corr = df.groupby("Cheese")["Rating"].agg(["describe", "median"])
cheese_desc = cheese_corr[cheese_corr["describe", "count"] >= appear_thresh]
cheese_by_std = cheese_desc.sort_values(by=("describe", "std"))

# roughage...
rough_corr = df.groupby("Roughage")["Rating"].agg(["describe", "median"])
rough_desc = rough_corr[rough_corr["describe", "count"] >= appear_thresh]
rough_by_std = rough_desc.sort_values(by=("describe", "std"))

# wild magic...
wild_corr = df.groupby("Wild Magic")["Rating"].agg(["describe", "median"])
wild_desc = wild_corr[wild_corr["describe", "count"] >= appear_thresh]
wild_by_std = wild_desc.sort_values(by=("describe", "std"))

# and sauce
sauce_corr = df.groupby("Sauce")["Rating"].agg(["describe", "median"])
sauce_desc = sauce_corr[sauce_corr["describe", "count"] >= appear_thresh]
sauce_by_std = sauce_desc.sort_values(by=("describe", "std"))

# %% All ingredients

all_sauces = df["Sauce"].unique()
