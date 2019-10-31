import ckan.logic as logic
from ckanext.scheming.helpers import scheming_get_dataset_schema
import json

_get_or_bust = logic.get_or_bust


def data_dict_with_spatial(context, data_dict):
    # parent dataset
    # https://github.com/aptivate/ckanext-datasetversions/issues/10

    t = _get_or_bust(data_dict, "type")
    expanded = data_dict.get("expanded", True)
    s = scheming_get_dataset_schema(t, expanded)
    # data_dict['temp'] = s

    longitudes = []
    latitudes = []
    for field in s["dataset_fields"]:
        if field["field_name"] != "location":
            continue
        for choice in scheming_locations_choices(None):
            if choice["value"] not in data_dict.get("location", []):
                continue
            longitudes.append(choice["lon"])
            latitudes.append(choice["lat"])

    if not longitudes or not latitudes:
        return coat_package_create(context, data_dict)

    lon_min, lon_max = min(longitudes), max(longitudes)
    lat_min, lat_max = min(latitudes), max(latitudes)
    geometry = {
        "type": "Polygon",
        "coordinates": [
            [
                [lon_min, lat_max],
                [lon_max, lat_max],
                [lon_max, lat_min],
                [lon_min, lat_min],
                [lon_min, lat_max],
            ]
        ],
    }

    value = json.dumps(geometry)
    data_dict.setdefault("extras", [])  # ?
    for item in data_dict["extras"]:
        if item.get("key") == "spatial":
            item["value"] = value
            break
    else:
        data_dict["extras"].append({"key": "spatial", "value": value})

    return data_dict


def scheming_tags_choices(field):
    return [
        {"value": "aerial-imagery", "label": "Aerial imagery"},
        {"value": "air-temperature", "label": "Air temperature"},
        {"value": "albedo", "label": "Albedo"},
        {"value": "artificial-nests", "label": "Artificial nests"},
        {"value": "barcoding", "label": "Barcoding"},
        {"value": "birch-forest", "label": "Birch forest"},
        {"value": "camera-traps", "label": "Camera traps"},
        {"value": "dendroecology", "label": "Dendroecology"},
        {"value": "distance-sampling", "label": "Distance sampling"},
        {"value": "dwarf-shrub-heath", "label": "Dwarf shrub heath"},
        {"value": "experimental-exclosures", "label": "Experimental exclosures"},
        {"value": "flight-intercept-traps", "label": "Flight intercept traps"},
        {"value": "forest", "label": "Forest"},
        {"value": "GPS-tags", "label": "GPS tags"},
        {"value": "grassy-tundra", "label": "Grassy tundra"},
        {"value": "ground-ice", "label": "Ground ice"},
        {"value": "ground-temperature", "label": "Ground temperature"},
        {"value": "heath", "label": "Heath"},
        {"value": "humidity", "label": "Humidity"},
        {"value": "hummock-tundra", "label": "Hummock tundra"},
        {"value": "hunting-records", "label": "Hunting records"},
        {"value": "ice-thickness", "label": "Ice thickness"},
        {"value": "icing", "label": "Icing"},
        {"value": "live-trapping", "label": "Live trapping"},
        {"value": "meadow", "label": "Meadow"},
        {"value": "metabarcoding", "label": "Metabarcoding"},
        {"value": "microsatellites", "label": "Microsatellites"},
        {"value": "modelling", "label": "Modelling"},
        {"value": "moss-tundra", "label": "Moss tundra"},
        {"value": "NDVI", "label": "NDVI"},
        {"value": "NIRS", "label": "NIRS"},
        {"value": "pellet-counts", "label": "Pellet counts"},
        {"value": "point-intercept", "label": "Point intercept"},
        {"value": "population-modelling", "label": "Population modelling"},
        {"value": "precipitation", "label": "Precipitation"},
        {"value": "radiation", "label": "Radiation"},
        {"value": "rain-on-snow", "label": "Rain on snow"},
        {"value": "remote-sensing", "label": "Remote sensing"},
        {"value": "repeat-photography", "label": "Repeat photography"},
        {"value": "satellite-imagery", "label": "Satellite imagery"},
        {"value": "satellite-tags", "label": "Satellite tags"},
        {"value": "scat-analysis", "label": "Scat analysis"},
        {"value": "snap-trapping", "label": "Snap trapping"},
        {"value": "snow-beds", "label": "Snow beds"},
        {"value": "snow-depth", "label": "Snow depth"},
        {"value": "snow-melt", "label": "Snow melt"},
        {"value": "snow-modelling", "label": "Snow modelling"},
        {"value": "snow-pits", "label": "Snow pits"},
        {"value": "snow-structure", "label": "Snow structure"},
        {"value": "snow-tracking", "label": "Snow tracking"},
        {"value": "soil-temperature", "label": "Soil temperature"},
        {"value": "stable-isotopes", "label": "Stable isotopes"},
        {"value": "surveys", "label": "Surveys"},
        {"value": "tall-shrub", "label": "Tall shrub"},
        {"value": "temperature", "label": "Temperature"},
        {"value": "temperature-logger", "label": "Temperature logger"},
        {"value": "timing-of-icing", "label": "Timing of icing"},
        {"value": "timing-of-snow-melt", "label": "Timing of snow melt"},
        {"value": "tundra", "label": "Tundra"},
        {"value": "weather-station", "label": "Weather station"},
        {"value": "wind", "label": "Wind"},
    ]


