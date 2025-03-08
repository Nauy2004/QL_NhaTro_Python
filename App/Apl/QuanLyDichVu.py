import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def quan_ly_dich_vu(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    def ket_noi_csdl():
        return sqlite3.connect("../Data/BTL_QLPT.db")

    def hien_thi_danh_sach():
        tree.delete(*tree.get_children())
        conn = ket_noi_csdl()
        cursor = conn.cursor()
        cursor.execute("SELECT MaDV, TenDV, GiaDV FROM DichVu")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def them_dich_vu():
        madv, tendv, giadv = madv_box.get(), tendv_box.get(), giadv_box.get()
        if not madv or not tendv or not giadv:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin")
            return
        try:
            conn = ket_noi_csdl()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO DichVu (MaDV, TenDV, GiaDV) VALUES (?, ?, ?)", (madv, tendv, giadv))
            conn.commit()
            conn.close()
            hien_thi_danh_sach()
            messagebox.showinfo("Thành công", "Đã thêm dịch vụ")
        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi", "Mã dịch vụ đã tồn tại")

    def sua_dich_vu():
        madv, tendv, giadv = madv_box.get(), tendv_box.get(), giadv_box.get()
        if not madv:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dịch vụ để sửa")
            return
        conn = ket_noi_csdl()
        cursor = conn.cursor()
        cursor.execute("UPDATE DichVu SET TenDV=?, GiaDV=? WHERE MaDV=?", (tendv, giadv, madv))
        conn.commit()
        conn.close()
        hien_thi_danh_sach()
        messagebox.showinfo("Thành công", "Đã cập nhật thông tin dịch vụ")

    def xoa_dich_vu():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dịch vụ để xóa")
            return
        madv = tree.item(selected[0], "values")[0]
        conn = ket_noi_csdl()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM DichVu WHERE MaDV=?", (madv,))
        conn.commit()
        conn.close()
        hien_thi_danh_sach()
        messagebox.showinfo("Thành công", "Đã xóa dịch vụ")

    label = tk.Label(parent_frame, text="Quản lý Dịch Vụ", font=("Times New Roman", 20), fg="blue", bg="white")
    label.place(x=400, y=20)

    frame = ttk.LabelFrame(parent_frame, text="Thông tin dịch vụ")
    frame.place(x=20, y=60, width=900, height=100)

    ttk.Label(frame, text="Mã DV:", font=("Arial", 10)).place(x=5, y=7)
    madv_box = ttk.Entry(frame)
    madv_box.place(x=55, y=5, width=150, height=25)

    ttk.Label(frame, text="Tên DV:", font=("Arial", 10)).place(x=245, y=7)
    tendv_box = ttk.Entry(frame)
    tendv_box.place(x=300, y=5, width=150, height=25)

    ttk.Label(frame, text="Giá DV:", font=("Arial", 10)).place(x=485, y=7)
    giadv_box = ttk.Entry(frame)
    giadv_box.place(x=540, y=5, width=150, height=25)

    btn_frame = ttk.Frame(parent_frame)
    btn_frame.place(x=20, y=160, width=900, height=40)
    ttk.Button(btn_frame, text="Thêm", command=them_dich_vu).place(x=10, y=5, width=80)
    ttk.Button(btn_frame, text="Sửa", command=sua_dich_vu).place(x=100, y=5, width=80)
    ttk.Button(btn_frame, text="Xóa", command=xoa_dich_vu).place(x=190, y=5, width=80)
    ttk.Button(btn_frame, text="Làm mới", command=hien_thi_danh_sach).place(x=280, y=5, width=80)

    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 11), rowheight=25)
    style.configure("Treeview.Heading", font=("Arial", 13))

    cot = ("MaDV", "TenDV", "GiaDV")
    tree = ttk.Treeview(parent_frame, columns=cot, show="headings")
    for col in cot:
        tree.heading(col, text=col)
        tree.column(col, width=180, anchor="center")
    tree.place(x=20, y=215, width=900, height=350)

    def chon_dich_vu(event):
        selected = tree.selection()
        if selected:
            values = tree.item(selected[0], "values")
            madv_box.delete(0, tk.END)
            madv_box.insert(0, values[0])
            tendv_box.delete(0, tk.END)
            tendv_box.insert(0, values[1])
            giadv_box.delete(0, tk.END)
            giadv_box.insert(0, values[2])

    tree.bind("<ButtonRelease-1>", chon_dich_vu)
    hien_thi_danh_sach()
