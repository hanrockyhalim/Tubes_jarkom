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

    # Menerima respons header dari server
    response_header = b''
    while b'\r\n\r\n' not in response_header:
        data = client_socket.recv(4096)
        if not data:
            break
        response_header += data

    # Mencetak respons header yang dapat dibaca manusia
    header_lines = response_header.decode('latin-1').split('\r\n')
    for line in header_lines[0:5]:
        if line and ':' in line:
            key, *values = line.split(':', 1)
            value = values[0].strip() if values else ''
            print(f"{key}: {value}")

    print("Respons Header:")
    print(header_lines[0:3])


except ConnectionRefusedError:
    print('Tidak dapat terhubung ke server')

finally:
    # Menutup koneksi
    client_socket.close()
