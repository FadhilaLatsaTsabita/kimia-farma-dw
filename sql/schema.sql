-- HAPUS TABEL LAMA JIKA ADA (UNTUK RESET SKEMA)
DROP TABLE IF EXISTS fact_penjualan CASCADE;
DROP TABLE IF EXISTS dim_produk CASCADE;
DROP TABLE IF EXISTS dim_apotek CASCADE;
DROP TABLE IF EXISTS dim_pelanggan CASCADE;
DROP TABLE IF EXISTS dim_karyawan CASCADE;
DROP TABLE IF EXISTS dim_supplier CASCADE;
DROP TABLE IF EXISTS dim_waktu CASCADE;

-- 1. MEMBUAT TABEL DIMENSI PRODUK
CREATE TABLE dim_produk (
    produkid VARCHAR(50) PRIMARY KEY,
    kodeproduk VARCHAR(50),
    namaproduk VARCHAR(255),
    kategoriproduk VARCHAR(100),
    jenisproduk VARCHAR(100),
    brand VARCHAR(100),
    supplierid VARCHAR(50),
    hargamodal NUMERIC(15, 2)
);

-- 2. MEMBUAT TABEL DIMENSI APOTEK
CREATE TABLE dim_apotek (
    apotekid VARCHAR(50) PRIMARY KEY,
    kodeapotek VARCHAR(50),
    namaapotek VARCHAR(255),
    kota VARCHAR(100),
    provinsi VARCHAR(100),
    wilayah VARCHAR(50),
    tipecabang VARCHAR(100)
);

-- 3. MEMBUAT TABEL DIMENSI PELANGGAN
CREATE TABLE dim_pelanggan (
    pelangganid VARCHAR(50) PRIMARY KEY,
    kodepelanggan VARCHAR(50),
    namapelanggan VARCHAR(255),
    jeniskelamin VARCHAR(20),
    usia INT,
    kelompokusia VARCHAR(50),
    kota VARCHAR(100),
    provinsi VARCHAR(100),
    tipepelanggan VARCHAR(100)
);

-- 4. MEMBUAT TABEL DIMENSI KARYAWAN
CREATE TABLE dim_karyawan (
    karyawanid VARCHAR(50) PRIMARY KEY,
    nik VARCHAR(50),
    namakaryawan VARCHAR(255),
    jabatan VARCHAR(100),
    departemen VARCHAR(100),
    statuskepegawaian VARCHAR(50),
    apotekid VARCHAR(50)
);

-- 5. MEMBUAT TABEL DIMENSI SUPPLIER
CREATE TABLE dim_supplier (
    supplierid VARCHAR(50) PRIMARY KEY,
    namasupplier VARCHAR(255),
    kotasupplier VARCHAR(100)
);

-- 6. MEMBUAT TABEL DIMENSI WAKTU (OLAP)
CREATE TABLE dim_waktu (
    waktuid INT PRIMARY KEY,
    tanggal DATE UNIQUE,
    hari VARCHAR(20),
    bulan VARCHAR(20),
    nomorbulan INT,
    kuartal VARCHAR(10),
    tahun INT
);

-- 7. MEMBUAT TABEL FAKTA PENJUALAN 
CREATE TABLE fact_penjualan (
    factid BIGSERIAL PRIMARY KEY,
    fakturid VARCHAR(50),
    waktuid INT REFERENCES dim_waktu(waktuid),
    apotekid VARCHAR(50) REFERENCES dim_apotek(apotekid),
    produkid VARCHAR(50) REFERENCES dim_produk(produkid),
    pelangganid VARCHAR(50) REFERENCES dim_pelanggan(pelangganid),
    karyawanid VARCHAR(50) REFERENCES dim_karyawan(karyawanid),
    supplierid VARCHAR(50) REFERENCES dim_supplier(supplierid),
    jumlahterjual INT,
    hargasatuan NUMERIC(15,2),
    diskon NUMERIC(15,2),
    totalpenjualan NUMERIC(15,2),
    keuntungan NUMERIC(15,2)
);