from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

def quan_ly_phong_tro(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    parent_frame.grid_rowconfigure(0, weight=1)
    parent_frame.grid_columnconfigure(0, weight=1)
    parent_frame.grid_columnconfigure(1, weight=2)

    frame_nha = Frame(parent_frame, bg="white")
    frame_nha.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

    Label(frame_nha, text="Danh sách Tòa Nhà", font=("Times New Roman", 14, "bold"), bg="white").pack(pady=5)

    canvas = Canvas(frame_nha, bg="white")
    scrollbar = Scrollbar(frame_nha, orient=VERTICAL, command=canvas.yview)
    scrollable_frame = Frame(canvas, bg="white")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    frame_phong = Frame(parent_frame, bg="white")
    frame_phong.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

    Label(frame_phong, text="Danh sách Phòng", font=("Times New Roman", 14, "bold"), bg="white").pack(pady=5)

    columns_phong = ("MaPhong", "TrangThai", "GiaPhong")
    phong = ttk.Treeview(frame_phong, columns=columns_phong, show="headings", height=15)

    phong.heading("MaPhong", text="Mã Phòng")
    phong.heading("TrangThai", text="Trạng Thái")
    phong.heading("GiaPhong", text="Giá Phòng")

    phong.column("MaPhong", width=80, anchor=CENTER)
    phong.column("TrangThai", width=120, anchor=CENTER)
    phong.column("GiaPhong", width=80, anchor=CENTER)

    phong.pack(pady=10, fill=BOTH, expand=True)

    btn_them_phong = Button(frame_phong, text="Thêm Phòng", font=("Arial", 12), bg="white", fg="black",
                             command=lambda: them_phong(ma_nha_chon) if ma_nha_chon else messagebox.showwarning("Cảnh báo", "Vui lòng chọn tòa nhà trước!"))
    btn_them_phong.pack(pady=5)

    def ket_noi_csdl():
        return sqlite3.connect("../Data/BTL_QLPT.db")

    def hien_thi_danh_sach_nha():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        conn = ket_noi_csdl()
        cursor = conn.cursor()
        cursor.execute("SELECT MaNha, DiaChi FROM NhaTro")
        rows = cursor.fetchall()
        conn.close()

        for row_index, (ma_nha, dia_chi) in enumerate(rows):
            btn = Button(scrollable_frame, text=f"Tòa {ma_nha}\n{dia_chi}",
                         font=("Arial", 12), width=20, height=3,
                         bg="white", fg="black",
                         command=lambda m=ma_nha: hien_thi_danh_sach_phong(m))
            btn.grid(row=row_index // 2, column=row_index % 2, padx=5, pady=5)

        btn_them_nha = Button(scrollable_frame, text="+ Thêm Tòa Nhà", font=("Arial", 12), width=15, height=1, bg="white", fg="black", command=them_nha)
        btn_them_nha.grid(row=(len(rows) // 2) + 1, column=0, columnspan=2, pady=10)

    def hien_thi_danh_sach_phong(ma_nha):
        nonlocal ma_nha_chon
        ma_nha_chon = ma_nha
        phong.delete(*phong.get_children())

        conn = ket_noi_csdl()
        cursor = conn.cursor()
        cursor.execute("SELECT MaPhong, TrangThai, GiaPhong FROM PhongTro WHERE MaNha = ?", (ma_nha,))
        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            phong.insert("", END, values=row)

    def them_nha():
        def luu_nha():
            ma_nha = entry_ma_nha.get()
            dia_chi = entry_dia_chi.get()
            conn = ket_noi_csdl()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO NhaTro (MaNha, DiaChi) VALUES (?, ?)", (ma_nha, dia_chi))
            conn.commit()
            conn.close()
            top.destroy()
            hien_thi_danh_sach_nha()

        top = Toplevel()
        top.geometry("550x180")
        top.title("Thêm Tòa Nhà")
        Label(top, text="Mã Nhà:").pack()
        entry_ma_nha = Entry(top)
        entry_ma_nha.pack()
        Label(top, text="Địa Chỉ:").pack()
        entry_dia_chi = Entry(top)
        entry_dia_chi.pack()
        Button(top, text="Lưu", command=luu_nha).pack()

    def them_phong(ma_nha):
        if ma_nha is None:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn tòa nhà trước khi thêm phòng!")
            return

        def luu_phong():
            ma_phong = entry_ma_phong.get()
            trang_thai = entry_trang_thai.get()
            gia_phong = entry_gia_phong.get()
            conn = ket_noi_csdl()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO PhongTro (MaPhong, MaNha, TrangThai, GiaPhong) VALUES (?, ?, ?, ?)",
                           (ma_phong, ma_nha, trang_thai, gia_phong))
            conn.commit()
            conn.close()
            top.destroy()
            hien_thi_danh_sach_phong(ma_nha)

        top = Toplevel()
        top.title("Thêm Phòng")
        top.geometry("500x180")
        Label(top, text="Mã Phòng:").pack()
        entry_ma_phong = Entry(top)
        entry_ma_phong.pack()
        Label(top, text="Trạng Thái:").pack()
        entry_trang_thai = Entry(top)
        entry_trang_thai.pack()
        Label(top, text="Giá Phòng:").pack()
        entry_gia_phong = Entry(top)
        entry_gia_phong.pack()
        Button(top, text="Lưu", command=luu_phong).pack()

    ma_nha_chon = None
    hien_thi_danh_sach_nha()