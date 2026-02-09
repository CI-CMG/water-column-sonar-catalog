from enum import Enum, unique

import pystac


@unique
class Providers(Enum):
    ### NOAA ###
    provider_noaa = pystac.Provider(
        name="National Oceanic and Atmospheric Administration (NOAA)",
        description="The National Oceanic and Atmospheric Administration is a United States scientific and regulatory agency tasked with forecasting weather, monitoring oceanic and atmospheric conditions, charting the seas, conducting deep-sea exploration, and managing fishing and protection of marine mammals and endangered species in the US exclusive economic zone.",
        roles=[pystac.ProviderRole.HOST],
        url="https://www.ncei.noaa.gov/",
    )
    provider_ncei = pystac.Provider(
        name="NOAA National Centers for Environmental Information (NCEI)",
        description="In collaboration with NOAA's National Marine Fisheries Service (NMFS) and the University of Colorado Boulder, NOAA’s National Centers for Environmental Information (NCEI) established a national archive for water column sonar data. This project entails ensuring the long-term stewardship of well-documented water column sonar data, and enabling discovery and access to researchers and the public around the world.",
        roles=[pystac.ProviderRole.HOST],
        url="https://www.ncei.noaa.gov/",
    )
    # NOAA Northeast Fisheries Science Center
    provider_nefsc = pystac.Provider(
        name="NOAA Northeast Fisheries Science Center",
        description="The Northeast Fisheries Science Center has conducted a comprehensive marine science program in the region since 1871. We study fishery species and fisheries, monitor and model ocean ecosystems, and provide reliable advice for policy makers.",
        roles=[pystac.ProviderRole.PRODUCER],
        url="https://www.fisheries.noaa.gov/about/northeast-fisheries-science-center",
    )

    provider_mgg = pystac.Provider(
        name="Marine Geology and Geophysics",
        description="The NOAA National Centers for Environmental Information (NCEI) are part of the US Department of Commerce, National Oceanic and Atmospheric Administration (NOAA), National Environmental Satellite, Data, and Information Service (NESDIS).",
        roles=[pystac.ProviderRole.PROCESSOR],
        url="https://www.ngdc.noaa.gov/mgg/aboutmgg/aboutmgg.html",
    )

    ### University of Colorado Boulder ###
    provider_cires = pystac.Provider(
        name="Cooperative Institute for Research In Environmental Sciences",
        description="At CIRES, the Cooperative Institute for Research In Environmental Sciences, hundreds of scientists work to understand the dynamic Earth system, including people’s relationship with the planet.",
        roles=[pystac.ProviderRole.PROCESSOR],
        url="https://cires.colorado.edu/",
    )

    ### SHIPS ###
    provider_henry_bigelow = pystac.Provider(
        name="Henry_B._Bigelow",
        description="Henry B. Bigelow conducts both acoustic and trawl surveys.",
        roles=[pystac.ProviderRole.PRODUCER],
        url="https://www.omao.noaa.gov/marine-operations/ships/henry-b-bigelow",
    )
    provider_okeanos_explorer = pystac.Provider(
        name="Okeanos_Explorer",
        description="An exploratory vessel for the National Oceanic and Atmospheric Administration (NOAA).",
        roles=[pystac.ProviderRole.PRODUCER],
        url="https://oceanexplorer.noaa.gov/okeanos/",
    )
