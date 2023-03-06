data = {
    'user': {
        'name': 'axel',
        'adress': {
            'line_1': 'jaja',
            'line_2': 'jeje'
            }
        }
    }

def exist(obj:dict, args):
    if actual_dict := obj.get(args[0]):
        return exist(actual_dict, args[1:]) if args[1:] else actual_dict
    else:
        return None

print(exist(data,('user','adress','line_1')))