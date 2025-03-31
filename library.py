#LIBRARY MANAGEMENT PROGRAM
#PYTHON+MYSQL

import mysql.connector as my
import time
c=my.connect(host='localhost',passwd='rach123',user='rachkanc')
co=c.cursor()
if c.is_connected():
   print('\t\t****WELCOME TO LIBRARY****')
   print('\t\t\t\t -MADE BY RACHIT')
else:   
   print('Connection not build')
q1='create database if not exists library'
co.execute(q1)
q2='use library'
co.execute(q2)
q3='create table if not exists book(ISBN varchar(10),BOOK_TITLE varchar(30),AUTHOR_NAME varchar(30),PUBLISHER varchar(30),PUBLICATION_YEAR int, BOOK_TYPE varchar(10),LANGUAGE varchar(10))'
co.execute(q3)
q4='create table if not exists issue (ISBN varchar(10),BOOK_TITLE varchar(30),ISSUER_NAME varchar(30),DATE_OF_ISSUE varchar(10),CONTACT_NO int)'
co.execute(q4)
q5='create table if not exists returns (ISBN varchar(10),BOOK_TITLE varchar(30),ISSUER_NAME varchar(30),DATE_OF_ISSUE varchar(10),DATE_OF_RETURN varchar(10),FINE float,CONTACT_NO int)'
co.execute(q5) 
c.commit()
 #SEARCHING
def select_type():
   t='y'
   while t=='y':
    print('__SEARCH BY__')
    print('ENTER \"1\" TO SORT BOOKS A-Z')
    print('ENTER \"2\" TO SORT BOOKS Z-A')
    print('ENTER \"3\" TO GROUP BY BOOK TYPE ')       
    print('ENTER \"4\" TO GROUP BY PUBLICATION YEAR')
    print('ENTER \"5\" TO SEARCH BY ISBN')
    print('ENTER \"6\" TO SEARCH BY BOOK TITLE')
    print('ENTER \"7\" TO SEARCH BY AUTHOR')
    print('ENTER \"8\" TO SEARCH BY PUBLISHER')
    print('ENTER \"9\" TO SEARCH BY PUBLICATION YEAR')
    print('ENTER \"10\" TO SEARCH BY BOOK TYPE')
    print('ENTER \"11\" TO SEARCH BY LANGUAGE')
    time.sleep(2)
    choice=int(input('ENTER YOUR CHOICE (1-10): '))
    if choice==1:
        q6='select * from book order by book_title'
        c.commit()
        x1=co.fetchall()
        print('The book you searched for are:')
        time.sleep(1)
        for row in x1:
            print(row)
    elif choice==2:
        q6='select * from book order by book_title desc'
        c.commit()
        x2=co.fetchall()
        print('The book you searched for are:')
        time.sleep(1)
        for row in x2:
            print(row)
    elif choice==3:
        q7='select * from book order by book_type'
        c.commit()
        x3=co.fetchall()
        print('The book you searched for are:')
        time.sleep(1)
        for row in x3:
            print(row)
    elif choice==4:
        print('__SELECT RANGE OF YEAR__')
        print('ENTER\"1\" TO SHOW BOOKS PUBLISHED BEFORE YEAR 2000')
        print('ENTER\"2\" TO SHOW BOOKS PUBLISHED BETWEEN YEAR 2000 TO 2010')
        print('ENTER\"3\" TO SHOW BOOKS PUBLISHED BETWEEN YEAR 2010 TO 2020')
        print('ENTER\"4\" TO SHOW BOOKS PUBLISHED AFTER YEAR 2020')
        ch=int(input('ENTER YOUR CHOICE(1-4):'))
        if ch==1:
            q8="select * from book where publication_year<2000 sort by publication_year "
            c.commit()
            x4=co.fetchall()
            print('The book you searched for are:')
            time.sleep(1)
            for row in x4:
                print(row)
        elif ch==2:
            q9="select * from book where publication_year between 2000 and 2010 sort by publication_year "
            c.commit()
            x5=co.fetchall()
            print('The book you searched for are:')
            time.sleep(1)
            for row in x5:
                print(row)
        elif ch==3:
            q10="select * from book where publication_year between 2011 and 2020 sort by publication_year"
            c.commit()
            x6=co.fetchall()
            time.sleep(1)
            print('The book you searched for are:')
            for row in x6:
                print(row)
        elif ch==4:
            q11="select * from book where publication_year>2020 sort by publication_year"
            c.commit()
            time.sleep(1)
            print('The book you searched for are:')
            x7=co.fetchall()
            for row in x7:
                print(row)
            else :
                print('ENTER CORRECT CHOICE !!')
        elif choice==5:
            q12='select * from book order by language'
            c.commit()
            x8=co.fetchall()
            time.sleep(1)
            print('The book you searched for are:')
            for row in x8:
                print(row)
        elif choice==6:
            a=input('ENTER ISBN OF BOOK YOU WANT TO SEARCH: ')
            q13='select * from where isbn = "{}" '.format = a
            c.commit()
            x9=co.fetchall()
            time.sleep(1)
            print('The book you searched for are:')
            for row in x9:
                print(row)
        elif choice==7:
            a=input('ENTER TITLE OF BOOK YOU WANT TO SEARCH: ')
            q14='select * from where book_title = "{}" '.format (a)
            c.commit()
            x10=co.fetchall()
            time.sleep(1)
            print('The book you searched for are:')
            for row in x10:
                print(row)
        elif choice==8:
            a=input('ENTER AUTHOR OF BOOK YOU WANT TO SEARCH: ')
            q15='select * from where author = "{}" '.format (a)
            c.commit()
            x11=co.fetchall()
            time.sleep(1)
            print('The book you searched for are:')
            for row in x11:
                print(row)
        elif choice==9:
            a=input('ENTER PUBLISHER OF BOOK YOU WANT TO SEARCH: ')
            q16='select * from where publisher = "{}" '.format (a)
            c.commit()
            x13=co.fetchall()
            time.sleep(1)
            print('The book you searched for are:')
            for row in x13:
                print(row)
        elif choice==10:
            a=input('ENTER PUBLICATION_YEAR OF BOOK YOU WANT TO SEARCH: ')
            q17='select * from where publisher_year = "{}" '.format (a)
            c.commit()
            x14=co.fetchall()
            time.sleep(1)
            print('The book you searched for are:')
            for row in x14:
                print(row)
        elif choice==11:
            a=input('ENTER LANGUAGE OF BOOK YOU WANT TO SEARCH: ')
            q18='select * from where language = "{}" '.format (a)
            c.commit()
            x15=c.fetchall()
            time.sleep(1)
            print('The book you searched for are:')
            for row in x15:
                print(row)
        elif choice==12:
            a=input('ENTER TYPE OF BOOK YOU WANT TO SEARCH: ')
            q19='select * from where book_type = "{}" '.format (a)
            c.commit()
            x16=c.fetchall()
            time.sleep(1)
            print('The book you searched for are:')
            for row in x16:
                 print(row)
        
        else:
            print('ENTER CORRECT CHOICE !!')
            print('DO YOU WANT SEARCH MORE ??')
            t=input('ENTER \"yes\" TO ADD MORE AND \"no\" TO EXIT')
