# Projeto-Py-DNA

Projeto das PyLadies para análise de sequências de DNA e design de primers com **Primer3**.

## Estrutura

```
Projeto-Py-DNA/
├── dados/              # Coloque aqui seus .fasta ou .txt
├── resultados/         # CSVs gerados pelo modo lote
├── desenho_primers.py  # Lógica + modo interativo (terminal)
├── main.py             # Modo lote (vários arquivos → tabela CSV)
└── requirements.txt
```

## Instalação

```bash
pip install -r requirements.txt
```

## Como usar

### Modo lote (planilhas)

Processa **todos** os arquivos de `dados/` e salva CSV em `resultados/`:

```bash
python main.py
```

Cada CSV traz: par de primers, Tm forward/reverse e tamanho do produto (pb).

### Modo interativo (terminal)

Escolhe **um** arquivo e vê o resultado na tela:

```bash
python desenho_primers.py
```

## Formato dos arquivos

- **FASTA**: cabeçalho com `>` e sequência nas linhas seguintes
- **TXT**: só a sequência (A, T, C, G)
- Mínimo recomendado: ~100 bases válidas

## Tecnologias

- Python 3
- pandas
- primer3-py
