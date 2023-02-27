input_total = input('')
list_string = list()

for i in range(int(input_total)):
    list_string.append(
        str(input("")).lower()
    )

temp_index = list()

for index, x in enumerate(list_string):
    temp = index + 1
    for idx, x_inner in enumerate(list_string):
        if (idx > index and x == x_inner):
            if (len(temp_index) < 2): temp_index.append(temp)
            temp_index.append(idx + 1)
    
    if len(temp_index) > 1:break

print(
    temp_index if len(temp_index) > 0 else "false"
)
