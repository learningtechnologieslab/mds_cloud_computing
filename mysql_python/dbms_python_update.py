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
        qry = 'UPDATE books SET first_name = %s WHERE book_id = %s'

        cur.execute(qry, ('Bob', 3)) 
        con.commit()

finally:

    con.close()
