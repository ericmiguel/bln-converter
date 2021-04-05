# BLN-Converter

## What is it?

A simple CLI utiliy tool for converting BLN files (a extension used on GIS software like Surfer) to [ESRI shape](https://pt.wikipedia.org/wiki/Shapefile) or [GeoJSON files](https://geojson.org).


## Where to get it

The source code is currently hosted on GitHub at: https://github.com/ericmiguel/bln-converter

Binary installers for the latest released version are available at the [Python Package Index (PyPI)](https://pypi.org/project/bln-converter).

```
pip install bln-converter
```

## How to use it

BLN converter offers a very simple CLI. Although under development, it is already functional. 

Convert BLN to ESRI shape: 
```
python -m bln-converter bln2shp -p {bln_folder}
```

or use bln2geojson command to get a GeoJSON output. 
```
python -m bln-converter bln2geojson -p {bln_folder}
```

BLN converter will find and process all BLN files in a given folder. The resultant files will be outputed to the origin folder. 


Other commands or instructions can be found using the help command 
```
python -m bln-converter --help
```


## Dependencies

- [Geopandas](https://geopandas.org)
- [Click](https://click.palletsprojects.com/en/7.x/)


## License

[MIT License](https://github.com/ericmiguel/bln-converter/blob/main/LICENSE)


## Contributing

Although BLN Converter is a simple and dirty utility script, all contributions are welcome.

