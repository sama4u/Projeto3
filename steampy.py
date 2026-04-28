#Matheus Araujo Campos RGM: 47211377
#Samuel Victor Giolo Camargo RGM: 47209585
import csv
import os
from datetime import datetime




def texto(valor):
    
    if valor is None or str(valor).strip() == "" or str(valor).lower() == "nan":
        return "Não informado"
    return str(valor).strip()


def numero_float(valor):
    
    try:
        if valor is None or str(valor).strip() == "" or str(valor).lower() == "nan":
            return 0.0
        return float(valor)
    except ValueError:
        return 0.0


def pedir_float(mensagem):
    
    while True:
        try:
            return float(input(mensagem).replace(",", "."))
        except ValueError:
            print("Digite um número válido.")


def pausar():
    input("\nPressione ENTER para continuar...")



class Jogo:
    def __init__(self, id_jogo, titulo, console, genero, publisher, developer,
                 critic_score, total_sales, na_sales, jp_sales, pal_sales,
                 other_sales, release_date):
        self.id = id_jogo
        self.titulo = titulo
        self.console = console
        self.genero = genero
        self.publisher = publisher
        self.developer = developer
        self.critic_score = critic_score
        self.total_sales = total_sales
        self.na_sales = na_sales
        self.jp_sales = jp_sales
        self.pal_sales = pal_sales
        self.other_sales = other_sales
        self.release_date = release_date

    def mostrar_resumido(self):
        return f"ID {self.id} | {self.titulo} | {self.console} | {self.genero} | Nota: {self.critic_score} | Vendas: {self.total_sales}"

    def mostrar_completo(self):
        return (
            f"ID: {self.id}\n"
            f"Título: {self.titulo}\n"
            f"Console: {self.console}\n"
            f"Gênero: {self.genero}\n"
            f"Publisher: {self.publisher}\n"
            f"Developer: {self.developer}\n"
            f"Nota crítica: {self.critic_score}\n"
            f"Vendas totais: {self.total_sales}\n"
            f"Vendas NA: {self.na_sales}\n"
            f"Vendas JP: {self.jp_sales}\n"
            f"Vendas PAL: {self.pal_sales}\n"
            f"Outras vendas: {self.other_sales}\n"
            f"Lançamento: {self.release_date}"
        )



class FilaBacklog:
    def __init__(self):
        self.itens = []

    def enqueue(self, jogo):
        self.itens.append(jogo)

    def dequeue(self):
        if self.is_empty():
            return None
        return self.itens.pop(0)

    def is_empty(self):
        return len(self.itens) == 0

    def mostrar(self):
        if self.is_empty():
            print("Backlog vazio.")
            return

        print("\n===== BACKLOG ATUAL =====")
        for posicao, jogo in enumerate(self.itens, start=1):
            print(f"{posicao}. {jogo.mostrar_resumido()}")

    def tamanho(self):
        return len(self.itens)

    def contem_id(self, id_jogo):
        for jogo in self.itens:
            if jogo.id == id_jogo:
                return True
        return False


class PilhaRecentes:
    def __init__(self, limite=20):
        self.itens = []
        self.limite = limite

    def push(self, jogo):
     
        self.itens = [j for j in self.itens if j.id != jogo.id]
        self.itens.append(jogo)

      
        if len(self.itens) > self.limite:
            self.itens.pop(0)

    def pop(self):
        if self.is_empty():
            return None
        return self.itens.pop()

    def topo(self):
        if self.is_empty():
            return None
        return self.itens[-1]

    def is_empty(self):
        return len(self.itens) == 0

    def mostrar(self):
        if self.is_empty():
            print("Nenhum jogo recente.")
            return

        print("\n===== JOGOS RECENTES =====")
       
        recentes_invertidos = list(reversed(self.itens))
        for posicao, jogo in enumerate(recentes_invertidos, start=1):
            print(f"{posicao}. {jogo.mostrar_resumido()}")

    def tamanho(self):
        return len(self.itens)


