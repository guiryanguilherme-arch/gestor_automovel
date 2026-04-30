# oficina.py
# Módulo responsável pela gestão de oficinas.
# Contém o CRUD completo: adicionar, listar, obter, atualizar e remover oficinas.
# Todas as funções devolvem (codigo_http, dados_ou_mensagem):
#   201 → criado com sucesso
#   200 → sucesso
#   404 → não encontrado
#   409 → conflito (email duplicado ou manutenções associadas)
#   500 → erro nos dados fornecidos

from utils import gerar_id,encontrar_por_id


#lista em memoria das oficinas durante a execução
oficinas = []

def adicionar_oficina(nome,morada,telefone,email):
    """ Cria uma nova oficina e adiciona-a à lista.
    Verifica se o email já existe antes de adicionar.
    Devolve (201, oficina) em caso de sucesso.
    Devolve (409, mensagem) se o email já estiver registado.
    Devolve (500, mensagem) se os dados forem inválidos.
    """
    if not nome or not morada or not telefone or not email:
        return 500, "Todos os campos são obrigatórios."

    # Verificar email duplicado (sem indentação extra)
    if any(o["email"] == email for o in oficinas):
        return 409, f"Email '{email}' já está registado."

    oficina = {
        "id": gerar_id(oficinas),
        "nome": nome,
        "morada": morada,
        "telefone": telefone,
        "email": email
    }
    oficinas.append(oficina)
    return 201, oficina


# ── READ ──────────────────────────────────────────────────────────────────────
def listar_oficinas():
    """Devolve a lista completa de oficinas.
    Devolve (200, lista) em caso de sucesso.
    Devolve (404, mensagem) se não existirem oficinas."""

    if not oficinas:
        return 404,"Não existem oficinas registadas."
    return 200,oficinas


def obter_oficina(id_oficina):
    """ Procura uma oficina pelo seu ID.
    Devolve (200, oficina) se encontrada.
    Devolve (404, mensagem) se não encontrada.
    """
    resultado = encontrar_por_id(oficinas, id_oficina)
    if not resultado:
        return 404,f"Oficina com ID {id_oficina} não encontrada."
    return 200,resultado



# ── UPDATE ────────────────────────────────────────────────────────────────────

def atualizar_oficina(id_oficina, dados):
    """Atualiza os campos permitidos de uma oficina existente.
    Campos que não podem ser alterados:Id, nome.
    Campos permitidos: morada, telefone, email.
    Devolve (200, oficina) em caso de sucesso.
    Devolve (404, mensagem) se não encontrada.
    Devolve (409, mensagem) se o novo email já estiver registado."""

    codigo, oficina = obter_oficina(id_oficina)
    if codigo != 200:
        return 404, oficina

    # Verificar email duplicado se for alterado
    if "email" in dados and dados["email"] != oficina["email"]:
        if any(o["email"] == dados["email"] for o in oficinas):
            return 409, f"Email '{dados['email']}' já está registado."

    campos_permitidos = {"morada", "telefone", "email"}
    for campo, valor in dados.items():
        if campo in campos_permitidos:
            oficina[campo] = valor
    return 200, oficina


# ── DELETE ────────────────────────────────────────────────────────────────────

def remover_oficina(id_oficina, manutencoes):
    """ Remove uma oficina da lista pelo seu ID.
    Não permite apagar se tiver manutenções associadas.
    Devolve (200, mensagem) em caso de sucesso.
    Devolve (404, mensagem) se não encontrada.
    Devolve (409, mensagem) se tiver manutenções associadas."""

    codigo, oficina = obter_oficina(id_oficina)
    if codigo != 200:
        return 404, oficina

    # Não permitir apagar se tiver manutenções associadas
    if any(m["id_oficina"] == id_oficina for m in manutencoes):
        return 409, "Não é possível apagar a oficina pois tem manutenções associadas."

    oficinas.remove(oficina)
    return 200, f"Oficina '{oficina['nome']}' removida com sucesso."

