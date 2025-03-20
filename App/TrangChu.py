from tkinter import *
from tkinter import ttk
import subprocess
from PIL import Image, ImageTk
from Apl import QuanLyDichVu, QuanLyNguoiThue, QuanLyPhongTro, QuanLyNhanVien ,QuanLyHopDong, QuanLyHoaDon,XemThongTin

def trang_chu():
    subprocess.run(["python", "TrangChu.py"])

def dang_xuat():
    window.destroy()
    subprocess.run(["python", "DangNhap.py"])

def thoat():
    exit()

def kich_thuoc(event=None):
    dai = window.winfo_width()
    cao = window.winfo_height()
    frame_menu.place(x=0, y=0, width=250, height=cao)
    frame_main.place(x=250, y=0, width=dai - 250, height=cao)
    label_tieude.place(x=(dai - 250) // 2 - 200, y=10)
    frame_gioithieu.place(x=20, y=50, width=dai - 290, height=cao - 100)
    label_gt3.place(x=(dai - 250) // 2 - 150, y=20)
    label_gt2.place(x=(dai - 250) // 2 - 330, y=60)

    SL_buttons = len(buttons)
    khoang_cach_button = (cao - 100) // (SL_buttons + 1) + 5
    for i, button in enumerate(buttons):
        button.place(x=20, y=(i + 1) * khoang_cach_button, width=200, height=40)

window = Tk()
window.title("Quản lý phòng trọ")
window.geometry("1250x700")

# Áp dụng theme Clam
style = ttk.Style()
style.theme_use('clam')

# Màu sắc chính cho ứng dụng
PRIMARY_COLOR = "#3498db"      # Xanh dương đậm
SECONDARY_COLOR = "#2ecc71"    # Xanh lá
ACCENT_COLOR = "#e74c3c"       # Đỏ cam
BG_COLOR = "#ecf0f1"           # Xám nhạt
MENU_BG = "#34495e"            # Xám đậm/xanh đậm
TEXT_COLOR = "#2c3e50"         # Gần đen
TEXT_LIGHT = "#ffffff"         # Trắng

window.configure(bg=BG_COLOR)
window.iconbitmap("../Picture_Icon/icon.ico")

# Cấu hình style cho các widget
style.configure('TButton', 
                background=PRIMARY_COLOR, 
                foreground=TEXT_LIGHT, 
                font=('Arial', 11),
                padding=5)

style.map('TButton', 
          background=[('active', SECONDARY_COLOR), ('disabled', '#cccccc')],
          foreground=[('active', TEXT_LIGHT), ('disabled', '#888888')])

style.configure('TFrame', background=BG_COLOR)
style.configure('TLabel', background=BG_COLOR, foreground=TEXT_COLOR, font=('Arial', 11))
style.configure('Header.TLabel', font=('Arial', 16, 'bold'), foreground=PRIMARY_COLOR)
                
# Tạo frames sử dụng ttk thay vì Frame thông thường
frame_menu = ttk.Frame(window, style='Menu.TFrame')
style.configure('Menu.TFrame', background=MENU_BG)

frame_main = ttk.Frame(window)

# Label tiêu đề với style mới
label_tieude = ttk.Label(frame_main, text="ỨNG DỤNG QUẢN LÝ PHÒNG TRỌ", 
                         font=("Arial", 20, "bold"), foreground=PRIMARY_COLOR)

frame_gioithieu = ttk.Frame(frame_main, relief="solid", borderwidth=1)
style.configure('Card.TFrame', background='white', relief='solid', borderwidth=1)

# Chỉnh sửa các label giới thiệu
text_gt3 = "Phần mềm quản lý cho thuê"
label_gt3 = ttk.Label(frame_gioithieu, text="", font=("Arial", 16, "bold"), foreground=SECONDARY_COLOR)

def gt3(index=0):
    if index < len(text_gt3):
        label_gt3.config(text=text_gt3[:index + 1])
        window.after(250, gt3, index + 1)
gt3()

text_gt2 = "Hiệu quả - Chuyên nghiệp - Tránh sai sót... Quản lý chưa bao giờ dễ dàng hơn thế!"
label_gt2 = ttk.Label(frame_gioithieu, text="", font=("Arial", 14), foreground=TEXT_COLOR)

def gt2(index=0):
    if index < len(text_gt2):
        label_gt2.config(text=text_gt2[:index + 1])
        window.after(80, gt2, index + 1)
gt2()

# Thêm ảnh nền
img = Image.open("../Picture_Icon/bg1.png")
img = img.resize((1000, 660), Image.Resampling.LANCZOS)
bg_image = ImageTk.PhotoImage(img)
label_bg = Label(frame_gioithieu, image=bg_image)
label_bg.place(relwidth=1, relheight=1)

# Tạo các button với ttk
buttons = []

# Tạo style riêng cho các button đặc biệt
style.configure('Warning.TButton', background=ACCENT_COLOR, foreground=TEXT_LIGHT)
style.map('Warning.TButton', background=[('active', '#c0392b')])

style.configure('Menu.TButton', background=MENU_BG, foreground=TEXT_LIGHT, font=("Arial", 11))
style.map('Menu.TButton', background=[('active', PRIMARY_COLOR)])

buttons.extend([
    ttk.Button(frame_menu, text="Trang chủ", command=trang_chu),
    ttk.Button(frame_menu, text="Quản lý nhân viên", 
              command=lambda: QuanLyNhanVien.quan_ly_nhan_vien(frame_gioithieu)),
    ttk.Button(frame_menu, text="Tạo tài khoản nhân viên", 
              command=lambda: subprocess.run(["python", "DangKy.py"])),
    ttk.Button(frame_menu, text="Xem thông tin tài khoản", 
              command=lambda: XemThongTin.XemThongTin(frame_gioithieu)),
    ttk.Button(frame_menu, text="Phòng Trọ", 
              command=lambda: QuanLyPhongTro.quan_ly_phong_tro(frame_gioithieu)),
    ttk.Button(frame_menu, text="Người thuê", 
              command=lambda: QuanLyNguoiThue.quan_ly_nguoi_thue(frame_gioithieu)),
    ttk.Button(frame_menu, text="Hợp đồng thuê", 
              command=lambda: QuanLyHopDong.quan_ly_hop_dong(frame_gioithieu)),
    ttk.Button(frame_menu, text="Dịch vụ", 
              command=lambda: QuanLyDichVu.quan_ly_dich_vu(frame_gioithieu)),
    ttk.Button(frame_menu, text="Chỉ số điện nước"),
    ttk.Button(frame_menu, text="Hóa đơn",
               command=lambda: QuanLyHoaDon.quan_ly_hoa_don(frame_gioithieu)),
    ttk.Button(frame_menu, text="Thống kê",
               command=lambda: subprocess.run(["python", "Apl/dasboard,py"])),
    ttk.Button(frame_menu, text="Đăng xuất", style='Warning.TButton', command=dang_xuat),
    ttk.Button(frame_menu, text="Thoát ứng dụng", style='Warning.TButton', command=thoat)
])

# Thêm đường viền phân cách giữa menu và nội dung chính
separator = ttk.Separator(window, orient='vertical')
separator.place(x=250, y=0, height=700)

window.bind("<Configure>", kich_thuoc)
window.mainloop()