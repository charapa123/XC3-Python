from urllib.request import urlopen
import pandas as pd
import snowflake.connector

url = "https://www.ign.com/wikis/xenoblade-chronicles-3/Side_Quests_-_List_of_Standard_Quests"

page = urlopen(url)

html_bytes = page.read()
html = html_bytes.decode("utf-8")

print(html)

tables = pd.read_html(html)

tables[0]['Chapter'] = "Chapter 1"
tables[1]['Chapter'] = "Chapter 2"
tables[2]['Chapter'] = "Chapter 3"
tables[3]['Chapter'] = "Chapter 4"
tables[4]['Chapter'] = "Chapter 5"
tables[5]['Chapter'] = "Chapter 6"
tables[6]['Chapter'] = "Chapter 7"
tables[7]['Chapter'] = "Post-Game"

result = pd.concat([tables[0],tables[1],tables[2],tables[3],tables[4],tables[5],tables[6],tables[7]], axis=0,ignore_index=True)

result = result.fillna("NULL")

print(result)



conn = snowflake.connector.connect(
    user='email',
    authenticator = 'externalbrowser',
    account='id.eu-west-2',
    region = 'eu-west-2',
    # authenticator = 'externalbrowser',  # Replace with your Snowflake account URL
    warehouse='warehouse name',  # Replace with your Snowflake warehouse name
    database='database name',
    schema='schema name'
)

# Your code for parsing and transforming the HTML
# ...

# Define the DataFrame with the adjusted schema
result = result[['Recommended Level', 'Quest Name', 'Chapter', 'Post-Game Quest', 'How to accept Quest', 'Objective', 'Reward']]
result.columns = ['RECOMMENDED_LEVEL', 'QUEST_NAME', 'CHAPTER', 'POST_GAME_QUEST', 'HOW_TO_ACCEPT_QUEST', 'OBJECTIVE', 'REWARD']

# Insert the data into the Snowflake table
cursor = conn.cursor()

# Use the executemany method to insert the DataFrame into the table
insert_query = "INSERT INTO XC3_TEST_QUESTS (RECCOMENDED_LEVEL, QUEST_NAME, CHAPTER, POST_GAME_QUEST, HOW_TO_ACCEPT_QUEST, OBJECTIVE, REWARD) VALUES (%(RECOMMENDED_LEVEL)s, %(QUEST_NAME)s, %(CHAPTER)s, %(POST_GAME_QUEST)s, %(HOW_TO_ACCEPT_QUEST)s, %(OBJECTIVE)s, %(REWARD)s)"
values = result.to_dict(orient='records')
cursor.executemany(insert_query, values)

cursor.close()
conn.commit()
conn.close()
