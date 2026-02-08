import geopandas as gpd
import numpy as np
from shapely.geometry import LineString, Polygon, mapping

from water_column_sonar_catalog.cruise import CruiseManager

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
            # print(len(geom.coords))
            gdf = gpd.GeoDataFrame({"geometry": [geom]}, crs="EPSG:4326")
            bounds = gdf.bounds
            footprint = Polygon(
                [
                    [
                        bounds.minx.values[0],
                        bounds.miny.values[0],
                    ],  # TODO: verify this...
                    [bounds.minx.values[0], bounds.maxy.values[0]],
                    [bounds.maxx.values[0], bounds.maxy.values[0]],
                    [bounds.maxx.values[0], bounds.miny.values[0]],
                ]
            )
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
            gdf_simplified = gpd.GeoDataFrame(
                {"geometry": [geom_simplified]}, crs="EPSG:4326"
            )
            ###
            return bounding_box, mapping(footprint), gdf_simplified.to_json()
            # ['minx', 'miny', 'maxx', 'maxy'] [0 -75.886169  34.613171 -65.729599  44.36824]

        except Exception as error:
            raise Exception(f"Problem: {error}")


# if __name__ == "__main__":
#     get_cruise_bounding_box = GetCruiseBoundingBox()
#     bbox, fp, _ = get_cruise_bounding_box.get_bounding_box()
#     print(bbox)
