"""Lógica de design de primers com Primer3."""

from __future__ import annotations

import os
import re
from typing import Iterable

import primer3

PASTA_DADOS = "dados"

REGRAS_PADRAO = {
    "PRIMER_OPT_SIZE": 20,
    "PRIMER_OPT_TM": 60.0,
}


def extrair_sequencia_dna(linhas: Iterable[str]) -> str:
    """Lê FASTA ou texto puro e devolve só as bases A/T/C/G."""
    bases: list[str] = []

    for linha in linhas:
        linha = linha.strip()
        if not linha or linha.startswith(">"):
            continue
        bases.append(re.sub(r"[^ATCGatcg]", "", linha))

    return "".join(bases).upper()


def calcular_parametros_primer3(
    linhas: Iterable[str],
    *,
    num_return: int = 3,
) -> dict:
    """Envia a sequência para o Primer3 e retorna o relatório bruto."""
    sequencia = extrair_sequencia_dna(linhas)

    if len(sequencia) < 100:
        raise ValueError(
            f"Sequência muito curta ({len(sequencia)} bp). "
            "O Primer3 precisa de pelo menos ~100 bases válidas (A, T, C, G)."
        )

    dados_do_dna = {"SEQUENCE_TEMPLATE": sequencia}
    regras = {
        **REGRAS_PADRAO,
        "PRIMER_NUM_RETURN": num_return,
    }

    return primer3.bindings.design_primers(dados_do_dna, regras)


def listar_arquivos_dna(pasta: str = PASTA_DADOS) -> list[str]:
    """Lista .fasta e .txt disponíveis na pasta de dados."""
    if not os.path.isdir(pasta):
        return []

    return sorted(
        nome
        for nome in os.listdir(pasta)
        if nome.endswith((".fasta", ".txt"))
    )


def formatar_resultado_console(relatorio: dict, nome_arquivo: str) -> None:
    """Mostra o primeiro par de primers de forma legível no terminal."""
    qtd = relatorio.get("PRIMER_PAIR_NUM_RETURNED", 0)

    if qtd == 0:
        print("\n[ERRO] Nenhum primer valido encontrado para esse DNA.")
        print("Dica: confira se o arquivo tem letras A, T, C e G e tamanho suficiente.")
        return

    print("\n" + "=" * 50)
    print(f"  PRIMERS - {nome_arquivo}")
    print("=" * 50)

    for i in range(qtd):
        print(f"\nPar {i + 1}")
        print(f"  Forward : {relatorio[f'PRIMER_LEFT_{i}_SEQUENCE']}")
        print(f"  Reverse : {relatorio[f'PRIMER_RIGHT_{i}_SEQUENCE']}")
        print(f"  Tm F/R  : {relatorio[f'PRIMER_LEFT_{i}_TM']:.1f}°C / "
              f"{relatorio[f'PRIMER_RIGHT_{i}_TM']:.1f}°C")
        print(f"  Produto : {relatorio[f'PRIMER_PAIR_{i}_PRODUCT_SIZE']} pb")


def menu_interativo() -> None:
    """Modo manual: escolhe um arquivo em dados/ e imprime os primers."""
    arquivos = listar_arquivos_dna()

    print("-" * 50)
    print("     GERADOR DE PRIMERS - modo interativo")
    print("-" * 50)

    if not arquivos:
        print(f"\nNenhum arquivo .fasta ou .txt em '{PASTA_DADOS}/'.")
        print("Coloque suas sequências lá e rode de novo.")
        return

    print("\nArquivos disponíveis:")
    for i, nome in enumerate(arquivos, start=1):
        print(f"  {i} - {nome}")

    print("-" * 50)
    opcao = input("Digite o número do arquivo: ").strip()

    if not opcao.isdigit() or not (1 <= int(opcao) <= len(arquivos)):
        print("[ERRO] Opcao invalida.")
        return

    nome_arquivo = arquivos[int(opcao) - 1]
    caminho = os.path.join(PASTA_DADOS, nome_arquivo)

    print(f"\nLendo {caminho}...")

    with open(caminho, encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()

    try:
        relatorio = calcular_parametros_primer3(linhas)
    except ValueError as erro:
        print(f"\n[ERRO] {erro}")
        return

    print("DNA carregado. Calculando primers...")
    formatar_resultado_console(relatorio, nome_arquivo)


if __name__ == "__main__":
    menu_interativo()
