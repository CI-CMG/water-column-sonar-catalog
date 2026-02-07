import os
from tempfile import TemporaryDirectory

import pandas as pd
import pystac
import xarray as xr

from water_column_sonar_catalog.cruise import CruiseManager
from water_column_sonar_catalog.geospatial import GeospatialManager

# from shapely.geometry import MultiPolygon, shape

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
        ship_name: str = "Henry_B._Bigelow",
        cruise_name: str = "HB1906",
        instrument_name: str = "EK60",
    ):
        self.ship_name = ship_name
        self.cruise_name = cruise_name
        self.instrument_name = instrument_name
        self.provider_national_centers_for_environmental_information = pystac.Provider(
            name="NOAA National Centers for Environmental Information",
            description="In collaboration with NOAA's National Marine Fisheries Service (NMFS) and the University of Colorado Boulder, NOAA’s National Centers for Environmental Information (NCEI) established a national archive for water column sonar data. This project entails ensuring the long-term stewardship of well-documented water column sonar data, and enabling discovery and access to researchers and the public around the world.",
            roles=[pystac.ProviderRole.HOST, pystac.ProviderRole.LICENSOR],
            url="https://www.ncei.noaa.gov/",
            # extra_fields: dict[str, Any] | None = None,
        )
        self.provider_marine_geology_and_geophysics = pystac.Provider(
            name="NCEI Marine Geology and Geophysics",
            description="The NOAA National Centers for Environmental Information (NCEI) are part of the US Department of Commerce, National Oceanic and Atmospheric Administration (NOAA), National Environmental Satellite, Data, and Information Service (NESDIS).",
            roles=[pystac.ProviderRole.PRODUCER],
            url="https://www.ngdc.noaa.gov/mgg/aboutmgg/aboutmgg.html",
            # extra_fields: dict[str, Any] | None = None,
        )
        self.provider_cooperative_institute_for_research_in_environmental_sciences = pystac.Provider(
            name="CU Cooperative Institute for Research In Environmental Sciences",
            description="At CIRES, the Cooperative Institute for Research In Environmental Sciences, hundreds of scientists work to understand the dynamic Earth system, including people’s relationship with the planet",
            roles=[pystac.ProviderRole.PROCESSOR],
            url="https://cires.colorado.edu/",
            # extra_fields: dict[str, Any] | None = None,
        )

    def create_level_2_catalog(self):
        """Cruise Level Zarr store Catalog"""
        try:
            ### Read in HB1906 cruise ###
            cruise_manager = CruiseManager()
            cruise = cruise_manager.get_cruise()

            # --- CATALOG --- #
            level_2_catalog = pystac.Catalog(
                id="water-column-sonar-level-2",
                description="Level 2 water column sonar data from the NOAA National Centers for Environmental Information",
                title="Water Column Sonar Level 2 Zarr Stores",
                # stac_extensions: 'list[str] | None' = None
                extra_fields=dict(
                    url="https://www.ncei.noaa.gov/products/water-column-sonar-data",
                ),
                # href="https://noaa-wcsd-zarr-pds.s3.amazonaws.com/index.html#level_2a/",
                # catalog_type=pystac.CatalogType.ABSOLUTE_PUBLISHED,
                # strategy: 'HrefLayoutStrategy | None' = None),
            )
            # print(list(level_2_catalog.get_children()))  # no children yet
            # print(list(level_2_catalog.get_items()))  # none yet

            # --- COLLECTION --- #
            ### bbox ###
            geospatial_manager = GeospatialManager()
            bbox, footprint, geojson = geospatial_manager.get_bounding_box()

            #### dates ###
            start_datetime = pd.Timestamp(cruise.time.values[0])
            end_datetime = pd.Timestamp(cruise.time.values[-1])
            temporal_extent = pystac.TemporalExtent(
                intervals=[[start_datetime, end_datetime]]
            )
            #### extent
            spatial_extent = pystac.SpatialExtent(bboxes=[bbox])
            extent = pystac.Extent(spatial=spatial_extent, temporal=temporal_extent)

            level_2_collection = pystac.Collection(
                id="HB1906",  # cruise name
                description="Level 2 water column sonar data from the Henry_B._Bigelow HB1906 cruise",
                extent=extent,
                title="Henry_B._Bigelow HB1906 Zarr Stores",
                # stac_extensions: 'list[str] | None' = None,
                href="https://noaa-wcsd-zarr-pds.s3.amazonaws.com/index.html#level_2a/",
                catalog_type=pystac.CatalogType.ABSOLUTE_PUBLISHED,
                # license: 'str' = 'other',
                keywords=[
                    "ocean",
                    "oceanography",
                    "marine",
                    "water column",
                    "sonar",
                    "fish",
                ],
                providers=[
                    self.provider_cooperative_institute_for_research_in_environmental_sciences,
                    self.provider_marine_geology_and_geophysics,
                    self.provider_national_centers_for_environmental_information,
                ],
                # summaries: 'Summaries | None' = None, # An optional map of property summaries, either a set of values or statistics such as a range.
                # TODO: for assets, would include XML, metadata
                # assets: 'dict[str, Asset] | None' = None,
                # strategy: 'HrefLayoutStrategy | None' = None,
            )
            # level_2_catalog.add_child(level_2_collection)
            # print(list(level_2_catalog.get_children()))  # no children yet
            # print(list(level_2_catalog.get_items()))  # none yet

            # --- ITEM --- #
            level_2_item = pystac.Item(
                id=f"{self.instrument_name}",  # EK60.zarr vs ME70.zarr
                geometry=geojson,
                bbox=bbox,
                datetime=None,
                properties=dict(
                    ship_name=self.ship_name,
                    cruise_name=self.cruise_name,
                    instrument_name=self.instrument_name,
                    #
                    processing_software_name="echofish",
                    processing_software_version="26.1.14",
                    processing_software_time="2026-01-20T09:39:09.116Z",
                    calibration_status=True,
                    doi="http://doi.org/10.25921/vt45-sa66",
                ),
                start_datetime=start_datetime,
                end_datetime=end_datetime,
                # stac_extensions: 'list[str] | None' = None,
                ### TODO: should this be a navigable url or zarr store url? ###
                href="https://noaa-wcsd-zarr-pds.s3.amazonaws.com/level_2a/Henry_B._Bigelow/HB1906/EK60/HB1906.zarr/",
                collection=level_2_collection,
                # extra_fields: 'dict[str, Any] | None' = None,
                # assets: 'dict[str, Asset] | None' = None,
            )
            # --- ASSET --- #
            level_2_asset = pystac.Asset(
                # href="https://noaa-wcsd-zarr-pds.s3.amazonaws.com/level_2a/Henry_B._Bigelow/HB1906/EK60/HB1906.zarr/",
                href="s3://noaa-wcsd-zarr-pds/level_2a/Henry_B._Bigelow/HB1906/EK60/HB1906.zarr/",
                title="HB1906 EK60 Zarr Store",
                description="Zarr store of the HB1906 EK60 data consolidated for the whole cruise",
                media_type=pystac.MediaType.ZARR,
                roles=["data", "zarr"],
                # extra_fields: dict[str, Any] | None = None,
            )
            level_2_item.add_asset(key="EK60", asset=level_2_asset)
            #
            #
            level_2_collection.add_item(level_2_item)
            level_2_catalog.add_child(level_2_collection)
            level_2_catalog.describe()
            #
            # --- ASSET --- #
            # level_2_asset_thumbnail = pystac.Asset(
            #     href="https://www.ncei.noaa.gov/sites/default/files/2022-03/AllBeamCurtains_griddedMultibeam-102-file-good-bathy442x185.jpg",
            #     media_type=pystac.MediaType.JPEG
            # )
            # level_2_item.add_asset(
            #     key="image",
            #     asset=level_2_asset_thumbnail,
            # )
            # level_2_item.add_link(
            #     pystac.Link(
            #         rel="s3://noaa-wcsd-zarr-pds/level_2a/Henry_B._Bigelow/HB1906/EK60/HB1906.zarr",
            #         media_type=pystac.MediaType.ZARR,
            #         title="asf",
            #         target="",
            #     )
            # )
            # asset = pystac.Asset(
            #     href="https://noaa-wcsd-zarr-pds.s3.us-east-1.amazonaws.com/L2A/Henry_B._Bigelow/HB1906/EK60/D20190903-T171901.zarr",
            #     title="HB1906",
            #     description="",
            #     media_type=pystac.MediaType.ZARR,
            #     roles=["data"],
            #     extra_fields=None,
            # )
            #
            # print(level_2_collection.describe())
            # print(new_catalog)
            # print(new_catalog.get_self_href())
            level_2_catalog.normalize_hrefs(os.path.join(tmp_dir.name, "stac"))
            # print(new_catalog.get_self_href())
            level_2_catalog.save(
                catalog_type=pystac.CatalogType.RELATIVE_PUBLISHED
            )  # .SELF_CONTAINED)
            print(f"saved to: {tmp_dir.name}/stac/")
            return (level_2_catalog, f"saved to: {tmp_dir.name}/stac/")
        except Exception as error:
            raise Exception(f"Problem creating catalog: {error}")


### TODO: follow zarr guide here: https://element84.com/software-engineering/zarr-stac/
if __name__ == "__main__":
    catalog_manager = CatalogManager()
    new_catalog, loc = catalog_manager.create_level_2_catalog()
    new_catalog.describe()
    ### https://github.com/stac-utils/xpystac ###
    # item = pystac.Item.from_file(f"{loc}")
    # asset = item.assets["visual"]
    # xr.open_dataset(asset)
    # list(new_catalog.get_items(recursive=True))
    # collection = new_catalog.get_collections()  # "HB1906"
    # asset = collection.assets["ZARR"]  # need way to distinguish??? EK60 vs ME70
    asset = list(new_catalog.get_items(recursive=True))[0].assets["EK60"]
    kwargs = {"consolidated": False}
    ds = xr.open_dataset(filename_or_obj=asset, engine="zarr", **kwargs)
    print(ds)
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
