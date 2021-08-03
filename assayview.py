from tkinter import *  
from tkinter import ttk
from tkinter.font import BOLD
from tkcalendar import DateEntry
from ttkthemes import ThemedTk
import datetime
import mysql.connector
import hashlib
import socket

today = datetime.date.today()
now = datetime.datetime.now()
tableoneselected = []

root = ThemedTk(theme="radiance")
root.title("Assayview")
root.state('zoomed')
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

assaydb = mysql.connector.connect(
          host = socket.gethostbyname("brightness"),
          user = "view1",
          passwd = "Assay123!",
          database="assay",
          autocommit = True
        )

mycursor = assaydb.cursor()

def changewindow():
  changewindow = Toplevel(root)
  changewindow.grab_set()
  changewindow.geometry('+500+140')
  def submitchange():
    #update record using id
    sql = "UPDATE assayresult SET returndate = %s, modified = %s WHERE id = %s"
    val = (date_cal.get_date(), now, tableoneselected[7])
    mycursor.execute(sql, val)
    assaydb.commit()
    for child in tableone.get_children(): #child = iid
      if formcode_label.cget("text") == str(tableone.item(child)['values'][1]):
        tableone.set(child, 5, date_cal.get_date().strftime("%d-%m-%Y %H:%M:%S"))
    changewindow.destroy()
  # frame for date
  date_frame = ttk.Frame(changewindow)
  date_frame.grid(column = 0,  row = 4, pady = (10,0))
  ttk.Label(date_frame, text='Date', font=("Helvetica", 16)).pack()
  date_cal = DateEntry(date_frame, justify= CENTER, font=("Helvetica", 14), width=15, background='darkblue', foreground='white', date_pattern = 'dd-mm-y', maxdate= today, showothermonthdays = False, showweeknumbers = False, weekendbackground = '#DCDCDC')
  date_cal.pack(padx=5, pady=5)
  ttk.Button(changewindow, text="Save", command=submitchange, style="buttonstyle.TButton", width = 10).grid(column = 0,  row = 5, pady = (10,0))

def changedate():
  root.after(1, changewindow)

rcm = Menu(root, tearoff = 0, font=('Calibri', 14))
rcm.add_command(label ="Edit Date", command = changedate)

def rightclickmenu(event):
  # select row under mouse
  iid = tableone.identify_row(event.y)
  if iid:
    # mouse pointer over item
    tableone.focus(iid)
    tableone.selection_set(iid)
    rcm.tk_popup(event.x_root, event.y_root)  

if (screen_width/screen_height) == (1920/1080):
  #Font Style for Treeviews
  style = ttk.Style()
  style.configure("mystyle.Treeview", font=('Calibri', 18, 'bold'), rowheight=30) # Modify the font of the body
  style.configure("mystyle.Treeview.Heading", font=('Calibri', 17,'bold')) # Modify the font of the headings
  style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
  #Font Style for Buttons
  buttonstyle = ttk.Style()
  buttonstyle.configure('buttonstyle.TButton', font=('Helvetica', 15, 'bold'))
elif (screen_width/screen_height) == (1366/768):
  #Font Style for Treeviews
  style = ttk.Style()
  style.configure("mystyle.Treeview", font=('Calibri', 16, 'bold'), rowheight=30) # Modify the font of the body
  style.configure("mystyle.Treeview.Heading", font=('Calibri', 15, 'bold')) # Modify the font of the headings
  style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
  #Font Style for Buttons
  buttonstyle = ttk.Style()
  buttonstyle.configure('buttonstyle.TButton', font=('Helvetica', 14, 'bold'))

