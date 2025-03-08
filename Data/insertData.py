import sqlite3

conn = sqlite3.connect(r"C:/Users/Admin/Desktop/COde/demobtl/BTL_QL_PHONG_TRO/Data/BTL_QLPT.db")
cursor = conn.cursor()

# Insert data for VanPhong (Office)
van_phong_data = [
    (1, "36 Nguyễn Văn Trỗi, Q.Phú Nhuận, TP.HCM"),
    (2, "120 Lê Lợi, Q.1, TP.HCM"),
    (3, "28 Trần Hưng Đạo, Q.5, TP.HCM"),
    (4, "52 Nguyễn Huệ, Q.1, TP.HCM"),
    (5, "15 Lý Tự Trọng, Q.3, TP.HCM"),
    (6, "77 Lê Duẩn, Q.1, TP.HCM"),
    (7, "94 Nguyễn Du, Q.Hai Bà Trưng, Hà Nội"),
    (8, "31 Trần Phú, TP.Đà Nẵng"),
    (9, "108 Phan Đình Phùng, TP.Huế"),
    (10, "45 Ngô Quyền, Q.Hải Châu, TP.Đà Nẵng")
]

for item in van_phong_data:
    cursor.execute("INSERT OR IGNORE INTO VanPhong (MaVP, DiaChi) VALUES (?, ?)", item)

# Insert data for NhaTro (Boarding House)
nha_tro_data = [
    (101, "132 Lê Văn Sỹ, Q.3, TP.HCM", 1),
    (102, "78 Trần Quang Diệu, Q.3, TP.HCM", 1),
    (103, "25 Nguyễn Thị Minh Khai, Q.1, TP.HCM", 2),
    (104, "14 Bùi Viện, Q.1, TP.HCM", 2),
    (105, "92 Nguyễn Thái Học, Q.1, TP.HCM", 2),
    (106, "65 Lê Thánh Tôn, Q.1, TP.HCM", 3),
    (107, "23 Hoàng Diệu, Q.Hai Bà Trưng, Hà Nội", 7),
    (108, "47 Nguyễn Công Trứ, Q.Hai Bà Trưng, Hà Nội", 7),
    (109, "19 Phan Chu Trinh, TP.Đà Nẵng", 8),
    (110, "56 Hùng Vương, TP.Huế", 9)
]

for item in nha_tro_data:
    cursor.execute("INSERT OR IGNORE INTO NhaTro (MaNha, DiaChi, MaVP) VALUES (?, ?, ?)", item)

# Insert data for PhongTro (Room)
phong_tro_data = [
    (1001, "Đã thuê", 101),
    (1002, "Trống", 101),
    (1003, "Đã thuê", 102),
    (1004, "Đã thuê", 102),
    (1005, "Trống", 103),
    (1006, "Đã thuê", 104),
    (1007, "Đã thuê", 105),
    (1008, "Đã thuê", 106),
    (1009, "Trống", 107),
    (1010, "Đã thuê", 108)
]

for item in phong_tro_data:
    cursor.execute("INSERT OR IGNORE INTO PhongTro (MaPhong, TrangThai, MaNha) VALUES (?, ?, ?)", item)

# Insert data for NguoiThue (Tenant)
nguoi_thue_data = [
    ("079201001234", "Nguyễn Văn An", "Nam", "0901234567", "Bình Định", 1001),
    ("079201002345", "Trần Thị Bình", "Nữ", "0912345678", "Long An", 1003),
    ("079201003456", "Lê Văn Công", "Nam", "0923456789", "Đồng Nai", 1004),
    ("079201004567", "Phạm Thị Dung", "Nữ", "0934567890", "Tiền Giang", 1006),
    ("079201005678", "Hoàng Văn Em", "Nam", "0945678901", "Bình Dương", 1007),
    ("079201006789", "Ngô Thị Phương", "Nữ", "0956789012", "Vũng Tàu", 1008),
    ("079201007890", "Vũ Văn Giang", "Nam", "0967890123", "Hà Nội", 1010),
    ("079201008901", "Đặng Thị Hương", "Nữ", "0978901234", "Hải Phòng", None),
    ("079201009012", "Bùi Văn Khánh", "Nam", "0989012345", "Đà Nẵng", None),
    ("079201000123", "Lý Thị Lan", "Nữ", "0990123456", "Huế", None)
]

