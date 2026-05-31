"""
Projeto: Análise da Cotação USD/BRL (2010-2019)
Dataset: USD_BRL_hist.csv
Descrição: Visualização da evolução do dólar frente ao real brasileiro
           com três tipos de gráficos distintos.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ─────────────────────────────────────────────
# CARREGAMENTO E TRATAMENTO DOS DADOS
# ─────────────────────────────────────────────

df = pd.read_csv("USD_BRL_hist.csv")

# Converte a coluna de data para o formato correto
df['Data'] = pd.to_datetime(df['Data'], format='%d.%m.%Y')

# Ordena cronologicamente (garante que o gráfico de linha fique correto)
df = df.sort_values('Data').reset_index(drop=True)

# Extrai o ano para agrupamentos
df['Ano'] = df['Data'].dt.year

# ─────────────────────────────────────────────
# ESTILO GERAL DOS GRÁFICOS
# ─────────────────────────────────────────────

plt.rcParams.update({
    'figure.facecolor': '#F7F9FC',
    'axes.facecolor':   '#F7F9FC',
    'axes.edgecolor':   '#CCCCCC',
    'axes.spines.top':  False,
    'axes.spines.right': False,
    'grid.color':       '#E0E0E0',
    'grid.linestyle':   '--',
    'grid.linewidth':   0.7,
    'font.family':      'DejaVu Sans',
    'axes.titlesize':   14,
    'axes.titleweight': 'bold',
    'axes.labelsize':   11,
    'xtick.labelsize':  10,
    'ytick.labelsize':  10,
})

# ─────────────────────────────────────────────
# GRÁFICO 1 — LINHA: Evolução temporal da cotação
# ─────────────────────────────────────────────
# Adequado para dados contínuos no tempo, mostrando tendência e variação diária.

fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(df['Data'], df['USD_BRL'],
        color='#1565C0', linewidth=1.2, alpha=0.85)

# Destaque para o valor mínimo e máximo
idx_min = df['USD_BRL'].idxmin()
idx_max = df['USD_BRL'].idxmax()

ax.scatter(df.loc[idx_min, 'Data'], df.loc[idx_min, 'USD_BRL'],
           color='#2E7D32', zorder=5, s=60)
ax.scatter(df.loc[idx_max, 'Data'], df.loc[idx_max, 'USD_BRL'],
           color='#C62828', zorder=5, s=60)

ax.annotate(f"Mín: R$ {df.loc[idx_min, 'USD_BRL']:.2f}",
            xy=(df.loc[idx_min, 'Data'], df.loc[idx_min, 'USD_BRL']),
            xytext=(30, 12), textcoords='offset points',
            color='#2E7D32', fontsize=9,
            arrowprops=dict(arrowstyle='->', color='#2E7D32', lw=1))

ax.annotate(f"Máx: R$ {df.loc[idx_max, 'USD_BRL']:.2f}",
            xy=(df.loc[idx_max, 'Data'], df.loc[idx_max, 'USD_BRL']),
            xytext=(30, -18), textcoords='offset points',
            color='#C62828', fontsize=9,
            arrowprops=dict(arrowstyle='->', color='#C62828', lw=1))

ax.set_title('Evolução Diária da Cotação USD/BRL (2010–2019)')
ax.set_xlabel('Ano')
ax.set_ylabel('Cotação (R$)')
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('R$ %.2f'))
ax.grid(True, axis='y')

plt.tight_layout()
plt.savefig('grafico1_linha.png', dpi=150, bbox_inches='tight')
plt.show()
print("✔ Gráfico 1 salvo: grafico1_linha.png")

# ─────────────────────────────────────────────
# GRÁFICO 2 — BARRAS: Média anual da cotação
# ─────────────────────────────────────────────
# Adequado para comparação de valores agregados por categoria (ano).

media_anual = df.groupby('Ano')['USD_BRL'].mean()

fig, ax = plt.subplots(figsize=(11, 6))

cores = ['#1565C0' if v < media_anual.mean() else '#C62828'
         for v in media_anual.values]

bars = ax.bar(media_anual.index, media_anual.values,
              color=cores, edgecolor='white', linewidth=0.8)

# Rótulos de valor em cima de cada barra
for bar, val in zip(bars, media_anual.values):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.03,
            f'R$ {val:.2f}',
            ha='center', va='bottom', fontsize=9, color='#333333')

# Linha de média geral
media_geral = media_anual.mean()
ax.axhline(media_geral, color='#555555', linestyle='--', linewidth=1.2,
           label=f'Média geral: R$ {media_geral:.2f}')

ax.set_title('Cotação Média Anual do Dólar (USD/BRL) por Ano')
ax.set_xlabel('Ano')
ax.set_ylabel('Cotação Média (R$)')
ax.set_xticks(media_anual.index)
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('R$ %.2f'))
ax.legend(fontsize=10)
ax.grid(True, axis='y')

# Legenda de cores
from matplotlib.patches import Patch
legend_cores = [Patch(color='#1565C0', label='Abaixo da média geral'),
                Patch(color='#C62828', label='Acima da média geral')]
ax.legend(handles=legend_cores + ax.get_legend_handles_labels()[0][1:],
          fontsize=9, loc='upper left')

plt.tight_layout()
plt.savefig('grafico2_barras.png', dpi=150, bbox_inches='tight')
plt.show()
print("✔ Gráfico 2 salvo: grafico2_barras.png")

# ─────────────────────────────────────────────
# GRÁFICO 3 — BOXPLOT: Distribuição por ano
# ─────────────────────────────────────────────
# Adequado para visualizar dispersão, mediana e outliers por grupo/ano.
# Escolhido no lugar do histograma para mostrar a distribuição COM contexto temporal.

dados_por_ano = [df[df['Ano'] == ano]['USD_BRL'].values
                 for ano in sorted(df['Ano'].unique())]
anos = sorted(df['Ano'].unique())

fig, ax = plt.subplots(figsize=(13, 6))

bp = ax.boxplot(dados_por_ano,
                patch_artist=True,
                notch=False,
                labels=anos,
                medianprops=dict(color='#C62828', linewidth=2),
                whiskerprops=dict(color='#1565C0', linewidth=1.2),
                capprops=dict(color='#1565C0', linewidth=1.5),
                flierprops=dict(marker='o', markerfacecolor='#FFCC00',
                                markersize=4, linestyle='none',
                                markeredgecolor='#999999'))

# Cor de preenchimento com gradiente manual por mediana
medianas = [pd.Series(d).median() for d in dados_por_ano]
norm = plt.Normalize(min(medianas), max(medianas))
cmap = plt.cm.Blues

for patch, med in zip(bp['boxes'], medianas):
    patch.set_facecolor(cmap(norm(med)))
    patch.set_alpha(0.85)

ax.set_title('Distribuição das Cotações USD/BRL por Ano (Boxplot)')
ax.set_xlabel('Ano')
ax.set_ylabel('Cotação (R$)')
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter('R$ %.2f'))
ax.grid(True, axis='y')

plt.tight_layout()
plt.savefig('grafico3_boxplot.png', dpi=150, bbox_inches='tight')
plt.show()
print("✔ Gráfico 3 salvo: grafico3_boxplot.png")

print("\n✅ Todos os gráficos gerados com sucesso!")