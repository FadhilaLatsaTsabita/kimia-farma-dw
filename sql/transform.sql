-- MENGOSONGKAN DATA LAMA SEBELUM PROSES RE-RUN ELT
TRUNCATE TABLE fact_penjualan CASCADE;
TRUNCATE TABLE dim_produk CASCADE;
TRUNCATE TABLE dim_apotek CASCADE;
TRUNCATE TABLE dim_pelanggan CASCADE;
TRUNCATE TABLE dim_karyawan CASCADE;
TRUNCATE TABLE dim_supplier CASCADE;
TRUNCATE TABLE dim_waktu CASCADE;

-- ============================================================================
-- INJEKSI DEFAULT VALUE ('UNKNOWN' / -1) UNTUK MENJAGA INTEGRITAS FK & MENCEGAH DATA DROP
-- ============================================================================
INSERT INTO dim_supplier (supplierid, namasupplier, kotasupplier)
VALUES ('UNKNOWN', 'Unknown Supplier', 'Unknown') ON CONFLICT (supplierid) DO NOTHING;

INSERT INTO dim_produk (produkid, kodeproduk, namaproduk, kategoriproduk, jenisproduk, brand, supplierid, hargamodal)
VALUES ('UNKNOWN', 'UNKNOWN', 'Unknown Product', 'Unknown', 'Unknown', 'Unknown', 'UNKNOWN', 0) ON CONFLICT (produkid) DO NOTHING;

INSERT INTO dim_apotek (apotekid, kodeapotek, namaapotek, kota, provinsi, wilayah, tipecabang)
VALUES ('UNKNOWN', 'UNKNOWN', 'Unknown Apotek', 'Unknown', 'Unknown', 'Unknown', 'Unknown') ON CONFLICT (apotekid) DO NOTHING;

INSERT INTO dim_pelanggan (pelangganid, kodepelanggan, namapelanggan, jeniskelamin, usia, kelompokusia, kota, provinsi, tipepelanggan)
VALUES ('UNKNOWN', 'UNKNOWN', 'Unknown Customer', 'Unknown', 0, 'Unknown', 'Unknown', 'Unknown', 'Unknown') ON CONFLICT (pelangganid) DO NOTHING;

INSERT INTO dim_karyawan (karyawanid, nik, namakaryawan, jabatan, departemen, statuskepegawaian, apotekid)
VALUES ('UNKNOWN', 'UNKNOWN', 'Unknown Karyawan', 'Unknown', 'Unknown', 'Unknown', 'UNKNOWN') ON CONFLICT (karyawanid) DO NOTHING;

INSERT INTO dim_waktu (waktuid, tanggal, hari, bulan, nomorbulan, kuartal, tahun)
VALUES (-1, '1900-01-01', 'Unknown', 'Unknown', 0, 'Q0', 1900) ON CONFLICT (waktuid) DO NOTHING;


-- ============================================================================
-- 1. TRANSFORMASI & PEMBERSIHAN DIM_PRODUK
-- ============================================================================
INSERT INTO dim_produk (produkid, kodeproduk, namaproduk, kategoriproduk, jenisproduk, brand, supplierid, hargamodal)
SELECT DISTINCT
    UPPER(REGEXP_REPLACE(TRIM(produkid), '[-_]', '', 'g')) AS produkid, 
    COALESCE(REGEXP_REPLACE(TRIM(kodeproduk), '[-_]', '', 'g'), 'UNKNOWN') AS kodeproduk,
    COALESCE(INITCAP(TRIM(namaproduk)), 'Unknown Product') AS namaproduk, 
    COALESCE(INITCAP(TRIM(kategoriproduk)), 'Unknown') AS kategoriproduk, 
    COALESCE(INITCAP(TRIM(jenisproduk)), 'Unknown') AS jenisproduk, 
    COALESCE(INITCAP(TRIM(brand)), 'Unknown') AS brand, 
    COALESCE(UPPER(REGEXP_REPLACE(TRIM(supplierid), '[-_]', '', 'g')), 'UNKNOWN') AS supplierid,
    COALESCE(CAST(hargamodal AS NUMERIC), 0) AS hargamodal
FROM stg_produk
WHERE produkid IS NOT NULL AND TRIM(CAST(produkid AS TEXT)) != ''
ON CONFLICT (produkid) DO NOTHING;

-- ============================================================================
-- 2. TRANSFORMASI & PEMBERSIHAN DIM_APOTEK
-- ============================================================================
INSERT INTO dim_apotek (apotekid, kodeapotek, namaapotek, kota, provinsi, wilayah, tipecabang)
SELECT DISTINCT
    UPPER(REGEXP_REPLACE(TRIM(apotekid), '[-_]', '', 'g')) AS apotekid, 
    COALESCE(REGEXP_REPLACE(TRIM(kodeapotek), '[-_]', '', 'g'), 'UNKNOWN') AS kodeapotek,
    COALESCE(INITCAP(TRIM(namaapotek)), 'Unknown Apotek') AS namaapotek, 
    COALESCE(INITCAP(TRIM(kota)), 'Unknown') AS kota, 
    COALESCE(INITCAP(TRIM(provinsi)), 'Unknown') AS provinsi, 
    COALESCE(INITCAP(TRIM(wilayah)), 'Unknown') AS wilayah, 
    COALESCE(INITCAP(TRIM(tipecabang)), 'Unknown') AS tipecabang 
