#cliente.py
# Módulo responsável pela gestão de clientes.
# Contém o CRUD completo: adicionar, listar, obter, atualizar e remover clientes.
# Todas as funções devolvem (codigo_http, dados_ou_mensagem):
#   201 → criado com sucesso
#   200 → sucesso
#   404 → não encontrado
#   409 → conflito (email ou nif duplicado)
#   500 → erro nos dados fornecidos

from utils import gerar_id, encontrar_por_id


# Lista em memória que guarda todos os clientes durante a execução
clientes = []


# ── CREATE ────────────────────────────────────────────────────────────────────

def adicionar_cliente(nome, telefone, email, nif):
    """
    Cria um novo cliente e adiciona-o à lista.
    Verifica se o email e o nif já existem antes de adicionar.
    Devolve (201, cliente) em caso de sucesso.
    Devolve (409, mensagem) se o email ou nif já estiverem registados.
    Devolve (500, mensagem) se os dados forem inválidos.
    """
    if not nome or not telefone or not email or not nif:
        return 500, "Todos os campos são obrigatórios."

    # Verificar email duplicado
    if any(c["email"] == email for c in clientes):
        return 409, f"Email '{email}' já está registado."

    # Verificar nif duplicado
    if any(c["nif"] == nif for c in clientes):
        return 409, f"NIF '{nif}' já está registado."

    cliente = {
        "id": gerar_id(clientes),
        "nome": nome,
        "telefone": telefone,
        "email": email,
        "nif": nif
    }
    clientes.append(cliente)
    return 201, cliente


# ── READ ──────────────────────────────────────────────────────────────────────

def listar_clientes():
    """
    Devolve a lista completa de clientes.
    Devolve (200, lista) em caso de sucesso.
    Devolve (404, mensagem) se não existirem clientes.
    """
    if not clientes:
        return 404, "Não existem clientes registados."
    return 200, clientes


def obter_cliente(id_cliente):
    """
    Procura um cliente pelo seu ID.
    Devolve (200, cliente) se encontrado.
    Devolve (404, mensagem) se não encontrado.
    """
    resultado = encontrar_por_id(clientes, id_cliente)
    if not resultado:
        return 404, f"Cliente com ID {id_cliente} não encontrado."
    return 200, resultado


# ── UPDATE ────────────────────────────────────────────────────────────────────

def atualizar_cliente(id_cliente, dados):
    """
    Atualiza os campos permitidos de um cliente existente.
    Campos que NÃO podem ser alterados: id, nif.
    Campos permitidos: nome, telefone, email.
    Devolve (200, cliente) em caso de sucesso.
    Devolve (404, mensagem) se não encontrado.
    Devolve (409, mensagem) se o novo email já estiver registado.
    """
    codigo, cliente = obter_cliente(id_cliente)
    if codigo != 200:
        return 404, cliente

    # Verificar email duplicado se for alterado
    if "email" in dados and dados["email"] != cliente["email"]:
        if any(c["email"] == dados["email"] for c in clientes):
            return 409, f"Email '{dados['email']}' já está registado."

    campos_permitidos = {"nome", "telefone", "email"}
    for campo, valor in dados.items():
        if campo in campos_permitidos:
            cliente[campo] = valor
    return 200, cliente


# ── DELETE ────────────────────────────────────────────────────────────────────

def remover_cliente(id_cliente, carros):
    """
    Remove um cliente da lista pelo seu ID.
    Não permite apagar se tiver carros associados.
    Devolve (200, mensagem) em caso de sucesso.
    Devolve (404, mensagem) se não encontrado.
    Devolve (409, mensagem) se tiver carros associados.
    """
    codigo, cliente = obter_cliente(id_cliente)
    if codigo != 200:
        return 404, cliente

    # Não permitir apagar se tiver carros associados
    if any(c["id_cliente"] == id_cliente for c in carros):
        return 409, "Não é possível apagar o cliente pois tem carros associados."

    clientes.remove(cliente)
    return 200, f"Cliente '{cliente['nome']}' removido com sucesso."
