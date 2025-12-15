import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 
from datetime import datetime

# --- KHAI BÁO MÀU NỀN CHUNG ---
LIGHT_BLUE_BG = '#E0FFFF' # Màu xanh nhạt (Light Cyan)
# ------------------------------

# =================================================================
#                         DỮ LIỆU GIẢ ĐỊNH
# =================================================================

# 1. Dữ liệu tài khoản đăng nhập (Phân quyền: admin/staff)
MOCK_USERS = {
    "admin": {"password": "123", "role": "admin"},
    "nhanvien01": {"password": "456", "role": "staff"},
    "nhanvien02": {"password": "789", "role": "staff"} 
}

# 2. Dữ liệu Menu (Mô phỏng Menu Tiệm Nhà Sóc Nhím)
MOCK_MENU_LIST = [
    {"name": "Trà Sữa Kem Trứng Dừa Nướng", "price": 25000},
    {"name": "Trà Sữa Truyền Thống", "price": 20000},
    {"name": "Trà Sữa Thái Xanh", "price": 20000},
    {"name": "Trà Sữa Bánh Flan", "price": 25000},
    {"name": "Cà Phê Muối", "price": 20000},
    {"name": "Cà Phê Sữa (Đá/Nóng)", "price": 20000},
    {"name": "Bạc Xỉu (Đá/Nóng)", "price": 20000},
    {"name": "Soda Việt Quất", "price": 15000},
    {"name": "Soda Đào", "price": 15000},
    {"name": "Soda Blue", "price": 15000},
    {"name": "Trà Tắc Xí Muội", "price": 15000},
    {"name": "Trà Đào", "price": 20000},
    {"name": "Trà Kiwi", "price": 20000},
    {"name": "Sữa Chua Đá", "price": 20000},
]

# 3. Dữ liệu Nhân viên (Quản lý Nhân viên)
MOCK_STAFF = [
    {"id": 1, "name": "Nguyễn Văn A", "username": "nhanvien01", "role": "staff"},
    {"id": 2, "name": "Trần Thị B", "username": "nhanvien02", "role": "staff"},
]
STAFF_ID_COUNTER = 3

# 4. Dữ liệu Hóa đơn (Đã thêm trường 'location' và 'item_count' cho hóa đơn mới)
MOCK_INVOICES = [
    {"id": 1, "staff": "Nhân viên Order", "time": "2025-12-14 10:00:00", "location": "Không rõ", "item_count": 3, "items": [("Cà Phê Đen", [2, 20000]), ("Trà Đào", [1, 30000])], "total": 70000},
    {"id": 2, "staff": "Nhân viên Order", "time": "2025-12-14 11:30:00", "location": "Không rõ", "item_count": 3, "items": [("Trà Sữa Trân Châu", [3, 35000])], "total": 105000}
]
INVOICE_COUNTER = 3 

# =================================================================
#                         CHỨC NĂNG CHUNG
# =================================================================

def format_currency(amount):
    """Định dạng tiền tệ sang VND"""
    # Xử lý trường hợp amount không phải số
    try:
        amount = int(amount)
    except (TypeError, ValueError):
        return "0₫"
        
    return f"{amount:,.0f}".replace(",", ".") + "₫"


# =================================================================
#                         LỚP CHÍNH CỦA ỨNG DỤNG
# =================================================================

class QuanNuocApp:
    def __init__(self, master):
        self.master = master
        master.title("Ứng Dụng Quán Nước")
        master.geometry("1000x650") 

        self.user_role = None
        self.current_page = None

        self.show_login_page()

    def clear_page(self):
        """Xóa tất cả widget trên cửa sổ hiện tại."""
        if self.current_page:
            for widget in self.current_page.winfo_children():
                widget.destroy()
            self.current_page.destroy()
        
    def show_login_page(self):
        """Hiển thị giao diện đăng nhập."""
        self.clear_page()
        self.master.geometry("800x600") 
        self.master.title("Ứng Dụng Quán Nước")
        self.current_page = LoginPage(self.master, self.login_success)
        self.current_page.pack(fill='both', expand=True)

    def login_success(self, role):
        """Hàm callback khi đăng nhập thành công."""
        self.user_role = role
        if role == "admin":
            self.show_admin_page()
        elif role == "staff":
            self.show_staff_page()
        else:
            messagebox.showerror("Lỗi", "Vai trò không hợp lệ.")

    def show_admin_page(self):
        """Hiển thị giao diện Admin."""
        self.clear_page()
        self.master.title("Ứng Dụng Quán Nước - Quản Lý")
        self.master.geometry("1000x650")
        self.current_page = AdminPage(self.master, self.show_login_page)
        self.current_page.pack(fill='both', expand=True)

    def show_staff_page(self):
        """Hiển thị giao diện Nhân viên (Order)."""
        self.clear_page()
        self.master.title("Ứng Dụng Quán Nước - Order")
        self.master.geometry("1000x650")
        self.current_page = StaffPage(self.master, self.show_login_page)
        self.current_page.pack(fill='both', expand=True)


