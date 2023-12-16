from urllib.request import urlopen
from bs4 import BeautifulSoup
import snowflake.connector

# URL to scrape
url = "https://www.dualshockers.com/xenoblade-chronicles-3-nopon-caravan/"

page = urlopen(url)

html_bytes = page.read()
html = html_bytes.decode("utf-8")

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')

# Find all <h3> elements in the HTML
h3_elements = soup.find_all('h3')

# Extract and store the text content of each <h3> element
h3_texts = [h3.get_text() for h3 in h3_elements]


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
for text in h3_texts:
    cursor.execute("INSERT INTO NOPON (NOPONN) VALUES (%s)", (text,))
cursor.close()
conn.commit()
conn.close()

