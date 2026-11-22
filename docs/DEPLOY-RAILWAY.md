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
DISPLAY_SIZEW=1280
DISPLAY_SIZEH=720
DISPLAY_REFRESH=30
SELKIES_MANUAL_RESOLUTION=true
SELKIES_MANUAL_WIDTH=1280
SELKIES_MANUAL_HEIGHT=720
SELKIES_FRAMERATE=30-30
```

- `CUSTOM_USER`: username login. Karakter yang didukung: huruf, angka, titik, underscore, @, dan tanda hubung.
- `PASSWORD`: password login, minimal 8 karakter; gunakan 12 karakter atau lebih.
- `PORT`: port Nginx/desktop, tetap `3000`.
- `TZ`: zona waktu container.
- `HARDEN_DESKTOP`: `true` menonaktifkan terminal dan sudo di desktop.
- `SELKIES_FILE_TRANSFERS`: `upload,download` mengaktifkan kedua arah transfer file pada sidebar.
- `DISPLAY_SIZEW`, `DISPLAY_SIZEH`, `DISPLAY_REFRESH`: mode desktop awal 1280×720 pada 30 Hz.
- `SELKIES_MANUAL_RESOLUTION`, `SELKIES_MANUAL_WIDTH`, `SELKIES_MANUAL_HEIGHT`: mengunci resolusi stream pada 1280×720 agar browser client tidak memaksakan desktop 1920 piksel.
- `SELKIES_FRAMERATE`: `30-30` mengunci stream pada 30 FPS. Ini default yang lebih ringan untuk container Railway 1 GB tanpa GPU.
- `RAILWAY_SHM_SIZE_BYTES`: shared memory yang diminta, 1 GiB. Startup wrapper memakai `--disable-dev-shm-usage` secara otomatis jika shared memory aktual kurang dari 512 MiB.

Jangan gunakan password contoh. Bila `PASSWORD` kosong atau tidak valid, startup sengaja mengunci login dengan password acak yang tidak diketahui dan mencatat peringatan ke Deploy Logs.

## 3. Filesystem biasa tanpa Volume

Jangan buat Railway Volume dan jangan pasang storage eksternal pada `/config`. Direktori `/config` disediakan oleh image Chromium dan menggunakan filesystem writable biasa milik container. Profil browser, cookies, ekstensi, bookmark, pengaturan, dan unduhan hanya bersifat sementara. Semuanya akan hilang ketika container dibuat ulang atau deployment diganti.

## 4. Networking dan health check

- Generate Railway Domain.
- Target port domain: `3000`.
- Healthcheck path: `/healthz`.
- Healthcheck timeout: `120` detik.

Endpoint `/healthz` mengembalikan HTTP 200 sederhana tanpa Basic Auth agar probe Railway dapat memeriksa web server. Endpoint ini hanya untuk liveness, bukan endpoint browser. Semua halaman browser dan stream tetap memerlukan login.

## 5. Login

Buka domain Railway melalui HTTPS. Masukkan nilai `CUSTOM_USER` dan `PASSWORD` dari Variables service. Setelah autentikasi berhasil, tampilan Chromium Desktop muncul di tab browser.

## 6. Troubleshooting

| Gejala | Solusi |
| --- | --- |
| `s6-overlay-suexec: fatal: can only run as pid 1` | Pastikan Dockerfile baru memakai entry point `catatonit → railway-start`, bukan entry point bawaan `/init`. |
| Domain 502 / connection refused | Periksa deployment status, Deploy Logs, dan target port 3000. |
| Healthcheck gagal | Pastikan `/healthz` aktif dan service telah menggunakan image hasil build terbaru. |
| Dialog login terus muncul | Periksa `CUSTOM_USER` dan `PASSWORD`; pastikan password minimal 8 karakter dan redeploy. |
| Profil hilang sesudah redeploy | Normal untuk mode tanpa Volume. Profil berada pada filesystem sementara container. |
| Chromium crash / tab “Aw, Snap!” | Container 1 GB memakai default 1280×720 / 30 FPS. Kurangi tab dan workload berat. Bila perlu beberapa tab/halaman AI sekaligus, gunakan paket Railway dengan batas memori lebih tinggi. Pastikan shared-memory fallback aktif. |

## 7. Keamanan

Nginx Basic Auth aktif secara paksa saat build. Startup membuat hash SHA-512 crypt pada `/etc/nginx/.htpasswd`, lalu menghapus password plaintext dari environment sebelum service desktop berjalan. Nginx juga memeriksa Origin untuk menolak cross-site access ke WebSocket, dan menambahkan header anti-framing.

Tetap perlakukan URL, password, dan data profil `/config` sebagai rahasia. Gunakan password unik yang panjang. Untuk organisasi/SSO, pasang access gateway tambahan di depan domain publik.
