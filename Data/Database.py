import sqlite3

conn = sqlite3.connect("BTL_QLPT.db")
cursor = conn.cursor()

# Người dùng
cursor.execute('''
    CREATE TABLE IF NOT EXISTS NguoiDung (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin', 'nhanvien')),
        MaNV INTEGER,  
        FOREIGN KEY (MaNV) REFERENCES NhanVien(MaNV) ON DELETE SET NULL
    )
''')

cursor.execute("SELECT * FROM NguoiDung WHERE username = 'admin'")
admin_exists = cursor.fetchone()

if not admin_exists:
    cursor.execute("INSERT INTO NguoiDung (username, password, role, MaNV) VALUES ('admin', '123', 'admin', NULL)")
    print("Tài khoản admin mặc định đã được tạo!")

# Văn phòng
cursor.execute('''
    CREATE TABLE IF NOT EXISTS VanPhong (
        MaVP INTEGER PRIMARY KEY,
        DiaChi TEXT
    )
''')

# Nhà trọ
cursor.execute('''
    CREATE TABLE IF NOT EXISTS NhaTro (
        MaNha INTEGER PRIMARY KEY,
        DiaChi TEXT,
        MaVP INTEGER,
        FOREIGN KEY (MaVP) REFERENCES VanPhong(MaVP)
    )
''')

# Phòng trọ
cursor.execute('''
    CREATE TABLE IF NOT EXISTS PhongTro (
        MaPhong INTEGER PRIMARY KEY,
        TrangThai TEXT,
        MaNha INTEGER,
        FOREIGN KEY (MaNha) REFERENCES NhaTro(MaNha)
    )
''')

# Người thuê
cursor.execute('''
    CREATE TABLE IF NOT EXISTS NguoiThue (
        CCCD TEXT PRIMARY KEY,
        HoTen TEXT,
        GioiTinh TEXT,
        SDT TEXT,
        DiaChi TEXT,
        MaPhong INTEGER,
        FOREIGN KEY (MaPhong) REFERENCES PhongTro(MaPhong)
    )
''')

# Hợp đồng
cursor.execute('''
    CREATE TABLE IF NOT EXISTS HopDong (
        MaHD INTEGER PRIMARY KEY,
        GiaPhong REAL,
        ThoiGianBD TEXT,
        ThoiGianKT TEXT,
        CCCD TEXT,
        FOREIGN KEY (CCCD) REFERENCES NguoiThue(CCCD)
    )
''')

# Hóa đơn
cursor.execute('''
    CREATE TABLE IF NOT EXISTS HoaDon (
        MaHoaDon INTEGER PRIMARY KEY,
        NgayLap TEXT,
        SoTien REAL,
        MaHD INTEGER,
        FOREIGN KEY (MaHD) REFERENCES HopDong(MaHD)
    )
''')

# Nhân viên
cursor.execute('''
    CREATE TABLE IF NOT EXISTS NhanVien (
        MaNV INTEGER PRIMARY KEY,
        HoTen TEXT,
        GioiTinh TEXT,
        DiaChi TEXT,
        SDT TEXT,
        MaVP INTEGER,
        FOREIGN KEY (MaVP) REFERENCES VanPhong(MaVP)
    )
''')

# Dịch vụ
cursor.execute('''
    CREATE TABLE IF NOT EXISTS DichVu (
        MaDV INTEGER PRIMARY KEY,
        TenDV TEXT,
        GiaDV REAL
    )
''')

# Chi tiết hóa đơn
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ChiTietHoaDon (
        MaHoaDon INTEGER,
        MaDV INTEGER,
        ThanhTien REAL,
        PRIMARY KEY (MaHoaDon, MaDV),
        FOREIGN KEY (MaHoaDon) REFERENCES HoaDon(MaHoaDon),
        FOREIGN KEY (MaDV) REFERENCES DichVu(MaDV)
    )
''')

# Trạng thái
cursor.execute('''
    CREATE TABLE IF NOT EXISTS TrangThai (
        MTT INTEGER PRIMARY KEY,
        MaHoaDon INTEGER,
        FOREIGN KEY (MaHoaDon) REFERENCES HoaDon(MaHoaDon)
    )
''')

conn.commit()
conn.close()

print("Hoàn tất")