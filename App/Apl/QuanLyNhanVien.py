import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def quan_ly_nhan_vien(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    def ket_noi_csdl():
        return sqlite3.connect("../Data/BTL_QLPT.db")

    def hien_thi_danh_sach():
        tree.delete(*tree.get_children())
        conn = ket_noi_csdl()
        cursor = conn.cursor()
        cursor.execute("SELECT MaNV, HoTen, GioiTinh, DiaChi, SDT, MaVP FROM NhanVien")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    def them_nhan_vien():
        manv, name, gender, address, phone, mavp = manv_box.get(), ten_box.get(), gt_combobox.get(), dchi_box.get(), sdt_box.get(), vp_combobox.get()
        if not manv or not name:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Mã nhân viên và Họ tên")
            return
        try:
            conn = ket_noi_csdl()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO NhanVien (MaNV, HoTen, GioiTinh, DiaChi, SDT, MaVP) VALUES (?, ?, ?, ?, ?, ?)", (manv, name, gender, address, phone, mavp))
            conn.commit()
            conn.close()
            hien_thi_danh_sach()
            messagebox.showinfo("Thành công", "Đã thêm nhân viên")
        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi", "Mã nhân viên đã tồn tại")

    def sua_nhan_vien():
        manv, name, gender, address, phone, mavp = manv_box.get(), ten_box.get(), gt_combobox.get(), dchi_box.get(), sdt_box.get(), vp_combobox.get()
        if not manv:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên để sửa")
            return
        conn = ket_noi_csdl()
        cursor = conn.cursor()
        cursor.execute("UPDATE NhanVien SET HoTen=?, GioiTinh=?, DiaChi=?, SDT=?, MaVP=? WHERE MaNV=?", (name, gender, address, phone, mavp, manv))
        conn.commit()
        conn.close()
        hien_thi_danh_sach()
        messagebox.showinfo("Thành công", "Đã cập nhật thông tin nhân viên")

    def xoa_nhan_vien():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên để xóa")
            return
        manv = tree.item(selected[0], "values")[0]
        conn = ket_noi_csdl()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM NhanVien WHERE MaNV=?", (manv,))
        conn.commit()
        conn.close()
        hien_thi_danh_sach()
        messagebox.showinfo("Thành công", "Đã xóa nhân viên")

    label = tk.Label(parent_frame, text="Quản lý Nhân Viên", font=("Times New Roman", 20), fg="blue", bg="white")
    label.place(x=400, y=20)

    frame = ttk.LabelFrame(parent_frame, text="Thông tin nhân viên")
    frame.place(x=20, y=60, width=900, height=120)

    ttk.Label(frame, text="Mã NV:", font=("Arial", 10)).place(x=5, y=5)
    manv_box = ttk.Entry(frame)
    manv_box.place(x=65, y=5, width=150, height=25)

    ttk.Label(frame, text="Họ Tên:", font=("Arial", 10)).place(x=245, y=5)
    ten_box = ttk.Entry(frame)
    ten_box.place(x=300, y=5, width=150, height=25)

    ttk.Label(frame, text="Giới Tính:", font=("Arial", 10)).place(x=475, y=5)
    gt_combobox = ttk.Combobox(frame, values=["Nam", "Nữ"], state="readonly")
    gt_combobox.place(x=540, y=5, width=100, height=25)
    gt_combobox.current(0)

    ttk.Label(frame, text="Địa Chỉ:", font=("Arial", 10)).place(x=5, y=35)
    dchi_box = ttk.Entry(frame)
    dchi_box.place(x=65, y=35, width=150, height=25)

    ttk.Label(frame, text="SĐT:", font=("Arial", 10)).place(x=245, y=35)
    sdt_box = ttk.Entry(frame)
    sdt_box.place(x=300, y=35, width=150, height=25)

    ttk.Label(frame, text="Mã VP:", font=("Arial", 10)).place(x=475, y=35)
    vp_combobox = ttk.Combobox(frame, values=["101", "102", "103"], state="readonly")
    vp_combobox.place(x=540, y=35, width=100, height=25)
    vp_combobox.current(0)

    btn_frame = ttk.Frame(parent_frame)
    btn_frame.place(x=20, y=180, width=900, height=40)
    ttk.Button(btn_frame, text="Thêm", command=them_nhan_vien).place(x=10, y=5, width=80)
    ttk.Button(btn_frame, text="Sửa", command=sua_nhan_vien).place(x=100, y=5, width=80)
    ttk.Button(btn_frame, text="Xóa", command=xoa_nhan_vien).place(x=190, y=5, width=80)
    ttk.Button(btn_frame, text="Làm mới", command=hien_thi_danh_sach).place(x=280, y=5, width=80)

    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 11), rowheight=30)
    style.configure("Treeview.Heading", font=("Arial", 13))

    columns = ("Mã NV", "Họ Tên", "Giới Tính", "Địa Chỉ", "SĐT", "Mã VP")
    tree = ttk.Treeview(parent_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=140, anchor="center")

    tree.place(x=20, y=230, width=900, height=350)

    def chon_nhan_vien(event):
        selected = tree.selection()
        if selected:
            values = tree.item(selected[0], "values")
            manv_box.delete(0, tk.END)
            manv_box.insert(0, values[0])
            ten_box.delete(0, tk.END)
            ten_box.insert(0, values[1])
            gt_combobox.set(values[2])
            dchi_box.delete(0, tk.END)
            dchi_box.insert(0, values[3])
            sdt_box.delete(0, tk.END)
            sdt_box.insert(0, values[4])
            vp_combobox.set(values[5])

    tree.bind("<ButtonRelease-1>", chon_nhan_vien)
    hien_thi_danh_sach()
