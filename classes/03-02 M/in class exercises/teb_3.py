# Goal: Keep asking until valid integer
# Keep asking for an integer until the user enters a valid one.

prompt = 'Entet an ineger : '
while True:

    try:
        x = int(input(prompt))
    except ValueError:
        prompt = 'listen dummy enter an integer'
    else:
        print(x)
        break 

#else happens if there are no errors
