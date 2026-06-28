import random
from pathlib import Path

bases = "ATCG"
nomes = [
    ("gene_alvo_A.fasta", "Morcego da Fruta", 42),
    ("gene_alvo_B.fasta", "Morcego Vampiro", 99),
    ("gene_alvo_C.fasta", "Morcego Insetivoro", 7),
]
pasta = Path(__file__).resolve().parent.parent / "dados"

for arquivo, desc, seed in nomes:
    random.seed(seed)
    seq = "".join(random.choice(bases) for _ in range(600))
    linhas = [f">{arquivo.replace('.fasta', '')} {desc}"]
    for i in range(0, len(seq), 70):
        linhas.append(seq[i : i + 70])
    pasta.joinpath(arquivo).write_text("\n".join(linhas) + "\n", encoding="utf-8")
    print(f"wrote {arquivo} ({len(seq)} bp)")