class SessaoJogo:
    def __init__(self, jogo, tempo_jogado, tempo_total, status):
        self.jogo = jogo
        self.tempo_jogado = tempo_jogado
        self.tempo_total = tempo_total
        self.data_sessao = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.percentual_simulado = self.calcular_percentual(tempo_total)
        self.status = status

    def calcular_percentual(self, tempo_total):
        
        percentual = (tempo_total / 20) * 100
        if percentual > 100:
            percentual = 100
        return round(percentual, 2)

    def mostrar(self):
        return (
            f"{self.data_sessao} | {self.jogo.titulo} | "
            f"Sessão: {self.tempo_jogado}h | Total: {self.tempo_total}h | "
            f"Progresso: {self.percentual_simulado}% | Status: {self.status}"
        )


class SteamPy:
    def __init__(self):
        self.catalogo = []                 
        self.jogos_por_id = {}             
        self.backlog = FilaBacklog()       
        self.recentes = PilhaRecentes()   
        self.historico = []                
        self.tempos_por_jogo = {}          

        self.arquivo_backlog = "backlog.txt"
        self.arquivo_historico = "historico_jogo.txt"
        self.arquivo_recentes = "recentes.txt"


    def carregar_jogos(self, nome_arquivo):
        if not os.path.exists(nome_arquivo):
            print(f"Arquivo {nome_arquivo} não encontrado.")
            return

        self.catalogo.clear()
        self.jogos_por_id.clear()

        linhas_invalidas = 0

        with open(nome_arquivo, "r", encoding="utf-8", newline="") as arquivo:
            leitor = csv.DictReader(arquivo)

            for indice, linha in enumerate(leitor, start=1):
                try:
                    titulo = texto(linha.get("title"))
                    if titulo == "Não informado":
                        linhas_invalidas += 1
                        continue

                    jogo = Jogo(
                        id_jogo=indice,
                        titulo=titulo,
                        console=texto(linha.get("console")),
                        genero=texto(linha.get("genre")),
                        publisher=texto(linha.get("publisher")),
                        developer=texto(linha.get("developer")),
                        critic_score=numero_float(linha.get("critic_score")),
                        total_sales=numero_float(linha.get("total_sales")),
                        na_sales=numero_float(linha.get("na_sales")),
                        jp_sales=numero_float(linha.get("jp_sales")),
                        pal_sales=numero_float(linha.get("pal_sales")),
                        other_sales=numero_float(linha.get("other_sales")),
                        release_date=texto(linha.get("release_date"))
                    )

                    self.catalogo.append(jogo)
                    self.jogos_por_id[jogo.id] = jogo

                except Exception:
                    linhas_invalidas += 1

        print(f"Catálogo carregado com {len(self.catalogo)} jogos.")
        if linhas_invalidas > 0:
            print(f"Linhas inválidas ignoradas: {linhas_invalidas}")

    def listar_jogos(self, quantidade=20):
        if not self.catalogo:
            print("O catálogo ainda não foi carregado.")
            return

        print(f"\n===== LISTANDO {quantidade} JOGOS =====")
        for jogo in self.catalogo[:quantidade]:
            print(jogo.mostrar_resumido())

    def buscar_jogo_por_nome(self, termo):
        termo = termo.lower().strip()
        resultados = []

        for jogo in self.catalogo:
            if termo in jogo.titulo.lower():
                resultados.append(jogo)

        return resultados

    def filtrar_por_genero(self, genero):
        genero = genero.lower().strip()
        return [jogo for jogo in self.catalogo if genero in jogo.genero.lower()]

    def filtrar_por_console(self, console):
        console = console.lower().strip()
        return [jogo for jogo in self.catalogo if console in jogo.console.lower()]

    def filtrar_por_nota(self, nota_minima):
        return [jogo for jogo in self.catalogo if jogo.critic_score >= nota_minima]

    def filtrar_por_vendas(self, vendas_minimas):
        return [jogo for jogo in self.catalogo if jogo.total_sales >= vendas_minimas]

    def filtrar_por_publisher(self, publisher):
        publisher = publisher.lower().strip()
        return [jogo for jogo in self.catalogo if publisher in jogo.publisher.lower()]

    def ordenar_jogos(self, criterio):
        criterio = criterio.lower().strip()

        if criterio == "titulo":
            return sorted(self.catalogo, key=lambda jogo: jogo.titulo)
        elif criterio == "nota":
            return sorted(self.catalogo, key=lambda jogo: jogo.critic_score, reverse=True)
        elif criterio == "vendas":
            return sorted(self.catalogo, key=lambda jogo: jogo.total_sales, reverse=True)
        elif criterio == "data":
            return sorted(self.catalogo, key=lambda jogo: jogo.release_date, reverse=True)
        elif criterio == "console":
            return sorted(self.catalogo, key=lambda jogo: jogo.console)
        elif criterio == "genero":
            return sorted(self.catalogo, key=lambda jogo: jogo.genero)
        else:
            print("Critério inválido.")
            return []

    def mostrar_resultados(self, resultados, limite=20):
        if not resultados:
            print("Nenhum resultado encontrado.")
            return

        print(f"\nForam encontrados {len(resultados)} resultados. Mostrando até {limite}:")
        for jogo in resultados[:limite]:
            print(jogo.mostrar_resumido())


    def adicionar_ao_backlog(self, jogo):
        if jogo is None:
            print("Jogo não encontrado.")
            return

        if self.backlog.contem_id(jogo.id):
            print("Esse jogo já está no backlog.")
            return

        self.backlog.enqueue(jogo)
        self.salvar_backlog()
        print(f"Jogo adicionado ao backlog: {jogo.titulo}")

    def mostrar_backlog(self):
        self.backlog.mostrar()

    def jogar_proximo(self):
        jogo = self.backlog.dequeue()

        if jogo is None:
            print("Backlog vazio. Não há próximo jogo.")
            return

        print(f"\nPróximo jogo iniciado: {jogo.titulo}")
        self.salvar_backlog()
        tempo = pedir_float("Quanto tempo jogou nesta sessão, em horas? ")
        self.registrar_sessao(jogo, tempo)

    def salvar_backlog(self):
        with open(self.arquivo_backlog, "w", encoding="utf-8") as arquivo:
            for jogo in self.backlog.itens:
                arquivo.write(f"{jogo.id};{jogo.titulo};{jogo.console}\n")

    def carregar_backlog(self):
        if not os.path.exists(self.arquivo_backlog):
            return

        with open(self.arquivo_backlog, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(";")
                if len(partes) >= 1:
                    try:
                        id_jogo = int(partes[0])
                        jogo = self.jogos_por_id.get(id_jogo)
                        if jogo is not None:
                            self.backlog.enqueue(jogo)
                    except ValueError:
                        pass


    def registrar_sessao(self, jogo, tempo):
        if jogo is None:
            print("Jogo não encontrado.")
            return

        if tempo <= 0:
            print("O tempo precisa ser maior que zero.")
            return

        tempo_atual = self.tempos_por_jogo.get(jogo.id, 0.0)
        tempo_total = round(tempo_atual + tempo, 2)
        self.tempos_por_jogo[jogo.id] = tempo_total

        status = self.definir_status(tempo_total)

        sessao = SessaoJogo(jogo, tempo, tempo_total, status)
        self.historico.append(sessao)
        self.recentes.push(jogo)

        self.salvar_historico()
        self.salvar_recentes()

        print("\nSessão registrada com sucesso!")
        print(sessao.mostrar())

    def definir_status(self, tempo_total):
        if tempo_total < 2:
            return "iniciado"
        elif tempo_total < 10:
            return "em andamento"
        elif tempo_total < 20:
            return "muito jogado"
        else:
            return "concluído simbolicamente"

    def mostrar_recentes(self):
        self.recentes.mostrar()

    def retomar_ultimo_jogo(self):
        jogo = self.recentes.topo()

        if jogo is None:
            print("Não existe jogo recente para retomar.")
            return

        print(f"Último jogo retomado: {jogo.titulo}")
        tempo = pedir_float("Quanto tempo jogou nesta sessão, em horas? ")
        self.registrar_sessao(jogo, tempo)


    def mostrar_historico(self):
        if not self.historico:
            print("Histórico vazio.")
            return

        print("\n===== HISTÓRICO COMPLETO =====")
        for sessao in self.historico:
            print(sessao.mostrar())

    def salvar_historico(self):
        with open(self.arquivo_historico, "w", encoding="utf-8") as arquivo:
            arquivo.write("id_jogo;titulo;tempo_sessao;tempo_total;data;status\n")
            for sessao in self.historico:
                arquivo.write(
                    f"{sessao.jogo.id};{sessao.jogo.titulo};{sessao.tempo_jogado};"
                    f"{sessao.tempo_total};{sessao.data_sessao};{sessao.status}\n"
                )

    def carregar_historico(self):
        if not os.path.exists(self.arquivo_historico):
            return

        with open(self.arquivo_historico, "r", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo, delimiter=";")
            for linha in leitor:
                try:
                    id_jogo = int(linha["id_jogo"])
                    jogo = self.jogos_por_id.get(id_jogo)
                    if jogo is None:
                        continue

                    tempo_sessao = numero_float(linha["tempo_sessao"])
                    tempo_total = numero_float(linha["tempo_total"])
                    status = texto(linha["status"])

                    sessao = SessaoJogo(jogo, tempo_sessao, tempo_total, status)
                    sessao.data_sessao = texto(linha["data"])
                    self.historico.append(sessao)
                    self.tempos_por_jogo[id_jogo] = tempo_total

                except Exception:
                    pass

    def salvar_recentes(self):
        with open(self.arquivo_recentes, "w", encoding="utf-8") as arquivo:
            for jogo in self.recentes.itens:
                arquivo.write(f"{jogo.id};{jogo.titulo};{jogo.console}\n")

    def carregar_recentes(self):
        if not os.path.exists(self.arquivo_recentes):
            return

        with open(self.arquivo_recentes, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(";")
                if len(partes) >= 1:
                    try:
                        id_jogo = int(partes[0])
                        jogo = self.jogos_por_id.get(id_jogo)
                        if jogo is not None:
                            self.recentes.push(jogo)
                    except ValueError:
                        pass

    def recomendar_jogos(self):
        if not self.historico:
            print("Ainda não existe histórico suficiente. Jogue alguns jogos primeiro.")
            return []

        genero_favorito = self.obter_mais_comum("genero")
        console_favorito = self.obter_mais_comum("console")
        publisher_favorito = self.obter_mais_comum("publisher")

        notas_jogadas = [sessao.jogo.critic_score for sessao in self.historico if sessao.jogo.critic_score > 0]
        media_nota = sum(notas_jogadas) / len(notas_jogadas) if notas_jogadas else 0

        ids_jogados = set(self.tempos_por_jogo.keys())
        ids_backlog = set(jogo.id for jogo in self.backlog.itens)

        recomendados = []

        for jogo in self.catalogo:
            if jogo.id in ids_jogados:
                continue
            if jogo.id in ids_backlog:
                continue

            pontos = 0

            if jogo.genero == genero_favorito:
                pontos += 3
            if jogo.console == console_favorito:
                pontos += 2
            if jogo.publisher == publisher_favorito:
                pontos += 1
            if jogo.critic_score >= media_nota:
                pontos += 2
            if jogo.total_sales >= 1:
                pontos += 1

            if pontos >= 4:
                recomendados.append((pontos, jogo))

        recomendados.sort(key=lambda item: (item[0], item[1].critic_score, item[1].total_sales), reverse=True)
        lista_final = [jogo for pontos, jogo in recomendados[:10]]

        print("\n===== RECOMENDAÇÕES =====")
        print(f"Critérios usados:")
        print(f"Gênero favorito: {genero_favorito}")
        print(f"Console favorito: {console_favorito}")
        print(f"Publisher recorrente: {publisher_favorito}")
        print(f"Média de nota dos jogos jogados: {round(media_nota, 2)}")
        print("Também foram evitados jogos já jogados e jogos já presentes no backlog.\n")

        self.mostrar_resultados(lista_final, limite=10)
        return lista_final

    def obter_mais_comum(self, campo):
        contagem = {}

        for sessao in self.historico:
            if campo == "genero":
                valor = sessao.jogo.genero
            elif campo == "console":
                valor = sessao.jogo.console
            elif campo == "publisher":
                valor = sessao.jogo.publisher
            else:
                valor = "Não informado"

            contagem[valor] = contagem.get(valor, 0) + 1

        if not contagem:
            return "Não informado"

        return max(contagem, key=contagem.get)

    def gerar_ranking_pessoal(self):
        if not self.historico:
            print("Ainda não existe histórico para montar ranking.")
            return

        print("\n===== RANKING PESSOAL =====")

        print("\n1. Jogos mais jogados:")
        ranking_jogos = sorted(self.tempos_por_jogo.items(), key=lambda item: item[1], reverse=True)
        for posicao, (id_jogo, tempo) in enumerate(ranking_jogos[:10], start=1):
            jogo = self.jogos_por_id.get(id_jogo)
            if jogo:
                print(f"{posicao}. {jogo.titulo} - {tempo}h")

        print("\n2. Gêneros mais jogados:")
        self.mostrar_ranking_por_campo("genero")

        print("\n3. Consoles mais jogados:")
        self.mostrar_ranking_por_campo("console")

        print("\n4. Top jogos por nota dentro do histórico:")
        jogos_unicos = {}
        for sessao in self.historico:
            jogos_unicos[sessao.jogo.id] = sessao.jogo

        top_nota = sorted(jogos_unicos.values(), key=lambda jogo: jogo.critic_score, reverse=True)
        for posicao, jogo in enumerate(top_nota[:10], start=1):
            print(f"{posicao}. {jogo.titulo} | Nota: {jogo.critic_score}")

    def mostrar_ranking_por_campo(self, campo):
        acumulado = {}

        for sessao in self.historico:
            if campo == "genero":
                chave = sessao.jogo.genero
            else:
                chave = sessao.jogo.console

            acumulado[chave] = acumulado.get(chave, 0) + sessao.tempo_jogado

        ranking = sorted(acumulado.items(), key=lambda item: item[1], reverse=True)
        for posicao, (nome, tempo) in enumerate(ranking[:10], start=1):
            print(f"{posicao}. {nome} - {round(tempo, 2)}h")

    def exibir_dashboard(self):
        total_catalogo = len(self.catalogo)
        total_backlog = self.backlog.tamanho()
        total_recentes = self.recentes.tamanho()
        total_sessoes = len(self.historico)
        tempo_total = sum(self.tempos_por_jogo.values())
        media_horas_sessao = tempo_total / total_sessoes if total_sessoes > 0 else 0

        jogo_mais_jogado = "Não informado"
        if self.tempos_por_jogo:
            id_mais_jogado = max(self.tempos_por_jogo, key=self.tempos_por_jogo.get)
            jogo_mais_jogado = self.jogos_por_id[id_mais_jogado].titulo

        genero_favorito = self.obter_mais_comum("genero") if self.historico else "Não informado"
        console_favorito = self.obter_mais_comum("console") if self.historico else "Não informado"

        jogos_jogados = []
        ids_usados = set()
        for sessao in self.historico:
            if sessao.jogo.id not in ids_usados:
                jogos_jogados.append(sessao.jogo)
                ids_usados.add(sessao.jogo.id)

        notas = [jogo.critic_score for jogo in jogos_jogados if jogo.critic_score > 0]
        nota_media = sum(notas) / len(notas) if notas else 0

        iniciados = 0
        em_andamento = 0
        concluidos = 0

        for id_jogo, tempo in self.tempos_por_jogo.items():
            status = self.definir_status(tempo)
            if status == "iniciado":
                iniciados += 1
            elif status == "em andamento" or status == "muito jogado":
                em_andamento += 1
            elif status == "concluído simbolicamente":
                concluidos += 1

        jogo_mais_popular = "Não informado"
        if jogos_jogados:
            jogo_mais_popular = max(jogos_jogados, key=lambda jogo: jogo.total_sales).titulo

        jogo_melhor_nota = "Não informado"
        if jogos_jogados:
            jogo_melhor_nota = max(jogos_jogados, key=lambda jogo: jogo.critic_score).titulo

        total_recomendacoes = len(self.gerar_recomendacoes_sem_mostrar()) if self.historico else 0

        print("\n========== DASHBOARD STEAMPY ==========")
        print(f"Total de jogos no catálogo: {total_catalogo}")
        print(f"Total de jogos no backlog: {total_backlog}")
        print(f"Total de jogos recentes: {total_recentes}")
        print(f"Total de sessões jogadas: {total_sessoes}")
        print(f"Tempo total jogado: {round(tempo_total, 2)}h")
        print(f"Jogo mais jogado: {jogo_mais_jogado}")
        print(f"Gênero favorito: {genero_favorito}")
        print(f"Console favorito: {console_favorito}")
        print(f"Nota média dos jogos jogados: {round(nota_media, 2)}")
        print(f"Total de jogos já iniciados: {iniciados}")
        print(f"Total de jogos em andamento: {em_andamento}")
        print(f"Total de jogos concluídos simbolicamente: {concluidos}")
        print(f"Total de recomendações disponíveis: {total_recomendacoes}")
        print(f"Média de horas por sessão: {round(media_horas_sessao, 2)}h")
        print(f"Jogo mais popular já jogado: {jogo_mais_popular}")
        print(f"Jogo com melhor nota já jogado: {jogo_melhor_nota}")
        print("=======================================")

    def gerar_recomendacoes_sem_mostrar(self):
        if not self.historico:
            return []

        genero_favorito = self.obter_mais_comum("genero")
        console_favorito = self.obter_mais_comum("console")
        ids_jogados = set(self.tempos_por_jogo.keys())
        ids_backlog = set(jogo.id for jogo in self.backlog.itens)

        recomendados = []
        for jogo in self.catalogo:
            if jogo.id in ids_jogados or jogo.id in ids_backlog:
                continue
            if jogo.genero == genero_favorito or jogo.console == console_favorito:
                if jogo.critic_score >= 7 or jogo.total_sales >= 1:
                    recomendados.append(jogo)
        return recomendados[:10]


    def obter_jogo_por_id_digitado(self):
        try:
            id_jogo = int(input("Digite o ID do jogo: "))
            jogo = self.jogos_por_id.get(id_jogo)
            if jogo is None:
                print("Jogo não encontrado.")
            return jogo
        except ValueError:
            print("ID inválido.")
            return None

    def iniciar_sistema(self, arquivo_dataset):
        self.carregar_jogos(arquivo_dataset)
        self.carregar_backlog()
        self.carregar_historico()
        self.carregar_recentes()


def menu():
    sistema = SteamPy()

    arquivo_dataset = "dataset.csv"
    sistema.iniciar_sistema(arquivo_dataset)

    while True:
        print("\n========== STEAMPY ==========")
        print("1. Carregar catálogo")
        print("2. Listar jogos")
        print("3. Buscar jogo por nome")
        print("4. Filtrar por gênero")
        print("5. Filtrar por console")
        print("6. Filtrar por nota")
        print("7. Ordenar catálogo")
        print("8. Adicionar jogo ao backlog")
        print("9. Ver backlog")
        print("10. Jogar próximo do backlog")
        print("11. Ver jogos recentes")
        print("12. Retomar último jogo")
        print("13. Registrar tempo de jogo")
        print("14. Ver histórico completo")
        print("15. Ver recomendações")
        print("16. Ver ranking pessoal")
        print("17. Ver dashboard")
        print("18. Salvar backlog")
        print("19. Filtrar por vendas mínimas")
        print("20. Filtrar por publisher")
        print("0. Sair")
        print("=============================")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            nome = input("Nome do arquivo CSV: ").strip()
            if nome == "":
                nome = arquivo_dataset
            sistema.carregar_jogos(nome)

        elif opcao == "2":
            qtd = input("Quantos jogos deseja listar? Padrão 20: ").strip()
            quantidade = int(qtd) if qtd.isdigit() else 20
            sistema.listar_jogos(quantidade)

        elif opcao == "3":
            termo = input("Digite parte do nome do jogo: ")
            resultados = sistema.buscar_jogo_por_nome(termo)
            sistema.mostrar_resultados(resultados)

        elif opcao == "4":
            genero = input("Digite o gênero: ")
            resultados = sistema.filtrar_por_genero(genero)
            sistema.mostrar_resultados(resultados)

        elif opcao == "5":
            console = input("Digite o console: ")
            resultados = sistema.filtrar_por_console(console)
            sistema.mostrar_resultados(resultados)

        elif opcao == "6":
            nota = pedir_float("Digite a nota mínima: ")
            resultados = sistema.filtrar_por_nota(nota)
            sistema.mostrar_resultados(resultados)

        elif opcao == "7":
            print("Critérios: titulo, nota, vendas, data, console, genero")
            criterio = input("Digite o critério: ")
            resultados = sistema.ordenar_jogos(criterio)
            sistema.mostrar_resultados(resultados)

        elif opcao == "8":
            jogo = sistema.obter_jogo_por_id_digitado()
            sistema.adicionar_ao_backlog(jogo)

        elif opcao == "9":
            sistema.mostrar_backlog()

        elif opcao == "10":
            sistema.jogar_proximo()

        elif opcao == "11":
            sistema.mostrar_recentes()

        elif opcao == "12":
            sistema.retomar_ultimo_jogo()

        elif opcao == "13":
            jogo = sistema.obter_jogo_por_id_digitado()
            if jogo:
                tempo = pedir_float("Quanto tempo jogou nesta sessão, em horas? ")
                sistema.registrar_sessao(jogo, tempo)

        elif opcao == "14":
            sistema.mostrar_historico()

        elif opcao == "15":
            sistema.recomendar_jogos()

        elif opcao == "16":
            sistema.gerar_ranking_pessoal()

        elif opcao == "17":
            sistema.exibir_dashboard()

        elif opcao == "18":
            sistema.salvar_backlog()
            print("Backlog salvo com sucesso.")

        elif opcao == "19":
            vendas = pedir_float("Digite as vendas mínimas: ")
            resultados = sistema.filtrar_por_vendas(vendas)
            sistema.mostrar_resultados(resultados)

        elif opcao == "20":
            publisher = input("Digite o publisher: ")
            resultados = sistema.filtrar_por_publisher(publisher)
            sistema.mostrar_resultados(resultados)

        elif opcao == "0":
            sistema.salvar_backlog()
            sistema.salvar_historico()
            sistema.salvar_recentes()
            print("Dados salvos. Encerrando o SteamPy.")
            break

        else:
            print("Opção inválida.")

        pausar()

if __name__ == "__main__":
    menu()
