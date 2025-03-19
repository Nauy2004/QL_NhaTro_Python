import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from tkcalendar import DateEntry
import openpyxl
from openpyxl.styles import Font, Border, Side, Alignment

from tkinter import ttk, messagebox, filedialog

# Định dạng tiền tệ VND
FORMAT_CURRENCY_VND = '#,##0 ₫'

def quan_ly_hoa_don(parent_frame): 
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Frame cho các chức năng
    frame_chuc_nang = tk.Frame(parent_frame, pady=10)
    frame_chuc_nang.pack(fill=tk.X)
    
    # Frame cho việc tìm kiếm
    frame_tim_kiem = tk.LabelFrame(frame_chuc_nang, text="Tìm kiếm", padx=5, pady=5)
    frame_tim_kiem.pack(side=tk.LEFT, padx=10)
    
    tk.Label(frame_tim_kiem, text="Mã hóa đơn:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    entry_ma_hoa_don_search = tk.Entry(frame_tim_kiem, width=15)
    entry_ma_hoa_don_search.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(frame_tim_kiem, text="Từ ngày:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
    entry_tu_ngay = DateEntry(frame_tim_kiem, width=12, background='darkblue', foreground='white', date_pattern='dd/MM/yyyy')
    entry_tu_ngay.grid(row=0, column=3, padx=5, pady=5)
    
    tk.Label(frame_tim_kiem, text="Đến ngày:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
    entry_den_ngay = DateEntry(frame_tim_kiem, width=12, background='darkblue', foreground='white', date_pattern='dd/MM/yyyy')
    entry_den_ngay.grid(row=0, column=5, padx=5, pady=5)
    
    btn_tim_kiem = tk.Button(frame_tim_kiem, text="Tìm kiếm", command=lambda: search_bills(entry_ma_hoa_don_search.get(), entry_tu_ngay.get_date(), entry_den_ngay.get_date(), tree_hoa_don))
    btn_tim_kiem.grid(row=0, column=6, padx=5, pady=5)
    
    # Frame cho các nút chức năng
    frame_buttons = tk.Frame(frame_chuc_nang)
    frame_buttons.pack(side=tk.RIGHT, padx=10)
    
    btn_them = tk.Button(frame_buttons, text="Thêm Hóa Đơn", command=lambda: show_bill_form(None, tree_hoa_don))
    btn_them.pack(side=tk.LEFT, padx=5)
    
    btn_sua = tk.Button(frame_buttons, text="Sửa", command=lambda: edit_selected_bill(tree_hoa_don))
    btn_sua.pack(side=tk.LEFT, padx=5)
    
    btn_xoa = tk.Button(frame_buttons, text="Xóa", command=lambda: delete_selected_bill(tree_hoa_don))
    btn_xoa.pack(side=tk.LEFT, padx=5)
    
    btn_xuat_excel = tk.Button(frame_buttons, text="Xuất Excel", command=lambda: export_to_excel(tree_hoa_don))
    btn_xuat_excel.pack(side=tk.LEFT, padx=5)
    
    btn_refresh = tk.Button(frame_buttons, text="Làm mới", command=lambda: refresh_data(tree_hoa_don))
    btn_refresh.pack(side=tk.LEFT, padx=5)
    
    # Frame cho bảng hiển thị hóa đơn
    frame_hoa_don = tk.Frame(parent_frame)
    frame_hoa_don.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Tạo Treeview để hiển thị hóa đơn
    columns = ('MaHoaDon', 'MaHD' , 'CCCD' , 'HoTen', 'SoTien', 'NgayLap' )
    tree_hoa_don = ttk.Treeview(frame_hoa_don, columns=columns, show='headings')
    
    # Định nghĩa tiêu đề các cột
    tree_hoa_don.heading('MaHoaDon', text='Mã Hóa Đơn')
    tree_hoa_don.heading('MaHD', text='Mã Hợp Đồng')
    tree_hoa_don.heading('NgayLap', text='Ngày Lập')
    tree_hoa_don.heading('SoTien', text='Số Tiền')
    tree_hoa_don.heading('HoTen', text='Họ Tên Người Thuê')
    tree_hoa_don.heading('CCCD', text='CCCD')
    
    # Định nghĩa độ rộng các cột
    tree_hoa_don.column('MaHoaDon', width=100, anchor=tk.CENTER)
    tree_hoa_don.column('MaHD', width=100, anchor=tk.CENTER)
    tree_hoa_don.column('NgayLap', width=150, anchor=tk.CENTER)
    tree_hoa_don.column('SoTien', width=150, anchor=tk.CENTER)
    tree_hoa_don.column('HoTen', width=200, anchor=tk.W)
    tree_hoa_don.column('CCCD', width=120, anchor=tk.CENTER)
    
    # Thêm thanh cuộn
    scrollbar = ttk.Scrollbar(frame_hoa_don, orient=tk.VERTICAL, command=tree_hoa_don.yview)
    tree_hoa_don.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree_hoa_don.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Đổ dữ liệu vào Treeview
    refresh_data(tree_hoa_don)
    
    # Panel hiển thị chi tiết hóa đơn khi click vào một hóa đơn
    frame_chi_tiet = tk.LabelFrame(parent_frame, text="Chi tiết hóa đơn", padx=10, pady=10)
    frame_chi_tiet.pack(fill=tk.X, padx=10, pady=10)
    
    # Thông tin chi tiết
    frame_info = tk.Frame(frame_chi_tiet)
    frame_info.pack(fill=tk.X)
    
    # Cột 1
    frame_col1 = tk.Frame(frame_info)
    frame_col1.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
    
    tk.Label(frame_col1, text="Mã hóa đơn:").grid(row=0, column=0, sticky=tk.W, pady=2)
    lbl_ma_hoa_don = tk.Label(frame_col1, text="", width=20)
    lbl_ma_hoa_don.grid(row=0, column=1, sticky=tk.W, pady=2)
    
    tk.Label(frame_col1, text="Ngày lập:").grid(row=1, column=0, sticky=tk.W, pady=2)
    lbl_ngay_lap = tk.Label(frame_col1, text="", width=20)
    lbl_ngay_lap.grid(row=1, column=1, sticky=tk.W, pady=2)
    
    tk.Label(frame_col1, text="Số tiền:").grid(row=2, column=0, sticky=tk.W, pady=2)
    lbl_so_tien = tk.Label(frame_col1, text="", width=20)
    lbl_so_tien.grid(row=2, column=1, sticky=tk.W, pady=2)
    
    # Cột 2
    frame_col2 = tk.Frame(frame_info)
    frame_col2.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
    
    tk.Label(frame_col2, text="Mã hợp đồng:").grid(row=0, column=0, sticky=tk.W, pady=2)
    lbl_ma_hd = tk.Label(frame_col2, text="", width=20)
    lbl_ma_hd.grid(row=0, column=1, sticky=tk.W, pady=2)
    
    tk.Label(frame_col2, text="Người thuê:").grid(row=1, column=0, sticky=tk.W, pady=2)
    lbl_ho_ten = tk.Label(frame_col2, text="", width=20)
    lbl_ho_ten.grid(row=1, column=1, sticky=tk.W, pady=2)
    
    tk.Label(frame_col2, text="CCCD:").grid(row=2, column=0, sticky=tk.W, pady=2)
    lbl_cccd = tk.Label(frame_col2, text="", width=20)
    lbl_cccd.grid(row=2, column=1, sticky=tk.W, pady=2)
    
    # Cột 3
    frame_col3 = tk.Frame(frame_info)
    frame_col3.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
    
    tk.Label(frame_col3, text="Giá phòng:").grid(row=0, column=0, sticky=tk.W, pady=2)
    lbl_gia_phong = tk.Label(frame_col3, text="", width=20)
    lbl_gia_phong.grid(row=0, column=1, sticky=tk.W, pady=2)
    
    tk.Label(frame_col3, text="Thời gian BĐ:").grid(row=1, column=0, sticky=tk.W, pady=2)
    lbl_thoi_gian_bd = tk.Label(frame_col3, text="", width=20)
    lbl_thoi_gian_bd.grid(row=1, column=1, sticky=tk.W, pady=2)
    
    tk.Label(frame_col3, text="Thời gian KT:").grid(row=2, column=0, sticky=tk.W, pady=2)
    lbl_thoi_gian_kt = tk.Label(frame_col3, text="", width=20)
    lbl_thoi_gian_kt.grid(row=2, column=1, sticky=tk.W, pady=2)
    
    # Định nghĩa hàm lấy thông tin chi tiết khi click vào một hóa đơn
    def item_selected(event):
        for selected_item in tree_hoa_don.selection():
            # Lấy ID của item được chọn
            item = tree_hoa_don.item(selected_item)
            record = item['values']
            
            # Hiển thị thông tin
            lbl_ma_hoa_don.config(text=record[0])
            lbl_ma_hd.config(text=record[1])
            lbl_cccd.config(text=record[2])
            lbl_ho_ten.config(text=record[3])
            lbl_so_tien.config(text=f"{record[4]:} VNĐ")
            lbl_ngay_lap.config(text=record[5])
            lbl_gia_phong.config(text=f"{record[6]:} VNĐ")
            
            # Lấy thông tin thời gian từ DB
            conn = ket_noi_csdl()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ThoiGianBD, ThoiGianKT FROM HopDong WHERE MaHD = ?
            ''', (record[1],))
            hop_dong_info = cursor.fetchone()
            conn.close()
            
            if hop_dong_info:
                lbl_thoi_gian_bd.config(text=hop_dong_info[0])
                lbl_thoi_gian_kt.config(text=hop_dong_info[1])
    
    # Gắn sự kiện khi click vào một hàng trong bảng
    tree_hoa_don.bind('<<TreeviewSelect>>', item_selected)
    
    # Frame cho các nút chức năng mới
    frame_new_buttons = tk.Frame(parent_frame)
    frame_new_buttons.pack(side=tk.RIGHT, padx=10, pady=10)
    
    btn_issue_invoice = tk.Button(frame_new_buttons, text="Phát hành Hóa Đơn", command=lambda: issue_invoice(tree_hoa_don))
    btn_issue_invoice.pack(side=tk.LEFT, padx=5)
    
    btn_issue_multiple_invoices = tk.Button(frame_new_buttons, text="Phát hành Nhiều Hóa Đơn", command=lambda: issue_multiple_invoices(tree_hoa_don))
    btn_issue_multiple_invoices.pack(side=tk.LEFT, padx=5)
    
    btn_another_function = tk.Button(frame_new_buttons, text="Chức năng khác", command=lambda: another_function(tree_hoa_don))
    btn_another_function.pack(side=tk.LEFT, padx=5)

    return parent_frame

# Hàm kết nối CSDL
def ket_noi_csdl():
    return sqlite3.connect("../Data/BTL_QLPT.db")

# Hàm lấy và hiển thị dữ liệu - đã sửa để sử dụng hàm ket_noi_csdl
def refresh_data(tree):
    # Xóa dữ liệu cũ
    for i in tree.get_children():
        tree.delete(i)
    
    # Kết nối CSDL và lấy dữ liệu
    conn = ket_noi_csdl()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT h.MaHoaDon, h.MaHD, n.CCCD, n.HoTen,
               h.SoTien, h.NgayLap, hd.GiaPhong
        FROM HoaDon h
        JOIN HopDong hd ON h.MaHD = hd.MaHD
        JOIN NguoiThue n ON hd.CCCD = n.CCCD
        ORDER BY h.NgayLap DESC
    ''')
    
    records = cursor.fetchall()
    conn.close()
    
    # Thêm dữ liệu vào Treeview
    for record in records:
        # Định dạng ngày tháng khi hiển thị
        try:
            date_obj = datetime.strptime(record[1], '%Y-%m-%d')
            formatted_date = date_obj.strftime('%d/%m/%Y')
        except:
            formatted_date = record[1]
        
        # Thêm dữ liệu vào hàng
        tree.insert('', tk.END, values=(
            record[0], 
            formatted_date, 
            record[2], 
            record[3], 
            record[4], 
            record[5], 
            record[6]
        ))

# Hàm tìm kiếm hóa đơn - đã sửa để sử dụng hàm ket_noi_csdl
def search_bills(ma_hoa_don, tu_ngay, den_ngay, tree):
    # Xóa dữ liệu cũ
    for i in tree.get_children():
        tree.delete(i)
    
    # Kết nối CSDL và tìm kiếm
    conn = ket_noi_csdl()
    cursor = conn.cursor()
    
    query = '''
        SELECT h.MaHoaDon, h.NgayLap, h.SoTien, h.MaHD, 
               n.HoTen, n.CCCD, hd.GiaPhong
        FROM HoaDon h
        JOIN HopDong hd ON h.MaHD = hd.MaHD
        JOIN NguoiThue n ON hd.CCCD = n.CCCD
        WHERE 1=1
    '''
    params = []
    
    if ma_hoa_don:
        query += " AND h.MaHoaDon LIKE ?"
        params.append(f"%{ma_hoa_don}%")
    
    if tu_ngay and den_ngay:
        # Chuyển đổi định dạng ngày
        tu_ngay_str = tu_ngay.strftime('%Y-%m-%d')
        den_ngay_str = den_ngay.strftime('%Y-%m-%d')
        
        query += " AND h.NgayLap BETWEEN ? AND ?"
        params.extend([tu_ngay_str, den_ngay_str])
    
    query += " ORDER BY h.NgayLap DESC"
    
    cursor.execute(query, params)
    records = cursor.fetchall()
    conn.close()
    
    # Thêm kết quả tìm kiếm vào Treeview
    for record in records:
        try:
            date_obj = datetime.strptime(record[1], '%Y-%m-%d')
            formatted_date = date_obj.strftime('%d/%m/%Y')
        except:
            formatted_date = record[1]
        
        tree.insert('', tk.END, values=(
            record[0], 
            formatted_date, 
            record[2], 
            record[3], 
            record[4], 
            record[5], 
            record[6]
        ))

# Điều chỉnh các hàm khác để sử dụng hàm ket_noi_csdl
def show_bill_form(edit_data, tree):
    bill_form = tk.Toplevel()
    bill_form.title("Thêm/Sửa Hóa Đơn")
    bill_form.geometry("500x350")
    
    # Frame cho form
    frame_form = tk.Frame(bill_form, padx=20, pady=20)
    frame_form.pack(fill=tk.BOTH, expand=True)
    
    # Các trường nhập liệu
    tk.Label(frame_form, text="Mã hóa đơn:").grid(row=0, column=0, sticky=tk.W, pady=5)
    entry_ma_hoa_don = tk.Entry(frame_form, width=30)
    entry_ma_hoa_don.grid(row=0, column=1, pady=5, padx=5)
    
    tk.Label(frame_form, text="Ngày lập:").grid(row=1, column=0, sticky=tk.W, pady=5)
    entry_ngay_lap = DateEntry(frame_form, width=28, background='darkblue', foreground='white', date_pattern='dd/MM/yyyy')
    entry_ngay_lap.grid(row=1, column=1, pady=5, padx=5)
    
    tk.Label(frame_form, text="Số tiền (VNĐ):").grid(row=2, column=0, sticky=tk.W, pady=5)
    entry_so_tien = tk.Entry(frame_form, width=30)
    entry_so_tien.grid(row=2, column=1, pady=5, padx=5)
    
    tk.Label(frame_form, text="Mã hợp đồng:").grid(row=3, column=0, sticky=tk.W, pady=5)
    
    # Combobox cho mã hợp đồng
    hop_dong_combo = ttk.Combobox(frame_form, width=28)
    hop_dong_combo.grid(row=3, column=1, pady=5, padx=5)
    
    # Lấy danh sách hợp đồng từ CSDL
    conn = ket_noi_csdl()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT hd.MaHD, n.HoTen 
        FROM HopDong hd
        JOIN NguoiThue n ON hd.CCCD = n.CCCD
    ''')
    hop_dong_list = cursor.fetchall()
    conn.close()
    
    # Tạo danh sách giá trị và hiển thị cho combobox
    hop_dong_values = [f"{hd[0]} - {hd[1]}" for hd in hop_dong_list]
    hop_dong_ids = [hd[0] for hd in hop_dong_list]
    hop_dong_combo['values'] = hop_dong_values
    
    # Thông tin bổ sung
    tk.Label(frame_form, text="Thông tin hợp đồng:").grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=10)
    
    lbl_info_nguoi_thue = tk.Label(frame_form, text="Người thuê: ")
    lbl_info_nguoi_thue.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=2)
    
    lbl_info_cccd = tk.Label(frame_form, text="CCCD: ")
    lbl_info_cccd.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=2)
    
    lbl_info_gia_phong = tk.Label(frame_form, text="Giá phòng: ")
    lbl_info_gia_phong.grid(row=7, column=0, columnspan=2, sticky=tk.W, pady=2)
    
    # Hàm hiển thị thông tin hợp đồng khi chọn
    def on_hop_dong_selected(event):
        selected = hop_dong_combo.current()
        if selected >= 0:
            ma_hd = hop_dong_ids[selected]
            
            # Lấy thông tin hợp đồng và người thuê
            conn = ket_noi_csdl()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT hd.GiaPhong, n.HoTen, n.CCCD
                FROM HopDong hd
                JOIN NguoiThue n ON hd.CCCD = n.CCCD
                WHERE hd.MaHD = ?
            ''', (ma_hd,))
            info = cursor.fetchone()
            conn.close()
            
            if info:
                lbl_info_nguoi_thue.config(text=f"Người thuê: {info[1]}")
                lbl_info_cccd.config(text=f"CCCD: {info[2]}")
                lbl_info_gia_phong.config(text=f"Giá phòng: {info[0]:,} VNĐ")
                
                # Tự động cập nhật số tiền nếu chưa có
                if not entry_so_tien.get():
                    entry_so_tien.delete(0, tk.END)
                    entry_so_tien.insert(0, info[0])
    
    hop_dong_combo.bind("<<ComboboxSelected>>", on_hop_dong_selected)
    
    # Nếu là sửa, điền thông tin có sẵn
    if edit_data:
        entry_ma_hoa_don.insert(0, edit_data[0])
        entry_ma_hoa_don.config(state='readonly')  # Không cho phép sửa mã
        
        # Điền ngày lập
        try:
            date_obj = datetime.strptime(edit_data[1], '%d/%m/%Y')
            entry_ngay_lap.set_date(date_obj)
        except:
            pass
        
        entry_so_tien.insert(0, edit_data[2])
        
        # Chọn hợp đồng trong combobox
        for i, ma_hd in enumerate(hop_dong_ids):
            if ma_hd == edit_data[3]:
                hop_dong_combo.current(i)
                on_hop_dong_selected(None)
                break
    
    # Frame cho các nút
    frame_buttons = tk.Frame(frame_form)
    frame_buttons.grid(row=8, column=0, columnspan=2, pady=15)
    
    # Hàm lưu hóa đơn
    def save_bill():
        # Lấy dữ liệu từ form
        ma_hoa_don = entry_ma_hoa_don.get()
        ngay_lap = entry_ngay_lap.get_date().strftime('%Y-%m-%d')
        
        try:
            so_tien = float(entry_so_tien.get().replace(',', ''))
        except ValueError:
            messagebox.showerror("Lỗi", "Số tiền không hợp lệ!")
            return
        
        selected = hop_dong_combo.current()
        if selected < 0:
            messagebox.showerror("Lỗi", "Vui lòng chọn hợp đồng!")
            return
        
        ma_hd = hop_dong_ids[selected]
        
        # Kiểm tra dữ liệu
        if not ma_hoa_don or not ngay_lap:
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        
        # Kết nối CSDL
        conn = ket_noi_csdl()
        cursor = conn.cursor()
        
        try:
            if edit_data:  # Cập nhật
                cursor.execute('''
                    UPDATE HoaDon
                    SET NgayLap = ?, SoTien = ?, MaHD = ?
                    WHERE MaHoaDon = ?
                ''', (ngay_lap, so_tien, ma_hd, ma_hoa_don))
                message = "Cập nhật hóa đơn thành công!"
            else:  # Thêm mới
                # Kiểm tra mã hóa đơn đã tồn tại chưa
                cursor.execute('SELECT MaHoaDon FROM HoaDon WHERE MaHoaDon = ?', (ma_hoa_don,))
                if cursor.fetchone():
                    messagebox.showerror("Lỗi", "Mã hóa đơn đã tồn tại!")
                    conn.close()
                    return
                
                cursor.execute('''
                    INSERT INTO HoaDon (MaHoaDon, NgayLap, SoTien, MaHD)
                    VALUES (?, ?, ?, ?)
                ''', (ma_hoa_don, ngay_lap, so_tien, ma_hd))
                message = "Thêm hóa đơn thành công!"
            
            conn.commit()
            messagebox.showinfo("Thông báo", message)
            bill_form.destroy()
            refresh_data(tree)
            
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi Database", str(e))
        finally:
            conn.close()
    
    # Nút lưu và hủy
    btn_save = tk.Button(frame_buttons, text="Lưu", width=10, command=save_bill)
    btn_save.pack(side=tk.LEFT, padx=5)
    
    btn_cancel = tk.Button(frame_buttons, text="Hủy", width=10, command=bill_form.destroy)
    btn_cancel.pack(side=tk.LEFT, padx=5)

# Hàm sửa hóa đơn đã chọn
def edit_selected_bill(tree):
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn hóa đơn cần sửa!")
        return
    
    selected_item = selected_items[0]
    values = tree.item(selected_item, 'values')
    
    # Mở form sửa với dữ liệu đã chọn
    show_bill_form(values, tree)

# Hàm xóa hóa đơn đã chọn
def delete_selected_bill(tree):
    selected_items = tree.selection()
    if not selected_items:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn hóa đơn cần xóa!")
        return
    
    result = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa hóa đơn này?")
    if not result:
        return
    
    selected_item = selected_items[0]
    ma_hoa_don = tree.item(selected_item, 'values')[0]
    
    # Kết nối CSDL và xóa
    conn = ket_noi_csdl()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM HoaDon WHERE MaHoaDon = ?', (ma_hoa_don,))
        conn.commit()
        messagebox.showinfo("Thông báo", "Xóa hóa đơn thành công!")
        refresh_data(tree)
    except sqlite3.Error as e:
        messagebox.showerror("Lỗi Database", str(e))
    finally:
        conn.close()
# Hàm xuất dữ liệu ra Excel mà không sử dụng pandas
def export_to_excel(tree):

    # Lấy tất cả dữ liệu từ Treeview
    data = []
    columns = ['Mã Hóa Đơn', 'Ngày Lập', 'Số Tiền', 'Mã Hợp Đồng', 'Họ Tên Người Thuê', 'CCCD', 'Giá Phòng']
    
    for item in tree.get_children():
        values = tree.item(item, 'values')
        data.append(list(values))
    
    # Tạo Workbook và Worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Hóa Đơn"
    
    # Thêm tiêu đề cột
    for col_num, column_title in enumerate(columns, 1):
        cell = ws.cell(row=1, column=col_num, value=column_title)
        cell.font = Font(bold=True)
    
    # Thêm dữ liệu vào các hàng
    for row_num, row_data in enumerate(data, 2):
        for col_num, cell_value in enumerate(row_data, 1):
            ws.cell(row=row_num, column=col_num, value=cell_value)
    
    # Lưu file
    try:
        file_path = tk.filedialog.asksaveasfilename(
            defaultextension='.xlsx',
            filetypes=[('Excel Files', '*.xlsx')],
            title='Lưu file Excel'
        )
        
        if file_path:
            wb.save(file_path)
            messagebox.showinfo("Thông báo", f"Đã xuất dữ liệu ra file: {file_path}")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi khi xuất Excel: {str(e)}")

# Hàm phát hành hóa đơn
def issue_invoice(tree):
    selected_items = tree.selection()
    print(selected_items)
    if not selected_items:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn hóa đơn cần phát hành!")
        return
    
    data = tree.item(selected_items[0], 'values')
    try:
        conn = ket_noi_csdl()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT h.MaHoaDon, h.MaHD, n.CCCD, n.HoTen,
                   h.SoTien, h.NgayLap, hd.GiaPhong
            FROM HoaDon h
            JOIN HopDong hd ON h.MaHD = hd.MaHD
            JOIN NguoiThue n ON hd.CCCD = n.CCCD
            WHERE h.MaHoaDon = ?
            ORDER BY h.NgayLap DESC
        ''',(data[0],))
        
        records = cursor.fetchall()
        conn.close()
        
        if not records:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để xuất.")
            return
        
        wb = openpyxl.Workbook()
        ws = wb.active
        
        # Thông tin nhà trọ
        ws['B2'] = 'Công Ty TNHH ABC'
        ws['B3'] = 'Địa chỉ: 123 Đường XYZ, Quận 1, TP.HCM'
        ws['B4'] = 'Điện thoại: 01234567890'
        
        # thông tin hóa đơn
        ws['B6'] = 'Mã hóa đơn'
        ws['C6'] = data[0]
        ws['B7'] = 'Mã hợp đồng'
        ws['C7'] = data[1]
        ws['B8'] = 'Họ tên'
        ws['C8'] = data[2]
        ws['B9'] = 'Ngày lập'
        ws['C9'] = data[3]
        ws['B10'] = 'Giá phòng'
        ws['C10'] = data[4]
        ws['B11'] = 'Số tiền'
        ws['C11'] = data[5]
        ws['B13'] = 'Tổng tiền:'
        ws['C13'] = '3,200,000 đ'
        
        # Định dạng cột
        ws.column_dimensions['B'].width = 20
        ws.column_dimensions['C'].width = 20
        ws.column_dimensions['D'].width = 15
        
        # Định dạng font và canh giữa
        for row in range(1, 13):
            for col in ['A', 'B', 'C']:
                if ws[f'{col}{row}'].value:
                    ws[f'{col}{row}'].font = Font(name='Arial', size=11)
                    ws[f'{col}{row}'].alignment = Alignment(vertical='center')
        
        # In đậm tên cột
        ws['A1'].font = Font(bold=True, size=12)
        
        # Thêm đường viền thick outside cho vùng từ A1 đến D14
        from openpyxl.styles import Border, Side
        
        # Áp dụng viền bao quanh cho từng ô trong vùng A1:D14
        for row in range(1, 15):  # 1 đến 14
            for col in ['A', 'B', 'C', 'D']:
                cell = ws[f'{col}{row}']
                
                # Khởi tạo border với style None (không có viền)
                border = Border(
                    left=Side(style=None),
                    right=Side(style=None),
                    top=Side(style=None),
                    bottom=Side(style=None)
                )
                
                # Đặt viền thick cho các ô ở biên ngoài
                if row == 1:  # Dòng đầu tiên
                    border.top = Side(style='thick')
                if row == 14:  # Dòng cuối cùng
                    border.bottom = Side(style='thick')
                if col == 'A':  # Cột đầu tiên
                    border.left = Side(style='thick')
                if col == 'D':  # Cột cuối cùng
                    border.right = Side(style='thick')
                
                # Áp dụng border cho ô
                cell.border = border
        
        # Save file
        wb.save('hoa_don.xlsx')
        messagebox.showinfo("Thông báo", "Xuất hóa đơn thành công! File hoa_don.xlsx đã được tạo.")
    
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

# Hàm chạy thử giao diện quản lý hóa đơn (đã loại bỏ chức năng tạo database)
def run_test():
    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ gốc
    
    hoa_don_window = quan_ly_hoa_don(root)
    
    root.mainloop()

# Chạy thử nếu chạy trực tiếp file này
if __name__ == "__main__":
    run_test()