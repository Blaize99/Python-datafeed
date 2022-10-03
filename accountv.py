import pickle

#to create an account as administrator or as a customer
def accr():
    i=1
    x=open("Account4",'ab+')
    x.seek(0)
    r={}
    name=input("Enter Your name")
    age=int(input("Enter age"))
    email=input("Enter your email ID")
    if email[-4:-1]=='.co':
        found=False
        try:
            while True:
                st=pickle.load(x)
                if st['email']==email:
                    found=True
        except EOFError:
            if found==True:
                print('Account exists')
            else:
                phone=int(input("Enter your contact number "))
                atype=int(input("Account Type \n 1.Customer \n 2.Administrator\n"))
                password=input("Please enter a suitable password for your account\n")
                r['name']=name
                r['age']=age
                r['email']=email
                r['phone']=phone
                r['password']=password
                r['atype']=atype           
                x.seek(0,2)
                pickle.dump(r,x)
                x.close()
                print('Account Created')
                return 0      
    else:
        print('invalid mail address')
def acclog():
    email=input("Enter email ID")
    x=open("Account4",'rb+')
    found=False
    try:
        while True:
            st=pickle.load(x)
            if st['email']==email:
                found=True
                cd=st['name']
                dc=st['atype']
                ty=st['email']
    except EOFError:
        if found==True:
            print('Login Successfull')
            x.close()
            return cd,dc,0,ty
        else:
            print('Account does not exist')

# to login to admin page and make the nessasary changes
def admin():
    import mysql.connector as msc
    j='y'
    while j=='y' or j=='Y':
        print("\t\t1.Insertion of new product","\t\t2.Deletion of a product","\t\t3.Product discount",sep='\n')
        t=int(input()) 
        if t==1:
            a='y'
            while a=='y' or a=='Y':
                i=int(input("\t\tEnter the item number "))
                b=input("\t\tEnter the category of item ")
                c=input("\t\tEnter the name of the item ")
                d=input("\t\tEnter colour ")
                a=float(input("\t\tEnter size "))
                m=float(input("\t\tEnter the price "))
                k=input("\t\tEnter manufacturer details ")
                r=int(input("\t\tEnter the number of items present "))
                # enter your password and database
                con=msc.connect(host="localhost",user="root",passwd="",database="blaize")
                cur=con.cursor()
                query="insert into amazon(item_no,item,item_name,colour,size,cost,manufacturer,item_left) values({},'{}','{}','{}',{},{},'{}',{})".format(i,b,c,d,a,m,k,r)
                cur.execute(query)               
                con.commit()
                print("\t\tSucessfully inserted ")
                a=input("\t\tDo you want to enter another product ")
            con.close()
        if t==3:
            # enter your password and database
            con=msc.connect(host="localhost",user="root",passwd="",database="blaize")
            cur=con.cursor()
            a='y'
            while a=='y' or a=='Y':
                b=int(input("\t\tEnter the item number of the item you want to give discount "))
                cur.execute("select * from amazon where item_no={}".format(b,))
                data=cur.fetchall()
                if data==[]:
                    print("\t\tNo such item")
                else:
                    print(data)
                    k=int(input("\t\tEnter the discount amount "))
                    y=data[0]
                    r=y[5]
                    y=list(y) 
                    r=int(r)
                    if r<=k:
                        print("\t\tDiscount cannot be more than the price of the item")
                    else:
                        r=r-k
                        del y[5]
                        y.insert(5,r)
                        cur.execute("delete from amazon where item_no={}".format(b,))
                        con.commit()
                        cur.execute("insert into amazon(item_no,item,item_name,colour,size,cost,manufacturer,item_left) values({},'{}','{}','{}',{},{},'{}',{})".format(y[0],y[1],y[2],y[3],y[4],y[5],y[6],y[7]))
                        con.commit()
                        cur.execute("select * from amazon where item_no={}".format(b,))
                        data=cur.fetchall()
                        for i in data:
                            print(i)
                a=input("\t\tDo you wish to continue ")
            con.close()
        if t==2:
            # enter your password and database
            con=msc.connect(host="localhost",user="root",passwd="",database="blaize")
            csr=con.cursor()
            a='y'
            while a=='y' or a=='Y':
                r=int(input("Enter the number of the item you want to delete "))
                csr.execute("select * from amazon where item_no={}".format(r,))
                data=csr.fetchall()
                if data==[]:
                    print("no such item")
                else:
                    for j in data:
                        i=len(j)-1
                        if j[i]==0:
                            csr.execute("delete from amazon where item_no={}".format(r,))
                            con.commit()
                        else:
                            print("Stock still left for this item. Cannot be deleted")
                a=input("Do you wish to delete another item ")
                con.close()
        j=input("\t\tDo you wish to stay in administerator page ")

