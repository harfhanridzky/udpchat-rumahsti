import socket
import threading
import queue
import tkinter as tk

# Konfigurasi server
server_ip = "0.0.0.0"
server_port = 9999
password = "12345678"  # password untuk masuk ke chatroom

messages = queue.Queue()
clients = {}

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((server_ip, server_port))

# Fungsi untuk menerima pesan dari client
def receive():
    while True:
        try:
            message, address = server.recvfrom(1024)
            messages.put((message, address))
        except:
            pass

# Fungsi untuk broadcast pesan ke semua client
def broadcast():
    while True:
        while not messages.empty():
            message, address = messages.get()
            message_decoded = message.decode()

            # Untuk client baru
            if address not in clients:
                if message_decoded.startswith("PASSWORD:"):
                    input_pass = message_decoded.split(":")[1]
                    if input_pass == password:
                        server.sendto("Password benar!, silahkan masukkan username anda.".encode(), address)
                    else:
                        server.sendto("Password salah!".encode(), address)
                elif message_decoded.startswith("USERNAME:"):
                    username = message_decoded.split(":")[1]
                    if username not in clients.values():
                        clients[address] = username
                        server.sendto(f"Selamat datang di rumahsti, {username}!".encode(), address)
                        print(f"{username} telah bergabung dalam rumahsti.")
                        update_gui(f"{username} telah bergabung dalam rumahsti.")  # Tampilkan di GUI server
                        update_user_list()  # Perbarui daftar pengguna di GUI
                    else:
                        server.sendto("Username telah diambil, silahkan ulangi!".encode(), address)
                continue

            # Broadcast pesan ke semua client, termasuk si pengirim
            broadcast_message = f"{clients[address]}: {message_decoded}"
            print(broadcast_message)  # Cetak pesan di terminal server
            update_gui(broadcast_message)  # Tampilkan pesan di GUI server
            for client in clients:
                try:
                    server.sendto(broadcast_message.encode(), client)
                except:
                    print(f"Gagal mengirim pesan ke {clients[client]}")
                    clients.pop(client)
                    update_user_list()  # Perbarui daftar pengguna saat client keluar

# Fungsi untuk memperbarui tampilan GUI dengan pesan baru
def update_gui(new_message):
    chat_box.config(state=tk.NORMAL)
    chat_box.insert(tk.END, new_message + "\n")
    chat_box.config(state=tk.DISABLED)
    chat_box.see(tk.END)

# Fungsi untuk memperbarui daftar pengguna aktif di GUI
def update_user_list():
    user_list.config(state=tk.NORMAL)
    user_list.delete(1.0, tk.END)  # Hapus daftar lama
    user_list.insert(tk.END, "User Aktif:\n")
    for username in clients.values():
        user_list.insert(tk.END, f"- {username}\n")  # Tambahkan nama pengguna aktif
    user_list.config(state=tk.DISABLED)

# Fungsi utama GUI server
def main():
    global chat_box, user_list
    root = tk.Tk()
    root.title("Server rumahsti")
    root.geometry("500x600")

    title_label = tk.Label(root, text="Server rumahsti", font=("Arial", 20, "bold"), foreground="black")
    title_label.pack(pady=10,padx=10)

    # Chat box untuk menampilkan pesan
    chat_box = tk.Text(root, state=tk.DISABLED, width=60, height=20, bg="grey")
    chat_box.pack(pady=10, padx=10)

    # User list untuk menampilkan pengguna aktif
    user_list = tk.Text(root, state=tk.DISABLED, width=60, height=15)
    user_list.pack(pady=10, padx=10)

    status_label = tk.Label(root, text="Server sudah nyala", font=("Arial", 14), foreground="black")
    status_label.pack(pady=10,padx=10)

    root.mainloop()

# Mulai thread untuk menerima pesan dan broadcast
threading.Thread(target=receive).start()
threading.Thread(target=broadcast).start()

if __name__ == "__main__":
    main()