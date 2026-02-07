import geopandas as gpd
import numpy as np

# from get_cruise import GetCruise
from shapely.geometry import LineString, Polygon, mapping

from water_column_sonar_catalog.cruise import CruiseManager

"""
Getting the bounding box for an individual cruise for stac catalog. 
"""


class GeospatialManager:
    def __init__(
        self,
    ):
        self.__overwrite = True

    @staticmethod
    def get_bounding_box():
        try:
            # bucket_name = "noaa-wcsd-zarr-pds"
            # ship_name = "Henry_B._Bigelow"
            # cruise_name = "HB1906"
            # sensor_name = "EK60"
            # zarr_store = f"{cruise_name}.zarr"
            # s3_zarr_store_path = f"{bucket_name}/level_2/{ship_name}/{cruise_name}/{sensor_name}/{zarr_store}"
            # cruise = xr.open_dataset(
            #     filename_or_obj=f"s3://{s3_zarr_store_path}",
            #     engine="zarr",
            #     storage_options={"anon": True},
            #     chunks={},
            # )
            get_cruise = CruiseManager()
            cruise = get_cruise.get_cruise()

            latitude = cruise.latitude.to_numpy()
            longitude = cruise.longitude.to_numpy()  # TODO: assert non null
            if np.isnan(latitude).any() or np.isnan(longitude).any():
                raise RuntimeError("There was missing lat-lon dataset")
            geom = LineString(list(zip(longitude, latitude)))
            print(len(geom.coords))
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
                tolerance=0.01,  # preserve_topology=True # 113
            )
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
