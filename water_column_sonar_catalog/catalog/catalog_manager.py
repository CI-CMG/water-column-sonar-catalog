from tempfile import TemporaryDirectory

import pandas as pd
import pystac
import xarray as xr

from water_column_sonar_catalog.cruise import CruiseManager
from water_column_sonar_catalog.geospatial import GeospatialManager

"""
Creating metadata catalog:
https://pystac.readthedocs.io/en/latest/tutorials/how-to-create-stac-catalogs.html
https://stacspec.org/en/tutorials/4-create-stac-collection/ 
"""

tmp_dir = TemporaryDirectory()


# img_path1 = os.path.join(tmp_dir.name, 'image1.tif')
# url1 = 'https://www.ncei.noaa.gov/sites/default/files/2022-03/AllBeamCurtains_griddedMultibeam-102-file-good-bathy442x185.jpg'
# urllib.request.urlretrieve(url1, img_path1)


# good tutorial https://stacspec.org/en/tutorials/4-create-stac-collection/
class CatalogManager:
    def __init__(
        self,
        bucket_name: str = "noaa-wcsd-zarr-pds",
        level: str = "level_2a",
        ship_name: str = "Henry_B._Bigelow",
        cruise_name: str = "HB1906",
        instrument_name: str = "EK60",
    ):
        self.bucket_name = bucket_name
        self.level = level
        self.ship_name = ship_name
        self.cruise_name = cruise_name
        self.instrument_name = instrument_name
        self.catalog_type = pystac.CatalogType.RELATIVE_PUBLISHED
        self.provider_ncei = pystac.Provider(
            name="NOAA National Centers for Environmental Information",
            description="In collaboration with NOAA's National Marine Fisheries Service (NMFS) and the University of Colorado Boulder, NOAA’s National Centers for Environmental Information (NCEI) established a national archive for water column sonar data. This project entails ensuring the long-term stewardship of well-documented water column sonar data, and enabling discovery and access to researchers and the public around the world.",
            roles=[pystac.ProviderRole.HOST],
            url="https://www.ncei.noaa.gov/",
        )
        self.provider_cires = pystac.Provider(
            name="Cooperative Institute for Research In Environmental Sciences",
            description="At CIRES, the Cooperative Institute for Research In Environmental Sciences, hundreds of scientists work to understand the dynamic Earth system, including people’s relationship with the planet.",
            roles=[pystac.ProviderRole.PROCESSOR],
            url="https://cires.colorado.edu/",
        )
        self.provider_henry_bigelow = pystac.Provider(
            name="Henry_B._Bigelow",
            description="Henry B. Bigelow conducts both acoustic and trawl surveys.",
            roles=[pystac.ProviderRole.PRODUCER],
            url="https://www.omao.noaa.gov/marine-operations/ships/henry-b-bigelow",
        )

    def create_level_2_catalog(self):
        """Cruise Level 2 Zarr store Catalog"""
        try:
            ### Read in cruise zarr store ###
            cruise_manager = CruiseManager(
                bucket_name=self.bucket_name,
                level=self.level,
                ship_name=self.ship_name,
                cruise_name=self.cruise_name,
                instrument_name=self.instrument_name,
            )
            cruise = cruise_manager.get_cruise()

            ################################ --- CATALOG --- ################################
            level_2_catalog = pystac.Catalog(
                id=f"water-column-sonar-{self.level}",
                description="Level 2 Water Column Sonar Data from the NOAA National Centers for Environmental Information",
                title=f"Water Column Sonar {self.level} Zarr Stores",
                href="https://www.ncei.noaa.gov/products/water-column-sonar-data",
                catalog_type=self.catalog_type,
            )

            ### bounding box ###
            geospatial_manager = GeospatialManager(
                bucket_name=self.bucket_name,
                level=self.level,
                ship_name=self.ship_name,
                cruise_name=self.cruise_name,
                instrument_name=self.instrument_name,
            )
            bbox, footprint, geojson = geospatial_manager.get_bounding_box()

            ### date range ###
            start_datetime = pd.Timestamp(cruise.time.values[0])
            end_datetime = pd.Timestamp(cruise.time.values[-1])
            temporal_extent = pystac.TemporalExtent(
                intervals=[[start_datetime, end_datetime]]
            )
            ### extent ###
            spatial_extent = pystac.SpatialExtent(bboxes=[bbox])
            extent = pystac.Extent(spatial=spatial_extent, temporal=temporal_extent)

            ################################ --- COLLECTION --- ################################
            level_2_collection = pystac.Collection(
                id=self.cruise_name,
                description=f"Level 2 water column sonar data from the {self.ship_name} {self.cruise_name} cruise.",
                extent=extent,
                title=f"{self.ship_name} {self.cruise_name} Zarr Stores",
                href=f"https://{self.bucket_name}.s3.amazonaws.com/index.html#{self.level}/",
                catalog_type=self.catalog_type,
                keywords=["oceanography"],
                providers=[self.provider_henry_bigelow, self.provider_ncei],
            )

            ################################ --- ASSET --- ################################
            level_2_asset = pystac.Asset(
                href=f"s3://{self.bucket_name}/{self.level}/{self.ship_name}/{self.cruise_name}/{self.instrument_name}/{self.cruise_name}.zarr",
                title=f"{self.level} {self.ship_name} {self.cruise_name} {self.instrument_name} Zarr Store",
                description="Consolidated cruise-level Zarr store",
                media_type=pystac.MediaType.ZARR,
                roles=["latest-version"],
            )

            ################################ --- ITEM --- ################################
            level_2_item = pystac.Item(
                id=f"{self.instrument_name}",
                geometry=geojson,
                bbox=bbox,
                datetime=None,
                properties=dict(
                    ship_name=self.ship_name,
                    cruise_name=self.cruise_name,
                    instrument_name=self.instrument_name,
                    level=self.level,
                    calibration_status=True,
                ),
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                href=f"https://{self.bucket_name}.s3.amazonaws.com/{self.level}/{self.ship_name}/{self.cruise_name}/{self.instrument_name}/{self.cruise_name}.zarr/",
                collection=level_2_collection,
                assets=dict(zarr=level_2_asset),
            )
            #
            ################################ --- ATTACH --- ################################
            level_2_collection.add_item(level_2_item)
            level_2_catalog.add_child(level_2_collection)
            #
            # level_2_catalog.normalize_hrefs(os.path.join(tmp_dir.name, "stac"))
            level_2_catalog.normalize_hrefs("../stac_catalog")
            level_2_catalog.save(catalog_type=pystac.CatalogType.RELATIVE_PUBLISHED)
            return level_2_catalog
        except Exception as error:
            raise Exception(f"Problem creating catalog: {error}")