# =================================================================
#                          LỚP ĐĂNG NHẬP
# =================================================================

class LoginPage(tk.Frame):
    def __init__(self, master, login_callback):
        super().__init__(master, bg=LIGHT_BLUE_BG) 
        self.login_callback = login_callback

        tk.Label(self, text="ĐĂNG NHẬP", font=('Arial', 20, 'bold'), bg=LIGHT_BLUE_BG).pack(pady=30) 
        
        input_frame = tk.Frame(self, bg=LIGHT_BLUE_BG) 
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Tên đăng nhập:", font=('Arial', 12), bg=LIGHT_BLUE_BG).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.username_entry = tk.Entry(input_frame, width=30, font=('Arial', 12))
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(input_frame, text="Mật khẩu:", font=('Arial', 12), bg=LIGHT_BLUE_BG).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.password_entry = tk.Entry(input_frame, width=30, show="*", font=('Arial', 12))
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self, text="ĐĂNG NHẬP", command=self.attempt_login, font=('Arial', 14, 'bold'), bg='green', fg='white').pack(pady=20)

    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in MOCK_USERS and MOCK_USERS[username]["password"] == password:
            role = MOCK_USERS[username]["role"]
            messagebox.showinfo("Thành công", f"Đăng nhập thành công! Vai trò: {role.upper()}")
            self.login_callback(role) 
        else:
            messagebox.showerror("Lỗi đăng nhập", "Tên đăng nhập hoặc mật khẩu không đúng!")


# =================================================================
#                          LỚP ADMIN (QUẢN LÝ)
# =================================================================

class AdminPage(tk.Frame):
    def __init__(self, master, logout_callback):
        super().__init__(master, bg=LIGHT_BLUE_BG) 
        self.logout_callback = logout_callback
        self.current_admin_sub_page = None
        
        tk.Label(self, text="GIAO DIỆN QUẢN LÝ (ADMIN)", font=('Arial', 24, 'bold'), fg='blue', bg=LIGHT_BLUE_BG).pack(pady=15)
        
        nav_frame = tk.Frame(self, bg=LIGHT_BLUE_BG) 
        nav_frame.pack(pady=10)

        tk.Button(nav_frame, text="Quản lý Menu", command=lambda: self.show_sub_page(MenuManagementPage), font=('Arial', 12), width=15).grid(row=0, column=0, padx=10)
        tk.Button(nav_frame, text="Quản lý Nhân viên", command=lambda: self.show_sub_page(StaffManagementPage), font=('Arial', 12), width=15).grid(row=0, column=1, padx=10)
        tk.Button(nav_frame, text="Xem Thống kê", command=lambda: self.show_sub_page(StatisticsPage), font=('Arial', 12), width=15).grid(row=0, column=2, padx=10)
        tk.Button(self, text="Đăng xuất", command=logout_callback, font=('Arial', 12), bg='red', fg='white').pack(pady=10)
        
        self.content_frame = tk.Frame(self, bg=LIGHT_BLUE_BG, bd=2, relief=tk.SUNKEN) 
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.show_sub_page(MenuManagementPage)

    def clear_sub_page(self):
        if self.current_admin_sub_page:
            self.current_admin_sub_page.destroy()

    def show_sub_page(self, PageClass):
        self.clear_sub_page()
        self.current_admin_sub_page = PageClass(self.content_frame)
        self.current_admin_sub_page.pack(fill='both', expand=True, padx=5, pady=5)


