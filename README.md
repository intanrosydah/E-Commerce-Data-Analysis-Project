# Proyek Analisis Data E-Commerce ✨

## Deskripsi Proyek

Proyek ini merupakan analisis data pada dataset Brazilian E-Commerce Public Dataset untuk mengetahui tren penjualan, performa revenue, persebaran pelanggan, serta segmentasi pelanggan menggunakan metode RFM Analysis.

Project ini dibuat sebagai submission kelas **Belajar Analisis Data dengan Python - Dicoding**.


## Struktur Folder

```bash
E-Commerce-Data-Analysis-Project/
│── dashboard/
│   └── dashboard.py
│── data/
│   └── all_data.csv
│── Proyek_Analisis_Data.ipynb
│── requirements.txt
│── README.md
│── url.txt
````

---

## Pertanyaan Bisnis

1. Bagaimana tren bulanan jumlah order dan total revenue periode Januari 2017 - Agustus 2018?
2. Provinsi mana yang memiliki total revenue tertinggi pada tahun 2018?
3. Bagaimana segmentasi pelanggan berdasarkan skor RFM?
4. Bagaimana persebaran revenue antar provinsi di Brasil?
5. Bagaimana pengelompokan pelanggan berdasarkan total spending?

---

## Setup Environment

### Menggunakan Anaconda

```bash
conda create --name main-ds python=3.10
conda activate main-ds
pip install -r requirements.txt
```

### Menggunakan PIP

```bash
pip install -r requirements.txt
```

---

## Menjalankan Dashboard Streamlit

```bash
cd dashboard
streamlit run dashboard.py
```

---

## Hasil Analisis

Dashboard menampilkan:

* Total Orders
* Total Revenue
* Tren Penjualan Bulanan
* Revenue per Provinsi
* Segmentasi Customer RFM
* Customer Spending Group

---

## Author

Aulia Intan Rosydah
S1 Sistem Informasi - Universitas Negeri Surabaya

```
