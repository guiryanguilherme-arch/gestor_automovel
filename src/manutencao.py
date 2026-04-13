# manutencao.py
# Módulo responsável pela gestão de manutenções.
# Contém o CRUD completo: criar, listar, obter, atualizar e remover manutenções.
# Todas as funções devolvem (codigo_http, dados_ou_mensagem):
#   201 → criado com sucesso
#   200 → sucesso
#   404 → não encontrado
#   500 → erro nos dados fornecidos
# A validação de datas é feita aqui diretamente, antes de guardar os dados.

from datetime import datetime
from utils import gerar_id, encontrar_por_id


# Lista com todos os tipos de manutenção disponíveis no sistema
TIPOS = [
    "Revisão",
    "Troca de óleo",
    "Troca de filtro",
    "Troca de pneus",
    "Alinhamento",
    "Balanceamento",
    "Freios",
    "Suspensão",
    "Reparo do motor",
    "Reparo da transmissão",
    "Reparo elétrico",
    "Reparo eletrónico",
    "Diagnóstico",
    "Bateria",
    "Ar condicionado",
    "Inspeção"
]

# Lista em memória que guarda todas as manutenções durante a execução
manutencoes = []


# ── VALIDAÇÃO DE DATAS (usada internamente) ───────────────────────────────────

def _validar_data(data_str):
    """
    Valida uma string de data no formato DD-MM-YYYY.
    Devolve True se válida, False se inválida.
    Função interna — usada por criar_manutencao e atualizar_manutencao.
    """
    if not data_str:
        return False
    try:
        datetime.strptime(data_str, "%d-%m-%Y")
        return True
    except ValueError:
        return False


# ── CREATE ────────────────────────────────────────────────────────────────────

def criar_manutencao(id_carro, tipo, data_criacao, custo_orcamento, descricao,
                     data_manutencao=None, custo_final=None, folha_obra_id=None):
    """
    Cria uma nova manutenção e adiciona-a à lista.
    Valida as datas antes de guardar.
    Devolve (201, manutencao) em caso de sucesso.
    Devolve (500, mensagem) se os dados forem inválidos.
    """
    # Validar data de criação antes de guardar
    if not _validar_data(data_criacao):
        return 500, "Data de criação inválida. Usa o formato DD-MM-YYYY."

    # Validar data de manutenção se fornecida
    if data_manutencao and not _validar_data(data_manutencao):
        return 500, "Data de manutenção inválida. Usa o formato DD-MM-YYYY."

    manut = {
        "id":              gerar_id(manutencoes),  # ID único gerado automaticamente
        "id_carro":        id_carro,               # Referência ao carro associado (FK)
        "tipo":            tipo,                   # Tipo de manutenção (ver lista TIPOS)
        "data_criacao":    data_criacao,            # Data de registo (string DD-MM-YYYY)
        "data_manutencao": data_manutencao,         # Data de execução (opcional, DD-MM-YYYY)
        "custo_orcamento": custo_orcamento,         # Custo estimado (>= 0)
        "custo_final":     custo_final,             # Custo real após execução (opcional)
        "descricao":       descricao,               # Descrição do trabalho realizado
        "folha_obra_id":   folha_obra_id,           # Referência a documento externo (opcional)
        "estado":          "pendente"               # Estado inicial: pendente ou concluída
    }
    manutencoes.append(manut)
    return 201, manut


# ── READ ──────────────────────────────────────────────────────────────────────

def listar_manutencoes():
    """
    Devolve a lista completa de manutenções registadas.
    Devolve (200, lista) em caso de sucesso.
    Devolve (404, mensagem) se não existirem manutenções.
    """
    if not manutencoes:
        return 404, "Não existem manutenções registadas."
    return 200, manutencoes


def obter_manutencao(id_manut):
    """
    Procura uma manutenção pelo seu ID.
    Devolve (200, manutencao) se encontrada.
    Devolve (404, mensagem) se não encontrada.
    """
    resultado = encontrar_por_id(manutencoes, id_manut)
    if not resultado:
        return 404, f"Manutenção com ID {id_manut} não encontrada."
    return 200, resultado


