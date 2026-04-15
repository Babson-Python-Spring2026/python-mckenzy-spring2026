class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)
    
    def is_square(self):
        if self.width == self.height:
            print("This is a square")
            return True
        
        else:
            print("This is not a square")
            return False

rect1 = Rectangle(9,8)
rect2 = Rectangle(4,5)

'''
print(rect1.area())
print(rect1.perimeter())
'''

print(rect1.is_square())


class Box:
    def __init__(self,value):
        self.value = value
    def add_one(self):
        self.count += 1
myint = Box(5)

student = {
    "name": "Ana",
    "score": 92
}

class Student:
    def __init__(self, name,score):
        self.name = name
        self.score = score
       
    def describe_self(self):
        print(f'{self.name} has the grade {self.score}')


student1 = Student("Ana",95)
describe_self(student1)


class PortfolioSystem:
    def __init__(self, prices_dates, prices_tickers, ticker_universe, mkt_dates):
        self.ticker_universe = ticker_universe
        self.mkt_dates = mkt_dates

    def get_num_market_dates(self):
        return len(self.mkt_dates)

    def get_num_tickers(self):
        return len(self.ticker_universe)

    def is_valid_ticker(self, ticker):
        return ticker in self.ticker_universe
    
    def get_first_market_date(self):
        return self.mkt_dates[0]
    
my_Port = PortfolioSystem([],[])




