from tkinter import *
from tkinter import messagebox
import sqlite3
import subprocess

username = ""

def dang_nhap():
    global username
    username = tk_box.get()
    password = mk_box.get()
    conn = sqlite3.connect("../Data/BTL_QLPT.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM NguoiDung WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        window.destroy()
        subprocess.run(["python", "../App/TrangChu.py"])  # Mở ứng dụng chính
    else:
        messagebox.showerror("Lỗi đăng nhập", "Tài khoản hoặc mật khẩu không đúng!")

window = Tk()
window.title("Quản lý phòng trọ")
window.geometry("1200x700")
window.configure(bg="Powder Blue")
window.iconbitmap("../Picture_Icon/icon.ico")

tieude = Label(window, text="ĐĂNG NHẬP", font=("Times New Roman", 32), fg="white", bg="Powder Blue")
tk = Label(window, text="Tài khoản: ", font=("Arial", 18), fg="black", bg="Powder Blue")
tk_box = Entry(window, font=("Arial", 20), width=30)
mk = Label(window, text="Mật khẩu: ", font=("Arial", 18), fg="black", bg="Powder Blue")
mk_box = Entry(window, font=("Arial", 20), width=30, show="*")
dangnhap = Button(window, text="Đăng Nhập", fg="white", bg="#89CFF0", font=("Arial", 14), command=dang_nhap, width=15, height=2)

def kich_thuoc(event=None):
    rong = window.winfo_width()
    cao = window.winfo_height()

    tieude.place(x=rong//2 - 90, y=cao//5)
    tk.place(x=rong//3 - 100, y=cao//3)
    tk_box.place(x=rong//3 + 50, y=cao//3)
    mk.place(x=rong//3 - 100, y=cao//3 + 90)
    mk_box.place(x=rong//3 + 50, y=cao//3 + 90)
    dangnhap.place(x=rong//2 - 65, y=cao//3 + 200)

window.bind("<Configure>", kich_thuoc)
window.mainloop()