FROM stg_apotek
WHERE apotekid IS NOT NULL AND TRIM(CAST(apotekid AS TEXT)) != ''
ON CONFLICT (apotekid) DO NOTHING;

-- ============================================================================
-- 3. TRANSFORMASI & PEMBERSIHAN DIM_PELANGGAN
-- ============================================================================
WITH cleaned_pelanggan AS (
    SELECT 
        pelangganid,
        kodepelanggan,
        namapelanggan,
        jeniskelamin,
        kelompokusia,
        kota,
        provinsi,
        tipepelanggan,
        CASE 
            WHEN REGEXP_REPLACE(TRIM(CAST(usia AS TEXT)), '[^0-9]', '', 'g') = '' THEN NULL
            ELSE CAST(REGEXP_REPLACE(TRIM(CAST(usia AS TEXT)), '[^0-9]', '', 'g') AS INT)
        END AS usia_cleaned
    FROM stg_pelanggan
    WHERE pelangganid IS NOT NULL AND TRIM(CAST(pelangganid AS TEXT)) != ''
),
median_usia AS (
    SELECT CAST(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY usia_cleaned) AS INT) AS median_val
    FROM cleaned_pelanggan
    WHERE usia_cleaned IS NOT NULL
)
INSERT INTO dim_pelanggan (pelangganid, kodepelanggan, namapelanggan, jeniskelamin, usia, kelompokusia, kota, provinsi, tipepelanggan)
SELECT DISTINCT
    UPPER(REGEXP_REPLACE(TRIM(pelangganid), '[-_]', '', 'g')) AS pelangganid,
    COALESCE(REGEXP_REPLACE(TRIM(kodepelanggan), '[-_]', '', 'g'), 'UNKNOWN') AS kodepelanggan,
    COALESCE(INITCAP(TRIM(namapelanggan)), 'Unknown Customer') AS namapelanggan, 
    COALESCE(INITCAP(TRIM(jeniskelamin)), 'Unknown') AS jeniskelamin, 
    COALESCE(usia_cleaned, (SELECT median_val FROM median_usia), 0) AS usia,
    COALESCE(INITCAP(TRIM(kelompokusia)), 'Unknown') AS kelompokusia, 
    COALESCE(INITCAP(TRIM(kota)), 'Unknown') AS kota, 
    COALESCE(INITCAP(TRIM(provinsi)), 'Unknown') AS provinsi, 
    COALESCE(INITCAP(TRIM(tipepelanggan)), 'Unknown') AS tipepelanggan 
FROM cleaned_pelanggan
ON CONFLICT (pelangganid) DO NOTHING;

-- ============================================================================
-- 4. TRANSFORMASI & PEMBERSIHAN DIM_KARYAWAN
-- ============================================================================
INSERT INTO dim_karyawan (karyawanid, nik, namakaryawan, jabatan, departemen, statuskepegawaian, apotekid)
SELECT DISTINCT
    UPPER(REGEXP_REPLACE(TRIM(karyawanid), '[-_]', '', 'g')) AS karyawanid, 
    COALESCE(TRIM(nik), 'Unknown') AS nik,
    COALESCE(INITCAP(TRIM(namakaryawan)), 'Unknown Karyawan') AS namakaryawan, 
    COALESCE(INITCAP(TRIM(jabatan)), 'Unknown') AS jabatan, 
    COALESCE(INITCAP(TRIM(departemen)), 'Unknown') AS departemen, 
    COALESCE(INITCAP(TRIM(statuskepegawaian)), 'Unknown') AS statuskepegawaian, 
    COALESCE(UPPER(REGEXP_REPLACE(TRIM(apotekid), '[-_]', '', 'g')), 'UNKNOWN') AS apotekid
FROM stg_karyawan
WHERE karyawanid IS NOT NULL AND TRIM(CAST(karyawanid AS TEXT)) != ''
ON CONFLICT (karyawanid) DO NOTHING;

-- ============================================================================
-- 5. TRANSFORMASI & PEMBERSIHAN DIM_SUPPLIER
-- ============================================================================
INSERT INTO dim_supplier (supplierid, namasupplier, kotasupplier)
SELECT DISTINCT
    UPPER(REGEXP_REPLACE(TRIM(supplierid), '[-_]', '', 'g')) AS supplierid, 
    COALESCE(INITCAP(TRIM(namasupplier)), 'Unknown Supplier') AS namasupplier, 
    COALESCE(INITCAP(TRIM(kotasupplier)), 'Unknown') AS kotasupplier 
