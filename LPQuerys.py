import mysql.connector
import datetime


def check(plaka):
    now = datetime.datetime.now()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        port="3306",
        database="proje"

    )
    mycursor = mydb.cursor()

    try:

        mydb.autocommit = True
        tuple = (plaka, )
        query = "SELECT * FROM proje.plakalar WHERE plaka = %s"
        mycursor.execute(query, tuple)
        users = mycursor.fetchall()

        if not users:
            mydb.commit()
            mydb.close()
            return False
        else:
            mydb.commit()
            mydb.close()
            mydb.close()
            return True

    except Exception as e:
        print(e)
        mydb.rollback()
        mydb.close()
        return False

    # disconnect from server



def entranceLog(plaka, blobLP):
    now = datetime.datetime.now()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        port="3306",
        database="proje"

    )
    mycursor = mydb.cursor()

    try:



        mydb.autocommit = True
        mycursor.execute('SELECT * FROM proje.entrance WHERE plaka = %s ORDER BY idEntrance desc LIMIT 1', (plaka,))
        user = mycursor.fetchall()
        minutes = now-user[0][1]

        if minutes.total_seconds() / 60 < 5:
            return False




        mycursor.execute(
            'INSERT INTO entrance (time, plaka, isim, soyisim, bina, plateimage) VALUES(%s, %s, %s, %s, %s, %s)',
            (now, plaka, user[0][3], user[0][4], user[0][5], blobLP))

        mycursor.execute('SELECT * FROM proje.plakalar ')
        users = mycursor.fetchall()

        for user in users:
            print(user)
        mydb.close()
        mycursor.close()
        return True
    except Exception as e:
        print(e)
        mydb.rollback()
        mydb.close()
        return False

    # disconnect from server
