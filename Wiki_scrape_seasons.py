import pandas as pd
import mysql.connector


mydb = mysql.connector.connect(
        host="***",
        user="***",
        password="***",
        database="***"
)

mycursor = mydb.cursor()
# Year 2000 - 2023 switching links, picking the right table for each page, 2 tables with exceptions #
for x in range(0, 23):
    year_start_link = 2000 + x
    year_end_link = 9301 + x
    url = f"https://en.wikipedia.org/wiki/{year_start_link}%E2%80%{year_end_link}_Premier_League"

    if x in (0, 1, 3, 22):
        df = pd.read_html(url)[5]

    if x in (2, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21):
        df = pd.read_html(url)[4]

    if x == 9:
        df = pd.read_html(url)[4]
        df['Pts'] = df['Pts'].astype(str).str.extract('(\d+)', expand=False)

    if x == 19:
        df = pd.read_html(url)[5]
        team_column = next((col for col in df.columns if 'Team' in col), None)

        if team_column is not None:
            df.rename(columns={team_column: 'Team'}, inplace=True)



    # Changes − in the numerical - #
    df['GD'] = df['GD'].str.replace('−', '-', )
    year_start = 2000 + x
    year_end = 2001 + x
    year_range = f"{year_start}/{year_end}"
    df['Year'] = year_range

    for i, row in df.iterrows():
        sql = "INSERT INTO 2000_now (Year, Pos, Team, PLD, Wins, Draw, Loss, Goals_for, Goals_against, Goal_differential, Points) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (row['Year'], row['Pos'], row['Team'], row['Pld'], row['W'], row['D'], row['L'], row['GF'], row['GA'], row['GD'], row['Pts'])
        mycursor.execute(sql, values)
    mydb.commit()
