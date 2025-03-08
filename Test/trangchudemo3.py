from tkinter import *
import sqlite3
import subprocess
from PIL import Image, ImageTk

def lay_nguoi_dung():
    """Lấy thông tin người dùng đang đăng nhập."""
    conn = sqlite3.connect("../Data/BTL_QLPT.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, role FROM NguoiDung LIMIT 1")
    user = cursor.fetchone()
    conn.close()
    return user if user else None

def xem_thong_tin():
    """Hiển thị thông tin tài khoản."""
    user = lay_nguoi_dung()
    if user:
        username, role = user
        if role == "admin":
            label_noidung.config(text=f"Bạn là admin.")
        else:
            conn = sqlite3.connect("../Data/BTL_QLPT.db")
            cursor = conn.cursor()
            cursor.execute("SELECT username, role FROM NguoiDung WHERE username = ?", (username,))
            user = cursor.fetchone()
            conn.close()
            label_noidung.config(text=f"Thông tin tài khoản:\nTên: {user[0]}\nVai trò: {user[1]}")
    else:
        label_noidung.config(text="Không tìm thấy thông tin tài khoản")

def dang_xuat():
    """Quay lại màn hình đăng nhập."""
    window.destroy()
    subprocess.run(["python", "DangNhap.py"])

def thoat_ung_dung():
    """Thoát ứng dụng."""
    window.destroy()

def tao_tai_khoan_nhan_vien():
    """Mở cửa sổ tạo tài khoản nhân viên."""
    subprocess.run(["python", "DangKy.py"])

# Tạo cửa sổ chính
window = Tk()
window.title("Trang chủ")
window.geometry("1200x700")
window.configure(bg="Alice Blue")

# Tạo frame cho menu bên trái
frame_menu = Frame(window, width=250, bg="Powder Blue")
frame_menu.pack(side="left", fill="y")

# Tạo nội dung chính
frame_main = Frame(window, bg="#F0F8FF")
frame_main.pack(side="right", expand=True, fill="both")

label_tieude = Label(frame_main, text="ỨNG DỤNG QUẢN LÝ PHÒNG TRỌ", font=("Times New Roman", 20, "bold"), fg="#89CFF0", bg="#F0F8FF")
label_tieude.pack(pady=10)

# Box giới thiệu
frame_gioithieu = Frame(frame_main, bg="white", bd=2, relief="solid")
frame_gioithieu.pack(pady=20, padx=20, fill="both", expand=True)

# Hình nền cho box (nếu có)
try:
    img = Image.open("anhnen2.png")
    img = img.resize((1000, 500), Image.Resampling.LANCZOS)
    bg_image = ImageTk.PhotoImage(img)
    label_bg = Label(frame_gioithieu, image=bg_image)
    label_bg.place(relwidth=1, relheight=1)
except:
    pass

label_gioithieu1 = Label(frame_gioithieu, text="Phần mềm quản lý nhà cho thuê 🎉", font=("Arial", 16, "bold"), fg="black", bg="white")
label_gioithieu1.pack(pady=10)

text_gioithieu2 = "Hiệu quả - Chuyên nghiệp - Tránh sai sót... Quản lý chưa bao giờ dễ dàng hơn thế!"
label_gioithieu2 = Label(frame_gioithieu, text="", font=("Arial", 14), fg="darkblue", bg="white")
label_gioithieu2.pack()

def hien_chu(index=0):
    if index < len(text_gioithieu2):
        label_gioithieu2.config(text=text_gioithieu2[:index+1])
        window.after(50, hien_chu, index+1)

def hien_gioithieu3():
    label_gioithieu3.config(text=txt_gioithieu3)

hien_chu()

# Các nút trong menu
button_taikhoan = Button(frame_menu, text="Xem thông tin tài khoản", font=("Times New Roman", 11), command=xem_thong_tin)
button_taikhoan.pack(pady=10, padx=10, fill="x")

user = lay_nguoi_dung()
if user and user[1] == "admin":
    button_tao_taikhoan = Button(frame_menu, text="Tạo tài khoản nhân viên", font=("Times New Roman", 11), command=tao_tai_khoan_nhan_vien)
    button_tao_taikhoan.pack(pady=10, padx=10, fill="x")

button_nha = Button(frame_menu, text="Tòa nhà", font=("Times New Roman", 11),  )
button_nha.pack(pady=10, padx=3, fill="x")

button_chiso = Button(frame_menu, text="Chỉ số điện nước", font=("Times New Roman", 11))
button_chiso.pack(pady=10, padx=3, fill="x")

button_hoadon = Button(frame_menu, text="Hóa đơn", font=("Times New Roman", 11))
button_hoadon.pack(pady = 10, padx = 3, fill = "x")

button_dichvu = Button(frame_menu, text="Dịch vụ", font=("Times New Roman", 11), command=lambda: Dichvu.quan_ly_dich_vu(frame_gioithieu))
button_dichvu.pack(pady=10, padx=3, fill="x")

button_thongke = Button(frame_menu, text="Thống kê", font=("Times New Roman", 11))
button_thongke.pack(pady = 10, padx = 3, fill = "x")

button_hopdong = Button(frame_menu, text="Hợp đồng thuê", font=("Times New Roman", 11))
button_hopdong.pack(pady = 10, padx = 3, fill = "x")

Button(frame_menu, text="Đăng xuất", font=("Times New Roman", 11), command=dang_xuat).pack(pady=100, padx=3, fill="x")
Button(frame_menu, text="Thoát ứng dụng", font=("Times New Roman", 11), command=thoat_ung_dung).pack(pady=0, padx=3, fill="x")

window.mainloop()