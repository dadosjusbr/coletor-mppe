import os
import parser
import unittest

class TestParser(unittest.TestCase):
    
    def test_membros_jan_2019(self):
        self.maxDiff = None
        
        expected = {    
            'reg': '1771124',
            'name': 'ADALBERTO MENDES PINTO VIEIRA',
            'role': 'PROCURADOR DE JUSTICA',
            'type': 'membro',
            'workplace': 'GABINETE 4 PROCURADOR JUSTICA CRIMINAL',
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
        employees = parser.parse(files, '01', '2019')
        
        #Verificações    
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)
        
    def test_membros_jan_2020(self):
        self.maxDiff = None
        
        expected = {    
            'reg': '1892770',
            'name': 'ADEMILTON DAS VIRGENS CARVALHO LEITÃO',
            'role': 'PROMOTOR 2. ENTRANCIA',
            'type': 'membro',
            'workplace': 'GAB 1 PROM JUSTICA CRIMINAL PAULISTA',
            'active': True,
            'income': {
                'total': 33572.65,
                'wage': 32004.65,
                'perks': {
                    'total': 1568.00,
                    'food': 1068.00,
                    'health': 500.00,
                    'transportation': 0.00,
                    'housing_aid': 0.00,
                },
                'other': {
                    'total': 0.00,
                    'trust_position': 0.00,
                    'others_total': 0.00,
                    'eventual_benefits': 0.00,
                    'others': {
                        'Gratificação Natalina': 0.00,
                        'Férias (1/3 constitucional)': 0.00,
                        'Abono de permanência': 0.00,
                        '0053-L PREM S/TRB': 0.00,
                        '0098-ABON PER ATR': 0.00,
                        '0201-DIF ENTRANC': 0.00,
                        '0244-ADC SERV EXT': 0.00,
                        '0251-SERV EXT PLT': 0.00,
                        '0265-IND FERIAS': 0.00,
                        '0267-ADC AT ESPEC': 0.00,
                        '0271-GRT SUB FGMP': 0.00,
                        '0275-AD EXERCICIO': 0.00, 
                        '0279-ADIC PR/TEMP': 0.00,
                        '0400-VENCIM ATR': 0.00,
                        '0401-DIF ENTR ATR': 0.00,
                        '0403-QUINQ ATR': 0.00,
                        '0408-AB FER PR AT': 0.00,
                        '0416-PENS AL ATR': 0.00,
                        '0420-INDZ ASS ATR' : 0.00,
                        '0426-13 SAL ATR': 0.00,
                        '0429-INDZ COO ATR': 0.00,
                        '0434-AD L16307 AT': 0.00,
                        '0435-SUBSIDIO ATR': 0.00,
                        '0443-AUX TRP ATR': 0.00,
                        '0444-AD SV EX ATR': 0.00,
                        '0451-SV EX PL ATR': 0.00,
                        '0459-COM LIC ATR': 0.00,
                        '0463-A FERIAS ATR': 0.00,
                        '0467-AD AT ES ATR': 0.00,
                        '0469-AUX REF ATR': 0.00,
                        '0470-AUX ALIM ATR': 0.00, 
                        '0471-GR SU FG ATR': 0.00,
                        "0472-AUX SAUDE AT": 0.00,
                        '0475-ADIC EXE ATR': 0.00,
                        '0479-AD PR/TP ATR': 0.00,
                        '0480-GRT FGMP ATR': 0.00,
                        '0483-IN CGSMP ATR': 0.00,
                        '0486-IND OUV ATR': 0.00,
                        '522 ATS.TRIBUTAV': 0.00,
                        '523 ATS.N.TRIBUT': 0.00,
                        '558 PAE NTRB ATR': 0.00,
                        '559 PAE TRIB ATR': 0.00,
                        '563 VAN.EXER.ATU': 0.00,
                        '564 VAN.EXER.ANT': 0.00,
                    },
            },
        },
            'discounts': {
                'total': 10907.96,
                'prev_contribution': 4320.63,
                'ceil_retention': 0.00,
                'income_tax': 6587.33,
            }
        }
        
        files = ('./output_test/2020_01_remu.xls',
                './output_test/2020_01_vi.xls')
        employees = parser.parse(files, '01', '2020')
        
        #Verificações    
        self.assertEqual(1, len(employees))
        self.assertDictEqual(employees[0], expected)

        
        
        
                
if __name__ == '__main__':
    unittest.main()
