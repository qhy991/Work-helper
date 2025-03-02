import tkinter as tk
from tkinter import ttk, filedialog,messagebox
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
def setup_chinese_fonts():
    """
    为 macOS 优化的中文字体设置
    """
    # macOS 常用中文字体路径
    macos_chinese_fonts = [
        '/System/Library/Fonts/PingFang.ttc',  # 苹方字体
        '/Library/Fonts/Microsoft Yahei.ttf',  # 微软雅黑
        '/System/Library/Fonts/STHeiti Light.ttc',  # 华文黑体
        '/System/Library/Fonts/STHeiti Medium.ttc',  # 华文黑体
        '/Library/Fonts/Songti.ttc',  # 宋体
        '/System/Library/Fonts/Supplemental/Songti.ttc'  # 备选宋体
    ]
    
    # 尝试找到可用的中文字体
    for font_path in macos_chinese_fonts:
        try:
            # 获取字体属性
            font_prop = fm.FontProperties(fname=font_path)
            font_name = font_prop.get_name()
            
            # 设置 matplotlib 参数
            plt.rcParams['font.family'] = 'sans-serif'
            plt.rcParams['font.sans-serif'] = [font_name]
            plt.rcParams['axes.unicode_minus'] = False
            
            print(f"成功设置中文字体：{font_name}")
            return font_prop
        except Exception as e:
            continue
    
    print("警告：未找到可用的中文字体。请检查系统字体或手动指定字体路径。")
    return None

# 全局字体属性
chinese_font = setup_chinese_fonts()

def set_chinese_font_for_fig(fig):
    """
    为特定图形设置中文字体
    
    Args:
        fig (matplotlib.figure.Figure): 需要设置字体的图形对象
    """
    if chinese_font:
        # 设置标题和各种文本元素的字体
        for text in fig.texts + [fig._suptitle] if fig._suptitle else []:
            text.set_fontproperties(chinese_font)
        
        # 设置坐标轴标签
        for ax in fig.axes:
            ax.title.set_fontproperties(chinese_font)
            ax.xaxis.label.set_fontproperties(chinese_font)
            ax.yaxis.label.set_fontproperties(chinese_font)
            
            # 设置刻度标签
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_fontproperties(chinese_font)

# 手动指定字体文件路径的备选方案
def manually_set_font(font_path):
    """
    手动设置字体文件路径
    
    Args:
        font_path (str): 字体文件的绝对路径
    """
    try:
        font_prop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.sans-serif'] = [font_prop.get_name()]
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['axes.unicode_minus'] = False
        print(f"成功设置字体：{font_prop.get_name()}")
    except Exception as e:
        print(f"设置字体失败：{e}")
        print("请检查字体文件路径是否正确")

