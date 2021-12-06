import unittest

from data import load


file_names = [
    "src/output_test/membros-ativos-contracheque-01-2020.xlsx",
    "src/output_test/membros-ativos-verbas-indenizatorias-01-2020.xlsx",
]


class TestData(unittest.TestCase):
    # Validação para ver se a planilha não foi apagada no processo...
    def test_validate_existence(self):
        STATUS_DATA_UNAVAILABLE = 4
        with self.assertRaises(SystemExit) as cm:
            dados = load(file_names, "2021", "02", "src/output_test") # Mês alterado para simular erro
            dados.validate()
        self.assertEqual(cm.exception.code, STATUS_DATA_UNAVAILABLE)


if __name__ == "__main__":
    unittest.main()