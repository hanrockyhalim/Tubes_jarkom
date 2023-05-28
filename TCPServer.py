import socket
import os

# Menentukan alamat IP dan port yang akan digunakan
host = 'localhost'  # Ganti dengan alamat IP yang diinginkan
port = 8080  # Ganti dengan nomor port yang diinginkan

# Membaca daftar file dalam direktori server


def get_file_list():
    file_list = []
    for file_name in os.listdir('.'):
        if os.path.isfile(file_name):
            file_list.append(file_name)
    return file_list

# Mengirim konten file ke klien


def send_file_content(conn, file_path):
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            content = file.read()

        # Menentukan tipe konten berdasarkan ekstensi file
        file_extension = os.path.splitext(file_path)[1].lower()
        content_type = ''
        if file_extension == '.pdf':
            content_type = 'application/pdf'
        elif file_extension in ['.jpg', '.jpeg']:
            content_type = 'image/jpeg'
        elif file_extension == '.png':
            content_type = 'image/png'
        elif file_extension == '.gif':
            content_type = 'image/gif'
        elif file_extension == '.mp3':
            content_type = 'audio/mpeg'
        elif file_extension == '.mp4':
            content_type = 'video/mp4'
        elif file_extension == '.html':
            content_type = 'text/html'
        else:
            # Tipe konten default jika tidak dikenali
            content_type = 'application/octet-stream'

        # Membuat header HTTP
        header = 'HTTP/1.1 200 OK\r\nContent-Type: {}\r\nContent-Length: {}\r\n\r\n'.format(
            content_type, len(content))

        # Mengirim header dan konten file ke klien
        conn.sendall(header.encode('utf-8') + content)
    else:
        response = 'File Not Found'
        status_code = '404 Not Found'
        response_header = 'HTTP/1.1 {}\r\nContent-Length: {}\r\n\r\n{}'.format(
            status_code, len(response), response)
        conn.sendall(response_header.encode('utf-8'))

# Menangani permintaan dari klien


def handle_request(conn):
    # Menerima data dari klien
    data = conn.recv(1024).decode('utf-8')
    if not data:
        return

    print('Pesan dari klien:', data)

    # Mengekstrak nama file dari pesan HTTP GET
    file_name = data.split('\r\n')[0].split()[1][1:]

    # Mengirim konten file ke klien
    send_file_content(conn, file_name)

    # Menutup koneksi
    conn.close()


def start_server():
    # Membuat objek socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Mengikat socket ke alamat IP dan port yang ditentukan
    sock.bind((host, port))

    # Mendengarkan koneksi masuk
    sock.listen(1)
    print('Server HTTP berjalan di {}:{}'.format(host, port))

    # Menerima koneksi dari klien dan menangani setiap koneksi dalam loop
    while True:
        conn, addr = sock.accept()
        print('Terhubung dengan', addr)

        # Menangani permintaan dari klien dalam thread terpisah
        handle_request(conn)


# Memulai server HTTP
start_server()
