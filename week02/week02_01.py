import argparse
import json
import os
import tempfile


def read_data(storage_path):
    if not os.path.exists(storage_path):
        return {}

    with open(storage_path, 'r') as file:
        raw_data = file.read()
        if raw_data:
            return json.loads(raw_data)
        return {}


def write_data(storage_path, data):
    with open(storage_path, 'w') as f:
        f.write(json.dumps(data))


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', help='Key')
    parser.add_argument('--val', help='Value')
    return parser.parse_args()


def put(storage_path, key, value):
    data = read_data(storage_path)
    data[key] = data.get(key, list())
    data[key].append(value)
    write_data(storage_path, data)


def get(storage_path, key):
    data = read_data(storage_path)
    return data.get(key, [])


def main(storage_path):
    args = parse()

    if args.key and args.val:
        put(storage_path, args.key, args.val)
    elif args.key:
        print(*get(storage_path, args.key), sep=', ')
    else:
        print('The program is called with invalid parameters.')


if __name__ == '__main__':
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    main(storage_path)

# Мой код!!!
# import argparse
# import json
# import os
# import tempfile
#
# dict_all = dict()
# parser = argparse.ArgumentParser()
# parser.add_argument("--key")
# parser.add_argument("--val")
# args = parser.parse_args()
#
# storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
# if os.path.exists(storage_path):
#     with open(storage_path, 'r') as f:
#         dict_all = json.load(f)
#     if args.val is None:
#         if args.key in dict_all.keys():
#             print(', '.join(dict_all[args.key]))
#     else:
#         if args.key in dict_all.keys():
#             tuple_temp = dict_all[args.key]
#             tuple_temp.append(args.val)
#         else:
#             tuple_temp = [args.val]
#         dict_all[args.key] = tuple_temp
# else:
#     dict_all[args.key] = [args.val]
# with open(storage_path, 'w') as f:
#     json.dump(dict_all, f)