def add_book():
    t='yes'
    while t=='yes':
        i=input('ENTER ISBN OF THE BOOK')
        b=input('ENTER TITLE OF THE BOOK')
        a=input('ENTER AUTHOR OF THE BOOK')
        p=input('ENTER PUBLISHER OF THE BOOK')
        py=int(input('ENTER PUBLICATION YEAR OF THE BOOK'))
        t=input('ENTER TYPE OF THE BOOK')
        l=input('ENTER LANGUAGE OF THE BOOK')
        q20="insert into book values('{}','{}','{}','{}',{},'{}','{}')".format(i,b,a,p,py,t,l)
        c.commit()
        time.sleep(1)
        print('BOOK SUCCESSFULLY ADDED !!')
def update_book():
    t=input('DO YOU WANT TO ADD MORE BOOKS (yes OR no)??')
    t='y'
    while t=='y':
        i=input('ENTER ISBN OF THE BOOK YOU WANT TO UPDATE: ')
        print('WHAT DO YOU WANT TO UPDATE??')
        print('ENTER \"1\" TO UPDATE BOOK TITLE')
        print('ENTER \"2\" TO UPDATE AUTHOR NAME')
        print('ENTER \"3\" TO UPDATE PUBLISHER')            
        print('ENTER \"4\" TO UPDATE PUBLICATION YEAR')
        print('ENTER \"5\" TO UPDATE BOOK TYPE')
        print('ENTER \"6\" TO UPDATE LANGUAGE')
        s=int(input('ENTER YOUR CHOICE(1 TO 6)'))
        if s==1:
           a=input('ENTER UPDATED BOOK TITLE: ')
           q21='update book set book_title="{}" where isbn="{}" '.format(a,i)
           c.commit()
           time.sleep(1)
           print('SUCCESSFULLY UPDATED !!')
        elif s==2:
           a=input('ENTER UPDATED AUTHOR NAME: ')
           q22='update book set author_name="{}" where isbn="{}"'.format(a,i)
           c.commit()
           time.sleep(1)
           print('SUCCESSFULLY UPDATED !!')
        elif s==3:
            a=input('ENTER UPDATED PUBLISHER:  ')
            q23='update book set publisher="{}" where isbn="{}"'.format=(a,i)
            c.commit()
            time.sleep(1)
            print('SUCCESSFULLY UPDATED !!')
        elif s==4:
            a=input('ENTER UPDATED PUBLICATION_YEAR:  ')
            q24='update book set publication_year="{}" where isbn="{}"'.format=(a,i)
            c.commit()
            time.sleep(1)
            print('SUCCESSFULLY UPDATED !!')
        elif s==5:
            a=input('ENTER UPDATED BOOK TYPE:  ')
            q25='update book set book_type="{}" where isbn="{}"'.format=(a,i)
            c.commit()
            time.sleep(1)
            print('SUCCESSFULLY UPDATED !!')
        elif s==6:
            a=input('ENTER UPDATED LANGUAGE:  ')
            q24='update book set language="{}" where isbn="{}"'.format=(a,i)
            c.commit()
            time.sleep(1)
            print('SUCCESSFULLY UPDATED !!')
        else:
            time.sleep(1)
            print('ENTER CORRECT CHOICE !!')
        t=input('DO YOU WANT TO UPDATE ANYTHING ELSE(yes or no)??')
