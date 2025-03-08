from tkinter import *
import sqlite3
from tkinter import messagebox


def ket_noi_csdl():
    return sqlite3.connect("../Data/BTL_QLPT.db")


def mo_cua_so_thong_tin_tai_khoan(username, parent_window):
    if not username:
        messagebox.showerror("Lỗi", "Chưa đăng nhập, không có thông tin!")
        return

    new_window = Toplevel(parent_window)
    new_window.title("Thông tin tài khoản")
    new_window.geometry("500x300")

    frame_main = Frame(new_window, bd=3, relief="solid")
    frame_main.pack(padx=20, pady=20, fill="both", expand=True)

    labels = [
        ("ID: ", "id"),
        ("Tên tài khoản: ", "username"),
        ("Chức vụ: ", "role"),
        ("Mã nhân viên: ", "MaNV")
    ]

    for i, (text, key) in enumerate(labels):
        Label(frame_main, text=text, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5)
        Label(frame_main, text="", font=("Arial", 12), anchor="w", name=key).grid(row=i, column=1, padx=10, pady=5)

    Button(new_window, text="Quay lại", command=new_window.destroy).pack(pady=10)

    conn = ket_noi_csdl()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, MaNV FROM NguoiDung WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result:
        for i, key in enumerate(["id", "username", "role", "MaNV"]):
            frame_main.nametowidget(key).config(text=result[i])

window = Tk()
window.title("Quản lý phòng trọ")
window.geometry("1250x700")

username = ""
mo_cua_so_thong_tin_tai_khoan(username, window)

window.mainloop()
