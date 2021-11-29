import json
import unittest

from google.protobuf.json_format import MessageToDict

from data import load
from parser import parse


class TestParser(unittest.TestCase):
    def test_jan_2018(self):
        self.maxDiff = None
        # Json com a saida esperada
        # with open('output_test/expected_2019.json', 'r') as fp:
        #     expected = json.load(fp)

        files = ['output_test/2019_01_remu.xlsx']
                 
        dados = load(files, '2019', '01')
        result_data = parse(dados, 'mppe/01/2019', '01', '2019')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)
        with open('output_test/expected_2019.json', 'w') as fp:
            json.dump(result_to_dict, fp, indent=4, ensure_ascii=False)
    #     self.assertEqual(expected, result_to_dict)


    def test_jan_2020(self):
        self.maxDiff = None
        # Json com a saida esperada
        # with open('output_test/expected_2020.json', 'r') as fp:
        #     expected = json.load(fp)

        files = ['output_test/2020_01_remu.xlsx',
                'output_test/2020_01_vi.xlsx',]

        dados = load(files, '2020', '01')
        result_data = parse(dados, 'mppe/1/2020', '01', '2020')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)

        with open('output_test/expected_2020.json', 'w') as fp:
            json.dump(result_to_dict, fp, indent=4, ensure_ascii=False)
        
        # self.assertEqual(expected, result_to_dict)


if __name__ == '__main__':
    unittest.main()