# 在图表中使用之前调用此函数
setup_chinese_fonts()
class SimpleCalendar(tk.Toplevel):
    """简单的日历弹出窗口"""
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self.parent = parent
        self.callback = callback
        
        self.title("选择日期")
        self.geometry("300x250")
        self.resizable(False, False)
        
        # 初始化为当前日期
        self.current_date = datetime.datetime.now()
        self.selected_date = self.current_date.date()
        
        self.create_widgets()
        
    def create_widgets(self):
        # 年月选择框架
        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 上一年按钮
        prev_year_btn = ttk.Button(top_frame, text="<<", width=3, 
                                  command=lambda: self.change_date(years=-1))
        prev_year_btn.pack(side=tk.LEFT, padx=2)
        
        # 上一月按钮
        prev_month_btn = ttk.Button(top_frame, text="<", width=3, 
                                   command=lambda: self.change_date(months=-1))
        prev_month_btn.pack(side=tk.LEFT, padx=2)
        
        # 年月显示标签
        self.date_label = ttk.Label(top_frame, width=15, anchor="center", 
                                   font=("SimHei", 10, "bold"))
        self.date_label.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 下一月按钮
        next_month_btn = ttk.Button(top_frame, text=">", width=3, 
                                   command=lambda: self.change_date(months=1))
        next_month_btn.pack(side=tk.LEFT, padx=2)
        
        # 下一年按钮
        next_year_btn = ttk.Button(top_frame, text=">>", width=3, 
                                  command=lambda: self.change_date(years=1))
        next_year_btn.pack(side=tk.LEFT, padx=2)
        
        # 日历框架
        calendar_frame = tk.Frame(self)
        calendar_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 星期标题
        weekdays = ["一", "二", "三", "四", "五", "六", "日"]
        for i, day in enumerate(weekdays):
            label = ttk.Label(calendar_frame, text=day, anchor="center", width=3)
            label.grid(row=0, column=i, padx=1, pady=1)
        
        # 创建日期按钮网格
        self.day_buttons = []
        for row in range(6):  # 最多6行以容纳所有情况
            for col in range(7):  # 7列代表周一到周日
                btn = ttk.Button(calendar_frame, width=3, text="", 
                                command=lambda r=row, c=col: self.select_day(r, c))
                btn.grid(row=row+1, column=col, padx=1, pady=1)
                self.day_buttons.append(btn)
        
        # 底部按钮框架
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 今天按钮
        today_btn = ttk.Button(bottom_frame, text="今天", 
                              command=self.select_today)
        today_btn.pack(side=tk.LEFT, padx=5)
        
        # 确定按钮
        ok_btn = ttk.Button(bottom_frame, text="确定", 
                           command=self.confirm_selection)
        ok_btn.pack(side=tk.RIGHT, padx=5)
        
        # 取消按钮
        cancel_btn = ttk.Button(bottom_frame, text="取消", 
                               command=self.destroy)
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        
        # 更新日历显示
        self.update_calendar()
        
        # 设置双击选择
        for btn in self.day_buttons:
            btn.bind('<Double-Button-1>', lambda e, b=btn: self.double_click_select(b))
        
    def update_calendar(self):
        """更新日历显示"""
        year = self.current_date.year
        month = self.current_date.month
        
        # 更新标题
        self.date_label.config(text=f"{year}年{month}月")
        
        # 计算当月第一天是星期几（0是周一，6是周日）
        first_day = datetime.date(year, month, 1)
        first_weekday = first_day.weekday()
        
        # 计算当月天数
        if month == 12:
            next_month = datetime.date(year + 1, 1, 1)
        else:
            next_month = datetime.date(year, month + 1, 1)
        days_in_month = (next_month - first_day).days
        
        # 清空所有按钮
        for btn in self.day_buttons:
            btn.config(text="", state=tk.DISABLED)
        
        # 填充当月天数
        for i in range(days_in_month):
            day = i + 1
            btn_idx = first_weekday + i
            if btn_idx < len(self.day_buttons):
                self.day_buttons[btn_idx].config(text=str(day), state=tk.NORMAL)
                
                # 高亮显示当前选择的日期
                current_date = datetime.date(year, month, day)
                if current_date == self.selected_date:
                    self.day_buttons[btn_idx].state(["pressed"])
                else:
                    self.day_buttons[btn_idx].state(["!pressed"])
    
    def double_click_select(self, button):
        """双击选择并确认日期"""
        if button['state'] != 'disabled' and button['text']:
            day = int(button['text'])
            self.selected_date = datetime.date(self.current_date.year, self.current_date.month, day)
            self.confirm_selection()
        
    def change_date(self, years=0, months=0):
        """改变当前显示的年月"""
        year = self.current_date.year + years
        month = self.current_date.month + months
        
        # 处理月份溢出
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
        """获取指定年月的天数"""
        if month == 12:
            next_month = datetime.date(year + 1, 1, 1)
        else:
            next_month = datetime.date(year, month + 1, 1)
        return (next_month - datetime.date(year, month, 1)).days
        
    def select_day(self, row, col):
        """选择日期"""
        btn_idx = row * 7 + col
        if btn_idx < len(self.day_buttons) and self.day_buttons[btn_idx]['state'] != 'disabled':
            day = int(self.day_buttons[btn_idx]['text'])
            self.selected_date = datetime.date(self.current_date.year, self.current_date.month, day)
            self.update_calendar()
            
    def select_today(self):
        """选择今天"""
        today = datetime.datetime.now()
        self.current_date = today
        self.selected_date = today.date()
        self.update_calendar()
        
    def confirm_selection(self):
        """确认选择"""
        if self.callback:
            self.callback(self.selected_date)
        self.destroy()


class DateSelector(tk.Frame):
    """自定义日期选择控件"""
    def __init__(self, master=None, **kwargs):
        super().__init__(master, bg="#f0f0f0")
        
        self.selected_date = datetime.datetime.now().date()
        
        # 创建日期显示和选择按钮
        self.date_var = tk.StringVar(value=self.selected_date.strftime("%Y-%m-%d"))
        
        self.date_entry = ttk.Entry(self, textvariable=self.date_var, width=12)
        self.date_entry.pack(side=tk.LEFT, padx=(0, 2))
        
        self.calendar_btn = ttk.Button(self, text="📅", width=2, 
                                      command=self.show_calendar)
        self.calendar_btn.pack(side=tk.LEFT)
        
    def show_calendar(self):
        """显示日历选择器"""
        calendar = SimpleCalendar(self, callback=self.set_date)
        calendar.transient(self)  # 设置为父窗口的临时窗口
        calendar.grab_set()  # 获取交互焦点
        
    def set_date(self, date):
        """设置选择的日期"""
        self.selected_date = date
        self.date_var.set(date.strftime("%Y-%m-%d"))
        
    def get_date(self):
        """获取当前选择的日期"""
        return self.selected_date


