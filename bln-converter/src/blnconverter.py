import sys
import click
import logging
import pandas as pd
import geopandas as gpd
from pathlib import Path
from shapely.geometry import Polygon

# ignores a useless PyProj FutureWarning 
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s',
                    level=logging.INFO, stream=sys.stdout)


def converter(caminho: str, ext: str, crs: int) -> None:
    parsed_path = Path(caminho)
    for item in parsed_path.glob("*.bln"):
        try:
            input_file = pd.read_csv(item, sep=",")
            longitude = input_file.iloc[:, 0].tolist()
            latitude = input_file.iloc[:, 1].tolist()
        except Exception:
            logging.error(f"'{item}' seems broken.")
            continue
        else:
            geometria = Polygon(zip(longitude, latitude))
            poligon = gpd.GeoDataFrame(index=[0], crs={'init': 'epsg:{}'.format(str(crs))},
                                        geometry=[geometria])

            output_exts = {
                "shp": {"ext": "shp",
                        "driver": "ESRI Shapefile"},
                "geojson": {"ext": "geojson",
                            "driver": "GeoJSON"}
            }

            ext_saida = output_exts[ext]["ext"]
            driver = output_exts[ext]["driver"]

            output_file_path = Path(
                item.parent, f"{item.stem}.{ext_saida}")

            poligon.to_file(filename=output_file_path,
                            driver=driver)

            logging.info(f"{output_file_path} gerado.")


@click.command("bln2shp")
@click.option('--path', '-p', help='Directory containing BLN files')
@click.option('--crs', '-crs', help='Coordinate Reference System (crs), default is 4326')
def bln2shp(path: Path, crs: int=4326):
    converter(path, ext="shp", crs=crs)
    
    
@click.command("bln2geojson")
@click.option('--path', '-p', help='Directory containing BLN files')
def bln2geojson(path: Path, crs: int=4326):
    converter(path, ext="geojson", crs=crs)
