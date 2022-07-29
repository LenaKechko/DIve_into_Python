import csv
import os.path


class CarBase():
    """базовый класс для транспортных средств"""

    # атрибут для хранения обязательных параметров класса, описывающего транспортное средство
    required = []

    def __init__(self, brand, photo_file_name, carrying):
        self.brand = self.validate_input(brand)
        self.photo_file_name = self.validate_photo_filename(photo_file_name)
        self.carrying = float(self.validate_input(carrying))

    def validate_input(self, value):
        """метод валидации данных, возвращает значение, если оно валидно,
        иначе выбрасывает исключение ValueError"""
        if value == '':
            raise ValueError
        return value

    def validate_photo_filename(self, filename):
        for ext in ('.jpg', '.jpeg', '.png', '.gif'):
            if filename.endswith(ext) and len(filename) > len(ext):
                return filename
        raise ValueError

    def get_photo_file_ext(self):
        _, ext = os.path.splitext(self.photo_file_name)
        return ext

    @classmethod
    def create_from_dict(cls, data):
        """создает экземпляр класса из словаря с параметрами"""
        parameters = [data[parameter] for parameter in cls.required]
        return cls(*parameters)


class Car(CarBase):
    """класс описывающий автомобили для перевозок людей"""
    car_type = "car"
    required = ['brand', 'photo_file_name', 'carrying', 'passenger_seats_count']

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(self.validate_input(passenger_seats_count))


class Truck(CarBase):
    """класс описывающий автомобили для перевозок грузов"""
    car_type = "truck"
    required = ['brand', 'photo_file_name', 'carrying', 'body_whl']

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.body_length, self.body_width, self.body_height = self.parse_whl(body_whl)

    def get_body_volume(self):
        """возвращает объем кузова"""
        return self.body_length * self.body_width * self.body_height

    def parse_whl(self, body_whl):
        """возвращает реальные размеры кузова length, width, height"""
        try:
            length, width, height = (float(c) for c in body_whl.split("x", 2))
        except Exception:
            length, width, height = 0.0, 0.0, 0.0
        return length, width, height


class SpecMachine(CarBase):
    """класс описывающий спецтехнику"""

    car_type = "spec_machine"
    required = ['brand', 'photo_file_name', 'carrying', 'extra']

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = self.validate_input(extra)


def get_car_list(csv_filename):
    """возвращает список объектов, сохраненных в файле csv_filename"""

    car_types = {'car': Car, 'spec_machine': SpecMachine, 'truck': Truck}
    csv.register_dialect('cars', delimiter=';')
    car_list = []

    with open(csv_filename, 'r') as file:
        reader = csv.DictReader(file, dialect='cars')
        for row in reader:
            try:
                car_class = car_types[row['car_type']]
                car_list.append(car_class.create_from_dict(row))
            except Exception:
                pass

    return car_list


if __name__ == '__main__':
    pass

# Мой код
# import os
# import csv
#
#
# class CarBase:
#     def __init__(self, brand, photo_file_name, carrying):
#         self.photo_file_name = photo_file_name
#         self.brand = brand
#         self.carrying = float(carrying)
#
#     """
#         метод get_photo_file_ext для получения
#         расширения файла изображения
#     """
#
#     def get_photo_file_ext(self):
#         return os.path.splitext(self.photo_file_name)[-1]
#
#
# class Car(CarBase):
#     def __init__(self, brand="", photo_file_name="",
#                  carrying=0.0, passenger_seats_count=0):
#         self.car_type = "car"
#         super().__init__(brand, photo_file_name, carrying)
#         self.passenger_seats_count = int(passenger_seats_count)
#
#
# class Truck(CarBase):
#     def __init__(self, brand="", photo_file_name="",
#                  carrying=0.0, body_whl=""):
#         self.car_type = "truck"
#         super().__init__(brand, photo_file_name, carrying)
#         try:
#             [self.body_length, self.body_width, self.body_height] = list(map(float, body_whl.split("x")))
#         except ValueError:
#             [self.body_length, self.body_width, self.body_height] = [0.0, 0.0, 0.0]
#
#     def get_body_volume(self):
#         return self.body_width * self.body_height * self.body_length
#
#
# class SpecMachine(CarBase):
#     def __init__(self, brand="", photo_file_name="",
#                  carrying=0.0, extra=""):
#         self.car_type = "spec_machine"
#         super().__init__(brand, photo_file_name, carrying)
#         self.extra = extra
#
#
# def get_car_list(csv_filename):
#     car_list = []
#     with open(csv_filename) as csv_fd:
#         reader = csv.reader(csv_fd, delimiter=";")
#         next(reader)  # пропускаем заголовок
#         for row in reader:
#             try:
#                 if (row[0] == "") or (row[0] not in ["car", "truck", "spec_machine"]) or (row[1] == "") or \
#                         (row[3] == "") or (os.path.splitext(row[3])[-1] not in [".jpg", ".jpeg", ".png", ".gif"]) or \
#                         row[5] == "":
#                     raise ValueError
#                 elif row[0] == "car":
#                     if not (row[2].isdigit()):
#                         raise ValueError
#                     car_list.append(Car(brand=row[1], passenger_seats_count=row[2],
#                                         photo_file_name=row[3], carrying=row[5]))
#                 elif row[0] == "truck":
#                     car_list.append(Truck(brand=row[1], photo_file_name=row[3],
#                                           body_whl=row[4], carrying=row[5]))
#                 else:
#                     if row[6] == "":
#                         raise ValueError
#                     car_list.append(SpecMachine(brand=row[1], photo_file_name=row[3],
#                                                 carrying=row[5], extra=row[6]))
#             except ValueError as err:
#                 continue
#             except IndexError:
#                 break
#     return car_list
