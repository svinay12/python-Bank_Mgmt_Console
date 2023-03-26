import os,rich,sys,random,datetime,time
from rich.console import Console
from rich.table import Table
import csv,pymongo
from rich import box
from rich.live import Live
from rich.table import Table


# mongo connection :

cluster = pymongo.MongoClient('mongodb+srv://vinsharex:G0emexG4oEc92DW9@pythonprojects.gn9deee.mongodb.net/customer_detail?retryWrites=true&w=majority')
db = cluster["customer_detail"]
client = db["customer_data"]


class ABC_Bank:
    bank_name="ABC BANK LTD"
    IFSC_code="ABCB0000189"
    
    # for dummy data :
    # name=['nitesh','vinay','sunny','bunny','jay','suresh','vinny','chinny','chiku','neeraj']
    # date=['18-04-2001','11-02-2001','05-02-2015','15-02-2020','02-02-2012','11-02-2012','13-02-2001','12-03-2011','12-02-2010','12-02-2002']
    # address=['indore','indore','bhopal','ujjain','devas']
    # bal=[12000,13000,50000,15000,20000,17000]
    
    # =================== Create account function =================== 
    def createAccount(self):

        #  deposite amount check :

        while True:
            deposite=int(input("Enter Deposite Amount : "))
            if deposite>10000:
                break
            elif deposite == 0 : sys.exit(0)
            elif deposite<10000 and deposite>0 : print("Insufficient Balance!!!\n\n Try again other wise press 0 to exit : \n")
        
        adhaar = int(input("enter adhar no : "))
        for data in client.find():
            if data["adhar"]==adhaar:
                return "Account Already exist!!"
                    
                 
        # taking neccessary information of the user :
        data = {"acc_no": random.randint(100,500),
            "openingDate":datetime.datetime.utcnow(),
            "name":input("Enter Customer Name : "),
            "contact":int(input("Enter phone No. : ")),
            "dob":input("enter date in this format yyyy-mm-dd"),
            "address":input("Enter Customer Address : "),
            "adhar":adhaar,
            "balance":deposite}  
        client.insert_one(data)

        return "your Record successfully created!!!"

    # =================== Check account detail =================== 
    def check_detail(self,acc):
        n=1
        data = client.find_one({"acc_no":acc})
        if data!=None:
            table = Table(title=f"Mr. {data['name']} Details",box=box.SQUARE_DOUBLE_HEAD)
            table.add_column("SNo.", style="grey30", no_wrap=True)
            table.add_column("Account Details", style="dark_cyan", no_wrap=True)
            table.add_column("Description", style="medium_spring_green", no_wrap=True)

            for item1 in data:
                if "_id"!=str(item1):
                    table.add_row(str(n),str(item1),str(data[item1])) 
                    n=int(n)+1
                # print(item1,data[item1])
            
            console = Console()
            console.print(table)
            
        else : return "Account Number not found !!!"    
        
    # =================== Customer lists =================== 
    def customer_list(self):
        data = client.find().sort("acc_no",1)


        table = Table(title="ABC Bank Customers Details",box=box.SQUARE_DOUBLE_HEAD)
        table.add_column("Acc.No", justify="right", style="deep_pink4", no_wrap=True)
        table.add_column("Open date", style="grey0")
        table.add_column("Adhar No.", style="dark_cyan")
        table.add_column("Customer Name", style="dark_cyan")
        table.add_column("Contact No", style="dark_cyan")
        table.add_column("DoB", style="dark_cyan")
        table.add_column("City",justify="right", style="dark_cyan")
        table.add_column("Balance", justify="right", style="sky_blue2")
        
        # date
        with Live(table, refresh_per_second=4):  # update 4 times a second to feel fluid
            for customer in data:
                time.sleep(0.4) 
                d2 = str(customer['openingDate']).split(" ")[0].split("-")
                d1 = datetime.datetime(int(d2[0]),int(d2[1]),int(d2[2]))
                d=datetime.datetime.strftime(d1,'%Y-%m-%d')
                # print(customer['acc_no'],customer['openingDate'],customer['name'],customer['contact'],customer['dob'],customer['address'],customer['balance'])
                table.add_row(str(customer['acc_no']),str(d),str(customer['adhar']),str(customer['name']),str(customer['contact']),str(customer['dob']),str(customer['address']),str(customer['balance']))
                

            # console = Console()
            # console.print(table)

        input("Press enter to exit.")

    # =================== update customer account =================== 
    def update_detail(self,acc):
        
            data = client.find_one({"acc_no":acc})
            print("Which information you want to update ? \n")
            # self.check_detail(acc)
            n=1
            data = client.find_one({"acc_no":acc})
            if data!=None:
                table = Table(title=f"Mr. {data['name']} Details",box=box.SQUARE_DOUBLE_HEAD)
                table.add_column("SNo.", style="grey30", no_wrap=True)
                table.add_column("Account Details", style="dark_cyan", no_wrap=True)
                table.add_column("Description", style="medium_spring_green", no_wrap=True)

                for item1 in data:
                    if "_id"!=str(item1) and "acc_no"!=str(item1) and "openingDate"!=str(item1) and "balance"!=str(item1):
                        table.add_row(str(n),str(item1),str(data[item1])) 
                        n=int(n)+1
                table.add_row("6","exit")  
                    # print(item1,data[item1])
                
                console = Console()
                console.print(table)
            # ----------------------------------------------------------------------
            
            print(f"Which information you want to update ? [any time you want to exit press 6] \nselect here : ")
            while True:   
                   
                    choice = int(input("Enter here : "))
                    if choice == 1:
                        client.update_one({"_id":data["_id"]}, {"$set": {"name":input("Enter correct name here : ")}}, upsert=False)
                    #    Ac_detail["name"]==input("Enter name here : ")
                    elif choice == 2:
                          client.update_one({"_id":data["_id"]}, {"$set": {"contact":int(input("Enter correct contact here : "))}}, upsert=False)
                  
                        # Ac_detail["contact"]==input("Enter contact here : ")
                    elif choice == 3:
                          client.update_one({"_id":data["_id"]}, {"$set": {"address":input("Enter correct address here : ")}}, upsert=False)
                  
                        # Ac_detail["address"]==input("Enter address here : ")
                    elif choice == 4:
                          client.update_one({"_id":data["_id"]}, {"$set": {"dob":int(input("Enter correct dob here : "))}}, upsert=False)
                  
                        # Ac_detail["dob"]==input("Enter dob here : ")
                    elif choice == 5:
                        client.update_one({"_id":data["_id"]}, {"$set": {"adhar":int(input("Enter correct adhar No here : "))}}, upsert=False)
                    elif choice == 6:
                         return "All detail updated succesfully!!!"

    # =================== customer transactions  =================== 
    def transaction(self,acc):
         data = client.find_one({"acc_no":acc})

         print("\nWhat do you want to do ? \n  1. Deposite Amount \n  2. Withdraw Amount \n  3. Check Account Balance \n  4. Exit")
         
        #  -------------------------------------------------------------------------------
               
         while(True):
            # print("How may i help you choose anyone ?\n  1. withdraw amount\n  2. deposite amount\n  3. check balance\n\n")

            try :
                choice=int(input("enter choice => "))

            except Exception:print("please enter number only")

            else :
                if choice==1:
                    amt=int(input("Amount : "))
                    self.withdraw(acc,amt,data['balance'])
                    
                elif choice==2:
                    amt=int(input("Amount : "))
                    client.update_one({'acc_no':acc},{"$set":{"balance":data['balance']+amt}})
                    
                elif choice==3:
                        print(data["balance"])
                     
                elif choice==4:
                   break

                else :print("Please Select correct option...")      
            
            # print("want to any operation (y/n)")
            # try:
            #     while True:
            #         want=input("=> ")
            #         if want=='y' or want=='yes':
            #             break
            #         elif want=='n' or want=='no':
            #             sys.exit(0)
            #         else : print("select correct option")
            # except Exception:
            #     print("enter yes or no")

            
               
        # -------------------------------------------------------------------------------
        

      
    # =================== withdraw amount  =================== 
  
    def withdraw(self,acc,amt,bal):
        # data = client.find_one({"acc_no":acc})

        if amt>bal:
            print("Insufficient balance ")
        elif amt<bal and amt>bal-10000 and bal>0:
            print("Amount will deduct from minimum balance.(2%) Charges  will be deducted from your account")        
            # x=(amt*2)/100
            # finalAmt=bal-(amt+(amt*2)/100)
            client.update_one({"acc_no":acc},{"$set":{"balance":bal-(amt+(amt*2)/100)}})
        elif amt<bal and amt<(bal-10000):
            client.update_one({"acc_no":acc},{"$set":{"balance":bal-amt}})
            print("Transaction success ")
        else : print("Wrong input")






while True:
    os.system('clear')
    print("************************************************************")
    print("*================== WELCOME TO ABC Bank ===================*")
    print("************************************************************")
    print("*            (1). Open New Account                         *")
    print("*            (2). Account Detail                           *")
    print("*            (3). Customers List                           *")
    print("*            (4). Transactions                             *")
    print("*            (5). Update Details                           *")
    print("*            (6). Quit                                     *")
    print("************************************************************")

    choice= int(input("Select option : "))
    customer=ABC_Bank()

    if choice==1:
        print(customer.createAccount())
        time.sleep(5)
    elif choice==2:
        print(customer.check_detail(int(input("Account No : "))))
        input("Press enter to exit.")
        time.sleep(1)
    elif choice==3:
        print(customer.customer_list())
        time.sleep(1)
    elif choice==4:
        print(customer.transaction(int(input("Account No : "))))
        time.sleep(5)
    elif choice==5:
        print(customer.update_detail(int(input("Account No : "))))  
        time.sleep(5)
    elif choice==6:
        sys.exit(0)      