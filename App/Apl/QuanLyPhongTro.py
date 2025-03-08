from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

def quan_ly_phong_tro(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    Label(parent_frame, text="Quản lý Phòng Trọ", font=("Times New Roman", 20), fg="blue", bg="white").pack(pady=10)

    Label(parent_frame, text="Danh sách Nhà:", font=("Times New Roman", 14), bg="white").place(x=20, y=50)
    columns_nha = ("MaNha", "Địa Chỉ", "MaVP")
    nha = ttk.Treeview(parent_frame, columns=columns_nha, show="headings", height=10)

    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 11), rowheight=25)
    style.configure("Treeview.Heading", font=("Arial", 13))

    nha.heading("MaNha", text="Mã Nhà")
    nha.heading("Địa Chỉ", text="Địa Chỉ")
    nha.heading("MaVP", text="Mã Văn Phòng")

    nha.column("MaNha", width=60, anchor=CENTER)
    nha.column("Địa Chỉ", width=400, anchor=CENTER)
    nha.column("MaVP", width=60, anchor=CENTER)
    nha.place(x=20, y=80, width=700, height=200)

    Label(parent_frame, text="Danh sách Phòng:", font=("Times New Roman", 14), bg="white").place(x=20, y=300)
    columns_phong = ("MaPhong", "MaNha", "TrangThai")
    phong = ttk.Treeview(parent_frame, columns=columns_phong, show="headings", height=10)

    phong.heading("MaPhong", text="Mã Phòng")
    phong.heading("MaNha", text="Mã Nhà")
    phong.heading("TrangThai", text="Trạng Thái")

    phong.column("MaPhong", width=60, anchor=CENTER)
    phong.column("MaNha", width=60, anchor=CENTER)
    phong.column("TrangThai", width=90, anchor=CENTER)

    phong.place(x=20, y=330, width=700, height=200)

    def ket_noi_csdl():
        return sqlite3.connect("../Data/BTL_QLPT.db")

    def hien_thi_danh_sach_nha():
        nha.delete(*nha.get_children())
        conn = ket_noi_csdl()
        cursor = conn.cursor()
        cursor.execute("SELECT MaNha, DiaChi, MaVP FROM NhaTro")
        rows = cursor.fetchall()
        for row in rows:
            nha.insert("", END, values=row)
        conn.close()

    def hien_thi_danh_sach_phong():
        phong.delete(*phong.get_children())
        conn = ket_noi_csdl()
        cursor = conn.cursor()
        cursor.execute("SELECT MaPhong, MaNha, TrangThai FROM PhongTro")
        rows = cursor.fetchall()
        for row in rows:
            phong.insert("", END, values=row)
        conn.close()

    hien_thi_danh_sach_nha()
    hien_thi_danh_sach_phong()