FROM stg_supplier
WHERE supplierid IS NOT NULL AND TRIM(CAST(supplierid AS TEXT)) != ''
ON CONFLICT (supplierid) DO NOTHING;

-- ============================================================================
-- 6. GENERATE DIM_WAKTU BERDASARKAN TANGGAL TRANSAKSI NYATA (FIXED)
-- ============================================================================
INSERT INTO dim_waktu (waktuid, tanggal, hari, bulan, nomorbulan, kuartal, tahun)
SELECT DISTINCT
    CAST(TO_CHAR(CAST(s.tanggal AS DATE), 'YYYYMMDD') AS INT) AS waktuid,
    CAST(s.tanggal AS DATE) AS tanggal,
    TRIM(TO_CHAR(CAST(s.tanggal AS DATE), 'Day')) AS hari,
    TRIM(TO_CHAR(CAST(s.tanggal AS DATE), 'Month')) AS bulan,
    CAST(EXTRACT(MONTH FROM CAST(s.tanggal AS DATE)) AS INT) AS nomorbulan,
    'Q' || EXTRACT(QUARTER FROM CAST(s.tanggal AS DATE)) AS kuartal,
    CAST(EXTRACT(YEAR FROM CAST(s.tanggal AS DATE)) AS INT) AS tahun
FROM stg_penjualan s
WHERE s.tanggal IS NOT NULL
  AND TRIM(CAST(s.tanggal AS TEXT)) != ''
ON CONFLICT (waktuid) DO NOTHING;

-- ============================================================================
-- 7. TRANSFORMASI & KALKULASI TABEL FAKTA PENJUALAN (BULLETPROOF & NO ROWS DROPPED)
-- ============================================================================
INSERT INTO fact_penjualan (
    fakturid, waktuid, produkid, apotekid, pelangganid, karyawanid, supplierid,
    jumlahterjual, hargasatuan, diskon, totalpenjualan, keuntungan
)
SELECT 
    COALESCE(UPPER(REGEXP_REPLACE(TRIM(s.fakturid), '[-_]', '', 'g')), 'UNKNOWN') AS fakturid,
    CASE
        WHEN s.tanggal IS NOT NULL
            AND TRIM(CAST(s.tanggal AS TEXT)) != ''
        THEN CAST(TO_CHAR(CAST(s.tanggal AS DATE), 'YYYYMMDD') AS INT)
        ELSE -1
    END AS waktuid,
    COALESCE(p.produkid, 'UNKNOWN') AS produkid,
    COALESCE(a.apotekid, 'UNKNOWN') AS apotekid,
    COALESCE(pl.pelangganid, 'UNKNOWN') AS pelangganid,
    COALESCE(k.karyawanid, 'UNKNOWN') AS karyawanid,
    COALESCE(p.supplierid, 'UNKNOWN') AS supplierid,
    COALESCE(CAST(s.jumlahterjual AS INT), 0) AS jumlahterjual,
    COALESCE(CAST(s.hargasatuan AS NUMERIC), 0) AS hargasatuan,
    COALESCE(CAST(s.diskon AS NUMERIC), 0) AS diskon,
    
    -- Kalkulasi Revenue Bisnis (TotalPenjualan)
    GREATEST(
        (COALESCE(CAST(s.jumlahterjual AS INT), 0) * COALESCE(CAST(s.hargasatuan AS NUMERIC), 0)) - COALESCE(CAST(s.diskon AS NUMERIC), 0),
        0
    ) AS totalpenjualan,
    
    -- Kalkulasi Profit Murni (Keuntungan) dengan fallback modal 0 jika Produk tidak terdaftar
    GREATEST(
        (COALESCE(CAST(s.jumlahterjual AS INT), 0) * COALESCE(CAST(s.hargasatuan AS NUMERIC), 0)) - COALESCE(CAST(s.diskon AS NUMERIC), 0),
        0
    ) - (COALESCE(CAST(s.jumlahterjual AS INT), 0) * COALESCE(p.hargamodal, 0)) AS keuntungan
FROM stg_penjualan s
LEFT JOIN dim_produk p ON UPPER(REGEXP_REPLACE(TRIM(s.produkid), '[-_]', '', 'g')) = p.produkid
LEFT JOIN dim_apotek a ON UPPER(REGEXP_REPLACE(TRIM(s.apotekid), '[-_]', '', 'g')) = a.apotekid
LEFT JOIN dim_pelanggan pl ON UPPER(REGEXP_REPLACE(TRIM(s.pelangganid), '[-_]', '', 'g')) = pl.pelangganid
LEFT JOIN dim_karyawan k ON UPPER(REGEXP_REPLACE(TRIM(s.karyawanid), '[-_]', '', 'g')) = k.karyawanid
WHERE s.fakturid IS NOT NULL AND TRIM(CAST(s.fakturid AS TEXT)) != '';