# --- Quản lý Menu (Admin) ---
class MenuManagementPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=LIGHT_BLUE_BG) 
        
        tk.Label(self, text="QUẢN LÝ DANH MỤC ĐỒ UỐNG", font=('Arial', 18, 'bold'), fg='DarkGreen', bg=LIGHT_BLUE_BG).pack(pady=10)
        
        main_frame = tk.Frame(self, bg=LIGHT_BLUE_BG) 
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        main_frame.grid_columnconfigure(0, weight=1) 
        main_frame.grid_columnconfigure(1, weight=0) 
        main_frame.grid_rowconfigure(0, weight=1)

        # 1. KHUNG DANH SÁCH MENU
        list_frame = tk.LabelFrame(main_frame, text="Danh sách Menu", font=('Arial', 12, 'bold'), bg=LIGHT_BLUE_BG) 
        list_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=5)
        
        self.tree_menu = ttk.Treeview(list_frame, columns=("price",), show="headings", height=15)
        
        # Cấu hình Tên món (cột #0)
        self.tree_menu.heading("#0", text="Tên món", anchor=tk.W)
        self.tree_menu.column("#0", stretch=tk.NO, width=200, anchor=tk.W) 
        
        self.tree_menu.heading("price", text="Giá (VND)", anchor=tk.E)
        self.tree_menu.column("price", anchor=tk.E, width=100)
        
        self.tree_menu.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.tree_menu.bind("<ButtonRelease-1>", self.load_menu_data_to_form)

        # 2. KHUNG THÊM/SỬA
        form_frame = tk.LabelFrame(main_frame, text="Thêm/Sửa Món", font=('Arial', 12, 'bold'), bg=LIGHT_BLUE_BG) 
        form_frame.grid(row=0, column=1, sticky='ns', padx=10, pady=5)
        
        tk.Label(form_frame, text="Tên món:", font=('Arial', 11), bg=LIGHT_BLUE_BG).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.item_name_entry = tk.Entry(form_frame, width=30)
        self.item_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Giá (VND):", font=('Arial', 11), bg=LIGHT_BLUE_BG).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.item_price_entry = tk.Entry(form_frame, width=30)
        self.item_price_entry.grid(row=1, column=1, padx=5, pady=5)
        
        btn_frame = tk.Frame(form_frame, bg=LIGHT_BLUE_BG) 
        btn_frame.grid(row=2, column=0, columnspan=2, pady=15)
        
        tk.Button(btn_frame, text="Thêm Mới", command=self.add_item, font=('Arial', 10, 'bold'), bg='green', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cập nhật", command=self.update_item, font=('Arial', 10, 'bold'), bg='blue', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Xóa", command=self.delete_item, font=('Arial', 10, 'bold'), bg='red', fg='white').pack(side=tk.LEFT, padx=5)
        
        self.load_menu_data()

    def load_menu_data(self):
        for i in self.tree_menu.get_children():
            self.tree_menu.delete(i)
            
        for item in MOCK_MENU_LIST:
            # Giá trị trong Treeview được định dạng (có dấu chấm)
            self.tree_menu.insert("", tk.END, text=item['name'], values=(f"{item['price']:,.0f}".replace(",", "."),))

    def load_menu_data_to_form(self, event):
        selected_item = self.tree_menu.focus()
        if selected_item:
            item_data = self.tree_menu.item(selected_item)
            name = item_data['text']
            # Bỏ dấu chấm để nhập vào Entry (Entry chỉ chấp nhận số)
            price_str = item_data['values'][0].replace(".", "") 
            
            self.item_name_entry.delete(0, tk.END)
            self.item_name_entry.insert(0, name)
            self.item_price_entry.delete(0, tk.END)
            self.item_price_entry.insert(0, price_str)
            
    def add_item(self):
        name = self.item_name_entry.get().strip()
        try:
            # Xóa dấu chấm phân cách hàng nghìn nếu có
            price = int(self.item_price_entry.get().replace(".", "").strip())
        except ValueError:
            messagebox.showerror("Lỗi", "Giá không hợp lệ. Vui lòng nhập số.")
            return

        if not name:
            messagebox.showerror("Lỗi", "Tên món không được để trống.")
            return

        if any(item['name'] == name for item in MOCK_MENU_LIST):
            messagebox.showwarning("Cảnh báo", "Món này đã tồn tại. Vui lòng sử dụng chức năng Cập nhật.")
            return
            
        MOCK_MENU_LIST.append({"name": name, "price": price})
        messagebox.showinfo("Thành công", f"Đã thêm món '{name}' thành công.")
        self.load_menu_data()
        self.item_name_entry.delete(0, tk.END)
        self.item_price_entry.delete(0, tk.END)
        
    def update_item(self):
        selected_item = self.tree_menu.focus()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn món cần cập nhật.")
            return
            
        old_name = self.tree_menu.item(selected_item, 'text')
        new_name = self.item_name_entry.get().strip()
        
        try:
            new_price = int(self.item_price_entry.get().replace(".", "").strip())
        except ValueError:
            messagebox.showerror("Lỗi", "Giá không hợp lệ. Vui lòng nhập số.")
            return
        
        for item in MOCK_MENU_LIST:
            if item['name'] == old_name:
                item['name'] = new_name
                item['price'] = new_price
                messagebox.showinfo("Thành công", f"Đã cập nhật món '{old_name}' thành công.")
                self.load_menu_data()
                return

    def delete_item(self):
        selected_item = self.tree_menu.focus()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn món cần xóa.")
            return
            
        name_to_delete = self.tree_menu.item(selected_item, 'text')
        
        if messagebox.askyesno("Xác nhận Xóa", f"Bạn có chắc chắn muốn xóa món '{name_to_delete}' không?"):
            global MOCK_MENU_LIST
            MOCK_MENU_LIST = [item for item in MOCK_MENU_LIST if item['name'] != name_to_delete]
            messagebox.showinfo("Thành công", f"Đã xóa món '{name_to_delete}'.")
            self.load_menu_data()
            self.item_name_entry.delete(0, tk.END)
            self.item_price_entry.delete(0, tk.END)


