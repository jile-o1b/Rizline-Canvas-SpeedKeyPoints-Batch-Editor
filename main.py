import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math
#你好啊

class RizlineSpeedTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Rizline 速度节点批量添加工具")
        self.root.geometry("900x650")
        self.root.minsize(900, 650)
        self.root.pack_propagate(False)
        
        self.chart_data = None
        self.current_file = None
        self.canvas_count = 0
        
        # 缓动类型分类
        self.ease_categories = {
            "Linear": ["线性"],
            "Sine": ["In", "Out", "InOut"],
            "Quad": ["In", "Out", "InOut"],
            "Cubic": ["In", "Out", "InOut"],
            "Quart": ["In", "Out", "InOut"]
        }
        
        # 缓动函数映射到easeType编号
        self.ease_type_mapping = {
            ("Linear", "线性"): 0,
            ("Sine", "In"): 1,
            ("Sine", "Out"): 2,
            ("Sine", "InOut"): 3,
            ("Quad", "In"): 4,
            ("Quad", "Out"): 5,
            ("Quad", "InOut"): 6,
            ("Cubic", "In"): 7,
            ("Cubic", "Out"): 8,
            ("Cubic", "InOut"): 9,
            ("Quart", "In"): 10,
            ("Quart", "Out"): 11,
            ("Quart", "InOut"): 12,
        }
        
        self.setup_ui()
    
    # ========== 缓动函数 ==========
    def ease_linear(self, t):
        """线性"""
        return t
    
    # Sine 缓动
    def ease_sine_in(self, t):
        """Sine In"""
        return 1 - math.cos((t * math.pi) / 2)
    
    def ease_sine_out(self, t):
        """Sine Out"""
        return math.sin((t * math.pi) / 2)
    
    def ease_sine_inout(self, t):
        """Sine InOut"""
        return -(math.cos(math.pi * t) - 1) / 2
    
    # Quad 缓动
    def ease_quad_in(self, t):
        """Quad In"""
        return t * t
    
    def ease_quad_out(self, t):
        """Quad Out"""
        return t * (2 - t)
    
    def ease_quad_inout(self, t):
        """Quad InOut"""
        if t < 0.5:
            return 2 * t * t
        else:
            return 1 - pow(-2 * t + 2, 2) / 2
    
    # Cubic 缓动
    def ease_cubic_in(self, t):
        """Cubic In"""
        return t * t * t
    
    def ease_cubic_out(self, t):
        """Cubic Out"""
        return 1 - pow(1 - t, 3)
    
    def ease_cubic_inout(self, t):
        """Cubic InOut"""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2
    
    # Quart 缓动
    def ease_quart_in(self, t):
        """Quart In"""
        return t * t * t * t
    
    def ease_quart_out(self, t):
        """Quart Out"""
        return 1 - pow(1 - t, 4)
    
    def ease_quart_inout(self, t):
        """Quart InOut"""
        if t < 0.5:
            return 8 * t * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 4) / 2
    
    def apply_easing(self, t, category, style):
        """应用缓动函数"""
        if category == "Linear":
            return self.ease_linear(t)
        elif category == "Sine":
            if style == "In":
                return self.ease_sine_in(t)
            elif style == "Out":
                return self.ease_sine_out(t)
            elif style == "InOut":
                return self.ease_sine_inout(t)
        elif category == "Quad":
            if style == "In":
                return self.ease_quad_in(t)
            elif style == "Out":
                return self.ease_quad_out(t)
            elif style == "InOut":
                return self.ease_quad_inout(t)
        elif category == "Cubic":
            if style == "In":
                return self.ease_cubic_in(t)
            elif style == "Out":
                return self.ease_cubic_out(t)
            elif style == "InOut":
                return self.ease_cubic_inout(t)
        elif category == "Quart":
            if style == "In":
                return self.ease_quart_in(t)
            elif style == "Out":
                return self.ease_quart_out(t)
            elif style == "InOut":
                return self.ease_quart_inout(t)
        
        return t  # 默认线性
    
    def get_ease_type_number(self, category, style):
        """根据缓动分类和样式获取对应的 easeType 编号"""
        key = (category, style)
        return self.ease_type_mapping.get(key, 0)
    
    def setup_ui(self):
        # 文件选择区域
        file_frame = ttk.LabelFrame(self.root, text="文件操作", padding=10)
        file_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(file_frame, text="加载谱面文件", command=self.load_file).pack(side="left", padx=5)
        self.file_label = ttk.Label(file_frame, text="未加载文件")
        self.file_label.pack(side="left", padx=5)
        
        # 显示当前文件路径的小标签
        self.path_label = ttk.Label(file_frame, text="", foreground="gray")
        self.path_label.pack(side="left", padx=10)
        
        # 画布选择区域
        canvas_frame = ttk.LabelFrame(self.root, text="画布选择", padding=10)
        canvas_frame.pack(fill="x", padx=10, pady=5)
        
        self.canvas_var = tk.StringVar()
        self.canvas_combo = ttk.Combobox(canvas_frame, textvariable=self.canvas_var, state="readonly", width=20)
        self.canvas_combo.pack(side="left", padx=5)
        # 画布选择后自动加载节点
        self.canvas_combo.bind('<<ComboboxSelected>>', self.on_canvas_selected)
        
        # 速度节点参数区域
        param_frame = ttk.LabelFrame(self.root, text="批量添加参数", padding=10)
        param_frame.pack(fill="x", padx=10, pady=5)
        
        # 时间范围（节拍）
        time_frame = ttk.Frame(param_frame)
        time_frame.pack(fill="x", pady=5)
        ttk.Label(time_frame, text="开始节拍:", width=12).pack(side="left")
        self.start_time = ttk.Entry(time_frame, width=15)
        self.start_time.pack(side="left", padx=5)
        ttk.Label(time_frame, text="结束节拍:", width=12).pack(side="left")
        self.end_time = ttk.Entry(time_frame, width=15)
        self.end_time.pack(side="left", padx=5)
        
        # 速度值范围
        speed_frame = ttk.Frame(param_frame)
        speed_frame.pack(fill="x", pady=5)
        ttk.Label(speed_frame, text="开始速度:", width=12).pack(side="left")
        self.start_speed = ttk.Entry(speed_frame, width=15)
        self.start_speed.pack(side="left", padx=5)
        ttk.Label(speed_frame, text="结束速度:", width=12).pack(side="left")
        self.end_speed = ttk.Entry(speed_frame, width=15)
        self.end_speed.pack(side="left", padx=5)
        
        # 填充密度（1/N）
        density_frame = ttk.Frame(param_frame)
        density_frame.pack(fill="x", pady=5)
        ttk.Label(density_frame, text="填充密度 (1/):", width=12).pack(side="left")
        self.density = ttk.Entry(density_frame, width=15)
        self.density.insert(0, "4")
        self.density.pack(side="left", padx=5)
        ttk.Label(density_frame, text="(将时间区间分成 N 段)", width=25).pack(side="left")
        
        # 缓动类型选择（两个选择框放在一行）
        ease_frame = ttk.Frame(param_frame)
        ease_frame.pack(fill="x", pady=5)
        
        ttk.Label(ease_frame, text="缓动:", width=12).pack(side="left")
        
        # 第一级：缓动分类
        self.category_var = tk.StringVar(value="Linear")
        self.category_combo = ttk.Combobox(ease_frame, textvariable=self.category_var, state="readonly", width=12)
        self.category_combo['values'] = list(self.ease_categories.keys())
        self.category_combo.pack(side="left", padx=2)
        self.category_combo.bind('<<ComboboxSelected>>', self.on_category_change)
        
        # 第二级：缓动样式
        self.style_var = tk.StringVar(value="线性")
        self.style_combo = ttk.Combobox(ease_frame, textvariable=self.style_var, state="readonly", width=8)
        self.style_combo.pack(side="left", padx=2)
        
        # 初始化样式下拉框
        self.update_style_combo()
        
        # 缓动预览按钮
        ttk.Button(ease_frame, text="预览曲线", command=self.preview_easing).pack(side="left", padx=10)
        
        # 操作按钮
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="预览节点", command=self.preview_nodes).pack(side="left", padx=5)
        ttk.Button(button_frame, text="添加节点", command=self.add_nodes).pack(side="left", padx=5)
        ttk.Button(button_frame, text="保存到原文件", command=self.save_file).pack(side="left", padx=5)
        
        # 预览区域
        preview_container = ttk.Frame(self.root)
        preview_container.pack(fill="both", expand=True, padx=10, pady=5)
        preview_container.pack_propagate(False)
        
        # 左侧速度节点表格
        left_frame = ttk.LabelFrame(preview_container, text="速度节点列表", padding=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0,5))
        
        columns = ("序号", "节拍(Beats)", "速度(Speed)", "累计位移(Floor Position)")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 右侧缓动预览表格
        right_frame = ttk.LabelFrame(preview_container, text="缓动曲线预览", padding=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5,0))
        
        self.ease_tree = ttk.Treeview(right_frame, columns=("进度", "缓动值"), show="headings", height=12)
        self.ease_tree.heading("进度", text="进度 (0-1)")
        self.ease_tree.heading("缓动值", text="缓动后比例")
        self.ease_tree.column("进度", width=100)
        self.ease_tree.column("缓动值", width=100)
        
        ease_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.ease_tree.yview)
        self.ease_tree.configure(yscrollcommand=ease_scrollbar.set)
        
        self.ease_tree.pack(side="left", fill="both", expand=True)
        ease_scrollbar.pack(side="right", fill="y")
        
        # 状态栏
        self.status_label = ttk.Label(self.root, text="就绪", relief="sunken")
        self.status_label.pack(fill="x", padx=10, pady=5)
    
    def on_canvas_selected(self, event=None):
        """选择画布后自动加载节点"""
        self.view_speed_points()
    
    def on_category_change(self, event=None):
        """当缓动分类改变时，更新样式下拉框"""
        self.update_style_combo()
        self.preview_easing()
    
    def update_style_combo(self):
        """更新样式下拉框的选项"""
        category = self.category_var.get()
        styles = self.ease_categories.get(category, ["线性"])
        self.style_combo['values'] = styles
        if styles:
            self.style_combo.current(0)
    
    def load_file(self):
        """加载谱面文件"""
        file_path = filedialog.askopenfilename(
            title="选择 Rizline 谱面文件",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.chart_data = json.load(f)
            
            self.current_file = file_path
            filename = file_path.split('/')[-1]
            self.file_label.config(text=f"已加载: {filename}")
            short_path = file_path if len(file_path) < 50 else "..." + file_path[-47:]
            self.path_label.config(text=short_path)
            
            if "canvasMoves" in self.chart_data:
                self.canvas_count = len(self.chart_data["canvasMoves"])
                canvas_options = [f"画布 {i}" for i in range(self.canvas_count)]
                self.canvas_combo['values'] = canvas_options
                if canvas_options:
                    self.canvas_combo.current(0)
                    self.view_speed_points()
                    
            self.status_label.config(text=f"加载成功，包含 {self.canvas_count} 个画布")
            
        except Exception as e:
            messagebox.showerror("错误", f"加载文件失败: {str(e)}")
    
    def preview_easing(self):
        """预览缓动曲线"""
        category = self.category_var.get()
        style = self.style_var.get()
        
        for item in self.ease_tree.get_children():
            self.ease_tree.delete(item)
        
        steps = 11
        for i in range(steps):
            t = i / (steps - 1)
            eased = self.apply_easing(t, category, style)
            self.ease_tree.insert("", "end", values=(
                f"{t:.1f}",
                f"{eased:.3f}"
            ))
        
        self.status_label.config(text=f"缓动类型: {category} {style}")
    
    def get_current_canvas_index(self):
        """获取当前选择的画布索引"""
        selection = self.canvas_var.get()
        if not selection:
            return None
        return int(selection.split(" ")[1])
    
    def tick_to_seconds(self, tick):
        """将 tick 转换为秒"""
        bpm = self.chart_data.get("bPM", 200.0)
        return tick * (60.0 / bpm)
    
    def view_speed_points(self):
        """查看当前画布的速度节点"""
        canvas_idx = self.get_current_canvas_index()
        if canvas_idx is None:
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        speed_points = self.chart_data["canvasMoves"][canvas_idx]["speedKeyPoints"]
        
        for i, point in enumerate(speed_points):
            # 节拍保持原样显示
            time_str = str(point['time'])
            if time_str.endswith('.0'):
                time_str = time_str[:-2]
                
            self.tree.insert("", "end", values=(
                i,
                time_str,
                f"{point['value']:.3f}",
                f"{point['floorPosition']:.6f}"
            ))
        
        self.status_label.config(text=f"画布 {canvas_idx} 共有 {len(speed_points)} 个速度节点")
    
    def generate_new_nodes(self):
        """生成新的速度节点（带缓动）"""
        try:
            start_t = float(self.start_time.get())
            end_t = float(self.end_time.get())
            start_v = float(self.start_speed.get())
            end_v = float(self.end_speed.get())
            segments = int(self.density.get())
            
            category = self.category_var.get()
            style = self.style_var.get()
            ease_type_num = self.get_ease_type_number(category, style)
            
            if start_t >= end_t:
                messagebox.showerror("错误", "开始节拍必须小于结束节拍")
                return None
            
            if segments < 1:
                messagebox.showerror("错误", "段数必须大于等于1")
                return None
            
            time_step = (end_t - start_t) / segments
            
            nodes = []
            for i in range(segments + 1):
                t = start_t + i * time_step
                if i == segments:
                    t = end_t
                
                linear_progress = i / segments
                eased_progress = self.apply_easing(linear_progress, category, style)
                v = start_v + (end_v - start_v) * eased_progress
                
                nodes.append({
                    "time": t,
                    "value": v,
                    "easeType": ease_type_num,
                    "floorPosition": 0
                })
            
            return nodes
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
            return None
    
    def preview_nodes(self):
        """预览要添加的节点"""
        canvas_idx = self.get_current_canvas_index()
        if canvas_idx is None:
            messagebox.showwarning("警告", "请先选择画布")
            return
        
        try:
            start_t = float(self.start_time.get())
            end_t = float(self.end_time.get())
        except:
            messagebox.showerror("错误", "请先填写有效的节拍")
            return
        
        new_nodes = self.generate_new_nodes()
        if not new_nodes:
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        category = self.category_var.get()
        style = self.style_var.get()
        for i, node in enumerate(new_nodes):
            progress = (i / (len(new_nodes) - 1)) * 100 if len(new_nodes) > 1 else 0
            
            time_str = str(node['time'])
            if time_str.endswith('.0'):
                time_str = time_str[:-2]
                
            self.tree.insert("", "end", values=(
                f"新{i}",
                time_str,
                f"{node['value']:.3f} ({progress:.0f}%)",
                "待计算"
            ))
        
        segments = int(self.density.get())
        self.status_label.config(
            text=f"预览：{category} {style}，节拍区间 {start_t:.2f}-{end_t:.2f} 分成 {segments} 段，添加 {len(new_nodes)} 个节点"
        )
    
    def add_nodes(self):
        """批量添加速度节点"""
        canvas_idx = self.get_current_canvas_index()
        if canvas_idx is None:
            messagebox.showwarning("警告", "请先选择画布")
            return
        
        if not self.chart_data or not self.current_file:
            messagebox.showwarning("警告", "请先加载谱面文件")
            return
        
        new_nodes = self.generate_new_nodes()
        if not new_nodes:
            return
        
        existing_points = self.chart_data["canvasMoves"][canvas_idx]["speedKeyPoints"]
        
        # 冲突检测
        conflict_times = set()
        for new_node in new_nodes:
            for existing_node in existing_points:
                if abs(new_node["time"] - existing_node["time"]) < 0.000001:
                    conflict_times.add(existing_node["time"])
        
        # 过滤冲突节点
        filtered_nodes = []
        for node in new_nodes:
            is_conflict = False
            for conflict_time in conflict_times:
                if abs(node["time"] - conflict_time) < 0.000001:
                    is_conflict = True
                    break
            if not is_conflict:
                filtered_nodes.append(node)
        
        # 显示冲突提示
        if conflict_times:
            conflict_list = []
            for t in sorted(conflict_times):
                t_str = str(t)
                if t_str.endswith('.0'):
                    t_str = t_str[:-2]
                conflict_list.append(t_str)
            
            messagebox.showinfo(
                "节点冲突", 
                f"以下节拍点已有节点，已自动保留原节点：\n{', '.join(conflict_list)}\n\n(共 {len(conflict_times)} 个冲突)"
            )
        
        if not filtered_nodes:
            messagebox.showinfo("提示", "所有新节点都与现有节点冲突，没有添加任何节点")
            self.view_speed_points()
            return
        
        # 合并并排序
        all_points = existing_points + filtered_nodes
        all_points.sort(key=lambda x: x["time"])
        
        # 重新计算 floorPosition
        if all_points:
            all_points[0]["floorPosition"] = 0.0
            for i in range(1, len(all_points)):
                prev = all_points[i-1]
                curr = all_points[i]
                time_diff_sec = self.tick_to_seconds(curr["time"] - prev["time"])
                curr["floorPosition"] = prev["floorPosition"] + time_diff_sec * prev["value"]
        
        self.chart_data["canvasMoves"][canvas_idx]["speedKeyPoints"] = all_points
        
        self.view_speed_points()
        
        category = self.category_var.get()
        style = self.style_var.get()
        segments = int(self.density.get())
        conflict_count = len(conflict_times)
        added_count = len(filtered_nodes)
        
        self.status_label.config(
            text=f"✅ 已添加 {added_count} 个新节点（{category} {style}，分成 {segments} 段），"
                 f"跳过 {conflict_count} 个冲突节点，现有 {len(all_points)} 个节点。记得保存！"
        )
    
    def save_file(self):
        """直接保存到原文件"""
        if not self.chart_data or not self.current_file:
            messagebox.showwarning("警告", "没有可保存的数据")
            return
        
        result = messagebox.askyesno(
            "确认保存",
            f"确定要直接保存到原文件吗？\n\n{self.current_file}\n\n此操作将覆盖原文件！",
            icon='warning'
        )
        
        if not result:
            self.status_label.config(text="保存已取消")
            return
        
        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                json.dump(self.chart_data, f, indent=2, ensure_ascii=False)
            
            self.status_label.config(text=f"✅ 保存成功: {self.current_file}")
            messagebox.showinfo("成功", "文件保存成功！")
            
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RizlineSpeedTool(root)
    root.mainloop()