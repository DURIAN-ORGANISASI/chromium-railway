# Panduan Deploy Chromium ke Railway

Dokumen ini menjalankan satu service **Chromium Desktop** yang dapat dibuka melalui domain HTTPS Railway dan dilindungi username/password. Tidak membutuhkan service tambahan atau database.

## 1. Buat service

1. Upload isi repository ke GitHub.
2. Di Railway, buat project atau pilih project yang akan digunakan.
3. Pilih **New → GitHub Repo**, lalu pilih repository `chromium-railway`.
4. Biarkan Root Directory kosong.
5. Pastikan builder menggunakan Dockerfile di root.
6. Namai service `chromium`.

## 2. Tempel Variables

Buka service **chromium → Variables → RAW Editor**, lalu tempel:

```dotenv
CUSTOM_USER=chromium
PASSWORD=GANTI_DENGAN_PASSWORD_UNIK_MINIMAL_12_KARAKTER
PORT=3000
TZ=Asia/Jakarta
HARDEN_DESKTOP=true
RAILWAY_SHM_SIZE_BYTES=1073741824
```

Penjelasan:

- `CUSTOM_USER`: username untuk login ke web Chromium.
- `PASSWORD`: password untuk login. Buat minimal 12 karakter, disarankan lebih panjang.
- `PORT`: port web Chromium. Biarkan `3000`.
- `TZ`: zona waktu container.
- `HARDEN_DESKTOP`: menonaktifkan terminal dan sudo desktop bila `true`.
- `RAILWAY_SHM_SIZE_BYTES`: shared memory 1 GiB agar tab modern lebih stabil.

**Jangan gunakan password contoh.** Pastikan `CUSTOM_USER` hanya memakai huruf, angka, `.`, `_`, `@`, atau `-`.

## 3. Tambahkan Volume

1. Buka tab **Volumes** pada service.
2. Buat Volume baru.
3. Isi mount path:

```text
/config
```

Volume `/config` menyimpan home directory dan browser profile. Jangan hapus Volume jika kamu ingin mempertahankan bookmark, cookie, ekstensi, dan sesi login website.

## 4. Generate Domain

1. Buka **Settings → Networking**.
2. Klik **Generate Domain**.
3. Atur target port domain ke `3000`.
4. Simpan lalu tunggu deployment aktif.

## 5. Login

1. Buka URL domain Railway.
2. Saat dialog autentikasi muncul, masukkan nilai `CUSTOM_USER`.
3. Masukkan nilai `PASSWORD`.
4. Chromium Desktop akan muncul setelah kredensial diterima.

Jika dialog login muncul berulang, periksa kedua nilai Variables dan pastikan perubahan sudah di-deploy.

## 6. Pemakaian

- Gunakan mouse dan keyboard langsung dari browser.
- Buka panel samping untuk clipboard, keyboard virtual, display settings, dan file transfer bila tersedia.
- Bookmark, ekstensi, cookies, dan browser settings disimpan di `/config`.
- Cukup satu replica untuk satu profil browser pribadi. Jangan scale beberapa replica yang memasang Volume profile yang sama.

## 7. Pengujian lokal (opsional)

```bash
cp .env.example .env
```

Edit password pada `.env`, kemudian:

```bash
docker compose up -d --build
```

Buka `http://localhost:3000`. Folder lokal `data/` akan menyimpan konfigurasi browser.

## Troubleshooting

| Gejala | Solusi |
| --- | --- |
| Deploy gagal | Buka Deploy Logs dan periksa kegagalan pull/build image. |
| Domain menampilkan 502 | Pastikan target port Networking `3000` dan service aktif. |
| Username/password ditolak | Periksa `CUSTOM_USER` dan `PASSWORD`, simpan, lalu redeploy. |
| Desktop tidak tampil | Tunggu browser desktop siap, refresh halaman, dan lihat Deploy Logs. |
| Profil hilang setelah deploy | Pastikan Volume dipasang pada `/config`. |
| Browser tab crash | Kurangi jumlah tab, alokasikan RAM lebih besar, gunakan shared memory `1073741824`. |

## Keamanan

Kredensial melindungi akses ke desktop Chromium, tetapi tidak membatasi situs apa yang dapat dibuka setelah login. Pengguna yang berhasil masuk dapat mengendalikan browser serta akun website yang sedang login. Perlakukan password dan Volume `/config` sebagai data sensitif. Untuk pembatasan organisasi/SSO, tambahkan access gateway di depan domain Railway.