class TaskDialog(tk.Toplevel):
    """任务添加/编辑对话框"""
    def __init__(self, parent, task_list=None, parent_task=None, start_date=None, callback=None):
        super().__init__(parent)
        self.parent = parent
        self.task_list = task_list or []
        self.parent_task = parent_task
        self.callback = callback
        
        self.title("添加任务")
        self.geometry("400x350")
        self.resizable(False, False)
        
        # 设置模态对话框
        self.transient(parent)
        self.grab_set()
        
        # 创建控件
        self.create_widgets(start_date)
        
        # 居中显示
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
    def create_widgets(self, start_date):
        frame = ttk.Frame(self, padding="20 20 20 20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 任务名称
        ttk.Label(frame, text="任务名称:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        self.name_entry = ttk.Entry(frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky=tk.W, pady=(0, 10))
        
        # 开始日期
        ttk.Label(frame, text="开始日期:").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        self.start_date = DateSelector(frame)
        self.start_date.grid(row=1, column=1, sticky=tk.W, pady=(0, 10))
        
        # 如果提供了开始日期，设置为默认值
        if start_date:
            self.start_date.set_date(start_date)
        
        # 结束日期
        ttk.Label(frame, text="结束日期:").grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        self.end_date = DateSelector(frame)
        self.end_date.grid(row=2, column=1, sticky=tk.W, pady=(0, 10))
        
        # 如果提供了开始日期，默认结束日期为一周后
        if start_date:
            end_date = start_date + datetime.timedelta(days=7)
            self.end_date.set_date(end_date)
        
        # 任务层级
        ttk.Label(frame, text="任务层级:").grid(row=3, column=0, sticky=tk.W, pady=(0, 10))
        self.level_var = tk.IntVar(value=0)
        
        level_frame = ttk.Frame(frame)
        level_frame.grid(row=3, column=1, sticky=tk.W, pady=(0, 10))
        
        ttk.Radiobutton(level_frame, text="主任务", variable=self.level_var, 
                       value=0, command=self.on_level_change).pack(side=tk.LEFT)
        ttk.Radiobutton(level_frame, text="子任务", variable=self.level_var, 
                       value=1, command=self.on_level_change).pack(side=tk.LEFT)
        ttk.Radiobutton(level_frame, text="子子任务", variable=self.level_var, 
                       value=2, command=self.on_level_change).pack(side=tk.LEFT)
        
        # 如果有父任务，默认为子任务
        if self.parent_task:
            if self.parent_task["level"] == 0:
                self.level_var.set(1)  # 父任务是主任务，则为子任务
            else:
                self.level_var.set(2)  # 父任务是子任务，则为子子任务
        
        # 父任务选择（仅当选择子任务或子子任务时显示）
        ttk.Label(frame, text="父任务:").grid(row=4, column=0, sticky=tk.W, pady=(0, 10))
        self.parent_var = tk.StringVar()
        self.parent_combo = ttk.Combobox(frame, textvariable=self.parent_var, width=28, state="readonly")
        self.parent_combo.grid(row=4, column=1, sticky=tk.W, pady=(0, 10))
        
        # 更新父任务列表
        self.update_parent_tasks()
        
        # 如果提供了父任务，设置为默认值
        if self.parent_task:
            self.parent_var.set(f"{self.parent_task['id']}: {self.parent_task['name']}")
        
        # 按钮区域
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="确定", command=self.confirm).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="取消", command=self.destroy).pack(side=tk.LEFT)
        
        # 初始化父任务选择器的可见性
        self.on_level_change()
        
    def on_level_change(self):
        """当任务层级改变时更新父任务选择器"""
        level = self.level_var.get()
        if level == 0:  # 主任务
            self.parent_combo.config(state="disabled")
            self.parent_var.set("")
        else:  # 子任务或子子任务
            self.parent_combo.config(state="readonly")
            # 更新父任务列表
            self.update_parent_tasks()
        
    def update_parent_tasks(self):
        """更新父任务下拉列表"""
        level = self.level_var.get()
        parent_options = []
        
        if level == 1:  # 子任务
            # 只显示主任务
            parent_options = [f"{task['id']}: {task['name']}" for task in self.task_list if task["level"] == 0]
        elif level == 2:  # 子子任务
            # 只显示子任务
            parent_options = [f"{task['id']}: {task['name']}" for task in self.task_list if task["level"] == 1]
        
        self.parent_combo['values'] = parent_options
        
        # 如果有值设置第一个为默认值
        if parent_options and not self.parent_var.get():
            self.parent_combo.current(0)
    
    def confirm(self):
        """确认添加任务"""
        # 获取输入值
        name = self.name_entry.get().strip()
        start = self.start_date.get_date()
        end = self.end_date.get_date()
        level = self.level_var.get()
        
        # 验证输入
        if not name:
            messagebox.showerror("错误", "请输入任务名称")
            return
        
        if end < start:
            messagebox.showerror("错误", "结束日期不能早于开始日期")
            return
        
        # 获取父任务ID
        parent_id = None
        if level > 0:
            parent_selection = self.parent_var.get()
            if not parent_selection:
                messagebox.showerror("错误", "请选择父任务")
                return
            parent_id = int(parent_selection.split(":")[0])
        
        # 回调函数传递任务数据
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
        """将任务转换为可序列化的格式"""
        serializable_tasks = []
        for task in tasks:
            task_copy = task.copy()
            # 将 datetime.date 转换为字符串
            task_copy['start'] = task_copy['start'].strftime('%Y-%m-%d')
            task_copy['end'] = task_copy['end'].strftime('%Y-%m-%d')
            
            # 将 RGB 颜色转换为 HSV 以便于存储和重现
            task_copy['color'] = list(rgb_to_hsv(task_copy['color']))
            
            serializable_tasks.append(task_copy)
        return serializable_tasks

    @staticmethod
    def convert_from_serializable(tasks):
        """将可序列化的任务转换回原始格式"""
        deserialized_tasks = []
        for task in tasks:
            task_copy = task.copy()
            # 将字符串日期转换回 datetime.date
            task_copy['start'] = datetime.datetime.strptime(task_copy['start'], '%Y-%m-%d').date()
            task_copy['end'] = datetime.datetime.strptime(task_copy['end'], '%Y-%m-%d').date()
            
            # 将 HSV 颜色转换回 RGB
            task_copy['color'] = hsv_to_rgb(task_copy['color'])
            
            deserialized_tasks.append(task_copy)
        return deserialized_tasks

