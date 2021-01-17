import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from pathlib import Path
import logging
import sys
import os
from collections import defaultdict

logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s',
                    level=logging.INFO, stream=sys.stdout)


"""
------------------------------------------------------------------------------------------------------------------
LISTAGEM DOS ARQUIVOS
------------------------------------------------------------------------------------------------------------------
"""


def filtrarArquivos(diretorio: Path, ext: str) -> list:
    """
    Filtragem recursiva de arquivos em um diretório.

    Filtra arquivos por extensão em um diretório. As
    subpastas são recursivamente verificadas.

    Parâmetros
    ------------
    diretorio:
        diretório a ser verificado
    ext:
        extensão dos arquivos desejados

    Retorna
    ------------
    lista contendo objetos Path direcionando aos arquivos
    filtrados.
    """

    arquivos = list()

    for path in sorted(diretorio.rglob('*')):
        if path.is_file() and path.suffix == ext:
            arquivos.append(path)

    return arquivos



if __name__ == '__main__':
    # define a pasta a ser vasculhada
    pasta_contornos = Path("Contornos")
    # executa a filtragem por arquivos .bln
    arquivos_bln = filtrarArquivos(diretorio=pasta_contornos, ext=".bln")

    # os contornos serão estruturados em um dicionário identificado
    # por modelo (ETA40 ou GEFS) e por bacia.
    # Cada chave de bacia de cada modelo corresponde a um polígono.
    contornos_por_modelo = defaultdict(lambda: defaultdict(Polygon))

    # itera pela listagem de arquivos bln
    for item in arquivos_bln:

        # define o diretório parental
        # i.e. pasta dos contornos de cada modelo
        parf = item.parents[1]

        # tratamento de erro para arquivos potencialmente fora de padrão
        try:
            # o arquivo bln possui codificação ASCII e pode ser lido como texto
            # a primeira coluna corresponde à longitude
            # a segunda coluna corresponde à latitude
            contorno = pd.read_csv(item, sep=",")
            longitude = contorno.iloc[:, 0].tolist()
            latitude = contorno.iloc[:, 1].tolist()
        except Exception:
            logging.error(f"({parf}) {item.name} não parece estar íntegro.")
            continue
        else:
            # cria o polígono a partir das coordenadas obtidas do bln
            geometria = Polygon(zip(longitude, latitude))
            poligono = gpd.GeoDataFrame(index=[0], crs={'init': 'epsg:4326'},
                                        geometry=[geometria])
            # armazena o polígono gerado à estrutura de dados
            contornos_por_modelo[parf][item.name] = poligono
            logging.info(f"({parf}) {item.name} processado.")

    """
    ------------------------------------------------------------------------------------------------------------------
    MAPAS
    ------------------------------------------------------------------------------------------------------------------
    """

    # projeção cartográfica
    proj = ccrs.PlateCarree()

    fig, ax = plt.subplots(ncols=2,
                           figsize=(12, 8),
                           subplot_kw=dict(projection=proj))

    for axis in ax:
        # contorno da linha de costa
        axis.coastlines("50m")

        # contorno dos países
        axis.add_feature(cfeature.BORDERS, linestyle='-', alpha=.5)

        # enquadramento do Brasil
        axis.set_extent([-75, -32.5, 7, -32.5])

    # estilização de plotagem dos contornos no mapa
    estilo_contornos = dict(crs=proj, facecolor='b', edgecolor='red',
                            linewidth=0.5, alpha=0.5)

    for axis, (modelo, poligonos) in zip(ax, contornos_por_modelo.items()):
        axis.set_title(modelo)
        for bacia, poligono in poligonos.items():
            try:
                axis.add_geometries(poligono['geometry'], **estilo_contornos)
            except Exception:
                logging.error("Erro ao processar o contorno {bacia}.")

    fig.savefig("contornos.png", dpi=300, bbox_inches="tight")

    """
    ------------------------------------------------------------------------------------------------------------------
    CONVERSÃO DE ARQUIVOS
    bln para shapefile (ESRI) ou GeoJSON
    ------------------------------------------------------------------------------------------------------------------
    """

    for modelo, poligonos in contornos_por_modelo.items():
        nome_modelo = modelo.name.split(os.sep)[-1]
        pasta_modelo_convetidos = Path("contornos_convertidos", nome_modelo)
        pasta_modelo_convetidos.mkdir(exist_ok=True, parents=True)
        logging.info(f"Convertendo arquivos .bln de {modelo}")
        for bacia, poligono in poligonos.items():
            try:
                # nome do arquivo de saída (convertido)
                nome_arquivo = bacia.split(os.sep)[-1].split(".")[0]

                # opcionalmente, é possível salvar como GeoJSON.
                # Útil caso desejem exibir os
                # contornos em sites com mapas, como o Windy
                ext_saida = "shp"  # geojson
                conversor = "ESRI Shapefile"  # GeoJSON

                destino_arquivo_saida = Path(pasta_modelo_convetidos,
                                             f"{nome_arquivo}.{ext_saida}")

                poligono.to_file(filename=destino_arquivo_saida,
                                 driver=conversor)

            except Exception:
                logging.error(f"Erro ao converter {bacia}.")
            else:
                logging.info(f"{bacia} convertido com sucesso.")
