import sys
import pandas as pd
import os

def clean_currency(data, beg_col, end_col):
    for col in data.columns[beg_col:end_col]:
        data[col] = data[col].apply(clean_currency_val)

def clean_currency_val(value):
    return float(value)

def read(path):
    try:
        data = pd.read_excel(path, engine='xlrd')
        return data
    except Exception as excep:
        sys.stderr.write("'Não foi possível ler o arquivo: " + path + '. O seguinte erro foi gerado: ' + excep)
        os._exit(1)

def employees_parser(file_path):
    data = read(file_path)
    
    #Ajustando dataframe
    data = data.dropna()
    clean_currency(data,4,17)
    
    #Parsing data
    rows = data.to_numpy()
    employees = {}
    
    for row in rows:
        reg = str(row[0]) #Matrícula 
        name = row[1] #Nome
        role = row[2] #Cargo
        workplace = row[3] #Lotação
        remuneration = row[4] #Remuneração do cargo efetivo
        other_verbs =  row[5] #Outras Verbas Remuneratórias, Legais ou Judiciais   
        trust_pos = row[6] #Função de Confiança ou Cargo em Comissão 
        christmas_grati = row[7] #Gratificação Natalina
        terco_ferias = row[8] #Férias (1/3 constitucional)
        abono_permanencia = row[9] #Abono de Permanência 
        total = row[10] #Total de rendimentos brutos
        prev_contrib = row[11] #Contribuição Previdenciária
        imposto_renda = row[12] #Imposto de Renda
        ceil_ret = row[13] #Retenção do Teto       
        idemnity = row[16] #Indenizações
        temp_remu = row[17] #Outras Remunerações Retroativas/Temporárias
        
        employees[reg] = {
            'reg': reg,
            'name': name,
            'role': role,
            'type': 'membro',
            'workplace': workplace,
            'active': True,
            "income":
        {
            'total': total,
            'wage': remuneration + other_verbs,
            'perks':{
                'total': idemnity,
            },
            'other':
            { 
                'total': trust_pos + christmas_grati + terco_ferias + abono_permanencia + temp_remu,
                'trust_position': trust_pos,
                'eventual_benefits': temp_remu,
                'others_total': christmas_grati + terco_ferias + abono_permanencia,
                'others': {
                    'Gratificação Natalina': christmas_grati,
                    'Férias (1/3 constitucional)': terco_ferias,
                    'Abono de permanência': abono_permanencia,
                }
            },

        },
        'discounts':
        {
            'total': round(prev_contrib + ceil_ret + imposto_renda, 2),
            'prev_contribution': prev_contrib,
            'ceil_retention': ceil_ret,
            'income_tax': imposto_renda
        }
    }
    
    return employees

def parse(file_names):
    employees = {}
    
    for file_name in file_names:
        if 'vi' not in file_name:
            employees.update(employees_parser(file_name))
    
    return list(employees.values())