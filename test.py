def new_line(text: str):
    textList = text.split("\n")
    result = ""
    for text in textList:
        result += f"{text}\n"
    print(result)


a = "123\n456"
# new_line("123\n456")
print(a)
