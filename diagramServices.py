import plotly.graph_objects as go
from collections import defaultdict
import plotly.io as pio
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def displayYearDiagram(show_percentage, dataframes, attribute_choice):
    """
    Args:
    - show_percentage (bool): Ob der prozentuale Anteil angezeigt werden soll.
    - dataframes (dict): Ein Dictionary mit Dataframes und Attributen.
    - attribute_choice (str): Der Name des Attributs, nach dem gruppiert werden soll ('instrument' oder 'configuration').
    """

    pio.templates.default = "plotly"

    # Datenorganisation basierend auf der Auswahl des Attributs
    data_by_year = defaultdict(lambda: defaultdict(int))
    total_per_year = defaultdict(int)
    for name, (df, attrs) in dataframes.items():
        key = attrs[attribute_choice]  # Benutze attribute_choice hier, um entweder nach 'instrument' oder 'configuration' zu gruppieren
        data_by_year[attrs["year"]][key] += 1
        total_per_year[attrs["year"]] += 1

    years = sorted(data_by_year.keys())
    attributes = sorted({attr for year_data in data_by_year.values() for attr in year_data})  # 'attributes' repräsentiert nun entweder Instrumente oder Konfigurationen

    # Diagrammdaten vorbereiten
    fig = go.Figure()

    # Balkendiagramm für die absoluten Zahlen
    for attribute in attributes:
        fig.add_trace(go.Bar(
            x=list(years),
            y=[data_by_year[year][attribute] for year in years],
            name=attribute
        ))

    if show_percentage:
        # Liniendiagramm für den prozentualen Anteil, falls gewünscht
        for attribute in attributes:
            fig.add_trace(go.Scatter(
                x=list(years),
                y=[(data_by_year[year][attribute] / total_per_year[year] * 100) if total_per_year[year] else 0 for year in years],
                name=f"{attribute} % Anteil",
                mode='lines+markers',
                yaxis='y2'
            ))

    # Layout-Update für das Diagramm
    fig.update_layout(
        title=f"{attribute_choice.capitalize()} Einsatz und prozentualer Anteil pro Jahr",
        xaxis=dict(title='Jahr'),
        yaxis=dict(title=f"Anzahl der {attribute_choice.capitalize()}"),
        yaxis2=dict(
            overlaying='y',
            side='right',
            range=[0, 100],
            title_standoff=20
        ),
        barmode='stack',
        hovermode='closest',
        legend=dict(x=1.0, y=1.0),
        width=1200,
        height=600,
        margin=dict(r=200)
    )

    # Diagramm anzeigen
    fig.show()

def displayAttrCombinationDiagram(dataframes):
    attrs_list = []
    for name, (df, attrs) in dataframes.items():
        attrs_list.append(attrs)

    attrs_df = pd.DataFrame(attrs_list)
    attrs_count = attrs_df.groupby(['configuration', 'instrument']).size().reset_index(name='Counts')
    heatmap_data = attrs_count.pivot(index='configuration', columns='instrument', values='Counts')

    # Die Heatmap erstellen
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, annot=True, cmap='Oranges', fmt="d")

    # Anzeigen der Heatmap
    plt.title('Häufigkeit der Konfigurations- und Instrumentenkombinationen')
    plt.ylabel('Konfiguration')
    plt.xlabel('Instrument')
    plt.show()

def displayFrequencies(dataframes):

    attrs_list = []
    for name, (df, attrs) in dataframes.items():
        attrs_list.append(attrs)

    attrs_df = pd.DataFrame(attrs_list)

    # Berechnen der Häufigkeiten
    config_frequencies = attrs_df['configuration'].value_counts()
    instrument_frequencies = attrs_df['instrument'].value_counts()

    # Erstellen des Säulendiagramms für Konfigurationen
    plt.figure(figsize=(10, 6))
    plt.gca().set_facecolor('white')  # Hintergrundfarbe auf Weiß setzen
    config_frequencies.plot(kind='bar')
    plt.title('Häufigkeiten der Konfigurationen')
    plt.xlabel('Konfiguration')
    plt.ylabel('Häufigkeit')
    plt.xticks(rotation=45)
    plt.tight_layout()  # Verbessert die Darstellung bei längeren Beschriftungen
    plt.show()

    # Erstellen des Säulendiagramms für Instrumente
    plt.figure(figsize=(10, 6))
    instrument_frequencies.plot(kind='bar', color='orange')
    plt.title('Häufigkeiten der Instrumente')
    plt.xlabel('Instrument')
    plt.ylabel('Häufigkeit')
    plt.xticks(rotation=45)
    plt.tight_layout()  # Verbessert die Darstellung bei längeren Beschriftungen
    plt.show()