def add_json_methods(cls):
    """为 GanttChartApp 类添加 JSON 保存和加载方法"""
    def save_to_json(self):
        """将当前任务保存到 JSON 文件"""
        if not self.tasks:
            messagebox.showinfo("提示", "没有可保存的任务")
            return

        # 打开文件对话框选择保存位置
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if not file_path:
            return

        try:
            # 将任务转换为可序列化格式
            serializable_tasks = JSONHandler.convert_to_serializable(self.tasks)
            
            # 保存到 JSON 文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(serializable_tasks, f, ensure_ascii=False, indent=4)
            
            messagebox.showinfo("成功", f"任务已保存到 {file_path}")
        except Exception as e:
            messagebox.showerror("错误", f"保存文件时发生错误：{str(e)}")

    def load_from_json(self):
        """从 JSON 文件加载任务"""
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON 文件", "*.json"), ("所有文件", "*.*")]
        )
        
        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                loaded_tasks = json.load(f)
            
            # 将加载的任务转换回原始格式
            deserialized_tasks = JSONHandler.convert_from_serializable(loaded_tasks)
            
            # 清空当前任务列表
            self.tasks.clear()
            
            # 重置任务ID计数器
            self.next_task_id = 1
            
            # 添加加载的任务
            for task in deserialized_tasks:
                # 为每个任务分配新的ID
                task['id'] = self.next_task_id
                self.next_task_id += 1
                
                self.tasks.append(task)
            
            # 更新任务列表和图表
            self.update_task_list()
            self.update_chart()
            
            messagebox.showinfo("成功", f"成功从 {file_path} 加载任务")
        
        except json.JSONDecodeError:
            messagebox.showerror("错误", "文件格式不正确")
        except Exception as e:
            messagebox.showerror("错误", f"加载文件时发生错误：{str(e)}")

    # 为类动态添加方法
    cls.save_to_json = save_to_json
    cls.load_from_json = load_from_json
    return cls