### TODO: follow zarr guide here: https://element84.com/software-engineering/zarr-stac/
if __name__ == "__main__":
    catalog_manager = CatalogManager(
        bucket_name="noaa-wcsd-zarr-pds",
        level="level_2a",
        ship_name="Henry_B._Bigelow",
        cruise_name="HB1906",
        instrument_name="EK60",
    )
    new_collection, new_catalog = catalog_manager.create_level_2_catalog()
    new_catalog.describe()
    #
    asset = list(new_catalog.get_items(recursive=True))[0].assets["zarr"]
    kwargs = {"consolidated": False}
    ds = xr.open_dataset(filename_or_obj=asset.href, engine="zarr", **kwargs)
    print(ds.Sv.shape)
    #
    print(  # This gets the latest zarr store for an item
        list(new_catalog.get_items(recursive=True))[0].get_assets(role="latest-version")
    )
    #
    # catalog = pystac_client.Client.open(
    #     "https://earth-search.aws.element84.com/v1",
    # )
    # search = catalog.search(
    #     intersects=dict(type="Point", coordinates=[-105.78, 35.79]),
    #     collections=["sentinel-2-l2a"],
    #     datetime="2022-04-01/2022-05-01",
    # )
    # xr.open_dataset(search, engine="stac")
    #
    print("done")

"""
* <Catalog id=water-column-sonar-level-2>
    * <Collection id=HB1906>
      * <Item id=HB1906.zarr>



https://noaa-wcsd-pds.s3.amazonaws.com/index.html#data/raw/Henry_B._Bigelow/HB1906/
### raw data ###      
* <Catalog id=water-column-sonar-level-0>
    * <Collection id=HB1906>
      * <Item id=D20190903-T171901.raw> EK60
      * <Item id=D20190903-T171901.bot>
      * <Item id=D20190903-T171901.idx geometry= bbox= datetime= properties=SHIP start_datetime= end_datetime= href= collection= assets= >
      ...
      * <Item id=HB-D20190903-T171908.raw> ME70
      ...
      <Asset id=HBBigelow_018kHz_20August2019.cal>
      <Asset id=D20190903-T171901-D20190904-T093044.xml>
      ...
    * <Collection id=HB0707>
      * <Item id=D20070711-T182032.raw>
      ...
    ...

### file level zarr stores ###
* <Catalog id=water-column-sonar-level-1>
    * <Collection id=HB1906>
      * <Item id=D20190903-T171901.zarr geometry= bbox= datetime=X properties= start_datetime= end_datetime= stac_extensions=X href= collection= extra_fields= assets= >
      * <Item id=D20190903-T171901.nc>
      * <Item id=D20190903-T175930.zarr>
      * <Item id=D20190903-T175930.nc>
      * <Item id=D20190903-T183959.zarr>
      * <Item id=D20190903-T183959.nc>

### cruise level zarr store ###
* <Catalog id=water-column-sonar-level-2>
    * <Collection id=HB1906>
      * <Item id=HB1906.zarr ek60> <-- this should be 'HB1906_EK60.zarr'
      * <Item id=HB1906_int8.zarr>
      * <Item id=HB1906.zarr ek80> 


Catalog(id: 'str', description: 'str', title: 'str | None' = None, stac_extensions: 'list[str] | None' = None, extra_fields: 'dict[str, Any] | None' = None, href: 'str | None' = None, catalog_type: 'CatalogType' = 'ABSOLUTE_PUBLISHED', strategy: 'HrefLayoutStrategy | None' = None)
Collection(id: 'str', description: 'str', extent: 'Extent', title: 'str | None' = None, stac_extensions: 'list[str] | None' = None, href: 'str | None' = None, extra_fields: 'dict[str, Any] | None' = None, catalog_type: 'CatalogType | None' = None, license: 'str' = 'other', keywords: 'list[str] | None' = None, providers: 'list[Provider] | None' = None, summaries: 'Summaries | None' = None, assets: 'dict[str, Asset] | None' = None, strategy: 'HrefLayoutStrategy | None' = None)
Item(id: 'str', geometry: 'dict[str, Any] | None', bbox: 'list[float] | None', datetime: 'Datetime | None', properties: 'dict[str, Any]', start_datetime: 'Datetime | None' = None, end_datetime: 'Datetime | None' = None, stac_extensions: 'list[str] | None' = None, href: 'str | None' = None, collection: 'str | Collection | None' = None, extra_fields: 'dict[str, Any] | None' = None, assets: 'dict[str, Asset] | None' = None)
Asset(href: 'str', title: 'str | None' = None, description: 'str | None' = None, media_type: 'str | None' = None, roles: 'list[str] | None' = None, extra_fields: 'dict[str, Any] | None' = None) -> 'None'

"""
