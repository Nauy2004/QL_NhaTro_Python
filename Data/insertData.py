import sqlite3
import random
from datetime import datetime, timedelta

# Connect to the database
conn = sqlite3.connect("../Data/BTL_QLPT.db")
cursor = conn.cursor()

# Function to generate random dates
def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

# Sample data for VanPhong
van_phong_data = [
    (1, "123 Nguyễn Văn Cừ, Quận 5, TP.HCM"),
    (2, "45 Lê Duẩn, Quận 1, TP.HCM"),
    (3, "78 Võ Văn Tần, Quận 3, TP.HCM"),
    (4, "56 Trần Hưng Đạo, Quận Hoàn Kiếm, Hà Nội"),
    (5, "34 Nguyễn Chí Thanh, Quận Đống Đa, Hà Nội"),
    (6, "90 Lê Lợi, TP. Đà Nẵng"),
    (7, "12 Nguyễn Huệ, TP. Huế"),
    (8, "67 Lạc Long Quân, TP. Cần Thơ"),
    (9, "89 Trần Phú, TP. Nha Trang"),
    (10, "23 Phan Chu Trinh, TP. Vũng Tàu")
]

# Insert data into VanPhong
cursor.executemany("INSERT OR IGNORE INTO VanPhong (MaVP, DiaChi) VALUES (?, ?)", van_phong_data)

# Sample data for NhanVien
nhan_vien_data = [
    (1, "Nguyễn Văn An", "Nam", "123 Nguyễn Trãi, Q.1, TP.HCM", "0901234567", 1),
    (2, "Trần Thị Bình", "Nữ", "45 Lê Lai, Q.1, TP.HCM", "0912345678", 1),
    (3, "Lê Văn Cường", "Nam", "67 Cao Thắng, Q.3, TP.HCM", "0923456789", 2),
    (4, "Phạm Thị Dung", "Nữ", "89 Nguyễn Du, Q.1, TP.HCM", "0934567890", 2),
    (5, "Hoàng Văn Em", "Nam", "12 Võ Thị Sáu, Q.3, TP.HCM", "0945678901", 3),
    (6, "Ngô Thị Phương", "Nữ", "34 Điện Biên Phủ, Q.Bình Thạnh, TP.HCM", "0956789012", 3),
    (7, "Vũ Văn Giang", "Nam", "56 Lý Tự Trọng, Q.1, TP.HCM", "0967890123", 4),
    (8, "Đặng Thị Hồng", "Nữ", "78 Cách Mạng Tháng 8, Q.3, TP.HCM", "0978901234", 5),
    (9, "Bùi Văn Khánh", "Nam", "90 Trần Hưng Đạo, Q.5, TP.HCM", "0989012345", 6),
    (10, "Lý Thị Lan", "Nữ", "12 Nguyễn Thị Minh Khai, Q.1, TP.HCM", "0990123456", 7)
]

# Insert data into NhanVien
cursor.executemany("INSERT OR IGNORE INTO NhanVien (MaNV, HoTen, GioiTinh, DiaChi, SDT, MaVP) VALUES (?, ?, ?, ?, ?, ?)", nhan_vien_data)

# Update admin user to link with a staff member
cursor.execute("UPDATE NguoiDung SET MaNV = 1 WHERE username = 'admin'")

# Sample data for NguoiDung
nguoi_dung_data = [
    ("nhanvien1", "123456", "nhanvien", 2),
    ("nhanvien2", "123456", "nhanvien", 3),
    ("nhanvien3", "123456", "nhanvien", 4),
    ("nhanvien4", "123456", "nhanvien", 5),
    ("nhanvien5", "123456", "nhanvien", 6),
    ("nhanvien6", "123456", "nhanvien", 7),
    ("nhanvien7", "123456", "nhanvien", 8),
    ("nhanvien8", "123456", "nhanvien", 9),
    ("nhanvien9", "123456", "nhanvien", 10)
]

# Insert data into NguoiDung
cursor.executemany("INSERT OR IGNORE INTO NguoiDung (username, password, role, MaNV) VALUES (?, ?, ?, ?)", nguoi_dung_data)