@add_json_methods
class GanttChartApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("甘特图管理系统")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        # 任务列表
        self.tasks = []
        self.next_task_id = 1  # 用于生成唯一任务ID
        
        # 初始日期（用于计算周数）
        self.initial_date = datetime.datetime.now().date()
        
        # 创建主框架
        self.main_frame = tk.Frame(root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建左侧输入区域
        self.input_frame = tk.Frame(self.main_frame, bg="#f0f0f0", width=350, 
                                    highlightbackground="#ddd", highlightthickness=1)
        self.input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10, pady=10)
        
        # 确保输入区域宽度固定
        self.input_frame.pack_propagate(False)
        
        # 创建右侧图表区域
        self.chart_frame = tk.Frame(self.main_frame, bg="white", 
                                   highlightbackground="#ddd", highlightthickness=1)
        self.chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建标题
        title_label = tk.Label(self.input_frame, text="任务管理", bg="#f0f0f0", 
                              font=("SimHei", 16, "bold"))
        title_label.pack(pady=(20, 30))
        
        # 创建输入字段和任务列表
        self.create_input_fields()
        
        # 创建甘特图画布
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 绑定鼠标事件
        self.canvas.mpl_connect('button_press_event', self.on_chart_click)
        
        # 初始化图表
        self.update_chart()
        
    def create_input_fields(self):
        # 添加任务按钮
        style = ttk.Style()
        style.configure("TButton", font=("SimHei", 10, "bold"))
        
        # 容器框架用于组织按钮
        button_frame = tk.Frame(self.input_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        add_button = ttk.Button(button_frame, text="添加任务", style="TButton", 
                            command=self.show_task_dialog)
        add_button.pack(side=tk.LEFT, padx=(0, 10))
        
        edit_button = ttk.Button(button_frame, text="编辑任务", style="TButton", 
                                command=self.edit_selected_task)
        edit_button.pack(side=tk.LEFT, padx=(0, 10))
        
        delete_button = ttk.Button(button_frame, text="删除任务", style="TButton", 
                                command=self.delete_selected_task)
        delete_button.pack(side=tk.LEFT)
        
        # 添加保存和加载按钮的新框架
        save_load_frame = tk.Frame(self.input_frame, bg="#f0f0f0")
        save_load_frame.pack(fill=tk.X, padx=20, pady=10)
        
        save_button = ttk.Button(save_load_frame, text="保存项目", style="TButton", 
                                command=self.save_to_json)
        save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        load_button = ttk.Button(save_load_frame, text="加载项目", style="TButton", 
                                command=self.load_from_json)
        load_button.pack(side=tk.LEFT)
        
        export_button = ttk.Button(save_load_frame, text="导出图片", style="TButton", 
                               command=self.export_chart_to_image)
        export_button.pack(side=tk.LEFT)
        
        # 任务列表框架
        task_list_frame = tk.Frame(self.input_frame, bg="#f0f0f0")
        task_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 10))
        
        task_list_label = tk.Label(task_list_frame, text="当前任务列表", bg="#f0f0f0", 
                                  font=("SimHei", 12, "bold"))
        task_list_label.pack(anchor="w", pady=(0, 10))
        
        # 创建任务列表的树视图
        columns = ("ID", "名称", "开始", "结束", "层级", "父任务")
        self.task_tree = ttk.Treeview(task_list_frame, columns=columns, 
                                    show="headings", height=18)
        
        # 定义列
        self.task_tree.heading("ID", text="ID")
        self.task_tree.heading("名称", text="名称")
        self.task_tree.heading("开始", text="开始日期")
        self.task_tree.heading("结束", text="结束日期")
        self.task_tree.heading("层级", text="层级")
        self.task_tree.heading("父任务", text="父任务")
        
        # 设置列宽
        self.task_tree.column("ID", width=30)
        self.task_tree.column("名称", width=100)
        self.task_tree.column("开始", width=80)
        self.task_tree.column("结束", width=80)
        self.task_tree.column("层级", width=50)
        self.task_tree.column("父任务", width=80)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(task_list_frame, orient="vertical", command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=scrollbar.set)
        
        self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定双击事件
        self.task_tree.bind("<Double-1>", lambda e: self.edit_selected_task())
        
    def show_task_dialog(self, parent_task=None, start_date=None):
        """显示任务添加对话框"""
        dialog = TaskDialog(
            self.root, 
            task_list=self.tasks, 
            parent_task=parent_task,
            start_date=start_date,
            callback=self.add_task
        )
        
    def edit_selected_task(self):
        """编辑选中的任务"""
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showinfo("提示", "请先选择要编辑的任务")
            return
            
        # 获取选中的任务ID
        task_id = int(self.task_tree.item(selected_item[0])['values'][0])
        
        # 查找任务
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if not task:
            return
            
        # TODO: 实现编辑功能
        messagebox.showinfo("提示", f"编辑任务 {task['name']} 的功能正在开发中")
        
    def delete_selected_task(self):
        """删除选中的任务"""
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showinfo("提示", "请先选择要删除的任务")
            return
            
        # 获取选中的任务ID
        task_id = int(self.task_tree.item(selected_item[0])['values'][0])
        
        # 查找任务
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if not task:
            return
            
        # 确认删除
        if not messagebox.askyesno("确认", f"确定要删除任务 \"{task['name']}\" 吗？"):
            return
            
        # 检查是否有子任务
        has_children = any(t["parent_id"] == task_id for t in self.tasks)
        if has_children:
            if messagebox.askyesno("警告", "该任务有子任务，删除它将同时删除所有子任务。确定要继续吗？"):
                # 递归删除子任务
                self.delete_task_and_children(task_id)
        else:
            # 直接删除任务
            self.tasks = [t for t in self.tasks if t["id"] != task_id]
            
        # 更新任务列表和图表
        self.update_task_list()
        self.update_chart()
        
    def delete_task_and_children(self, task_id):
        """递归删除任务及其子任务"""
        # 找出所有子任务ID
        child_ids = [t["id"] for t in self.tasks if t.get("parent_id") == task_id]
        
        # 递归删除子任务
        for child_id in child_ids:
            self.delete_task_and_children(child_id)
            
        # 删除当前任务
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        
    def add_task(self, task_data):
        """添加任务"""
        # 生成随机HSV色调
        hue = random.random()  # 随机色相
        saturation = 0.8  # 固定饱和度
        value = max(0.5, 1.0 - task_data["level"] * 0.2)  # 根据层级调整亮度
        
        # 创建新任务
        task = {
            "id": self.next_task_id,
            "name": task_data["name"],
            "start": task_data["start"],
            "end": task_data["end"],
            "level": task_data["level"],
            "parent_id": task_data["parent_id"],
            "color": hsv_to_rgb([hue, saturation, value])
        }
        
        # 增加ID计数器
        self.next_task_id += 1
        
        # 如果是子任务，检查是否需要调整日期范围
        if task["parent_id"]:
            parent_task = next((t for t in self.tasks if t["id"] == task["parent_id"]), None)
            if parent_task:
                # 确保子任务的时间范围在父任务之内
                if task["start"] < parent_task["start"]:
                    task["start"] = parent_task["start"]
                if task["end"] > parent_task["end"]:
                    task["end"] = parent_task["end"]
                    messagebox.showinfo("提示", f"子任务结束日期已调整为与父任务一致: {parent_task['end'].strftime('%Y-%m-%d')}")
        
        # 添加任务到列表
        self.tasks.append(task)
        
        # 更新任务列表和图表
        self.update_task_list()
        self.update_chart()
        
    def update_task_list(self):
        """更新任务列表视图"""
        # 清空现有项
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
            
        # 添加所有任务
        for task in self.tasks:
            # 获取父任务名称（如果有）
            parent_name = ""
            if task["parent_id"]:
                parent = next((t for t in self.tasks if t["id"] == task["parent_id"]), None)
                if parent:
                    parent_name = parent["name"]
                    
            # 获取层级名称
            level_names = ["主任务", "子任务", "子子任务"]
            level_name = level_names[task["level"]] if task["level"] < len(level_names) else f"层级 {task['level']}"
                    
            # 添加到树形视图
            self.task_tree.insert(
                "", 
                "end", 
                values=(
                    task["id"],
                    task["name"],
                    task["start"].strftime("%Y-%m-%d"),
                    task["end"].strftime("%Y-%m-%d"),
                    level_name,
                    parent_name
                )
            )
    def export_chart_to_image(self):
        """导出甘特图为图片"""
        # 弹出文件保存对话框
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG 图片", "*.png"),
                ("JPEG 图片", "*.jpg"),
                ("SVG 矢量图", "*.svg"),
                ("PDF 文件", "*.pdf"),
                ("所有文件", "*.*")
            ]
        )
        
        if not file_path:
            return

        try:
            # 调整图表布局，确保导出的图片看起来整洁
            self.fig.tight_layout(pad=2.0)
            
            # 导出图片
            # 对于位图格式（PNG、JPEG），使用较高的 DPI 获得清晰图像
            # 对于矢量格式（SVG、PDF），使用默认 DPI
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.fig.savefig(file_path, dpi=300, bbox_inches='tight')
            else:
                self.fig.savefig(file_path, bbox_inches='tight')
            
            # 显示成功消息
            messagebox.showinfo("导出成功", f"甘特图已成功导出到 {file_path}")
        
        except Exception as e:
            # 处理可能的导出错误
            messagebox.showerror("导出错误", f"导出图片时发生错误：{str(e)}")  
    def update_chart(self):
        """更新甘特图"""
        self.ax.clear()
        
        if not self.tasks:
            self.ax.text(0.5, 0.5, "尚无任务数据", ha='center', va='center', transform=self.ax.transAxes)
            self.canvas.draw()
            return
            
        # 计算图表的日期范围
        min_date = min(task["start"] for task in self.tasks)
        max_date = max(task["end"] for task in self.tasks)
        
        # 确保至少有1周的显示范围
        if (max_date - min_date).days < 7:
            max_date = min_date + datetime.timedelta(days=7)
            
        # 更新初始日期（用于计算周数）
        self.initial_date = min_date
            
        # 设置横轴日期格式
        self.ax.xaxis_date()
        
        # 设置图表参数
        self.ax.set_xlim([min_date - datetime.timedelta(days=1), max_date + datetime.timedelta(days=1)])
        self.ax.set_title("项目甘特图", fontsize=14, pad=20)
        
        # 设置Y轴标签和刻度
        task_names = []
        y_positions = []
        
        # 按层级和父任务分组和排序任务
        sorted_tasks = self.sort_tasks_hierarchically()
        
        for i, task in enumerate(sorted_tasks):
            # 计算Y位置（任务列表从上到下）
            y_pos = len(sorted_tasks) - i - 1
            
            # 任务开始和结束日期
            start_date = task["start"]
            end_date = task["end"]
            duration = (end_date - start_date).days + 1  # 包括结束日期
            
            # 根据任务层级设置任务名称的缩进
            indent = "  " * task["level"]
            task_name = f"{indent}{task['name']}"
            
            # 添加到名称和位置列表
            task_names.append(task_name)
            y_positions.append(y_pos)
            
            # 绘制任务条
            bar_height = 0.5
            
            # 根据任务层级设置不同的偏移和高度
            if task["level"] > 0:
                # 子任务略窄和偏离中心
                bar_height = 0.4
                
            # 绘制任务条
            self.ax.barh(
                y_pos,
                duration,
                left=start_date,
                height=bar_height,
                align='center',
                color=task["color"],
                alpha=0.8,
                edgecolor='black',
                linewidth=1
            )
            
            # 为长任务添加任务名称
            if duration > 3:  # 如果任务持续超过3天，在任务条内显示名称
                # 计算任务条中点
                mid_date = start_date + datetime.timedelta(days=duration / 2)
                self.ax.text(
                    mid_date, 
                    y_pos, 
                    task["name"],
                    ha='center',
                    va='center',
                    color='black',
                    fontsize=8,
                    fontweight='bold'
                )
            
            # 绘制父子任务的连接线
            if task["parent_id"]:
                parent = next((t for t in sorted_tasks if t["id"] == task["parent_id"]), None)
                if parent:
                    # 获取父任务的Y位置
                    parent_index = sorted_tasks.index(parent)
                    parent_y_pos = len(sorted_tasks) - parent_index - 1
                    
                    # 绘制连接线
                    self.ax.plot(
                        [start_date, start_date], 
                        [y_pos + bar_height/2, parent_y_pos - bar_height/2],
                        'k--', 
                        alpha=0.3,
                        linewidth=1
                    )
        
        # 设置Y轴刻度和标签
        self.ax.set_yticks(y_positions)
        self.ax.set_yticklabels(task_names)
        
        # 设置网格线
        self.ax.grid(True, axis='x', linestyle='--', alpha=0.7)
        
        # # 设置今天的垂直线
        # today = datetime.datetime.now().date()
        # if min_date <= today <= max_date:
        #     self.ax.axvline(today, color='red', linestyle='-', linewidth=2, alpha=0.7)
            
        #     # 在图表顶部添加"今天"标签
        #     self.ax.text(today, self.ax.get_ylim()[1], " 今天", 
        #                 ha='left', va='top', color='red', fontsize=9, 
        #                 transform=self.ax.get_xaxis_transform())
        
        # 设置周末底色
        self.highlight_weekends(min_date, max_date)
        
        # 调整布局
        self.fig.tight_layout()
        
        # 刷新画布
        self.canvas.draw()
        
    def sort_tasks_hierarchically(self):
        """按层级和父子关系排序任务"""
        # 创建任务副本
        sorted_tasks = []
        
        # 首先添加主任务
        main_tasks = [task for task in self.tasks if task["level"] == 0]
        
        # 对于每个主任务，递归添加其子任务
        for main_task in main_tasks:
            sorted_tasks.append(main_task)
            self.add_subtasks_recursively(main_task["id"], sorted_tasks)
            
        return sorted_tasks
        
    def add_subtasks_recursively(self, parent_id, sorted_tasks):
        """递归添加子任务到排序列表"""
        # 查找直接子任务
        subtasks = [task for task in self.tasks if task["parent_id"] == parent_id]
        
        for subtask in subtasks:
            sorted_tasks.append(subtask)
            # 递归添加子任务的子任务
            self.add_subtasks_recursively(subtask["id"], sorted_tasks)
            
    def highlight_weekends(self, start_date, end_date):
        """在甘特图中高亮显示周末"""
        # 计算日期范围内的所有日期
        delta = (end_date - start_date).days + 1
        all_dates = [start_date + datetime.timedelta(days=i) for i in range(delta)]
        
        # 找出所有周六周日
        weekends = [date for date in all_dates if date.weekday() >= 5]  # 5=周六, 6=周日
        
        # 高亮周末区域
        for weekend in weekends:
            self.ax.axvspan(
                weekend, 
                weekend + datetime.timedelta(days=1), 
                facecolor='lightgray', 
                alpha=0.3,
                zorder=0
            )
            
    def on_chart_click(self, event):
        """处理图表点击事件"""
        # 检查点击是否在绘图区域内
        if event.xdata is None or event.ydata is None:
            return
            
        # 将x坐标转换为日期
        clicked_date = matplotlib.dates.num2date(event.xdata).date()
        
        # 检查是否双击（添加新任务）
        if event.dblclick:
            # 显示添加任务对话框
            self.show_task_dialog(start_date=clicked_date)
            return
            
        # 计算点击位置对应的任务（如果有）
        sorted_tasks = self.sort_tasks_hierarchically()
        
        # 转换y坐标到任务索引
        y_index = len(sorted_tasks) - int(round(event.ydata)) - 1
        
        # 确保索引在有效范围内
        if 0 <= y_index < len(sorted_tasks):
            clicked_task = sorted_tasks[y_index]
            
            # 检查点击是否在任务条上
            task_start = clicked_task["start"]
            task_end = clicked_task["end"]
            
            if task_start <= clicked_date <= task_end:
                # 点击在任务条上，显示任务详情或快捷菜单
                self.show_task_menu(event, clicked_task)
                
    def show_task_menu(self, event, task):
        """显示任务的右键菜单"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label=f"任务: {task['name']}")
        menu.add_separator()
        menu.add_command(label="编辑任务", command=lambda: self.edit_task(task))
        menu.add_command(label="添加子任务", command=lambda: self.show_task_dialog(parent_task=task))
        menu.add_command(label="删除任务", command=lambda: self.confirm_delete_task(task))
        
        # 显示菜单
        try:
            menu.tk_popup(event.canvas.winfo_rootx() + event.x, 
                        event.canvas.winfo_rooty() + event.y)
        finally:
            menu.grab_release()
            
    def edit_task(self, task):
        """编辑任务"""
        # TODO: 实现编辑功能
        messagebox.showinfo("提示", f"编辑任务 {task['name']} 的功能正在开发中")
        
    def confirm_delete_task(self, task):
        """确认删除任务"""
        if messagebox.askyesno("确认", f"确定要删除任务 \"{task['name']}\" 吗？"):
            # 检查是否有子任务
            has_children = any(t["parent_id"] == task["id"] for t in self.tasks)
            if has_children:
                if messagebox.askyesno("警告", "该任务有子任务，删除它将同时删除所有子任务。确定要继续吗？"):
                    # 递归删除任务及其子任务
                    self.delete_task_and_children(task["id"])
            else:
                # 直接删除任务
                self.tasks = [t for t in self.tasks if t["id"] != task["id"]]
                
            # 更新任务列表和图表
            self.update_task_list()
            self.update_chart()


# 程序入口
if __name__ == "__main__":
    root = tk.Tk()
    app = GanttChartApp(root)
    root.mainloop()