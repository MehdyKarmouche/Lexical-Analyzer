import lexer

fileName = input("Enter your file name: ")

if(fileName == 'stdin'):
    while True:
        text = input('magnus > ')
        result, error = lexer.run(fileName, text)
        if error:
            print(error)
        else:
            print("\n".join(map(str, result)))

else:
    with open(fileName, "r") as f:
        text = f.read()
        result, error = lexer.run(fileName, text)
        if error:
            print(error)
        else:
            print("\n".join(map(str, result)))
