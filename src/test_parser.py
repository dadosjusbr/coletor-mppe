import json
import unittest

from google.protobuf.json_format import MessageToDict

from data import load
from parser import parse


class TestParser(unittest.TestCase):
    def test_jan_2018(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('output_test/expected_2019.json', 'r') as fp:
            expected = json.load(fp)

        files = ['output_test/membros-ativos-contracheque-01-2019.xlsx']
                 
        dados = load(files, '2019', '01')
        result_data = parse(dados, 'mppe/01/2019', '01', '2019', './output_test')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)
        
        self.assertEqual(expected, result_to_dict)


    def test_jan_2020(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('output_test/expected_2020.json', 'r') as fp:
            expected = json.load(fp)

        files = ['output_test/membros-ativos-contracheque-01-2020.xlsx',
                'output_test/membros-ativos-verbas-indenizatorias-01-2020.xlsx',]

        dados = load(files, '2020', '01')
        result_data = parse(dados, 'mppe/1/2020', '01', '2020', './output_test')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)
        
        self.assertEqual(expected, result_to_dict)


if __name__ == '__main__':
    unittest.main()
