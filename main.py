"""Processa todos os arquivos de dados/ e gera planilhas CSV em resultados/."""

import os

import pandas as pd

from desenho_primers import calcular_parametros_primer3, listar_arquivos_dna

PASTA_DADOS = "dados"
PASTA_RESULTADOS = "resultados"

os.makedirs(PASTA_RESULTADOS, exist_ok=True)


def nome_csv_saida(nome_arquivo: str) -> str:
    return (
        nome_arquivo.replace(".fasta", "_primers.csv").replace(".txt", "_primers.csv")
    )


def processar_arquivo(nome_arquivo: str) -> bool:
    caminho_entrada = os.path.join(PASTA_DADOS, nome_arquivo)
    caminho_saida = os.path.join(PASTA_RESULTADOS, nome_csv_saida(nome_arquivo))

    with open(caminho_entrada, encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    print(f"Origem : {caminho_entrada}")
    print(f"Destino: {caminho_saida}")

    try:
        resultado = calcular_parametros_primer3(linhas)
    except ValueError as erro:
        print(f"[ERRO] {erro}")
        print("-" * 50)
        return False

    qtd = resultado.get("PRIMER_PAIR_NUM_RETURNED", 0)
    if qtd == 0:
        print(f"[ERRO] Nenhum primer valido para {nome_arquivo}")
        print("-" * 50)
        return False

    linhas_tabela = []
    for i in range(qtd):
        linhas_tabela.append(
            {
                "Par": f"Par_{i + 1}",
                "Primer_Forward": resultado[f"PRIMER_LEFT_{i}_SEQUENCE"],
                "Tm_Forward": round(resultado[f"PRIMER_LEFT_{i}_TM"], 2),
                "Primer_Reverse": resultado[f"PRIMER_RIGHT_{i}_SEQUENCE"],
                "Tm_Reverse": round(resultado[f"PRIMER_RIGHT_{i}_TM"], 2),
                "Tamanho_Produto_pb": resultado[f"PRIMER_PAIR_{i}_PRODUCT_SIZE"],
            }
        )

    pd.DataFrame(linhas_tabela).to_csv(caminho_saida, index=False)
    print(f"[OK] Planilha gerada ({qtd} par(es) de primers)")
    print("-" * 50)
    return True


def main() -> None:
    arquivos = listar_arquivos_dna(PASTA_DADOS)

    print("=" * 50)
    print("  Projeto Py-DNA - lote (dados/ -> resultados/)")
    print("=" * 50)

    if not arquivos:
        print(f"\nNenhum arquivo em '{PASTA_DADOS}/'.")
        print("Adicione arquivos .fasta ou .txt e rode: python main.py")
        return

    ok = 0
    for nome in arquivos:
        print()
        if processar_arquivo(nome):
            ok += 1

    print(f"\nConcluído: {ok}/{len(arquivos)} arquivo(s) processado(s).")
    print("Modo interativo (um arquivo por vez): python desenho_primers.py")


if __name__ == "__main__":
    main()
