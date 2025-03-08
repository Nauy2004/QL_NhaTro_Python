from tkinter import *
from tkinter import messagebox
import sqlite3
import subprocess

def dang_nhap():
    username = tk_box.get()
    password = mk_box.get()

    conn = sqlite3.connect("../Data/BTL_QLPT.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM NguoiDung WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        window.destroy()
        subprocess.run(["python", "TrangChu.py"])
    else:
        messagebox.showerror("Lỗi đăng nhập", "Tài khoản hoặc mật khẩu không đúng!")

window = Tk()
window.title("Quản lý phòng trọ")
window.geometry("1000x1000")
#window.geometry(f"{window.winfo_screenwidth()}x{window.winfo_screenheight()}")

tieude = Label(text = "ĐĂNG NHẬP", font = ("Arial", 27), fg = "#89CFF0")
tieude.place(x = 430, y = 250)

tk = Label(text = "Tài khoản: ", font = ("Arial", 18), fg = "black")
tk.place(x = 250, y = 350)
tk_box = Entry(window, font = ("Arial", 20), width = 30)
tk_box.place(x = 380, y = 350)

mk = Label(text = "Mật khẩu: ", font = ("Arial", 18), fg = "black")
mk.place(x = 250, y = 440)
mk_box = Entry(window, font = ("Arial", 20), width = 30, show = "*")
mk_box.place(x = 380, y = 440)

dangnhap = Button(text = "Đăng Nhập", fg = "white", bg = "#89CFF0", font = ("Arial", 14), command = dang_nhap)
dangnhap.place(x = 470, y = 540, width = 130, height = 50)

window.mainloop()