import pymysql.cursors
import pandas as pd
import datetime
from itertools import combinations


con = pymysql.connect(host='134.209.169.96',
                             user='is2710practice',
                             password='!s2710Pra6t1c3',
                             db='test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
try:

    with con.cursor() as cur:

        cur.execute('SELECT * FROM books')

        rows = cur.fetchall()

        for row in rows:
            print(row['book_id'], row['first_name'], row['last_name'])

finally:

    con.close()