def delete_book():
    s=input('ENTER ISBN OF THE BOOK YOU WANT TO DELETE ??')
    time.sleep(1)
    print('THE ITEM DELETED CANNOT BE RETRIVED!!')
    ch=input('ARE YOU SURE YOU WANT TO DELETE ??(y OR n)')
    if ch=='y':
        q25='delete from book where isbn="{}"'.format(s)
        c.commit()
        time.sleep(1)
        print('BOOK DELETED SUCESSFULLY !!')
    elif ch=='n':
        time.sleep(1)
        print('NO ITEM DELETED!!')
    else:
        time.sleep(1)
        print('ENTER CORRECT CHOICE !!')
 #ISSUING A BOOK
def issue_book():
    time.sleep(1)
    print(' ENTER THE FOLLOWING DETAILS T0 ISSUE A BOOK :  ')
    i=input('ENTER ISBN OF THE BOOK YOU WANT TO ENTER: ')
    n=input('ENTER NAME OF ISSER: ')
    d=input('ENTER DATE OF ISSUE(YYYY-MM-DD): ')
    p=int(input('ENTER CONTACT NUMBER OF THE ISSUER: '))
    q26='insert into issue values("{}","{}","{}",{})'.format(i,n,d,p)
    c.commit()
    time.sleep(1)
    print('YOU HAVE SUCCESSFULLY ISSUED THE BOOK !!')
    time.sleep(1)
    print('ENJOY READING!!')
def select_issued():
    t='yes'
    while t=='yes':
        print('HOW DO YOU WANT TO DISPLAY ?')
        print('ENTER \"1\" TO SORT BY ISBN')
        print('ENTER \"2\" TO SORT BY NAME OF ISSUER')
        print('ENTER \"3\" TO SEARCH NAME OF ISSUER')
        s=int(input('ENTER YOU CHOICE (1-3)'))
        ch=int(input('DO YOU WANT TO CONTINUE ?'))
        if ch==1:
            q27='select * from issue order by ISBN'
            c.commit()
            x17=co.fetchall()
            time.sleep(1)
            for row in x17:
                print(row)
        elif ch==2:
            q28='select * from issue order by issuer_name'
            c.commit()
            x18=co.fetchall()
            time.sleep(1)
            for row in x18:
                print(row)
        elif ch==3:
            a=input('ENTER NAME OF ISSUER YOU WANT TO SEARCH:  ')
            q2='select * from issue where issuer_name="{}"'.format(a)
            c.commit()
            x19=co.fetchall()
            time.sleep(1)
            for row in x19:
                print(row)
        else:
            time.sleep(1)
            print('ENTER CORRECT OPTION !!')
        t=print('DO YOU WANT TO CONTINUE ? yes or no')
