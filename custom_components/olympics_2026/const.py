DOMAIN = "olympics_2026"
CONF_COUNTRY = "country"

UPDATE_INTERVAL = 300  # 5 minutes

WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/2026_Winter_Olympics_medal_table"

# CET operating hours
START_HOUR = 8
END_HOUR = 24

PARTICIPATING_COUNTRIES = {
    "ALB": "Albania",
    "AND": "Andorra",
    "ARG": "Argentina",
    "ARM": "Armenia",
    "AUS": "Australia",
    "AUT": "Austria",
    "AZE": "Azerbaijan",
    "BEL": "Belgium",
    "BIH": "Bosnia and Herzegovina",
    "BRA": "Brazil",
    "BUL": "Bulgaria",
    "CAN": "Canada",
    "CHI": "Chile",
    "CHN": "China",
    "COL": "Colombia",
    "CRO": "Croatia",
    "CYP": "Cyprus",
    "CZE": "Czech Republic",
    "DEN": "Denmark",
    "ESP": "Spain",
    "EST": "Estonia",
    "FIN": "Finland",
    "FRA": "France",
    "GBR": "Great Britain",
    "GEO": "Georgia",
    "GER": "Germany",
    "GRE": "Greece",
    "HKG": "Hong Kong",
    "HUN": "Hungary",
    "IND": "India",
    "IRL": "Ireland",
    "ISL": "Iceland",
    "ISR": "Israel",
    "ITA": "Italy",
    "JAM": "Jamaica",
    "JPN": "Japan",
    "KAZ": "Kazakhstan",
    "KOR": "South Korea",
    "KOS": "Kosovo",
    "LAT": "Latvia",
    "LIE": "Liechtenstein",
    "LTU": "Lithuania",
    "LUX": "Luxembourg",
    "MDA": "Moldova",
    "MEX": "Mexico",
    "MKD": "North Macedonia",
    "MNE": "Montenegro",
    "MON": "Monaco",
    "NED": "Netherlands",
    "NOR": "Norway",
    "NZL": "New Zealand",
    "PAK": "Pakistan",
    "POL": "Poland",
    "POR": "Portugal",
    "PRK": "North Korea",
    "PUR": "Puerto Rico",
    "ROU": "Romania",
    "RSA": "South Africa",
    "RUS": "Russia",
    "SAN": "San Marino",
    "SER": "Serbia",
    "SLO": "Slovenia",
    "SVK": "Slovakia",
    "SUI": "Switzerland",
    "SWE": "Sweden",
    "THA": "Thailand",
    "TPE": "Chinese Taipei",
    "TUR": "Turkey",
    "UKR": "Ukraine",
    "USA": "United States",
    "UZB": "Uzbekistan",
}

COUNTRY_NAME_MAPPING = {
    "United States": "USA",
    "Great Britain": "GBR",
    "South Korea": "KOR",
    "North Korea": "PRK",
    "Chinese Taipei": "TPE",
    "Czech Republic": "CZE",
    "New Zealand": "NZL",
    "South Africa": "RSA",
}

for code, name in PARTICIPATING_COUNTRIES.items():
    COUNTRY_NAME_MAPPING[name] = code
