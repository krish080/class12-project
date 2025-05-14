import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ast 
current_date = datetime.now().strftime("%d %m %Y")


main_data = None
screen = tk.Tk()
screen.title("Elite Bank")
screen.geometry("1000x600")
screen.configure(bg="#ADD8E6")
screen.resizable(False, False)




with open("data.txt", "r") as txt_file:
    content = txt_file.read()  # Read the file content
    main_data = ast.literal_eval(content)
    

show_password_state = False
show_button = None
password_entry = None
username_entry, password_entry = None, None
user = None
recipient = None
pin_val=None
sr="login"

def mail(receiver_email,subject,body):
    sender_email = "elitebank038@gmail.com"
    
    password = "qnyt yvar xouz qqev"  

    # Email content
    

    # Create the email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
        
def show_password():
    global show_password_state, show_button, password_entry,pin_val

    if show_password_state == False:
        show_button.config(bg="red", fg="white", text="Hide")
        show_password_state = True
        if  sr=="login":
            password_entry.config(show="")
        else:
            pin_val.config(show="")
    else:
        show_button.config(bg="blue", fg="white", text="Show")
        show_password_state = False
        if  sr=="login":
            password_entry.config(show="*")
        else:    
            pin_val.config(show="*")


def show_admin_screen():
    global main_data
    with open("data.txt", "w") as txt_file:
    
        txt_file.write(str(main_data))


    for i in screen.winfo_children():
        i.destroy()

    heading_label = tk.Label(screen, text="Admin Control Panal", font=("Helvetica", 20, "bold"), bg="#98FB98")
    heading_label.place(relx=0.5, rely=0.1, anchor='center')
    
    deposit = tk.Button(screen, text="Deposit", font=("Helvetica", 16), width=12, height=1, bg="#4CAF50", fg="white", command=lambda:show_deposit_withdrawal_screen("deposit"))
    deposit.place(relx=0.5,y=230,anchor='center')

    withdraw = tk.Button(screen, text="Withdraw", font=("Helvetica", 16), width=12, height=1, bg="#008CBA", fg="white",command=lambda:show_deposit_withdrawal_screen("Withdrawal"))
    withdraw.place(relx=0.5,y=290,anchor='center')

    logout = tk.Button(screen, text="Logout", font=("Helvetica", 16), width=12, height=1, bg="red", fg="white",command=show_home)
    logout.place(relx=0.5,y=350,anchor='center')
cutomer=None
type=None

def dw_search():
    global main_data,customer_account_entry,customer
    
    heading_label = tk.Label(screen, text="Admin Control Panal", font=("Helvetica", 20, "bold"), bg="#98FB98")
    heading_label.place(relx=0.5, rely=0.1, anchor='center')
    for x,i in enumerate(main_data["Users"]):
        if i["AccountNo"]==int(customer_account_entry.get()):
            customer=x
            deposit_withdrawal()
            break
    else:
        messagebox.showinfo("", "Account not found")


def d_w(amount):
    global type,main_data,customer,show_admin_screen
    if type=="deposit":
        main_data["Users"][customer]["balance"]+=amount
        messagebox.showinfo("", "Amount Deposited")
        main_data["Users"][customer]["transactionHistory"].append({"transactionId":main_data["Users"][customer]["notr"]+1,"amount": int(amount),"type": "Deposited","date": current_date})


        show_admin_screen()
    else:   
        if main_data["Users"][customer]["balance"]>=amount:
            main_data["Users"][customer]["balance"]-=amount
            main_data["Users"][customer]["transactionHistory"].append({"transactionId":main_data["Users"][customer]["notr"]+1,"amount": int(amount),"type": "Withdrawed","date": current_date})
            messagebox.showinfo("", "Amount Withdrawed")
            show_admin_screen()
        else:
            messagebox.showinfo("", "Insufficient Balance")