def loginwindow():
  def wrongpassword():
    wrongpassword = Toplevel(loginwindow)
    wrongpassword.grab_set()
    wrongpassword.geometry('+610+290')
    ttk.Label(wrongpassword,  text ="Username or password is invalid.").grid(column = 0,  row = 0, pady = (20,0), padx = 20)
    wrongok = ttk.Button(wrongpassword, text = 'Ok', command = wrongpassword.destroy)
    wrongok.grid(column = 0,  row = 1, pady = (10,0))

  def login(event=None):
    mycursor.execute("SELECT email, pwhash, salt FROM user WHERE role = 'admin' OR role = 'boss' OR role = 'worker' ORDER BY role ASC")
    dbresult = mycursor.fetchall()
    admin = dbresult[0]
    boss = dbresult[1]
    worker = dbresult[2]
    if username_entry.get() == admin[0]:
      #get the salt and check is the password correct or not
      currentpwhash = admin[1]
      currentsalt = admin[2]
      check_pwhash = hashlib.pbkdf2_hmac('sha256', pw_entry.get().encode('utf8'), currentsalt, 100000)
      global loginperson
      #'global' to enable change on global var
      if currentpwhash == check_pwhash: #pw is correct
        loginwindow.destroy() #Removes the toplevel window
        root.deiconify() #Unhides the root window
        root.state('zoomed')
        loginperson = "admin"
        # Create Menu After Login#
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=filemenu)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        root.config(menu=menubar)
      else:
        #pw is wrong
        root.after(1, wrongpassword)
    elif username_entry.get() == boss[0]:
      #get the salt and check is the password correct or not
      currentpwhash = boss[1]
      currentsalt = boss[2]
      check_pwhash = hashlib.pbkdf2_hmac('sha256', pw_entry.get().encode('utf8'), currentsalt, 100000)
      if currentpwhash == check_pwhash: #pw is correct
        loginwindow.destroy() #Removes the toplevel window
        root.deiconify() #Unhides the root window
        root.state('zoomed')
        loginperson = "boss" 
        # Create Menu After Login#
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=filemenu)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        root.config(menu=menubar)
      else:
        #pw is wrong
        root.after(1, wrongpassword)
    elif username_entry.get() == worker[0]:
      #get the salt and check is the password correct or not
      currentpwhash = worker[1]
      currentsalt = worker[2]
      check_pwhash = hashlib.pbkdf2_hmac('sha256', pw_entry.get().encode('utf8'), currentsalt, 100000)
      if currentpwhash == check_pwhash: #pw is correct
        loginwindow.destroy() #Removes the toplevel window
        root.deiconify() #Unhides the root window
        root.state('zoomed')
        loginperson = "worker"
        # Create Menu After Login#
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=filemenu)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)
        root.config(menu=menubar)
      else:
        #pw is wrong
        root.after(1, wrongpassword)
    else:
      #wrong username
      root.after(1, wrongpassword)

  def closeprogram():
    loginwindow.destroy() #Removes the toplevel window
    root.destroy() #Removes the hidden root window

  loginwindow = Toplevel(root)
  loginwindow.title('Login')
  loginwindow.geometry('+600+280')
  def event_X():
    loginwindow.destroy() #Removes the toplevel window
    root.destroy() #Removes the hidden root window
  loginwindow.protocol("WM_DELETE_WINDOW",event_X) #assign action when 'x' is clicked
  loginentry_frame = ttk.Frame(loginwindow)
  loginentry_frame.grid(column = 0, row = 0, pady = (20,10), padx = 20)
  ttk.Label(loginentry_frame, text ="Username: ").grid(column = 0,  row = 0)
  username_entry = ttk.Entry(loginentry_frame) #Username entry
  username_entry.grid(column = 1, row = 0)
  ttk.Label(loginentry_frame, text ="Password: ").grid(column = 0,  row = 1)
  pw_entry = ttk.Entry(loginentry_frame, show = "*") #Password entry
  pw_entry.grid(column = 1, row = 1)
  pw_entry.bind('<Return>', login)
  loginbutton_frame = ttk.Frame(loginwindow)
  loginbutton_frame.grid(column = 0, row = 1, pady = (0,10), padx = 20)
  login_button = ttk.Button(loginbutton_frame, text="Login", command=lambda:login()) #Login button
  login_button.grid(column = 0, row = 0)
  cancel_button = ttk.Button(loginbutton_frame, text="Cancel", command=lambda:closeprogram()) #Cancel button
  cancel_button.grid(column = 1, row = 0)
  
  mycursor.execute("SELECT email FROM user WHERE role = 'worker'")
  usernameresult = mycursor.fetchall()
  if usernameresult[0][0]:
    username_entry.insert(0, usernameresult[0][0])
  loginwindow.focus_set()
  if username_entry.get():
    pw_entry.focus_set()
  else:
    username_entry.focus_set()

