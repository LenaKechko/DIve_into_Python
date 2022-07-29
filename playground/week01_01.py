import sys

digit_string = sys.argv[1]

if digit_string.isdigit():
    my_digit = int(digit_string)
    result = 0
    while my_digit != 0:
        result += my_digit % 10
        my_digit //= 10
    print(result)
# print(sum([int(x) for x in sys.argv[1]]))
