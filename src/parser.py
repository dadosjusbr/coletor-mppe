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
        name = row[1].strip() #Nome
        role = row[2].strip() #Cargo
        workplace = row[3].strip() #Lotação
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

def employees_idemnity(file_path, employees):
    data =  read(file_path)
    
    #Ajustando dataframe
    data = data.dropna()
    clean_currency(data, 4, 50)
    
    #Parsing data
    rows  = data.to_numpy()
    for row in rows:
        reg = str(row[0]) #Matrícula
        prm =  row[5] #0053-L PREM S/TRB
        
        transporte =  row[6] #0243-AUX TRANSP
        housing_aid = row[7] #0261-AUX MORADIA
        aux_refei = row[8] #0269-AUX REFEICAO
        aux_ali = row[9] #0270-AUX ALIM
        aux_saude = row[10] #0272-AUX SAUDE
        
        abon  = row[11] #0098-ABON PER ATR
        diff = row[12] #0201-DIF ENTRANC
        adc_ser_ex = row[13] #0244-ADC SERV EXT
        serv_ex_pĺt = row[14] #0251-SERV EXT PLT
        ind_ferias = row[15] #0265-IND FERIAS
        adc_at_esp = row[16] #0267-ADC AT ESPEC
        grt_sub = row[17] #0271-GRT SUB FGMP
        adc_exercicio = row[18] #0275-AD EXERCICIO
        adc_pr = row[19]  #0279-ADIC PR/TEMP
        atr_venci = row[20] #0400-VENCIM ATR
        diff_entr = row[21] #0401-DIF ENTR ATR
        quino  = row[22] #0403-QUINQ ATR
        fer_at = row[23] #0408-AB FER PR AT
        pens_ali = row[24] #0416-PENS AL ATR
        indz_ass = row[25] #0420-INDZ ASS ATR
        sal_atr = row[26] #0426-13 SAL ATR
        indz_coo = row[27] #0429-INDZ COO ATR
        ad_li = row[28] #0434-AD L16307 AT
        sub_atr = row[29] #0435-SUBSIDIO ATR
        aux_trp = row[30] #0443-AUX TRP ATR
        ad_sev_ex = row[31] #0444-AD SV EX ATR
        ad_sev_pl = row[32] #0451-SV EX PL ATR
        ad_com = row[33] #0459-COM LIC ATR
        adc_ferias = row[34] #0463-A FERIAS ATR
        ad_at = row[35] #0467-AD AT ES ATR
        aux_ref_atr = row[36] #0469-AUX REF ATR
        aux_ali_atr = row[37] #0470-AUX ALIM ATR
        gr_su = row[38] #0471-GR SU FG ATR
        aux_saude_atr = row[39] #0472-AUX SAUDE AT
        adc_exe = row[40] #0475-ADIC EXE ATR
        adc_pr = row[41] #0479-AD PR/TP ATR
        grt_fgmp = row[42] #0480-GRT FGMP ATR
        in_cgsmp = row[43] #0483-IN CGSMP ATR
        ind_ouv = row[44] #0486-IND OUV ATR
        ats_tribu = row[45] #522 ATS.TRIBUTAV
        ats_ntribut = row[46] #523 ATS.N.TRIBUT
        pae_ntrb = row[47] #558 PAE NTRB ATR
        pae_trib = row[48] #559 PAE TRIB ATR
        van_exer = row[49] #563 VAN.EXER.ATU
        van_exer_ant = row[50] #564 VAN.EXER.ANT
        
        emp = employees[reg]
        
        emp['income']['perks'].update({
            'total': round(aux_ali + aux_refei + aux_saude , transporte, housing_aid),
            'food': aux_ali + aux_refei,
            'health': aux_saude,
            'transportation': transporte,
            'housing_aid': housing_aid,
        })
        emp['income']['other']['others'].update({
            '0053-L PREM S/TRB': prm,
            '0098-ABON PER ATR': abon,
            '0201-DIF ENTRANC': diff,
            '0244-ADC SERV EXT': adc_ser_ex,
            '0251-SERV EXT PLT': serv_ex_pĺt,
            '0265-IND FERIAS': ind_ferias,
            '0267-ADC AT ESPEC': adc_at_esp,
            '0271-GRT SUB FGMP': grt_sub,
            '0275-AD EXERCICIO': adc_exercicio, 
            '0279-ADIC PR/TEMP': adc_pr,
            '0400-VENCIM ATR': atr_venci,
            '0401-DIF ENTR ATR': diff_entr,
            '0403-QUINQ ATR': quino,
            '0408-AB FER PR AT': fer_at,
            '0416-PENS AL ATR': pens_ali,
            '0420-INDZ ASS ATR' : indz_ass,
            '0426-13 SAL ATR': sal_atr,
            '0429-INDZ COO ATR': indz_coo,
            '0434-AD L16307 AT': ad_li,
            '0435-SUBSIDIO ATR': sub_atr,
            '0443-AUX TRP ATR': aux_trp,
            '0444-AD SV EX ATR': ad_sev_ex,
            '0451-SV EX PL ATR': ad_sev_pl,
            '0459-COM LIC ATR': ad_com,
            '0463-A FERIAS ATR': adc_ferias,
            '0467-AD AT ES ATR': ad_at,
            '0469-AUX REF ATR': aux_ref_atr,
            '0470-AUX ALIM ATR': aux_ali_atr, 
            '0471-GR SU FG ATR': gr_su,
            "0472-AUX SAUDE AT": aux_saude_atr,
            '0475-ADIC EXE ATR': adc_exe,
            '0479-AD PR/TP ATR': adc_pr,
            '0480-GRT FGMP ATR': grt_fgmp,
            '0483-IN CGSMP ATR': in_cgsmp,
            '0486-IND OUV ATR': ind_ouv,
            '522 ATS.TRIBUTAV': ats_tribu,
            '523 ATS.N.TRIBUT': ats_ntribut,
            '558 PAE NTRB ATR': pae_ntrb,
            '559 PAE TRIB ATR': pae_trib,
            '563 VAN.EXER.ATU': van_exer,
            '564 VAN.EXER.ANT': van_exer_ant,
        })
        emp['income']['other'].update({
            'others_total':round(
                prm + abon + diff + adc_ser_ex + serv_ex_pĺt + ind_ferias  + adc_at_esp + grt_sub + adc_exercicio + 
                adc_pr + atr_venci + diff_entr + quino + fer_at + pens_ali + indz_ass + sal_atr + indz_coo 
                + ad_li + sub_atr + aux_trp + ad_sev_ex + ad_sev_pl + ad_com + adc_ferias + ad_at 
                + aux_ref_atr + aux_ali_atr + gr_su + aux_saude_atr + adc_exe + adc_pr + grt_fgmp 
                + in_cgsmp + ind_ouv + ats_tribu + ats_ntribut + pae_ntrb + pae_trib + van_exer 
                + van_exer_ant, 2)
        })
        
def parse(file_names, month, year):
    employees = {}
    
    for file_name in file_names:
        if 'vi' not in file_name:
            employees.update(employees_parser(file_name))
        elif int(month) >= 7 and int(year) == 2019 :
            employees.update(employees_idemnity(file_name, employees))
        elif int(year) > 2019:
            employees.update(employees_idemnity(file_name, employees))
            
    return list(employees.values())