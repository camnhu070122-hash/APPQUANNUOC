import pandas as pd
from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import subprocess 

# --- CẤU HÌNH ---
DATA_FILE = 'student_data.csv'

# ====================================================================
# I. LỚP QUẢN LÝ DỮ LIỆU (BUSINESS LOGIC) - StudentManager
# ====================================================================

class StudentManager:
    """Quản lý logic nghiệp vụ và dữ liệu Sinh viên."""
    def __init__(self):
        file_exists = os.path.exists(DATA_FILE)
        
        if file_exists:
            try:
                self.df = pd.read_csv(DATA_FILE)
            except pd.errors.EmptyDataError:
                self.df = self._create_empty_dataframe()
        else:
            self.df = self._create_empty_dataframe()
            self._populate_initial_data() 
            
        if 'MaSV' in self.df.columns:
            self.df['MaSV'] = self.df['MaSV'].astype(str)

    def _create_empty_dataframe(self):
        """Tạo DataFrame rỗng với các cột cần thiết cho Sinh viên."""
        return pd.DataFrame(columns=[
            'MaSV', 'HoTen', 'NgaySinh', 'GioiTinh', 'Lop', 'DiemTrungBinh'
        ])

    def _save_data(self):
        """Lưu DataFrame hiện tại vào file CSV."""
        self.df.to_csv(DATA_FILE, index=False)

    def _populate_initial_data(self):
        """Tạo 10 bộ dữ liệu sinh viên mẫu với Mã SV 4 ký tự."""
        initial_data = [
           {'MaSV': 'S001', 'HoTen': 'Nguyễn Văn A', 'NgaySinh': '10/05/2001', 'GioiTinh': 'Nam', 'Lop': 'K64-CNTT1', 'DiemTrungBinh': 3.5},
            {'MaSV': 'S002', 'HoTen': 'Trần Thị B', 'NgaySinh': '22/08/2001', 'GioiTinh': 'Nữ', 'Lop': 'K64-CNTT1', 'DiemTrungBinh': 3.2},
            {'MaSV': 'S003', 'HoTen': 'Lê Minh C', 'NgaySinh': '01/11/2000', 'GioiTinh': 'Nam', 'Lop': 'K63-CNTT2', 'DiemTrungBinh': 2.8},
            {'MaSV': 'S004', 'HoTen': 'Phạm Hải D', 'NgaySinh': '15/01/2002', 'GioiTinh': 'Nam', 'Lop': 'K65-KT01', 'DiemTrungBinh': 3.8},
            {'MaSV': 'S005', 'HoTen': 'Hoàng Yến E', 'NgaySinh': '29/03/2001', 'GioiTinh': 'Nữ', 'Lop': 'K64-CNTT3', 'DiemTrungBinh': 3.0},
            {'MaSV': 'S006', 'HoTen': 'Vũ Đức F', 'NgaySinh': '07/07/2002', 'GioiTinh': 'Nam', 'Lop': 'K65-KT01', 'DiemTrungBinh': 2.5},
            {'MaSV': 'S007', 'HoTen': 'Đào Thu G', 'NgaySinh': '18/09/2000', 'GioiTinh': 'Nữ', 'Lop': 'K63-CNTT2', 'DiemTrungBinh': 3.9},
            {'MaSV': 'S008', 'HoTen': 'Huỳnh Đức H', 'NgaySinh': '04/04/2001', 'GioiTinh': 'Nam', 'Lop': 'K64-CNTT1', 'DiemTrungBinh': 3.1},
            {'MaSV': 'S009', 'HoTen': 'Ngô Kim I', 'NgaySinh': '30/12/2002', 'GioiTinh': 'Nữ', 'Lop': 'K65-KT02', 'DiemTrungBinh': 2.9},
            {'MaSV': 'S010', 'HoTen': 'Trịnh Bá K', 'NgaySinh': '16/06/2001', 'GioiTinh': 'Nam', 'Lop': 'K64-CNTT3', 'DiemTrungBinh': 3.4},
        ]
        self.df = pd.concat([self.df, pd.DataFrame(initial_data)], ignore_index=True)
        self._save_data()
    
    # ------------------ CHỨC NĂNG 1: THÊM SINH VIÊN ------------------
    def add_student(self, masv, hoten, ngaysinh, gioitinh, lop, dtb):
        """Thêm sinh viên mới (Có kiểm tra độ dài Mã SV)."""
        try:
            # KIỂM TRA ĐỘ DÀI
            if len(masv) != 4:
                return "Lỗi: Mã Sinh viên phải có đúng 4 ký tự."
                
            # Kiểm tra Mã SV đã tồn tại chưa
            if masv in self.df['MaSV'].values:
                return f"Lỗi: Mã Sinh viên {masv} đã tồn tại."
                
            new_row = {
                'MaSV': masv,
                'HoTen': hoten,
                'NgaySinh': ngaysinh,
                'GioiTinh': gioitinh,
                'Lop': lop,
                'DiemTrungBinh': float(dtb)
            }
            new_df = pd.DataFrame([new_row])
            self.df = pd.concat([self.df, new_df], ignore_index=True)
            self._save_data()
            return f"Đã thêm thành công Sinh viên: {hoten} ({masv})"
        except ValueError:
            return "Lỗi: Điểm trung bình phải là số."
        except Exception as e:
            return f"Lỗi khi thêm dữ liệu: {e}"

    # ------------------ CHỨC NĂNG 2: CHỈNH SỬA THÔNG TIN ------------------
    def edit_student(self, masv, data):
        """Chỉnh sửa dữ liệu của một sinh viên dựa trên Mã SV."""
        try:
            idx = self.df[self.df['MaSV'] == masv].index
            
            if idx.empty:
                return "Lỗi: Không tìm thấy Mã Sinh viên này."
            
            for key, value in data.items():
                if value is not None and value != '':
                    if key == 'DiemTrungBinh':
                        value = float(value)
                    self.df.loc[idx, key] = value
            
            self._save_data()
            return f"Đã cập nhật thành công Sinh viên có Mã SV: {masv}"
        except ValueError:
            return "Lỗi: Điểm trung bình phải là số hợp lệ."
        except Exception as e:
            return f"Lỗi khi cập nhật dữ liệu: {e}"

    # ------------------ CHỨC NĂNG 3: XUẤT FILE EXCEL VÀ MỞ ------------------
    def export_to_excel(self, filename="danh_sach_sinh_vien.xlsx"):
        """Xuất toàn bộ dữ liệu ra file Excel và tự động mở."""
        try:
            self.df.to_excel(filename, index=False)
            
            absolute_path = os.path.abspath(filename)
            
            if os.name == 'nt': 
                os.startfile(absolute_path)
            elif os.uname().sysname == 'Darwin': 
                subprocess.call(('open', absolute_path))
            elif os.name == 'posix': 
                subprocess.call(('xdg-open', absolute_path))

            return f"Xuất file Excel thành công và đang mở: {filename}"
        
        except FileNotFoundError:
             return f"Lỗi: Không tìm thấy thư viện 'openpyxl'. Vui lòng chạy 'pip install openpyxl'."
             
        except Exception as e:
            return f"Lỗi khi xuất hoặc mở file Excel: {e}"

