import csv
from collections import Counter
import os
import fnmatch




class BookStore:
    # sLoad Books Into A List.
    def __init__(self,ids=[],customerId=""):
        # Book List
        self.books=[]
        # Cart List
        self.cart=[]
        # Final Price
        self.price=0
        self.getFiles()
    # edited Add Selected Book ID To A Cart.
        for i in ids:
            if self.getBook(i):
                self.cart.append(self.getBook(i))
            else:
                if customerId:
                    raise Exception(f"aOrder from {customerId}: book with the ID of {i} Do Not Exist!")
                else:    
                    raise Exception(f"A book with the ID of {i} Do Not Exist!")    
        self.getCartPrice()
        if customerId:
            print(f'{customerId} total price is: {self.price}')
        else:
            print(f'The total price is: {self.price}')
    # Get CSV Files.
    def getFiles(self):
        with open('bookstore.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    book={
                        "book_id":int(row[0]),
                        "book_title":row[1],
                        "price":float(row[2]),
                    }
                    self.books.append(book)
    #  Get Book By ID.
    def getBook(self,id):
        for i in self.books:
            if id == i["book_id"]:
                return i
    # Check if Cart Length is 1, If NOT call the Discount Func.
    def getCartPrice(self):
        if len(self.cart) == 1:
            self.price = round(self.cart[0]["price"],2)
            return self.price
        if len(self.cart) > 1:
            check_mult=[]
            for i in self.cart:
                check_mult.append(i["book_id"])
            counter=Counter(check_mult)
            self.discount_price(counter.most_common())
    def discount_price(self,disc_list):
        # Check how many times a value repeated in the list, And give the selected Discount. 
        for i in disc_list:
            book_price = self.getBook(i[0])["price"]
            self.price += book_price
            if i[1] > 1:
                for x in range(0,i[1]-1):
                    self.price += book_price - (book_price * 0.05)
        books_count =sum([i[1] for i in disc_list] )
        # Last Discount base on item count.
        if books_count == 2:
            self.price = round(self.price - (self.price * 0.10),2)
            return self.price
        if books_count == 3:
            self.price = round(self.price - (self.price * 0.15),2)
            return self.price
        if books_count >= 4:
           self.price = round(self.price - (self.price * 0.20),2)
           return self.price
# Get All Customers Order From .csv File.
class GetCustomers():
    def __init__(self):
        customer_count = len(fnmatch.filter(os.listdir("./customers"), '*.csv'))
        customers={}
        prices={}
        for i in range(0,customer_count):
            with open(f'./customers/customer{i+1}.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                customer=[]
                for row in csv_reader:
                    if line_count == 0:
                        line_count += 1
                    else:
                        customer.append(int(row[0]))
            customers[f"customer{i+1}"]=customer
        for k,v in customers.items():
            prices[k]=BookStore(v,k)
# c=GetCustomers()        #Get All .csv Files from customers Folder #
b = BookStore([1,8,8,9,6,4]) #Create Single BookStore Object#
