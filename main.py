import geopandas as gpd
import numpy as np
from sklearn.cluster import DBSCAN
from shapely.geometry import MultiPolygon
from shapely.ops import unary_union
import json

def process_bairros_porto_ferreira(shapefile_path, output_path):
    """
    Processa shapefile criando convex hulls para clusters de bairros

    Args:
        shapefile_path (str): Caminho do shapefile
        output_path (str): Caminho do GeoJSON de saída
    """

    # Carrega e filtra dados
    print("Carregando dados...")
    gdf = gpd.read_file(shapefile_path)

    print(f"Total de registros: {len(gdf)}")

    # Converte para UTM para clustering
    gdf_utm = gdf.to_crs('EPSG:3857')

    result = []

    # Processa cada localidade
    for localidade in gdf['DSC_LOCALIDADE'].unique():
        print(f"Processando: {localidade}")

        local_data = gdf_utm[gdf_utm['DSC_LOCALIDADE'] == localidade]

        if len(local_data) < 10:
            print("Bairro não possui pontos suficientes")
            continue

        # Extrai centroides para clustering
        coords = np.array([
            [geom.centroid.x, geom.centroid.y]
            for geom in local_data.geometry
        ])

        # Clustering DBSCAN
        clustering = DBSCAN(eps=500, min_samples=10).fit(coords)
        clusters = clustering.labels_

        # Filtra clusters válidos (remove noise = -1)
        valid_clusters = [c for c in np.unique(clusters) if c != -1]

        if not valid_clusters:
            print("Bairro não tem cluster válido")
            continue

        cluster_hulls = []

        # Cria convex hull para cada cluster
        for cluster_id in valid_clusters:
            cluster_mask = clusters == cluster_id
            cluster_geoms = local_data.iloc[cluster_mask]['geometry']

            # União das geometrias
            union_geom = unary_union(cluster_geoms.tolist())

            # Convex hull
            hull = union_geom.convex_hull
            cluster_hulls.append(hull)

        # Se há hulls válidos, cria MultiPolygon
        if cluster_hulls:
            if len(cluster_hulls) == 1:
                final_geom = MultiPolygon([cluster_hulls[0]])
            else:
                final_geom = MultiPolygon(cluster_hulls)

            result.append({
                'localidade': localidade,
                'geometry': final_geom
            })

    # Cria GeoDataFrame e salva
    if result:
        result_gdf = gpd.GeoDataFrame(result, crs='EPSG:3857')
        result_gdf = result_gdf.to_crs('EPSG:4326')

        print(f"Salvando {len(result_gdf)} bairros...")
        result_gdf.to_file(output_path, driver='GeoJSON')

        print("Bairros processados:")
        for _, row in result_gdf.iterrows():
            print(f"  - {row['localidade']}")

        return result_gdf
    else:
        print("Nenhum bairro válido encontrado!")
        return None

if __name__ == "__main__":
    # Configurar caminhos
    shapefile_path = "data/qg_810_endereco_Munic3540705.json.zip"  # Ajustar caminho
    output_path = "out/bairros_porto_ferreira.geojson"

    # Processar
    try:
        result = process_bairros_porto_ferreira(shapefile_path, output_path)
        print("Processamento concluído com sucesso!")

    except Exception as e:
        print(f"Erro durante o processamento: {e}")