import pandas as pd
import geopandas as gpd
import io
from fiona.io import ZipMemoryFile
from shapely.geometry import Point
#from pygeos import Geometry

zipshp = io.BytesIO(open('../Data/shapefiles23Sept.zip', 'rb').read())

with (ZipMemoryFile(zipshp)) as memfile:
    with memfile.open("2109_STIB_MIVB_Network") as src:
        crs = src.crs
        # lines = gpd.GeoDataFrame.from_features(src, crs=crs)
        lines = gpd.GeoDataFrame.from_features(src)
        lines.set_crs(epsg=31370)


tracks = pd.read_csv('../Data/Track 7.csv')

geometry = [Point(xy) for xy in zip(tracks["lon"], tracks["lat"])]
# geometry = [Geometry("POINT (" + str(xy[0]) + " " + str(xy[1]) + ")") for xy in zip(tracks["lon"], tracks["lat"])]

#crs = {'init': 'epsg:2263'}  # http://www.spatialreference.org/ref/epsg/2263/    15929
#geo_df = gpd.GeoDataFrame(tracks, crs=crs, geometry=geometry)
geo_df = gpd.GeoDataFrame(tracks, geometry=geometry).set_crs(crs=None, epsg=4326).to_crs(epsg=31370)

res = []
for point_index, point in geo_df.iterrows():
    for line_index, line in lines.iterrows():
        distance = point["geometry"].distance(line["geometry"])
        if distance <= 10.0:
            res.append([point_index, point["TrackId"], point["time"],point["lon"], point["lat"], line["LIGNE"], line["VARIANTE"], distance])

with open("../ahaha2.csv", "w") as output_file:
    output_file.write("Point_Index,TrackId,Time,Lon,Lat,Ligne,Variante,Distance\n")
    for d in res:
        output_file.write(",".join(str(elem) for elem in d) + "\n")

# for index, lines in lines.iterrows():

#line = lines.query("LIGNE == '001m' and VARIANTE == 1").iloc[0]

#point = tracks.query("TrackId == 1").iloc[0]
#geo_df.to_crs(crs=None, epsg=31370, inplace=True)
#res = gpd.sjoin_nearest(geo_df, lines, "left", 12.0, distance_col = "distance")
#res.drop('geometry',axis=1).to_csv('../plswo.csv')
