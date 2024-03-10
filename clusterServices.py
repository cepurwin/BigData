from sklearn.cluster import DBSCAN
import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.metrics import pairwise_distances_argmin_min


def clusterWallThicknessAndCalculateMean(dataframes):
    for name, (df, attrs) in dataframes.items():
        # timestamp von timestamp zu UNIX
        df['timestamp'] = pd.to_datetime(df['timestamp'], format="%Y-%m-%dT%H:%M:%S").astype('int64') // 10 ** 9
        print(f"Wall_thickness Clusterverarbeitung von {name}...")
        # Annahme: 'timestamp' und 'wall_thickness' sind die benötigten Spalten
        filteredDf = pd.DataFrame({
            'timestamp_unix': df['timestamp'],
            'wall_thickness': df['wall_thickness']
        })

        # Daten vorbereiten
        X = filteredDf[['timestamp_unix', 'wall_thickness']].values

        # Standardisieren der Daten
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # DBSCAN Anwendung
        dbscan = DBSCAN(eps=0.4, min_samples=10)
        labels = dbscan.fit_predict(X_scaled)

        # Wiederherstellen der ursprünglichen Daten, falls benötigt
        X_restored = scaler.inverse_transform(X_scaled)

        # Ergebnisse speichern
        filteredDf['cluster'] = labels
        filteredDf['wall_thickness_scaled'] = X_restored[:, 1]

        # Durchschnittliche Wandstärke für jedes Cluster berechnen
        cluster_means = {}
        for cluster in np.unique(labels):
            if cluster != -1: # Nicht Ausreißer berücksichtigen
                cluster_mean = filteredDf.loc[filteredDf['cluster'] == cluster, 'wall_thickness'].mean()
                cluster_means[cluster] = cluster_mean

        # Wandstärke aktualisieren
        for cluster in filteredDf['cluster'].unique():
            if cluster != -1:  # Nicht Ausreißer berücksichtigen
                filteredDf.loc[filteredDf['cluster'] == cluster, 'wall_thickness'] = cluster_means[cluster]

        # Ausreißer behandeln
        if -1 in labels:
            outliers_indices = filteredDf[filteredDf['cluster'] == -1].index
            core_samples_mask = labels != -1
            core_samples = X_scaled[core_samples_mask]
            outlier_samples = X_scaled[~core_samples_mask]
            closest_cores_indices, _ = pairwise_distances_argmin_min(outlier_samples, core_samples)
            closest_clusters = labels[core_samples_mask][closest_cores_indices]

            for outlier_idx, closest_cluster in zip(outliers_indices, closest_clusters):
                filteredDf.at[outlier_idx, 'wall_thickness'] = cluster_means[closest_cluster]

        # timestamp zurück zu timestamp konvertieren
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s').dt.strftime("%Y-%m-%dT%H:%M:%S")

        # Ergebnis aktualisieren im ursprünglichen DataFrame
        df.update(filteredDf[['wall_thickness']])
        print("done")

        # Optional: Visualisierung hier kommentieren oder aktivieren
        # plt.figure(figsize=(10, 6))
        # plt.scatter(filteredDf['timestamp_unix'], filteredDf['wall_thickness'], c=filteredDf['cluster'], cmap='tab10', s=20)
        # plt.title(f'DBSCAN Clustering für {name}')
        # plt.xlabel('Unix-Timestamp')
        # plt.ylabel('Wall Thickness (aktualisiert)')
        # plt.show()
    print("-----Wall-thickness Cluster Verarbeitung abgeschlossen-----")
    return dataframes
