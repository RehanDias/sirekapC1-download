
# Sirekap C1 Image Downloader

This repository contains scripts to fetch and download Form C1 images from the Indonesian General Election Commission (KPU) API. The provided scripts are available in both JavaScript (Node.js) and Python.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
  - [JavaScript (Node.js)](#javascript-nodejs)
  - [Python](#python)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Indonesian General Election Commission (KPU) provides an API that allows access to election-related data, including Form C1 images. This repository contains scripts to fetch data from the KPU API and download Form C1 images sequentially.

## Prerequisites

Ensure that you have the following software installed on your system:

- [Node.js](https://nodejs.org/) (for JavaScript script)
- [Python](https://www.python.org/) (for Python script)

## Setup

1. Clone the repository to your local machine:

```bash
git clone https://github.com/RehanDias/sirekapC1-download.git
```

2. Navigate to the repository directory:

```bash
cd sirekapC1-download
```

3. Install dependencies for the JavaScript script:

```bash
npm install axios
```

No additional dependencies are required for the Python script.

## Usage

### JavaScript (Node.js)

The JavaScript script (`sirekap-v.js`) fetches data from the KPU API and downloads Form C1 images sequentially.

1. Run the script using the following command:

```bash
node sirekap-v.js
```

2. The script will create directories for each administrative division (province, regency/municipality, district, village), fetch the necessary data from the KPU API, and download the Form C1 images into their respective folders.

### Python

The Python script (`sirekap-v.py`) also fetches data from the KPU API and downloads Form C1 images sequentially.

1. Run the script using the following command:

```bash
python sirekap-v.py
```

2. The script performs similar operations as the JavaScript script, creating directories for administrative divisions, fetching data from the KPU API, and downloading the Form C1 images.

## Contributing

Contributions are welcome! Feel free to submit pull requests or open issues for any improvements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).
