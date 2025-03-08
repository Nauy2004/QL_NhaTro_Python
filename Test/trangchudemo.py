
from tkinter import *
import sqlite3
import subprocess

def lay_nguoi_dung():
    conn = sqlite3.connect("../Data/BTL_QLPT.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, role FROM NguoiDung LIMIT 1")
    user = cursor.fetchone()
    conn.close()
    return user if user else None

def xem_thong_tin():
    user = lay_nguoi_dung()
    if user:
        username, role = user
        if role == "admin":
            label_noidung.config(text=f"Bạn là admin.")
        else:
            conn = sqlite3.connect("BTL_QLPT.db")
            cursor = conn.cursor()
            cursor.execute("SELECT username, role FROM NguoiDung WHERE username = ?", (username,))
            user = cursor.fetchone()
            conn.close()
            label_noidung.config(text=f"Thông tin tài khoản:\nTên: {user[0]}\nVai trò: {user[1]}")
    else:
        label_noidung.config(text="Không tìm thấy thông tin tài khoản")

def dang_xuat():
    window.destroy()
    subprocess.run(["python", "DangNhap.py"])

def thoat_ung_dung():
    window.destroy()

def tao_tai_khoan_nhan_vien():
    subprocess.run(["python", "DangKy.py"])

window = Tk()
window.title("Trang chủ")
window.geometry("1200x700")
window.configure(bg="Alice Blue")
window.iconbitmap("../Picture_Icon/icon.ico")

frame_menu = Frame(window, width=250, bg="Powder Blue")
frame_menu.pack(side="left", fill="y")

frame_main = Frame(window, bg="#F0F8FF")
frame_main.pack(side="right", expand=True, fill="both")

label_tieude = Label(frame_main, text="Chào mừng bạn!", font=("Arial", 20), fg="#89CFF0", bg="#F0F8FF")
label_tieude.pack(pady=20)

label_noidung = Label(frame_main, text="", font=("Arial", 16), fg="black", bg="#F0F8FF")
label_noidung.pack(pady=20)

button_taikhoan = Button(frame_menu, text="Xem thông tin tài khoản", font=("Arial", 14), command=xem_thong_tin)
button_taikhoan.pack(pady=10, padx=10, fill="x")

user = lay_nguoi_dung()
if user and user[1] == "admin":
    button_tao_taikhoan = Button(frame_menu, text="Tạo tài khoản nhân viên", font=("Arial", 14), command=tao_tai_khoan_nhan_vien)
    button_tao_taikhoan.pack(pady=10, padx=10, fill="x")

button_dangxuat = Button(frame_menu, text="Đăng xuất", font=("Arial", 14), command=dang_xuat)
button_dangxuat.pack(pady=20, padx=10, fill="x")

button_thoat = Button(frame_menu, text="Thoát ứng dụng", font=("Arial", 14), command=thoat_ung_dung)
button_thoat.pack(pady=20, padx=10, fill="x")

window.mainloop()