# to search for a product
def search(d):
    import mysql.connector as msc
    # enter your password and database
    con=msc.connect(host="localhost",user="root",passwd="",database="blaize")
    csr=con.cursor()
    z='y'
    while z=='y' or z=='Y':
        a=0
        while a==0:
            b=input("Enter the item you want to search ")
            csr.execute("select * from amazon where item='{}'".format(b,))
            data=csr.fetchall()
            data=list(data)
            if data==[]:
                print("No such item found ")
                a=1
                k='b'
            else:
                a=1         
                k=input("Do you want to fiter the search y/n ")
        while k=='y' or k=='Y':
            print("1.sort by price","2.sort by brand","3.sort by colour", "4.sort by size" ,sep='\n')      
            n=int(input())
            s=0
            if n==1:
                l=int(input("Enter your budget price "))
                for i in data:
                     if i[5]<=l:
                        print(i)
                        s=s+1
                        k='b'
                if s==0:
                    print("No",b,"below this price is available ")  
            elif n==2:
                l=input("enter the brand")
                for i in data:
                    if i[6]==l:
                        print(i)
                        s=s+1
                        k='b'
                if s==0:
                    print("The brand is not available ")        
            elif n==3:
                l=input("Enter the colour you want ")
                for i in data:
                    if i[3]==l:
                        print(i)
                        s=s+1
                        k='b'
                if s==0:
                    print("The colour you searched for is not available")    
            elif n==4:
                l=float(input("Enter the size "))
                for i in data:
                    if i[4]==l:
                        print(i)
                        s=s+1
                        k='b'
                if s==0:
                     print("This size is not available for this product ")         
            else:
                print("Wrong choice")
        if k!='y' and k!='b':
            for i in data:
                print(i)
        u=input("Do you wish to add anything to the cart y/n ")
        if u=='y' or u=='Y':
            l='y'
            while l=='y' or l=='Y':
                b=int(input("\t\tEnter the item number you want to add to cart "))
                csr.execute("select * from amazon where item_no={}".format(b,))
                data=csr.fetchall()
                if data==[]:
                    print("\t\tNo such item")
                else:
                    for i in data:
                        l=i
                        email=d[3]
                        csr.execute("insert into cart(item_no,item,item_name,colour,size,cost,manufacturer,item_left,email) values({},'{}','{}','{}',{},{},'{}',{},'{}')".format(l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7],email))
                        con.commit()

            l=input("\t\tDo you wish to add anything else to the cart y/n ")
        z=input("\t\tDo you want to search another item y/n ")
    con.close()    
    w=input("\t\tDo you wish to buy anythng from the cart y/n ")
    if w=='y' or w=='Y':
        return 1

# to buy a product
def buy(d):
    import mysql.connector as msc
    # enter your password and database
    con=msc.connect(host='localhost',user='root',passwd='',database='blaize')
    cur=con.cursor()
    email=d[3]
    cur.execute("select * from cart where email='{}'".format(email,))
    data=cur.fetchall()
    if data==[]:
        print("\t\tNo items in your cart ")
        search(d)
    else:
        for i in data:
            print(i)
        l=input("\t\tDo you wish to delete any item form the cart y/n ")
        while l=='y' or l=='Y':
            b=int(input("Enter the item number you want to delete "))
            cur.execute("delete from cart where item_no={}".format(b,))
            con.commit()
            l=input("\t\tDo you wish to delete any more item from the cart y/n ")
        cur.execute("select * from cart where email='{}'".format(email,))
        data=cur.fetchall()     
        con.close()
        sum=0
        c=[]                
        for i in data:
            sum+=i[5]
            c.append(i[1])            
        print("\t\tThe amount you have to pay is",sum,"rupees ")
        x=input("\t\tEnter you address in a single line ")
        print("\n PAYMENT PAGE ")
        a1=int(input("Enter your card number "))
        a2=input("Enter your name ")
        a3=int(input("Enter CVV (Last 3 digits) "))
        print("PROCESSING...... ")
        print("Transaction successfull ") 
        f=d[0]
        print("item",c,'has been dispatched to',f,'to the location',x)
        for i in data:
            b=i[0]
            # enter your password and database
            con=msc.connect(host="localhost",user="root",passwd="",database="blaize")
            cur=con.cursor()
            cur.execute("select * from amazon where item_no={}".format(b,))
            d=cur.fetchall()
            y=data[0]
            r=y[7]
            y=list(y) 
            r=int(r)           
            r=r-1
            del y[7]
            y.insert(7,r)
            cur.execute("delete from amazon where item_no={}".format(b,))
            con.commit()
            cur.execute("insert into amazon(item_no,item,item_name,colour,size,cost,manufacturer,item_left) values({},'{}','{}','{}',{},{},'{}',{})".format(y[0],y[1],y[2],y[3],y[4],y[5],y[6],y[7]))
            con.commit()

#main program
w='y'
while w=='y' or w=='Y':
    print("Welcome To AMAZON.COM")
    print("1.Sign up \n 2.Login \n 3.Exit \n")
    n=int(input("Choose your option "))
    pr=1
    ps=1
    if n==1:
        while pr==1:
            pr=accr()
            n=2
    elif n==2:
        while ps==1:
            d=acclog()
            ps=d[2]
    else:
        print("Thank you for visiting us ")
        break
    while ps==0:
        print("WELCOME TO AMAZON")
        if d[1]==2:
            admin()
            break
        else:
            o=search(d)
            if o==1:
                buy(d)
            break    
    w=input("do you wish to continue the program")           