# ====================================================================
# II. LỚP GIAO DIỆN NGƯỜI DÙNG (GUI) - StudentApp
# ====================================================================

class StudentApp:
    def __init__(self, master):
        self.manager = StudentManager()
        self.master = master
        master.title("Ứng Dụng Quản Lý Sinh Viên")
        master.geometry("850x600")

        menu_frame = tk.Frame(master, bd=2, relief=tk.RIDGE)
        menu_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        self.display_frame = tk.Frame(master)
        self.display_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        tk.Button(menu_frame, text="1. Thêm Sinh Viên", command=self.show_add_student).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(menu_frame, text="2. Xem/Chỉnh Sửa DS", command=self.show_view_edit).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(menu_frame, text="3. Xuất Excel", command=self.export_excel).pack(side=tk.LEFT, padx=5, pady=5)
        
        self.show_view_edit() 

    def clear_display_frame(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

    def show_data_in_treeview(self, df):
        self.clear_display_frame()
        if df.empty:
            tk.Label(self.display_frame, text="Không có dữ liệu sinh viên.").pack(pady=20)
            return

        columns = list(df.columns)
        self.tree = ttk.Treeview(self.display_frame, columns=columns, show='headings')
        
        vsb = ttk.Scrollbar(self.display_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.display_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        self.tree.pack(fill='both', expand=True, side='left')

        col_names_vn = {
            'MaSV': 'Mã SV', 'HoTen': 'Họ Tên', 'NgaySinh': 'Ngày Sinh', 
            'GioiTinh': 'Giới Tính', 'Lop': 'Lớp', 'DiemTrungBinh': 'Điểm TB'
        }
        for col in columns:
            col_name = col_names_vn.get(col, col)
            self.tree.heading(col, text=col_name)
            self.tree.column(col, width=120, anchor=tk.CENTER)

        for index, row in df.iterrows():
            self.tree.insert("", tk.END, values=list(row))
            
        return self.tree

    # --- CHỨC NĂNG 1: THÊM SINH VIÊN ---
    def show_add_student(self):
        self.clear_display_frame()
        tk.Label(self.display_frame, text="THÊM THÔNG TIN SINH VIÊN", font=('Arial', 14, 'bold')).pack(pady=10)

        fields = ['Mã SV (4 ký tự)', 'Họ Tên', 'Ngày Sinh (YYYY-MM-DD)', 'Giới Tính (Nam/Nữ)', 'Lớp', 'Điểm Trung Bình (float)']
        entries = {}

        for i, field in enumerate(fields):
            row = tk.Frame(self.display_frame)
            row.pack(padx=5, pady=2, fill=tk.X)
            tk.Label(row, text=field + ":", width=35, anchor='w').pack(side=tk.LEFT)
            entry = tk.Entry(row)
            entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
            entries[field] = entry

        def submit():
            data = {
                'masv': entries['Mã SV (4 ký tự)'].get().strip().upper(),
                'hoten': entries['Họ Tên'].get().strip(),
                'ngaysinh': entries['Ngày Sinh (YYYY-MM-DD)'].get().strip(),
                'gioitinh': entries['Giới Tính (Nam/Nữ)'].get().strip(),
                'lop': entries['Lớp'].get().strip(),
                'dtb': entries['Điểm Trung Bình (float)'].get().strip()
            }
            
            if not all(data.values()):
                messagebox.showerror("Lỗi Nhập liệu", "Vui lòng điền đầy đủ các trường.")
                return

            result = self.manager.add_student(**data)
            messagebox.showinfo("Kết quả Thêm SV", result)
            
            if result.startswith("Đã thêm thành công"):
                for entry in entries.values():
                    entry.delete(0, tk.END)
                self.show_view_edit()

        tk.Button(self.display_frame, text="Thêm Sinh Viên", command=submit).pack(pady=15)

    # --- CỬA SỔ CHỈNH SỬA CHI TIẾT ---
    def show_edit_window(self, masv):
        selected_df = self.manager.df[self.manager.df['MaSV'] == masv]
        
        if selected_df.empty:
            messagebox.showerror("Lỗi", f"Không tìm thấy Mã SV: {masv}")
            return
            
        selected_student = selected_df.iloc[0].to_dict()

        edit_window = tk.Toplevel(self.master)
        edit_window.title(f"Chỉnh Sửa Sinh Viên: {masv}")
        edit_window.geometry("450x350")

        tk.Label(edit_window, text=f"CHỈNH SỬA THÔNG TIN ({masv})", font=('Arial', 12, 'bold')).pack(pady=10)

        fields_map = {
            'MaSV': 'Mã SV', 'HoTen': 'Họ Tên', 'NgaySinh': 'Ngày Sinh', 
            'GioiTinh': 'Giới Tính', 'Lop': 'Lớp', 'DiemTrungBinh': 'Điểm TB'
        }
        entries = {}

        for key, vn_name in fields_map.items():
            row = tk.Frame(edit_window)
            row.pack(padx=10, pady=2, fill=tk.X)
            
            tk.Label(row, text=vn_name + ":", width=15, anchor='w').pack(side=tk.LEFT)
            entry = tk.Entry(row)
            entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
            entries[key] = entry
            
            entry.insert(0, selected_student.get(key, ''))
            
            if key == 'MaSV':
                entry.config(state='readonly')
                
        def save_changes():
            new_data = {}
            for key in fields_map.keys():
                new_data[key] = entries[key].get().strip()

            data_to_update = {
                'HoTen': new_data['HoTen'],
                'NgaySinh': new_data['NgaySinh'],
                'GioiTinh': new_data['GioiTinh'],
                'Lop': new_data['Lop'],
                'DiemTrungBinh': new_data['DiemTrungBinh']
            }
            
            try:
                float(data_to_update['DiemTrungBinh'])
            except ValueError:
                messagebox.showerror("Lỗi", "Điểm Trung Bình phải là số hợp lệ.", parent=edit_window)
                return

            result = self.manager.edit_student(masv, data_to_update)
            messagebox.showinfo("Kết quả Chỉnh sửa", result, parent=edit_window)
            
            if result.startswith("Đã cập nhật thành công"):
                edit_window.destroy()
                self.show_view_edit()

        tk.Button(edit_window, text="Lưu Thay Đổi", command=save_changes, bg='green', fg='white').pack(pady=15, padx=10)
        edit_window.grab_set()

    # --- CHỨC NĂNG 2: XEM/CHỈNH SỬA DANH SÁCH ---
    def show_view_edit(self):
        self.clear_display_frame()
        tk.Label(self.display_frame, text="DANH SÁCH SINH VIÊN", font=('Arial', 14, 'bold')).pack(pady=5)
        
        if self.manager.df.empty:
            tk.Label(self.display_frame, text="Không có dữ liệu sinh viên.").pack()
            return
            
        tree = self.show_data_in_treeview(self.manager.df)
        
        edit_frame = tk.Frame(self.display_frame)
        edit_frame.pack(pady=10)
        
        def handle_edit(event=None):
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showerror("Lỗi", "Vui lòng chọn một dòng để chỉnh sửa.")
                return
            
            values = tree.item(selected_item, 'values')
            masv = values[0]
            
            self.show_edit_window(masv)
            
        tk.Button(edit_frame, text="Chỉnh Sửa Thông Tin SV Đã Chọn", command=handle_edit).pack(side=tk.LEFT, padx=10)
        
        tree.bind('<Double-1>', handle_edit)

    # --- CHỨC NĂNG 3: XUẤT FILE EXCEL ---
    def export_excel(self):
        filename = simpledialog.askstring("Xuất Excel", "Nhập tên file Excel:", initialvalue="danh_sach_sinh_vien.xlsx")
        if filename:
            result = self.manager.export_to_excel(filename)
            messagebox.showinfo("Xuất File", result)

# ====================================================================
# III. CHẠY ỨNG DỤNG
# ====================================================================

if __name__ == '__main__':
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()