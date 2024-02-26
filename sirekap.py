import os
import urllib.request
import json

base_path = "./C-FORM"  # Path base FOLDER

# Fungsi untuk mengunduh gambar dengan percobaan ulang
def download_image_with_retry(image_url, image_path):
    max_retries = 3  # Jumlah maksimum percobaan
    retries = 0

    while retries < max_retries:
        try:
            # Mengunduh gambar menggunakan urllib
            urllib.request.urlretrieve(image_url, image_path)
            print(f"Image downloaded successfully from {image_url}")
            return  # Keluar dari loop jika berhasil
        except Exception as e:
            print(f"Error downloading image from {image_url}: {e}")
            retries += 1  # Meningkatkan jumlah percobaan

    print(f"Failed to download image after {max_retries} retries")

# Fungsi untuk mengunduh gambar secara berurutan
def download_images_sequentially(image_urls, kelurahan_folder, tps):
    for i, image_url in enumerate(image_urls):
        if not image_url:
            print(f"Null image URL for TPS {tps['kode']}")
            continue
        # Mendapatkan ekstensi gambar dan nama file
        image_extension = os.path.splitext(image_url)[1]
        image_name = f"{tps['nama']}-{i}{image_extension}"
        image_path = os.path.join(kelurahan_folder, image_name)

        try:
            download_image_with_retry(image_url, image_path)
        except Exception as e:
            print(f"Error downloading image from {image_url}: {e}")

# Fungsi untuk mengambil data dari API dan mengunduh gambar
def fetch_data():
    try:
        with urllib.request.urlopen("https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/pdpr/0.json") as response:
            provinsi_data = json.loads(response.read())

            # Looping provinsi
            for provinsi in provinsi_data:
                provinsi_folder = os.path.join(base_path, provinsi["nama"])
                os.makedirs(provinsi_folder, exist_ok=True)

                with urllib.request.urlopen(f"https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{provinsi['kode']}.json") as response_kabupaten:
                    kabupaten_data = json.loads(response_kabupaten.read())

                    # Looping kabupaten
                    for kabupaten in kabupaten_data:
                        kabupaten_folder = os.path.join(provinsi_folder, kabupaten["nama"])
                        os.makedirs(kabupaten_folder, exist_ok=True)

                        with urllib.request.urlopen(f"https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{provinsi['kode']}/{kabupaten['kode']}.json") as response_kecamatan:
                            kecamatan_data = json.loads(response_kecamatan.read())

                            # Looping kecamatan
                            for kecamatan in kecamatan_data:
                                kecamatan_folder = os.path.join(kabupaten_folder, kecamatan["nama"])
                                os.makedirs(kecamatan_folder, exist_ok=True)

                                with urllib.request.urlopen(f"https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{provinsi['kode']}/{kabupaten['kode']}/{kecamatan['kode']}.json") as response_kelurahan:
                                    kelurahan_data = json.loads(response_kelurahan.read())

                                    # Looping kelurahan
                                    for kelurahan in kelurahan_data:
                                        kelurahan_folder = os.path.join(kecamatan_folder, kelurahan["nama"])
                                        os.makedirs(kelurahan_folder, exist_ok=True)

                                        with urllib.request.urlopen(f"https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{provinsi['kode']}/{kabupaten['kode']}/{kecamatan['kode']}/{kelurahan['kode']}.json") as response_tps:
                                            tps_data = json.loads(response_tps.read())

                                            # Looping TPS
                                            for tps in tps_data:
                                                with urllib.request.urlopen(f"https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/pdpr/{provinsi['kode']}/{kabupaten['kode']}/{kecamatan['kode']}/{kelurahan['kode']}/{tps['kode']}.json") as response_tps_detail:
                                                    tps_detail_data = json.loads(response_tps_detail.read())
                                                    image_urls = tps_detail_data.get("images", [])
                                                    download_images_sequentially(image_urls, kelurahan_folder, tps)
    except Exception as e:
        print("Error fetching data:", e)

# Memulai proses pengambilan data dan pengunduhan gambar
fetch_data()
