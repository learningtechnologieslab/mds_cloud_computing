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
        qry = 'DELETE FROM books WHERE book_id = %s'

        cur.execute(qry, (3)) 
        con.commit()

finally:

    con.close()
