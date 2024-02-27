import os
import urllib.request
import json
import time

class ImageDownloader:
    def __init__(self, base_path):
        self.base_path = base_path

    def download_image_with_retry(self, image_url, image_path):
        max_retries = 3
        retries = 0

        # Try downloading the image with retries
        while retries < max_retries:
            try:
                urllib.request.urlretrieve(image_url, image_path)
                print(f"Image downloaded successfully from {image_url}")
                return
            except Exception as e:
                print(f"Error downloading image from {image_url}: {e}")
                retries += 1

        print(f"Failed to download image after {max_retries} retries")

    def download_images_sequentially(self, image_urls, folder_path, tps_name):
        # Download each image in the list sequentially
        for i, image_url in enumerate(image_urls):
            if not image_url:
                print(f"Null image URL for TPS {tps_name}")
                continue

            # Generate image name and path
            image_extension = os.path.splitext(image_url)[1]
            image_name = f"{tps_name}-{i}{image_extension}"
            image_path = os.path.join(folder_path, image_name)

            try:
                # Attempt to download the image with retries
                self.download_image_with_retry(image_url, image_path)
            except Exception as e:
                print(f"Error downloading image from {image_url}: {e}")

class DataFetcher:
    def __init__(self, base_path):
        self.base_path = base_path
        self.downloader = ImageDownloader(base_path)

    def fetch_data(self):
        try:
            # Fetch province data
            with urllib.request.urlopen("https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/pdpr/0.json") as response:
                provinsi_data = json.loads(response.read())

                for provinsi in provinsi_data:
                    provinsi_folder = os.path.join(self.base_path, provinsi["nama"])
                    os.makedirs(provinsi_folder, exist_ok=True)

                    self.fetch_kabupaten_data(provinsi_folder, provinsi)

        except urllib.error.URLError as e:
            # Retry mechanism for URL errors
            print("URLError: Failed to fetch data:", e.reason)
            print("Retrying in 5 seconds...")
            time.sleep(5)
            self.fetch_data()  # Retry

        except Exception as e:
            print("Error fetching data:", e)

    def fetch_kabupaten_data(self, provinsi_folder, provinsi):
        # Fetch district data
        with urllib.request.urlopen(f"https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{provinsi['kode']}.json") as response_kabupaten:
            kabupaten_data = json.loads(response_kabupaten.read())

            for kabupaten in kabupaten_data:
                kabupaten_folder = os.path.join(provinsi_folder, kabupaten["nama"])
                os.makedirs(kabupaten_folder, exist_ok=True)

                self.fetch_kecamatan_data(kabupaten_folder, provinsi['kode'], kabupaten)

    def fetch_kecamatan_data(self, kabupaten_folder, provinsi_kode, kabupaten):
        # Fetch sub-district data
        with urllib.request.urlopen(f"https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{provinsi_kode}/{kabupaten['kode']}.json") as response_kecamatan:
            kecamatan_data = json.loads(response_kecamatan.read())

            for kecamatan in kecamatan_data:
                kecamatan_folder = os.path.join(kabupaten_folder, kecamatan["nama"])
                os.makedirs(kecamatan_folder, exist_ok=True)

                self.fetch_kelurahan_data(kecamatan_folder, provinsi_kode, kabupaten['kode'], kecamatan)

    def fetch_kelurahan_data(self, kecamatan_folder, provinsi_kode, kabupaten_kode, kecamatan):
        # Fetch village data
        with urllib.request.urlopen(f"https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{provinsi_kode}/{kabupaten_kode}/{kecamatan['kode']}.json") as response_kelurahan:
            kelurahan_data = json.loads(response_kelurahan.read())

            for kelurahan in kelurahan_data:
                kelurahan_folder = os.path.join(kecamatan_folder, kelurahan["nama"])
                os.makedirs(kelurahan_folder, exist_ok=True)

                self.fetch_tps_data(kelurahan_folder, provinsi_kode, kabupaten_kode, kecamatan['kode'], kelurahan)

    def fetch_tps_data(self, kelurahan_folder, provinsi_kode, kabupaten_kode, kecamatan_kode, kelurahan):
        # Fetch polling station data
        with urllib.request.urlopen(f"https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{provinsi_kode}/{kabupaten_kode}/{kecamatan_kode}/{kelurahan['kode']}.json") as response_tps:
            tps_data = json.loads(response_tps.read())

            for tps in tps_data:
                with urllib.request.urlopen(f"https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/pdpr/{provinsi_kode}/{kabupaten_kode}/{kecamatan_kode}/{kelurahan['kode']}/{tps['kode']}.json") as response_tps_detail:
                    tps_detail_data = json.loads(response_tps_detail.read())
                    image_urls = tps_detail_data.get("images", [])
                    self.downloader.download_images_sequentially(image_urls, kelurahan_folder, tps['nama'])

# Usage
base_path = "./C-FORM"
data_fetcher = DataFetcher(base_path)
data_fetcher.fetch_data()
