import asyncio


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol,
                              host, port
                              )
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class ClientServerProtocol(asyncio.Protocol):
    dict_data = {}

    def process_data(self, data):
        try:
            if not data.endswith('\n'):
                return "error\nwrong command\n\n"
            command, data = data.split(" ", 1)
            if command == "put":
                try:
                    key, value, timestamp = data.split(" ")
                    if key not in self.dict_data:
                        self.dict_data[key] = {}
                    self.dict_data[key][int(timestamp.strip())] = float(value)
                    return "ok\n\n"
                except Exception:
                    return "error\nwrong command\n\n"
            elif command == "get":
                if data == "*\n":
                    try:
                        result = f"ok\n"
                        print(result)
                        for key in self.dict_data.keys():
                            for timestamp, value in self.dict_data[key].items():
                                result += f"{key} {value} {timestamp}\n"
                        result += f"\n"
                        return result
                    except Exception:
                        return "error\nwrong command\n\n"
                else:
                    try:
                        key = data.strip()
                        if key.count(" ") != 0 or key in {"", " "}:
                            return "error\nwrong command\n\n"
                        if key not in self.dict_data:
                            return "ok\n\n"
                        result = f"ok\n"
                        for timestamp, value in self.dict_data[key].items():
                            result += f"{key} {value} {timestamp}\n"
                        result += f"\n"
                        print("ok\n\n")
                        return result
                    except Exception:
                        return "error\nwrong command\n\n"
            else:
                return "error\nwrong command\n\n"
        except Exception:
            return "error\nwrong command\n\n"

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        try:
            resp = self.process_data(data.decode())
        except Exception:
            resp = f"error\nwrong command\n\n"
        self.transport.write(resp.encode())


# if __name__ == "__main__":
#     run_server("127.0.0.1", 8181)

# Код преподавателей!!!
# import asyncio
# from collections import defaultdict
# from copy import deepcopy
#
#
# class StorageDriverError(ValueError):
#     pass
#
#
# class Storage:
#     """Класс для хранения метрик в памяти процесса"""
#
#     def __init__(self):
#         self._data = defaultdict(dict)
#
#     def put(self, key, value, timestamp):
#         self._data[key][timestamp] = value
#
#     def get(self, key):
#
#         if key == '*':
#             return deepcopy(self._data)
#
#         if key in self._data:
#             return {key: deepcopy(self._data.get(key))}
#
#         return {}
#
#
# class StorageDriver:
#     """Класс, предосталяющий интерфейс для работы с хранилищем данных"""
#
#     def __init__(self, storage):
#         self.storage = storage
#
#     def __call__(self, data):
#
#         method, *params = data.split()
#
#         if method == "put":
#             key, value, timestamp = params
#             value, timestamp = float(value), int(timestamp)
#             self.storage.put(key, value, timestamp)
#             return {}
#         elif method == "get":
#             key = params.pop()
#             if params:
#                 raise StorageDriverError
#             return self.storage.get(key)
#         else:
#             raise StorageDriverError
#
#
# class MetricsStorageServerProtocol(asyncio.Protocol):
#     """Класс для реализации сервера при помощи asyncio"""
#
#     # Обратите внимание на то, что storage является атрибутом класса, что предоставляет
#     # доступ к хранилищу данных для всех экземпляров класса MetricsStorageServerProtocol
#     # через обращение к атрибуту self.storage.
#     storage = Storage()
#     # настройки сообщений сервера
#     sep = '\n'
#     error_message = "wrong command"
#     code_err = 'error'
#     code_ok = 'ok'
#
#     def __init__(self):
#         super().__init__()
#         self.driver = StorageDriver(self.storage)
#         self._buffer = b''
#
#     def connection_made(self, transport):
#         self.transport = transport
#
#     def data_received(self, data):
#         """Метод data_received вызывается при получении данных в сокете"""
#
#         self._buffer += data
#
#         try:
#             request = self._buffer.decode()
#             # ждем данных, если команда не завершена символом \n
#             if not request.endswith(self.sep):
#                 return
#
#             self._buffer, message = b'', ''
#             raw_data = self.driver(request.rstrip(self.sep))
#
#             for key, values in raw_data.items():
#                 message += self.sep.join(f'{key} {value} {timestamp}' \
#                                          for timestamp, value in sorted(values.items()))
#                 message += self.sep
#
#             code = self.code_ok
#         except (ValueError, UnicodeDecodeError, IndexError):
#             message = self.error_message + self.sep
#             code = self.code_err
#
#         response = f'{code}{self.sep}{message}{self.sep}'
#         # отправляем ответ
#         self.transport.write(response.encode())
#
#
# def run_server(host, port):
#     loop = asyncio.get_event_loop()
#     coro = loop.create_server(MetricsStorageServerProtocol, host, port)
#     server = loop.run_until_complete(coro)
#
#     try:
#         loop.run_forever()
#     except KeyboardInterrupt:
#         pass
#
#     server.close()
#     loop.run_until_complete(server.wait_closed())
#     loop.close()
#
#
# if __name__ == "__main__":
#     run_server("127.0.0.1", 8888)