# Function for checking the key pressed and updating the listbox 
def checkkey(event): 
  if event.keysym=='Down':
    lbsearch.focus_set()
    lbsearch.select_set(0) #This only sets focus on the first item.
    lbsearch.event_generate("<<ListboxSelect>>")
  else:
    value = event.widget.get() 
    # get data from clsearch 
    if value == '': 
      data = clsearch
      update(data)
      lbsearch.pack_forget()
    else: 
      data = [] 
      for item in clsearch: 
        if value.lower() in item.lower(): 
          data.append(item)
          update(data)
          lbsearch.pack()
def update(data): 
  # clear previous data 
  lbsearch.delete(0, 'end') 
  # put new data 
  for item in data:
    lbsearch.insert('end', item) 
def selectcustomer(event):
  selection = event.widget.curselection()
  lbsearch.pack_forget()
  if selection:
      index = selection[0]
      customersearch.set(event.widget.get(index))
      customersearch_entry.focus_set()
def submitsearch():
  if customersearch_entry.get():
    sql = "SELECT assayresult.created AS created, assayresult.formcode AS formcode, user.name AS customer, assayresult.returndate AS returndate, assayresult.collector AS collector, assayresult.incharge AS incharge, assayresult.id AS id FROM assayresult INNER JOIN user ON assayresult.customer = user.id WHERE user.name LIKE %s and assayresult.created >= %s and assayresult.created <= %s ORDER BY assayresult.formcode, assayresult.created"
    val = (customersearch_entry.get(), start_cal.get_date(), end_cal.get_date()+ datetime.timedelta(days=1))
    mycursor.execute(sql, val)
    tableoneresult = mycursor.fetchall()
  else:
    sql = "SELECT assayresult.created AS created, assayresult.formcode AS formcode, user.name AS customer, assayresult.returndate AS returndate, assayresult.collector AS collector, assayresult.incharge AS incharge, assayresult.id AS id FROM assayresult INNER JOIN user ON assayresult.customer = user.id WHERE assayresult.created >= %s and assayresult.created <= %s ORDER BY assayresult.formcode, assayresult.created"
    val = (start_cal.get_date(), end_cal.get_date()+ datetime.timedelta(days=1))
    mycursor.execute(sql, val)
    tableoneresult = mycursor.fetchall()
  tableonedata = []
  for x in tableoneresult:
    newx = list(x) #convert tuple to list for modification
    #calculate and insert number of item in a formcode
    if tableonedata:
      if newx[1] == tableonedata[-1][1]:
        tableonedata[-1][2] += 1
      else:
        newx.insert(2,int(1))
        newx[0] = newx[0].strftime("%d/%m/%Y")
        tableonedata.append(newx)
    else:
      newx.insert(2,int(1))
      newx[0] = newx[0].strftime("%d/%m/%Y")
      tableonedata.append(newx)
  #convert potential "None" to ""
  for x in tableonedata:
    if not x[4]:
      x[4] = ""
    if not x[5]:
      x[5] = ""
    if not x[6]:
      x[6] = ""
  for i in tableone.get_children():
    tableone.delete(i)
  for record in tableonedata:
    tableone.insert("", 'end', text = "L1", iid = record[7], values = record, tags = ("normal"))
  tableone.tag_configure('normal', background='white')