def deposit_withdrawal():
    global type,customer
    for i in screen.winfo_children():
        i.destroy()
    heading_label = tk.Label(screen, text=type.upper(), font=("Helvetica", 20, "bold"), bg="#98FB98")
    heading_label.place(relx=0.5, rely=0.1, anchor='center')

    name = tk.Label(screen, text="Name : " + main_data["Users"][customer]["name"], font=("Helvetica", 12, "bold"), background="#98FB98")
    name.place(relx=0.5, rely=0.345,anchor='center')
    
    acno = tk.Label(screen, text="Account no : " + str(main_data["Users"][customer]["AccountNo"]), font=("Helvetica", 12, "bold"), background="#98FB98")
    acno.place(relx=0.5, rely=0.395,anchor='center')
    
    amount = tk.Label(screen, text="Amount :" , font=("Helvetica", 12, "bold"), background="#98FB98")
    amount.place(relx=0.37, rely=0.47,anchor='center')
    
    amount_val = tk.Entry(screen, font=("Helvetica", 12))
    amount_val.place(relx=0.5, rely=0.47, anchor='center')

    transfer_button = tk.Button(screen, text=type.upper(), font=("Helvetica", 12), command=lambda:d_w(int(amount_val.get())))
    transfer_button.place(relx=0.5, rely=0.65, anchor='center')

def show_deposit_withdrawal_screen(type1):
    global customer_account_entry,type,main_data
    type=type1
    with open("data.txt", "w") as txt_file:
    
        txt_file.write(str(main_data))
    for i in screen.winfo_children():
        i.destroy()

    screen.configure(bg="#98FB98")


    heading_label = tk.Label(screen, text="Admin Control Panal", font=("Helvetica", 20, "bold"), bg="#98FB98")
    heading_label.place(relx=0.5, rely=0.1, anchor='center')

    customer_account_label = tk.Label(screen, text="Customer Account No", font=("Helvetica", 12, 'bold'), bg="#98FB98")
    customer_account_label.place(relx=0.5, rely=0.4, anchor='center')

    
    customer_account_entry = tk.Entry(screen, font=("Helvetica", 12))
    customer_account_entry.place(relx=0.5, rely=0.45, anchor='center')

    search_button = tk.Button(screen, text="Search", font=("Helvetica", 12), command=dw_search)
    search_button.place(relx=0.5, rely=0.55, anchor='center')

