# carros.py
# Módulo responsável pela gestão de carros.
# Contém o CRUD completo: adicionar, listar, obter, atualizar e remover carros.
# Todas as funções devolvem (codigo_http, dados_ou_mensagem):
#   201 → criado com sucesso
#   200 → sucesso
#   404 → não encontrado
#   409 → conflito (ex: matrícula duplicada)
#   500 → erro nos dados fornecidos

from utils import gerar_id, encontrar_por_id

#teste


# Lista com os tipos de combustível aceites pelo sistema
COMBUSTIVEIS = ["Gasolina", "Gasóleo", "Elétrico", "Híbrido", "GPL"]

# Lista em memória que guarda todos os carros durante a execução
carros = []


# ── CREATE ────────────────────────────────────────────────────────────────────

def adicionar_carro(marca, modelo, matricula, ano, mes, combustivel, potencia_cv, cilindrada_cc):
    """
    Cria um novo carro e adiciona-o à lista.
    Verifica se a matrícula já existe antes de adicionar.
    Devolve (201, carro) em caso de sucesso.
    Devolve (409, mensagem) se a matrícula já estiver registada.
    Devolve (500, mensagem) se os dados forem inválidos.
    """
    # Verificar campos obrigatórios
    if not marca or not modelo or not matricula or not ano or not mes or not combustivel or not potencia_cv or not cilindrada_cc:
        return 500, "Todos os campos são obrigatórios."

    # Impede matrículas duplicadas
    codigo, _ = procurar_por_matricula(matricula)
    if codigo == 200:
        return 409, f"Conflito - Matrícula '{matricula.upper()}' já está registada."

    carro = {
        "id":            gerar_id(carros),    # ID único gerado automaticamente
        "marca":         marca,
        "modelo":        modelo,
        "matricula":     matricula.upper(),   # Guardada sempre em maiúsculas
        "ano":           ano,
        "mes":           mes,
        "combustivel":   combustivel,
        "potencia_cv":   potencia_cv,
        "cilindrada_cc": cilindrada_cc
    }
    carros.append(carro)
    return 201, carro


# ── READ ──────────────────────────────────────────────────────────────────────

def listar_carros():
    """
    Devolve a lista completa de carros registados.
    Devolve (200, lista) em caso de sucesso.
    Devolve (404, mensagem) se não existirem carros.
    """
    if not carros:
        return 404, "Não existem carros registados."
    return 200, carros


def obter_carro(id_carro):
    """
    Procura um carro pelo seu ID.
    Devolve (200, carro) se encontrado.
    Devolve (404, mensagem) se não encontrado.
    """
    carro = encontrar_por_id(carros, id_carro)
    if not carro:
        return 404, f"Carro com ID {id_carro} não encontrado."
    return 200, carro


def procurar_por_matricula(matricula):
    """
    Procura um carro pela matrícula (insensível a maiúsculas/minúsculas).
    Devolve (200, carro) se encontrado.
    Devolve (404, mensagem) se não encontrado.
    """
    resultado = next((c for c in carros if c["matricula"] == matricula.upper()), None)
    if not resultado:
        return 404, f"Nenhum carro encontrado com matrícula '{matricula.upper()}'."
    return 200, resultado


def total_carros():
    """Devolve (200, total) com o número total de carros registados."""
    return 200, len(carros)


# ── UPDATE ────────────────────────────────────────────────────────────────────

def atualizar_carro(id_carro, dados):
    """
    Atualiza os campos permitidos de um carro existente.
    Campos que NÃO podem ser alterados: id, marca, matricula.
    Campos permitidos: modelo, combustivel, potencia_cv, cilindrada_cc, ano, mes.
    Devolve (200, carro) em caso de sucesso.
    Devolve (404, mensagem) se o carro não for encontrado.
    """
    codigo, resultado = obter_carro(id_carro)
    if codigo != 200:
        return 404, resultado

    campos_permitidos = {"modelo", "combustivel", "potencia_cv", "cilindrada_cc", "ano", "mes"}
    for campo, valor in dados.items():
        if campo in campos_permitidos:
            resultado[campo] = valor
    return 200, resultado


# ── DELETE ────────────────────────────────────────────────────────────────────

def remover_carro(id_carro, manutencoes):
    """
    Remove um carro da lista pelo seu ID.
    Apaga também todas as manutenções associadas (eliminação em cascata).
    Recebe a lista de manutenções como argumento para evitar importação circular.
    Devolve (200, mensagem) em caso de sucesso.
    Devolve (404, mensagem) se o carro não for encontrado.
    """
    codigo, resultado = obter_carro(id_carro)
    if codigo != 200:
        return 404, resultado

    # Elimina em cascata todas as manutenções do carro
    manutencoes[:] = [m for m in manutencoes if m["id_carro"] != id_carro]
    carros.remove(resultado)
    return 200, f"Carro '{resultado['marca']} {resultado['modelo']}' removido com sucesso."