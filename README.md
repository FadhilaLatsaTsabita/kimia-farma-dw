# 💊 Kimia Farma Data Warehouse & Business Intelligence Platform

## 📌 Deskripsi Proyek

Proyek ini merupakan implementasi **Data Warehouse** dan **Business Intelligence Platform** untuk analisis data operasional Kimia Farma menggunakan pendekatan **ELT (Extract, Load, Transform)** dan model dimensional **Star Schema OLAP**.

> ⚠️ **Catatan Penting Mengenai Dataset:**
> Dikarenakan data operasional asli perusahaan bersifat rahasia (*confidential*), seluruh data yang digunakan dalam proyek ini adalah **dataset dummy/sintetis**. Data ini dibangkitkan secara khusus menggunakan Python dengan karakteristik dan distribusi yang dirancang sedemikian rupa agar mendekati pola data operasional riil pada salah satu farmasi di Indonesia.

Data operasional tiruan tersebut diekstraksi menggunakan Python, dimuat ke **Supabase PostgreSQL**, ditransformasikan menjadi tabel dimensi dan fakta menggunakan SQL. Hasil transformasi disajikan secara interaktif untuk mendukung simulasi pengambilan keputusan bisnis berbasis data melalui dua platform visualisasi:
*   📊 **Power BI Dashboard (Utama):** Dashboard produksi utama dengan analisis mendalam, pemodelan data tingkat lanjut, dan visualisasi interaktif yang komprehensif.
*   🌐 **Streamlit Dashboard (Alternatif):** Dashboard berbasis web Python yang berfungsi sebagai platform alternatif yang ringan dan portabel.

---

## 🏗️ Arsitektur Sistem

```text
Raw Data
    │
    ▼
Extract Layer (Python)
    │
    ▼
Staging Tables (Supabase PostgreSQL)
    │
    ▼
Transform Layer (SQL)
    │
    ▼
Star Schema Data Warehouse
    │
    ├── Fact Table
    └── Dimension Tables
    │
    ▼
Analytical View
    │
    ├───► Power BI Dashboard (Main Platform)
    │
    └───► Streamlit Dashboard (Alternative Web)
```

---

## 📂 Struktur Proyek

```text
kimia-farma-dw/
│
├── .streamlit/
│   └── secrets.toml
│
├── data/
│
├── reports/
│   └── dashboard.pbix
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   └── app.py
│
├── sql/
│   ├── schema.sql
│   ├── transform.sql
│   └── views.sql
│
├── requirements.txt
└── README.md
```

---

## 🗄️ Data Warehouse Design

### Fact Table

* `fact_penjualan`

### Dimension Tables

* `dim_produk`
* `dim_apotek`
* `dim_pelanggan`
* `dim_karyawan`
* `dim_supplier`
* `dim_waktu`

### Analytical View

* `v_analitik_penjualan`

---

## 📊 Dashboard Features

### Executive KPI

* Total Revenue
* Total Profit
* Total Product Sold
* Total Transactions

### Business Insights

1. Pola Pembelian Kelompok Lansia Pengguna BPJS
2. Margin Keuntungan per Tipe Cabang
3. Top Supplier Penyumbang Profit Tertinggi
4. Tren Revenue Bulanan Multi-Tahun
5. Top Produk Penyumbang Revenue Terbesar
6. Distribusi Revenue per Kota Apotek

---

## ⚙️ Teknologi yang Digunakan

| Komponen             | Teknologi        |
| -------------------- | ---------------- |
| Programming Language | Python           |
| Main Dashboard       | Power BI         |
| Alternatif Dashboard | Streamlit        |
| Database             | PostgreSQL       |
| Cloud Database       | Supabase         |
| Data Processing      | Pandas           |
| Database Connection  | SQLAlchemy       |
| Visualization        | Plotly           |
| Data Modeling        | Star Schema OLAP |

---

## 🚀 Akses Dashboard & Deployment

### 1. Dashboard Utama (Power BI)
Dashboard utama dapat diakses langsung melalui file Microsoft Power BI yang berada di folder reports/dashboard.pbix

### 2. Dashboard Alternatif (Streamlit)
Aplikasi telah berhasil di-deploy menggunakan Streamlit Community Cloud dan dapat diakses melalui:

🔗 https://kimia-farma-dw.streamlit.app/


## 🚀 Menjalankan Proyek Secara Lokal

### 1. Clone Repository

```bash
git clone https://github.com/username/kimia-farma-dw.git
cd kimia-farma-dw
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Konfigurasi Secrets

Buat folder:

```text
.streamlit/
```

Kemudian buat file:

```text
.streamlit/secrets.toml
```

Isi dengan:

```toml
DB_URL = "postgresql://username:password@host:5432/database"
```

### 4. Jalankan Dashboard

```bash
streamlit run src/app.py
```

---

## 📈 Business Intelligence Objectives

Dashboard ini dirancang untuk membantu analisis:

* Performa penjualan dan profit perusahaan
* Pola pembelian berdasarkan karakteristik pelanggan
* Kontribusi supplier terhadap profit
* Tren pendapatan dari waktu ke waktu
* Produk dengan performa terbaik
* Distribusi pendapatan antar wilayah

---

## 🎓 Informasi Akademik

**Mata Kuliah:** Data Warehouse 

**Program Studi:** Teknik Informatika 

**Institusi:** Universitas Padjadjaran

---

## 👥 Tim Pengembang

* Fadhila Latsa Tsabita — 140810230005
* Adelia Felisha Putri — 140810230003
* Muhammad Ainur Rafiq Noantaria — 140810230009