# --- Quản lý Nhân viên (Admin) ---
class StaffManagementPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=LIGHT_BLUE_BG) 
        
        tk.Label(self, text="QUẢN LÝ TÀI KHOẢN NHÂN VIÊN", font=('Arial', 18, 'bold'), fg='DarkOrange', bg=LIGHT_BLUE_BG).pack(pady=10)

        main_frame = tk.Frame(self, bg=LIGHT_BLUE_BG) 
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        main_frame.grid_columnconfigure(0, weight=1) 
        main_frame.grid_columnconfigure(1, weight=0) 
        main_frame.grid_rowconfigure(0, weight=1)

        # 1. KHUNG DANH SÁCH NHÂN VIÊN
        list_frame = tk.LabelFrame(main_frame, text="Danh sách Nhân viên", font=('Arial', 12, 'bold'), bg=LIGHT_BLUE_BG) 
        list_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=5)
        
        self.tree_staff = ttk.Treeview(list_frame, columns=("id", "username", "role"), show="headings", height=15)
        self.tree_staff.heading("id", text="ID", anchor=tk.CENTER)
        self.tree_staff.heading("#0", text="Họ tên", anchor=tk.W)
        self.tree_staff.heading("username", text="Username", anchor=tk.W)
        self.tree_staff.heading("role", text="Role", anchor=tk.CENTER)
        
        self.tree_staff.column("id", anchor=tk.CENTER, width=50)
        self.tree_staff.column("#0", stretch=tk.NO, width=200) 
        self.tree_staff.column("username", anchor=tk.W, width=120)
        self.tree_staff.column("role", anchor=tk.CENTER, width=80)
        
        self.tree_staff.pack(fill='both', expand=True, padx=5, pady=5)
        self.tree_staff.bind("<ButtonRelease-1>", self.load_staff_data_to_form)

        # 2. KHUNG THÊM/SỬA & RESET MẬT KHẨU
        form_frame = tk.LabelFrame(main_frame, text="Thêm/Sửa Tài khoản", font=('Arial', 12, 'bold'), bg=LIGHT_BLUE_BG) 
        form_frame.grid(row=0, column=1, sticky='ns', padx=10, pady=5)

        tk.Label(form_frame, text="Họ tên:", font=('Arial', 11), bg=LIGHT_BLUE_BG).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.staff_name_entry = tk.Entry(form_frame, width=30)
        self.staff_name_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Username:", font=('Arial', 11), bg=LIGHT_BLUE_BG).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.staff_username_entry = tk.Entry(form_frame, width=30)
        self.staff_username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(form_frame, text="Mật khẩu:", font=('Arial', 11), bg=LIGHT_BLUE_BG).grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.staff_password_entry = tk.Entry(form_frame, width=30, show='*')
        self.staff_password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        self.selected_staff_id = None 

        btn_frame = tk.Frame(form_frame, bg=LIGHT_BLUE_BG) 
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)
        
        tk.Button(btn_frame, text="Thêm Tài khoản", command=self.add_staff, font=('Arial', 10, 'bold'), bg='green', fg='white').pack(pady=5)
        tk.Button(btn_frame, text="Reset Mật khẩu (123)", command=self.reset_password, font=('Arial', 10, 'bold'), bg='orange', fg='white').pack(pady=5)
        tk.Button(btn_frame, text="Xóa Nhân viên", command=self.delete_staff, font=('Arial', 10, 'bold'), bg='red', fg='white').pack(pady=5)
        
        self.load_staff_data()

    def load_staff_data_to_form(self, event):
        selected_item = self.tree_staff.focus()
        if selected_item:
            item_data = self.tree_staff.item(selected_item)
            values = item_data['values']
            
            self.selected_staff_id = values[0]
            
            self.staff_name_entry.delete(0, tk.END)
            self.staff_name_entry.insert(0, item_data['text'])
            self.staff_username_entry.delete(0, tk.END)
            self.staff_username_entry.insert(0, values[1])
            self.staff_password_entry.delete(0, tk.END) 
            
    def load_staff_data(self):
        for i in self.tree_staff.get_children():
            self.tree_staff.delete(i)
            
        for staff in MOCK_STAFF:
            self.tree_staff.insert("", tk.END, text=staff['name'], values=(staff['id'], staff['username'], staff['role']))

    def add_staff(self):
        global STAFF_ID_COUNTER
        name = self.staff_name_entry.get().strip()
        username = self.staff_username_entry.get().strip()
        password = self.staff_password_entry.get().strip()

        if not name or not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng điền đủ Họ tên, Username và Mật khẩu.")
            return

        if any(staff['username'] == username for staff in MOCK_STAFF):
            messagebox.showwarning("Cảnh báo", "Username đã tồn tại.")
            return

        new_staff = {"id": STAFF_ID_COUNTER, "name": name, "username": username, "role": "staff"}
        MOCK_STAFF.append(new_staff)
        STAFF_ID_COUNTER += 1
        
        MOCK_USERS[username] = {"password": password, "role": "staff"} 
        
        messagebox.showinfo("Thành công", f"Đã tạo tài khoản '{username}' thành công.")
        self.load_staff_data()
        self.staff_name_entry.delete(0, tk.END)
        self.staff_username_entry.delete(0, tk.END)
        self.staff_password_entry.delete(0, tk.END)
        
    def reset_password(self):
        selected_item = self.tree_staff.focus()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên cần reset mật khẩu.")
            return
            
        username_to_reset = self.tree_staff.item(selected_item)['values'][1]
        
        if messagebox.askyesno("Xác nhận Reset", f"Bạn có chắc chắn muốn reset mật khẩu tài khoản '{username_to_reset}' về mặc định ('123') không?"): 
            if username_to_reset in MOCK_USERS:
                MOCK_USERS[username_to_reset]["password"] = "123"
                messagebox.showinfo("Thành công", f"Mật khẩu của '{username_to_reset}' đã được reset về '123'.")
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy tài khoản để reset mật khẩu.")

    def delete_staff(self):
        selected_item = self.tree_staff.focus()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên cần xóa.")
            return
            
        username_to_delete = self.tree_staff.item(selected_item)['values'][1]
        
        if messagebox.askyesno("Xác nhận Xóa", f"Bạn có chắc chắn muốn xóa nhân viên '{username_to_delete}' không?"):
            global MOCK_STAFF
            MOCK_STAFF = [staff for staff in MOCK_STAFF if staff['username'] != username_to_delete]
            
            if username_to_delete in MOCK_USERS:
                del MOCK_USERS[username_to_delete]
            
            messagebox.showinfo("Thành công", f"Đã xóa nhân viên '{username_to_delete}'.")
            self.load_staff_data()


