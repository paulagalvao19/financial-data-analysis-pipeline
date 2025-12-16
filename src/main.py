from __future__ import annotations  # faz o Python tratar anotações de tipo como texto, não como objeto imediato

from typing import Any, Dict
import pandas as pd
import matplotlib.pyplot as plt
import os


COLUNAS_OBRIGATORIAS: list[str] = [
    "data",
    "descricao",
    "categoria",
    "conta",
    "tipo",
    "valor",
]


def carregar_dados(caminho: str) -> pd.DataFrame:
    if os.path.exists(caminho):
        df = pd.read_csv(caminho)
        return df
    else:
        print(f"Arquivo não encontrado: {caminho}")
        return pd.DataFrame()


def padronizar_colunas(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.strip().str.lower()
    return df


def validar_dados(df: pd.DataFrame) -> None:
    obrigatorias = set(COLUNAS_OBRIGATORIAS)
    colunas_presentes = set(df.columns)
    faltando = sorted(obrigatorias - colunas_presentes)

    if faltando:
        mensagem = (
            "CSV inválido: faltam colunas obrigatórias.\n"
            f"Faltando: {faltando}\n"
            f"Obrigatórias: {sorted(obrigatorias)}\n"
            f"Encontradas no CSV: {sorted(colunas_presentes)}"
        )
        raise ValueError(mensagem)


def gerar_colunas_auxiliares(df: pd.DataFrame) -> pd.DataFrame:
    df["data"] = pd.to_datetime(df["data"], dayfirst=True, errors="coerce")
    df["dia"] = df["data"].dt.day
    df["mes"] = df["data"].dt.month
    df["ano"] = df["data"].dt.year

    # Aqui estamos convertendo o valor com , para . (float)
    df["valor"] = (
        df["valor"]
        .astype(str)
        .str.strip()
        .str.replace(",", ".", regex=False)
    )
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

    df["tipo"] = df["tipo"].astype(str).str.strip().str.lower()

    df["valor_assinado"] = df["valor"]
    df.loc[df["tipo"] == "despesa", "valor_assinado"] *= -1

    return df


def resumo_geral(df: pd.DataFrame) -> Dict[str, Any]:
    total_receita = float(df[df["tipo"] == "receita"]["valor_assinado"].sum())
    total_despesas = float(df[df["tipo"] == "despesa"]["valor_assinado"].sum())
    saldo_final = float(df["valor_assinado"].sum())

    resumo = {
        "total_receita": total_receita,
        "total_despesas": total_despesas,
        "soma_final": saldo_final,
    }
    return resumo


def resumo_por_categoria(df: pd.DataFrame, top_n: int = 5) -> pd.DataFrame:
    despesas = df[df["tipo"] == "despesa"].copy()
    despesas["total_gasto"] = despesas["valor_assinado"].abs()

    resumo_categoria = (
        despesas
        .groupby("categoria", as_index=False)["total_gasto"]
        .sum()
        .sort_values(by="total_gasto", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )
    return resumo_categoria


def resumo_mensal(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["ano", "mes"]).copy()

    df["ano_mes"] = (
        df["ano"].astype("Int64").astype(str)
        + "-"
        + df["mes"].astype("Int64").astype(str).str.zfill(2)
    )

    resumo = (
        df
        .groupby("ano_mes")
        .agg(
            total_receitas=("valor_assinado", lambda x: x[x > 0].sum()),
            total_despesas=("valor_assinado", lambda x: abs(x[x < 0].sum())),
            saldo_mensal=("valor_assinado", "sum"),
        )
        .reset_index()
        .sort_values("ano_mes")
    )

    return resumo


def salvar_dados_limpos(df: pd.DataFrame, caminho_saida: str) -> None:
    diretorio = os.path.dirname(caminho_saida)

    # se não existir o diretório vamos criar
    if diretorio and not os.path.exists(diretorio):
        os.makedirs(diretorio, exist_ok=True)

    df.to_csv(caminho_saida, index=False)

    print(f"✅ Dados limpos salvos com sucesso em: {caminho_saida}")


def gerar_grafico_categorias(resumo_categoria: pd.DataFrame, caminho_saida: str) -> None:
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

    dados = resumo_categoria.sort_values("total_gasto", ascending=True).copy()


    cores = []
    for i in range(len(dados)):
        if i == 0:
            cores.append("#81C784") 
        elif i == len(dados) - 1:
            cores.append("#E57373")  
        else:
            cores.append("#64B5F6") 

    plt.figure(figsize=(9, 5))

    barras = plt.barh(
        dados["categoria"],
        dados["total_gasto"],
        color=cores
    )

    plt.title("Top Gastos por Categoria")
    plt.xlabel("Total Gasto (R$)")
    plt.ylabel("Categoria")

    plt.grid(axis="x", linestyle="--", alpha=0.3)

    for bar in barras:
        valor = bar.get_width()
        plt.text(
            valor,
            bar.get_y() + bar.get_height() / 2,
            f" R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            va="center"
        )

    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=150)
    plt.close()



def gerar_grafico_saldo_mensal(resumo_mes: pd.DataFrame, caminho_saida: str) -> None:
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

    dados = resumo_mes.sort_values("ano_mes").copy()

    idx_melhor = dados["saldo_mensal"].idxmax()
    idx_pior = dados["saldo_mensal"].idxmin()

    melhor_mes = dados.loc[idx_melhor, "ano_mes"]
    pior_mes = dados.loc[idx_pior, "ano_mes"]

    plt.figure(figsize=(11, 5))

    # Linha principal (neutra)
    plt.plot(
        dados["ano_mes"],
        dados["saldo_mensal"],
        color="steelblue",
        linewidth=2,
        marker="o",
        label="Saldo mensal"
    )

    # Linha zero (referência)
    plt.axhline(0, color="gray", linestyle="--", linewidth=1)

    # Melhor mês (verde)
    plt.scatter(
        melhor_mes,
        dados.loc[idx_melhor, "saldo_mensal"],
        color="green",
        s=130,
        label="Melhor mês"
    )

    # Pior mês (vermelho)
    plt.scatter(
        pior_mes,
        dados.loc[idx_pior, "saldo_mensal"],
        color="red",
        s=130,
        label="Pior mês"
    )

    # Anotações
    plt.annotate(
        f"{melhor_mes}\nR$ {dados.loc[idx_melhor, 'saldo_mensal']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        (melhor_mes, dados.loc[idx_melhor, "saldo_mensal"]),
        textcoords="offset points",
        xytext=(10, 10)
    )

    plt.annotate(
        f"{pior_mes}\nR$ {dados.loc[idx_pior, 'saldo_mensal']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        (pior_mes, dados.loc[idx_pior, "saldo_mensal"]),
        textcoords="offset points",
        xytext=(10, -25)
    )

    plt.title("Saldo Mensal (Receitas - Despesas)")
    plt.xlabel("Mês/Ano")
    plt.ylabel("Saldo (R$)")

    plt.grid(True, linestyle="--", alpha=0.35)
    plt.xticks(rotation=45)
    plt.legend()

    plt.tight_layout()
    plt.savefig(caminho_saida, dpi=150)
    plt.close()

    

def main() -> None:
    caminho = "data/raw/gastos.csv"

    try:
        df = carregar_dados(caminho)

        if df.empty:
            print(" Execução interrompida: não foi possível carregar os dados.")
            return

        df = padronizar_colunas(df)
        validar_dados(df)
        df = gerar_colunas_auxiliares(df)

        _resumo = resumo_geral(df)
        _top5 = resumo_por_categoria(df, top_n=5)
        _resumo_mes = resumo_mensal(df)

        gerar_grafico_categorias(
            _top5,
            "dashboard/top_categorias.png"
        )
        gerar_grafico_saldo_mensal(
            _resumo_mes,
            "dashboard/saldo_mensal.png"
        )


        salvar_dados_limpos(df, "data/processed/gastos_limpos.csv")

        # Confirmação curta (pipeline OK)
        print(" Pipeline executado com sucesso. Resumos calculados. Dashboard criados")

    except Exception as e:
        print(f"Falha na execução: {e}")


if __name__ == "__main__":
    main()
