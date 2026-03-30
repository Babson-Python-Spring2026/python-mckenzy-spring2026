cach = 10000
positions = {"APPL" : 10, "MSFT" : 5}
prices = {"APPL" : 190, "MSFT" : 420}

port = {"cash" : 10000.00,
        "positions" : [{"symb": "APPL" , 
                        "shares": 10, 
                        "price" : 190,
                        "symb": "MSFT" , 
                        "shares": 5, 
                        "price" : 420}]}

def buy_stock(port):

    sym = input("Enter your stock symbol that you want to buy: ")
    txt = input("Enter the shares you want to buy: ")

    while True:
        try:
            shares = int(input(txt))
            breakS
        except ValueError:
            txt = "You must unter an integer"
            

    txt = f"enter the price of {sym}: "

    while True:
        try:
            price = float(input(txt))
            break
        except ValueError:
            txt = "You must enter a float"
        
        if shares * price > port["cash"]:
            print("insufficient cash. transaction denied")
            return none
        else:
            new_position = {"sym" : sym,
                            "shares": shares,
                            "price": price}
            port["positions".append(new_position)]
            return none
            
    

