import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

mysql=mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD")
)

cursor=mysql.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS url_shortener")
cursor.execute("USE url_shortener")

cursor.execute("CREATE TABLE IF NOT EXISTS links (id INT AUTO_INCREMENT PRIMARY KEY, url TEXT, path VARCHAR(255) UNIQUE, user VARCHAR(255))")

def add_link(url, path):
    cursor.execute("INSERT INTO links (url, path) VALUES (%s, %s)", (url, path))
    mysql.commit()
    debug()

def debug():
    cursor.execute("SELECT * FROM links")
    results=cursor.fetchall()
    for x in results:
        print(x)