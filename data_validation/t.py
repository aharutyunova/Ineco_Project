def max_value(num_list):
    max = num_list[0]
    for i in num_list[1:]:
        if i > max:
            max = i
    return max
a = (input("Enter list of nums in space:"))
print(f"Maximum value is:  {max_value(a)}")  