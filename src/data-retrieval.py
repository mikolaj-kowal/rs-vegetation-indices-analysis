import os
import geopandas as gpd
import requests
import yaml
import zipfile


from dotenv import load_dotenv
from pathlib import Path
from pystac_client import Client

load_dotenv()

# load configuration from config file
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

output_dir = Path(config["output_dir"])
data_dir = Path(config["data_dir"])

date_from = config["date_from"]
date_to = config["date_to"]
max_cloud_cover = config["max_cloud_cover"]

# define Area of Interest (AOI)
aoi = gpd.read_file(config["aoi"]).to_crs("EPSG:4326")
bbox = aoi.total_bounds

# search CDSE STAC
catalog = Client.open("https://stac.dataspace.copernicus.eu/v1")
search = catalog.search(
    collections=config["collection"],
    bbox=bbox,
    datetime=f"{date_from}/{date_to}",
    query={
        "eo:cloud_cover": {
            "lte": max_cloud_cover
        }
    },
)

items = list(search.items())
if not items:
    raise RuntimeError("No Sentinel-2 L2A scenes found.")

# select scene with lowest cloud cover
items.sort(key=lambda item: item.properties.get("eo:cloud_cover", 100))
scene = items[0]

# get access token
username = os.getenv("CDSE_USERNAME")
password = os.getenv("CDSE_PASSWORD")

if not username or not password:
    raise RuntimeError("CDSE_USERNAME and CDSE_PASSWORD must be set")

auth_url = (
    "https://identity.dataspace.copernicus.eu/"
    "auth/realms/CDSE/protocol/openid-connect/token"
)

response = requests.post(
    auth_url,
    data={
        "client_id": "cdse-public",
        "grant_type": "password",
        "username": username,
        "password": password,
    },
)

response.raise_for_status()
access_token = response.json()["access_token"]
print("Authentication successful!")

# get product id
url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
params = {
    "$filter": f"contains(Name, '{scene.id}')",
    "$top": 10
}

response = requests.get(url, params=params)

print("Status:", response.status_code)
print(response.url)

data = response.json()

print("\nNumber of products:", len(data["value"]))

for product in data["value"]:
    print(product["Id"])
    print(product["Name"])
    print()

product_id = product["Id"]

# download product
download_url = (
    f"https://download.dataspace.copernicus.eu/odata/v1/"
    f"Products({product_id})/$value"
)

print(download_url)

headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(
    download_url,
    headers=headers,
    stream=True,
    timeout=120
)
response.raise_for_status()

downloaded_product = r"data/scene.zip"

with open(downloaded_product, "wb") as f:
    for chunk in response.iter_content(chunk_size=1024 * 1024):
        if chunk:
            f.write(chunk)
print("Download complete.")

# extract required bands
scene_dir = data_dir / scene.id
scene_dir.mkdir(parents=True, exist_ok=True)

to_extract = [
    "_B01_60m.jp2",
    "_B02_10m.jp2",
    "_B03_10m.jp2",
    "_B04_10m.jp2",
    "_B05_20m.jp2",
    "_B06_20m.jp2",
    "_B07_20m.jp2",
    "_B08_10m.jp2",
    "_B8A_20m.jp2",
    "_B09_60m.jp2",
    "_B11_20m.jp2",
    "_B12_20m.jp2",
    "_SCL_20m.jp2",
]

with zipfile.ZipFile(downloaded_product, "r") as z:
    for member in z.namelist():
        if member.endswith("/"):
            continue
        filename = Path(member).name
        if any(filename.endswith(f"{pattern}") for pattern in to_extract):
            print("Extracting: ", member)
            with z.open(member) as source:
                with open(scene_dir / filename, "wb") as target:
                    target.write(source.read())
