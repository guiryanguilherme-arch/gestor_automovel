# 🚗 Gestor de Manutenção Automóvel

## 📌 Descrição

Projeto desenvolvido em Python para gerir uma oficina automóvel em modo consola.
Permite gerir clientes, oficinas, carros e manutenções.
Os dados são armazenados em memória com listas de dicionários durante a execução.

## 🎯 Funcionalidades

👤 **Clientes** — adicionar, listar, atualizar e remover (bloqueado se tiver carros associados)

🏢 **Oficinas** — adicionar, listar, atualizar e remover (bloqueada se tiver manutenções associadas)

🚘 **Carros** — adicionar (associado a cliente), listar, atualizar, remover com cascata e ver histórico de manutenções

🔧 **Manutenções** — registar (associada a carro e oficina), atualizar, remover e marcar como concluída

📊 **Relatórios** — total de carros, manutenções, total gasto, média e manutenção mais cara

## 🗂️ Estrutura do Projeto
projeto/
├── main.py        # Menu principal e interação com o utilizador
├── cliente.py     # Gestão de clientes (CRUD)
├── oficina.py     # Gestão de oficinas (CRUD)
├── carros.py      # Gestão de carros (CRUD)
├── manutencao.py  # Gestão de manutenções (CRUD)
├── utils.py       # Funções auxiliares genéricas
└── README.md      # Documentação do projeto

## ⚙️ Tecnologias

- Python 3
- Programação estruturada (sem classes)
- Listas e dicionários para armazenamento em memória
- Padrão de retorno inspirado em códigos HTTP

## 🧠 Estrutura de Dados

```python
# Cliente
{"id": 1, "nome": "João Silva", "telefone": "912345678", "email": "joao@email.com", "nif": "123456789"}

# Oficina
{"id": 1, "nome": "Oficina Central", "morada": "Rua das Flores, 10", "telefone": "210000000", "email": "oficina@email.com"}

# Carro
{"id": 1, "id_cliente": 1, "marca": "BMW", "modelo": "320d", "matricula": "AA-00-BB", "ano": "2020", "mes": "5", "combustivel": "Gasóleo", "potencia_cv": "190", "cilindrada_cc": "2000"}

# Manutenção
{"id": 1, "id_carro": 1, "id_oficina": 1, "tipo": "Revisão", "data_criacao": "10-01-2024", "custo_orcamento": 100.0, "custo_final": 120.0, "descricao": "Troca de óleo", "estado": "concluída"}
```

## 🔁 Padrão de Retorno HTTP

| Código | Significado |
|--------|-------------|
| 200 | Sucesso |
| 201 | Criado com sucesso |
| 404 | Não encontrado |
| 409 | Conflito (ex: matrícula duplicada) |
| 500 | Erro nos dados fornecidos |

## ▶️ Como Executar

```bash
python main.py
```

## 🧪 Validações

- Emails e NIF duplicados não são permitidos
- Matrículas duplicadas não são permitidas
- Não apaga cliente com carros nem oficina com manutenções associadas
- Remover carro elimina automaticamente as suas manutenções
- Datas validadas no formato DD-MM-YYYY
- Campos obrigatórios verificados em todos os módulos
