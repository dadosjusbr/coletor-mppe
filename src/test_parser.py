import json
import unittest

from google.protobuf.json_format import MessageToDict

from data import load
from parser import parse


class TestParser(unittest.TestCase):
    def test_jan_2019(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected_01_2019.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/membros-ativos-contracheque-01-2019.xlsx']
                 
        dados = load(files, '2019', '01', 'src/output_test')
        result_data = parse(dados, 'mppe/01/2019', '01', '2019')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)
        
        self.assertEqual(expected, result_to_dict)


    def test_ago_2019(self):
            self.maxDiff = None
            # Json com a saida esperada
            with open('src/output_test/expected_08_2019.json', 'r') as fp:
                expected = json.load(fp)

            files = ['src/output_test/membros-ativos-contracheque-08-2019.xlsx',
                    'src/output_test/membros-ativos-verbas-indenizatorias-08-2019.xlsx',]

            dados = load(files, '2019', '08', 'src/output_test')
            result_data = parse(dados, 'mppe/8/2019', '08', '2019')
            # Converto o resultado do parser, em dict
            result_to_dict = MessageToDict(result_data)

            self.assertEqual(expected, result_to_dict)

    def test_jan_2020(self):
        self.maxDiff = None
        # Json com a saida esperada
        with open('src/output_test/expected_01_2020.json', 'r') as fp:
            expected = json.load(fp)

        files = ['src/output_test/membros-ativos-contracheque-01-2020.xlsx',
                'src/output_test/membros-ativos-verbas-indenizatorias-01-2020.xlsx',]

        dados = load(files, '2020', '01', 'src/output_test')
        result_data = parse(dados, 'mppe/1/2020', '01', '2020')
        # Converto o resultado do parser, em dict
        result_to_dict = MessageToDict(result_data)
        
        self.assertEqual(expected, result_to_dict)


if __name__ == '__main__':
    unittest.main()