# Sample data for NhaTro
nha_tro_data = [
    (1, "123 Nguyễn Trãi, Q.5, TP.HCM", 1),
    (2, "45 Lê Lợi, Q.1, TP.HCM", 1),
    (3, "67 Nguyễn Thị Minh Khai, Q.3, TP.HCM", 2),
    (4, "89 Võ Văn Tần, Q.3, TP.HCM", 2),
    (5, "12 Lý Tự Trọng, Q.1, TP.HCM", 3),
    (6, "34 Cách Mạng Tháng 8, Q.3, TP.HCM", 4),
    (7, "56 Trần Hưng Đạo, Q.5, TP.HCM", 5),
    (8, "78 Hai Bà Trưng, Q.1, TP.HCM", 6),
    (9, "90 Lê Duẩn, Q.1, TP.HCM", 7),
    (10, "12 Điện Biên Phủ, Q.Bình Thạnh, TP.HCM", 8)
]

# Insert data into NhaTro
cursor.executemany("INSERT OR IGNORE INTO NhaTro (MaNha, DiaChi, MaVP) VALUES (?, ?, ?)", nha_tro_data)

# Sample data for PhongTro
phong_tro_data = [
    (1, 1, 3000000, "Trống"),
    (2, 1, 3500000, "Đang thuê"),
    (3, 2, 4000000, "Đang thuê"),
    (4, 2, 3800000, "Trống"),
    (5, 3, 4200000, "Đang thuê"),
    (6, 4, 3600000, "Bảo trì"),
    (7, 5, 3200000, "Đang thuê"),
    (8, 6, 3900000, "Trống"),
    (9, 7, 4500000, "Đang thuê"),
    (10, 8, 4100000, "Đang thuê"),
    (11, 9, 3700000, "Trống"),
    (12, 10, 4300000, "Đang thuê")
]

# Insert data into PhongTro
cursor.executemany("INSERT OR IGNORE INTO PhongTro (MaPhong, MaNha, GiaPhong, TrangThai) VALUES (?, ?, ?, ?)", phong_tro_data)

# Sample data for NguoiThue
nguoi_thue_data = [
    ("079201001234", "Nguyễn Thị Mai", "Nữ", "0901122334", "123 Nguyễn Văn Cừ, Q.5, TP.HCM"),
    ("079201002345", "Trần Văn Nam", "Nam", "0912233445", "45 Lê Lợi, Q.1, TP.HCM"),
    ("079201003456", "Lê Thị Oanh", "Nữ", "0923344556", "67 Nguyễn Thị Minh Khai, Q.3, TP.HCM"),
    ("079201004567", "Phạm Văn Phúc", "Nam", "0934455667", "89 Võ Văn Tần, Q.3, TP.HCM"),
    ("079201005678", "Hoàng Thị Quỳnh", "Nữ", "0945566778", "12 Lý Tự Trọng, Q.1, TP.HCM"),
    ("079201006789", "Ngô Văn Rồng", "Nam", "0956677889", "34 Cách Mạng Tháng 8, Q.3, TP.HCM"),
    ("079201007890", "Vũ Thị Sương", "Nữ", "0967788990", "56 Trần Hưng Đạo, Q.5, TP.HCM"),
    ("079201008901", "Đặng Văn Tuấn", "Nam", "0978899001", "78 Hai Bà Trưng, Q.1, TP.HCM"),
    ("079201009012", "Bùi Thị Uyên", "Nữ", "0989900112", "90 Lê Duẩn, Q.1, TP.HCM"),
    ("079201000123", "Lý Văn Vũ", "Nam", "0990011223", "12 Điện Biên Phủ, Q.Bình Thạnh, TP.HCM")
]

# Insert data into NguoiThue
cursor.executemany("INSERT OR IGNORE INTO NguoiThue (CCCD, HoTen, GioiTinh, SDT, DiaChi) VALUES (?, ?, ?, ?, ?)", nguoi_thue_data)

# Sample data for HopDong
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

