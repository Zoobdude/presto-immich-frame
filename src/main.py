import time
import jpegdec
from presto import Presto

from immich_connector import ImmichConnector
import secrets

presto = Presto(ambient_light=True, full_res=True)
display = presto.display
WIDTH, HEIGHT = display.get_bounds()
j = jpegdec.JPEG(display)

wifi = presto.connect()


def display_img_file(img_name: str):
    j.open_file(f"{img_name}.jpeg")

    img_height, img_width = j.get_height(), j.get_width()
    img_height = img_height // 4
    img_width = img_width // 4

    img_x = 0
    img_y = 0

    # if the image isn't exactly 240x240 then we'll try to centre the image
    if img_width < WIDTH:
        img_x = (WIDTH // 2) - (img_width // 2)

    if img_height < HEIGHT:
        img_y = (HEIGHT // 2) - (img_height // 2)
    j.decode(img_x, img_y, jpegdec.JPEG_SCALE_QUARTER, dither=True)


def display_img_bytes(img_bytes: bytes):
    j.open_RAM(img_bytes)

    img_height, img_width = j.get_height(), j.get_width()
    img_height = img_height // 4
    img_width = img_width // 4

    img_x = 0
    img_y = 0

    # if the image isn't exactly 240x240 then we'll try to centre the image
    if img_width < WIDTH:
        img_x = (WIDTH // 2) - (img_width // 2)

    if img_height < HEIGHT:
        img_y = (HEIGHT // 2) - (img_height // 2)
    j.decode(img_x, img_y, jpegdec.JPEG_SCALE_QUARTER, dither=True)


def main():
    connector = ImmichConnector(secrets.BASE_URL, secrets.API_KEY)

    print(connector.test_connection())

    current_asset_counter = 0
    while True:
        print("Fetching asset")
        asset = connector.get_asset_from_album(
            "813556ca-3166-40be-8075-4fce01303fe4", current_asset_counter
        )

        print("Downloading asset")
        img = connector.download_asset_to_memory(asset["id"])

        print("Displaying asset")
        presto.clear()
        display_img_bytes(img)
        current_asset_counter += 1
        presto.update()
        
        time.sleep(5)


main()
