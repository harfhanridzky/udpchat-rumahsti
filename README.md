# udpchat-rumahsti

### Deskripsi

Socket Programming Chatroom yang diimplementasikan menggunakan Socket UDP dan Threading.  
Komunikasi menggunakan protokol UDP yang merupakan protokol connectionless sehingga cocok untuk chatroom yang perlu real-time

### Fitur

- Menggunakan UDP Socket untuk komunikasi antar client dan server.
- Threading digunakan untuk memastikan server dapat menangani beberapa client secara bersamaan.
- User Interface GUI untuk server dan client dibuat menggunakan tkinter.
- Proses autentikasi client dengan password dan username.
- Pesan dari client yang valid akan diteruskan (broadcast) ke semua client yang terhubung.

### Kebutuhan

- **Python 3**

### Eksekusi

1. Jalankan server.py dan client.py. Untuk client.py sesuaikan IP dengan IP device yang menjalankan server
2. Setelah client dijalankan, pengguna akan diminta untuk memasukkan password.
3. Jika password benar, pengguna akan diminta untuk memasukkan username unik, jika salah pengguna akan diminta memasukkan ulang hingga benar
4. Setelah proses autentikasi selesai, client dapat mulai mengirim pesan. 

### Developers

- **Nicholas Zefanya Lamtyo Nababan** / [18223111]
- **Harfhan Ikhtiar Ahmad Ridzky** / [18223123]
