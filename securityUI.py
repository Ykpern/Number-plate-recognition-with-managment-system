from tkinter import *
import datetime
import mysql.connector

security = Tk(screenName="security")
security.title("security")
security.geometry("580x800")
security.resizable(0, 0)
scrollbar = Scrollbar(security)
scrollbar.pack(side=RIGHT, fill=Y, anchor=E)
mylist = Listbox(security, width=50, height=32, yscrollcommand=scrollbar.set, font=("Arial", 15))

scrollbar.config(command=mylist.yview)
mylist.pack(side="left", fill="both", expand=True)

back_button = Button(security, text="Close", command=security.destroy)
back_button.place(relx=0, rely=0)

txt_LP = Entry(security)
txt_LP.place(x=430, y=2)


def refresh():
    mainpage()
    mainloop()


def search():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        port="3306",
        database="proje"

    )
    mycursor = mydb.cursor()
    LP = txt_LP.get()
    if LP != '':
        mydb.autocommit = True
        query ="SELECT time, plaka, isim, soyisim, bina  FROM proje.entrance WHERE plaka = %s ORDER BY time DESC"
        tupleLP = LP,
        mycursor.execute(query, tupleLP)

        users = mycursor.fetchall()

        try:
            if not users:
                mydb.commit()
                mydb.close()

            else:
                mylist.delete(0, END)
                for user in users:
                    mylist.insert(END, user)

                mylist.pack(expand=True)
                mylist.place(x=0, y=25)
                scrollbar.config(command=mylist.yview)
                mydb.commit()
                mydb.close()
                mydb.close()
                mainloop()

        except Exception as e:
            print(e)
            mydb.rollback()
            mydb.close()

def week():

    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            port="3306",
            database="proje"

        )
        mycursor = mydb.cursor()

        mydb.autocommit = True

        query = "select time, plaka, isim, soyisim, bina from proje.entrance where time between date_sub(now(),INTERVAL 1 WEEK) and now();"

        mycursor.execute(query)
        users = mycursor.fetchall()

        if not users:
            mydb.commit()
            mydb.close()

        else:
            mylist.delete(0,END)
            for user in users:
                mylist.insert(END, user)


            mylist.pack(expand=True)
            mylist.place(x=0, y=25)
            scrollbar.config(command=mylist.yview)
            mydb.commit()
            mydb.close()
            mydb.close()


    except Exception as e:
        print(e)
        mydb.rollback()
        mydb.close()



ref_button = Button(security, text="REFRESH", command=refresh)
lp_button = Button(security, text="Search", command=search)
week_button = Button(security, text="This WEEK", command=week)
ref_button.place(x=40, y=0)
week_button.place(x=100, y=0)
lp_button.place(x=380, y=0)



def mainpage():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            port="3306",
            database="proje"

        )
        mycursor = mydb.cursor()

        mydb.autocommit = True

        query = "SELECT time, plaka, isim, soyisim, bina  FROM proje.entrance ORDER BY idEntrance DESC "
        mycursor.execute(query)
        users = mycursor.fetchall()

        if not users:
            mydb.commit()
            mydb.close()

        else:
            mylist.delete(0,END)
            for user in users:
                mylist.insert(END, user)


            mylist.pack(expand=True)
            mylist.place(x=0, y=25)
            scrollbar.config(command=mylist.yview)
            mydb.commit()
            mydb.close()
            mydb.close()


    except Exception as e:
        print(e)
        mydb.rollback()
        mydb.close()

        # disconnect from server
refresh()
mainloop()