def displayandloaditem(a):
  #display selected item
  curItem = tableone.focus()
  global tableoneselected
  tableoneselected = tableone.item(curItem).get('values')
  displayfc.set(tableoneselected[1])
  displayc.set(tableoneselected[3])
  displaycollector.set(tableoneselected[5])
  displayincharge.set(tableoneselected[6])
  if tableoneselected[5] == "" or tableoneselected[6] == "":
    collector_entry.focus_set()

  #load item to tabletwo
  mycursor.execute(f"SELECT assayresult.formcode AS formcode, user.name AS customer, assayresult.itemcode AS itemcode, assayresult.sampleweight AS sampleweight, assayresult.samplereturn AS samplereturn, assayresult.finalresult AS finalresult, assayresult.id AS id FROM assayresult INNER JOIN user ON assayresult.customer = user.id WHERE assayresult.formcode = '{tableoneselected[1]}' ORDER BY assayresult.created")
  tabletworesult = mycursor.fetchall()
  tabletwodata = list(tabletworesult)
  for i in tabletwo.get_children():
    tabletwo.delete(i)
  for record in tabletwodata:
    recordlist = list(record)
    if not recordlist[4]:
      recordlist[4] = ""
    if recordlist[5] == -1:
      recordlist[5] = "Reject"
      tabletwo.insert("", 'end', text = "L1", iid = recordlist[6], values = recordlist, tags = ("reject"))
    elif recordlist[5] == -2:
      recordlist[5] = "Redo"
      tabletwo.insert("", 'end', text = "L1", iid = recordlist[6], values = recordlist, tags = ("redo"))
    elif not recordlist[5]:
      recordlist[5] = ""
      tabletwo.insert("", 'end', text = "L1", iid = recordlist[6], values = recordlist, tags = ("normal"))
    else:
      tabletwo.insert("", 'end', text = "L1", iid = recordlist[6], values = recordlist, tags = ("normal"))
  tabletwo.tag_configure('normal', background='white')
  tabletwo.tag_configure('reject', foreground='red', background='white')
  tabletwo.tag_configure('redo', foreground='red', background='white')
def customercaps(*args):
  customersearch.set(customersearch.get().upper())
#get customer from db
mycursor.execute("SELECT * FROM user WHERE role ='customer'")
myresult = mycursor.fetchall()
clsearch = []
if myresult:
  for x in myresult:
    clsearch.append(x[8])
if (screen_width/screen_height) == (1920/1080):
  # frame for info
  filter_frame = ttk.Frame(root)
  filter_frame.grid(column = 0,  row = 0, sticky = N, padx = 10, rowspan=2)
  ttk.Label(filter_frame,  text ="Customer", font=("Helvetica", 16, BOLD)).grid(column = 0,  row = 0, padx = (5,0), pady = (5,0), sticky=W)
  # Combobox creation
  # create a frame 
  customer_input_frame = ttk.Frame(filter_frame)
  customer_input_frame.grid(column = 0,  row = 1)
  # If customer not in list, pop up add new customer fw_pct_frame
  customersearch = StringVar()
  customersearch.trace("w", customercaps)
  customersearch_entry = ttk.Entry(customer_input_frame, textvariable=customersearch, font=("Helvetica", 17))
  customersearch_entry.pack() 
  customersearch_entry.bind('<KeyRelease>', checkkey) 
  #creating list box 
  lbsearch = Listbox(customer_input_frame, font=("Helvetica", 16), height=5)
  lbsearch.pack()
  lbsearch.pack_forget()
  update(clsearch) 
  lbsearch.bind("<KeyRelease-Return>", selectcustomer)
  lbsearch.bind("<ButtonRelease-1>", selectcustomer)
  lbsearch.bind("<Double-Button-1>", selectcustomer)
  # frame for date
  date_frame = ttk.Frame(filter_frame)
  date_frame.grid(column = 0,  row = 4, pady = (10,0))
  ttk.Label(date_frame, text='Start date', font=("Helvetica", 17)).pack()
  start_cal = DateEntry(date_frame, justify= CENTER, font=("Helvetica", 15), width=16, background='darkblue', foreground='white', date_pattern = 'dd-mm-y', maxdate= today, showothermonthdays = False, showweeknumbers = False, weekendbackground = '#DCDCDC')
  start_cal.pack(padx=5, pady=5)
  ttk.Label(date_frame, text='End date', font=("Helvetica", 17)).pack()
  end_cal = DateEntry(date_frame, justify= CENTER, font=("Helvetica", 15), width=16, background='darkblue', foreground='white', date_pattern = 'dd-mm-y', maxdate= today, showothermonthdays = False, showweeknumbers = False, weekendbackground = '#DCDCDC')
  end_cal.pack(padx=5, pady=5)
  ttk.Button(filter_frame, text="Search", command=submitsearch, style="buttonstyle.TButton", width = 10).grid(column = 0,  row = 5, pady = (10,0))
