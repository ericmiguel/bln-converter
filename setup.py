import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bln-converter",
    version="1.0.0",
    author="Eric Miguel Ribeiro",
    author_email="ericmiguel@id.uff.br",
    description="Easy BLN file conversion to ESRI shape or GeoJSON",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ericmiguel/bln-converter",
    install_requires=['certifi==2020.12.5',
                      'click==7.1.2',
                      'click-plugins==1.1.1',
                      'cligj==0.7.1',
                      'Fiona==1.8.18',
                      'geopandas==0.8.1',
                      'munch==2.5.0',
                      'numpy==1.19.5',
                      'pandas==1.2.0',
                      'pycodestyle==2.6.0',
                      'pyproj==3.0.0.post1',
                      'python-dateutil==2.8.1',
                      'pytz==2020.5',
                      'Shapely==1.7.1',
                      'six==1.15.0',
                      'toml==0.10.2'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)