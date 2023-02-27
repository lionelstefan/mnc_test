inputs = input("")
open = [
    "<",
    "{",
    "["
]
close = [
    ">",
    "}",
    "]"
]

if len(inputs) > 4096:
    print("false")

stack = []
for index, element in enumerate(inputs):
    if element in open:
        stack.append(element)

    if element in close:
        if len(stack) > 0 and (open[close.index(element)] == stack[len(stack)-1]):
            stack.pop()
        else:
            print(False)
            quit()

if len(stack) == 0 : 
    print(True)
    quit()

print(False)
