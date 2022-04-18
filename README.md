![Docker](https://github.com/dadosjusbr/coletor-mppe/actions/workflows/docker-publish.yml/badge.svg)

# Ministério Público do Estado de Pernambuco

Este coletor tem como objetivo a recuperação de informações sobre folhas de pagamentos dos funcionários do Ministério Público do Estado de Pernambuco. O site com as informações pode ser acessado [aqui](https://transparencia.mppe.mp.br/index.php/contracheque/category/225-proventos-de-todos-os-membros-inativos).

O coletor será estruturado como uma CLI. Uma vez passado como argumentos mês e ano, será feito o download de duas planilhas no formato XLSX. Cada planilha é referente a uma dessas categorias:

- Tipo I - Folha de remuneração: Membros Ativos

- Tipo II - Verbas Indenizatórias e outras remunerações temporárias referentes há membros ativos.

# Coletando usando Docker

Por exemplo, para coletar o mês de novembro de 2020, basta executar os seguintes comandos:

```sh
$ sudo docker build -t mppe .
sudo docker run -e MONTH=01 -e YEAR=2020 -e GIT_COMMIT=$(git rev-parse HEAD) -e OUTPUT_FOLDER='/output' mppe
```

# Coleta sem utilização do Docker:

**Obs:** Antes de mais nada, deve-se instalar as dependências do programa, executando o comando:

```sh
pip install -r requirements.txt
```

> ## 1. Através da CLI

Por exemplo, para coletar o mês de fevereiro de 2022, os seguintes comandos podem ser executados

- ```sh
  python src/main.py --YEAR=2022 --MONTH=02 --GIT_COMMIT=$(git rev-parse HEAD) --OUTPUT_FOLDER=/output
  ```
- ```sh
  python src/main.py --YEAR 2022 --MONTH 02 --GIT_COMMIT $(git rev-parse HEAD) --OUTPUT_FOLDER /output
  ```
- ```sh
  python src/main.py -y 2022 -m 02 -gc $(git rev-parse HEAD) -of /output
  ```
  Obs: O comando abaixo não funciona no sistema operacional Windows
- ```sh
  YEAR=2022 MONTH=02 GIT_COMMIT=$(git rev-list -1 HEAD) python3 src/main.py
  ```

> ## 2. Criando arquivo **.env**

Por exemplo, para coletar o mês de fevereiro de 2022:

- Criar um arquivo **.env** na raíz do projeto, com as variáveis de ambiente descritas no arquivo **.env.example**, dessa forma:

  ```
  YEAR=2022
  MONTH=02
  GIT_COMMIT=$(git rev-list -1 HEAD)
  OUTPUT_FOLDER=/output
  ```

  Com o arquivo **.env** criado, executar o comando:

  ```sh
  python src/main.py
  ```

# Dicionário de dados

As planilhas referentes á remunerações possuem as seguintes colunas:

- **Nome (String)**: Nome completo do funcionário
- **Cargo (String)**: Cargo do funcionário dentro do MP
- **Lotação (String)**: Local (cidade, departamento, promotoria) em que o funcionário trabalha
- **Remuneração do cargo efetivo (Number)**: Vencimento, GAMPU, V.P.I, Adicionais de Qualificação, G.A.E e G.A.S, além de outras desta natureza. Soma de todas essas remunerações
- **Outras Verbas Remuneratórias Legais/Judiciais (Number)**: V.P.N.I., Adicional por tempo de serviço, quintos, décimos e vantagens decorrentes de sentença judicial ou extensão administrativa
- **Função de Confiança ou Cargo em Comissão (Number)**: Rubricas que representam a retribuição paga pelo exercício de função (servidor efetivo) ou remuneração de cargo em comissão (servidor sem vínculo ou requisitado)
- **Gratificação Natalina (Number)**: Parcelas da Gratificação Natalina (13º) pagas no mês corrente, ou no caso de vacância ou exoneração do servidor
- **Adicional de Férias (Number)**: Adicional correspondente a remuneração paga ao servidor por ocasião das férias
- **Abono de Permanência (Number)**: Valor equivalente ao da contribuição previdenciária, devido ao funcionário público que esteja em condição de aposentar-se, mas que optou por continuar em atividade (instituído pela Emenda Constitucional nº 41, de 16 de dezembro de 2003)
- **Outras Remunerações Temporárias (Number)**: Valores pagos a título de Auxílio-alimentação, Auxílio-cursos,Auxílio-Saúde, Auxílio-creche, Auxílio-moradia.
- **Verbas Indenizatórias (Number)**: Verbas referentes á indenizações recebidas pelo funcionario á titulo de Adicional noturno, Cumulações, Serviços extraordinários e substituição de função.

# Dificuldades na libertação de dados:

## Dificuldades de coleta:

- Todos os anos possuem um código que varia para Verbas Indenizatórias, forçando mapeamento. Exemplo: 2018 está associado ao código 405, 2019 ao código 445, 2020 ao código 504. Não existindo progressão lógica a necessidade de mapeamento adiciona complexidade de código.
- Todos os anos possuem um código que varia para remunerações simples, forçando mapeamento. Exemplo: 2018 está associado ao código 415, 2019 ao código 451, 2020 ao código 510. Não existindo progressão lógica a necessidade de mapeamento adiciona complexidade de código.
- Cada planilha possui um código de identificação que varia e que deve ser enviado na requisição, forçando busca.
- Download Verbas Indenizatórias referentes á 2018 e 2019 recebem o nome do mês (Janeiro, Feveiro ... ) como parâmetro da url, anos posteriores recebem o numeral referente ao mês (01 para Janeiro, 02 para Fevereiro ....).
- Nome das planilhas de verbas indenizatórias alterados nas urls posteriores após 2019. Exemplo: para 2018 e 2019 temos: ('virt'), para 2020 em diante temos: ('indeniz').
- Exemplos de urls, ilustrando os problemas:
  - https://transparencia.mppe.mp.br/index.php/contracheque/category/405-remuneracao-de-todos-os-membros-ativos-2018?download=4784:membros-ativos-12-2018
  - https://transparencia.mppe.mp.br/index.php/contracheque/category/504-remuneracao-de-todos-os-membros-ativos-2020?download=6429:membros-ativos-12-2020
  - https://transparencia.mppe.mp.br/index.php/contracheque/category/451-verbas-indenizatorias-e-outras-remuneracoes-temporarias-2019?download=5651:virt-dezembro-2019
  - https://transparencia.mppe.mp.br/index.php/contracheque/category/555-verbas-indenizatorias-e-outras-remuneracoes-temporarias-2021?download=6729:indeniz032021

## Dificuldades de Parsing:

- Planilhas referentes á verbas indenizatórias possuem aproximadamente 50 colunas.
- Nomeclatura das colunas referentes á verbas indenizatórias é pouco descritiva, Exemplo: 0201-DIF ENTRANC, 0416-PENS AL ATR.
- Permutação da localização das colunas Indenizações e Outras Remunerações Retroativas/Temporárias, entre 2020 e 2019/2018 sendo necessário abordagem especializada.
- Inexistência de dados referente á verbas indenizatórias anteriores á setembro de 2019.
