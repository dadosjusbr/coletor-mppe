import os
import parser
import unittest

class TestParser(unittest.TestCase):
    
    def test_membros_jan_2019(self):
        self.maxDiff = None
        
        expected = {    
            'reg': '1771124',
            'name': 'ADALBERTO MENDES PINTO VIEIRA',
            'role': 'PROCURADOR DE JUSTICA                             ',
            'type': 'membro',
            'workplace': 'GABINETE 4 PROCURADOR JUSTICA CRIMINAL            ',
            'active': True,
            'income': {
                'total': 41687.06,
                'wage': 35462.22,
                'perks': {
                    'total': 1068.00,
                },
                'other': {
                    'total': 6224.84,
                    'trust_position': 0.00,
                    'others_total': 6224.84,
                    'eventual_benefits': 0.00,
                    'others': {
                        'Gratificação Natalina': 0.00,
                        'Férias (1/3 constitucional)': 0.00,
                        'Abono de permanência': 6224.84,
                    },
            },
        },
            'discounts': {
                'total': 18035.71,
                'prev_contribution': 6224.84,
                'ceil_retention': 0.00,
                'income_tax': 11810.87,
            }
        }
    
        files = ('./output_test/2019_01_remu.xls',
                './output_test/2019_01_vi.xls')
        employees = parser.parse(files)
        
        #Verificações    
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)
        
if __name__ == '__main__':
    unittest.main()
