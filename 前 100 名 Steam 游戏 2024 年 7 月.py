import pandas as pd
from pyecharts.charts import Bar, Line
from pyecharts import options as opts

df = pd.read_csv('./top_100_steam_games.csv')
print(df.head())
print(df.isna().sum())
print(df.info())

df.columns = df.columns.str.strip()

split_df = df.assign(Genre=df['Genre'].str.split(' / ')).explode('Genre')

genre_counts = split_df['Genre'].value_counts()

# 类型分布的水平柱状图
bar = (
    Bar()
    .add_xaxis(genre_counts.index.tolist())
    .add_yaxis("游戏数量", genre_counts.values.tolist())
    .set_global_opts(
        title_opts=opts.TitleOpts(title="游戏类型的分布"),
        yaxis_opts=opts.AxisOpts(name="游戏数量"),
        xaxis_opts=opts.AxisOpts(name="类型"),
        toolbox_opts=opts.ToolboxOpts(),
        datazoom_opts=[opts.DataZoomOpts()],
    )
)
bar.render('游戏类型的分布.html')

genre_games = split_df.groupby('Genre')['Title'].apply(list).to_dict()

# 游戏类型下的游戏名称
for genre, games in genre_games.items():
    print(f'Genre:{genre}')
    print('Games:')
    for idx, game in enumerate(games, 1):
        print(f'{idx}.{game}')
    print()

# 将数值列从字符串类型转换为数值型
df['Current'] = df['Current'].str.replace(',', '').astype(int)
df['24h Peak'] = df['24h Peak'].str.replace(',', '').astype(int)
df['All-Time Peak'] = df['All-Time Peak'].str.replace(',', '').astype(int)

# 对游戏类型分类，并为每个类型创建一个新的数据框
split_df = df.assign(Genre=df['Genre'].str.split(' / ')).explode('Genre')
genre_means = split_df.groupby('Genre')[['Current', '24h Peak', 'All-Time Peak']].mean()

# 按类型绘制平均玩家人数折线图
line = (
    Line()
    .add_xaxis(genre_means.index.tolist())
    .add_yaxis("Current", genre_means["Current"].tolist(), is_smooth=True)
    .add_yaxis("24h Peak", genre_means["24h Peak"].tolist(), is_smooth=True)
    .add_yaxis("All-Time Peak", genre_means["All-Time Peak"].tolist(), is_smooth=True)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="按类型划分的平均玩家人数折线图"),
        xaxis_opts=opts.AxisOpts(name="类型", axislabel_opts={"rotate": 45}),
        yaxis_opts=opts.AxisOpts(name="平均玩家人数"),
        toolbox_opts=opts.ToolboxOpts(),
        datazoom_opts=[opts.DataZoomOpts()],
    )
)
line.render('按类型划分的平均玩家人数折线图.html')

# 找出最高和最低排名游戏
highest_rank_game = df[df['Rank'] == df['Rank'].max()]
lowest_rank_game = df[df['Rank'] == df['Rank'].min()]

#  提取排名最高和最低游戏的玩家人数
highest_rank_counts = highest_rank_game[['Current', '24h Peak', 'All-Time Peak']].squeeze()
lowest_rank_counts = lowest_rank_game[['Current', '24h Peak', 'All-Time Peak']].squeeze()

metrics = ['Current', '24h Peak', 'All-Time Peak']

# 最高和最低排名游戏的玩家人数对比
bar2 = (
    Bar()
    .add_xaxis(metrics)
    .add_yaxis("最高游戏排名", highest_rank_counts.tolist(), stack="stack1")
    .add_yaxis("最低游戏排名", lowest_rank_counts.tolist(), stack="stack1")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="最高和最低排名游戏的玩家人数对比"),
        xaxis_opts=opts.AxisOpts(name="玩家人数指标"),
        yaxis_opts=opts.AxisOpts(name="玩家人数"),
        toolbox_opts=opts.ToolboxOpts(),
    )
)
bar2.render('最高和最低排名游戏的玩家人数对比.html')

genre_player_count = split_df.groupby('Genre')[['Current', '24h Peak', 'All-Time Peak']].sum()

most_popular_genre = genre_player_count.sum(axis=1).idxmax()
least_popular_genre = genre_player_count.sum(axis=1).idxmin()

bar3 = (
    Bar()
    .add_xaxis(["最流行类型", "最不流行类型"])
    .add_yaxis(most_popular_genre, genre_player_count.loc[most_popular_genre].tolist(), stack="stack1")
    .add_yaxis(least_popular_genre, genre_player_count.loc[least_popular_genre].tolist(), stack="stack1")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="最受欢迎和最不受欢迎游戏类型的玩家参与度"),
        yaxis_opts=opts.AxisOpts(name="玩家总数"),
        toolbox_opts=opts.ToolboxOpts(),
    )
)
bar3.render('最受欢迎和最不受欢迎游戏类型的玩家参与度.html')

print(f'按类型分类的玩家总数: \n {genre_player_count}')

