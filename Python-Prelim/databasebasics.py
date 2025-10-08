import sqlite3
from employee import Employee


conn = sqlite3.connect('employee.db') #instance that where the data is stored, can be a file or an in memory database 
#in memory: connect(':memory:'). use for testing to start with a fresh database each time
#create the file if it does not it exist. if it does, just connect to it 

c = conn.cursor() #call SQLite functions with a cursor 

# c.execute("""CREATE TABLE employees (
#             first text,
#             last text, 
#             pay integer
#             )""") #"""""" represents a docstring. Write a string with multiple lines wihtout breaks

def insert_emp(emp):
    with conn: #within the contex manager, no need for commit statement
        c.execute("INSERT INTO employees VALUES(:first, :last, :pay)", {'first': emp.first, 'last': emp.last, 'pay': emp.pay,})

def get_emps_by_name(lastname):
    c.execute("SELECT * FROM employees WHERE last=:last",{'last': lastname})
    return c.fetchall()

def update_pay(emp, pay):
    with conn:
        c.execute("""UPDATE employees SET pay = :pay
                    WHERE first = :first AND last = :last""",
                  {'first': emp.first, 'last': emp.last, 'pay': pay})

def remove_emp(emp):
    with conn:
        c.execute("DELETE from employees WHERE first = :first AND last = :last",
                  {'first': emp.first, 'last': emp.last})


#comment out table beacuse it's already been made

emp_1 = Employee('John', 'Doe', 80000)
emp_2 = Employee('Jane', 'Doe', 90000)
emp_3 = Employee('Jerry', 'Rivers', 9910000000000009)


#using methods above 
insert_emp(emp_3)

emps = get_emps_by_name('Rivers')
print(emps)

update_pay(emp_3, 9500000)
remove_emp(emp_2)


#String formatting method for adding instances into database. Do not do this, vulnerable to SQL Injections 
#c.execute("INSERT INTO employees VALUES('{}', '{}', {})".format(emp_1.first, emp_1.last, emp_1.pay))

#Correct way to insert data
#1. DB API Placeholder 
# c.execute("INSERT INTO employees VALUES(?, ?, ?)", (emp_1.first, emp_1.last, emp_1.pay))
# conn.commit()

#2. placeholder/dictonary and placeholder/dictonary key (more readable)
# c.execute("INSERT INTO employees VALUES(:first, :last, :pay)", {'first': emp_2.first, 'last': emp_2.last, 'pay': emp_2.pay,})
# conn.commit()


#c.execute("INSERT INTO employees VALUES('Mary', 'Schafer', 50000)")
#comment out because it was already added 
#conn.commit

#hardcode database
c.execute("SELECT * FROM employees WHERE last='Schafer'") #query for employees with lat name schafer 
print(c.fetchall())

#method 1
c.execute("SELECT * FROM employees WHERE last=?",('Doe',)) #always put a comma even for one value because it is a tuple
#print(c.fetchone()) #return the top or very next row after the SELECT command has been called
#c.fetchmany(5) #takes in a number and returns that many rows as a list. If none, return empty
print(c.fetchall()) #returns all occurences as a lsit. If none, return an empty list

#method 2
c.execute("SELECT * FROM employees WHERE last=:last",{'last': 'Doe'})
print(c.fetchall())

conn.commit() #commit changes 

conn.close #close connection