elif (screen_width/screen_height) == (1366/768):
  # frame for info
  filter_frame = ttk.Frame(root)
  filter_frame.grid(column = 0,  row = 0, sticky = N, padx = 10, rowspan=2)
  ttk.Label(filter_frame,  text ="Customer", font=("Helvetica", 14, BOLD)).grid(column = 0,  row = 0, padx = (5,0), pady = (5,0), sticky=W)
  # Combobox creation
  # create a frame 
  customer_input_frame = ttk.Frame(filter_frame)
  customer_input_frame.grid(column = 0,  row = 1)
  # If customer not in list, pop up add new customer fw_pct_frame
  customersearch = StringVar()
  customersearch.trace("w", customercaps)
  customersearch_entry = ttk.Entry(customer_input_frame, textvariable=customersearch, font=("Helvetica", 14))
  customersearch_entry.pack() 
  customersearch_entry.bind('<KeyRelease>', checkkey) 
  #creating list box 
  lbsearch = Listbox(customer_input_frame, font=("Helvetica", 14), height=5)
  lbsearch.pack()
  lbsearch.pack_forget()
  update(clsearch) 
  lbsearch.bind("<KeyRelease-Return>", selectcustomer)
  lbsearch.bind("<ButtonRelease-1>", selectcustomer)
  lbsearch.bind("<Double-Button-1>", selectcustomer)
  # frame for date
  date_frame = ttk.Frame(filter_frame)
  date_frame.grid(column = 0,  row = 4, pady = (10,0))
  ttk.Label(date_frame, text='Start date', font=("Helvetica", 15)).pack()
  start_cal = DateEntry(date_frame, justify= CENTER, font=("Helvetica", 14), width=16, background='darkblue', foreground='white', date_pattern = 'dd-mm-y', maxdate= today, showothermonthdays = False, showweeknumbers = False, weekendbackground = '#DCDCDC')
  start_cal.pack(padx=5, pady=5)
  ttk.Label(date_frame, text='End date', font=("Helvetica", 15)).pack()
  end_cal = DateEntry(date_frame, justify= CENTER, font=("Helvetica", 14), width=16, background='darkblue', foreground='white', date_pattern = 'dd-mm-y', maxdate= today, showothermonthdays = False, showweeknumbers = False, weekendbackground = '#DCDCDC')
  end_cal.pack(padx=5, pady=5)
  ttk.Button(filter_frame, text="Search", command=submitsearch, style="buttonstyle.TButton", width = 10).grid(column = 0,  row = 5, pady = (10,0))

