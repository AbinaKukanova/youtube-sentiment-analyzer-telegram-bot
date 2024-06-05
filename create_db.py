import sqlite3
from bs4 import BeautifulSoup
import re


conn = sqlite3.connect('final_res.db')
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS comments 
(id int PRIMARY KEY, comment text) 
""")

conn.commit()
conn.close()

