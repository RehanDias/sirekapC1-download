import os
import urllib.request
import json
import time
from urllib.parse import urlparse

# Add safe URL opener setup
def create_safe_opener():
    """Create URL opener that only allows HTTP/HTTPS schemes"""
    opener = urllib.request.build_opener(
        urllib.request.HTTPHandler(),
        urllib.request.HTTPSHandler()
    )
    return opener

# Create global safe opener
safe_opener = create_safe_opener()

class ImageDownloader:
    def __init__(self, base_path):
        self.base_path = base_path
        self.opener = safe_opener

    def is_valid_url(self, url):
        """Validate if URL uses HTTPS scheme"""
        parsed = urlparse(url)
        return parsed.scheme == 'https' and parsed.netloc.endswith('kpu.go.id')

    def download_image_with_retry(self, image_url, image_path):
        if not self.is_valid_url(image_url):
            print(f"Invalid URL scheme or domain: {image_url}")
            return

        max_retries = 3
        retries = 0

        while retries < max_retries:
            try:
                # Replace urlretrieve with safe download
                with self.opener.open(image_url) as response:
                    with open(image_path, 'wb') as f:
                        f.write(response.read())
                print(f"Gambar berhasil diunduh dari {image_url}")
                return
            except Exception as e:
                print(f"Error saat mengunduh gambar dari {image_url}: {e}")
                retries += 1

        print(f"Gagal mengunduh gambar setelah {max_retries} percobaan")

    def download_images_sequentially(self, image_urls, folder_path, tps_name):
        # Unduh setiap gambar dalam daftar secara berurutan
        for i, image_url in enumerate(image_urls):
            if not image_url:
                print(f"URL gambar kosong untuk TPS {tps_name}")
                continue

            # Generate nama dan path gambar
            image_extension = os.path.splitext(image_url)[1]
            image_name = f"{tps_name}-{i}{image_extension}"
            image_path = os.path.join(folder_path, image_name)

            try:
                # Coba unduh gambar dengan percobaan
                self.download_image_with_retry(image_url, image_path)
            except Exception as e:
                print(f"Error saat mengunduh gambar dari {image_url}: {e}")

class DataFetcher:
    def __init__(self, base_path):
        self.base_path = base_path
        self.downloader = ImageDownloader(base_path)
        self.base_api_url = "https://sirekap-obj-data.kpu.go.id"
        self.opener = safe_opener

    def is_valid_url(self, url):
        """Validate if URL uses HTTPS scheme"""
        parsed = urlparse(url)
        return parsed.scheme == 'https' and parsed.netloc.endswith('kpu.go.id')

    def safe_urlopen(self, url):
        """Safely open URLs after validation"""
        if not self.is_valid_url(url):
            raise ValueError(f"Invalid URL scheme or domain: {url}")
        return self.opener.open(url)

    def fetch_data(self):
        try:
            api_url = f"{self.base_api_url}/wilayah/pemilu/pdpr/0.json"
            with self.safe_urlopen(api_url) as response:
                provinsi_data = json.loads(response.read())

                for provinsi in provinsi_data:
                    provinsi_folder = os.path.join(self.base_path, provinsi["nama"])
                    os.makedirs(provinsi_folder, exist_ok=True)

                    self.fetch_kabupaten_data(provinsi_folder, provinsi)

        except urllib.error.URLError as e:
            # Penanganan kesalahan URL
            print("URLError: Gagal mengambil data:", e.reason)
            print("Mencoba lagi dalam 5 detik...")
            time.sleep(5)
            self.fetch_data()  # Coba lagi

        except Exception as e:
            # Penanganan kesalahan lainnya
            print("Error saat mengambil data:", e)

        except KeyboardInterrupt:
            # Penanganan interrupt keyboard
            print("Proses dihentikan oleh pengguna.")

    def fetch_kabupaten_data(self, provinsi_folder, provinsi):
        api_url = f"{self.base_api_url}/wilayah/pemilu/ppwp/{provinsi['kode']}.json"
        with self.safe_urlopen(api_url) as response_kabupaten:
            kabupaten_data = json.loads(response_kabupaten.read())

            for kabupaten in kabupaten_data:
                kabupaten_folder = os.path.join(provinsi_folder, kabupaten["nama"])
                os.makedirs(kabupaten_folder, exist_ok=True)

                self.fetch_kecamatan_data(kabupaten_folder, provinsi['kode'], kabupaten)

    def fetch_kecamatan_data(self, kabupaten_folder, provinsi_kode, kabupaten):
        api_url = f"{self.base_api_url}/wilayah/pemilu/ppwp/{provinsi_kode}/{kabupaten['kode']}.json"
        with self.safe_urlopen(api_url) as response_kecamatan:
            kecamatan_data = json.loads(response_kecamatan.read())

            for kecamatan in kecamatan_data:
                kecamatan_folder = os.path.join(kabupaten_folder, kecamatan["nama"])
                os.makedirs(kecamatan_folder, exist_ok=True)

                self.fetch_kelurahan_data(kecamatan_folder, provinsi_kode, kabupaten['kode'], kecamatan)

    def fetch_kelurahan_data(self, kecamatan_folder, provinsi_kode, kabupaten_kode, kecamatan):
        api_url = f"{self.base_api_url}/wilayah/pemilu/ppwp/{provinsi_kode}/{kabupaten_kode}/{kecamatan['kode']}.json"
        with self.safe_urlopen(api_url) as response_kelurahan:
            kelurahan_data = json.loads(response_kelurahan.read())

            for kelurahan in kelurahan_data:
                kelurahan_folder = os.path.join(kecamatan_folder, kelurahan["nama"])
                os.makedirs(kelurahan_folder, exist_ok=True)

                self.fetch_tps_data(kelurahan_folder, provinsi_kode, kabupaten_kode, kecamatan['kode'], kelurahan)

    def fetch_tps_data(self, kelurahan_folder, provinsi_kode, kabupaten_kode, kecamatan_kode, kelurahan):
        api_url = f"{self.base_api_url}/wilayah/pemilu/ppwp/{provinsi_kode}/{kabupaten_kode}/{kecamatan_kode}/{kelurahan['kode']}.json"
        with self.safe_urlopen(api_url) as response_tps:
            tps_data = json.loads(response_tps.read())

            for tps in tps_data:
                detail_url = f"{self.base_api_url}/pemilu/hhcw/pdpr/{provinsi_kode}/{kabupaten_kode}/{kecamatan_kode}/{kelurahan['kode']}/{tps['kode']}.json"
                with self.safe_urlopen(detail_url) as response_tps_detail:
                    tps_detail_data = json.loads(response_tps_detail.read())
                    image_urls = tps_detail_data.get("images", [])
                    self.downloader.download_images_sequentially(image_urls, kelurahan_folder, tps['nama'])

# Penggunaan
base_path = "./C-FORM"
data_fetcher = DataFetcher(base_path)
data_fetcher.fetch_data()
