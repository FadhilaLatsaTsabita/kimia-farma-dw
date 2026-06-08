CREATE OR REPLACE VIEW v_analitik_penjualan AS
SELECT 
    -- Fakta Transaksi Utama
    f.fakturid,
    f.waktuid,
    
    -- Detail Waktu (Dim Waktu)
    w.tanggal,
    w.hari,
    w.bulan,
    w.nomorbulan,
    w.kuartal,
    w.tahun,
    
    -- Detail Cabang (Dim Apotek)
    f.apotekid,
    a.kodeapotek,
    a.namaapotek,
    a.kota AS kotaapotek,
    a.provinsi AS provinsiapotek,
    a.wilayah,
    a.tipecabang, -- Disesuaikan jadi lowercase
    
    -- Detail Obat/Alkes (Dim Produk)
    f.produkid,
    p.kodeproduk,
    p.namaproduk,
    p.kategoriproduk,
    p.jenisproduk,
    p.brand,
    p.hargamodal,
    
    -- Detail Pembeli (Dim Pelanggan)
    f.pelangganid,
    pl.kodepelanggan,
    pl.namapelanggan,
    pl.jeniskelamin AS genderpelanggan,
    pl.usia AS usiapelanggan,
    pl.kelompokusia,
    pl.kota AS kotapelanggan,
    pl.provinsi AS provinsipelanggan,
    pl.tipepelanggan,
    
    -- Detail Kasir/Staf (Dim Karyawan)
    f.karyawanid,
    k.nik AS nikkaryawan,
    k.namakaryawan,
    k.jabatan AS jabatankaryawan,
    k.departemen AS departemenkaryawan,
    k.statuskepegawaian,
    
    -- Detail Penyedia Data (Dim Supplier)
    f.supplierid,
    s.namasupplier,
    s.kotasupplier,
    
    -- Metrik Angka Transaksional
    f.jumlahterjual,
    f.hargasatuan,
    f.diskon,
    f.totalpenjualan,
    f.keuntungan
FROM fact_penjualan f
JOIN dim_waktu w ON f.waktuid = w.waktuid
JOIN dim_apotek a ON f.apotekid = a.apotekid
JOIN dim_produk p ON f.produkid = p.produkid
JOIN dim_pelanggan pl ON f.pelangganid = pl.pelangganid
JOIN dim_karyawan k ON f.karyawanid = k.karyawanid
JOIN dim_supplier s ON f.supplierid = s.supplierid;