import pandas as pd
import geopandas as gpd
import io
from fiona.io import ZipMemoryFile
from shapely.geometry import Point

zipshp = io.BytesIO(open('Data/shapefiles23Sept.zip', 'rb').read())

with (ZipMemoryFile(zipshp)) as memfile:
    with memfile.open("2109_STIB_MIVB_Network") as src:
        crs = src.crs
        lines = gpd.GeoDataFrame.from_features(src, crs=crs)


tracks = pd.read_csv('Data/GPStracks.csv')

geometry = [Point(xy) for xy in zip(tracks["lat"], tracks["lon"])]
crs = {'init': 'epsg:2263'}  # http://www.spatialreference.org/ref/epsg/2263/    15929
geo_df = gpd.GeoDataFrame(tracks, crs=crs, geometry=geometry)
# geo_df = gpd.GeoDataFrame(df, geometry=geometry)

"""
for index, point in tracks.iterrows():
    for i, line in lines.iterrows():
    row['']
"""
# for index, lines in lines.iterrows():

line = lines.query("LIGNE == '001m' and VARIANTE == 1").iloc[0]

point = tracks.query("TrackId == 1").iloc[0]
