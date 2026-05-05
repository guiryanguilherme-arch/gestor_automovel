# main.py
# Ponto de entrada do programa.
# Contém o menu principal e toda a interação com o utilizador.
# Trata os códigos HTTP devolvidos pelas funções de cada módulo:
#   200 → sucesso | 201 → criado | 404 → não encontrado | 409 → conflito | 500 → erro


from carros import (
    adicionar_carro,
    listar_carros,
    obter_carro,
    atualizar_carro,
    remover_carro,
    total_carros,
    COMBUSTIVEIS,
)
from manutencao import (
    criar_manutencao,
    obter_manutencao,
    atualizar_manutencao,
    remover_manutencao,
    atualizar_estado,
    listar_por_carro,
    total_manutencoes,
    total_gasto,
    media_gastos,
    manutencao_mais_cara,
    manutencoes,
    TIPOS,
)
from cliente import (
    adicionar_cliente,
    listar_clientes,
    obter_cliente,
    atualizar_cliente,
    remover_cliente,
)
from oficina import (
    adicionar_oficina,
    listar_oficinas,
    obter_oficina,
    atualizar_oficina,
    remover_oficina,
    oficinas,
)
from carros import carros


def ler_id(prompt):
    """Lê um ID introduzido pelo utilizador. Devolve -1 se não for um número válido."""
    valor = input(prompt).strip()
    try:
        return int(valor)
    except ValueError:
        return -1


