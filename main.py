import os
import pandas as pd

from desenho_primers import calcular_parametros_primer3

PASTA_DADOS = "dados"
PASTA_RESULTADOS = "resultados"

os.makedirs(PASTA_RESULTADOS, exist_ok=True)

print("Iniciando a leitura das pastas...")

for nome_arquivo in os.listdir(PASTA_DADOS):
    if nome_arquivo.endswith(".fasta") or nome_arquivo.endswith(".txt"):

        caminho_entrada = os.path.join(PASTA_DADOS, nome_arquivo)
        nome_saida = nome_arquivo.replace(".fasta", "_primers.csv").replace(".txt", "_primers.csv")
        caminho_saida = os.path.join(PASTA_RESULTADOS, nome_saida)

        with open(caminho_entrada, "r") as f:
            linhas = f.readlines()

        print(f"Arquivo de origem encontrado: {caminho_entrada}")
        print(f"Arquivo de destino mapeado: {caminho_saida}")

        # ====================================================================
        # 1. ENVIANDO OS DADOS: Aqui chamamos a função do arquivo desenho_primers
        # ====================================================================
        resultado_primer3 = calcular_parametros_primer3(linhas)
        qtd_encontrada = resultado_primer3.get('PRIMER_PAIR_NUM_RETURNED', 0)

        # Proteção: se o desenho_primers não achar nada para esse gene, pula pro próximo
        if qtd_encontrada == 0:
            print(f"❌ Nenhum primer válido encontrado para {nome_arquivo}")
            print("-" * 30)
            continue
 # Criamos uma lista vazia para guardar as linhas da tabela
        linhas_da_tabela = []

        # Pegamos os dados do Primer3 e organizamos de forma amigável
        for i in range(qtd_encontrada):
            dados_do_par = {
                "Par": f"Par_{i+1}",
                "Primer_Forward": resultado_primer3[f'PRIMER_LEFT_{i}_SEQUENCE'],
                "Tm_Forward": round(resultado_primer3[f'PRIMER_LEFT_{i}_TM'], 2),
                "Primer_Reverse": resultado_primer3[f'PRIMER_RIGHT_{i}_SEQUENCE'],
                "Tm_Reverse": round(resultado_primer3[f'PRIMER_RIGHT_{i}_TM'], 2)
            }
            linhas_da_tabela.append(dados_do_par)

        # O Pandas transforma a lista diretamente em uma planilha e salva no HD!
        tabela_final = pd.DataFrame(linhas_da_tabela)
        tabela_final.to_csv(caminho_saida, index=False)

        print(f"✓ Planilha de resultados gerada com sucesso!")
        print("-" * 30)
