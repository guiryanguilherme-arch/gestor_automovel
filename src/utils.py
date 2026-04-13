# utils.py
# Funções utilitárias genéricas usadas pelos outros módulos.
# Contém: geração de IDs, busca por ID, validação de números e operações sobre listas.
# Nota: validação de datas está em manutencao.py, onde é usada diretamente.


# ── IDs ───────────────────────────────────────────────────────────────────────

def gerar_id(lista):
    """
    Gera um novo ID único para qualquer lista de dicionários.
    Usa o maior ID existente + 1 para evitar duplicados ao apagar itens.
    Exemplo: gerar_id(carros) ou gerar_id(manutencoes)
    """
    if not lista:
        return 1
    return max(item["id"] for item in lista) + 1


# ── BUSCA ─────────────────────────────────────────────────────────────────────

def encontrar_por_id(lista, id_item):
    """
    Procura e devolve o dicionário cujo campo "id" corresponde a id_item.
    Devolve None se não encontrar.
    """
    for item in lista:
        if item.get("id") == id_item:
            return item
    return None


def existe_id(lista, id_item):
    """Devolve True se existir um item com o id dado, False caso contrário."""
    return encontrar_por_id(lista, id_item) is not None


# ── NÚMEROS ───────────────────────────────────────────────────────────────────

def validar_numero(valor):
    """
    Converte valor para float e verifica que não é negativo.
    Devolve o float se válido, ou None se inválido ou negativo.
    """
    try:
        n = float(valor)
        if n < 0:
            return None
        return n
    except (ValueError, TypeError):
        return None


def validar_inteiro(valor):
    """
    Converte valor para int e verifica que é positivo (> 0).
    Devolve o int se válido, ou None se inválido ou não positivo.
    """
    try:
        n = int(valor)
        if n <= 0:
            return None
        return n
    except (ValueError, TypeError):
        return None


# ── LISTAS ────────────────────────────────────────────────────────────────────

def filtrar(lista, campo, valor):
    """
    Filtra uma lista de dicionários devolvendo apenas os que têm campo == valor.
    Exemplo: filtrar(carros, "combustivel", "Elétrico")
    """
    return [item for item in lista if item.get(campo) == valor]


def ordenar_por(lista, campo, reverso=False):
    """
    Ordena uma lista de dicionários por um campo específico.
    reverso=True para ordem decrescente.
    Exemplo: ordenar_por(manutencoes, "custo_orcamento", reverso=True)
    """
    return sorted(lista, key=lambda x: x.get(campo, 0), reverse=reverso)


# ── UTILIDADES ────────────────────────────────────────────────────────────────

def contar(lista):
    """Devolve o número de elementos numa lista."""
    return len(lista)


def somar(lista, campo):
    """Soma os valores de um campo numérico em todos os dicionários da lista."""
    return sum(item.get(campo, 0) for item in lista)


def maior(lista, campo):
    """Devolve o dicionário com o maior valor num campo. Devolve None se lista vazia."""
    if not lista:
        return None
    return max(lista, key=lambda x: x.get(campo, 0))


def menor(lista, campo):
    """Devolve o dicionário com o menor valor num campo. Devolve None se lista vazia."""
    if not lista:
        return None
    return min(lista, key=lambda x: x.get(campo, 0))