for item in nguoi_thue_data:
    cursor.execute("INSERT OR IGNORE INTO NguoiThue (CCCD, HoTen, GioiTinh, SDT, DiaChi, MaPhong) VALUES (?, ?, ?, ?, ?, ?)", item)

# Insert data for HopDong (Contract)
hop_dong_data = [
    (5001, 3000000, "2024-01-01", "2025-01-01", "079201001234"),
    (5002, 3500000, "2024-02-15", "2025-02-15", "079201002345"),
    (5003, 2800000, "2024-03-10", "2025-03-10", "079201003456"),
    (5004, 4000000, "2024-01-20", "2025-01-20", "079201004567"),
    (5005, 3200000, "2024-02-05", "2025-02-05", "079201005678"),
    (5006, 3800000, "2024-03-15", "2025-03-15", "079201006789"),
    (5007, 4200000, "2024-02-28", "2025-02-28", "079201007890"),
    (5008, 3500000, "2023-12-01", "2024-12-01", "079201008901"),
    (5009, 3100000, "2023-11-15", "2024-11-15", "079201009012"),
    (5010, 2900000, "2023-10-20", "2024-10-20", "079201000123")
]

for item in hop_dong_data:
    cursor.execute("INSERT OR IGNORE INTO HopDong (MaHD, GiaPhong, ThoiGianBD, ThoiGianKT, CCCD) VALUES (?, ?, ?, ?, ?)", item)

# Insert data for HoaDon (Invoice)
hoa_don_data = [
    (7001, "2024-02-01", 3300000, 5001),
    (7002, "2024-03-01", 3800000, 5001),
    (7003, "2024-03-15", 3900000, 5002),
    (7004, "2024-04-10", 3100000, 5003),
    (7005, "2024-02-20", 4200000, 5004),
    (7006, "2024-03-05", 3400000, 5005),
    (7007, "2024-04-15", 4100000, 5006),
    (7008, "2024-03-28", 4500000, 5007),
    (7009, "2024-01-01", 3700000, 5008),
    (7010, "2024-02-15", 3300000, 5009)
]

for item in hoa_don_data:
    cursor.execute("INSERT OR IGNORE INTO HoaDon (MaHoaDon, NgayLap, SoTien, MaHD) VALUES (?, ?, ?, ?)", item)

# Insert data for NhanVien (Employee)
nhan_vien_data = [
    (801, "Trần Văn Xuân", "Nam", "Q.3, TP.HCM", "0909123456", 1),
    (802, "Nguyễn Thị Yến", "Nữ", "Q.Phú Nhuận, TP.HCM", "0918234567", 1),
    (803, "Lê Văn Zách", "Nam", "Q.1, TP.HCM", "0927345678", 2),
    (804, "Phan Thị Ánh", "Nữ", "Q.5, TP.HCM", "0936456789", 3),
    (805, "Đỗ Văn Bình", "Nam", "Q.3, TP.HCM", "0945567890", 4),
    (806, "Võ Thị Châu", "Nữ", "Q.1, TP.HCM", "0954678901", 5),
    (807, "Hoàng Văn Đức", "Nam", "Q.Hai Bà Trưng, Hà Nội", "0963789012", 7),
    (808, "Nguyễn Thị Gấm", "Nữ", "Q.Hai Bà Trưng, Hà Nội", "0972890123", 7),
    (809, "Trần Văn Hải", "Nam", "TP.Đà Nẵng", "0981901234", 8),
    (810, "Lý Thị Kim", "Nữ", "TP.Huế", "0990012345", 9)
]

for item in nhan_vien_data:
    cursor.execute("INSERT OR IGNORE INTO NhanVien (MaNV, HoTen, GioiTinh, DiaChi, SDT, MaVP) VALUES (?, ?, ?, ?, ?, ?)", item)

# Insert data for NguoiDung (User)
nguoi_dung_data = [
    (1, "admin", "123", "admin", None),  # Admin default account (should already exist)
    (2, "xuantv", "123456", "nhanvien", 801),
    (3, "yennt", "123456", "nhanvien", 802),
    (4, "zachlv", "123456", "nhanvien", 803),
    (5, "anhpt", "123456", "nhanvien", 804),
    (6, "binhdv", "123456", "nhanvien", 805),
    (7, "chauv", "123456", "nhanvien", 806),
    (8, "duchv", "123456", "nhanvien", 807),
    (9, "gamnt", "123456", "nhanvien", 808),
    (10, "haitv", "123456", "nhanvien", 809),
    (11, "kimlt", "123456", "nhanvien", 810)
]

