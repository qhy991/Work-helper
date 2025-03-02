import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import datetime
import random
import matplotlib.font_manager as fm
import numpy as np
import matplotlib
import json
from matplotlib.colors import hsv_to_rgb, rgb_to_hsv

# 设置中文字体
def setup_chinese_fonts():
    macos_chinese_fonts = [
        '/System/Library/Fonts/PingFang.ttc',
        '/Library/Fonts/Microsoft Yahei.ttf',
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/System/Library/Fonts/STHeiti Medium.ttc',
        '/Library/Fonts/Songti.ttc',
        '/System/Library/Fonts/Supplemental/Songti.ttc'
    ]
    for font_path in macos_chinese_fonts:
        try:
            font_prop = fm.FontProperties(fname=font_path)
            font_name = font_prop.get_name()
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.sans-serif'] = [font_name]
            plt.rcParams['axes.unicode_minus'] = False
            print(f"成功设置中文字体：{font_name}")
            return font_prop
        except Exception as e:
            continue
    print("警告：未找到可用的中文字体。请检查系统字体或手动指定字体路径。")
    return None

chinese_font = setup_chinese_fonts()

class SimpleCalendar(tk.Toplevel):
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self.parent = parent
        self.callback = callback
        self.title("选择日期")
        self.geometry("300x250")
        self.resizable(False, False)
        self.current_date = datetime.datetime.now()
        self.selected_date = self.current_date.date()
        self.create_widgets()

    def create_widgets(self):
        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        prev_year_btn = ttk.Button(top_frame, text="<<", width=3, command=lambda: self.change_date(years=-1))
        prev_year_btn.pack(side=tk.LEFT, padx=2)
        prev_month_btn = ttk.Button(top_frame, text="<", width=3, command=lambda: self.change_date(months=-1))
        prev_month_btn.pack(side=tk.LEFT, padx=2)
        self.date_label = ttk.Label(top_frame, width=15, anchor="center", font=("SimHei", 10, "bold"))
        self.date_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        next_month_btn = ttk.Button(top_frame, text=">", width=3, command=lambda: self.change_date(months=1))
        next_month_btn.pack(side=tk.LEFT, padx=2)
        next_year_btn = ttk.Button(top_frame, text=">>", width=3, command=lambda: self.change_date(years=1))
        next_year_btn.pack(side=tk.LEFT, padx=2)
        calendar_frame = tk.Frame(self)
        calendar_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        weekdays = ["一", "二", "三", "四", "五", "六", "日"]
        for i, day in enumerate(weekdays):
            label = ttk.Label(calendar_frame, text=day, anchor="center", width=3)
            label.grid(row=0, column=i, padx=1, pady=1)
        self.day_buttons = []
        for row in range(6):
            for col in range(7):
                btn = ttk.Button(calendar_frame, width=3, text="", command=lambda r=row, c=col: self.select_day(r, c))
                btn.grid(row=row+1, column=col, padx=1, pady=1)
                self.day_buttons.append(btn)
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(fill=tk.X, padx=5, pady=5)
        today_btn = ttk.Button(bottom_frame, text="今天", command=self.select_today)
        today_btn.pack(side=tk.LEFT, padx=5)
        ok_btn = ttk.Button(bottom_frame, text="确定", command=self.confirm_selection)
        ok_btn.pack(side=tk.RIGHT, padx=5)
        cancel_btn = ttk.Button(bottom_frame, text="取消", command=self.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        self.update_calendar()
        for btn in self.day_buttons:
            btn.bind('<Double-Button-1>', lambda e, b=btn: self.double_click_select(b))

    def update_calendar(self):
        year = self.current_date.year
        month = self.current_date.month
        self.date_label.config(text=f"{year}年{month}月")
        first_day = datetime.date(year, month, 1)
        first_weekday = first_day.weekday()
        if month == 12:
            next_month = datetime.date(year + 1, 1, 1)
        else:
            next_month = datetime.date(year, month + 1, 1)
        days_in_month = (next_month - first_day).days
        for btn in self.day_buttons:
            btn.config(text="", state=tk.DISABLED)
        for i in range(days_in_month):
            day = i + 1
            btn_idx = first_weekday + i
            if btn_idx < len(self.day_buttons):
                self.day_buttons[btn_idx].config(text=str(day), state=tk.NORMAL)
                current_date = datetime.date(year, month, day)
                if current_date == self.selected_date:
                    self.day_buttons[btn_idx].state(["pressed"])
                else:
                    self.day_buttons[btn_idx].state(["!pressed"])

    def double_click_select(self, button):
        if button['state'] != 'disabled' and button['text']:
            day = int(button['text'])
            self.selected_date = datetime.date(self.current_date.year, self.current_date.month, day)
            self.confirm_selection()

    def change_date(self, years=0, months=0):
        year = self.current_date.year + years
        month = self.current_date.month + months
        if month > 12:
            month = 1
            year += 1
        elif month < 1:
            month = 12
            year -= 1
        day = min(self.current_date.day, self.get_days_in_month(year, month))
        self.current_date = datetime.datetime(year, month, day)
        self.update_calendar()

    def get_days_in_month(self, year, month):
        if month == 12:
            next_month = datetime.date(year + 1, 1, 1)
        else:
            next_month = datetime.date(year, month + 1, 1)
        return (next_month - datetime.date(year, month, 1)).days

    def select_day(self, row, col):
        btn_idx = row * 7 + col
        if btn_idx < len(self.day_buttons) and self.day_buttons[btn_idx]['state'] != 'disabled':
            day = int(self.day_buttons[btn_idx]['text'])
            self.selected_date = datetime.date(self.current_date.year, self.current_date.month, day)
            self.update_calendar()

    def select_today(self):
        today = datetime.datetime.now()
        self.current_date = today
        self.selected_date = today.date()
        self.update_calendar()

    def confirm_selection(self):
        if self.callback:
            self.callback(self.selected_date)
        self.destroy()

class DateSelector(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, bg="#f0f0f0")
        self.selected_date = datetime.datetime.now().date()
        self.date_var = tk.StringVar(value=self.selected_date.strftime("%Y-%m-%d"))
        self.date_entry = ttk.Entry(self, textvariable=self.date_var, width=12)
        self.date_entry.pack(side=tk.LEFT, padx=(0, 2))
        self.calendar_btn = ttk.Button(self, text="📅", width=2, command=self.show_calendar)
        self.calendar_btn.pack(side=tk.LEFT)

    def show_calendar(self):
        calendar = SimpleCalendar(self, callback=self.set_date)
        calendar.transient(self)
        calendar.grab_set()

    def set_date(self, date):
        self.selected_date = date
        self.date_var.set(date.strftime("%Y-%m-%d"))

    def get_date(self):
        return self.selected_date

class TaskDialog(tk.Toplevel):
    def __init__(self, parent, task_list=None, parent_task=None, start_date=None, callback=None):
        super().__init__(parent)
        self.parent = parent
        self.task_list = task_list or []
        self.parent_task = parent_task
        self.callback = callback
        self.title("添加任务")
        self.geometry("400x350")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        self.create_widgets(start_date)
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def create_widgets(self, start_date):
        frame = ttk.Frame(self, padding="20 20 20 20")
        frame.pack(fill=tk.BOTH, expand=True)
        ttk.Label(frame, text="任务名称:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        self.name_entry = ttk.Entry(frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky=tk.W, pady=(0, 10))
        ttk.Label(frame, text="开始日期:").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        self.start_date = DateSelector(frame)
        self.start_date.grid(row=1, column=1, sticky=tk.W, pady=(0, 10))
        if start_date:
            self.start_date.set_date(start_date)
        ttk.Label(frame, text="结束日期:").grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        self.end_date = DateSelector(frame)
        self.end_date.grid(row=2, column=1, sticky=tk.W, pady=(0, 10))
        if start_date:
            end_date = start_date + datetime.timedelta(days=7)
            self.end_date.set_date(end_date)
        ttk.Label(frame, text="任务层级:").grid(row=3, column=0, sticky=tk.W, pady=(0, 10))
        self.level_var = tk.IntVar(value=0)
        level_frame = ttk.Frame(frame)
        level_frame.grid(row=3, column=1, sticky=tk.W, pady=(0, 10))
        ttk.Radiobutton(level_frame, text="主任务", variable=self.level_var, value=0, command=self.on_level_change).pack(side=tk.LEFT)
        ttk.Radiobutton(level_frame, text="子任务", variable=self.level_var, value=1, command=self.on_level_change).pack(side=tk.LEFT)
        ttk.Radiobutton(level_frame, text="子子任务", variable=self.level_var, value=2, command=self.on_level_change).pack(side=tk.LEFT)
        if self.parent_task:
            if self.parent_task["level"] == 0:
                self.level_var.set(1)
            else:
                self.level_var.set(2)
        ttk.Label(frame, text="父任务:").grid(row=4, column=0, sticky=tk.W, pady=(0, 10))
        self.parent_var = tk.StringVar()
        self.parent_combo = ttk.Combobox(frame, textvariable=self.parent_var, width=28, state="readonly")
        self.parent_combo.grid(row=4, column=1, sticky=tk.W, pady=(0, 10))
        self.update_parent_tasks()
        if self.parent_task:
            self.parent_var.set(f"{self.parent_task['id']}: {self.parent_task['name']}")
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        ttk.Button(button_frame, text="确定", command=self.confirm).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="取消", command=self.destroy).pack(side=tk.LEFT)
        self.on_level_change()

    def on_level_change(self):
        level = self.level_var.get()
        if level == 0:
            self.parent_combo.config(state="disabled")
            self.parent_var.set("")
        else:
            self.parent_combo.config(state="readonly")
            self.update_parent_tasks()

    def update_parent_tasks(self):
        level = self.level_var.get()
        parent_options = []
        if level == 1:
            parent_options = [f"{task['id']}: {task['name']}" for task in self.task_list if task["level"] == 0]
        elif level == 2:
            parent_options = [f"{task['id']}: {task['name']}" for task in self.task_list if task["level"] == 1]
        self.parent_combo['values'] = parent_options
        if parent_options and not self.parent_var.get():
            self.parent_combo.current(0)

    def confirm(self):
        name = self.name_entry.get().strip()
        start = self.start_date.get_date()
        end = self.end_date.get_date()
        level = self.level_var.get()
        if not name:
            messagebox.showerror("错误", "请输入任务名称")
            return
        if end < start:
            messagebox.showerror("错误", "结束日期不能早于开始日期")
            return
        parent_id = None
        if level > 0:
            parent_selection = self.parent_var.get()
            if not parent_selection:
                messagebox.showerror("错误", "请选择父任务")
                return
            parent_id = int(parent_selection.split(":")[0])
        if self.callback:
            self.callback({
                "name": name,
                "start": start,
                "end": end,
                "level": level,
                "parent_id": parent_id
            })
        self.destroy()

class JSONHandler:
    @staticmethod
    def convert_to_serializable(tasks):
        serializable_tasks = []
        for task in tasks:
            task_copy = task.copy()
            task_copy['start'] = task_copy['start'].strftime('%Y-%m-%d')
            task_copy['end'] = task_copy['end'].strftime('%Y-%m-%d')
            task_copy['color'] = list(rgb_to_hsv(task_copy['color']))
            serializable_tasks.append(task_copy)
        return serializable_tasks

    @staticmethod
    def convert_from_serializable(tasks):
        deserialized_tasks = []
        for task in tasks:
            task_copy = task.copy()
            task_copy['start'] = datetime.datetime.strptime(task_copy['start'], '%Y-%m-%d').date()
            task_copy['end'] = datetime.datetime.strptime(task_copy['end'], '%Y-%m-%d').date()
            task_copy['color'] = hsv_to_rgb(task_copy['color'])
            deserialized_tasks.append(task_copy)
        return deserialized_tasks

def add_json_methods(cls):
    def save_to_json(self):
        if not self.tasks:
            messagebox.showinfo("提示", "没有可保存的任务")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")])
        if not file_path:
            return
        try:
            serializable_tasks = JSONHandler.convert_to_serializable(self.tasks)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(serializable_tasks, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("成功", f"任务已保存到 {file_path}")
        except Exception as e:
            messagebox.showerror("错误", f"保存文件时发生错误：{str(e)}")

    def load_from_json(self):
        file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")])
        if not file_path:
            return
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                loaded_tasks = json.load(f)
            deserialized_tasks = JSONHandler.convert_from_serializable(loaded_tasks)
            self.tasks.clear()
            self.next_task_id = 1
            for task in deserialized_tasks:
                task['id'] = self.next_task_id
                self.next_task_id += 1
                self.tasks.append(task)
            self.update_task_list()
            self.update_chart()
            messagebox.showinfo("成功", f"成功从 {file_path} 加载任务")
        except json.JSONDecodeError:
            messagebox.showerror("错误", "文件格式不正确")
        except Exception as e:
            messagebox.showerror("错误", f"加载文件时发生错误：{str(e)}")

    cls.save_to_json = save_to_json
    cls.load_from_json = load_from_json
    return cls

@add_json_methods
class GanttChartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("甘特图管理系统")
        self.root.geometry("1200x800")
        self.root.configure(bg="#ECEFF1")  # 浅灰蓝色背景
        self.tasks = []
        self.next_task_id = 1
        self.initial_date = datetime.datetime.now().date()
        self.main_frame = tk.Frame(root, bg="#ECEFF1")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.input_frame = tk.Frame(self.main_frame, bg="#ECEFF1", width=350, highlightbackground="#ddd", highlightthickness=1)
        self.input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10, pady=10)
        self.input_frame.pack_propagate(False)
        self.chart_frame = tk.Frame(self.main_frame, bg="white", highlightbackground="#ddd", highlightthickness=1)
        self.chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        title_label = tk.Label(self.input_frame, text="任务管理", bg="#ECEFF1", font=("SimHei", 16, "bold"))
        title_label.pack(pady=(20, 30))
        self.create_input_fields()
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect('button_press_event', self.on_chart_click)
        self.update_chart()
        # 绑定快捷键
        self.root.bind("<Control-s>", lambda e: self.save_to_json())
        self.root.bind("<Control-o>", lambda e: self.load_from_json())
        self.root.bind("<Control-n>", lambda e: self.show_task_dialog())

    def create_input_fields(self):
        style = ttk.Style()
        style.theme_use('clam')  # 使用现代化主题
        style.configure("TButton", background="#4CAF50", foreground="white", font=("SimHei", 10, "bold"))
        button_frame = tk.Frame(self.input_frame, bg="#ECEFF1")
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        add_button = ttk.Button(button_frame, text="➕ 添加任务", style="TButton", command=self.show_task_dialog)
        add_button.pack(side=tk.LEFT, padx=(0, 10))
        edit_button = ttk.Button(button_frame, text="✏️ 编辑任务", style="TButton", command=self.edit_selected_task)
        edit_button.pack(side=tk.LEFT, padx=(0, 10))
        delete_button = ttk.Button(button_frame, text="🗑️ 删除任务", style="TButton", command=self.delete_selected_task)
        delete_button.pack(side=tk.LEFT)
        save_load_frame = tk.Frame(self.input_frame, bg="#ECEFF1")
        save_load_frame.pack(fill=tk.X, padx=20, pady=10)
        save_button = ttk.Button(save_load_frame, text="💾 保存项目", style="TButton", command=self.save_to_json)
        save_button.pack(side=tk.LEFT, padx=(0, 10))
        load_button = ttk.Button(save_load_frame, text="📂 加载项目", style="TButton", command=self.load_from_json)
        load_button.pack(side=tk.LEFT)
        export_button = ttk.Button(save_load_frame, text="🖼️ 导出图片", style="TButton", command=self.export_chart_to_image)
        export_button.pack(side=tk.LEFT)
        task_list_frame = tk.Frame(self.input_frame, bg="#ECEFF1")
        task_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 10))
        task_list_label = tk.Label(task_list_frame, text="当前任务列表", bg="#ECEFF1", font=("SimHei", 12, "bold"))
        task_list_label.pack(anchor="w", pady=(0, 10))
        columns = ("ID", "名称", "开始", "结束", "层级", "父任务")
        self.task_tree = ttk.Treeview(task_list_frame, columns=columns, show="headings", height=18)
        self.task_tree.heading("ID", text="ID", anchor="center")
        self.task_tree.heading("名称", text="名称", anchor="w")
        self.task_tree.heading("开始", text="开始日期", anchor="center", command=lambda: self.sort_column("start"))
        self.task_tree.heading("结束", text="结束日期", anchor="center", command=lambda: self.sort_column("end"))
        self.task_tree.heading("层级", text="层级", anchor="center")
        self.task_tree.heading("父任务", text="父任务", anchor="w")
        self.task_tree.column("ID", width=30, anchor="center")
        self.task_tree.column("名称", width=120, anchor="w")
        self.task_tree.column("开始", width=80, anchor="center")
        self.task_tree.column("结束", width=80, anchor="center")
        self.task_tree.column("层级", width=50, anchor="center")
        self.task_tree.column("父任务", width=80, anchor="w")
        scrollbar = ttk.Scrollbar(task_list_frame, orient="vertical", command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_tree.bind("<Double-1>", lambda e: self.show_task_details())

    def show_task_dialog(self, parent_task=None, start_date=None):
        dialog = TaskDialog(self.root, task_list=self.tasks, parent_task=parent_task, start_date=start_date, callback=self.add_task)

    def edit_selected_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showinfo("提示", "请先选择要编辑的任务")
            return
        task_id = int(self.task_tree.item(selected_item[0])['values'][0])
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if not task:
            return
        messagebox.showinfo("提示", f"编辑任务 {task['name']} 的功能正在开发中")

    def delete_selected_task(self):
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showinfo("提示", "请先选择要删除的任务")
            return
        task_id = int(self.task_tree.item(selected_item[0])['values'][0])
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if not task:
            return
        if not messagebox.askyesno("确认", f"确定要删除任务 \"{task['name']}\" 吗？"):
            return
        has_children = any(t["parent_id"] == task_id for t in self.tasks)
        if has_children:
            if messagebox.askyesno("警告", "该任务有子任务，删除它将同时删除所有子任务。确定要继续吗？"):
                self.delete_task_and_children(task_id)
        else:
            self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self.update_task_list()
        self.update_chart()

    def delete_task_and_children(self, task_id):
        child_ids = [t["id"] for t in self.tasks if t.get("parent_id") == task_id]
        for child_id in child_ids:
            self.delete_task_and_children(child_id)
        self.tasks = [t for t in self.tasks if t["id"] != task_id]

    def add_task(self, task_data):
        hue = random.random()
        saturation = 0.8
        value = max(0.5, 1.0 - task_data["level"] * 0.2)
        task = {
            "id": self.next_task_id,
            "name": task_data["name"],
            "start": task_data["start"],
            "end": task_data["end"],
            "level": task_data["level"],
            "parent_id": task_data["parent_id"],
            "color": hsv_to_rgb([hue, saturation, value])
        }
        self.next_task_id += 1
        if task["parent_id"]:
            parent_task = next((t for t in self.tasks if t["id"] == task["parent_id"]), None)
            if parent_task:
                if task["start"] < parent_task["start"]:
                    task["start"] = parent_task["start"]
                if task["end"] > parent_task["end"]:
                    task["end"] = parent_task["end"]
                    messagebox.showinfo("提示", f"子任务结束日期已调整为与父任务一致: {parent_task['end'].strftime('%Y-%m-%d')}")
        self.tasks.append(task)
        self.update_task_list()
        self.update_chart()

    def update_task_list(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        for task in self.tasks:
            parent_name = ""
            if task["parent_id"]:
                parent = next((t for t in self.tasks if t["id"] == task["parent_id"]), None)
                if parent:
                    parent_name = parent["name"]
            level_names = ["主任务", "子任务", "子子任务"]
            level_name = level_names[task["level"]] if task["level"] < len(level_names) else f"层级 {task['level']}"
            self.task_tree.insert("", "end", values=(task["id"], task["name"], task["start"].strftime("%Y-%m-%d"), task["end"].strftime("%Y-%m-%d"), level_name, parent_name))

    def export_chart_to_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG 图片", "*.png"), ("JPEG 图片", "*.jpg"), ("SVG 矢量图", "*.svg"), ("PDF 文件", "*.pdf"), ("所有文件", "*.*")])
        if not file_path:
            return
        try:
            self.fig.tight_layout(pad=2.0)
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.fig.savefig(file_path, dpi=300, bbox_inches='tight')
            else:
                self.fig.savefig(file_path, bbox_inches='tight')
            messagebox.showinfo("导出成功", f"甘特图已成功导出到 {file_path}")
        except Exception as e:
            messagebox.showerror("导出错误", f"导出图片时发生错误：{str(e)}")

    def update_chart(self):
        self.ax.clear()
        if not self.tasks:
            self.ax.text(0.5, 0.5, "尚无任务数据", ha='center', va='center', transform=self.ax.transAxes)
            self.canvas.draw()
            return
        min_date = min(task["start"] for task in self.tasks)
        max_date = max(task["end"] for task in self.tasks)
        if (max_date - min_date).days < 7:
            max_date = min_date + datetime.timedelta(days=7)
        self.initial_date = min_date
        self.ax.xaxis_date()
        self.ax.set_xlim([min_date - datetime.timedelta(days=1), max_date + datetime.timedelta(days=1)])
        self.ax.set_title("项目甘特图", fontsize=14, pad=20)
        task_names = []
        y_positions = []
        sorted_tasks = self.sort_tasks_hierarchically()
        for i, task in enumerate(sorted_tasks):
            y_pos = len(sorted_tasks) - i - 1
            start_date = task["start"]
            end_date = task["end"]
            duration = (end_date - start_date).days + 1
            indent = "  " * task["level"]
            task_name = f"{indent}{task['name']}"
            task_names.append(task_name)
            y_positions.append(y_pos)
            bar_height = 0.5
            if task["level"] > 0:
                bar_height = 0.4
            self.ax.barh(y_pos, duration, left=start_date, height=bar_height, align='center', color=task["color"], alpha=0.8, edgecolor='black', linewidth=1)
            if duration > 3:
                mid_date = start_date + datetime.timedelta(days=duration / 2)
                self.ax.text(mid_date, y_pos, task["name"], ha='center', va='center', color='black', fontsize=8, fontweight='bold')
            if task["parent_id"]:
                parent = next((t for t in sorted_tasks if t["id"] == task["parent_id"]), None)
                if parent:
                    parent_index = sorted_tasks.index(parent)
                    parent_y_pos = len(sorted_tasks) - parent_index - 1
                    self.ax.plot([start_date, start_date], [y_pos + bar_height/2, parent_y_pos - bar_height/2], 'k--', alpha=0.3, linewidth=1)
        self.ax.set_yticks(y_positions)
        self.ax.set_yticklabels(task_names)
        self.ax.grid(True, axis='x', linestyle='--', alpha=0.7)
        self.highlight_weekends(min_date, max_date)
        self.fig.tight_layout()
        self.canvas.draw()

    def sort_tasks_hierarchically(self):
        sorted_tasks = []
        main_tasks = [task for task in self.tasks if task["level"] == 0]
        for main_task in main_tasks:
            sorted_tasks.append(main_task)
            self.add_subtasks_recursively(main_task["id"], sorted_tasks)
        return sorted_tasks

    def add_subtasks_recursively(self, parent_id, sorted_tasks):
        subtasks = [task for task in self.tasks if task["parent_id"] == parent_id]
        for subtask in subtasks:
            sorted_tasks.append(subtask)
            self.add_subtasks_recursively(subtask["id"], sorted_tasks)

    def highlight_weekends(self, start_date, end_date):
        delta = (end_date - start_date).days + 1
        all_dates = [start_date + datetime.timedelta(days=i) for i in range(delta)]
        weekends = [date for date in all_dates if date.weekday() >= 5]
        for weekend in weekends:
            self.ax.axvspan(weekend, weekend + datetime.timedelta(days=1), facecolor='lightgray', alpha=0.3, zorder=0)

    def on_chart_click(self, event):
        if event.xdata is None or event.ydata is None:
            return
        clicked_date = matplotlib.dates.num2date(event.xdata).date()
        if event.dblclick:
            self.show_task_dialog(start_date=clicked_date)
            return
        sorted_tasks = self.sort_tasks_hierarchically()
        y_index = len(sorted_tasks) - int(round(event.ydata)) - 1
        if 0 <= y_index < len(sorted_tasks):
            clicked_task = sorted_tasks[y_index]
            task_start = clicked_task["start"]
            task_end = clicked_task["end"]
            if task_start <= clicked_date <= task_end:
                self.show_task_menu(event, clicked_task)

    def show_task_menu(self, event, task):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label=f"任务: {task['name']}")
        menu.add_separator()
        menu.add_command(label="编辑任务", command=lambda: self.edit_task(task))
        menu.add_command(label="添加子任务", command=lambda: self.show_task_dialog(parent_task=task))
        menu.add_command(label="删除任务", command=lambda: self.confirm_delete_task(task))
        try:
            menu.tk_popup(event.canvas.winfo_rootx() + event.x, event.canvas.winfo_rooty() + event.y)
        finally:
            menu.grab_release()

    def edit_task(self, task):
        messagebox.showinfo("提示", f"编辑任务 {task['name']} 的功能正在开发中")

    def confirm_delete_task(self, task):
        if messagebox.askyesno("确认", f"确定要删除任务 \"{task['name']}\" 吗？"):
            has_children = any(t["parent_id"] == task["id"] for t in self.tasks)
            if has_children:
                if messagebox.askyesno("警告", "该任务有子任务，删除它将同时删除所有子任务。确定要继续吗？"):
                    self.delete_task_and_children(task["id"])
            else:
                self.tasks = [t for t in self.tasks if t["id"] != task["id"]]
            self.update_task_list()
            self.update_chart()

    def show_task_details(self):
        selected = self.task_tree.selection()
        if selected:
            task_id = int(self.task_tree.item(selected[0])["values"][0])
            task = next(t for t in self.tasks if t["id"] == task_id)
            details = f"任务名称: {task['name']}\n开始日期: {task['start']}\n结束日期: {task['end']}\n层级: {'主任务' if task['level'] == 0 else '子任务' if task['level'] == 1 else '子子任务'}\n父任务: {task.get('parent_id', '无')}"
            messagebox.showinfo("任务详情", details)

    def sort_column(self, col):
        if col == "start":
            self.tasks.sort(key=lambda x: x["start"])
        elif col == "end":
            self.tasks.sort(key=lambda x: x["end"])
        self.update_task_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = GanttChartApp(root)
    root.mainloop()