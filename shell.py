import magnus

while True:
    text = input('magnus > ')
    result, error = magnus.run('<stdin>', text)

    if error: print(error.as_string())
    else: print(result)