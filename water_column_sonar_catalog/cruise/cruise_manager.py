import xarray as xr


class CruiseManager:
    #######################################################
    def __init__(
        self,
    ):
        self.__overwrite = True

    @staticmethod
    def get_cruise():
        try:
            bucket_name = "noaa-wcsd-zarr-pds"
            level = "level_2a"
            ship_name = "Henry_B._Bigelow"
            cruise_name = "HB1906"
            sensor_name = "EK60"
            zarr_store = f"{cruise_name}.zarr"
            s3_zarr_store_path = f"{bucket_name}/{level}/{ship_name}/{cruise_name}/{sensor_name}/{zarr_store}"
            kwargs = {"consolidated": False}
            return xr.open_dataset(
                filename_or_obj=f"s3://{s3_zarr_store_path}",
                engine="zarr",
                storage_options={"anon": True},
                **kwargs,
            )
        except Exception as error:
            raise Exception(f"Problem opening cruise: {error}")


# if __name__ == "__main__":
#     cruise_manager = CruiseManager()
#     cruise = cruise_manager.get_cruise()
#     print(cruise)

#######################################################


###########################################################
