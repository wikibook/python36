import os
import pandas

home_folder = os.path.expanduser("~")
data_folder = os.path.join(home_folder, "Documents", "python", "nba_winner")

data_files=["nba_2015_10.csv", "nba_2015_11.csv", "nba_2015_12.csv",
            "nba_2016_01.csv", "nba_2016_02.csv", "nba_2016_03.csv",
            "nba_2016_04.csv", "nba_2016_05.csv", "nba_2016_06.csv"]

cvs_objs = []
for f in data_files:
    month_data = os.path.join(data_folder, f)
    cvs_objs.append(pandas.read_csv(month_data))

season_result = pandas.concat(cvs_objs, ignore_index=True)
season_result.columns = ["Date", "StartTime", "VisitorTeam", "VisitorPts",
                         "HomeTeam", "HomePts", "ScoreType", "Overtime", "Notes"]

print(season_result[-5:])

# HomeWin: 홈팀이 승리한 경우에는 True, 아닌 경우에는 False으로 입력
season_result["HomeWin"] = season_result["HomePts"] > season_result["VisitorPts"]

# 홈팀으로 적극적인 응원을 받는 경우, 팀의 승리에 유리한지 확인
score = 100 * season_result["HomeWin"].sum() / season_result["HomeWin"].count()
print("Home Win percentage: {0:.1f}%".format(score))

# 작년 시즌의 순위를 고려
standing_file = os.path.join(data_folder, "nba_2014_2015_standing.csv")
standing_result = pandas.read_csv(standing_file, skiprows=[0])

# 선수 개개인의 능력치를 고려
player_file = os.path.join(data_folder, "nba_2016_player_stat.csv")
player_result = pandas.read_csv(player_file)
print(player_result["PLAYER"][:3])

# 팀 약자와 팀명을 맵핑
team_name = {"GS"  : "Golden State Warriors",
             "SA"  : "San Antonio Spurs",
             "CLE" : "Cleveland Cavaliers",
             "TOR" : "Toronto Raptors",
             "OKC" : "Oklahoma City Thunder",
             "LAC" : "Los Angeles Clippers",
             "ATL" : "Atlanta Hawks",
             "BOS" : "Boston Celtics",
             "CHA" : "Charlotte Hornets",
             "MIA" : "Miami Heat",
             "IND" : "Indiana Pacers",
             "DET" : "Detroit Pistons",
             "POR" : "Portland Trail Blazers",
             "DAL" : "Dallas Mavericks",
             "MEM" : "Memphis Grizzlies",
             "CHI" : "Chicago Bulls",
             "HOU" : "Houston Rockets",
             "WSH" : "Washington Wizards",
             "UTAH" : "Utah Jazz",
             "ORL" : "Orlando Magic",
             "DEN" : "Denver Nuggets",
             "MIL" : "Milwaukee Bucks",
             "SAC" : "Sacramento Kings",
             "NY" : "New York Knicks",
             "NO" : "New Orleans Pelicans",
             "MIN" : "Minnesota Timberwolves",
             "PHX" : "Phoenix Suns",
             "BKN" : "Brooklyn Nets",
             "LAL" : "Los Angeles Lakers",
             "PHI" : "Philadelphia 76ers",
}

# NBA 모든 선수를 정보를 순회하면서 각 선수의 팀과 PER 값을 추출
team_per = {}
for key, value in team_name.items():
    team_per[value] = []

for idx, row in player_result.iterrows():
    player = row["PLAYER"]
    per = row["PER"]
    team_list = player.split(',')[1].strip(' ').split("/")
    for team in team_list:
        team_per[team_name[team]].append(per)

# PER 지수 비교
import numpy
print("Golden State Warriors: Sum of PER: {0:.2f} / Mean of PER: {1:.2f}"
      .format(numpy.sum(team_per["Golden State Warriors"]), numpy.mean(team_per["Golden State Warriors"])))
print("Philadelphia 76ers: Sum of PER: {0:.2f} / Mean of PER: {1:.2f}"
      .format(numpy.sum(team_per["Philadelphia 76ers"]), numpy.mean(team_per["Philadelphia 76ers"])))


# 홈팀, 원정팀의 연승 횟수를 세기 위한 추가 컬럼
season_result["HomeWinStreak"] = 0
season_result["VisitorWinStreak"] = 0

from collections import defaultdict
winning_streak = defaultdict(int)

for index, row in season_result.iterrows():
    home = row["HomeTeam"]
    visitor = row["VisitorTeam"]
    row["HomeWinStreak"] = winning_streak[home]
    row["VisitorWinStreak"] = winning_streak[visitor]
    season_result.ix[index] = row

    if row["HomeWin"]:
        winning_streak[home] += 1
        winning_streak[visitor] = 0
    else:
        winning_streak[home] = 0
        winning_streak[visitor] += 1

