from tkinter import *
from tkinter import messagebox
import sqlite3
import subprocess


def dang_ky():
    username = tk_box.get()
    employee_id = mnv_box.get()
    password = mk_box.get()
    confirm_password = mk2_box.get()
    role = "nhanvien"

    if password != confirm_password:
        messagebox.showerror("Lỗi", "Mật khẩu nhập lại không khớp!")
        return

    conn = sqlite3.connect("../Data/BTL_QLPT.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM NguoiDung WHERE username = ?", (username,))
    if cursor.fetchone():
        messagebox.showerror("Lỗi", "Tài khoản đã tồn tại!")
        conn.close()
        return

    cursor.execute("SELECT * FROM NhanVien WHERE MaNV = ?", (employee_id,))
    if not cursor.fetchone():
        messagebox.showerror("Lỗi", "Mã nhân viên không tồn tại!")
        conn.close()
        return

    cursor.execute("INSERT INTO NguoiDung (username, password, role, MaNV) VALUES (?, ?, ?, ?)",
                   (username, password, role, employee_id))
    conn.commit()
    conn.close()

    messagebox.showinfo("Thành công", "Đăng ký thành công!")
    window.destroy()
    subprocess.run(["python", "../App/TrangChu.py"])


window = Tk()
window.title("Đăng ký tài khoản")
window.geometry("1100x600")
window.configure(bg="Powder Blue")
window.iconbitmap("../Picture_Icon/icon.ico")

tieude = Label(window, text="ĐĂNG KÝ", font=("Times New Roman", 32), fg="white", bg="Powder Blue")
tk = Label(window, text="Tài khoản: ", font=("Arial", 18), fg="black", bg="Powder Blue")
tk_box = Entry(window, font=("Arial", 20), width=30)
mnv = Label(window, text="Mã nv: ", font=("Arial", 18), fg="black", bg="Powder Blue")
mnv_box = Entry(window, font=("Arial", 20), width=30)
mk = Label(window, text="Mật khẩu: ", font=("Arial", 18), fg="black", bg="Powder Blue")
mk_box = Entry(window, font=("Arial", 20), width=30, show="*")
mk2 = Label(window, text="Nhập lại mk: ", font=("Arial", 18), fg="black", bg="Powder Blue")
mk2_box = Entry(window, font=("Arial", 20), width=30, show="*")

dangky = Button(window, text="Đăng Ký", fg="white", bg="#89CFF0", font=("Arial", 14), command=dang_ky, width=15,
                height=2)


def kich_thuoc(event=None):
    rong = window.winfo_width()
    cao = window.winfo_height()

    tieude.place(x=rong // 2 - 90, y=cao // 7)
    tk.place(x=rong // 3 - 100, y=cao // 4)
    tk_box.place(x=rong // 3 + 50, y=cao // 4)
    mnv.place(x=rong // 3 - 100, y=cao // 4 + 60)
    mnv_box.place(x=rong // 3 + 50, y=cao // 4 + 60)
    mk.place(x=rong // 3 - 100, y=cao // 4 + 120)
    mk_box.place(x=rong // 3 + 50, y=cao // 4 + 120)
    mk2.place(x=rong // 3 - 100, y=cao // 4 + 180)
    mk2_box.place(x=rong // 3 + 50, y=cao // 4 + 180)
    dangky.place(x=rong // 2 - 65, y=cao // 4 + 260)


window.bind("<Configure>", kich_thuoc)

window.mainloop()