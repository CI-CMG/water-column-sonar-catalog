import xarray as xr


class CruiseManager:
    #######################################################
    def __init__(
        self,
        bucket_name: str,
        level: str,
        ship_name: str,
        cruise_name: str,
        instrument_name: str,
    ):
        self.bucket_name = bucket_name
        self.level = level
        self.ship_name = ship_name
        self.cruise_name = cruise_name
        self.instrument_name = instrument_name

    def get_cruise(self):
        try:
            zarr_store = f"{self.cruise_name}.zarr"
            s3_zarr_store_path = f"{self.bucket_name}/{self.level}/{self.ship_name}/{self.cruise_name}/{self.instrument_name}/{zarr_store}"

            kwargs = {"consolidated": False}
            return xr.open_dataset(
                filename_or_obj=f"s3://{s3_zarr_store_path}",
                engine="zarr",
                storage_options={"anon": True},
                cache=True,
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
