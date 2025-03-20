import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def quan_ly_hop_dong(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    def ket_noi_csdl():
        return sqlite3.connect("../Data/BTL_QLPT.db")

    def get_next_ma_hd():
        conn = ket_noi_csdl()
        cursor = conn.cursor()
        cursor.execute("SELECT MaHD FROM HopDong ORDER BY MaHD DESC LIMIT 1")
        last_ma_hd = cursor.fetchone()
        conn.close()

        if last_ma_hd:
            num = int(last_ma_hd[0]) + 1
        else:
            num = 1
        return f"{num:04d}"  # Định dạng 4 chữ số: 0001, 0002, ...

    def lay_danh_sach_phong_chua_co_hop_dong():
        conn = ket_noi_csdl()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT MaPhong 
            FROM PhongTro 
            WHERE MaPhong NOT IN (SELECT MaPhong FROM HopDong)
        ''')
        phong_list = cursor.fetchall()
        conn.close()
        return phong_list

    def cap_nhat_combobox_phong():
        phong_list = lay_danh_sach_phong_chua_co_hop_dong()
        ma_phong_combo['values'] = [phong[0] for phong in phong_list]
        ma_phong_combo.set("")  # Xóa lựa chọn hiện tại sau khi cập nhật
        if not phong_list:  # Nếu không còn mã phòng trống
            messagebox.showinfo("Thông báo", "Không còn phòng trống để thêm hợp đồng!")
            ma_phong_combo.config(state='disabled')  # Vô hiệu hóa Combobox
        else:
            ma_phong_combo.config(state='normal')  # Kích hoạt Combobox

    def hien_thi_danh_sach():
        tree.delete(*tree.get_children())
        conn = ket_noi_csdl()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT hd.MaHD, hd.MaPhong, pt.MaNha, hd.ThoiGianBD, hd.ThoiGianKT, hd.CCCD 
            FROM HopDong hd
            JOIN PhongTro pt ON hd.MaPhong = pt.MaPhong
        ''')
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()
        cap_nhat_combobox_phong()  # Cập nhật lại danh sách mã phòng sau khi hiển thị

    def them_hop_dong():
        ma_phong = ma_phong_combo.get()
        tg_bd = tg_bd_var.get()
        tg_kt = tg_kt_var.get()
        cccd = cccd_var.get()

        if not ma_phong or not tg_bd or not tg_kt or not cccd:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            # Tạo mã hợp đồng tự động
            ma_hd = get_next_ma_hd()

            # Lấy giá phòng từ bảng PhongTro dựa trên MaPhong
            conn = ket_noi_csdl()
            cursor = conn.cursor()

            # Thêm hợp đồng vào bảng HopDong
            cursor.execute('''
                INSERT INTO HopDong (MaHD, MaPhong, ThoiGianBD, ThoiGianKT, CCCD) 
                VALUES (?, ?, ?, ?, ?)
            ''', (ma_hd, ma_phong, tg_bd, tg_kt, cccd))
            conn.commit()
            conn.close()

            hien_thi_danh_sach()
            messagebox.showinfo("Thành công", "Đã thêm hợp đồng!")

            # Xóa các ô nhập liệu sau khi thêm
            ma_phong_combo.set("")
            tg_bd_var.set("")
            tg_kt_var.set("")
            cccd_var.set("")

        except sqlite3.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm hợp đồng: {str(e)}")
            if 'conn' in locals():
                conn.close()

    def sua_hop_dong():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hợp đồng để sửa!")
            return
        mahd = tree.item(selected[0], "values")[0]
        ma_phong = ma_phong_combo.get()

        if not ma_phong:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn mã phòng!")
            return

        try:
            # Lấy giá phòng mới từ bảng PhongTro dựa trên MaPhong
            conn = ket_noi_csdl()
            cursor = conn.cursor()
            cursor.execute("SELECT GiaPhong FROM PhongTro WHERE MaPhong=?", (ma_phong,))
            gia_phong_result = cursor.fetchone()
            if not gia_phong_result:
                messagebox.showerror("Lỗi", f"Không tìm thấy giá phòng cho mã phòng {ma_phong}!")
                conn.close()
                return
            gia_phong = gia_phong_result[0]

            # Cập nhật hợp đồng
            cursor.execute('''
                UPDATE HopDong 
                SET MaPhong=?, GiaPhong=?, ThoiGianBD=?, ThoiGianKT=?, CCCD=? 
                WHERE MaHD=?
            ''', (ma_phong, gia_phong, tg_bd_var.get(), tg_kt_var.get(), cccd_var.get(), mahd))
            conn.commit()
            conn.close()

            hien_thi_danh_sach()
            messagebox.showinfo("Thành công", "Đã cập nhật hợp đồng!")

        except sqlite3.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật hợp đồng: {str(e)}")
            if 'conn' in locals():
                conn.close()

    def xoa_hop_dong():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hợp đồng để xóa!")
            return
        mahd = tree.item(selected[0], "values")[0]
        try:
            conn = ket_noi_csdl()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM HopDong WHERE MaHD=?", (mahd,))
            conn.commit()
            conn.close()
            hien_thi_danh_sach()
            messagebox.showinfo("Thành công", "Đã xóa hợp đồng!")
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa hợp đồng: {str(e)}")
            if 'conn' in locals():
                conn.close()

    frame = ttk.LabelFrame(parent_frame, text="Thông tin hợp đồng")
    frame.pack(fill="x", padx=10, pady=5)

    # Mã phòng (Combobox)
    ttk.Label(frame, text="Mã phòng:").grid(row=0, column=0, padx=5, pady=5)
    ma_phong_combo = ttk.Combobox(frame, width=18)
    ma_phong_combo.grid(row=0, column=1, padx=5, pady=5)
    cap_nhat_combobox_phong()  # Khởi tạo danh sách mã phòng

    # Thời gian bắt đầu
    ttk.Label(frame, text="Thời gian bắt đầu:").grid(row=0, column=2, padx=5, pady=5)
    tg_bd_var = tk.StringVar()
    ttk.Entry(frame, textvariable=tg_bd_var).grid(row=0, column=3, padx=5, pady=5)

    # Thời gian kết thúc
    ttk.Label(frame, text="Thời gian kết thúc:").grid(row=1, column=0, padx=5, pady=5)
    tg_kt_var = tk.StringVar()
    ttk.Entry(frame, textvariable=tg_kt_var).grid(row=1, column=1, padx=5, pady=5)

    # CCCD
    ttk.Label(frame, text="CCCD:").grid(row=1, column=2, padx=5, pady=5)
    cccd_var = tk.StringVar()
    ttk.Entry(frame, textvariable=cccd_var).grid(row=1, column=3, padx=5, pady=5)

    btn_frame = ttk.Frame(parent_frame)
    btn_frame.pack(fill="x", padx=10, pady=5)
    ttk.Button(btn_frame, text="Thêm", command=them_hop_dong).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Sửa", command=sua_hop_dong).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Xóa", command=xoa_hop_dong).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Làm mới", command=hien_thi_danh_sach).pack(side="left", padx=5)

    tree = ttk.Treeview(parent_frame, columns=("MaHD", "MaPhong", "MaNha", "ThoiGianBD", "ThoiGianKT", "CCCD"), show="headings")
    tree.heading("MaHD", text="Mã HĐ")
    tree.heading("MaPhong", text="Mã Phòng")
    tree.heading("MaNha", text="Mã Nhà")
    tree.heading("ThoiGianBD", text="Thời Gian BD")
    tree.heading("ThoiGianKT", text="Thời Gian KT")
    tree.heading("CCCD", text="CCCD")
    for col in ("MaHD", "MaPhong", "MaNha", "ThoiGianBD", "ThoiGianKT", "CCCD"):
        tree.column(col, width=120, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=5)
    tree.bind("<ButtonRelease-1>", lambda event: chon_hop_dong(event, tree, ma_phong_combo, tg_bd_var, tg_kt_var, cccd_var))

    hien_thi_danh_sach()

def chon_hop_dong(event, tree, ma_phong_combo, tg_bd_var, tg_kt_var, cccd_var):
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0], "values")
        ma_phong_combo.set(values[1])  # Cập nhật combobox mã phòng
        tg_bd_var.set(values[4])
        tg_kt_var.set(values[5])
        cccd_var.set(values[6])

# Hàm chạy thử giao diện
def run_test():
    root = tk.Tk()
    root.title("Quản lý hợp đồng")
    root.geometry("800x600")
    quan_ly_hop_dong(root)
    root.mainloop()

if __name__ == "__main__":
    run_test()