Gestor Automovel
🚗 Gestor de Manutenção Automóvel
📌 Descrição
Este projeto consiste num sistema de gestão de uma oficina automóvel desenvolvido em Python.
Permite gerir:

Carros registados na oficina
Manutenções associadas a cada carro
O programa funciona em modo consola (terminal) e utiliza listas de dicionários para armazenar os dados em memória durante a execução.

🎯 Funcionalidades
🚘 Gestão de Carros
Adicionar carro ao sistema
Listar todos os carros
Ver histórico de manutenções ao consultar um carro
Atualizar dados de um carro
Remover carro (com eliminação em cascata das manutenções associadas)
Procurar carro por ID ou matrícula
Ver total de carros registados
🔧 Gestão de Manutenções
Registar manutenção associada a um carro
Atualizar manutenção
Remover manutenção
Marcar manutenção como concluída
📊 Relatórios
Total de carros
Total de manutenções
Total gasto em manutenções
Média de gastos por manutenção
Manutenção mais cara
🗂️ Estrutura do Projeto
📁 projeto/
│
├── main.py          # Menu principal e interação com o utilizador
├── carros.py        # Gestão de carros (CRUD)
├── manutencao.py    # Gestão de manutenções (CRUD)
├── utils.py         # Funções auxiliares genéricas
└── README.md        # Documentação do projeto
⚙️ Tecnologias Utilizadas
Python 3
Programação estruturada (sem classes)
Listas e dicionários para armazenamento em memória
Padrão de retorno HTTP (códigos de estado)
🧠 Estrutura de Dados
O sistema utiliza:

Listas (list) → armazenam conjuntos de dados (carros e manutenções)
Dicionários (dict) → representam cada entidade
Exemplo de carro:
{
  "id": 1,
  "marca": "BMW",
  "modelo": "320d",
  "matricula": "AA-00-BB",
  "ano": "2020",
  "mes": "5",
  "combustivel": "Gasóleo",
  "potencia_cv": "190",
  "cilindrada_cc": "2000"
}
Exemplo de manutenção:
{
  "id": 1,
  "id_carro": 1,
  "tipo": "Revisão",
  "data_criacao": "10-01-2024",
  "data_manutencao": "15-01-2024",
  "custo_orcamento": "100",
  "custo_final": "120",
  "descricao": "Troca de óleo e filtros",
  "folha_obra_id": None,
  "estado": "concluída"
}
🔁 Padrão de Retorno HTTP
Todas as funções de carros.py e manutencao.py devolvem um tuplo (codigo, resultado) seguindo o padrão HTTP:

Código	Significado
200	Sucesso
201	Criado com sucesso
404	Não encontrado
409	Conflito (ex: matrícula duplicada)
500	Erro nos dados fornecidos
Exemplo de uso:
codigo, resultado = adicionar_carro(dados)
if codigo == 201:
    print("✅ Carro adicionado com sucesso.")
else:
    print(f"❌ Erro {codigo}: {resultado}")
▶️ Como Executar
Certifica-te que tens Python 3 instalado
Abre o terminal na pasta do projeto
Executa:
python main.py
🧪 Validações
O sistema inclui as seguintes validações:

Matrículas duplicadas — não permite registar dois carros com a mesma matrícula
Existência do carro — verifica se o carro existe antes de registar uma manutenção
Datas — valida o formato DD-MM-YYYY antes de guardar
IDs válidos — verifica se o ID existe antes de atualizar ou remover
Campos obrigatórios — verifica campos em falta ao adicionar um carro
Eliminação em cascata — ao remover um carro, todas as suas manutenções são removidas automaticamente