# Robson Mattos
# rjnmattos@gmail.com

import psycopg2

DBNAME = "news"
conn = psycopg2.connect(dbname=DBNAME)
cursor = conn.cursor()

print'S u m m a r y'


def quiz(sql):
    print('-' * 80)
    cursor.execute(sql)
    results = cursor.fetchall()

    for result in results:
        print (result[0])

quiz('select * from vw_quiz_one')
quiz('select * from vw_quiz_two')
quiz('select * from vw_quiz_three')

conn.close()
