import ckan.logic as logic
from ckanext.scheming.helpers import scheming_get_dataset_schema
import json

_get_or_bust = logic.get_or_bust


def get_site_statistics():
    stats = {}
    stats['dataset_count'] = logic.get_action('package_search')(
        {}, {"rows": 1})['count']
    stats['group_count'] = len(logic.get_action('group_list')({}, {}))
    stats['organization_count'] = len(
        logic.get_action('organization_list')({}, {}))
    stats['user_count'] = len(
        logic.get_action('user_list')({}, {}))
    return stats

def data_dict_with_spatial(context, data_dict):
    #t = _get_or_bust(data_dict, "type")
    t = 'dataset'
    expanded = data_dict.get("expanded", True)
    s = scheming_get_dataset_schema(t, expanded)

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
        return data_dict

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
    locations = [
        {
            "label": "Svalbard",
            "lon": 16.1761980317877,
            "lat": 78.27838387,
        },
        {
            "label": "Svalbard - Kongsfjorden",
            "lon": 12.00434,
            "lat": 79.061159,
        },
        {
            "label": "Svalbard - Kongsfjorden - Blomstrandoya",
            "lon": 12.10577,
            "lat": 78.975803,
        },
        {
            "label": "Svalbard - Kongsfjorden - Broggerhalvoya",
            "lon": 11.735704,
            "lat": 78.914647,
        },
        {
            "label": "Svalbard - Kongsfjorden - Broggerhalvoya - Simlestupet",
            "lon": 11.735704,
            "lat": 78.914647,
        },
        {
            "label": "Svalbard - Kongsfjorden - Broggerhalvoya - Leinstranda",
            "lon": 11.735704,
            "lat": 78.914647,
        },
        {
            "label": "Svalbard - Kongsfjorden - Kaffioyra",
            "lon": 11.976978,
            "lat": 78.628325,
        },
        {
            "label": "Svalbard - Kongsfjorden - Ossiansarsfjellet",
            "lon": 12.476667,
            "lat": 78.942761,
        },
        {
            "label": "Svalbard - Kongsfjorden - Sarsoyra",
            "lon": 11.647155,
            "lat": 78.756613,
        },
        {
            "label": "Svalbard - Nordenkioldland",
            "lon": 15.116477,
            "lat": 78.013984,
        },
        {
            "label": "Svalbard - Nordenskioldland - Adventdalen",
            "lon": 16.250824,
            "lat": 78.179487,
        },
        {
            "label": "Svalbard - Nordenskioldland - Adventdalen - Endalen",
            "lon": 16.250824,
            "lat": 78.179487,
        },
        {
            "label": "Svalbard - Nordenskioldland - Adventdalen - Janssonhaugen",
            "lon": 16.250824,
            "lat": 78.179487,
        },
        {
            "label": "Svalbard - Nordenskioldland - Adventdalen - Bjorndalen",
            "lon": 16.250824,
            "lat": 78.179487,
        },
        {
            "label": "Svalbard - Nordenskioldland - Adventdalen - Hanaskogdalen",
            "lon": 16.250824,
            "lat": 78.179487,
        },
        {
            "label": "Svalbard - Nordenskioldland - Adventdalen - Malardalen",
            "lon": 16.250824,
            "lat": 78.179487,
        },
        {
            "label": "Svalbard - Nordenskioldland - Adventdalen - Todalen",
            "lon": 16.250824,
            "lat": 78.179487,
        },
        {
            "label": "Svalbard - Nordenskioldland - Adventdalen - Bolterdalen",
            "lon": 16.250824,
            "lat": 78.179487,
        },
        {
            "label": "Svalbard - Nordenskioldland - Alkhornet",
            "lon": 13.741739,
            "lat": 78.215766,
        },
        {
            "label": "Svalbard - Nordenskioldland - Colesdalen",
            "lon": 15.202606,
            "lat": 78.080511,
        },
        {
            "label": "Svalbard - Nordenskioldland - Reindalen",
            "lon": 15.765129,
            "lat": 77.950241,
        },
        {
            "label": "Svalbard - Nordenskioldland - Sassendalen",
            "lon": 17.211454,
            "lat": 78.26552,
        },
        {
            "label": "Svalbard - Nordenskioldland - Sassendalen - Gjelhallet",
            "lon": 17.211454,
            "lat": 78.26552,
        },
        {
            "label": "Svalbard - Nordenskioldland - Sassendalen - Eskerdalen",
            "lon": 17.211454,
            "lat": 78.26552,
        },
        {
            "label": "Svalbard - Nordenskioldland - Semmeldalen",
            "lon": 15.416838,
            "lat": 77.966604,
        },
        {
            "label": "Varanger",
            "lon": 29.5298900097758,
            "lat": 70.39534162,
        },
        {
            "label": "Varanger - Siskkit corgas ja lagesduottar",
            "lon": 27.514059,
            "lat": 70.60438,
        },
        {
            "label": "Varanger - Siskkit corgas ja lagesduottar - Bekkarfjord",
            "lon": 27.476085,
            "lat": 70.705655,
        },
        {
            "label": "Varanger - Siskkit corgas ja lagesduottar - Ifjordfjellet",
            "lon": 27.4692352873563,
            "lat": 70.42233736,
        },
        {
            "label": "Varanger - Siskkit corgas ja lagesduottar - Ifjordfjellet - Eastordalen",
            "lon": 27.4692352873563,
            "lat": 70.42233736,
        },
        {
            "label": "Varanger - Siskkit corgas ja lagesduottar - Ifjordfjellet - Storelva",
            "lon": 27.4692352873563,
            "lat": 70.42233736,
        },
        {
            "label": "Varanger - Siskkit corgas ja lagesduottar - Ifjordfjellet - Iesjohka",
            "lon": 27.4692352873563,
            "lat": 70.42233736,
        },
        {
            "label": "Varanger - Siskkit corgas ja lagesduottar - Ifjordfjellet - Giksjohka",
            "lon": 27.4692352873563,
            "lat": 70.42233736,
        },
        {
            "label": "Varanger - Siskkit corgas ja lagesduottar - Ifjordfjellet - Gurrojohka",
            "lon": 27.4692352873563,
            "lat": 70.42233736,
        },
        {
            "label": "Varanger - Siskkit corgas ja lagesduottar - Ifjordfjellet - Suoljavri",
            "lon": 27.4692352873563,
            "lat": 70.42233736,
        },
        {
            "label": "Varanger - Olggut corgas oarje deatnu",
            "lon": 27.85705,
            "lat": 70.907408,
        },
        {
            "label": "Varanger - Olggut corgas oarje deatnu - Nordkynn",
            "lon": 27.74431,
            "lat": 70.9333935,
        },
        {
            "label": "Varanger - Olggut corgas oarje deatnu - Tana",
            "lon": 27.7096679608677,
            "lat": 70.07999344,
        },
        {
            "label": "Varanger - Olggut corgas oarje deatnu - Skjaernes",
            "lon": 27.8498,
            "lat": 70.442,
        },
        {
            "label": "Varanger - Olggut corgas oarje deatnu - Boftsa",
            "lon": 28.178,
            "lat": 70.3701,
        },
        {
            "label": "Varanger - Bahcaveaijji",
            "lon": 29.185076,
            "lat": 69.78709,
        },
        {
            "label": "Varanger - Bahcaveaijji - Bugoyfjord",
            "lon": 29.3306369580431,
            "lat": 69.89285477,
        },
        {
            "label": "Varanger - Bahcaveaijji - Kirkenes",
            "lon": 29.350363333001,
            "lat": 69.76388,
        },
        {
            "label": "Varanger - Rakkonjarga",
            "lon": 28.8749670228275,
            "lat": 70.65542217,
        },
        {
            "label": "Varanger - Rakkonjarga - Austertana",
            "lon": 28.5673587353134,
            "lat": 70.43537992,
        },
        {
            "label": "Varanger - Rakkonjarga - Luftjok",
            "lon": 28.3815452755338,
            "lat": 70.25333517,
        },
        {
            "label": "Varanger - Rakkonjarga - Polmak",
            "lon": 27.9812148162841,
            "lat": 70.03199545,
        },
        {
            "label": "Varanger - Rakkonjarga - Polmak - Polmak finland",
            "lon": 27.9812148162841,
            "lat": 70.03199545,
        },
        {
            "label": "Varanger - Rakkonjarga - Polmak - Polmak norway",
            "lon": 27.9812148162841,
            "lat": 70.03199545,
        },
        {
            "label": "Varanger - Rakkonjarga - Stjernevann",
            "lon": 29.211285,
            "lat": 70.54163917,
        },
        {
            "label": "Varanger - Varjjatnjarga",
            "lon": 29.7042036634186,
            "lat": 70.36574553,
        },
        {
            "label": "Varanger - Varjjatnjarga - Bergebydalen",
            "lon": 29.016312,
            "lat": 70.236493,
        },
        {
            "label": "Varanger - Varjjatnjarga - Komagdalen",
            "lon": 30.0043184621013,
            "lat": 70.33535233,
        },
        {
            "label": "Varanger - Varjjatnjarga - Komagdalen - Komagdalen ovre",
            "lon": 30.0043184621013,
            "lat": 70.33535233,
        },
        {
            "label": "Varanger - Varjjatnjarga - Komagdalen - Komagdalen midtre",
            "lon": 30.0043184621013,
            "lat": 70.33535233,
        },
        {
            "label": "Varanger - Varjjatnjarga - Komagdalen - Komagdalen nedre",
            "lon": 30.0043184621013,
            "lat": 70.33535233,
        },
        {
            "label": "Varanger - Varjjatnjarga - Komagdalen - Sanfjorddalen",
            "lon": 30.0043184621013,
            "lat": 70.33535233,
        },
        {
            "label": "Varanger - Varjjatnjarga - Komagdalen - Kjoltindan",
            "lon": 30.0043184621013,
            "lat": 70.33535233,
        },
        {
            "label": "Varanger - Varjjatnjarga - Komagdalen - Gargas",
            "lon": 30.0043184621013,
            "lat": 70.33535233,
        },
        {
            "label": "Varanger - Varjjatnjarga - Komagdalen - Ryggfjellet",
            "lon": 30.0043184621013,
            "lat": 70.33535233,
        },
        {
            "label": "Varanger - Varjjatnjarga - Komagdalen - Hubejohka",
            "lon": 30.0043184621013,
            "lat": 70.33535233,
        },
        {
            "label": "Varanger - Varjjatnjarga - Komagdalen - Roussachokka",
            "lon": 30.0043184621013,
            "lat": 70.33535233,
        },
        {
            "label": "Varanger - Varjjatnjarga - Vestre Jakobselv",
            "lon": 29.0756827124289,
            "lat": 70.29141287,
        },
        {
            "label": "Varanger - Varjjatnjarga - Vestre Jakobselv - Torvhaugdalen",
            "lon": 29.0756827124289,
            "lat": 70.29141287,
        },
        {
            "label": "Varanger - Varjjatnjarga - Vestre Jakobselv - Baeralveaijohka",
            "lon": 29.0756827124289,
            "lat": 70.29141287,
        },
        {
            "label": "Varanger - Varjjatnjarga - Vestre Jakobselv - Jakobselv",
            "lon": 29.0756827124289,
            "lat": 70.29141287,
        },
        {
            "label": "Varanger - Varjjatnjarga - Vestre Jakobselv - Reinhaugen",
            "lon": 29.0756827124289,
            "lat": 70.29141287,
        },
        {
            "label": "Varanger - Varjjatnjarga - Vestre Jakobselv - Skoarrajohka",
            "lon": 29.0756827124289,
            "lat": 70.29141287,
        },
        {
            "label": "Varanger - Varjjatnjarga - Vestre Jakobselv - Tranemyra",
            "lon": 29.0756827124289,
            "lat": 70.29141287,
        },
        {
            "label": "Varanger - Varjjatnjarga - Vestre Jakobselv - Gaasevannan",
            "lon": 29.0756827124289,
            "lat": 70.29141287,
        },
    ]
    for location in locations:
        label = location['label'].split(' - ')[-1]
        location['value'] = ''.join(c for c in label.lower() if c.isalpha())
    return sorted(locations, key = lambda kv: kv['label'])


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
