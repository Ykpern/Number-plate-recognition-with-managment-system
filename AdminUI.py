from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from tkinter import ttk
import util
import mysql

from UIQuerys import ADD, DELETE, REP

admin = Tk(screenName="admin")
admin.title("admin")
admin.geometry("850x450")


def securityui():
    security1 = Tk(screenName="security1")
    security1.title("security")
    security1.geometry("450x800")
    scrollbar = Scrollbar(security1)
    scrollbar.pack(side=RIGHT, fill=Y)
    mylist = Listbox(security1, width=50, height=200, yscrollcommand=scrollbar.set, font=("Arial", 15))
    scrollbar.config(command=mylist.yview)
    mylist.pack(side="left", fill="both", expand=True)

    back_button = Button(security1, text="Close", command=security1.destroy)
    back_button.place(relx=0, rely=0)

    def refresh():
        if mylist.curselection() != []:
            mylist.delete(0, END)

    ref_button = Button(security1, text="REFRESH", command=refresh)
    ref_button.place(x=35, y=0)

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        port="3306",
        database="proje"

    )
    mycursor = mydb.cursor()
    row = 0

    try:

        mydb.autocommit = True

        query = "SELECT time, plaka, isim, soyisim, bina  FROM proje.entrance ORDER BY idEntrance DESC "
        mycursor.execute(query)
        users = mycursor.fetchall()

        if not users:
            mydb.commit()
            mydb.close()

        else:
            index = 0
            for user in users:
                mylist.insert(END, user)
                row += 30
                index = + 1

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

    #mainloop()


back_button = Button(admin, text="Enrtrance", command=securityui)
back_button.place(relx=0, rely=0)

Label(admin, text='Name').place(x=200, y=140)
Label(admin, text='Surname').place(x=200, y=170)
Label(admin, text='Apartment No').place(x=400, y=140)
Label(admin, text='Licence plate').place(x=400, y=170)

txt_name = Entry(admin)
txt_surname = Entry(admin)
txt_aptNo = Entry(admin)
txt_LP = Entry(admin)


def add_event():
    if txt_name.get() != '' and txt_surname.get() != '' and txt_aptNo.get() != '' and txt_LP.get() != '' and util.license_complies_format(txt_LP.get()):
        if ADD(txt_name.get(), txt_surname.get(), txt_aptNo.get(), txt_LP.get().upper()):
            messagebox.showinfo("Successful")
        else:
            messagebox.showinfo("Database Error")
    else:
        messagebox.showinfo("Empty Textbox")


def del_event():
    if txt_LP.get() != '':
        if DELETE(txt_LP.get()):
            messagebox.showinfo("Successful")
        else:
            messagebox.showinfo("Database Error")
    else:
        messagebox.showinfo("Error LP Empty")


def rep_event():
    if (txt_name.get() != '' and txt_surname.get() != '' and txt_aptNo.get() != '' and txt_LP.get() != ''):

        replace = Tk(screenName="Replace")
        replace.title("Replace")
        replace.geometry("850x450")

        back_button = Button(replace, text="Back", command=replace.destroy)
        back_button.place(relx=0, rely=0)

        Label(replace, text='Name').place(x=200, y=140)
        Label(replace, text='Surname').place(x=200, y=170)
        Label(replace, text='Apartment No').place(x=400, y=140)
        Label(replace, text='Licence plate').place(x=400, y=170)

        txt_name1 = Entry(replace)
        txt_surname1 = Entry(replace)
        txt_aptNo1 = Entry(replace)
        txt_LP1 = Entry(replace)

        txt_name1.place(x=260, y=140)
        txt_surname1.place(x=260, y=170)
        txt_aptNo1.place(x=480, y=140)
        txt_LP1.place(x=480, y=170)

        def rep_event2():
            if (txt_name1.get() != '' and txt_surname1.get() != '' and txt_aptNo1.get() != '' and txt_LP1.get() != ''):
                if REP(txt_name.get(), txt_surname.get(), txt_aptNo.get(), txt_LP.get(), txt_name1.get(),
                       txt_surname1.get(),
                       txt_aptNo1.get(), txt_LP1.get()):
                    replace.destroy()
                    messagebox.showinfo("Successful")
                else:
                    replace.destroy()
                    messagebox.showinfo("Error")
            else:
                replace.destroy()
                messagebox.showinfo("Text box empty")

        REP_button = Button(replace, text="REPLACE", command=rep_event2)
        REP_button.place(x=380, y=230)


txt_name.place(x=260, y=140)
txt_surname.place(x=260, y=170)
txt_aptNo.place(x=480, y=140)
txt_LP.place(x=480, y=170)

ADD_button = Button(admin, text="ADD", command=add_event)
ADD_button.place(x=310, y=230)

DELETE_button = Button(admin, text="DELETE", command=del_event)
DELETE_button.place(x=370, y=230)

REPL_button = Button(admin, text="REPLACE", command=rep_event)
REPL_button.place(x=440, y=230)

mainloop()
