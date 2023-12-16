import requests
import snowflake.connector

urls = [
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/386225",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/386494",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/387299",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/386610",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/393672",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/386308",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/387247",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/384515",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/386170",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/387278",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/386152",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/387441",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/386300",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/386254",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/386287",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/386460",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/386818",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/386156",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/387480",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/386420",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/386381",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/386253",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/386765",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/386488",
    "https://game8.co/games/Xenoblade-Chronicles-3/archives/384515"
]

html_contents = []  # Store the HTML content
url_column = []  # Store the URLs as a single column

for url in urls:
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for any request errors

        html_content = response.text
        html_contents.append(html_content)
        url_column.append(url)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

# Establish the Snowflake connection
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

# Create a cursor for executing SQL queries
cursor = conn.cursor()

# Insert the data into the Snowflake table, one row at a time
for url, html_content in zip(url_column, html_contents):
    cursor.execute("INSERT INTO MyHTMLDataAscention (URL, HTMLContent) VALUES (%s, %s)", (url, html_content))

# Close the cursor and commit the changes
cursor.close()
conn.commit()

# Close the Snowflake connection
conn.close()