def show_transactions_history():
    global screen, main_data,show_password
    with open("data.txt", "w") as txt_file:
    
        txt_file.write(str(main_data))
    global user
    
    transaction_window = tk.Toplevel()
    transaction_window.title(f"{user['name']}'s Transaction History")
    transaction_window.geometry("400x300")
    
   
    title_label = tk.Label(transaction_window, text="Transaction History", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    if user['transactionHistory']:
     
        transaction_listbox = tk.Listbox(transaction_window, font=("Helvetica", 12), width=50, height=10)
        transaction_listbox.pack(pady=10)

       
        for transaction in user['transactionHistory']:
            transaction_text = f"ID: {transaction['transactionId']}, {transaction['amount']}-{transaction['type']}  on {transaction['date']}"
            transaction_listbox.insert(tk.END, transaction_text)
    else:
       
        no_transactions_label = tk.Label(transaction_window, text="No transactions found", font=("Helvetica", 12, "italic"))
        no_transactions_label.pack(pady=10)

    
    close_button = tk.Button(transaction_window, text="Close", command=transaction_window.destroy)
    close_button.pack(pady=10)
    

def show_transferScreen():
    global screen, main_data,show_password,sr
    sr="t"
    with open("data.txt", "w") as txt_file:
    
        txt_file.write(str(main_data))
   
    screen.config(background="#98FB98")
    
    for widget in screen.winfo_children():
        widget.destroy()

    heading_label = tk.Label(screen, text="MONEY TRANSFER", font=("Helvetica", 20, "bold"), bg="#98FB98")
    heading_label.place(relx=0.5, rely=0.1, anchor='center')

    def moneytransfer():
        global recipient,user
        global pin_val, amount_val,show_button
        otp1=random.randrange(1000,10000)
        mail(
    user["mail"],
    "Elite Bank - Transaction OTP",
    """Dear Customer,

You are attempting to perform a transaction through your Elite Bank account.
Please use the following One-Time Password (OTP) to authorize the transaction:

OTP: """ + str(otp1) + """

If you did not initiate this transaction, please contact our customer support immediately to secure your account.

Thank you,
Elite Bank Security Team"""
)

        def transfer():
            global recipient,user
            for x,i in enumerate(main_data['Users']):
                for y,j in enumerate(main_data['Users']):
                    if i["name"]==user["name"] and j["name"]==recipient["name"]:
                        if int(main_data["Users"][x]["pin"])==int(pin_val.get()):
                            if otp_val.get()==str(otp1):
                                
                                if int(amount_val.get())>=0:
                                    if main_data["Users"][x]["balance"]>=int(amount_val.get()):
                                        
                                        main_data["Users"][x]["balance"]-=int(amount_val.get())
                                        main_data["Users"][y]["balance"]+=int(amount_val.get())
                                        
                                        main_data["Users"][x]["transactionHistory"].append({"transactionId":main_data["Users"][x]["notr"]+1,"amount": int(amount_val.get()),"type": "Transferred To "+j["name"],"date": current_date})
                                        main_data["Users"][y]["transactionHistory"].append({"transactionId":main_data["Users"][y]["notr"]+1,"amount": int(amount_val.get()),"type": "Transferred From "+i["name"],"date": current_date})
                                    
                                        main_data["Users"][x]["notr"]+=1
                                        main_data["Users"][y]["notr"]+=1
                                        
                                        messagebox.showinfo("", "Transaction is being processed")
                                        
                                        mail(user["mail"],"Amount Debited",str(amount_val.get())+" sent to "+recipient["name"])
                                        mail(recipient["mail"],"Amount Credited",str(amount_val.get())+" received from "+user["name"])
                                        
                                    else:
                                        messagebox.showinfo("", "Insufficient balance")
                                        break
                                else:
                                    messagebox.showinfo("", "Kindly enter a valid amount")
                            else:
                                messagebox.showinfo("", "Wrong OTP")
                                
                        else:
                            messagebox.showinfo("", "Wrong PIN")
                            break
            else:
                messagebox.showinfo("", "TRANSFER SUCESSFUL")
                show_accountDetails()
            
            
        for widget in screen.winfo_children():
            widget.destroy()
        global bg
        bg = tk.PhotoImage(file="assets/transfer.png")  
        bgl = tk.Label(screen, image=bg)
        bgl.place(x=0, y=0, relwidth=1, relheight=1)
        
        
        
        name = tk.Label(screen, text= recipient["name"], font=("Helvetica", 12, "bold"), background="white")
        name.place(relx=0.525, rely=0.345,anchor='center')
        
        acno = tk.Label(screen, text= str(recipient["AccountNo"]), font=("Helvetica", 12, "bold"), background="white")
        acno.place(relx=0.55, rely=0.395,anchor='center')
        
        
        amount_val = tk.Entry(screen, font=("Helvetica", 12),bd=2,relief="solid")
        amount_val.place(relx=0.5, rely=0.47, anchor='center')
        
        pin_val = tk.Entry(screen, font=("Helvetica", 12),show="*",bd=2,relief="solid")
        pin_val.place(relx=0.5, rely=0.55, anchor='center')
        
        
        otp_val = tk.Entry(screen, font=("Helvetica", 12),show="",bd=2,relief="solid")
        otp_val.place(relx=0.5, rely=0.63, anchor='center')
        
        transfer_button = tk.Button(screen, text="Transfer", font=("Helvetica", 12),bg="green", command=transfer)
        transfer_button.place(relx=0.5, rely=0.71, anchor='center')
        
        show_button = tk.Button(screen, text="Show", font=("Helvetica", 10), bg="blue", fg="white", command=show_password)
        show_button.place(relx=0.63, rely=0.55,anchor='center')

    def search():
        global screen, main_data, recipient_account_entry, found, recipient
        found = False
        for i in main_data["Users"]:
            if str(i["AccountNo"]) == str(recipient_account_entry.get()):
                recipient = i
                found = True
                messagebox.showinfo("", "Account Found")
                moneytransfer()
        if not found:
            messagebox.showinfo("", "Account Not Found")

    global bg_image
    
    bg_image = tk.PhotoImage(file="assets/searchac.png")  # Load once and keep a reference!
    bg_label = tk.Label(screen, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    

    global recipient_account_entry 
    recipient_account_entry = tk.Entry(screen, font=("Helvetica", 12),bd=2,relief="solid")
    recipient_account_entry.place(relx=0.5, rely=0.45, anchor='center')

    search_button = tk.Button(screen, text="Search", font=("Helvetica", 12),bg="green", command=search)
    search_button.place(relx=0.5, rely=0.55, anchor='center')

def show_signup():
    
    global main_data
    with open("data.txt", "w") as txt_file:
    
        txt_file.write(str(main_data))
    global screen
    screen.configure(bg="#98FB98")
    for i in screen.winfo_children():
        i.destroy()
    
    global bg_image
    
    bg_image = tk.PhotoImage(file="assets/SIGNUP.png")  # Load once and keep a reference!
    bg_label = tk.Label(screen, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    def signup():
        if username_entry.get()!="" and password_entry.get()!="" and confirm_password_entry.get()!="" and confirm_password_entry.get()!="" and Pin_entry.get()!="":
            if password_entry.get()==confirm_password_entry.get():
                main_data["Users"].append({
                    "name":username_entry.get(),
                    "Password":password_entry.get(),
                    "mail":mail_entry.get(),
                    "pin":Pin_entry.get(),
                    "AccountNo":main_data["noac"]+101,
                    "balance":0,
                    "notr":0,
                    "transactionHistory":[]
                    
                })
                main_data["noac"]+=1
                messagebox.showinfo("", "Your account has been created")
                show_home()
            else:
                messagebox.showinfo("", "Passwords not matching")
        else:
            messagebox.showinfo("", "Kindly fill all the details")
            
    
    global username_entry,password_entry,confirm_password_entry,confirm_password_entry,Pin_entry
    
    
    username_entry = tk.Entry(screen, font=("Helvetica", 12), background="white")
    username_entry.place(relx=0.45, rely=0.29, relwidth=0.15, relheight=0.05)

    password_entry = tk.Entry(screen, font=("Helvetica", 12), background="white", show="")
    password_entry.place(relx=0.45, rely=0.38, relwidth=0.15, relheight=0.05)
    
    confirm_password_entry = tk.Entry(screen, font=("Helvetica", 12), background="white", show="")
    confirm_password_entry.place(relx=0.45, rely=0.46, relwidth=0.15, relheight=0.05)
     
    mail_entry = tk.Entry(screen, font=("Helvetica", 12), background="white", show="")
    mail_entry.place(relx=0.45, rely=0.55, relwidth=0.15, relheight=0.05)
    
    
    Pin_entry = tk.Entry(screen, font=("Helvetica", 12), background="white", show="")
    Pin_entry.place(relx=0.45, rely=0.63, relwidth=0.15, relheight=0.05)
    
    Signup_button = tk.Button(screen, text="Signup", font=("Helvetica", 16, 'bold'), bg="blue", fg="white", command=signup)
    Signup_button.place(relheight=0.08, relwidth=0.10, relx=0.5, rely=0.77,anchor='center')



def show_accountDetails():

    with open("data.txt", "w") as txt_file:
    
        txt_file.write(str(main_data))
    screen.config(background="#98FB98") 
    
    
    
    for i in screen.winfo_children():
        i.destroy()
        
    global bg_image
    
    bg_image = tk.PhotoImage(file="assets/account_details.png")  # Load once and keep a reference!
    bg_label = tk.Label(screen, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    
    
    name = tk.Label(screen, text=user["name"], font=("Helvetica", 15, "bold"), background="white")
    name.place(relx=0.38, rely=0.284)
    
    mo = tk.Label(screen, text= str(user["mail"]), font=("Helvetica", 15, "bold"), background="white")
    mo.place(relx=0.38, rely=0.336)
    
    acno = tk.Label(screen, text=str(user["AccountNo"]), font=("Helvetica", 15, "bold"), background="white")
    acno.place(relx=0.38, rely=0.395)
    
    bal = tk.Label(screen, text=str(user["balance"]), font=("Helvetica", 15, "bold"), background="white")
    bal.place(relx=0.38, rely=0.45)
    
    Transfer_money = tk.Button(screen, text="Transfer", font=("Helvetica", 16, 'bold'), bg="blue", fg="white", command=show_transferScreen)
    Transfer_money.place(relheight=0.08, relwidth=0.1, relx=0.33, rely=0.7,anchor='center')
    
    Transfer_history = tk.Button(screen, text="Transfer History", font=("Helvetica", 16, 'bold'), bg="#4CAF50", fg="white", command=show_transactions_history)
    Transfer_history.place(relheight=0.08, relwidth=0.17, relx=0.5, rely=0.7,anchor='center')

    Transfer_money = tk.Button(screen, text="LOGOUT", font=("Helvetica", 16, 'bold'), bg="red", fg="white", command=show_home)
    Transfer_money.place(relheight=0.08, relwidth=0.1, relx=0.67, rely=0.7,anchor='center')


def check_password():
    global main_data, username_entry, password_entry, user
    login_st = False
    u = username_entry.get()
    p = password_entry.get()
    
    if u=="Admin" and p=="Admin_123":
        show_admin_screen()
    else:
        for i in main_data["Users"]:
            if i["name"] == u:
                login_st = True
                if i["Password"] == p:
                    messagebox.showinfo("LOGIN SUCCESSFUL", "Login successful")
                    user = i
                    show_accountDetails()
                else:
                    messagebox.showinfo("LOGIN FAILURE", "Login failure")
        if not login_st:
            messagebox.showinfo("LOGIN FAILURE", "Login failure")


def show_forgot_passord():
    global main_data,mail
    global u1
    u1=0
    
    for i in screen.winfo_children():
        i.destroy()
        
    global bg
    bg = tk.PhotoImage(file="assets/Forgotpassword.png")  
    bgl = tk.Label(screen, image=bg)
    bgl.place(x=0, y=0, relwidth=1, relheight=1)
    
    
    
    def findUser(name):
        for z,i in enumerate(main_data["Users"]):
            if i["name"]==name:
                global u1
                u1=z
                OTP(i)
                break
        else:
            messagebox.showinfo("", "Account not found")
            
    
    def resetPassword():
        for i in screen.winfo_children():
            i.destroy()
        def reset(x,y):
            global u1
            if x==y:
                main_data["Users"][u1]["Password"]=x
                messagebox.showinfo("", "Password Updated")
                show_home()
            else:
                messagebox.showinfo("", "Passwords are not matching")
                
                
        global bg
        bg = tk.PhotoImage(file="assets/resetp.png")  
        bgl = tk.Label(screen, image=bg)
        bgl.place(x=0, y=0, relwidth=1, relheight=1)
        
        password_entry1 = tk.Entry(screen, font=("Helvetica", 12), background="white", show="",bd=2,relief="solid")
        password_entry1.place(relx=0.42, rely=0.37, relwidth=0.15, relheight=0.05)
        
        confirm_password_entry1 = tk.Entry(screen, font=("Helvetica", 12), background="white", show="",bd=2,relief="solid")
        confirm_password_entry1.place(relx=0.42, rely=0.45, relwidth=0.15, relheight=0.05)
        
        go_button = tk.Button(screen, text="GO", font=("Helvetica", 15, 'bold'), bg="#FFA500", fg="white", command=lambda:reset(password_entry1.get(),confirm_password_entry1.get()))
        go_button.place(relx=0.51, rely=0.55)
        
    def username():
        
        for i in screen.winfo_children():
            i.destroy()
        global bg
        bg = tk.PhotoImage(file="assets/Forgotpassword.png")  
        bgl = tk.Label(screen, image=bg)
        bgl.place(x=0, y=0, relwidth=1, relheight=1)
        
        
        
        u_entry = tk.Entry(screen, font=("Helvetica", 12), background="white", show="",bd=2,relief="solid")
        u_entry.place(relx=0.42, rely=0.33, relwidth=0.15, relheight=0.05)
        
        ugo_button = tk.Button(screen, text="GO", font=("Helvetica", 15, 'bold'), bg="#FFA500", fg="white", command=lambda:findUser(u_entry.get()))
        ugo_button.place(relx=0.52, rely=0.4)
        
        back_button = tk.Button(screen, text="Back", font=("Helvetica", 15, 'bold'), bg="#333333", fg="white",command=show_home)
        back_button.place(relx=0.4195, rely=0.4)
    
    def OTP(user):
        def check_opt(otp,otp_entered):
            if otp==otp_entered:
                resetPassword()
            else:
                messagebox.showinfo("", "OTP IS WRONG")

        f_otp=random.randrange(1000,10000)
        messagebox.showinfo("", "Sending OTP")
        
        mail(user["mail"],
    "Elite Bank - Password Reset Request",
    "Dear Customer,\n\n"
    "We received a request to reset the password associated with your Elite Bank account.\n"
    "Please use the following One-Time Password (OTP) to proceed with resetting your password:\n\n"
    "OTP: " + str(f_otp) + "\n\n"
    "If you did not initiate this request, please contact our customer support immediately.\n\n"
    "Thank you,\n"
    "Elite Bank Support Team"
                                                )
        messagebox.showinfo("", "OTP SENT")
        
        for i in screen.winfo_children():
            i.destroy()
        
        global bg
        bg = tk.PhotoImage(file="assets/fpreset.png")  
        bgl = tk.Label(screen, image=bg)
        bgl.place(x=0, y=0, relwidth=1, relheight=1)
        
        otp_entry = tk.Entry(screen, font=("Helvetica", 12), background="white", show="",bd=2,relief="solid")
        otp_entry.place(relx=0.42, rely=0.33, relwidth=0.15, relheight=0.05)
        
        ogo_button = tk.Button(screen, text="GO", font=("Helvetica", 15, 'bold'), bg="#FFA500", fg="white", command=lambda:check_opt(f_otp,int(otp_entry.get())))
        ogo_button.place(relx=0.52, rely=0.4)
        
        back_button = tk.Button(screen, text="Back", font=("Helvetica", 15, 'bold'), bg="#333333", fg="white",command=username)
        back_button.place(relx=0.4195, rely=0.4)
    username()
    
    
def show_login_screen():
    global main_data,sr,show_forgot_passord
    sr="login"
    with open("data.txt", "w") as txt_file:
    
        txt_file.write(str(main_data))
    global screen, show_button, password_entry, username_entry, password_entry,bg_image
    
    for i in screen.winfo_children():
        i.destroy()
        
    screen.config(background="#98FB98")   
    
    bg_image = tk.PhotoImage(file="assets/login.png")  # Load once and keep a reference!
    bg_label = tk.Label(screen, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    username_entry = tk.Entry(screen, font=("Helvetica", 12), background="white")
    username_entry.place(relx=0.42, rely=0.37, relwidth=0.15, relheight=0.05)
    
    password_entry = tk.Entry(screen, font=("Helvetica", 12), background="white", show="*")
    password_entry.place(relx=0.42, rely=0.45, relwidth=0.15, relheight=0.05)
    
    fp = tk.Button(screen, text="Forgot Password", font=("Helvetica", 10),command=show_forgot_passord)
    fp.place(relx=0.49, rely=0.55,anchor='center')
    
    show_button = tk.Button(screen, text="Show", font=("Helvetica", 10), bg="blue", fg="white", command=show_password)
    show_button.place(relx=0.6, rely=0.45)
    
    back_button = tk.Button(screen, text="Back", font=("Helvetica", 15, 'bold'), bg="#333333", fg="white",command=show_home)
    back_button.place(relx=0.4195, rely=0.6)
    
    go_button = tk.Button(screen, text="GO", font=("Helvetica", 15, 'bold'), bg="#FFA500", fg="white", command=check_password)
    go_button.place(relx=0.51, rely=0.6)


def show_home():
    global main_data
    with open("data.txt", "w") as txt_file:
    
        txt_file.write(str(main_data))
    global screen, bg_image
    screen.configure(bg="#ADD8E6")
    for i in screen.winfo_children():
        i.destroy()
    
    
    # Load and set background image
    bg_image = tk.PhotoImage(file="assets/home.png")  # Load once and keep a reference!
    bg_label = tk.Label(screen, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    

    login_button = tk.Button(screen, text="Login", font=("Helvetica", 16), width=12, height=1, bg="#4CAF50", fg="white", command=show_login_screen)
    login_button.place(x=140,y=280)

    sign_in_button = tk.Button(screen, text="Sign Up", font=("Helvetica", 16), width=12, height=1, bg="#008CBA", fg="white",command=show_signup)
    sign_in_button.place(x=140,y=350)

    

show_home()

screen.mainloop()