
# SIREKAP C1-Form Image Downloader 📷

This repository contains scripts to fetch and download Form C1 images from the Indonesian General Election Commission (KPU) API. The provided scripts are available in both JavaScript (Node.js) and Python.

## Table of Contents 📜

- [Introduction](?tab=readme-ov-file#introduction-ℹ️)
- [Prerequisites](?tab=readme-ov-file#prerequisites-️)
- [Setup](?tab=readme-ov-file#setup-️)
- [Usage](?tab=readme-ov-file#usage-)
  - [JavaScript (Node.js)](?tab=readme-ov-file#javascript-nodejs-)
  - [Python](?tab=readme-ov-file#python-)
- [Differences](?tab=readme-ov-file#differences-)
- [JavaScript Code Overview](?tab=readme-ov-file#javascript-code-overview-)
- [Python Code Overview](?tab=readme-ov-file#python-code-overview-)
- [Contributing](?tab=readme-ov-file#contributing-)
- [License](?tab=readme-ov-file#license-)



## Introduction ℹ️

The Indonesian General Election Commission (KPU) provides an API that allows access to election-related data, including Form C1 images. This repository contains scripts to fetch data from the KPU API and download Form C1 images sequentially.

## Prerequisites 🛠️

Ensure that you have the following software installed on your system:

- [Node.js](https://nodejs.org/) (for JavaScript script)
- [Python](https://www.python.org/) (for Python script)

## Setup ⚙️

1. Clone the repository to your local machine:

```bash
git clone https://github.com/RehanDias/sirekapC1-download.git
```

2. Navigate to the repository directory:

```bash
cd sirekapC1-download
```

3. Install dependencies for the JavaScript script if you want to run the JavaScript file:

```bash
npm install axios
```

No additional dependencies are required for the Python script.

## Usage ▶️

### JavaScript (Node.js) 🟢

The JavaScript script (`sirekap-v.js`) fetches data from the KPU API and downloads Form C1 images sequentially.

1. Run the script using the following command:

```bash
node sirekap-v.js
```

2. The script will create directories for each administrative division (province, regency/municipality, district, village), fetch the necessary data from the KPU API, and download the Form C1 images into their respective folders.

### Python 🐍

The Python script (`sirekap-v.py`) also fetches data from the KPU API and downloads Form C1 images sequentially.

1. Run the script using the following command:

```bash
python sirekap-v.py
```

2. The script performs similar operations as the JavaScript script, creating directories for administrative divisions, fetching data from the KPU API, and downloading the Form C1 images.

## Differences ↔️

While both scripts achieve the same goal of fetching and downloading Form C1 images from the KPU API, there are some differences in their implementation:

- **Language**: The JavaScript script is written in Node.js, while the Python script is written in Python.
- **Dependencies**: The JavaScript script requires the `axios` library for making HTTP requests, while the Python script uses built-in libraries such as `urllib.request` for the same purpose.
- **Error Handling**: Error handling mechanisms may vary between the two scripts due to differences in language constructs and libraries used.

## JavaScript Code Overview 📋

The JavaScript script (`sirekap-v.js`) consists of the following main components:

1. **ImageDownloader Class**: Manages the downloading of images from URLs with retry mechanisms.
2. **DataFetcher Class**: Fetches data from the KPU API and downloads images sequentially for administrative divisions.
3. **Main Execution**: The `fetchData()` function initiates the data fetching and image downloading process.

## Python Code Overview 🐍

The Python script (`sirekap-v.py`) comprises the following main components:

1. **ImageDownloader Class**: Manages image downloading with retry mechanisms.
2. **DataFetcher Class**: Fetches data from the KPU API and downloads images sequentially for administrative divisions.
3. **Main Execution**: The `fetch_data()` function starts the data fetching and image downloading process.

## Contributing 🤝

Contributions are welcome! Feel free to submit pull requests or open issues for any improvements or bug fixes.

## License 📝

This project is licensed under the [MIT License](LICENSE).
