import geopandas as gpd
import numpy as np
import shapely  # import set_precision
from cruise.cruise_manager import CruiseManager
from shapely.geometry import LineString

"""
Getting the bounding box for an individual cruise for stac catalog. 
"""


class GeospatialManager:
    def __init__(
        self,
        bucket_name,
        level,
        ship_name,
        cruise_name,
        instrument_name,
    ):
        self.simplification_tolerance = 0.01
        self.bucket_name = bucket_name
        self.level = level
        self.ship_name = ship_name
        self.cruise_name = cruise_name
        self.instrument_name = instrument_name

    def get_bounding_box(self):
        try:
            get_cruise = CruiseManager(
                bucket_name=self.bucket_name,
                level=self.level,
                ship_name=self.ship_name,
                cruise_name=self.cruise_name,
                instrument_name=self.instrument_name,
            )
            cruise = get_cruise.get_cruise()

            latitude = cruise.latitude.to_numpy()
            longitude = cruise.longitude.to_numpy()
            if np.isnan(latitude).any() or np.isnan(longitude).any():
                raise RuntimeError("There was missing lat-lon dataset")
            geom = LineString(list(zip(longitude, latitude)))
            gdf = gpd.GeoDataFrame({"geometry": [geom]}, crs="EPSG:4326")
            bounds = gdf.bounds
            bounding_box = [
                bounds.minx.values[0],
                bounds.miny.values[0],
                bounds.maxx.values[0],
                bounds.maxy.values[0],
            ]
            ### simplify geometry
            geom_simplified = LineString(list(zip(longitude, latitude))).simplify(
                tolerance=self.simplification_tolerance,
                preserve_topology=False,  # 113
            )  # 1=36k,
            geom_simplified2 = shapely.set_precision(geom_simplified, 1e-5)
            gdf_simplified3 = gpd.GeoDataFrame(
                {"geometry": [geom_simplified2]}, crs="EPSG:4326"
            )
            ###
            # TODO: add details to geo dict
            #  'type': 'LineString'}, 'id': '0', 'properties': {}, 'type': 'Feature'}], 'type': 'FeatureCollection'}
            return bounding_box, gdf_simplified3.to_geo_dict()
            # return bounding_box, shapely.from_geojson(
            #     gdf_simplified3.get_geometry(0).to_json(drop_id=True, to_wgs84=True)
            # )
            # ).to_geo_dict()

        except Exception as error:
            raise Exception(f"Problem: {error}")


# if __name__ == "__main__":
#     get_cruise_bounding_box = GetCruiseBoundingBox()
#     bbox, fp, _ = get_cruise_bounding_box.get_bounding_box()
#     print(bbox)
