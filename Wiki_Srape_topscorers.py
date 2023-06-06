import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
    host="***",
    user="***",
    password="***",
    database="***"
)

mycursor = mydb.cursor()
dataframes = []
url = 'https://en.wikipedia.org/wiki/List_of_top_Premier_League_goal_scorers_by_season'
y = 0

### Selecting seasons 2000 till now ###
for x in range(8, 31):
    y = x - 8
    df = pd.read_html(url)[x]
    # Most goal columns had a source in them, removed them #
    if 'Goals' not in df.columns:
        for col in df.columns:
            if 'goals' in col.lower():
                df.rename(columns={col: 'Goals'}, inplace= True)
                break
    # 2 Columns in the tables were named Team instead of Club making sure it's unified#
    if 'Club' not in df.columns:
        for col in df.columns:
            if 'team' in col.lower():
                df.rename(columns={col: 'Club'}, inplace=True)
                break
    year_start = 2000 + y
    year_end = 2001 + y
    year_range = f"{year_start}/{year_end}"
    df['Year'] = year_range

    dataframes.append(df)

# for each dataframe in dataframes, it adds all rows to Mysql on the corresponding column #
for df in dataframes:
    for i, row in df.iterrows():
        sql = "INSERT topscorer (Year, Pos, Player, Club, Goals) VALUES (%s, %s, %s, %s, %s)"
        values = (row['Year'], row['Rank'], row['Player'], row['Club'], row['Goals'])
        mycursor.execute(sql, values)

mydb.commit()
