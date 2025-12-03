# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""


from __future__ import annotations

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# --- Constantes de salida ---
DOCS_DIR = Path("docs")
INPUT_CSV = Path("files/input/shipping-data.csv")

PLOTS = {
    "shipping_per_warehouse": DOCS_DIR / "shipping_per_warehouse.png",
    "mode_of_shipment": DOCS_DIR / "mode_of_shipment.png",
    "average_customer_rating": DOCS_DIR / "average_customer_rating.png",
    "weight_distribution": DOCS_DIR / "weight_distribution.png",
}
INDEX_HTML = DOCS_DIR / "index.html"


def _ensure_docs_dir() -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)


def _clean_spines(ax: plt.Axes, hide_left: bool = False) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if hide_left:
        ax.spines["left"].set_visible(False)


def _save_and_close(fig: plt.Figure, path: Path) -> None:
    fig.savefig(path.as_posix(), bbox_inches="tight")
    plt.close(fig)


def grafico_envios_por_bodega(df: pd.DataFrame) -> None:
    """Crea visualización de Shipping per Warehouse."""
    counts = df["Warehouse_block"].value_counts()

    fig, ax = plt.subplots()
    ax.bar(counts.index.astype(str), counts.values)
    ax.set_title("Shipping per Warehouse")
    ax.set_xlabel("Warehouse block")
    ax.set_ylabel("Record Count")
    ax.tick_params(axis="x", rotation=0, labelsize=8)

    _clean_spines(ax)
    _save_and_close(fig, PLOTS["shipping_per_warehouse"])


def grafico_modo_envio(df: pd.DataFrame) -> None:
    """Crea visualización de Mode of shipment."""
    counts = df["Mode_of_Shipment"].value_counts()

    fig, ax = plt.subplots()
    ax.pie(
        counts.values,
        labels=counts.index.astype(str),
        wedgeprops=dict(width=0.35),
    )
    ax.set_title("Mode of shipment")

    _save_and_close(fig, PLOTS["mode_of_shipment"])


def grafico_promedio_calificacion_cliente(df: pd.DataFrame) -> None:
    """Crea visualización de Average Customer Rating (rango min-max y media)."""
    stats = (
        df.groupby("Mode_of_Shipment")["Customer_rating"]
        .agg(["mean", "min", "max"])
        .sort_index()
    )

    fig, ax = plt.subplots()

    # Barra de fondo: rango [min, max]
    ax.barh(
        y=stats.index.astype(str),
        width=(stats["max"] - stats["min"]).values,
        left=stats["min"].values,
        height=0.9,
        alpha=0.35,
    )

    # Barra de frente: desde min hasta mean
    ax.barh(
        y=stats.index.astype(str),
        width=(stats["mean"] - stats["min"]).values,
        left=stats["min"].values,
        height=0.5,
    )

    ax.set_title("Average Customer Rating")

    ax.spines["left"].set_color("gray")
    ax.spines["bottom"].set_color("gray")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    _save_and_close(fig, PLOTS["average_customer_rating"])


def grafico_distribucion_peso(df: pd.DataFrame) -> None:
    """Crea visualización de Shipped Weight Distribution."""
    fig, ax = plt.subplots()
    ax.hist(df["Weight_in_gms"].dropna(), edgecolor="white")
    ax.set_title("Shipped Weight Distribution")

    _clean_spines(ax)
    _save_and_close(fig, PLOTS["weight_distribution"])


def generar_html_principal() -> None:
    """Crea el archivo docs/index.html con las visualizaciones."""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Shipping Data Dashboard</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    h1 { text-align: center; }
    .container { display: flex; flex-wrap: wrap; justify-content: center; }
    .chart { margin: 20px; text-align: center; }
    img { max-width: 100%; height: auto; border: 1px solid #ddd; }
  </style>
</head>
<body>
  <h1>Shipping Data Dashboard</h1>
  <div class="container">
    <div class="chart"><img src="shipping_per_warehouse.png" alt="Shipping per Warehouse"></div>
    <div class="chart"><img src="mode_of_shipment.png" alt="Mode of Shipment"></div>
    <div class="chart"><img src="average_customer_rating.png" alt="Average Customer Rating"></div>
    <div class="chart"><img src="weight_distribution.png" alt="Weight Distribution"></div>
  </div>
</body>
</html>
"""
    INDEX_HTML.write_text(html, encoding="utf-8")


def pregunta_01():
    """Función principal que genera todas las visualizaciones + index.html."""
    _ensure_docs_dir()

    df = pd.read_csv(INPUT_CSV)

    grafico_envios_por_bodega(df)
    grafico_modo_envio(df)
    grafico_promedio_calificacion_cliente(df)
    grafico_distribucion_peso(df)

    generar_html_principal()



