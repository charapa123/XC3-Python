import snowflake.connector
import requests

# URL to scrape
url = "https://game8.co/games/Xenoblade-Chronicles-3/archives/384734"

try:
    response = requests.get(url)
    response.raise_for_status()  # Check for any request errors

    # Store the HTML content in a variable
    html_content = response.text
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")

# Set up your Snowflake connection
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



# Insert the data into the Snowflake table
cursor = conn.cursor()
cursor.execute("INSERT INTO MyHTMLData (HTMLContent) VALUES (%s)", (html_content,))
cursor.close()
conn.commit()
conn.close()