# 홈팀의 승리 결과는 y_test 변수에 저장
y_test = season_result["HomeWin"].values


from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score

clf = DecisionTreeClassifier(random_state=7)
x_test = season_result[["HomeWinStreak", "VisitorWinStreak"]].values
scores = cross_val_score(clf, x_test, y_test, scoring='accuracy')

print("Accuracy: {0:.1f}% (+/- {1:.2f}%)".format(numpy.mean(scores) * 100, numpy.std(scores)))

# 각 팀별 상위 10명의 선수의 PER 합계를 저장
standing_result["PER_Sum"] = 0
for idx, row in standing_result.iterrows():
    team = row["Team"]
    row["PER_Sum"] = numpy.sum(team_per[team][:10])
    standing_result.ix[idx] = row

# 매 경기마다 Home team의 PER이 높은 경우를 1, 아닌 경우를 0으로 설정
season_result["HomePERHigh"] = 0
for idx, row in season_result.iterrows():
    home = row["HomeTeam"]
    visitor = row["VisitorTeam"]

    home_per = standing_result[standing_result["Team"] == home]["PER_Sum"].values[0]
    visitor_per = standing_result[standing_result["Team"] == visitor]["PER_Sum"].values[0]
    row["HomePERHigh"] = int(home_per > visitor_per)
    season_result.ix[idx] = row

x_test = season_result[["HomePERHigh"]].values
clf = DecisionTreeClassifier(random_state=7)
scores = cross_val_score(clf, x_test, y_test, scoring='accuracy')
print("Accuracy: {0:.1f}% (+/- {1:.2f}%)".format(numpy.mean(scores) * 100, numpy.std(scores)))

x_test = season_result[["HomeWinStreak", "VisitorWinStreak", "HomePERHigh"]].values
clf = DecisionTreeClassifier(random_state=7)
scores = cross_val_score(clf, x_test, y_test, scoring='accuracy')
print("Accuracy: {0:.1f}% (+/- {1:.2f}%)".format(numpy.mean(scores) * 100, numpy.std(scores)))


# 각 팀의 이름을 숫자로 변환: Label encoding
from sklearn.preprocessing import LabelEncoder
name_encoding = LabelEncoder()
name_encoding.fit(season_result["HomeTeam"].values)

print(name_encoding.transform(["Golden State Warriors", "Cleveland Cavaliers"]))
print(name_encoding.inverse_transform([9, 5]))

# 숫자로 변환된 팀 경기 정보를 team_match에 저장
home_teams = name_encoding.transform(season_result["HomeTeam"].values)
visitor_teams = name_encoding.transform(season_result["VisitorTeam"].values)
team_match = numpy.vstack([home_teams, visitor_teams]).T

from sklearn.preprocessing import OneHotEncoder
onehot = OneHotEncoder()
x_test = onehot.fit_transform(team_match).todense()

clf = DecisionTreeClassifier(random_state=7)
scores = cross_val_score(clf, x_test, y_test, scoring='accuracy')
print("Accuracy: {0:.1f}% (+/- {1:.2f}%)".format(numpy.mean(scores) * 100, numpy.std(scores)))

# 작년 시즌의 팀의 순위를 고려하는 경우
season_result["HomeRankHigh"] = 0
for idx, row in season_result.iterrows():
    home = row["HomeTeam"]
    visitor = row["VisitorTeam"]

    home_rank = standing_result[standing_result["Team"] == home]["Rk"].values[0]
    visitor_rank = standing_result[standing_result["Team"] == visitor]["Rk"].values[0]
    row["HomeRankHigh"] = int(home_rank > visitor_rank)
    season_result.ix[idx] = row

x_test = season_result[["HomeRankHigh"]].values
clf = DecisionTreeClassifier(random_state=7)
scores = cross_val_score(clf, x_test, y_test, scoring='accuracy')
print("Accuracy: {0:.1f}% (+/- {1:.2f}%)".format(numpy.mean(scores) * 100, numpy.std(scores)))

# 작년 시즌의 팀의 순위와 per, 연승 정보를 같이 고려하는 경우
x_test = season_result[["HomeRankHigh", "HomePERHigh", "HomeWinStreak", "VisitorWinStreak"]].values
clf = DecisionTreeClassifier(random_state=7)
scores = cross_val_score(clf, x_test, y_test, scoring='accuracy')
print("Accuracy: {0:.1f}% (+/- {1:.2f}%)".format(numpy.mean(scores) * 100, numpy.std(scores)))


