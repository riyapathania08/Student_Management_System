from re import search
from tkinter import *
import time
from tkinter import ttk, messagebox
import pymysql
import ttkthemes
from datetime import datetime

def iexit():
    result=messagebox.askyesno('Confirm','Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass






def update_student():
    def update_data():
        try:
            current_date = datetime.now().strftime('%Y-%m-%d')
            current_time = datetime.now().strftime('%H:%M:%S')
            query = '''
                UPDATE student 
                SET name = %s, mobile = %s, email = %s, address = %s, gender = %s, dob = %s, date = %s, time = %s 
                WHERE id = %s
            '''

            # Executing the update query with correctly ordered parameters
            mycursor.execute(query, (
                nameEntry.get(),
                phoneEntry.get(),
                EmailEntry.get(),
                addressEntry.get(),
                genderEntry.get(),
                dobEntry.get(),
                current_date,
                current_time,
                idEntry.get(),
            ))
            con.commit()
            messagebox.showinfo('Success', f'Id {idEntry.get()} is modified successfully',parent=update_window)
            update_window.destroy()
            show_student()
        except Exception as e:
            messagebox.showerror('Error', f'Error updating data: {e}')

    update_window = Toplevel()
    update_window.resizable(False, False)
    update_window.title('Update Student')

    # ID Entry
    idLabel = Label(update_window, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0)
    idEntry = Entry(update_window, font=('roman', 15, 'bold'))
    idEntry.grid(row=0, column=1)

    # Name Entry
    nameLabel = Label(update_window, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky='W')
    nameEntry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    # Phone Entry
    phoneLabel = Label(update_window, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky='W')
    phoneEntry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    # Email Entry
    EmailLabel = Label(update_window, text='Email', font=('times new roman', 20, 'bold'))
    EmailLabel.grid(row=3, column=0, padx=30, pady=15, sticky='W')
    EmailEntry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
    EmailEntry.grid(row=3, column=1, pady=15, padx=10)

    # Address Entry
    addressLabel = Label(update_window, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky='W')
    addressEntry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    # Gender Entry
    genderLabel = Label(update_window, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky='W')
    genderEntry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    # DOB Entry
    dobLabel = Label(update_window, text='D.O.B', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky='W')
    dobEntry = Entry(update_window, font=('roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    # Update Button
    update_student_button = ttk.Button(update_window, text='UPDATE', command=update_data)
    update_student_button.grid(row=7, columnspan=2, pady=15)

    # Fetch selected student data
    indexing = studentTable.focus()
    content = studentTable.item(indexing)
    listdata = content['values']

    # Populate entries with selected student data
    idEntry.insert(0, listdata[0])
    nameEntry.insert(0, listdata[1])
    phoneEntry.insert(0, listdata[2])
    EmailEntry.insert(0, listdata[3])
    addressEntry.insert(0, listdata[4])
    genderEntry.insert(0, listdata[5])
    dobEntry.insert(0, listdata[6])





def show_student():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def delete_student():
    indexing=studentTable.focus()
    print(indexing)
    content=studentTable.item(indexing)
    content_id=content['values'][0]
    query='delete from student where id=%s'
    mycursor.execute(query,(content_id,))
    con.commit()
    messagebox.showinfo('Deleted',f'This {content_id} is deleted successfully')
    query='select * from student'
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('',END,values=data)



def search_student():
    def search_data():
        query = "SELECT * FROM student WHERE 1=1"
        params = []

        # Check if an ID is provided and add to the query
        if idEntry.get():
            query += " AND id=%s"
            params.append(idEntry.get())

        # Check if a Name is provided and add to the query
        if nameEntry.get():
            query += " AND name=%s"
            params.append(nameEntry.get())

        if EmailEntry.get():
            query += " AND email=%s"
            params.append(EmailEntry.get())
        if phoneEntry.get():
            query += " AND mobiles=%s"
            params.append(phoneEntry.get())
        if addressEntry.get():
            query += " AND address=%s"
            params.append(addressEntry.get())

        if genderEntry.get():
            query += " AND gender=%s"
            params.append(genderEntry.get())
        if dobEntry.get():
            query += " AND dob=%s"
            params.append(dobEntry.get())
        # Execute the query only if there are parameters
        if params:
            mycursor.execute(query, tuple(params))
            studentTable.delete(*studentTable.get_children())  # Clear existing rows in the table
            fetched_data = mycursor.fetchall()
            for data in fetched_data:
                studentTable.insert('', END, values=data)
        else:
            # Handle case where no search criteria are provided
            messagebox.showwarning("Input Error", "Please enter either an ID or Name to search.")

    # Create the search window
    search_window = Toplevel()
    search_window.resizable(False, False)
    search_window.title('Search Student')

    # ID Entry
    idLabel = Label(search_window, text='Id', font=('times new roman', 20, 'bold'))
    idLabel.grid(row=0, column=0)
    idEntry = Entry(search_window, font=('roman', 15, 'bold'))
    idEntry.grid(row=0, column=1)

    # Name Entry
    nameLabel = Label(search_window, text='Name', font=('times new roman', 20, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=15, sticky=W)
    nameEntry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
    nameEntry.grid(row=1, column=1, pady=15, padx=10)

    # Unused fields (can be removed if not needed in the UI)
    phoneLabel = Label(search_window, text='Phone', font=('times new roman', 20, 'bold'))
    phoneLabel.grid(row=2, column=0, padx=30, pady=15, sticky=W)
    phoneEntry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
    phoneEntry.grid(row=2, column=1, pady=15, padx=10)

    EmailLabel = Label(search_window, text='Email', font=('times new roman', 20, 'bold'))
    EmailLabel.grid(row=3, column=0, padx=30, pady=15, sticky=W)
    EmailEntry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
    EmailEntry.grid(row=3, column=1, pady=15, padx=10)

    addressLabel = Label(search_window, text='Address', font=('times new roman', 20, 'bold'))
    addressLabel.grid(row=4, column=0, padx=30, pady=15, sticky=W)
    addressEntry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
    addressEntry.grid(row=4, column=1, pady=15, padx=10)

    genderLabel = Label(search_window, text='Gender', font=('times new roman', 20, 'bold'))
    genderLabel.grid(row=5, column=0, padx=30, pady=15, sticky=W)
    genderEntry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
    genderEntry.grid(row=5, column=1, pady=15, padx=10)

    dobLabel = Label(search_window, text='D.O.B', font=('times new roman', 20, 'bold'))
    dobLabel.grid(row=6, column=0, padx=30, pady=15, sticky=W)
    dobEntry = Entry(search_window, font=('roman', 15, 'bold'), width=24)
    dobEntry.grid(row=6, column=1, pady=15, padx=10)

    # Search Button
    search_student_button = ttk.Button(search_window, text='SEARCH', command=search_data)
    search_student_button.grid(row=7, columnspan=2, pady=15)


# Function to add a student
def add_student():
    def add_data():

        # Check if any fields are empty
        if not all([idEntry.get(), nameEntry.get(), phoneEntry.get(), EmailEntry.get(), addressEntry.get(),
                    genderEntry.get(), dobEntry.get()]):
            messagebox.showerror('Error', 'All fields are required', parent=add_window)
        else:
            # Insert data into the database
            current_date = time.strftime('%d/%m/%Y')
            current_time = time.strftime('%H:%M:%S')
            query = 'INSERT INTO student (id, name, mobile, email, address, gender, dob, date, time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
            try:
                mycursor.execute(query, (
                    idEntry.get(), nameEntry.get(), phoneEntry.get(), EmailEntry.get(), addressEntry.get(),
                    genderEntry.get(), dobEntry.get(), current_date, current_time
                ))
                con.commit()
                result = messagebox.askyesno('Confirm', 'Data added successfully. Do you want to clear the form?',
                                             parent=add_window)
                if result:
                    idEntry.delete(0, END)
                    nameEntry.delete(0, END)
                    phoneEntry.delete(0, END)
                    EmailEntry.delete(0, END)
                    addressEntry.delete(0, END)
                    genderEntry.delete(0, END)
                    dobEntry.delete(0, END)
            except Exception as e:
                messagebox.showerror('Error', f'Failed to add data: {e}', parent=add_window)
                return
            query='select * from student'
            mycursor.execute(query)
            fetched_data=mycursor.fetchall()
            studentTable.delete(*studentTable.get_children())
            for data in fetched_data:
                dataList=list(data)
                studentTable.insert('',END,values=dataList)


    # Create add student window
    add_window = Toplevel()
    add_window.resizable(False, False)
    add_window.grab_set()

    # Define labels and entries for student data
    fields = ['Id', 'Name', 'Phone', 'Email', 'Address', 'Gender', 'D.O.B']
    entries = []
    for i, field in enumerate(fields):
        label = Label(add_window, text=field, font=('times new roman', 20, 'bold'))
        label.grid(row=i, column=0, padx=30, pady=15, sticky=W)
        entry = Entry(add_window, font=('roman', 15, 'bold'), width=24)
        entry.grid(row=i, column=1, pady=15, padx=10)
        entries.append(entry)

    # Map entries to their corresponding variables
    idEntry, nameEntry, phoneEntry, EmailEntry, addressEntry, genderEntry, dobEntry = entries

    add_student_button = ttk.Button(add_window, text='SUBMIT', command=add_data)
    add_student_button.grid(row=len(fields), columnspan=2, pady=15)


# Function to connect to the database
def connect_database():
    def connect():
        global con, mycursor
        try:
            # Connect to the MySQL server
            con = pymysql.connect(host=hostEntry.get(), user=usernameEntry.get(), password=passwordEntry.get())
            mycursor = con.cursor()
            messagebox.showinfo('Success', 'Database Connection is successful', parent=connectWindow)

            # Create database and table if not exist
            mycursor.execute('CREATE DATABASE IF NOT EXISTS studentmanagementsystem')
            mycursor.execute('USE studentmanagementsystem')
            mycursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS student (
                    id INT PRIMARY KEY,
                    name VARCHAR(30),
                    mobile VARCHAR(10),
                    email VARCHAR(30),
                    address VARCHAR(100),
                    gender VARCHAR(20),
                    dob VARCHAR(20),
                    date VARCHAR(50),
                    time VARCHAR(50)
                )
                '''
            )
            con.commit()

            # Enable buttons after successful connection
            addstudentButton.config(state=NORMAL)
            searchstudentButton.config(state=NORMAL)
            updatestudentButton.config(state=NORMAL)
            deletestudentButton.config(state=NORMAL)
            showstudentButton.config(state=NORMAL)


            connectWindow.destroy()
        except Exception as e:
            messagebox.showerror('Error', f'Failed to connect: {e}', parent=connectWindow)



    # Create a connection window
    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0, 0)

    # Labels and entries for connection details
    labels = ['Host Name', 'User Name', 'Password']
    entries = []
    for i, label_text in enumerate(labels):
        label = Label(connectWindow, text=label_text, font=('arial', 20, 'bold'))
        label.grid(row=i, column=0)
        entry = Entry(connectWindow, font=('roman', 15, 'bold'), bd=2)
        entry.grid(row=i, column=1, padx=40, pady=20)
        entries.append(entry)

    # Map entries to variables
    hostEntry, usernameEntry, passwordEntry = entries

    connectButton = ttk.Button(connectWindow, text='CONNECT', command=connect)
    connectButton.grid(row=3, columnspan=2)
count = 0
text = ''

# Slider and Clock functions
def slider():
    global text, count
    if count == len(s):
        count = 0
        text = ''
    text = text + s[count]
    sliderLabel.config(text=text)
    count += 1
    sliderLabel.after(100, slider)


# Functionality Part
def clock():
    global current_date, current_time
    current_date = time.strftime('%d/%m/%Y')
    current_time = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'Date: {current_date}\nTime: {current_time}')
    datetimeLabel.after(1000, clock)


root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.geometry('1174x680+0+0')
root.resizable(False, False)
root.title('Student Management System')

# Corrected Label variable name
datetimeLabel = Label(root, text='', font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=5, y=5)

clock()
s = 'Student Management System '
sliderLabel = Label(root, text=s, font=('arial', 28, 'italic bold'), width=30)
sliderLabel.place(x=200, y=0)
slider()

connectButton = ttk.Button(root, text='Connect database', command=connect_database)
connectButton.place(x=980, y=0)
leftFrame = Frame(root)
leftFrame.place(x=50, y=80, width=300, height=800)

logo_image = PhotoImage(file='student (1).png')
logo_Label = Label(leftFrame, image=logo_image)
logo_Label.grid(row=0, column=0)

addstudentButton = ttk.Button(leftFrame, text='Add Student', width=25, command=add_student)
addstudentButton.grid(row=1, column=0, pady=20)

searchstudentButton = ttk.Button(leftFrame, text='Search Student', width=25,command=search_student)
searchstudentButton.grid(row=2, column=0, pady=20)

deletestudentButton = ttk.Button(leftFrame, text='Delete Student', width=25,command=delete_student)
deletestudentButton.grid(row=3, column=0, pady=20)

updatestudentButton = ttk.Button(leftFrame, text='Update Student', width=25,command=update_student)
updatestudentButton.grid(row=4, column=0, pady=20)

showstudentButton = ttk.Button(leftFrame, text='Show Student', width=25,command=show_student)
showstudentButton.grid(row=5, column=0, pady=20)



exitstudentButton = ttk.Button(leftFrame, text='Exit', width=25,command=iexit)
exitstudentButton.grid(row=7, column=0, pady=20)

rightFrame = Frame(root)
rightFrame.place(x=350, y=80, width=820, height=600)

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

studentTable = ttk.Treeview(rightFrame, columns=(
'Id', 'Name', 'Mobile', 'Email', 'Address', 'Gender', 'D.O.B', 'Added Date', 'Added Time'),
                            xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)
scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)
studentTable.pack(fill=BOTH, expand=1)
studentTable.heading('Id', text='Id')
studentTable.heading('Name', text='Name')
studentTable.heading('Mobile', text='Mobile No')
studentTable.heading('Email', text='Email Address')
studentTable.heading('Address', text='Address')

studentTable.heading('Gender', text='Gender')
studentTable.heading('D.O.B', text='D.O.B')
studentTable.heading('Added Date', text='Added Date')
studentTable.heading('Added Time', text='Added Time')

studentTable.column('Id',width=50,anchor=CENTER)
studentTable.column('Name',width=300,anchor=CENTER)
studentTable.column('Email',width=300,anchor=CENTER)
studentTable.column('Mobile',width=200,anchor=CENTER)
studentTable.column('Address',width=300,anchor=CENTER)
studentTable.column('Gender',width=100,anchor=CENTER)
studentTable.column('D.O.B',width=100,anchor=CENTER)
studentTable.column('Added Date',width=200,anchor=CENTER)
studentTable.column('Added Time',width=200,anchor=CENTER)
studentTable.config(show='headings')

style=ttk.Style()
style.configure('Treeview',rowheight=40,font=('arial',12,'bold'),foreground='black',fieldbackgroun='white')
style.configure('Treeview.Heading',font=('arial',14,'bold'),foreground='green')
root.mainloop()
