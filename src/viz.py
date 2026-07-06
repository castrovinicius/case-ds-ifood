"""Estilo padrão de visualização do projeto (matplotlib).

Paleta categórica e contraste; marcas finas,
grid discreto e rótulos diretos seletivos.
"""

import matplotlib.pyplot as plt

# Paleta categórica (ordem fixa, nunca reciclar cores)
SERIES = ["#2a78d6", "#1baf7a", "#eda100", "#C507C5", "#4a3aa7", "#e34948"]

# Rampa sequencial (azul, claro -> escuro) para estágios ordenados
SEQ = ["#86b6ef", "#3987e5", "#1c5cab"]

INK = "#0b0b0b"        # texto principal
INK_SOFT = "#52514e"   # texto secundário
MUTED = "#898781"      # eixos / rótulos de apoio
GRID = "#e1e0d9"       # linhas de grade
BASELINE = "#c3c2b7"   # linha de base


def setup_style() -> None:
    """Aplica o estilo padrão do projeto aos gráficos matplotlib."""
    plt.rcParams.update(
        {
            "figure.figsize": (9, 4.5),
            "figure.dpi": 110,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": BASELINE,
            "axes.labelcolor": INK_SOFT,
            "axes.titlecolor": INK,
            "axes.titlesize": 12,
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.spines.left": False,
            "axes.grid": True,
            "axes.axisbelow": True,
            "grid.color": GRID,
            "grid.linewidth": 0.8,
            "xtick.color": MUTED,
            "ytick.color": MUTED,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.frameon": False,
            "legend.fontsize": 9,
            "font.size": 10,
            # rótulos contêm "R$": não interpretar $...$ como mathtext
            "text.parse_math": False,
        }
    )
