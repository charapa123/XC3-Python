from urllib.request import urlopen
import pandas as pd
import snowflake.connector

url = "https://www.ign.com/wikis/xenoblade-chronicles-3/All_Heroes_and_How_to_Unlock_(Hero_Quests)"

page = urlopen(url)

html_bytes = page.read()
html = html_bytes.decode("utf-8")


tables = pd.read_html(html)

tables[0]['Chapter'] = "Chapter 3"
tables[1]['Chapter'] = "Chapter 4"
tables[2]['Chapter'] = "Chapter 5"
tables[3]['Chapter'] = "Chapter 6"
tables[4]['Chapter'] = "Post-Game Heros"

result = pd.concat([tables[0],tables[1],tables[2],tables[3],tables[4]], axis=0,ignore_index=True)

result = result.fillna("NULL")

columns_to_drop = ["Class","Unnamed: 1"]
result = result.drop(columns=columns_to_drop)

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
result = result[['Hero', 'Hero Quest', 'Chapter']]
result.columns = ['HERO', 'HERO_QUEST', 'CHAPTER']

# Insert the data into the Snowflake table
cursor = conn.cursor()

# Use the executemany method to insert the DataFrame into the table
insert_query = "INSERT INTO XC3_HERO_QUESTS (HERO, HERO_QUEST, CHAPTER) VALUES (%(HERO)s, %(HERO_QUEST)s, %(CHAPTER)s)"
values = result.to_dict(orient='records')
cursor.executemany(insert_query, values)

cursor.close()
conn.commit()
conn.close()
