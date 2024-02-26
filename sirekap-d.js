const axios = require("axios");
const fs = require("fs");
const path = require("path");

const basePath = "./C-FORM"; // Path base FOLDER

// Fungsi untuk mengunduh gambar dengan percobaan ulang
async function downloadImageWithRetry(imageUrl, imagePath) {
  const maxRetries = 3; // Jumlah maksimum percobaan
  let retries = 0;

  while (retries < maxRetries) {
    try {
      // Mengunduh gambar menggunakan Axios
      const imageResponse = await axios({
        url: imageUrl,
        method: "GET",
        responseType: "stream",
      });

      // Menulis gambar ke dalam file
      const writer = fs.createWriteStream(imagePath);
      imageResponse.data.pipe(writer);

      // Menunggu sampai penulisan selesai
      await new Promise((resolve, reject) => {
        writer.on("finish", resolve);
        writer.on("error", reject);
      });

      console.log(`Image downloaded successfully from ${imageUrl}`);
      return; // Keluar dari loop jika berhasil
    } catch (error) {
      console.error(`Error downloading image from ${imageUrl}:`, error);
      retries++; // Meningkatkan jumlah percobaan
    }
  }

  console.error(`Failed to download image after ${maxRetries} retries`);
}

// Fungsi untuk mengunduh gambar secara berurutan
async function downloadImagesSequentially(imageUrls, kelurahanFolder, tps) {
  for (let i = 0; i < imageUrls.length; i++) {
    const imageUrl = imageUrls[i];
    if (!imageUrl) {
      console.error(`Null image URL for TPS ${tps.kode}`);
      continue;
    }
    // Mendapatkan ekstensi gambar dan nama file
    const imageExtension = path.extname(imageUrl);
    const imageName = `${tps.nama}-${i}${imageExtension}`;
    const imagePath = path.join(kelurahanFolder, imageName);

    try {
      await downloadImageWithRetry(imageUrl, imagePath);
    } catch (error) {
      console.error(`Error downloading image from ${imageUrl}:`, error);
    }
  }
}

// Fungsi untuk mengambil data dari API dan mengunduh gambar
async function fetchData() {
  try {
    const nasionalUrl =
      "https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/pdpr/0.json";
    const responNasional = await axios.get(nasionalUrl);
    const provinsiData = responNasional.data;

    // Looping provinsi
    for (const provinsi of provinsiData) {
      const provinsiFolder = path.join(basePath, provinsi.nama);
      fs.mkdirSync(provinsiFolder, { recursive: true });

      const kabupatenUrl = `https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/${provinsi.kode}.json`;
      const responseKabupaten = await axios.get(kabupatenUrl);
      const kabupatenData = responseKabupaten.data;

      // Looping kabupaten
      for (const kabupaten of kabupatenData) {
        const kabupatenFolder = path.join(provinsiFolder, kabupaten.nama);
        fs.mkdirSync(kabupatenFolder, { recursive: true });

        const kecamatanUrl = `https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/${provinsi.kode}/${kabupaten.kode}.json`;
        const responseKecamatan = await axios.get(kecamatanUrl);
        const kecamatanData = responseKecamatan.data;

        // Looping kecamatan
        for (const kecamatan of kecamatanData) {
          const kecamatanFolder = path.join(kabupatenFolder, kecamatan.nama);
          fs.mkdirSync(kecamatanFolder, { recursive: true });

          const kelurahanUrl = `https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/${provinsi.kode}/${kabupaten.kode}/${kecamatan.kode}.json`;
          const responseKelurahan = await axios.get(kelurahanUrl);
          const kelurahanData = responseKelurahan.data;

          // Looping kelurahan
          for (const kelurahan of kelurahanData) {
            const kelurahanFolder = path.join(kecamatanFolder, kelurahan.nama);
            fs.mkdirSync(kelurahanFolder, { recursive: true });

            const tpsUrl = `https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/${provinsi.kode}/${kabupaten.kode}/${kecamatan.kode}/${kelurahan.kode}.json`;
            const responseTps = await axios.get(tpsUrl);
            const tpsData = responseTps.data;

            // Looping TPS
            for (const tps of tpsData) {
              const tpsDetailUrl = `https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/pdpr/${provinsi.kode}/${kabupaten.kode}/${kecamatan.kode}/${kelurahan.kode}/${tps.kode}.json`;
              const responseTpsDetail = await axios.get(tpsDetailUrl);
              const tpsDetailData = responseTpsDetail.data;

              const imageUrls = tpsDetailData.images;
              await downloadImagesSequentially(imageUrls, kelurahanFolder, tps);
            }
          }
        }
      }
    }
  } catch (error) {
    console.error("Error fetching data:", error);
  }
}

// Memulai proses pengambilan data dan pengunduhan gambar
fetchData();
