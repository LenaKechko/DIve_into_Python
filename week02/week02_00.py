"""
Напишите функцию, которая превращает
список чисел в список строк.
"""


def stringify_list(num_list):
    return list(map(str, num_list))


print(stringify_list(range(10)))

# def preobr(args):
#     list_temp = list()
#     for element in args:
#         list_temp.append(str(element))
#     return list_temp
#
#
# list_number = list()
# for number in range(10):
#     list_number.append(number)
# print(list_number)
#
#
# list_str = preobr(list_number)
# print(list_str)

# def F(a):
#     return str(a)
#
#
# # list_str = list(map(F, range(10)))
#
# list_number = list()
# for number in range(10):
#     list_number.append(number)
# print(list_number)
#
# list_str = list(map(F, [x for x in list_number]))
# print(list_str)