def savedata():
  sql = "UPDATE assayresult SET returndate = %s, collector = %s, incharge = %s, modified = %s WHERE formcode = %s"
  val = (now, collector_entry.get(), incharge_entry.get(), now, formcode_label.cget("text"))
  mycursor.execute(sql, val)
  assaydb.commit()
  for child in tableone.get_children(): #child = iid
    if formcode_label.cget("text") == str(tableone.item(child)['values'][1]):
      tableone.set(child, 5, now.strftime("%d-%m-%Y %H:%M:%S"))
      tableone.set(child, 6, collector_entry.get())
      tableone.set(child, 7, incharge_entry.get())
def focusincharge(e):
  incharge_entry.focus_set()
def displayinchargecaps(*args):
  displayincharge.set(displayincharge.get().upper())
def displaycollectorcaps(*args):
  displaycollector.set(displaycollector.get().upper())
if (screen_width/screen_height) == (1920/1080):
  #Display and edit frame
  display_frame = ttk.Frame(filter_frame)
  display_frame.grid(column = 0,  row = 6, pady = (20,0), padx = 10)
  ttk.Label(display_frame, text='Formcode', font=("Helvetica", 16, BOLD)).grid(column = 0,  row = 0, sticky=W, pady = (10,0))
  displayfc = StringVar() 
  formcode_label = ttk.Label(display_frame, textvariable = displayfc, font=("Helvetica", 17))
  formcode_label.grid(column = 0,  row = 1, sticky=W)
  ttk.Label(display_frame, text='Customer', font=("Helvetica", 16, BOLD)).grid(column = 0,  row = 2, sticky=W, pady = (10,0))
  displayc = StringVar()
  ttk.Entry(display_frame, textvariable = displayc, font=("Helvetica", 17), state=DISABLED).grid(column = 0,  row = 3, sticky=W)
  ttk.Label(display_frame, text='Collector', font=("Helvetica", 16, BOLD)).grid(column = 0,  row = 4, sticky=W, pady = (10,0))
  displaycollector = StringVar()
  displaycollector.trace("w", displayinchargecaps)
  collector_entry = ttk.Entry(display_frame, textvariable=displaycollector, font=("Helvetica", 17))
  collector_entry.grid(column = 0,  row = 5, sticky=W)
  collector_entry.bind('<Return>', focusincharge)
  ttk.Label(display_frame, text='In Charge', font=("Helvetica", 16, BOLD)).grid(column = 0,  row = 6, sticky=W, pady = (10,0))
  displayincharge = StringVar()
  displayincharge.trace("w", displaycollectorcaps)
  incharge_entry = ttk.Entry(display_frame, textvariable=displayincharge, font=("Helvetica", 17))
  incharge_entry.grid(column = 0,  row = 7, sticky=W)
  ttk.Button(display_frame, text="Save", command=savedata, style="buttonstyle.TButton", width = 8).grid(column = 0,  row = 8, pady = (10,0))

  # First Table
  tableone_frame = ttk.Frame(root)
  tableone_frame.grid(column = 1,  row = 0, pady = 20)
  # Constructing vertical scrollbar 
  tableone_scroll = ttk.Scrollbar(tableone_frame, orient ="vertical") 
  tableone_scroll.pack(side ='right', fill='y')
  # sh table # 
  tableone = ttk.Treeview(tableone_frame, style="mystyle.Treeview", selectmode ='browse', height = 10, yscrollcommand = tableone_scroll.set, columns = ("1", "2", "3", "4", "5", "6", "7"), show = 'headings') 
  tableone.pack(side ='left')
  # Configuring scrollbar 
  tableone_scroll.configure(command = tableone.yview) 
  # Assigning the width and anchor to the respective columns 
  tableone.column("1", width = 130, anchor ='c') 
  tableone.column("2", width = 100, anchor ='c') 
  tableone.column("3", width = 100, anchor ='c') 
  tableone.column("4", width = 280, anchor ='c') 
  tableone.column("5", width = 190, anchor ='c') 
  tableone.column("6", width = 140, anchor ='c')
  tableone.column("7", width = 140, anchor ='c') 
  # Assigning the heading names to the respective columns 
  tableone.heading("1", text ="Date") 
  tableone.heading("2", text ="Formcode")
  tableone.heading("3", text ="Number") 
  tableone.heading("4", text ="Customer")
  tableone.heading("5", text ="Return Date")
  tableone.heading("6", text ="Receiver")
  tableone.heading("7", text ="In Charge")
  tableone.bind('<<TreeviewSelect>>', displayandloaditem)
  tableone.bind("<Button-3>", rightclickmenu)

  # Second Table
  tabletwo_frame = ttk.Frame(root)
  tabletwo_frame.grid(column = 1,  row = 1, pady = 20)
  # Constructing vertical scrollbar 
  tabletwo_scroll = ttk.Scrollbar(tabletwo_frame, orient ="vertical") 
  tabletwo_scroll.pack(side ='right', fill='y')
  # sh table # 
  tabletwo = ttk.Treeview(tabletwo_frame, style="mystyle.Treeview", selectmode ='browse', height = 10, yscrollcommand = tabletwo_scroll.set, columns = ("1", "2", "3", "4", "5", "6"), show = 'headings') 
  tabletwo.pack(side ='left')
  # Configuring scrollbar 
  tabletwo_scroll.configure(command = tabletwo.yview) 
  # Assigning the width and anchor to the respective columns 
  tabletwo.column("1", width = 100, anchor ='c') 
  tabletwo.column("2", width = 280, anchor ='c') 
  tabletwo.column("3", width = 100, anchor ='c') 
  tabletwo.column("4", width = 100, anchor ='c') 
  tabletwo.column("5", width = 100, anchor ='c') 
  tabletwo.column("6", width = 100, anchor ='c')
  # Assigning the heading names to the respective columns 
  tabletwo.heading("1", text ="Formcode") 
  tabletwo.heading("2", text ="Customer")
  tabletwo.heading("3", text ="Itemcode") 
  tabletwo.heading("4", text ="Sample Weight")
  tabletwo.heading("5", text ="Sample Return")
  tabletwo.heading("6", text ="Result")