# Skip the first admin user as it's already added in your schema creation
for item in nguoi_dung_data[1:]:
    cursor.execute("INSERT OR IGNORE INTO NguoiDung (id, username, password, role, MaNV) VALUES (?, ?, ?, ?, ?)", item)

# Insert data for DichVu (Service)
dich_vu_data = [
    (601, "Điện", 4000),  # Price per kWh
    (602, "Nước", 15000),  # Price per cubic meter
    (603, "Internet", 200000),  # Fixed monthly price
    (604, "Dọn dẹp", 150000),  # Fixed monthly price
    (605, "Giặt ủi", 100000),  # Fixed monthly price
    (606, "Gửi xe", 100000),  # Fixed monthly price
    (607, "Bảo vệ", 50000),  # Fixed monthly price
    (608, "Rác", 30000),  # Fixed monthly price
    (609, "Gas", 80000),  # Fixed monthly price
    (610, "Sửa chữa", 0)  # Price depends on service
]

for item in dich_vu_data:
    cursor.execute("INSERT OR IGNORE INTO DichVu (MaDV, TenDV, GiaDV) VALUES (?, ?, ?)", item)

# Insert data for ChiTietHoaDon (Invoice Detail)
chi_tiet_hoa_don_data = [
    (7001, 601, 300000),  # Electricity
    (7001, 602, 100000),  # Water
    (7001, 603, 200000),  # Internet
    (7001, 606, 100000),  # Parking
    (7002, 601, 350000),  # Electricity
    (7002, 602, 150000),  # Water
    (7002, 603, 200000),  # Internet
    (7002, 604, 150000),  # Cleaning
    (7003, 601, 320000),  # Electricity
    (7003, 602, 180000),  # Water
    (7003, 603, 200000),  # Internet
    (7004, 601, 280000),  # Electricity
    (7004, 602, 120000),  # Water
    (7004, 606, 100000),  # Parking
    (7004, 608, 30000),   # Garbage
    (7005, 601, 400000),  # Electricity
    (7005, 602, 150000),  # Water
    (7005, 603, 200000),  # Internet
    (7005, 605, 100000),  # Laundry
    (7006, 601, 250000),  # Electricity
    (7006, 602, 120000),  # Water
    (7006, 603, 200000),  # Internet
    (7007, 601, 320000),  # Electricity
    (7007, 602, 180000),  # Water
    (7007, 603, 200000),  # Internet
    (7007, 604, 150000),  # Cleaning
    (7008, 601, 380000),  # Electricity
    (7008, 602, 170000),  # Water
    (7008, 603, 200000),  # Internet
    (7008, 607, 50000),   # Security
    (7009, 601, 350000),  # Electricity
    (7009, 602, 150000),  # Water
    (7009, 603, 200000),  # Internet
    (7009, 606, 100000),  # Parking
    (7010, 601, 280000),  # Electricity
    (7010, 602, 120000),  # Water
    (7010, 603, 200000),  # Internet
]

for item in chi_tiet_hoa_don_data:
    cursor.execute("INSERT OR IGNORE INTO ChiTietHoaDon (MaHoaDon, MaDV, ThanhTien) VALUES (?, ?, ?)", item)

# Insert data for TrangThai (Status)
trang_thai_data = [
    (901, 7001),  # Paid
    (902, 7002),  # Paid
    (903, 7003),  # Paid
    (904, 7004),  # Paid
    (905, 7005),  # Paid
    (906, 7006),  # Paid
    (907, 7007),  # Unpaid
    (908, 7008),  # Unpaid
    (909, 7009),  # Paid
    (910, 7010),  # Paid
]

for item in trang_thai_data:
    cursor.execute("INSERT OR IGNORE INTO TrangThai (MTT, MaHoaDon) VALUES (?, ?)", item)

conn.commit()
conn.close()

print("Hoàn tất thêm data mẫu vào cơ sở dữ liệu!")