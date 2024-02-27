const axios = require("axios");
const fs = require("fs");
const path = require("path");

class ImageDownloader {
    constructor(basePath) {
        this.basePath = basePath;
    }

    async downloadImage(imageUrl, imagePath) {
        try {
            // Mengunduh gambar dari URL dan menyimpannya ke file
            const response = await axios.get(imageUrl, {
                responseType: "stream"
            });
            const writer = fs.createWriteStream(imagePath);
            response.data.pipe(writer);
            await new Promise((resolve, reject) => {
                writer.on("finish", resolve);
                writer.on("error", reject);
            });
            console.log(`Image downloaded successfully from ${imageUrl}`);
            return true;
        } catch (error) {
            console.error(`Error downloading image from ${imageUrl}:`, error);
            return false;
        }
    }

    async downloadImagesSequentially(imageUrls, folderPath, tps) {
        for (let i = 0; i < imageUrls.length; i++) {
            const imageUrl = imageUrls[i];
            if (!imageUrl) {
                // Menampilkan pesan jika URL gambar null
                console.error(`Null image URL for TPS ${tps.kode}`);
                continue;
            }
            const imageExtension = path.extname(imageUrl);
            const imageName = `${tps.nama}-${i}${imageExtension}`;
            const imagePath = path.join(folderPath, imageName);
            await this.downloadImage(imageUrl, imagePath);
        }
    }
}

class DataFetcher {
    constructor(basePath) {
        this.basePath = basePath;
        this.imageDownloader = new ImageDownloader(basePath);
    }

    async fetchData() {
        try {
            // Mengambil data pemilu nasional
            const nationalUrl =
                "https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/pdpr/0.json";
            const nationalResponse = await axios.get(nationalUrl);
            const provinces = nationalResponse.data;

            // Loop melalui setiap provinsi
            for (const province of provinces) {
                const provinceFolder = path.join(this.basePath, province.nama);
                // Membuat folder untuk setiap provinsi
                fs.mkdirSync(provinceFolder, {
                    recursive: true
                });
                await this.fetchProvinceData(province, provinceFolder);
            }
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    }

    async fetchProvinceData(province, provinceFolder) {
        try {
            // Mengambil data kabupaten/kota dari suatu provinsi
            const districtUrl = `https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/${province.kode}.json`;
            const districtResponse = await axios.get(districtUrl);
            const districts = districtResponse.data;

            // Loop melalui setiap kabupaten/kota
            for (const district of districts) {
                const districtFolder = path.join(provinceFolder, district.nama);
                // Membuat folder untuk setiap kabupaten/kota
                fs.mkdirSync(districtFolder, {
                    recursive: true
                });
                await this.fetchDistrictData(province.kode, district, districtFolder);
            }
        } catch (error) {
            console.error("Error fetching district data:", error);
        }
    }

    async fetchDistrictData(provinceCode, district, districtFolder) {
        try {
            // Mengambil data kecamatan dari suatu kabupaten/kota
            const subDistrictUrl = `https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/${provinceCode}/${district.kode}.json`;
            const subDistrictResponse = await axios.get(subDistrictUrl);
            const subDistricts = subDistrictResponse.data;

            // Loop melalui setiap kecamatan
            for (const subDistrict of subDistricts) {
                const subDistrictFolder = path.join(districtFolder, subDistrict.nama);
                // Membuat folder untuk setiap kecamatan
                fs.mkdirSync(subDistrictFolder, {
                    recursive: true
                });
                await this.fetchSubDistrictData(
                    provinceCode,
                    district.kode,
                    subDistrict,
                    subDistrictFolder
                );
            }
        } catch (error) {
            console.error("Error fetching sub-district data:", error);
        }
    }

    async fetchSubDistrictData(
        provinceCode,
        districtCode,
        subDistrict,
        subDistrictFolder
    ) {
        try {
            // Mengambil data desa/kelurahan dari suatu kecamatan
            const villageUrl = `https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/${provinceCode}/${districtCode}/${subDistrict.kode}.json`;
            const villageResponse = await axios.get(villageUrl);
            const villages = villageResponse.data;

            // Loop melalui setiap desa/kelurahan
            for (const village of villages) {
                const villageFolder = path.join(subDistrictFolder, village.nama);
                // Membuat folder untuk setiap desa/kelurahan
                fs.mkdirSync(villageFolder, {
                    recursive: true
                });
                await this.fetchVillageData(
                    provinceCode,
                    districtCode,
                    subDistrict.kode,
                    village,
                    villageFolder
                );
            }
        } catch (error) {
            console.error("Error fetching village data:", error);
        }
    }

    async fetchVillageData(
        provinceCode,
        districtCode,
        subDistrictCode,
        village,
        villageFolder
    ) {
        try {
            // Mengambil data TPS (Tempat Pemungutan Suara) dari suatu desa/kelurahan
            const tpsUrl = `https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/${provinceCode}/${districtCode}/${subDistrictCode}/${village.kode}.json`;
            const tpsResponse = await axios.get(tpsUrl);
            const tpsData = tpsResponse.data;

            // Loop melalui setiap TPS
            for (const tps of tpsData) {
                // Mengambil detail TPS
                const tpsDetailUrl = `https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/pdpr/${provinceCode}/${districtCode}/${subDistrictCode}/${village.kode}/${tps.kode}.json`;
                const tpsDetailResponse = await axios.get(tpsDetailUrl);
                const tpsDetailData = tpsDetailResponse.data;
                const imageUrls = tpsDetailData.images;

                // Mengunduh gambar-gambar TPS secara berurutan
                await this.imageDownloader.downloadImagesSequentially(
                    imageUrls,
                    villageFolder,
                    tps
                );
            }
        } catch (error) {
            console.error("Error fetching TPS data:", error);
        }
    }
}

// Gunakan kelas DataFetcher untuk memulai pengambilan data dan pengunduhan gambar
const dataFetcher = new DataFetcher("./C-FORM");
dataFetcher.fetchData();