def update_info():
    t='yes'
    while t=='yes':
        i=input('ENTER ISBN OF THE BOOK ISSUED YOU WANT TO EDIT: ')
        print('ENTER \"1\" TO UPDATE ISSUER NAME')
        print('ENTER \"2\" TO UPDATE DATE OF ISSUE')
        print('ENTER \"3\" TO UPDATE CONTACT INFO')
        s=int(input('ENTER YOUR CHOICE(1 TO 6)'))
        if s==1:
            a=input('ENTER UPDATED ISSUER NAME: ')
            q21='update issue set issuer_name="{}" where isbn="{}"'.format(a,i)
            c.commit()
            time.sleep(1)
            print('SUCCESSFULLY UPDATED !!')
        elif s==2:
            a=input('ENTER UPDATED DATE OF ISSUE: ')
            q22='update issue set date_of_issue="{}" where isbn="{}"' .format(a,i)
            c.commit()
            time.sleep(1)
            print('SUCCESSFULLY UPDATED !!')
        elif s==3:
            a=int(input('ENTER UPDATED CONTACT NUMBER:  '))
            q23='update issue set contact_no="{}" where isbn="{}"'.format=(a,i)
            c.commit()
            time.sleep(1)
            print('SUCCESSFULLY UPDATED !!')
        else :
            print('ENTER CORRECT CHOICE !!')
        t=input('DO YOU WANT TO UPDATE MORE ?? yes OR no  ')
def delete_issuer():
    s=input('ENTER ISBN OF THE BOOK ISSUED YOU WANT TO DELETE : ')
    time.sleep(1)
    print('THE ITEM DELETED CANNOT BE RETRIVED!!')
    ch=input('ARE YOU SURE YOU WANT TO DELETE ??(y OR n)')
    if ch=='y':
        q25='delete from issue where isbn="{}"'.format(s)
        c.commit()
        time.sleep(1)
        print('BOOK ISSUED DELETED SUCESSFULLY !!')
    elif ch=='n':
        time.sleep(1)
        print('NO ITEM DELETED!!')
    else:
        time.sleep(1)
        print('ENTER CORRECT CHOICE !!')
 #RETURN
def return_book():
    time.sleep(1)
    print(' ENTER THE FOLLOWING DETAILS T0 RETURN A BOOK :  ')
    i=input('ENTER ISBN OF THE BOOK YOU WANT TO RETURN: ')
    n=input('ENTER NAME OF ISSER: ')
    d=input('ENTER DATE OF ISSUE(YYYY-MM-DD): ')
    r=input('ENTER DATE OF RETURN(YYYY-MM-DD): ')
    f=float(input('ENTER FINE'))
    p=int(input('ENTER CONTACT NUMBER OF THE ISSUER: '))
    q26='insert into return values("{}","{}","{}","{}",{},{})'.format(i,n,d,r,f,p)
    c.commit()
    time.sleep(1)
    print('YOU HAVE SUCCESSFULLY RETURNED THE BOOK !!')
def select_retun():
    t='yes'
    while t=='yes':
        print('HOW DO YOU WANT TO DISPLAY RETURN INFO ?')
        print('ENTER \"1\" TO SORT BY ISBN')
        print('ENTER \"2\" TO SORT BY NAME OF ISSUER')
        print('ENTER \"3\" TO SEARCH NAME OF ISSUER')
        ch=int(input('ENTER YOU CHOICE (1-3)'))

        if ch==1:
            q27='select * from return order by ISBN'
            c.commit()
            x17=co.fetchall()
            time.sleep(1)
            for row in x17:
                print(row)
        elif ch==2:
            q28='select * from return order by issuer_name'
            c.commit()
            x18=co.fetchall()
            time.sleep(1)
            for row in x18:
                print(row)
        elif ch==3:
            a=input('ENTER NAME OF ISSUER YOU WANT TO SEARCH:  ')
            q2='select * from return where issuer_name="{}"'.format(a)
            c.commit()
            x19=co.fetchall()
            time.sleep(1)
            for row in x19:
                print(row)
        else:
            time.sleep(1)
            print('ENTER CORRECT OPTION !!')
        t=print('DO YOU WANT TO CONTINUE ? yes or no')
