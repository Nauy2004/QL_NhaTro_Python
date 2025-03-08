import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def quan_ly_hop_dong(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    def ket_noi_csdl():
        return sqlite3.connect("../Data/BTL_QLPT.db")

    def hien_thi_danh_sach():
        tree.delete(*tree.get_children())
        conn = ket_noi_csdl()
        cursor = conn.cursor()
        cursor.execute("SELECT MaHD, GiaPhong, ThoiGianBD, ThoiGianKT, CCCD FROM HopDong")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def them_hop_dong():
        gia_phong, tg_bd, tg_kt, cccd = gia_phong_var.get(), tg_bd_var.get(), tg_kt_var.get(), cccd_var.get()
        if not gia_phong or not tg_bd or not tg_kt or not cccd:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin")
            return
        conn = ket_noi_csdl()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO HopDong (GiaPhong, ThoiGianBD, ThoiGianKT, CCCD) VALUES (?, ?, ?, ?)",
                       (gia_phong, tg_bd, tg_kt, cccd))
        conn.commit()
        conn.close()
        hien_thi_danh_sach()
        messagebox.showinfo("Thành công", "Đã thêm hợp đồng")

    def sua_hop_dong():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hợp đồng để sửa")
            return
        mahd = tree.item(selected[0], "values")[0]
        conn = ket_noi_csdl()
        cursor = conn.cursor()
        cursor.execute("UPDATE HopDong SET GiaPhong=?, ThoiGianBD=?, ThoiGianKT=?, CCCD=? WHERE MaHD=?",
                       (gia_phong_var.get(), tg_bd_var.get(), tg_kt_var.get(), cccd_var.get(), mahd))
        conn.commit()
        conn.close()
        hien_thi_danh_sach()
        messagebox.showinfo("Thành công", "Đã cập nhật hợp đồng")

    def xoa_hop_dong():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hợp đồng để xóa")
            return
        mahd = tree.item(selected[0], "values")[0]
        conn = ket_noi_csdl()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM HopDong WHERE MaHD=?", (mahd,))
        conn.commit()
        conn.close()
        hien_thi_danh_sach()
        messagebox.showinfo("Thành công", "Đã xóa hợp đồng")

    frame = ttk.LabelFrame(parent_frame, text="Thông tin hợp đồng")
    frame.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame, text="Giá phòng:").grid(row=0, column=0, padx=5, pady=5)
    gia_phong_var = tk.StringVar()
    ttk.Entry(frame, textvariable=gia_phong_var).grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame, text="Thời gian bắt đầu:").grid(row=0, column=2, padx=5, pady=5)
    tg_bd_var = tk.StringVar()
    ttk.Entry(frame, textvariable=tg_bd_var).grid(row=0, column=3, padx=5, pady=5)

    ttk.Label(frame, text="Thời gian kết thúc:").grid(row=1, column=0, padx=5, pady=5)
    tg_kt_var = tk.StringVar()
    ttk.Entry(frame, textvariable=tg_kt_var).grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame, text="CCCD:").grid(row=1, column=2, padx=5, pady=5)
    cccd_var = tk.StringVar()
    ttk.Entry(frame, textvariable=cccd_var).grid(row=1, column=3, padx=5, pady=5)

    btn_frame = ttk.Frame(parent_frame)
    btn_frame.pack(fill="x", padx=10, pady=5)
    ttk.Button(btn_frame, text="Thêm", command=them_hop_dong).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Sửa", command=sua_hop_dong).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Xóa", command=xoa_hop_dong).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Làm mới", command=hien_thi_danh_sach).pack(side="left", padx=5)

    tree = ttk.Treeview(parent_frame, columns=("MaHD", "GiaPhong", "ThoiGianBD", "ThoiGianKT", "CCCD"), show="headings")
    for col in ("MaHD", "GiaPhong", "ThoiGianBD", "ThoiGianKT", "CCCD"):
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=5)
    tree.bind("<ButtonRelease-1>", lambda event: chon_hop_dong(event, tree, gia_phong_var, tg_bd_var, tg_kt_var, cccd_var))

    hien_thi_danh_sach()

def chon_hop_dong(event, tree, gia_phong_var, tg_bd_var, tg_kt_var, cccd_var):
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0], "values")
        gia_phong_var.set(values[1])
        tg_bd_var.set(values[2])
        tg_kt_var.set(values[3])
        cccd_var.set(values[4])
