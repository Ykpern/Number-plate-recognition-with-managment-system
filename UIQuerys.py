import mysql.connector
import datetime
from tkinter import *
from tkinter import messagebox

now = datetime.datetime.now()


def ADD(isim, soyisim, bina, plaka):
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
        mycursor.execute('INSERT INTO plakalar ( isim, soyisim, bina, plaka) VALUES(%s, %s, %s, %s)',
                         (isim, soyisim, bina, plaka))

        mycursor.execute('SELECT * FROM proje.plakalar ')
        users = mycursor.fetchall()

        for user in users:
            print(user)
        mydb.close()
        mycursor.close()
        return True
    except:
        mydb.rollback()
        mydb.close()
        return False

    # disconnect from server


def DELETE(plaka):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        port="3306",
        database="proje"

    )
    mycursor = mydb.cursor()
    delete_flg = False

    def setflagtrue():
        try:
            delete_flg = True
            if delete_flg == True:
                query = 'SELECT * FROM proje.plakalar WHERE plaka = %s'
                mycursor.execute(query, tuple1)
                users = mycursor.fetchall()
                query = "DELETE FROM plakalar WHERE plaka = %s"

                mycursor.execute(query, tuple1)
                mycursor.execute(
                    'INSERT INTO delete_log ( date, isim, soyisim, plaka, operation) VALUES(%s, %s, %s, %s, %s)',
                    (now, users[0][0], users[0][1], plaka, "DELETE"))
                mycursor.execute('SELECT * FROM proje.plakalar ')
                users = mycursor.fetchall()
                for user in users:
                    print(user)

                mydb.close()
                mycursor.close()
                confirm.destroy()
                messagebox.showinfo("Successful")
                return True
            else:
                confirm.destroy()
                messagebox.showinfo("Error")
                return False
        except Exception as e:
            print(e)
            mydb.rollback()
            mydb.close()
            messagebox.showinfo(e)
            return False

    def setflagfalse():
        confirm.destroy()
        return False

    try:

        mydb.autocommit = True
        tuple1 = (plaka,)
        query = 'SELECT * FROM proje.plakalar WHERE plaka = %s'
        mycursor.execute(query, tuple1)
        users = mycursor.fetchall()

        if not users:
            mydb.commit()
            mydb.close()
            return False
        else:
            confirm = Tk(screenName="security")
            confirm.title("security")
            confirm.geometry("450x200")
            user_lbl = Label(confirm, text="Do you want to delete user ")
            user_lbl.place(relx=0.5, rely=0.1, anchor=CENTER)
            user_lbl2 = Label(confirm, text="NAME: " + users[0][0] + " SURNAME: " + users[0][1] + "\n APARTMENT NO: "+ users[0][2] + " LICENCE PLATE: " + users[0][3])
            user_lbl2.place(relx=0.5, rely=0.3, anchor=CENTER)
            yes_btn = Button(confirm, text="YES", command=setflagtrue)
            yes_btn.place(relx=0.6, rely=0.5, anchor=CENTER)
            no_btn = Button(confirm, text="NO", command=setflagfalse)
            no_btn.place(relx=0.4, rely=0.5, anchor=CENTER)
            mainloop()


    except Exception as e:
        print(e)
        mydb.rollback()
        mydb.close()
        return False


def REP(isim, soyisim, bina, plaka, isim1, soyisim1, bina1, plaka1):
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
        tuple1 = (isim, soyisim, bina, plaka)
        query = 'SELECT * FROM proje.plakalar WHERE isim = %s AND soyisim = %s AND bina = %s AND plaka = %s'
        mycursor.execute(query, tuple1)
        users = mycursor.fetchall()

        if not users:
            mydb.commit()
            mydb.close()
            return False
        else:
            query = "DELETE FROM plakalar WHERE isim = %s AND soyisim = %s AND bina = %s AND plaka = %s"

            mycursor.execute(query, tuple1)
            mycursor.execute(
                'INSERT INTO delete_log ( date, isim, soyisim, plaka, operation) VALUES(%s, %s, %s, %s, %s)',
                (now, isim, soyisim, plaka, "REPLACE"))

        mycursor.execute('INSERT INTO plakalar ( isim, soyisim, bina, plaka) VALUES(%s, %s, %s, %s)',
                         (isim1, soyisim1, bina1, plaka1))
        users = mycursor.fetchall()
        for user in users:
            print(user)

        mydb.close()
        mycursor.close()
        return True
    except:

        mydb.rollback()
        mydb.close()

        return False

# disconnect from server
