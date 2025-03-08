import tkinter as tk
import tkinter
from tkinter import ttk, messagebox
import sqlite3
import csv

def quan_ly_nguoi_thue(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    def hien_thi_danh_sach():
        tree.delete(*tree.get_children())
        conn = ket_noi_csdl()
        cursor = conn.cursor()
        cursor.execute("SELECT CCCD, HoTen, GioiTinh, SDT, DiaChi FROM NguoiThue")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def them_khach_hang():
        cccd, name, gender, phone, address = cccd_box.get(), ten_box.get(), gt_combobox.get(), sdt_box.get(), dchi_box.get()
        if not cccd or not name:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập CCCD và Họ tên")
            return
        try:
            conn = ket_noi_csdl()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO NguoiThue (CCCD, HoTen, GioiTinh, SDT, DiaChi) VALUES (?, ?, ?, ?, ?)", (cccd, name, gender, phone, address))
            conn.commit()
            conn.close()
            hien_thi_danh_sach()
            messagebox.showinfo("Thành công", "Đã thêm khách hàng")
        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi", "CCCD đã tồn tại")

    def sua_khach_hang():
        cccd, name, gender, phone, address = cccd_box.get(), ten_box.get(), gt_combobox.get(), sdt_box.get(), dchi_box.get()
        if not cccd:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng để sửa")
            return
        conn = ket_noi_csdl()
        cursor = conn.cursor()
        cursor.execute("UPDATE NguoiThue SET HoTen=?, GioiTinh=?, SDT=?, DiaChi=? WHERE CCCD=?", (name, gender, phone, address, cccd))
        conn.commit()
        conn.close()
        hien_thi_danh_sach()
        messagebox.showinfo("Thành công", "Đã cập nhật thông tin khách hàng")

    def xoa_khach_hang():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng để xóa")
            return
        cccd = tree.item(selected[0], "values")[0]
        conn = ket_noi_csdl()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM NguoiThue WHERE CCCD=?", (cccd,))
        conn.commit()
        conn.close()
        hien_thi_danh_sach()
        messagebox.showinfo("Thành công", "Đã xóa khách hàng")

    label = tkinter.Label(parent_frame, text="Quản lý Khách Hàng", font=("Times New Roman", 20), fg="blue", bg="white")
    label.place(x=400, y=20)

    frame = ttk.LabelFrame(parent_frame, text="Thông tin khách hàng")
    frame.place(x=20, y=60, width=900, height=100)

    ttk.Label(frame, text="CCCD:", font=("Arial", 10)).place(x=5, y=5)
    cccd_box = ttk.Entry(frame)
    cccd_box.place(x=55, y=5, width=150, height=25)

    ttk.Label(frame, text="Họ Tên:", font=("Arial", 10)).place(x=245, y=5)
    ten_box = ttk.Entry(frame)
    ten_box.place(x=300, y=5, width=150, height=25)

    ttk.Label(frame, text="Giới Tính:", font=("Arial", 10)).place(x=475, y=5)
    gt = tk.StringVar()
    gt_combobox = ttk.Combobox(frame, textvariable=gt, values=["Nam", "Nữ"], state="readonly")
    gt_combobox.place(x=540, y=5, width=100, height=25)
    gt_combobox.current(0)

    ttk.Label(frame, text="SĐT:", font=("Arial", 10)).place(x=5, y=35)
    sdt_box = ttk.Entry(frame)
    sdt_box.place(x=55, y=35, width=150, height=25)

    ttk.Label(frame, text="Địa Chỉ:", font=("Arial", 10)).place(x=245, y=35)
    dchi_box = ttk.Entry(frame)
    dchi_box.place(x=300, y=35, width=150, height=25)

    btn_frame = ttk.Frame(parent_frame)
    btn_frame.place(x=20, y=160, width=900, height=40)
    ttk.Button(btn_frame, text="Thêm", command=them_khach_hang).place(x=10, y=5, width=80)
    ttk.Button(btn_frame, text="Sửa", command=sua_khach_hang).place(x=100, y=5, width=80)
    ttk.Button(btn_frame, text="Xóa", command=xoa_khach_hang).place(x=190, y=5, width=80)
    ttk.Button(btn_frame, text="Làm mới", command=hien_thi_danh_sach).place(x=280, y=5, width=80)

    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 11), rowheight=25)
    style.configure("Treeview.Heading", font=("Arial", 13))

    columns = ("CCCD", "Họ Tên", "Giới Tính", "SĐT", "Địa Chỉ")
    tree = ttk.Treeview(parent_frame, columns=columns, show="headings")
    for i, col in enumerate(columns):
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.place(x=20, y=215, width=900, height=350)

    def ket_noi_csdl():
        return sqlite3.connect("../Data/BTL_QLPT.db")

    def chon_khach_hang(event):
        selected = tree.selection()
        if selected:
            values = tree.item(selected[0], "values")
            cccd_box.delete(0, tk.END)
            cccd_box.insert(0, values[0])
            ten_box.delete(0, tk.END)
            ten_box.insert(0, values[1])
            gt_combobox.set(values[2])
            sdt_box.delete(0, tk.END)
            sdt_box.insert(0, values[3])
            dchi_box.delete(0, tk.END)
            dchi_box.insert(0, values[4])
    tree.bind("<ButtonRelease-1>", chon_khach_hang)
    hien_thi_danh_sach()