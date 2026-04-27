# main.py
# Ponto de entrada do programa.
# Contém o menu principal e toda a interação com o utilizador.
# Trata os códigos HTTP devolvidos pelas funções de carros.py e manutencao.py:
#   200 → sucesso | 201 → criado | 404 → não encontrado | 409 → conflito | 500 → erro



from carros import (
    adicionar_carro,
    listar_carros,
    obter_carro,
    atualizar_carro,
    remover_carro,
    total_carros,
    COMBUSTIVEIS
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
    TIPOS
)



def ler_id(prompt):
    """Lê um ID introduzido pelo utilizador. Devolve -1 se não for um número válido."""
    valor = input(prompt).strip()
    try:
        return int(valor)
    except ValueError:
        return -1

def main():
    while True:
        # Menu principal
        print("\n🚗 GESTOR DE MANUTENÇÃO AUTOMÓVEL")
        print("1. Adicionar carro")
        print("2. Listar carros")
        print("3. Atualizar carro")
        print("4. Remover carro")
        print("5. Registar manutenção")
        print("6. Atualizar manutenção")
        print("7. Remover manutenção")
        print("8. Marcar manutenção como concluída")
        print("9. Relatórios")
        print("0. Sair")

        op = input("\n👉 ").strip()
        # ── CARROS ────────────────────────────────────────────────────────────
        # Recolhe os dados do novo carro e tenta adicionar
        if op == "1":
            print("\n── Adicionar Carro ──")
            marca = input("Marca: ").strip()
            modelo = input("Modelo: ").strip()
            matricula = input("Matrícula (ex: AB-12-CD): ").strip()
            ano = input("Ano: ").strip()
            mes = input("Mês (1-12): ").strip()

            # Mostra os combustíveis disponíveis e pede escolha por número
            print("Combustíveis:")
            for i, c in enumerate(COMBUSTIVEIS, 1):
                print(f"  {i}. {c}")
            op_comb = input("Escolha o número: ").strip()
            potencia = input("Potência (cv): ").strip()
            cilindrada = input("Cilindrada (cc): ").strip()


            codigo, resultado = adicionar_carro(marca, modelo, matricula, ano, mes, op_comb, potencia, cilindrada)
            if codigo == 201:
                print(f"✅ Carro adicionado com ID {resultado['id']}.")
            elif codigo == 409:
                print(f"❌ Conflito: {resultado}")
            else:
                print(f"❌ Erro {codigo}: {resultado}")

        elif op == "2":
            # Lista todos os carros e oferece ver o histórico de um deles
            print("\n── Lista de Carros ──")
            codigo, resultado = listar_carros()
            if codigo == 200:
                for c in resultado:
                    print(f"  [{c['id']}] {c['marca']} {c['modelo']} | {c['matricula']} | "
                          f"{c['mes']}/{c['ano']} | {c['combustivel']} | "
                          f"{c['potencia_cv']}cv | {c['cilindrada_cc']}cc")

                # Após listar, pergunta se quer ver o histórico de manutenções de um carro
                ver = input("\nVer histórico de manutenções de um carro? (s/n): ").strip().lower()
                if ver == "s":
                    id_carro = ler_id("ID do carro: ")
                    cod_c, res_c = obter_carro(id_carro)
                    if cod_c != 200:
                        print(f"❌ Erro {cod_c}: {res_c}")
                    else:
                        print(f"\n  {res_c['marca']} {res_c['modelo']} | {res_c['matricula']}")
                        cod_h, historico = listar_por_carro(res_c["id"])
                        if cod_h != 200:
                            print("  Sem manutenções registadas.")
                        else:
                            print(f"  {'ID':<5} {'Tipo':<22} {'Data':<12} {'Custo':>8} {'Estado'}")
                            print("  " + "─" * 58)
                            for m in historico:
                                # Usa custo_final se disponível, senão mostra orçamento
                                custo = m["custo_final"] if m["custo_final"] is not None else m["custo_orcamento"]
                                print(f"  [{m['id']}]  {m['tipo']:<22} {m['data_criacao']:<12} "
                                      f"{custo:>7} € {m['estado']}")
            else:
                print(f"❌ Erro {codigo}: {resultado}")

        elif op == "3":
            # Atualiza campos permitidos de um carro (Enter para manter valor atual)
            print("\n── Atualizar Carro ──")
            id_carro = ler_id("ID do carro: ")
            cod_c, carro = obter_carro(id_carro)
            if cod_c != 200:
                print(f"❌ Erro {cod_c}: {carro}")
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

        elif op == "4":
            # Remove o carro e todas as manutenções associadas após confirmação
            print("\n── Remover Carro ──")
            id_carro = ler_id("ID do carro: ")
            confirmar = input("Tens a certeza? (s/n): ").strip().lower()
            if confirmar == "s":
                codigo, resultado = remover_carro(id_carro, manutencoes)
                if codigo == 200:
                    print(f"✅ {resultado}")
                else:
                    print(f"❌ Erro {codigo}: {resultado}")

        # ── MANUTENÇÕES ───────────────────────────────────────────────────────

        elif op == "5":
            # Regista uma nova manutenção para um carro existente
            print("\n── Registar Manutenção ──")
            cod_l, res_l = listar_carros()
            if cod_l != 200:
                print("❌ Não existem carros registados.")
                continue

            id_carro = ler_id("ID do carro: ")
            cod_c, _ = obter_carro(id_carro)
            if cod_c != 200:
                print("❌ Carro não encontrado.")
                continue

            # Mostra os tipos disponíveis e pede escolha por número
            print("Tipos disponíveis:")
            for i, t in enumerate(TIPOS, 1):
                print(f"  {i:2}. {t}")
            op_tipo      = input("Escolha o número: ").strip()
            data_criacao = input("Data criação (DD-MM-YYYY): ").strip()
            custo_orc    = input("Orçamento (€): ").strip()
            descricao    = input("Descrição: ").strip()

            # Campos opcionais: Enter para saltar
            print("Campos opcionais (Enter para saltar):")
            data_man      = input("Data manutenção (DD-MM-YYYY): ").strip() or None
            custo_final_s = input("Custo final (€): ").strip() or None
            folha         = input("Folha de obra ID: ").strip() or None

            codigo, resultado = criar_manutencao(
                int(id_carro), op_tipo, data_criacao,
                custo_orc, descricao, data_man, custo_final_s, folha
            )
            if codigo == 201:
                print(f"✅ Manutenção registada com ID {resultado['id']}.")
            else:
                print(f"❌ Erro {codigo}: {resultado}")

        elif op == "6":
            # Atualiza descrição e/ou custo final de uma manutenção
            print("\n── Atualizar Manutenção ──")
            id_manut = ler_id("ID da manutenção: ")
            cod_m, m = obter_manutencao(id_manut)
            if cod_m != 200:
                print(f"❌ Erro {cod_m}: {m}")
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

        elif op == "7":
            # Remove uma manutenção após confirmação
            print("\n── Remover Manutenção ──")
            id_manut = ler_id("ID da manutenção: ")
            confirmar = input("Tens a certeza? (s/n): ").strip().lower()
            if confirmar == "s":
                codigo, resultado = remover_manutencao(int(id_manut))
                if codigo == 200:
                    print(f"✅ {resultado}")
                else:
                    print(f"❌ Erro {codigo}: {resultado}")

        elif op == "8":
            # Muda o estado de uma manutenção de 'pendente' para 'concluída'
            print("\n── Marcar como Concluída ──")
            id_manut = ler_id("ID da manutenção: ")
            codigo, resultado = atualizar_estado(id_manut, "concluída")
            if codigo == 200:
                print(f"✅ {resultado}")
            else:
                print(f"❌ Erro {codigo}: {resultado}")

        elif op == "9":
            # Mostra estatísticas gerais do sistema
            print("\n── Relatórios ──")
            _, total_c    = total_carros()
            _, total_m    = total_manutencoes()
            _, gasto      = total_gasto()
            cod_med, media = media_gastos()
            print(f"Total carros:         {total_c}")
            print(f"Total manutenções:    {total_m}")
            print(f"Total gasto:          {gasto} €")
            if cod_med != 200:
                media = 0
            print(f"Média por manutenção: {media} €")
            cod_cara, mais_cara = manutencao_mais_cara()
            if cod_cara == 200:
                print(f"Manutenção mais cara: [{mais_cara['id']}] {mais_cara['tipo']}")

        elif op == "0":
            print("\nAté logo! 👋")
            break

        else:
            print("❌ Opção inválida.")


# Ponto de entrada do programa
if __name__ == "__main__":
    main()