import sys
import click
import logging
import pandas as pd
import geopandas as gpd
from pathlib import Path
from shapely.geometry import Polygon

# ignora um FutureWarning da dependência PyProj
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s',
                    level=logging.INFO, stream=sys.stdout)


def converter(caminho: str, ext: str):
    caminho = Path(caminho)
    for item in caminho.glob("*.bln"):
        try:
            contorno = pd.read_csv(item, sep=",")
            longitude = contorno.iloc[:, 0].tolist()
            latitude = contorno.iloc[:, 1].tolist()
        except Exception:
            logging.error(f"'{item}' não parece estar íntegro.")
            continue
        else:
            geometria = Polygon(zip(longitude, latitude))
            poligono = gpd.GeoDataFrame(index=[0], crs={'init': 'epsg:4326'},
                                        geometry=[geometria])

            formatos = {
                "shp": {"ext": "shp",
                        "conversor": "ESRI Shapefile"},
                "geojson": {"ext": "geojson",
                            "conversor": "GeoJSON"}
            }

            ext_saida = formatos[ext]["ext"]
            conversor = formatos[ext]["conversor"]

            destino_arquivo_saida = Path(
                item.parent, f"{item.stem}.{ext_saida}")

            poligono.to_file(filename=destino_arquivo_saida,
                             driver=conversor)

            logging.info(f"{destino_arquivo_saida} gerado.")


@click.command("bln2shp")
@click.option('--path', '-p', help='Directory containing BLN files')
def bln2shp(path: Path):
    converter(path, ext="shp")
    
    
@click.command("bln2geojson")
@click.option('--path', '-p', help='Directory containing BLN files')
def bln2geojson(path: Path):
    converter(path, ext="geojson")