elif (screen_width/screen_height) == (1366/768):
  #Display and edit frame
  display_frame = ttk.Frame(filter_frame)
  display_frame.grid(column = 0,  row = 6, pady = (20,0), padx = 10)
  ttk.Label(display_frame, text='Formcode', font=("Helvetica", 15, BOLD)).grid(column = 0,  row = 0, sticky=W, pady = (10,0))
  displayfc = StringVar() 
  formcode_label = ttk.Label(display_frame, textvariable = displayfc, font=("Helvetica", 16))
  formcode_label.grid(column = 0,  row = 1, sticky=W)
  ttk.Label(display_frame, text='Customer', font=("Helvetica", 15, BOLD)).grid(column = 0,  row = 2, sticky=W, pady = (10,0))
  displayc = StringVar()
  ttk.Entry(display_frame, textvariable = displayc, font=("Helvetica", 16), state = DISABLED).grid(column = 0,  row = 3, sticky=W)
  ttk.Label(display_frame, text='Collector', font=("Helvetica", 15, BOLD)).grid(column = 0,  row = 4, sticky=W, pady = (10,0))
  displaycollector = StringVar()
  displaycollector.trace("w", displayinchargecaps)
  collector_entry = ttk.Entry(display_frame, textvariable=displaycollector, font=("Helvetica", 16))
  collector_entry.grid(column = 0,  row = 5, sticky=W)
  collector_entry.bind('<Return>', focusincharge)
  ttk.Label(display_frame, text='In Charge', font=("Helvetica", 15, BOLD)).grid(column = 0,  row = 6, sticky=W, pady = (10,0))
  displayincharge = StringVar()
  displayincharge.trace("w", displaycollectorcaps)
  incharge_entry = ttk.Entry(display_frame, textvariable=displayincharge, font=("Helvetica", 16))
  incharge_entry.grid(column = 0,  row = 7, sticky=W)
  ttk.Button(display_frame, text="Save", command=savedata, style="buttonstyle.TButton", width = 8).grid(column = 0,  row = 8, pady = (10,0))

  # First Table
  tableone_frame = ttk.Frame(root)
  tableone_frame.grid(column = 1,  row = 0, pady = (10,0))
  # Constructing vertical scrollbar 
  tableone_scroll = ttk.Scrollbar(tableone_frame, orient ="vertical") 
  tableone_scroll.pack(side ='right', fill='y')
  # sh table # 
  tableone = ttk.Treeview(tableone_frame, style="mystyle.Treeview", selectmode ='browse', height = 10, yscrollcommand = tableone_scroll.set, columns = ("1", "2", "3", "4", "5", "6", "7"), show = 'headings') 
  tableone.pack(side ='left')
  # Configuring scrollbar 
  tableone_scroll.configure(command = tableone.yview) 
  # Assigning the width and anchor to the respective columns 
  tableone.column("1", width = 130, anchor ='c') 
  tableone.column("2", width = 80, anchor ='c') 
  tableone.column("3", width = 60, anchor ='c') 
  tableone.column("4", width = 300, anchor ='c') 
  tableone.column("5", width = 200, anchor ='c') 
  tableone.column("6", width = 120, anchor ='c')
  tableone.column("7", width = 120, anchor ='c') 
  # Assigning the heading names to the respective columns 
  tableone.heading("1", text ="Date") 
  tableone.heading("2", text ="Formcode")
  tableone.heading("3", text ="No") 
  tableone.heading("4", text ="Customer")
  tableone.heading("5", text ="Return Date")
  tableone.heading("6", text ="Receiver")
  tableone.heading("7", text ="In Charge")
  tableone.bind('<<TreeviewSelect>>', displayandloaditem)

  # Second Table
  tabletwo_frame = ttk.Frame(root)
  tabletwo_frame.grid(column = 1,  row = 1, pady = (10,0))
  # Constructing vertical scrollbar 
  tabletwo_scroll = ttk.Scrollbar(tabletwo_frame, orient ="vertical") 
  tabletwo_scroll.pack(side ='right', fill='y')
  # sh table # 
  tabletwo = ttk.Treeview(tabletwo_frame, style="mystyle.Treeview", selectmode ='browse', height = 10, yscrollcommand = tabletwo_scroll.set, columns = ("1", "2", "3", "4", "5", "6"), show = 'headings') 
  tabletwo.pack(side ='left')
  # Configuring scrollbar 
  tabletwo_scroll.configure(command = tabletwo.yview) 
  # Assigning the width and anchor to the respective columns 
  tabletwo.column("1", width = 110, anchor ='c') 
  tabletwo.column("2", width = 300, anchor ='c') 
  tabletwo.column("3", width = 110, anchor ='c') 
  tabletwo.column("4", width = 110, anchor ='c') 
  tabletwo.column("5", width = 110, anchor ='c') 
  tabletwo.column("6", width = 110, anchor ='c')
  # Assigning the heading names to the respective columns 
  tabletwo.heading("1", text ="Formcode") 
  tabletwo.heading("2", text ="Customer")
  tabletwo.heading("3", text ="Itemcode") 
  tabletwo.heading("4", text ="Sample Weight")
  tabletwo.heading("5", text ="Sample Return")
  tabletwo.heading("6", text ="Result")

root.withdraw() #This hides the main window, it's still present it just can't be seen or interacted with
root.after(1, loginwindow) #opens loginwindow

timer = None
def userisinactive():
  root.withdraw()
  root.after(1, loginwindow)

def reset_timer(event=None):
  global timer
  # cancel the previous event
  if timer is not None:
    root.after_cancel(timer)

  # create new timer
  timer = root.after(10000, userisinactive)

root.bind_all('<Any-KeyPress>', reset_timer)
root.bind_all('<Any-ButtonPress>', reset_timer)
reset_timer()

root.mainloop()  