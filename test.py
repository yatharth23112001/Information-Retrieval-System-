with open('Documents/doc/Text-1.txt','r+') as file:
    doc = file.read()
    # for line in file.readlines():
    #     print(line)
    for word in doc.split():
        print(word)