import socket
import threading
import tkinter as tk

server_ip = "127.0.0.1"
server_port = 9999
server_address = (server_ip, server_port)

# SOCKET UDP/IP
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Variabel untuk username dan password
name = ""
password = ""
authen = False
username_accepted = False  # Flag untuk cek apakah username sudah diterima
password_check = True      # Flag untuk cek apakah sedang meminta password
username_check = True

# Fungsi untuk menerima pesan dari server
def receive():
    global authen, username_accepted, password_check, username_check
    while True:
        try:
            message, _ = client.recvfrom(1024)
            message_decoded = message.decode()

            # Tampilkan pesan di chatbox client
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, message_decoded + "\n")
            chat_box.config(state=tk.DISABLED)
            chat_box.see(tk.END)

            # Cek apakah password benar
            if "Password benar" in message_decoded:
                authen = True
                password_check = False  # Password benar, lanjut ke username
                chat_box.config(state=tk.NORMAL)
                chat_box.insert(tk.END, "Masukkan username Anda:\n")
                chat_box.config(state=tk.DISABLED)

            # Cek jika password salah
            elif "Password salah" in message_decoded:
                authen = False
                password = ""  # Reset password agar bisa input ulang
                password_check = True  # Minta input password ulang
                chat_box.config(state=tk.NORMAL)
                chat_box.insert(tk.END, "Password salah, silahkan coba lagi!\n")
                chat_box.config(state=tk.DISABLED)

            # Cek jika username sudah diambil
            elif "Username telah diambil" in message_decoded:
                username_accepted = False
                username_check = True
                name = ""  # Reset username agar bisa input ulang
                chat_box.config(state=tk.NORMAL)
                chat_box.insert(tk.END, "Username sudah digunakan, coba yang lain!\n")
                chat_box.config(state=tk.DISABLED)

            # Cek jika username diterima
            elif "Selamat datang" in message_decoded:
                username_accepted = True  # Username diterima
                username_check = False
                chat_box.config(state=tk.NORMAL)
                chat_box.insert(tk.END, "Anda sudah terhubung, silahkan kirim pesan ke rumahsti!\n")
                chat_box.config(state=tk.DISABLED)

        except:
            break

# Fungsi untuk mengirim pesan ke server
def send_message():
    global name, password, authen, username_accepted, password_check, username_check
    message = message_entry.get()

    if not authen:
        # Proses autentikasi password
        if password_check:
            password = message  # Ambil password dari input
            client.sendto(f"PASSWORD:{password}".encode(), server_address)
        elif not password_check:
            chat_box.config(state=tk.NORMAL)
            chat_box.insert(tk.END, "Masuskkan password Anda:\n")
            chat_box.config(state=tk.DISABLED)
            password_check = True
    elif not username_accepted:
        # Proses autentikasi username setelah password benar
        if username_check:
            name = message  # Ambil username dari input
            client.sendto(f"USERNAME:{name}".encode(), server_address)
    else:
        # Setelah autentikasi selesai, kirim pesan ke server
        client.sendto(f"{message}".encode(), server_address)

    message_entry.delete(0, tk.END)

# Setup GUI
root = tk.Tk()
root.title("rumahsti")

root.geometry("400x500")

input_password = tk.Label(root, text="Masukkan Password: ")
input_password.pack(pady=5)

chat_box = tk.Text(root, state=tk.DISABLED, width=50, height=25)
chat_box.pack(pady=10)

message_entry = tk.Entry(root, width=40)
message_entry.pack(pady=10)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=10)

# Mulai thread untuk menerima pesan
threading.Thread(target=receive, daemon=True).start()

root.mainloop()