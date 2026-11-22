# Panduan Deploy Chromium ke Railway

Repository ini menjalankan Chromium Desktop visual di satu Docker service Railway. Chromium dibuka melalui domain HTTPS dan dilindungi login username/password.

## 1. Source dan build

- Source: GitHub `DURIAN-ORGANISASI/chromium-railway`, branch `main`.
- Root Directory: kosong.
- Dockerfile Path: `Dockerfile` di root repository.
- Port web: `3000`.
- Service harus berjalan dalam satu replica untuk satu profil browser.

Pastikan Railway membangun Dockerfile, bukan mencoba mendeteksi aplikasi Node/Python. Dockerfile memakai LinuxServer Chromium dengan digest tetap serta wrapper `services/browser/railway-start.sh`. Wrapper ini menghindari konflik PID 1 s6-overlay yang membuat deployment sebelumnya crash.

## 2. Variables

Buka service **Chromium → Variables → RAW Editor**, lalu tempel:

```dotenv
CUSTOM_USER=chromium
PASSWORD=GANTI_DENGAN_PASSWORD_UNIK_MINIMAL_12_KARAKTER
PORT=3000
TZ=Asia/Jakarta
HARDEN_DESKTOP=true
RAILWAY_SHM_SIZE_BYTES=1073741824
```

- `CUSTOM_USER`: username login. Karakter yang didukung: huruf, angka, titik, underscore, @, dan tanda hubung.
- `PASSWORD`: password login, minimal 8 karakter; gunakan 12 karakter atau lebih.
- `PORT`: port Nginx/desktop, tetap `3000`.
- `TZ`: zona waktu container.
- `HARDEN_DESKTOP`: `true` menonaktifkan terminal dan sudo di desktop.
- `RAILWAY_SHM_SIZE_BYTES`: shared memory yang diminta, 1 GiB. Startup wrapper memakai `--disable-dev-shm-usage` secara otomatis jika shared memory aktual kurang dari 512 MiB.

Jangan gunakan password contoh. Bila `PASSWORD` kosong atau tidak valid, startup sengaja mengunci login dengan password acak yang tidak diketahui dan mencatat peringatan ke Deploy Logs.

## 3. Persistent Volume

Buat Railway Volume dan pasang pada service Chromium dengan mount path tepat:

```text
/config
```

Volume menyimpan profil browser, cookies, ekstensi, bookmark, pengaturan, dan file unduhan. Jangan menghapus atau memindahkan Volume jika ingin mempertahankan data browser.

## 4. Networking dan health check

- Generate Railway Domain.
- Target port domain: `3000`.
- Healthcheck path: `/healthz`.
- Healthcheck timeout: `120` detik.

Endpoint `/healthz` diteruskan ke health endpoint Selkies tanpa meminta Basic Auth, sehingga Railway dapat memeriksa service. Semua halaman browser tetap memerlukan login.

## 5. Login

Buka domain Railway melalui HTTPS. Masukkan nilai `CUSTOM_USER` dan `PASSWORD` dari Variables service. Setelah autentikasi berhasil, tampilan Chromium Desktop muncul di tab browser.

## 6. Troubleshooting

| Gejala | Solusi |
| --- | --- |
| `s6-overlay-suexec: fatal: can only run as pid 1` | Pastikan Dockerfile baru memakai entry point `catatonit → railway-start`, bukan entry point bawaan `/init`. |
| Domain 502 / connection refused | Periksa deployment status, Deploy Logs, dan target port 3000. |
| Healthcheck gagal | Pastikan `/healthz` aktif dan service telah menggunakan image hasil build terbaru. |
| Dialog login terus muncul | Periksa `CUSTOM_USER` dan `PASSWORD`; pastikan password minimal 8 karakter dan redeploy. |
| Profil hilang sesudah redeploy | Pastikan Volume terpasang di `/config`. |
| Chromium crash / tab “Aw, Snap!” | Kurangi tab, cek memory limit Railway, dan pastikan shared-memory fallback aktif. Untuk desktop visual, alokasikan RAM minimal 1 GB; lebih banyak RAM lebih stabil. |

## 7. Keamanan

Nginx Basic Auth aktif secara paksa saat build. Startup membuat hash SHA-512 crypt pada `/etc/nginx/.htpasswd`, lalu menghapus password plaintext dari environment sebelum service desktop berjalan. Nginx juga memeriksa Origin untuk menolak cross-site access ke WebSocket, dan menambahkan header anti-framing.

Tetap perlakukan URL, password, dan Volume `/config` sebagai rahasia. Gunakan password unik yang panjang. Untuk organisasi/SSO, pasang access gateway tambahan di depan domain publik.
