import magnus

fileName = 'script.mg'

if(fileName == '<stdin>'):
    while True:
        text = input('magnus > ')

        result, error = magnus.run(fileName, text)

        if error:
            print(error)
        else:
            print(result)
else:
    with open(fileName, "r") as f:
        text = f.read()
        result, error = magnus.run(fileName, text)
        if error:
            print(error)
        else:
            print(result)