def update_info():
    t='yes'
    while t=='yes':
        i=input('ENTER ISBN OF THE BOOK ISSUED YOU WANT TO EDIT: ')
        print('ENTER \"1\" TO UPDATE ISSUER NAME')
        print('ENTER \"2\" TO UPDATE DATE OF RETURN')
        print('ENTER \"3\" TO UPDATE FINE')
        print('ENTER \"4\" TO UPDATE CONTACT INFO')
        s=int(input('ENTER YOUR CHOICE(1 TO 6)'))
        if s==1:
            a=input('ENTER UPDATED ISSUER NAME: ')
            q21='update return set issuer_name="{}" where isbn="{}"' .format(a,i)
            c.commit()
            time.sleep(1)
            print('SUCCESSFULLY UPDATED !!')
        elif s==2:
            a=input('ENTER UPDATED DATE OF RETURN: ')
            q22='update return set date_of_return="{}" where ISBN="{}"'.format(a,i)
            c.commit()
            time.sleep(1)
            print('SUCCESSFULLY UPDATED !!')
        elif s==3:
            a=float(input('ENTER UPDATED FINE: '))
            q23='update return set fine="{}" where ISBN="{}"'.format(a,i)
            c.commit()
            time.sleep(1)
            print('SUCCESSFULLY UPDATED !!')
        elif s==4:
            a=int(input('ENTER UPDATED CONTACT NUMBER:  '))
            q24='update return set contact_no="{}" where isbn="{}"'.format=(a,i)
            c.commit()
            time.sleep(1)
            print('SUCCESSFULLY UPDATED !!')
        else :
            print('ENTER CORRECT CHOICE !!')
        t=input('DO YOU WANT TO UPDATE MORE ?? yes OR no  ')
def delete_return():
    s=input('ENTER ISBN OF THE BOOK RETURNED YOU WANT TO DELETE: ')
    time.sleep(1)
    print('THE ITEM DELETED CANNOT BE RETRIVED!!')
    ch=input('ARE YOU SURE YOU WANT TO DELETE ??(y OR n)')
    if ch=='y':
        q25='delete from return where isbn="{}"'.format(s)
        c.commit()
        time.sleep(1)
        print('BOOK ISSUED DELETED SUCESSFULLY !!')
    elif ch=='n':
        time.sleep(1)
        print('NO ITEM DELETED!!')
    else:
        time.sleep(1)
        print('ENTER CORRECT CHOICE !!')
 # FUNCTIONS TO CALL FUNCTIONS
def books_library():
    print('***WELCOME TO BOOKS SECTION***')
    print('WHAT DO YOU WANT TO DO HERE??')
    print('ENTER \"1\" TO SEARCH BOOKS')
    print('ENTER \"2\" TO ADD BOOKS')
    print('ENTER \"3\" TO UPDATE BOOK INFO ')
    print('ENTER \"4\" TO DELETE A BOOK')
    ch=int(input('ENTER YOUR CHOICE: '))
    if ch==1:
        select_type()
    elif ch==2:
        add_book()
    elif ch==3:
        update_book()
    elif ch==4:
        delete_book()
    else:
        print('ENTER CORRECT OPTION:')
def books_issue():
    print('***WELCOME TO BOOK ISSUE SECTION')
    print('WHAT DO YOU WANT TO DO HERE??')
    print('ENTER \"1\" TO ISSUE A BOOK')
    print('ENTER \"2\" TO SEARCH ISSUER')
    print('ENTER \"3\" TO UPDATE BOOK INFO ')
    print('ENTER \"4\" TO DELETE A BOOK')
    ch=int(input('ENTER YOUR CHOICE: '))
    if ch==1:
        issue_book()  
    elif ch==2:
        select_issued()
    elif ch==3:
        update_info()
    elif ch==4:
        delete_issuer()
    else:
        print('ENTER CORRECT OPTION:')
def books_returned():
    print('***WELCOME TO BOOK RETURN SECTION***')
    print('WHAT DO YOU WANT TO DO HERE??')
    print('ENTER \"1\" TO RETURN A BOOK')
    print('ENTER \"2\" TO SEARCH RETURN INFO')
    print('ENTER \"3\" TO UPDATE RETURN INFO ')
    print('ENTER \"4\" TO DELETE A RETURN INFO')
    ch=int(input('ENTER YOUR CHOICE: '))
    if ch==1:
        return_book()
    elif ch==2:
        select_retun()
    elif ch==3:
        update_info()
    elif ch==4:
        delete_return()
    else:
        print('ENTER CORRECT OPTION !!')
#MAIN PROGRAM 
t='yes'
while t=='yes':
    print('WHAT WOULD YOU LIKE TO DO HERE ??')
    print('ENTER \"1\" TO VIEW BOOKS')
    print('ENTER \"2\" TO ISSUE BOOKS')
    print('ENTER \"3\" TO RETURN BOOKS ')
    ch=int(input('ENTER YOUR CHOICE: '))
    if ch==1:
        books_library()
    elif ch==2:
        books_issue()
    elif ch==3:
        books_returned()
    else : 
        print('ENTER CORRECT CHOICE!!')
    t=input('DO YOU WANT TO DO SOMETHING ELSE ??(yes or no)')
    print('\t\t\t****THANKS FOR VISITING****')