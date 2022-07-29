class PascalList:
    def __init__(self, orirginal_list=None):
        self.container = orirginal_list or []

    def __getitem__(self, index):
        return self.container[index - 1]

    def __setitem__(self, index, value):
        self.container[index - 1] = value

    def __str__(self):
        return self.container.__str__()


numbers = PascalList([1, 2, 3, 4, 5])

print(numbers[1])

numbers[5] = 25
print(numbers)


