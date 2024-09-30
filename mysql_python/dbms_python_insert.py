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
        qry = 'INSERT INTO books (book_id, first_name, last_name, number_of_books, dob)'
        qry = qry + 'VALUES(%s, %s, %s, %s, %s)'

        cur.execute(qry, (3, 'Stephen', 'King', 400, '1947-09-21')) 
        con.commit()

finally:

    con.close()