def main():
    while True:
        print("\n🚗 GESTOR DE MANUTENÇÃO AUTOMÓVEL")
        print("── Clientes ──────────")
        print(" 1. Adicionar cliente")
        print(" 2. Listar clientes")
        print(" 3. Atualizar cliente")
        print(" 4. Remover cliente")
        print("── Oficinas ──────────")
        print(" 5. Adicionar oficina")
        print(" 6. Listar oficinas")
        print(" 7. Atualizar oficina")
        print(" 8. Remover oficina")
        print("── Carros ────────────")
        print(" 9. Adicionar carro")
        print("10. Listar carros")
        print("11. Atualizar carro")
        print("12. Remover carro")
        print("── Manutenções ───────")
        print("13. Registar manutenção")
        print("14. Atualizar manutenção")
        print("15. Remover manutenção")
        print("16. Marcar como concluída")
        print("── Relatórios ────────")
        print("17. Relatórios")
        print(" 0. Sair")

        op = input("\n👉 ").strip()

        # ── CARROS ────────────────────────────────────────────────────────────

        if op == "1":
            print("\n── Adicionar Cliente ──")
            nome = input("Nome: ").strip()
            telefone = input("Telefone: ").strip()
            email = input("Email: ").strip()
            nif = input("NIF: ").strip()
            codigo, resultado = adicionar_cliente(nome, telefone, email, nif)
            if codigo == 201:
                print(f"✅ Cliente '{resultado['nome']}' adicionado com ID {resultado['id']}.")
            elif codigo == 409:
                print(f"❌ Conflito: {resultado}")
            else:
                print(f"❌ Erro {codigo}: {resultado}")


        elif op == "2":
            print("\n── Lista de Clientes ──")
            codigo, resultado = listar_clientes()
            if codigo == 200:
                for cl in resultado:
                    print(f"  [{cl['id']}] {cl['nome']} | {cl['email']} | NIF: {cl['nif']}")
            else:
                print(f"❌ {resultado}")


        elif op == "3":
            print("\n── Atualizar Cliente ──")
            id_cliente = ler_id("ID do cliente: ")
            codigo, cliente = obter_cliente(id_cliente)
            if codigo != 200:
                print(f"❌ {cliente}")
                continue
            print(f"  A editar: {cliente['nome']} (Enter para manter)")
            dados = {}
            novo_nome = input(f"  Nome [{cliente['nome']}]: ").strip()
            if novo_nome:
                dados["nome"] = novo_nome
            novo_tel = input(f"  Telefone [{cliente['telefone']}]: ").strip()
            if novo_tel:
                dados["telefone"] = novo_tel
            novo_email = input(f"  Email [{cliente['email']}]: ").strip()
            if novo_email:
                dados["email"] = novo_email
            if dados:
                codigo, resultado = atualizar_cliente(id_cliente, dados)
                if codigo == 200:
                    print("✅ Cliente atualizado com sucesso.")
                else:
                    print(f"❌ Erro {codigo}: {resultado}")
            else:
                print("Nenhuma alteração efectuada.")


        elif op == "4":
            print("\n── Remover Cliente ──")
            id_cliente = ler_id("ID do cliente: ")
            codigo, cliente = obter_cliente(id_cliente)
            if codigo != 200:
                print(f"❌ {cliente}")
                continue
            confirmar = input(f"Remover '{cliente['nome']}'? (s/n): ").strip().lower()
            if confirmar == "s":
                codigo, resultado = remover_cliente(id_cliente, carros)
                if codigo == 200:
                    print(f"✅ {resultado}")
                else:
                    print(f"❌ Erro {codigo}: {resultado}")

                # ── OFICINAS ──────────────────────────────────────────────────────────

        elif op == "5":
            print("\n── Adicionar Oficina ──")
            nome = input("Nome: ").strip()
            morada = input("Morada: ").strip()
            telefone = input("Telefone: ").strip()
            email = input("Email: ").strip()
            codigo, resultado = adicionar_oficina(nome, morada, telefone, email)
            if codigo == 201:
                print(f"✅ Oficina '{resultado['nome']}' adicionada com ID {resultado['id']}.")
            elif codigo == 409:
                print(print(f"✅ Removido com sucesso."))
            else:
                print(f"❌ Erro {codigo}: {resultado}")


        elif op == "6":
            print("\n── Lista de Oficinas ──")
            codigo, resultado = listar_oficinas()
            if codigo == 200:
                for o in resultado:
                    print(f"  [{o['id']}] {o['nome']} | {o['morada']} | {o['email']}")
            else:
                print(f"❌ {resultado}")


        elif op == "7":
            print("\n── Atualizar Oficina ──")
            id_oficina = ler_id("ID da oficina: ")
            codigo, oficina = obter_oficina(id_oficina)
            if codigo != 200:
                print(f"❌ {oficina}")
                continue
            print(f"  A editar: {oficina['nome']} (Enter para manter)")
            dados = {}
            nova_morada = input(f"  Morada [{oficina['morada']}]: ").strip()
            if nova_morada:
                dados["morada"] = nova_morada
            novo_tel = input(f"  Telefone [{oficina['telefone']}]: ").strip()
            if novo_tel:
                dados["telefone"] = novo_tel
            novo_email = input(f"  Email [{oficina['email']}]: ").strip()
            if novo_email:
                dados["email"] = novo_email
            if dados:
                codigo, resultado = atualizar_oficina(id_oficina, dados)
                if codigo == 200:
                    print("✅ Oficina atualizada com sucesso.")
                else:
                    print(f"❌ Erro {codigo}: {resultado}")
            else:
                print("Nenhuma alteração efectuada.")


        elif op == "8":
            print("\n── Remover Oficina ──")
            id_oficina = ler_id("ID da oficina: ")
            codigo, oficina = obter_oficina(id_oficina)
            if codigo != 200:
                print(f"❌ {oficina}")
                continue
            confirmar = input(f"Remover '{oficina['nome']}'? (s/n): ").strip().lower()
            if confirmar == "s":
                codigo, resultado = remover_oficina(id_oficina, manutencoes)
                if codigo == 200:
                    print(print(f"✅ Removido com sucesso."))
                else:
                    print(f"❌ Erro {codigo}: {resultado}")


        elif op == "9":
            print("\n── Adicionar Carro ──")
            codigo, resultado = listar_clientes()
            if codigo != 200:
                print("❌ Não existem clientes. Adiciona um cliente primeiro.")
                continue
            for cl in resultado:
                print(f"  [{cl['id']}] {cl['nome']}")
            id_cliente = ler_id("ID do cliente: ")
            if obter_cliente(id_cliente)[0] != 200:
                print("❌ Cliente não encontrado.")
                continue
            marca = input("Marca: ").strip()
            modelo = input("Modelo: ").strip()
            matricula = input("Matrícula (ex: AB-12-CD): ").strip()
            ano = input("Ano: ").strip()
            mes = input("Mês (1-12): ").strip()
            print("Combustíveis:")
            for i, c in enumerate(COMBUSTIVEIS, 1):
                print(f"  {i}. {c}")
            op_comb = input("Escolha o número: ").strip()
            try:
                combustivel = COMBUSTIVEIS(int(op_comb) - 1)
            except (ValueError, IndexError):
                print("❌ Opção de combustível inválida.")
                continue
            potencia = input("Potência (cv): ").strip()
            cilindrada = input("Cilindrada (cc): ").strip()
            codigo, resultado = adicionar_carro(id_cliente, marca, modelo, matricula, ano, mes, combustivel, potencia,
                                                cilindrada)
            if codigo == 201:
                print(f"✅ Carro adicionado com ID {resultado['id']}.")
            elif codigo == 409:
                print(f"❌ Conflito: {resultado}")
            else:
                print(f"❌ Erro {codigo}: {resultado}")


        elif op == "10":
            print("\n── Lista de Carros ──")
            codigo, resultado = listar_carros()
            if codigo == 200:
                for c in resultado:
                    print(f"  [{c['id']}] {c['marca']} {c['modelo']} | {c['matricula']} | "
                          f"{c['mes']}/{c['ano']} | {c['combustivel']} | "
                          f"{c['potencia_cv']}cv | {c['cilindrada_cc']}cc")
                ver = input("\nVer histórico de manutenções de um carro? (s/n): ").strip().lower()
                if ver == "s":
                    id_carro = ler_id("ID do carro: ")
                    cod_c, res_c = obter_carro(id_carro)
                    if cod_c != 200:
                        print(f"❌ {res_c}")
                    else:
                        print(f"\n  {res_c['marca']} {res_c['modelo']} | {res_c['matricula']}")
                        cod_h, historico = listar_por_carro(res_c["id"])
                        if cod_h != 200:
                            print("  Sem manutenções registadas.")
                        else:
                            print(f"  {'ID':<5} {'Tipo':<22} {'Data':<12} {'Custo':>8} {'Estado'}")
                            print("  " + "─" * 58)
                            for m in historico:
                                custo = m["custo_final"] if m["custo_final"] is not None else m["custo_orcamento"]
                                print(f"  [{m['id']}]  {m['tipo']:<22} {m['data_criacao']:<12} "
                                      f"{custo:>7} € {m['estado']}")
            else:
                print(f"❌ {resultado}")


        elif op == "11":
            print("\n── Atualizar Carro ──")
            id_carro = ler_id("ID do carro: ")
            cod_c, carro = obter_carro(id_carro)
            if cod_c != 200:
                print(f"❌ {carro}")
                continue
            print(f"  A editar: {carro['marca']} {carro['modelo']} (Enter para manter)")
            dados = {}
            novo_modelo = input(f"  Modelo [{carro['modelo']}]: ").strip()
            if novo_modelo:
                dados["modelo"] = novo_modelo
            novo_ano = input(f"  Ano [{carro['ano']}]: ").strip()
            if novo_ano:
                dados["ano"] = novo_ano
            novo_mes = input(f"  Mês [{carro['mes']}]: ").strip()
            if novo_mes:
                dados["mes"] = novo_mes
            if dados:
                codigo, resultado = atualizar_carro(carro["id"], dados)
                if codigo == 200:
                    print("✅ Carro atualizado com sucesso.")
                else:
                    print(f"❌ Erro {codigo}: {resultado}")
            else:
                print("Nenhuma alteração efectuada.")


        elif op == "12":
            print("\n── Remover Carro ──")
            id_carro = ler_id("ID do carro: ")
            cod_c, carro = obter_carro(id_carro)
            if cod_c != 200:
                print(f"❌ {carro}")
                continue
            confirmar = input(f"Remover '{carro['marca']} {carro['modelo']}'? (s/n): ").strip().lower()
            if confirmar == "s":
                codigo, resultado = remover_carro(id_carro, manutencoes)
                if codigo == 200:
                    print(f"✅ {resultado}")
                else:
                    print(f"❌ Erro {codigo}: {resultado}")

            # ── MANUTENÇÕES ───────────────────────────────────────────────────────

        elif op == "13":
            print("\n── Registar Manutenção ──")
            codigo, resultado = listar_carros()
            if codigo != 200:
                print("❌ Não existem carros registados.")
                continue
            for c in resultado:
                print(f"  [{c['id']}] {c['marca']} {c['modelo']} | {c['matricula']}")
            id_carro = ler_id("ID do carro: ")
            if obter_carro(id_carro)[0] != 200:
                print("❌ Carro não encontrado.")
                continue
            codigo, resultado = listar_oficinas()
            if codigo != 200:
                print("❌ Não existem oficinas registadas.")
                continue
            for o in resultado:
                print(f"  [{o['id']}] {o['nome']}")
            id_oficina = ler_id("ID da oficina: ")
            if obter_oficina(id_oficina)[0] != 200:
                print("❌ Oficina não encontrada.")
                continue
            print("Tipos disponíveis:")
            for i, t in enumerate(TIPOS, 1):
                print(f"  {i:2}. {t}")
            op_tipo = input("Escolha o número: ").strip()
            try:
                tipo = TIPOS[int(op_tipo) - 1]
            except (ValueError, IndexError):
                print("❌ Tipo inválido.")
                continue
            data_criacao = input("Data criação (DD-MM-YYYY): ").strip()
            custo_orc = input("Orçamento (€): ").strip()
            descricao = input("Descrição: ").strip()
            print("Campos opcionais (Enter para saltar):")
            data_man = input("Data manutenção (DD-MM-YYYY): ").strip() or None
            custo_final_s = input("Custo final (€): ").strip() or None
            folha = input("Folha de obra ID: ").strip() or None
            codigo, resultado = criar_manutencao(
                id_carro, id_oficina, tipo, data_criacao,
                custo_orc, descricao, data_man, custo_final_s, folha
            )
            if codigo == 201:
                print(f"✅ Manutenção registada com ID {resultado['id']}.")
            else:
                print(f"❌ Erro {codigo}: {resultado}")


        elif op == "14":
            print("\n── Atualizar Manutenção ──")
            id_manut = ler_id("ID da manutenção: ")
            cod_m, m = obter_manutencao(id_manut)
            if cod_m != 200:
                print(f"❌ {m}")
                continue
            dados = {}
            nova_desc = input(f"  Descrição [{m['descricao']}]: ").strip()
            if nova_desc:
                dados["descricao"] = nova_desc
            novo_custo = input(f"  Custo final [{m['custo_final']}]: ").strip()
            if novo_custo:
                dados["custo_final"] = novo_custo
            if dados:
                codigo, resultado = atualizar_manutencao(m["id"], dados)
                if codigo == 200:
                    print("✅ Manutenção atualizada com sucesso.")
                else:
                    print(f"❌ Erro {codigo}: {resultado}")
            else:
                print("Nenhuma alteração efectuada.")

        elif op == "15":
            print("\n── Remover Manutenção ──")
            id_manut = ler_id("ID da manutenção: ")
            cod_m, m = obter_manutencao(id_manut)
            if cod_m != 200:
                print(f"❌ {m}")
                continue
            confirmar = input(f"Remover manutenção ID {id_manut}? (s/n): ").strip().lower()
            if confirmar == "s":
                codigo, resultado = remover_manutencao(id_manut)
                if codigo == 200:
                    print(f"✅ {resultado}")
                else:
                    print(f"❌ Erro {codigo}: {resultado}")

        elif op == "16":
            print("\n── Marcar como Concluída ──")
            id_manut = ler_id("ID da manutenção: ")
            codigo, resultado = atualizar_estado(id_manut, "concluída")
            if codigo == 200:
                print(f"✅ {resultado}")
            else:
                print(f"❌ Erro {codigo}: {resultado}")

            # ── RELATÓRIOS ────────────────────────────────────────────────────────

        elif op == "17":
            print("\n── Relatórios ──")
            _, total_c = total_carros()
            _, total_m = total_manutencoes()
            _, gasto = total_gasto()
            cod_med, media = media_gastos()
            if cod_med != 200:
                media = 0
            print(f"  Total clientes:       {len(oficinas)}")
            print(f"  Total carros:         {total_c}")
            print(f"  Total manutenções:    {total_m}")
            print(f"  Total gasto:          {gasto:.2f} €")
            print(f"  Média por manutenção: {media:.2f} €")
            cod_cara, mais_cara = manutencao_mais_cara()
            if cod_cara == 200:
                print(f"  Manutenção mais cara: [{mais_cara['id']}] {mais_cara['tipo']}")


        elif op == "0":
            print("\nAté logo! 👋")
            break

        else:
            print("❌ Opção inválida.")


# Ponto de entrada do programa
if __name__ == "__main__":
    main()