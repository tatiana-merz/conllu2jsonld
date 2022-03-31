from conllu import parse_incr, parse
from io import open
import json
import os

def get_data():
    dirrectory = 'results_jsonld'
    data_file = open('UD_English-ParTUT.conllu', 'r', encoding='utf-8')
    for tokenlist in parse_incr(data_file):
        dict_token = tokenlist.metadata
        dict_struct = parse(tokenlist.serialize())[0][:-1]

        result_dict = {}

        for value_struct in dict_struct:
            for key in value_struct.keys():
                id_ = value_struct['id']

                if isinstance(value_struct[key], dict):
                    result_value = ''
                    for key2, value in value_struct[key].items():
                        result_value += f'{key2}={value}|'
                    result_dict[f'{key}{id_}'] = result_value
                elif isinstance(value_struct[key], list):
                    result_value = ''
                    for value in value_struct[key][0]:
                        result_value += f'{value}|'
                    result_dict[f'{key}{id_}'] = result_value
                else:
                    result_dict[f'{key}{id_}'] = value_struct[key]


        type_ = [
            'TEXT',
        ]

        context = [
            'https://schema.org',
            {
                'Components': {
                '@type': 'class',
                '@id': 'https://URL.ru',
            }
            }
        ]
        Json = {
            '@context': context,
            '@type': type_,
            'name': dict_token['text'],
            }

        Json = {**Json, **result_dict}

        #file_name, number = dict_token['sent_id'].split('.')
        file_name = dict_token['sent_id']#.split('.')
        #number = number.split('_')[1]

        if not os.path.isdir(dirrectory):
            os.mkdir(dirrectory)

        path_file = os.path.join(dirrectory, f'{file_name}.jsonld')

        with open(path_file, 'w') as file:
            json.dump(Json, file, indent=4, ensure_ascii=False)


def main():
    get_data()


if __name__ == '__main__':
    main()