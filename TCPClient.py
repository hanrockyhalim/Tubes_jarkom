import socket

# Menentukan alamat IP dan port server
host = 'localhost'  # Ganti dengan alamat IP server
port = 8080  # Ganti dengan nomor port server

# Membuat objek socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Terhubung ke server
    client_socket.connect((host, port))

    # Menerima input file GET dari pengguna
    file_get = input("Masukkan file GET: ")

    # Mengirim permintaan HTTP GET ke server
    request = 'GET /{} HTTP/1.1\r\nHost: {}:{}\r\n\r\n'.format(
        file_get, host, port)
    client_socket.sendall(request.encode())

    # Menerima dan mencetak respons dari server
    response = client_socket.recv(4096).decode()
    print('Respons dari server:')
    print(response)

except ConnectionRefusedError:
    print('Tidak dapat terhubung ke server')

finally:
    # Menutup koneksi
    client_socket.close()
