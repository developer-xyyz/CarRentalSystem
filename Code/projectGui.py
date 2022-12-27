from tkinter import *
from datetime import datetime
import mysql.connector

root = Tk()
root.title('Car Rental Project')
root.geometry("1200x700")

#connects to mysql server
def connect2MySQLDB():
    global db
    db = mysql.connector.connect(
        host="localhost",
        user="", #username of the mysql server
        passwd="", #password of the mysql server
        database="" #desired database that the program will query
    )    

    global my_cursor
    my_cursor = db.cursor()

connect2MySQLDB()
my_cursor.execute("SET SQL_SAFE_UPDATES = 0")

def countDays(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

#Adds new customer information
def submit():
    connect2MySQLDB()

    insrt = "INSERT INTO CUSTOMER(Name,Phone) values(%s,%s)"
    values=(C_name.get(),C_phone.get())

    my_cursor.execute(insrt,values)
    db.commit()
    
    C_name.delete(0,END)
    C_phone.delete(0,END)
    db.close()

#Adds new vehicle information
def submit2():
    connect2MySQLDB()
    
    insrt = "INSERT INTO VEHICLE(VehicleID,Description,Year,Type,Category) values(%s,%s,%s,%s,%s)"
    values=(V_id.get(),V_desc.get(),V_year.get(),V_type.get(),V_cat.get())

    my_cursor.execute(insrt,values)
    db.commit()
    
    V_id.delete(0,END)
    V_desc.delete(0,END)
    V_year.delete(0,END)
    V_type.delete(0,END)
    V_cat.delete(0,END)
    db.close()

#returns a car
def returnCar():
    connect2MySQLDB()
    query1="UPDATE RENTAL SET PaymentDate=%s WHERE ReturnDate=%s AND CustID=%s AND VehicleID=%s"
    values=(R_returndate.get(),R_returndate.get(),R_custID.get(),R_vehiD.get())
    my_cursor.execute(query1,values)
    db.commit()

    query2="UPDATE RENTAL SET Returned = 1 WHERE ReturnDate=%s AND CustID=%s AND VehicleID=%s"
    values2=(R_returndate.get(),R_custID.get(),R_vehiD.get())

    my_cursor.execute(query2,values2)
    db.commit()
    #print('success')
    returnRentalPage()
    
    db.close()

def returnCar2():
    connect2MySQLDB()

    query2="UPDATE RENTAL SET Returned = 1 WHERE ReturnDate=%s AND CustID=%s AND VehicleID=%s"
    values2=(R_returndate.get(),R_custID.get(),R_vehiD.get())

    my_cursor.execute(query2,values2)
    db.commit()
    #print('success')
    returnRentalPage()
    
    db.close()

#Queries return information to handle return of a car
def searchRental():
    connect2MySQLDB()
    
    query="SELECT CustID, VehicleID, StartDate, OrderDate, TotalAmount, PaymentDate FROM RENTAL WHERE ReturnDate=%s AND CustID=%s AND VehicleID=%s"
    values=(R_returndate.get(),R_custID.get(),R_vehiD.get())

    my_cursor.execute(query,values)
    
    print_balance = ''
    balance ='Amount due: $'
    paymentDate=''
    for line in my_cursor:
        paymentDate+=str(line[5])
        if(paymentDate=='None'):
            print_balance+= str(line[0]) +"            " + str(line[1]) + "    " + str(line[2]) + "     " + str(line[3]) + "     " + str(line[4]) + "               \n"
        else:
            print_balance+= str(line[0]) +"            " + str(line[1]) + "    " + str(line[2]) + "     " + str(line[3]) + "               " + "0" + "               \n"
        balance += str(line[4])
        
    rentalInfoLabel = Label(returnRental, text="Rental Information")
    rentalInfoLabel.place(x=20,y=300)
    
        
    formatLabel = Label(returnRental, text="CustID       VehicleID                          StartDate       OrderDate       Amount Due($)")
    formatLabel.place(x=20,y=330)

    rentalInfo = Label(returnRental,text=print_balance)
    rentalInfo.place(x=20,y=350)
    if(paymentDate=='None'):
        label1 = Label(returnRental,text=balance+". Pay and return now?", font=("Arial", 18))
        label1.place(x=20,y=450)

        payndreturn = Button(returnRental,text="Pay & Return",command=returnCar)
        payndreturn.place(x=20,y=480)
    else:
        label1 = Label(returnRental,text="Balance due: $0. Return now?", font=("Arial", 18))
        label1.place(x=20,y=450)

        payndreturn = Button(returnRental,text="Return",command=returnCar2)
        payndreturn.place(x=20,y=480)

    #R_returndate.delete(0,END)
    #R_custID.delete(0,END)
    #R_vehiD.delete(0,END)
    db.close()

#Queries all customers
def viewData():
    connect2MySQLDB()
    
    my_cursor.execute("SELECT * FROM CUSTOMER")
    records = my_cursor.fetchall()

    myList = Listbox(resultConsole)
    myList.config(width=900,height=400)
    print_records='{:^30} {:>15} {:>70}'.format('CustomerID', 'Name', 'Phone Number') 
    myList.insert(END, print_records + "\n")
    count=0
    for record in records:
        line_new = '{:^30} {:>25} {:>70}'.format(str(record[0]), str(record[1]), str(record[2]))     
        myList.insert(END, line_new + "\n")
        myList.config(font=('bold',20))
        count +=1
   
    myList.pack(side=LEFT,fill=BOTH)
    label = "Returned Result: " + str(count)
    cntLabel = Label(newCustomerFrame,text=label)
    cntLabel.place(x=770,y=270)
    db.close()

#queries all vehicles
def viewVehicleData():
    connect2MySQLDB()
    
    my_cursor.execute("SELECT * FROM VEHICLE")
    records = my_cursor.fetchall()

    myList = Listbox(resultConsole2)
    myList.config(width=900,height=400)
    print_records='{:^30} {:>45} {:>45} {:>45} {:>30}'.format('VehicleID', 'Description', 'Year', 'Type', 'Category') 
    myList.insert(END, print_records + "\n")
    count=0
    for record in records:
        line_new = '{:^35} {:>35} {:>35} {:>35} {:>35}'.format(str(record[0]), str(record[1]), str(record[2]), str(record[3]), str(record[4]))
        #print(line_new)
        myList.insert(END, line_new + "\n")
        myList.config(font=('bold',14))
        count+=1
    myList.pack(side=LEFT,fill=BOTH)
    label = "Returned Result: " + str(count)
    cntLabel = Label(newVehicleFrame,text=label)
    cntLabel.place(x=770,y=270)
    db.close()

#enters new rental with customer who made payment on the spot
def payNow():
    connect2MySQLDB()
    query="INSERT INTO RENTAL (CustID , VehicleID , StartDate, OrderDate, RentalType, Qty, ReturnDate, TotalAmount, PaymentDate, Returned) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values=(cust_id.get(), vehid.get(), R_Rstartdate.get(), order_date, str(rentalType), str(qty),R_Renddate.get(),str(paymentAmt), order_date,'0')
    my_cursor.execute(query,values)
    db.commit()
    db.close()
    newRentalPage()
    
#enters new rental with customer who wants to pay later
def payLater():
    connect2MySQLDB()
    query="INSERT INTO RENTAL (CustID , VehicleID , StartDate, OrderDate, RentalType, Qty, ReturnDate, TotalAmount, PaymentDate, Returned) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values=(cust_id.get(), vehid.get(), R_Rstartdate.get(), order_date, str(rentalType), str(qty),R_Renddate.get(),str(paymentAmt), None,'0')
    my_cursor.execute(query,values)
    db.commit()
    db.close()
    newRentalPage()

#calculuates payment for new rental
def submit3():
    connect2MySQLDB()
    global paymentAmt
    paymentAmt=0
    rate=0

    if(rentalType==7):
        query="SELECT Weekly from RATE JOIN VEHICLE ON RATE.Type=VEHICLE.Type AND RATE.Category=VEHICLE.Category WHERE VEHICLE.VehicleID=%s"
        my_cursor.execute(query,(vehid.get(), ))
        for line in my_cursor:
            rate = str(line[0])
        rate = int(rate)
    else:
        query="SELECT Daily from RATE JOIN VEHICLE ON RATE.Type=VEHICLE.Type AND RATE.Category=VEHICLE.Category WHERE VEHICLE.VehicleID=%s"
        my_cursor.execute(query,(vehid.get(), ))
        for line in my_cursor:
            rate = str(line[0])
        rate = int(rate)

    paymentAmt = rate * qty
    paymentText = "Your total is $" + str(paymentAmt) + " Pay now?"
    paymentLabel = Label(newRentalFrame,text=paymentText,font=("Arial", 25))
    paymentLabel.place(x=400, y=300)

    yes_btn=Button(newRentalFrame,text="Yes",command=payNow)
    yes_btn.place(x=400,y=340)

    no_btn=Button(newRentalFrame,text="No",command=payLater)
    no_btn.place(x=460,y=340)
    db.close()

#queries for available car for rental
def searchAvailableCars():
    connect2MySQLDB()
    query="select * from vehicle where VehicleID not in (select VehicleID from rental  where StartDate >= %s and ReturnDate <= %s)"
    values=(R_Rstartdate.get(),R_Renddate.get())

    my_cursor.execute(query,values)
    records = my_cursor.fetchall()

    myList = Listbox(availableCarsConsole)
    myList.config(width=900,height=200)
    print_records='{:^35} {:>40} '.format('VehicleID', 'Description')
    myList.insert(END,print_records + "\n")
    count=0
    for record in records:
        line_new = '{:^35} {:>35} '.format(str(record[0]), str(record[1]))
        myList.insert(END, line_new + "\n")
        myList.config(font=('bold',20))
        count+=1
    
    myList.pack(side=LEFT,fill=BOTH)
    label = "Returned Result: " + str(count)
    cntLabel = Label(newRentalFrame,text=label)
    cntLabel.place(x=770,y=470)
    label =Label(newRentalFrame, text="Select a vehicle from the following available vehicles and copy the Vehicle ID")
    label.place(x=0, y=470)

    custid_label=Label(newRentalFrame,text="Enter Your Customer ID")
    custid_label.place(x=20,y=200)
    global cust_id
    cust_id=Entry(newRentalFrame,width=10)
    cust_id.place(x=20,y=230)
    vehid_label=Label(newRentalFrame,text="Enter Vehicle ID")
    vehid_label.place(x=20,y=270)
    global vehid
    vehid=Entry(newRentalFrame,width=25)
    vehid.place(x=20,y=300)
    global order_date
    order_date = datetime.today().strftime('%Y-%m-%d')
    duration=countDays(R_Rstartdate.get(),R_Renddate.get())
    global rentalType
    global qty
    rentalType=0
    qty=0
    if(duration %7 ==0):
        rentalType=7
        qty=duration/7
    else:
        rentalType=1
        qty=duration/1
    qty = int(qty)
    #print(str(rentalType) + " " + str(qty))
    submit_btn = Button(newRentalFrame,text="Submit",command=submit3)
    submit_btn.place(x=20,y=340)
    db.close()

#customer's view's result
def searchCustView():
    connect2MySQLDB()

    if(views_custID.get() != ""):
        query="select CustomerID , CustomerName , SUM(RentalBalance) AS RentalBalance FROM vrentalinfo WHERE CustomerID=%s GROUP BY CustomerID ORDER BY RentalBalance"
        my_cursor.execute(query,(views_custID.get(), ))
        myList = Listbox(custViewsConsole)
        myList.config(width=900,height=320)
        print_records='{:^35} {:>25} {:>35}'.format('CustomerID','Name', 'Balance')
        myList.insert(END, print_records+ "\n")
        count=0
        for line in my_cursor:
            line_new = '{:^35} {:>35} {:>35}'.format(str(line[0]), str(line[1]),'$'+str(line[2]))
            myList.insert(END, line_new+ "\n")
            myList.config(font=('bold',20))
            count+=1

        myList.pack(side=LEFT,fill=BOTH)
        label = "Returned Result: " + str(count)
        cntLabel = Label(custPage,text=label)
        cntLabel.place(x=770,y=350)
        
    elif(views_fullname.get() != ""):
        query="select CustomerID , CustomerName , SUM(RentalBalance) AS RentalBalance FROM vrentalinfo WHERE CustomerName =%s GROUP BY CustomerID ORDER BY RentalBalance"
        my_cursor.execute(query,(views_fullname.get(), ))
        myList = Listbox(custViewsConsole)
        myList.config(width=900,height=320)
        print_records='{:^35} {:>25} {:>35}'.format('CustomerID','Name', 'Balance')
        myList.insert(END, print_records+ "\n")
        count=0
        for line in my_cursor:
            line_new = '{:^35} {:>35} {:>35}'.format(str(line[0]), str(line[1]),'$'+str(line[2]))
            myList.insert(END, line_new+ "\n")
            myList.config(font=('bold',20))
            count+=1
        myList.pack(side=LEFT,fill=BOTH)
        label = "Returned Result: " + str(count)
        cntLabel = Label(custPage,text=label)
        cntLabel.place(x=770,y=350)

    elif(views_partialname.get()!=""):
        query="select CustomerID , CustomerName , SUM(RentalBalance) AS RentalBalance FROM vrentalinfo WHERE LOWER(CustomerName)  REGEXP  %s GROUP BY CustomerID ORDER BY RentalBalance"
        regex = "^.*" + views_partialname.get() + "*"
        my_cursor.execute(query,(regex, ))
        myList = Listbox(custViewsConsole)
        myList.config(width=900,height=320)
        print_records='{:^35} {:>25} {:>35}'.format('CustomerID','Name', 'Balance')
        myList.insert(END, print_records+ "\n")
        count=0
        for line in my_cursor:
            line_new = '{:^35} {:>35} {:>35}'.format(str(line[0]), str(line[1]),'$'+str(line[2]))
            myList.insert(END, line_new+ "\n")
            myList.config(font=('bold',20))
            count+=1
        myList.pack(side=LEFT,fill=BOTH)
        label = "Returned Result: " + str(count)
        cntLabel = Label(custPage,text=label)
        cntLabel.place(x=770,y=350)

    else:
        query="select CustomerID ,CustomerName , Sum(RentalBalance) AS RentalBalance FROM vrentalinfo  GROUP BY CustomerID ORDER BY RentalBalance"
        my_cursor.execute(query)
        myList = Listbox(custViewsConsole)
        myList.config(width=900,height=320)
        print_records='{:^35} {:>25} {:>35}'.format('CustomerID','Name', 'Balance')
        myList.insert(END, print_records+ "\n")
        count=0
        for line in my_cursor:
            line_new = '{:^35} {:>35} {:>35}'.format(str(line[0]), str(line[1]),'$'+str(line[2]))
            myList.insert(END, line_new+ "\n")
            myList.config(font=('bold',20))
            count+=1
        
        myList.pack(side=LEFT,fill=BOTH)
        label = "Returned Result: " + str(count)
        cntLabel = Label(custPage,text=label)
        cntLabel.place(x=770,y=350)
    db.close()

#vehicle's view's result
def searchVehicleView():
    connect2MySQLDB()

    if(views_vehicleID.get() != ""):
        query="SELECT VIN , VEHICLE , AVG(OrderAmount/TotalDays) AS AverageDailyPrice FROM vrentalinfo WHERE VIN =%s GROUP BY VIN  ORDER BY AverageDailyPrice"
        my_cursor.execute(query,(views_vehicleID.get(), ))
        myList = Listbox(vehViewsConsole)
        myList.config(width=900,height=320)
        print_records='{:^35} {:>45} {:>65}'.format('VehicleID','Description', 'Average Daily Price')
        myList.insert(END, print_records+ "\n")
        count=0
        for line in my_cursor:
            num = float(line[2])
            num = round(num,2)
            line_new = '{:^35} {:>35} {:>45}'.format(str(line[0]), str(line[1]),'$'+str(num))
            myList.insert(END, line_new+ "\n")
            myList.config(font=('bold',20))
            count+=1
        myList.pack(side=LEFT,fill=BOTH)
        label = "Returned Result: " + str(count)
        cntLabel = Label(vehcPage,text=label)
        cntLabel.place(x=770,y=350)

    elif(views_carname.get() != ""):
        query="SELECT VIN , VEHICLE , AVG(OrderAmount/TotalDays) AS AverageDailyPrice FROM vrentalinfo WHERE VEHICLE =%s GROUP BY VIN  ORDER BY AverageDailyPrice"
        my_cursor.execute(query,(views_carname.get(), ))
        myList = Listbox(vehViewsConsole)
        myList.config(width=900,height=320)
        print_records='{:^35} {:>45} {:>65}'.format('VehicleID','Description', 'Average Daily Price')
        myList.insert(END, print_records+ "\n")
        count=0
        for line in my_cursor:
            num = float(line[2])
            num = round(num,2)
            line_new = '{:^35} {:>35} {:>45}'.format(str(line[0]), str(line[1]),'$'+str(num))
            myList.insert(END, line_new+ "\n")
            myList.config(font=('bold',20))
            count+=1
        myList.pack(side=LEFT,fill=BOTH)
        label = "Returned Result: " + str(count)
        cntLabel = Label(vehcPage,text=label)
        cntLabel.place(x=770,y=350)

    elif(views_partialcname.get() != ""):
        query="SELECT VIN , VEHICLE , AVG(OrderAmount/TotalDays) AS AverageDailyPrice FROM vrentalinfo WHERE VEHICLE REGEXP %s GROUP BY VIN  ORDER BY AverageDailyPrice"
        regex = "^.*" + views_partialcname.get() + ".*"
        my_cursor.execute(query,(regex, ))
        myList = Listbox(vehViewsConsole)
        myList.config(width=900,height=320)
        print_records='{:^35} {:>45} {:>65}'.format('VehicleID','Description', 'Average Daily Price')
        myList.insert(END, print_records+ "\n")
        count=0
        for line in my_cursor:
            num = float(line[2])
            num = round(num,2)
            line_new = '{:^35} {:>35} {:>45}'.format(str(line[0]), str(line[1]),'$'+str(num))
            myList.insert(END, line_new+ "\n")
            myList.config(font=('bold',20))
            count+=1
        myList.pack(side=LEFT,fill=BOTH)
        label = "Returned Result: " + str(count)
        cntLabel = Label(vehcPage,text=label)
        cntLabel.place(x=770,y=350)

    else:
        query="SELECT VIN , VEHICLE , AVG(OrderAmount/TotalDays) AS AverageDailyPrice FROM vrentalinfo GROUP BY VIN  ORDER BY AverageDailyPrice"
        my_cursor.execute(query)
        myList = Listbox(vehViewsConsole)
        myList.config(width=900,height=320)
        print_records='{:^35} {:>45} {:>65}'.format('VehicleID','Description', 'Average Daily Price')
        myList.insert(END, print_records+ "\n")
        num =0
        count=0
        for line in my_cursor:
            num = float(line[2])
            num = round(num,2)
            line_new = '{:^35} {:>35} {:>45}'.format(str(line[0]), str(line[1]),'$'+str(num))
            myList.insert(END, line_new+ "\n")
            myList.config(font=('bold',20))
            count+=1
        myList.pack(side=LEFT,fill=BOTH)
        label = "Returned Result: " + str(count)
        cntLabel = Label(vehcPage,text=label)
        cntLabel.place(x=770,y=350)
    db.close()

def destroyFrames():
    for frame in mainFrame.winfo_children():
        frame.destroy()

#initializes New Customer page
def newCustomerPage():
    destroyFrames()
    global newCustomerFrame
    newCustomerFrame = Frame(mainFrame, bg="#c7c7c7")
    newCustomerFrame.pack(side=LEFT)
    newCustomerFrame.pack_propagate(False)
    newCustomerFrame.configure(width=900,height=700)

    global resultConsole
    resultConsole = Frame(newCustomerFrame, bg="#262626")
    resultConsole.pack(side=BOTTOM)
    resultConsole.pack_propagate(False)
    resultConsole.configure(width=900,height=400)

    lb = Label(newCustomerFrame, text='New Customer Information', font=('bold',30))
    lb.pack()

    C_name_label=Label(newCustomerFrame, text='Enter Customer name')
    C_name_label.place(x=20,y=50)
    global C_name
    C_name = Entry(newCustomerFrame, width=30)
    C_name.place(x=20,y=80)
    C_phone_label = Label(newCustomerFrame, text='Enter Customer Phone Number')
    C_phone_label.place(x=20,y=120)
    global C_phone
    C_phone = Entry(newCustomerFrame, width=30)
    C_phone.place(x=20,y=150)
    
    submit_btn = Button(newCustomerFrame,text="Submit",command=submit)
    submit_btn.place(x=20,y=200)
    view_btn = Button(newCustomerFrame,text="View Records",command=viewData)
    view_btn.place(x=120,y=200)

#initializes new Vehicle page
def newVehiclePage():
    destroyFrames()
    global newVehicleFrame
    newVehicleFrame = Frame(mainFrame, bg="#c7c7c7")
    newVehicleFrame.pack(side=LEFT)
    newVehicleFrame.pack_propagate(False)
    newVehicleFrame.configure(width=900,height=700)

    global resultConsole2
    resultConsole2 = Frame(newVehicleFrame, bg="#262626")
    resultConsole2.pack(side=BOTTOM)
    resultConsole2.pack_propagate(False)
    resultConsole2.configure(width=900,height=400)

    lb = Label(newVehicleFrame, text='New Vehicle Creation', font=('bold',30))
    lb.pack()

    V_id_label=Label(newVehicleFrame, text='Enter Vehicle ID')
    V_id_label.place(x=20,y=50)
    global V_id
    V_id = Entry(newVehicleFrame, width=30)
    V_id.place(x=20,y=80)
    V_desc_label=Label(newVehicleFrame, text='Enter Vehicle Description')
    V_desc_label.place(x=20,y=120)
    global V_desc
    V_desc = Entry(newVehicleFrame, width=30)
    V_desc.place(x=20,y=150)
    V_year_label=Label(newVehicleFrame, text='Enter Vehicle Year')
    V_year_label.place(x=20,y=190)
    global V_year
    V_year = Entry(newVehicleFrame,width=30)
    V_year.place(x=20,y=220)
    V_type_label=Label(newVehicleFrame, text='Enter Vehicle Type')
    V_type_label.place(x=350,y=50)
    global V_type
    V_type = Entry(newVehicleFrame,width=30)
    V_type.place(x=350,y=80)
    V_cat_label=Label(newVehicleFrame, text='Enter Vehicle Category')
    V_cat_label.place(x=350,y=120)
    global V_cat
    V_cat = Entry(newVehicleFrame,width=30)
    V_cat.place(x=350,y=150)
    submit_btn = Button(newVehicleFrame,text="Submit",command=submit2)
    submit_btn.place(x=20,y=260)
    view_btn = Button(newVehicleFrame,text="View Records",command=viewVehicleData)
    view_btn.place(x=120,y=260)

#initializes new rental page
def newRentalPage():
    destroyFrames()
    global newRentalFrame
    newRentalFrame = Frame(mainFrame, bg="#c7c7c7")
    newRentalFrame.pack(side=LEFT)
    newRentalFrame.pack_propagate(False)
    newRentalFrame.configure(width=900,height=700)

    global availableCarsConsole
    availableCarsConsole =Frame(newRentalFrame, bg="#c7c7c7")
    availableCarsConsole.pack(side=BOTTOM)
    availableCarsConsole.pack_propagate(False)
    availableCarsConsole.configure(width=900,height=200)

    lb = Label(newRentalFrame, text='New Rental Creation', font=('bold',30))
    lb.pack()

    label1=Label(newRentalFrame,text='Enter Rental Start Date')
    label1.place(x=20,y=80)
    global R_Rstartdate
    R_Rstartdate = Entry(newRentalFrame, width=10)
    R_Rstartdate.place(x=20,y=110)
    label2=Label(newRentalFrame,text='Enter Rental End Date')
    label2.place(x=400,y=80)
    global R_Renddate
    R_Renddate = Entry(newRentalFrame, width=10)
    R_Renddate.place(x=400,y=110)
    submit_btn = Button(newRentalFrame,text="Submit",command=searchAvailableCars)
    submit_btn.place(x=20,y=150)

#initializes rental return page
def returnRentalPage():
    destroyFrames()
    global returnRental
    returnRental = Frame(mainFrame, bg="#c7c7c7")
    returnRental.pack(side=LEFT)
    returnRental.pack_propagate(False)
    returnRental.configure(width=900,height=700)

    lb = Label(returnRental, text='Return Rental', font=('bold',30))
    lb.pack()

    R_returndate_label=Label(returnRental, text='Enter Return Date')
    R_returndate_label.place(x=20,y=50)
    global R_returndate
    R_returndate = Entry(returnRental, width=30)
    R_returndate.place(x=20,y=80)    
    R_custID_label=Label(returnRental, text='Enter Customer ID')
    R_custID_label.place(x=20,y=120)
    global R_custID
    R_custID = Entry(returnRental, width=30)
    R_custID.place(x=20,y=150)  
    R_vehiD_label=Label(returnRental, text='Enter Vehicle ID')
    R_vehiD_label.place(x=20,y=190)
    global R_vehiD
    R_vehiD = Entry(returnRental, width=30)
    R_vehiD.place(x=20,y=220)
    submit_btn = Button(returnRental,text="Search",command=searchRental)
    submit_btn.place(x=20,y=260)

#initializes customer's view's result
def customerPage():
    destroyFrames()
    global custPage
    custPage = Frame(mainFrame,bg="#c7c7c7")
    custPage.pack(side=BOTTOM)
    custPage.pack_propagate(False)
    custPage.configure(width=900,height=700)

    global custViewsConsole
    custViewsConsole = Frame(custPage,bg="#262626")
    custViewsConsole.pack(side=BOTTOM)
    custViewsConsole.pack_propagate(False)
    custViewsConsole.configure(width=900,height=320)

    lb = Label(custPage, text="Customer's View", font=('bold',30))
    lb.pack()

    custID_label = Label(custPage, text="Enter Customer ID")
    custID_label.place(x=20,y=80)
    global views_custID
    views_custID=Entry(custPage,width=20)
    views_custID.place(x=20,y=120)

    fullname_label=Label(custPage,text="Enter Full Name")
    fullname_label.place(x=20,y=160)
    global views_fullname
    views_fullname=Entry(custPage,width=20)
    views_fullname.place(x=20,y=200)

    partialname_label=Label(custPage,text="Enter Partial Name (Optional)")
    partialname_label.place(x=20,y=240)
    global views_partialname
    views_partialname=Entry(custPage,width=20)
    views_partialname.place(x=20,y=280)

    searchViewsBtn = Button(custPage,text="Search",command=searchCustView)
    searchViewsBtn.place(x=20,y=320)

#initializes vehicles's view's result
def vehiclePage():
    destroyFrames()
    global vehcPage
    vehcPage = Frame(mainFrame,bg="#c7c7c7")
    vehcPage.pack(side=BOTTOM)
    vehcPage.pack_propagate(False)
    vehcPage.configure(width=900,height=700)

    global vehViewsConsole
    vehViewsConsole = Frame(vehcPage,bg="#262626")
    vehViewsConsole.pack(side=BOTTOM)
    vehViewsConsole.pack_propagate(False)
    vehViewsConsole.configure(width=900,height=320)

    lb = Label(vehcPage, text="Vehicle's View", font=('bold',30))
    lb.pack()

    vehicleID_label = Label(vehcPage, text="Enter Vehicle ID")
    vehicleID_label.place(x=20,y=80)
    global views_vehicleID
    views_vehicleID=Entry(vehcPage,width=20)
    views_vehicleID.place(x=20,y=120)

    carname_label=Label(vehcPage,text="Enter Car Name")
    carname_label.place(x=20,y=160)
    global views_carname
    views_carname=Entry(vehcPage,width=20)
    views_carname.place(x=20,y=200)

    partialcname_label=Label(vehcPage,text="Enter Partial Car Name (Optional)")
    partialcname_label.place(x=20,y=240)
    global views_partialcname
    views_partialcname=Entry(vehcPage,width=20)
    views_partialcname.place(x=20,y=280)

    searchViewsBtn = Button(vehcPage,text="Search",command=searchVehicleView)
    searchViewsBtn.place(x=20,y=320)


optionsFrame = Frame(root,bg="#000000")
optionsFrame.pack(side=LEFT)
optionsFrame.pack_propagate(False)
optionsFrame.configure(width=250,height=700)

mainFrame = Frame(root,bg="#000000")
mainFrame.pack(side=LEFT)
mainFrame.pack_propagate(False)
mainFrame.configure(width=950,height=700)


newCustomer = Button(optionsFrame, text="New Customer",padx=30,pady=30,command=newCustomerPage)
newCustomer.place(x=30,y=50)

newVehicle = Button(optionsFrame, text="New Vehicle",padx=37,pady=30,command=newVehiclePage)
newVehicle.place(x=30,y=150)

newRental = Button(optionsFrame, text="New Rental",padx=40,pady=30, command=newRentalPage)
newRental.place(x=30,y=250)

returnRental = Button(optionsFrame, text="Return Rental",padx=33,pady=30,command=returnRentalPage)
returnRental.place(x=30,y=350)

CustomerBtn = Button(optionsFrame, text="Customer",padx=45,pady=30,command=customerPage)
CustomerBtn.place(x=30,y=450)

VehicleBTN = Button(optionsFrame, text="Vehicle",padx=53,pady=30,command=vehiclePage)
VehicleBTN.place(x=30,y=550)

root.resizable(False,False)
root.mainloop()