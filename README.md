# 💊 Kimia Farma Data Warehouse & Business Intelligence Platform

## 📌 Deskripsi Proyek

Proyek ini merupakan implementasi **Data Warehouse** dan **Business Intelligence Dashboard** untuk analisis data operasional Kimia Farma menggunakan pendekatan **ELT (Extract, Load, Transform)** dan model dimensional **Star Schema OLAP**.

Data operasional diekstraksi menggunakan Python, dimuat ke **Supabase PostgreSQL**, ditransformasikan menjadi tabel dimensi dan fakta menggunakan SQL, kemudian disajikan melalui dashboard interaktif berbasis **Streamlit** untuk mendukung pengambilan keputusan bisnis berbasis data.

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
    ▼
Streamlit Dashboard
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
| Dashboard            | Streamlit        |
| Database             | PostgreSQL       |
| Cloud Database       | Supabase         |
| Data Processing      | Pandas           |
| Database Connection  | SQLAlchemy       |
| Visualization        | Plotly           |
| Data Modeling        | Star Schema OLAP |

---

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

## ☁️ Deployment ke Streamlit Cloud

1. Push project ke GitHub
2. Deploy repository melalui Streamlit Community Cloud
3. Buka **App Settings → Secrets**
4. Tambahkan konfigurasi berikut:

```toml
DB_URL = "postgresql://username:password@host:5432/database"
```

> File `.streamlit/secrets.toml` **tidak perlu dan tidak boleh diunggah ke GitHub** karena berisi kredensial database.

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

**Mata Kuliah:** Praktikum Perancangan Data Warehouse & Business Intelligence

**Program Studi:** Teknik Informatika / Ilmu Komputer

**Institusi:** Universitas Padjadjaran

---

## 👥 Tim Pengembang

* Fadhila Latsa Tsabita — Lead Data Engineer
* Anggota Kelompok