hop_dong_data = []
for i in range(1, 11):
    start_day = random_date(start_date, end_date).strftime("%Y-%m-%d")
    end_day = (datetime.strptime(start_day, "%Y-%m-%d") + timedelta(days=365)).strftime("%Y-%m-%d")
    
    # Assign rented rooms to contracts
    room_id = i + 1 if i < 5 else i + 3
    
    hop_dong_data.append((
        i,
        random.uniform(3000000, 5000000),
        start_day,
        end_day,
        nguoi_thue_data[i-1][0],  # Using CCCD from nguoi_thue_data
        room_id
    ))

# Insert data into HopDong
cursor.executemany("INSERT OR IGNORE INTO HopDong (MaHD, GiaHopDong, ThoiGianBD, ThoiGianKT, CCCD, MaPhong) VALUES (?, ?, ?, ?, ?, ?)", hop_dong_data)

# Sample data for DichVu
dich_vu_data = [
    (1, "Điện", 3500),
    (2, "Nước", 25000),
    (3, "Internet", 200000),
    (4, "Dọn vệ sinh", 100000),
    (5, "Giặt ủi", 150000),
    (6, "Giữ xe", 100000),
    (7, "Bảo vệ", 50000),
    (8, "Thu gom rác", 30000),
    (9, "Sửa chữa nhỏ", 200000),
    (10, "Điều hòa", 300000)
]

# Insert data into DichVu
cursor.executemany("INSERT OR IGNORE INTO DichVu (MaDV, TenDV, GiaDV) VALUES (?, ?, ?)", dich_vu_data)

# Sample data for HoaDon
hoa_don_data = []
invoice_date = datetime(2023, 2, 1)
invoice_end = datetime(2024, 1, 31)

for i in range(1, 11):
    invoice_day = random_date(invoice_date, invoice_end).strftime("%Y-%m-%d")
    payment_status = random.choice(["Chưa thanh toán", "Đã thanh toán"])
    
    # Random bill amount
    amount = random.uniform(500000, 1500000)
    
    hoa_don_data.append((
        i,
        invoice_day,
        amount,
        i,  # MaHD
        payment_status
    ))

# Insert data into HoaDon
cursor.executemany("INSERT OR IGNORE INTO HoaDon (MaHoaDon, NgayLap, SoTien, MaHD, TrangThai) VALUES (?, ?, ?, ?, ?)", hoa_don_data)

# Sample data for ChiTietHoaDon
chi_tiet_hoa_don_data = []
for i in range(1, 11):
    # Add 2-4 random services to each invoice
    num_services = random.randint(2, 4)
    service_ids = random.sample(range(1, 11), num_services)
    
    for service_id in service_ids:
        # Get service price
        cursor.execute("SELECT GiaDV FROM DichVu WHERE MaDV = ?", (service_id,))
        service_price = cursor.fetchone()[0]
        
        # Calculate random amount based on service
        if service_id == 1:  # Electricity
            units = random.randint(50, 200)
            amount = units * service_price
        elif service_id == 2:  # Water
            units = random.randint(5, 20)
            amount = units * service_price
        else:
            # Fixed price services
            amount = service_price
            
        chi_tiet_hoa_don_data.append((
            i,  # MaHoaDon
            service_id,
            amount
        ))

# Insert data into ChiTietHoaDon
cursor.executemany("INSERT OR IGNORE INTO ChiTietHoaDon (MaHoaDon, MaDV, ThanhTien) VALUES (?, ?, ?)", chi_tiet_hoa_don_data)

# Sample data for ChiSo
chi_so_data = []
for i in range(1, 11):
    room_id = i + 1 if i < 5 else i + 3
    old_reading = random.randint(0, 500)
    new_reading = old_reading + random.randint(50, 150)
    
    chi_so_data.append((
        i,
        room_id,
        old_reading,
        new_reading
    ))

# Insert data into ChiSo
cursor.executemany("INSERT OR IGNORE INTO ChiSo (MaChiSo, MaPhong, ChiSoCu, ChiSoMoi) VALUES (?, ?, ?, ?)", chi_so_data)

# Commit changes and close connection
conn.commit()
conn.close()

print("Dữ liệu mẫu đã được thêm thành công!")