# --- Xem Thống kê (Admin) ---
class StatisticsPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=LIGHT_BLUE_BG) 
        
        tk.Label(self, text="XEM THỐNG KÊ DOANH THU", font=('Arial', 18, 'bold'), fg='DarkBlue', bg=LIGHT_BLUE_BG).pack(pady=10)

        # Khung tổng kết
        summary_frame = tk.LabelFrame(self, text="Tổng kết nhanh", font=('Arial', 12, 'bold'), bg=LIGHT_BLUE_BG) 
        summary_frame.pack(fill='x', padx=20, pady=10)
        
        total_invoices = len(MOCK_INVOICES)
        total_revenue = sum(inv['total'] for inv in MOCK_INVOICES)
        
        tk.Label(summary_frame, text=f"Tổng số hóa đơn đã bán:", font=('Arial', 12), bg=LIGHT_BLUE_BG).grid(row=0, column=0, padx=10, pady=5, sticky='w')
        tk.Label(summary_frame, text=f"{total_invoices}", font=('Arial', 12, 'bold'), fg='blue', bg=LIGHT_BLUE_BG).grid(row=0, column=1, padx=10, pady=5, sticky='w')
        
        tk.Label(summary_frame, text=f"Tổng Doanh thu:", font=('Arial', 12), bg=LIGHT_BLUE_BG).grid(row=1, column=0, padx=10, pady=5, sticky='w')
        tk.Label(summary_frame, text=format_currency(total_revenue), font=('Arial', 14, 'bold'), fg='red', bg=LIGHT_BLUE_BG).grid(row=1, column=1, padx=10, pady=5, sticky='w')

        tk.Button(self, text="Xuất báo cáo (PDF/Excel)", command=self.export_report, font=('Arial', 12, 'bold'), bg='gray', fg='white').pack(pady=15) 
        
        tk.Label(self, text="Chi tiết các hóa đơn đã giao dịch:", font=('Arial', 14, 'bold'), bg=LIGHT_BLUE_BG).pack(pady=5)
        self.view_invoices(self)

    def export_report(self):
        messagebox.showinfo("Thông báo", "Chức năng Xuất báo cáo đang được phát triển.")
        
    def view_invoices(self, master):
        """Hiển thị danh sách hóa đơn (có cột Vị trí và SL món)"""
        
        tree_invoices = ttk.Treeview(master, columns=("id", "time", "location", "item_count", "total"), show="headings", height=15)
        
        tree_invoices.heading("id", text="ID Hóa Đơn", anchor=tk.CENTER)
        tree_invoices.heading("time", text="Thời gian", anchor=tk.CENTER)
        tree_invoices.heading("location", text="Vị trí", anchor=tk.CENTER)
        tree_invoices.heading("item_count", text="SL Món", anchor=tk.CENTER)
        tree_invoices.heading("total", text="Tổng tiền (VND)", anchor=tk.CENTER)
        
        tree_invoices.column("id", anchor=tk.CENTER, width=80)
        tree_invoices.column("time", anchor=tk.CENTER, width=150)
        tree_invoices.column("location", anchor=tk.CENTER, width=100)
        tree_invoices.column("item_count", anchor=tk.CENTER, width=80)
        tree_invoices.column("total", anchor=tk.E, width=120)

        tree_invoices.pack(fill='both', expand=True, padx=10, pady=5)
        
        for inv in MOCK_INVOICES:
            # Dùng .get để tránh lỗi nếu hóa đơn cũ thiếu trường
            location_info = inv.get('location', 'Không rõ') 
            item_count = inv.get('item_count', sum(data[0] for _, data in inv['items'])) # Tính lại nếu hóa đơn cũ không có
            
            tree_invoices.insert("", tk.END, values=(
                inv['id'], 
                inv['time'], 
                location_info,
                item_count,
                format_currency(inv['total']).replace("₫", "")
            ))
            
        tree_invoices.bind("<Double-1>", lambda event: self.show_invoice_details(event, tree_invoices))

    def show_invoice_details(self, event, tree):
        selected_item = tree.focus()
        if not selected_item:
            return

        # Lấy ID hóa đơn từ giá trị của dòng được chọn
        invoice_id_str = tree.item(selected_item, 'values')[0]
        
        invoice = next((inv for inv in MOCK_INVOICES if str(inv['id']) == invoice_id_str), None)
        
        if invoice:
            details = f"--- HÓA ĐƠN #{invoice['id']} ---\n"
            details += f"Thời gian: {invoice['time']}\n"
            details += f"Vị trí: {invoice.get('location', 'Không rõ')}\n"
            details += f"Nhân viên: {invoice['staff']}\n"
            details += "--------------------------------------\n"
            
            for item_name, data in invoice['items']:
                qty, price = data
                subtotal = qty * price
                details += f"{item_name}: {qty} x {format_currency(price)} = {format_currency(subtotal)}\n"
            
            details += "--------------------------------------\n"
            details += f"TỔNG CỘNG: {format_currency(invoice['total'])}"
            
            messagebox.showinfo(f"Chi Tiết Hóa Đơn #{invoice['id']}", details)


