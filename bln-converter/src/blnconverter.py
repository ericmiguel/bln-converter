import sys
import click
import logging
import pandas as pd
import geopandas as gpd
from pathlib import Path
from shapely.geometry import Polygon

# ignore a PyProj FutureWarning 
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

logger = logging.getLogger()
logging.basicConfig(format='%(asctime)s | %(levelname)s : %(message)s',
                    level=logging.INFO, stream=sys.stdout)


def converter(bln_dir: str, output_ext: str, crs: int) -> None:
    parsed_path = Path(bln_dir)
    for input_file_path in parsed_path.glob("*.bln"):
        try:
            input_file = pd.read_csv(input_file_path, sep=",")
            longitude = input_file.iloc[:, 0].tolist()
            latitude = input_file.iloc[:, 1].tolist()
        except Exception:
            logging.error(f"'{input_file_path}' seems broken.")
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

            ext_saida = output_exts[output_ext]["ext"]
            driver = output_exts[output_ext]["driver"]

            output_file_name = f"{input_file_path.stem}.{ext_saida}"
            output_file_path = Path(input_file_path.parent, output_file_name)

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