def scheming_locations_choices(field):
    return [
        {
            "value": "Svalbard",
            "label": "Svalbard",
            "lon": 16.1761980317877,
            "lat": 78.27838387,
        },
        {
            "value": "Kongsfjorden",
            "label": "Svalbard - Kongsfjorden",
            "lon": 12.00434,
            "lat": 79.061159,
        },
        {
            "value": "Blomstrandoya",
            "label": "Svalbard - Kongsfjorden - Blomstrandoya",
            "lon": 12.10577,
            "lat": 78.975803,
        },
        {
            "value": "Broggerhalvoya",
            "label": "Svalbard - Kongsfjorden - Broggerhalvoya",
            "lon": 11.735704,
            "lat": 78.914647,
        },
        {
            "value": "Simlestupet",
            "label": "Svalbard - Kongsfjorden - Broggerhalvoya - Simlestupet",
            "lon": 11.735704,
            "lat": 78.914647,
        },
        {
            "value": "Leinstranda",
            "label": "Svalbard - Kongsfjorden - Broggerhalvoya - Leinstranda",
            "lon": 11.735704,
            "lat": 78.914647,
        },
        {
            "value": "Kaffioyra",
            "label": "Svalbard - Kongsfjorden - Kaffioyra",
            "lon": 11.976978,
            "lat": 78.628325,
        },
        {
            "value": "Ossiansarsfjellet",
            "label": "Svalbard - Kongsfjorden - Ossiansarsfjellet",
            "lon": 12.476667,
            "lat": 78.942761,
        },
        {
            "value": "Sarsoyra",
            "label": "Svalbard - Kongsfjorden - Sarsoyra",
            "lon": 11.647155,
            "lat": 78.756613,
        },
        {
            "value": "Nordenkioldland",
            "label": "Svalbard - Nordenkioldland",
            "lon": 15.116477,
            "lat": 78.013984,
        },
        {
            "value": "Adventdalen",
            "label": "Svalbard - Nordenskioldland - Adventdalen",
            "lon": 16.250824,
            "lat": 78.179487,
        },
        {
            "value": "Endalen",
            "label": "Svalbard - Nordenskioldland - Adventdalen - Endalen",
            "lon": 16.250824,
            "lat": 78.179487,
        },
        {
            "value": "Janssonhaugen",
            "label": "Svalbard - Nordenskioldland - Adventdalen - Janssonhaugen",
            "lon": 16.250824,
            "lat": 78.179487,
        },
        {
            "value": "Bjorndalen",
            "label": "Svalbard - Nordenskioldland - Adventdalen - Bjorndalen",
            "lon": 16.250824,
            "lat": 78.179487,
        },
        {
            "value": "Hanaskogdalen",
            "label": "Svalbard - Nordenskioldland - Adventdalen - Hanaskogdalen",
            "lon": 16.250824,
            "lat": 78.179487,
        },
        {
            "value": "Malardalen",
            "label": "Svalbard - Nordenskioldland - Adventdalen - Malardalen",
            "lon": 16.250824,
            "lat": 78.179487,
        },
        {
            "value": "Todalen",
            "label": "Svalbard - Nordenskioldland - Adventdalen - Todalen",
            "lon": 16.250824,
            "lat": 78.179487,
        },
        {
            "value": "Bolterdalen",
            "label": "Svalbard - Nordenskioldland - Adventdalen - Bolterdalen",
            "lon": 16.250824,
            "lat": 78.179487,
        },
        {
            "value": "Alkhornet",
            "label": "Svalbard - Nordenskioldland - Alkhornet",
            "lon": 13.741739,
            "lat": 78.215766,
        },
        {
            "value": "Colesdalen",
            "label": "Svalbard - Nordenskioldland - Colesdalen",
            "lon": 15.202606,
            "lat": 78.080511,
        },
        {
            "value": "Reindalen",
            "label": "Svalbard - Nordenskioldland - Reindalen",
            "lon": 15.765129,
            "lat": 77.950241,
        },
        {
            "value": "Sassendalen",
            "label": "Svalbard - Nordenskioldland - Sassendalen",
            "lon": 17.211454,
            "lat": 78.26552,
        },
        {
            "value": "Gjelhallet",
            "label": "Svalbard - Nordenskioldland - Sassendalen - Gjelhallet",
            "lon": 17.211454,
            "lat": 78.26552,
        },
        {
            "value": "Eskerdalen",
            "label": "Svalbard - Nordenskioldland - Sassendalen - Eskerdalen",
            "lon": 17.211454,
            "lat": 78.26552,
        },
        {
            "value": "Semmeldalen",
            "label": "Svalbard - Nordenskioldland - Semmeldalen",
            "lon": 15.416838,
            "lat": 77.966604,
        },
        {
            "value": "Varanger",
            "label": "Varanger",
            "lon": 29.5298900097758,
            "lat": 70.39534162,
        },
        {
            "value": "Siskkit_corgas_ja_lagesduottar",
            "label": "Varanger - Siskkit_corgas_ja_lagesduottar",
            "lon": 27.514059,
            "lat": 70.60438,
        },
        {
            "value": "Bekkarfjord",
            "label": "Varanger - Siskkit_corgas_ja_lagesduottar - Bekkarfjord",
            "lon": 27.476085,
            "lat": 70.705655,
        },
        {
            "value": "Ifjordfjellet",
            "label": "Varanger - Siskkit_corgas_ja_lagesduottar - Ifjordfjellet",
            "lon": 27.4692352873563,
            "lat": 70.42233736,
        },
        {
            "value": "Eastordalen",
            "label": "Varanger - Siskkit_corgas_ja_lagesduottar - Ifjordfjellet - Eastordalen",
            "lon": 27.4692352873563,
            "lat": 70.42233736,
        },
        {
            "value": "Storelva",
            "label": "Varanger - Siskkit_corgas_ja_lagesduottar - Ifjordfjellet - Storelva",
            "lon": 27.4692352873563,
            "lat": 70.42233736,
        },
        {
            "value": "Iesjohka",
            "label": "Varanger - Siskkit_corgas_ja_lagesduottar - Ifjordfjellet - Iesjohka",
            "lon": 27.4692352873563,
            "lat": 70.42233736,
        },
        {
            "value": "Giksjohka",
            "label": "Varanger - Siskkit_corgas_ja_lagesduottar - Ifjordfjellet - Giksjohka",
            "lon": 27.4692352873563,
            "lat": 70.42233736,
        },
        {
            "value": "Gurrojohka",
            "label": "Varanger - Siskkit_corgas_ja_lagesduottar - Ifjordfjellet - Gurrojohka",
            "lon": 27.4692352873563,
            "lat": 70.42233736,
        },
        {
            "value": "Suoljavri",
            "label": "Varanger - Siskkit_corgas_ja_lagesduottar - Ifjordfjellet - Suoljavri",
            "lon": 27.4692352873563,
            "lat": 70.42233736,
        },
        {
            "value": "Olggut_corgas_oarje_deatnu",
            "label": "Varanger - Olggut_corgas_oarje_deatnu",
            "lon": 27.85705,
            "lat": 70.907408,
        },
        {
            "value": "Nordkynn",
            "label": "Varanger - Olggut_corgas_oarje_deatnu - Nordkynn",
            "lon": 27.74431,
            "lat": 70.9333935,
        },
        {
            "value": "Tana",
            "label": "Varanger - Olggut_corgas_oarje_deatnu -Tana",
            "lon": 27.7096679608677,
            "lat": 70.07999344,
        },
        {
            "value": "Skjaernes",
            "label": "Varanger - Olggut_corgas_oarje_deatnu -Skjaernes",
            "lon": 27.8498,
            "lat": 70.442,
        },
        {
            "value": "Boftsa",
            "label": "Varanger - Olggut_corgas_oarje_deatnu -Boftsa",
            "lon": 28.178,
            "lat": 70.3701,
        },
        {
            "value": "Bahcaveaijji",
            "label": "Varanger - Bahcaveaijji",
            "lon": 29.185076,
            "lat": 69.78709,
        },
        {
            "value": "Bugoyfjord",
            "label": "Varanger - Bahcaveaijji - Bugoyfjord",
            "lon": 29.3306369580431,
            "lat": 69.89285477,
        },
        {
            "value": "Kirkenes",
            "label": "Varanger - Bahcaveaijji - Kirkenes",
            "lon": 29.350363333001,
            "lat": 69.76388,
        },
        {
            "value": "Rakkonjarga",
            "label": "Varanger - Rakkonjarga",
            "lon": 28.8749670228275,
            "lat": 70.65542217,
        },
        {
            "value": "Austertana",
            "label": "Varanger - Rakkonjarga - Austertana",
            "lon": 28.5673587353134,
            "lat": 70.43537992,
        },
        {
            "value": "Luftjok",
            "label": "Varanger - Rakkonjarga - Luftjok",
            "lon": 28.3815452755338,
            "lat": 70.25333517,
        },
        {
            "value": "Polmak",
            "label": "Varanger - Rakkonjarga - Polmak",
            "lon": 27.9812148162841,
            "lat": 70.03199545,
        },
        {
            "value": "Polmak_finland",
            "label": "Varanger - Rakkonjarga - Polmak - Polmak_finland",
            "lon": 27.9812148162841,
            "lat": 70.03199545,
        },
        {
            "value": "Polmak_norway",
            "label": "Varanger - Rakkonjarga - Polmak - Polmak_norway",
            "lon": 27.9812148162841,
            "lat": 70.03199545,
        },
        {
            "value": "Stjernevann",
            "label": "Varanger - Rakkonjarga - Stjernevann",
            "lon": 29.211285,
            "lat": 70.54163917,
        },
        {
            "value": "Varjjatnjarga",
            "label": "Varanger - Varjjatnjarga",
            "lon": 29.7042036634186,
            "lat": 70.36574553,
        },
        {
            "value": "Bergebydalen",
            "label": "Varanger - Varjjatnjarga - Bergebydalen",
            "lon": 29.016312,
            "lat": 70.236493,
        },
        {
            "value": "Komagdalen",
            "label": "Varanger - Varjjatnjarga - Komagdalen",
            "lon": 30.0043184621013,
            "lat": 70.33535233,
        },
        {
            "value": "Komagdalen_ovre",
            "label": "Varanger - Varjjatnjarga - Komagdalen - Komagdalen_ovre",
            "lon": 30.0043184621013,
            "lat": 70.33535233,
        },
        {
            "value": "Komagdalen_midtre",
            "label": "Varanger - Varjjatnjarga - Komagdalen - Komagdalen_midtre",
            "lon": 30.0043184621013,
            "lat": 70.33535233,
        },
        {
            "value": "Komagdalen_nedre",
            "label": "Varanger - Varjjatnjarga - Komagdalen - Komagdalen_nedre",
            "lon": 30.0043184621013,
            "lat": 70.33535233,
        },
        {
            "value": "Sanfjorddalen",
            "label": "Varanger - Varjjatnjarga - Komagdalen - Sanfjorddalen",
            "lon": 30.0043184621013,
            "lat": 70.33535233,
        },
        {
            "value": "Kjoltindan",
            "label": "Varanger - Varjjatnjarga - Komagdalen - Kjoltindan",
            "lon": 30.0043184621013,
            "lat": 70.33535233,
        },
        {
            "value": "Gargas",
            "label": "Varanger - Varjjatnjarga - Komagdalen - Gargas",
            "lon": 30.0043184621013,
            "lat": 70.33535233,
        },
        {
            "value": "Ryggfjellet",
            "label": "Varanger - Varjjatnjarga - Komagdalen - Ryggfjellet",
            "lon": 30.0043184621013,
            "lat": 70.33535233,
        },
        {
            "value": "Hubejohka",
            "label": "Varanger - Varjjatnjarga - Komagdalen - Hubejohka",
            "lon": 30.0043184621013,
            "lat": 70.33535233,
        },
        {
            "value": "Roussachokka",
            "label": "Varanger - Varjjatnjarga - Komagdalen - Roussachokka",
            "lon": 30.0043184621013,
            "lat": 70.33535233,
        },
        {
            "value": "Vestre_Jakobselv",
            "label": "Varanger - Varjjatnjarga - Vestre_Jakobselv",
            "lon": 29.0756827124289,
            "lat": 70.29141287,
        },
        {
            "value": "Torvhaugdalen",
            "label": "Varanger - Varjjatnjarga - Vestre_Jakobselv - Torvhaugdalen",
            "lon": 29.0756827124289,
            "lat": 70.29141287,
        },
        {
            "value": "Baeralveaijohka",
            "label": "Varanger - Varjjatnjarga - Vestre_Jakobselv - Baeralveaijohka",
            "lon": 29.0756827124289,
            "lat": 70.29141287,
        },
        {
            "value": "Jakobselv",
            "label": "Varanger - Varjjatnjarga - Vestre_Jakobselv - Jakobselv",
            "lon": 29.0756827124289,
            "lat": 70.29141287,
        },
        {
            "value": "Reinhaugen",
            "label": "Varanger - Varjjatnjarga - Vestre_Jakobselv - Reinhaugen",
            "lon": 29.0756827124289,
            "lat": 70.29141287,
        },
        {
            "value": "Skoarrajohka",
            "label": "Varanger - Varjjatnjarga - Vestre_Jakobselv - Skoarrajohka",
            "lon": 29.0756827124289,
            "lat": 70.29141287,
        },
        {
            "value": "Tranemyra",
            "label": "Varanger - Varjjatnjarga - Vestre_Jakobselv - Tranemyra",
            "lon": 29.0756827124289,
            "lat": 70.29141287,
        },
        {
            "value": "Gaasevannan",
            "label": "Varanger - Varjjatnjarga - Vestre_Jakobselv - Gaasevannan",
            "lon": 29.0756827124289,
            "lat": 70.29141287,
        },
    ]


def scheming_topic_category_choices(field):
    return [
        {"value": "Biota", "label": "Biota"},
        {"value": "Boundaries", "label": "Boundaries"},
        {"value": "Climatology", "label": "Climatology /Meteorology /Atmosphere"},
        {"value": "Economy", "label": "Economy"},
        {"value": "Elevation", "label": "Elevation"},
        {"value": "Environment", "label": "Environment"},
        {"value": "Farming", "label": "Farming"},
        {"value": "Geoscientific", "label": "Geoscientific Information"},
        {"value": "Health", "label": "Health"},
        {"value": "Imagery", "label": "Imagery / Base Maps / Earth Cover"},
        {"value": "Inland_Waters", "label": "Inland Waters"},
        {"value": "Intelligence", "label": "Intelligence / Military"},
        {"value": "Location", "label": "Location"},
        {"value": "Oceans", "label": "Oceans"},
        {"value": "Planning", "label": "Planning / Cadastre"},
        {"value": "Society", "label": "Society"},
        {"value": "Structure", "label": "Structure"},
        {"value": "Transportation", "label": "Transportation"},
        {"value": "utilities", "label": "Utilities / Communication"},
    ]
