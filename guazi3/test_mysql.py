# -*- coding: utf-8 -*-
# 2017/1/23 0023
# JEFF

import mysql.connector as mysqlconn

conn = mysqlconn.connect(user='root', password='root', database='learnpy')

cursor = conn.cursor()
cursor.execute('select * from guazi_items limit {},{}'.format(0, 100))
values = cursor.fetchall()

for each in values:
    print(each)

cursor.close()
conn.close()
