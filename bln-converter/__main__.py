import click
from src import blnconverter

@click.group(help="Easy tool for BLN shape files to ESRI shape or GeoJSON conversion.")
def cli():
    pass


cli.add_command(blnconverter.bln2shp)
cli.add_command(blnconverter.bln2geojson)

if __name__ == '__main__':
    cli()