# =================================================================
#                          LỚP STAFF (ORDER)
# =================================================================

class StaffPage(tk.Frame):
    def __init__(self, master, logout_callback):
        super().__init__(master, bg=LIGHT_BLUE_BG) 
        self.logout_callback = logout_callback
        self.order_items = {} 
        self.current_table = tk.StringVar(value="Mang đi") 

        main_frame = tk.Frame(self, bg=LIGHT_BLUE_BG) 
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="GIAO DIỆN ĐẶT MÓN (ORDER) - NHÂN VIÊN", font=('Arial', 18, 'bold'), fg='green', bg=LIGHT_BLUE_BG).pack(pady=10) 

        content_frame = tk.Frame(main_frame, bg=LIGHT_BLUE_BG) 
        content_frame.pack(fill='both', expand=True, pady=10)
        
        content_frame.grid_columnconfigure(0, weight=1) 
        content_frame.grid_columnconfigure(1, weight=2) 
        content_frame.grid_rowconfigure(0, weight=1)

        # CỘT 1: MENU (CHỌN MÓN)
        menu_frame = tk.LabelFrame(content_frame, text="Menu Đồ uống", font=('Arial', 14, 'bold'), bg=LIGHT_BLUE_BG) 
        menu_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=5)
        
        menu_button_frame = tk.Frame(menu_frame, bg=LIGHT_BLUE_BG) 
        menu_button_frame.pack(padx=10, pady=10)

        menu_dict = {item['name']: item['price'] for item in MOCK_MENU_LIST}

        row_index = 0
        col_index = 0
        for item, price in menu_dict.items():
            command = lambda i=item, p=price: self.select_quantity(i, p) 
            
            tk.Button(menu_button_frame, 
                      text=f"{item}\n({format_currency(price)})",
                      command=command,
                      font=('Arial', 10, 'bold'), 
                      bg='#E0FFFF', width=14, height=3, 
                      relief=tk.RAISED
            ).grid(row=row_index, column=col_index, padx=5, pady=5)
            
            col_index += 1
            if col_index > 2: 
                col_index = 0
                row_index += 1

        # CỘT 2: HÓA ĐƠN & THANH TOÁN
        order_frame = tk.LabelFrame(content_frame, text="Hóa Đơn Hiện Tại", font=('Arial', 14, 'bold'), fg='darkred', bg=LIGHT_BLUE_BG) 
        order_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=5)
        
        # --- KHU VỰC CHỌN BÀN / MANG ĐI ---
        table_frame = tk.Frame(order_frame, bg=LIGHT_BLUE_BG)
        table_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(table_frame, text="Bàn/Hình thức:", font=('Arial', 12, 'bold'), bg=LIGHT_BLUE_BG).pack(side=tk.LEFT)
        
        table_options = ["Mang đi"] + [f"Bàn {i}" for i in range(1, 11)]
        
        self.table_combobox = ttk.Combobox(
            table_frame, 
            textvariable=self.current_table, 
            values=table_options,
            state="readonly",
            width=15,
            font=('Arial', 12)
        )
        self.table_combobox.pack(side=tk.LEFT, padx=10)
        self.table_combobox.set("Mang đi") 
        # ----------------------------------
        
        # SỬA LỖI HIỂN THỊ CỘT TRONG TREEVIEW
        self.tree = ttk.Treeview(order_frame, columns=("#0", "qty", "price", "subtotal"), show="headings", height=12) 
        
        # Cấu hình tiêu đề
        self.tree.heading("#0", text="Tên món nước", anchor=tk.W) # Cột Tên món
        self.tree.heading("qty", text="SL", anchor=tk.CENTER)
        self.tree.heading("price", text="Đơn giá (VND)", anchor=tk.E) # Cột giá tiền
        self.tree.heading("subtotal", text="Tổng (VND)", anchor=tk.E) # Cột tổng phụ
        
        # Cấu hình độ rộng cột
        self.tree.column("#0", anchor=tk.W, width=50) 
        self.tree.column("qty", anchor=tk.CENTER, width=50)
        self.tree.column("price", anchor=tk.E, width=120)
        self.tree.column("subtotal", anchor=tk.E, width=130)
        
        self.tree.pack(fill='x', padx=10, pady=10)

        total_frame = tk.Frame(order_frame, bg=LIGHT_BLUE_BG) 
        total_frame.pack(fill='x', padx=10, pady=5)
        tk.Label(total_frame, text="TỔNG CỘNG:", font=('Arial', 16, 'bold'), bg=LIGHT_BLUE_BG).pack(side=tk.LEFT)
        self.total_label = tk.Label(total_frame, text="0 VND", font=('Arial', 16, 'bold'), fg='red', bg=LIGHT_BLUE_BG)
        self.total_label.pack(side=tk.RIGHT)
        
        action_frame = tk.Frame(order_frame, bg=LIGHT_BLUE_BG) 
        action_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Button(action_frame, text="Xóa Món Đã Chọn", command=self.remove_item, font=('Arial', 10), bg='orange', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="XEM HÓA ĐƠN", command=self.view_invoices, font=('Arial', 10), bg='purple', fg='white').pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="IN HÓA ĐƠN", command=self.checkout, font=('Arial', 14, 'bold'), bg='green', fg='white').pack(side=tk.RIGHT) 

        tk.Button(main_frame, text="Đăng xuất", command=logout_callback, font=('Arial', 12), bg='red', fg='white').pack(pady=20)


    # --- LOGIC XỬ LÝ ORDER (Cập nhật cách hiển thị giá trị) ---

    def select_quantity(self, item_name, price):
        """Tạo cửa sổ pop-up để chọn số lượng món"""
        
        qty_window = tk.Toplevel(self)
        qty_window.title("Chọn Số Lượng")
        qty_window.geometry("300x150")
        qty_window.transient(self.master) 
        
        tk.Label(qty_window, text=f"Món: {item_name} ({format_currency(price)})", font=('Arial', 12, 'bold')).pack(pady=10)
        
        tk.Label(qty_window, text="Số lượng:", font=('Arial', 11)).pack()
        qty_var = tk.StringVar(value=1) 
        qty_spinbox = tk.Spinbox(qty_window, from_=1, to=100, width=5, font=('Arial', 11), textvariable=qty_var)
        qty_spinbox.pack(pady=5)
        
        def confirm_add():
            try:
                quantity = int(qty_var.get())
                if quantity > 0:
                    self.add_to_order(item_name, price, quantity)
                    qty_window.destroy() 
                else:
                    messagebox.showwarning("Lỗi", "Số lượng phải lớn hơn 0.")
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng không hợp lệ.")

        tk.Button(qty_window, text="Thêm vào Hóa đơn", command=confirm_add, font=('Arial', 11, 'bold'), bg='blue', fg='white').pack(pady=10)


    def add_to_order(self, item_name, price, quantity):
        """Xử lý chức năng Thêm Món với số lượng đã chọn"""
        
        if item_name in self.order_items:
            self.order_items[item_name][0] += quantity
        else:
            self.order_items[item_name] = [quantity, price] 
            
        self.update_order_display()

    def remove_item(self):
        """Xử lý chức năng Xóa Món Đã Chọn"""
        
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn món cần xóa trên hóa đơn.")
            return

        item_name = self.tree.item(selected_item, 'text')
        
        if item_name in self.order_items:
            
            response = messagebox.askyesnocancel(
                "Xóa món", 
                f"Bạn muốn giảm số lượng món '{item_name}' đi 1 hay xóa hoàn toàn khỏi hóa đơn?",
                icon='question', 
                type='yesnocancel', 
                default='yes',
                yes='Giảm số lượng', 
                no='Xóa hoàn toàn',
                cancel='Hủy'
            )
            
            if response is True: 
                self.order_items[item_name][0] -= 1
                if self.order_items[item_name][0] <= 0:
                    del self.order_items[item_name]
            elif response is False: 
                del self.order_items[item_name]
        
        self.update_order_display()
        
    def update_order_display(self):
        """Cập nhật Treeview và Tổng tiền"""
        
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        total_amount = 0
        
        for item_name, data in self.order_items.items():
            qty, price = data
            subtotal = qty * price
            total_amount += subtotal
            
            # CHỈNH SỬA CÁCH HIỂN THỊ GIÁ TRỊ (Bỏ ký hiệu ₫) để căn chỉnh trong cột Treeview
            self.tree.insert("", tk.END, text=item_name, values=(
                qty, 
                f"{price:,.0f}".replace(",", "."), 
                f"{subtotal:,.0f}".replace(",", ".")
            ))
            
        self.total_label.config(text=format_currency(total_amount))

    def checkout(self):
        """Xử lý chức năng In Hóa Đơn (Thanh toán) và thêm thông tin Bàn/Mang đi/SL món"""
        global MOCK_INVOICES, INVOICE_COUNTER
        
        if not self.order_items:
            messagebox.showwarning("Cảnh báo", "Hóa đơn trống. Vui lòng thêm món trước khi thanh toán.")
            return
            
        current_total = sum(data[0] * data[1] for data in self.order_items.values())
        item_count = sum(data[0] for data in self.order_items.values()) # Tính tổng số lượng món
        table_info = self.current_table.get()
        
        invoice_record = {
            "id": INVOICE_COUNTER,
            "staff": "Nhân viên Order", 
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "location": table_info, 
            "item_count": item_count, # Lưu tổng SL món
            "items": list(self.order_items.items()), 
            "total": current_total
        }
        MOCK_INVOICES.append(invoice_record)
        INVOICE_COUNTER += 1
        
        messagebox.showinfo("Thanh toán thành công", 
                            f"Hóa đơn #{invoice_record['id']} ({table_info}) đã được ghi lại.\nTổng tiền: {format_currency(current_total)}")
        
        # Reset hóa đơn hiện tại
        self.order_items = {}
        self.update_order_display()
        
    def view_invoices(self):
        """Mở cửa sổ mới hiển thị danh sách hóa đơn đã lưu"""
        
        view_window = tk.Toplevel(self)
        view_window.title("Danh Sách Hóa Đơn Đã Thanh Toán")
        view_window.geometry("800x450")
        
        tk.Label(view_window, text="Lịch Sử Hóa Đơn", font=('Arial', 16, 'bold'), fg='purple').pack(pady=10)

        tree_invoices = ttk.Treeview(view_window, columns=("id", "time", "location", "item_count", "total"), show="headings", height=15)
        
        tree_invoices.heading("id", text="ID Hóa Đơn", anchor=tk.CENTER)
        tree_invoices.heading("time", text="Thời gian", anchor=tk.CENTER)
        tree_invoices.heading("location", text="Vị trí", anchor=tk.CENTER)
        tree_invoices.heading("item_count", text="SL Món", anchor=tk.CENTER)
        tree_invoices.heading("total", text="Tổng tiền (VND)", anchor=tk.CENTER)
        
        tree_invoices.column("id", anchor=tk.CENTER, width=80)
        tree_invoices.column("time", anchor=tk.CENTER, width=150)
        tree_invoices.column("location", anchor=tk.CENTER, width=100)
        tree_invoices.column("item_count", anchor=tk.CENTER, width=80)
        tree_invoices.column("total", anchor=tk.E, width=120)

        tree_invoices.pack(fill='both', expand=True, padx=10, pady=5)
        
        for inv in MOCK_INVOICES:
            location_info = inv.get('location', 'Không rõ') 
            item_count = inv.get('item_count', sum(data[0] for _, data in inv['items']))
            
            tree_invoices.insert("", tk.END, values=(
                inv['id'], 
                inv['time'], 
                location_info, 
                item_count,
                format_currency(inv['total']).replace("₫", "")
            ))
            
        tree_invoices.bind("<Double-1>", lambda event: self.show_invoice_details(event, tree_invoices))

    def show_invoice_details(self, event, tree):
        selected_item = tree.focus()
        if not selected_item:
            return

        invoice_id_str = tree.item(selected_item, 'values')[0]
        
        invoice = next((inv for inv in MOCK_INVOICES if str(inv['id']) == invoice_id_str), None)
        
        if invoice:
            details = f"--- HÓA ĐƠN #{invoice['id']} ---\n"
            details += f"Thời gian: {invoice['time']}\n"
            details += f"Vị trí: {invoice.get('location', 'Không rõ')}\n"
            details += f"Nhân viên: {invoice['staff']}\n"
            details += "--------------------------------------\n"
            
            for item_name, data in invoice['items']:
                qty, price = data
                subtotal = qty * price
                details += f"{item_name}: {qty} x {format_currency(price)} = {format_currency(subtotal)}\n"
            
            details += "--------------------------------------\n"
            details += f"TỔNG CỘNG: {format_currency(invoice['total'])}"
            
            messagebox.showinfo(f"Chi Tiết Hóa Đơn #{invoice['id']}", details)

# =================================================================
#                         KHỞI CHẠY ỨNG DỤNG
# =================================================================

if __name__ == "__main__":
    
    root = tk.Tk()
    app = QuanNuocApp(root)
    root.mainloop()