def listar_por_carro(id_carro):
    """
    Devolve todas as manutenções associadas a um carro específico.
    Devolve (200, lista) em caso de sucesso.
    Devolve (404, mensagem) se não existirem manutenções para esse carro.
    """
    resultado = [m for m in manutencoes if m["id_carro"] == id_carro]
    if not resultado:
        return 404, f"Nenhuma manutenção encontrada para o carro com ID {id_carro}."
    return 200, resultado


def total_manutencoes():
    """Devolve (200, total) com o número total de manutenções registadas."""
    return 200, len(manutencoes)


def total_gasto():
    """
    Calcula o total gasto em todas as manutenções.
    Usa custo_final se disponível, senão usa custo_orcamento.
    Devolve (200, total).
    """
    total = sum(
        m["custo_final"] if m["custo_final"] is not None else m["custo_orcamento"]
        for m in manutencoes
    )
    return 200, total


def media_gastos():
    """
    Calcula a média de gastos por manutenção.
    Devolve (200, media) ou (404, mensagem) se não existirem manutenções.
    """
    if not manutencoes:
        return 404, "Não existem manutenções para calcular média."
    _, total = total_gasto()
    return 200, total / len(manutencoes)


def manutencao_mais_cara():
    """
    Devolve a manutenção com o custo mais elevado.
    Usa custo_final se disponível, senão usa custo_orcamento.
    Devolve (200, manutencao) ou (404, mensagem) se lista vazia.
    """
    if not manutencoes:
        return 404, "Não existem manutenções registadas."
    resultado = max(manutencoes, key=lambda m: m["custo_orcamento"] if m["custo_final"] is None else m["custo_final"])
    return 200, resultado


# ── UPDATE ────────────────────────────────────────────────────────────────────

def atualizar_manutencao(id_manut, dados):
    """
    Atualiza os campos permitidos de uma manutenção existente.
    Valida a data de manutenção se for fornecida.
    Campos que NÃO podem ser alterados: id, id_carro, data_criacao.
    Campos permitidos: tipo, data_manutencao, custo_final, descricao, estado.
    Devolve (200, manutencao) em caso de sucesso.
    Devolve (404, mensagem) se não encontrada.
    Devolve (500, mensagem) se a data for inválida.
    """
    codigo, resultado = obter_manutencao(id_manut)
    if codigo != 200:
        return 404, resultado

    # Validar data de manutenção antes de atualizar
    if "data_manutencao" in dados and dados["data_manutencao"]:
        if not _validar_data(dados["data_manutencao"]):
            return 500, "Data de manutenção inválida. Usa o formato DD-MM-YYYY."

    campos_permitidos = {"tipo", "data_manutencao", "custo_final", "descricao", "estado"}
    for campo, valor in dados.items():
        if campo in campos_permitidos:
            resultado[campo] = valor
    return 200, resultado


def atualizar_estado(id_manut, estado):
    """
    Atualiza apenas o estado de uma manutenção (ex: 'pendente' → 'concluída').
    Devolve (200, mensagem) se atualizado.
    Devolve (404, mensagem) se não encontrado.
    """
    codigo, resultado = obter_manutencao(id_manut)
    if codigo != 200:
        return 404, resultado
    resultado["estado"] = estado
    return 200, "Estado atualizado com sucesso."


# ── DELETE ────────────────────────────────────────────────────────────────────

def remover_manutencao(id_manut):
    """
    Remove uma manutenção da lista pelo seu ID.
    Devolve (200, mensagem) em caso de sucesso.
    Devolve (404, mensagem) se não encontrada.
    """
    codigo, resultado = obter_manutencao(id_manut)
    if codigo != 200:
        return 404, resultado
    manutencoes.remove(resultado)
    return 200, f"Manutenção ID {id_manut} removida com sucesso."