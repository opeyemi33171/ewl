import requests, os
from bs4 import BeautifulSoup
import mysql.connector


#set database setting from envirnoment varibles.
mydb = mysql.connector.connect(
    host = os.environ.get('MYSQL_HOST'),
    port = os.environ.get('MYSQL_PORT'),
    user = os.environ.get('MYSQL_USER'),
    passwd = os.environ.get('MYSQL_PASSWORD'),
    database = os.environ.get('MYSQL_DB'),
    auth_plugin='mysql_native_password'
    )

#cursor object used to execute sql queries against database.
cursor = mydb.cursor(buffered=True)

#queries to be executed.
selectQuery = """SELECT * FROM books"""
insertQuery = """UPDATE books Set name=%s, price=%s WHERE link=%s """
deleteQuery = """DELETE FROM books"""

#array stores all book links available
bookLinks = []

#updateQuery = """ UPDATE books Set"""

#selects all the books in books tables
cursor.execute(selectQuery)

#store all books links into bookLinks(array) 
for entry in cursor:
    print(entry)
    bookLinks.append(entry[4])

#delete all book entries in books tables
#cursor.execute(deleteQuery)
    

#definition of book properties to store in db
class Book:
   def __init__(self, name, price):
        self.name = name
        self.price = price


   def addLink(self, link):
        self.link = link
        

   def getLink(self):
       return self.link

    

def getPageHtml(link):
     res = requests.get(link)
     return res.text

def createBook(link):
    price = ""

    html = getPageHtml(link)
    bSoup = BeautifulSoup(html, 'html.parser')
    
    name = bSoup.select('.book-title')[0].getText()
    priceTag = bSoup.select('b')
    for element in priceTag:
        try:
            if element.attrs['itemprop'] == "price":
                price = element.getText()
        except KeyError:
             continue

    book = Book(name, price)
    book.addLink(link)

    return book

for link in bookLinks:
    book = createBook(link)
   
    try:
         cursor.execute(insertQuery, (book.name, book.price, book.getLink()))
    except mysql.connector.Error as err:
        print("Failed to execute query {}".format(err))
        


   
mydb.commit()
cursor.close()
mydb.close()
