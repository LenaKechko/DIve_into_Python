from week03_01 import FileReader

reader = FileReader("not_exist_file.txt")
text = reader.read()
print(text)

reader = FileReader('some_file.txt')
text = reader.read()
print(text)
