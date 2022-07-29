import os
import tempfile


class File:

    def __init__(self, path_to_file):
        if not os.path.exists(path_to_file):
            # open(self.path, 'w').close()
            with open(path_to_file, 'w') as f:
                f.write("")
        self.path_to_file = path_to_file
        self.current = 0
        self.end = os.path.getsize(self.path_to_file)

    def read(self):
        """
        чтение из файла, метод read возвращает
        строку с текущим содержанием файла
        """
        with open(self.path_to_file, "r") as f:
            return f.read()

    def write(self, new_string):
        """"
        запись в файл, метод write принимает в
        качестве аргумента строку с новым содержанием файла
        """
        with open(self.path_to_file, "w") as f:
            return f.write(new_string)
        # return os.path.getsize(self.path_to_file)

    def __add__(self, obj):
        new_file_obj = File(os.path.join(tempfile.gettempdir(), "new_filename"))
        # new_file_obj.write(self.read() + obj.read())
        with open(new_file_obj.path_to_file, "w") as f:
            f.write(self.read())
            f.write(obj.read())
        new_file_obj.current = 0
        new_file_obj.end = os.path.getsize(new_file_obj.path_to_file)
        return new_file_obj

    def __str__(self):
        return os.path.join(tempfile.gettempdir(), self.path_to_file)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.end:
            raise StopIteration
        with open(self.path_to_file, "r") as f:
            f.seek(self.current)
            line_in_file = f.readline()
            self.current = f.tell()
            return line_in_file

        # with open(self.path, 'r') as f:
        #     f.seek(self.current_position)
        #
        #     line = f.readline()
        #     if not line:
        #         self.current_position = 0
        #         raise StopIteration('EOF')
        #
        #     self.current_position = f.tell()
        #     return line


path_to_file = 'some_filename'
print(os.path.exists(path_to_file))

file_obj = File(path_to_file)
print(os.path.exists(path_to_file))
print(file_obj.read())
print(file_obj.write('some text'))
print(file_obj.read())
print(file_obj.write('other text'))
print(file_obj.read())

file_obj_1 = File(path_to_file + '_1')
file_obj_2 = File(path_to_file + '_2')
file_obj_1.write('line 1\n')
file_obj_2.write('line 2\n')
new_file_obj = file_obj_1 + file_obj_2
print(isinstance(new_file_obj, File))
print(new_file_obj)
for line in new_file_obj:
    print(ascii(line))
