import sys
import click
import logging
import pandas as pd
import geopandas as gpd
from pathlib import Path
from io import StringIO
from shapely.geometry import Polygon

# ignore a PyProj FutureWarning
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)


logger = logging.getLogger()
logging.basicConfig(
    format="%(asctime)s | %(levelname)s : %(message)s",
    level=logging.INFO,
    stream=sys.stdout,
)


def converter(bln_dir: str, output_ext: str, crs: int) -> None:
    parsed_path = Path(bln_dir)

    output_exts = {
        "shp": {"ext": "shp", "driver": "ESRI Shapefile"},
        "geojson": {"ext": "geojson", "driver": "GeoJSON"},
    }

    for input_file_path in parsed_path.glob("*.bln"):
        try:
            input_file = ""
            with open(input_file_path, 'r') as inFile: # Read file, adjust formatting in memory. Only keep geometry.
                for line in inFile.readlines():
                    line = line.replace("\t", ",").split(",")
                    input_file += "{lon},{lat}\n".format(lon=line[0], lat=line[1])
            input_file = StringIO(input_file) # convert to StringIO object for pd.read_csv()
            input_file = pd.read_csv(input_file, sep=",")
            # TODO: fix 'no overloads for "__getitem__"'
            longitude = input_file.iloc[:, 0].tolist()
            latitude = input_file.iloc[:, 1].tolist()
        except Exception:
            logging.error(f"'{input_file_path}' seems broken.")
            continue
        else:
            geometria = Polygon(zip(longitude, latitude))
            poligon = gpd.GeoDataFrame(
                index=[0],
                crs={"init": f"epsg:{crs}"},
                geometry=[geometria],
            )

            ext_saida = output_exts[output_ext]["ext"]
            driver = output_exts[output_ext]["driver"]

            output_file_name = f"{input_file_path.stem}.{ext_saida}"
            output_file_path = Path(input_file_path.parent, output_file_name)

            poligon.to_file(filename=output_file_path, driver=driver)

            logging.info(f"{output_file_path} gerado.")


@click.command("bln2shp")
@click.option("--path", "-p", help="Directory containing one or more BLN files.")
@click.option("--crs", "-crs", default=4326, help="Coordinate Reference System (crs).")
def bln2shp(path: str, crs: int):
    converter(path, output_ext="shp", crs=crs)


@click.command("bln2geojson")
@click.option("--path", "-p", help="Directory containing one or more BLN files.")
@click.option("--crs", "-crs", default=4326, help="Coordinate Reference System (crs).")
def bln2geojson(path: str, crs: int):
    converter(path, output_ext="geojson", crs=crs)
