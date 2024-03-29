from coleta import coleta_pb2 as Coleta


def captura(month, year):
    metadado = Coleta.Metadados()
    # As urls seguem um formato bem consistente até certo ponto, 
    # ex: https://transparencia.mppe.mp.br/index.php/contracheque/category/504-remuneracao-de-todos-os-membros-ativos-2020?download=5849:membros-ativos-03-2020
    # porém no parâmentro de download na URL, vem um pequeno código, 
    # que não podemos decifrar facilmente, e que muda para cada mês.
    metadado.acesso = Coleta.Metadados.FormaDeAcesso.RASPAGEM_DIFICULTADA
    metadado.extensao = Coleta.Metadados.Extensao.XLS
    metadado.estritamente_tabular = True
    metadado.formato_consistente = True
    metadado.tem_matricula = True
    metadado.tem_lotacao = True
    metadado.tem_cargo = True
    metadado.despesas = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    metadado.receita_base = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    metadado.outras_receitas = Coleta.Metadados.OpcoesDetalhamento.DETALHADO
    # Meses onde aconteceu uma mudança nos formatos das planilhas:
    if (int(year) == 2019 and int(month) in [7, 12]) or (int(year) == 2022 and int(month) == 2):
        metadado.formato_consistente = False
    # Não tem planilhas detalhando, apenas o total:
    if int(year) == 2018 or (int(year) == 2019 and int(month) < 7) or (int(year) == 2022 and int(month) == 2):
        metadado.despesas = Coleta.Metadados.OpcoesDetalhamento.SUMARIZADO

    return metadado
