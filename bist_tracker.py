try:
    import customtkinter as ctk
    import yfinance as yf
    from datetime import datetime, timedelta
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    import matplotlib
    import traceback
    
    print("Tüm modüller başarıyla yüklendi.")
    
    matplotlib.use('TkAgg')

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    print("Tema ayarları yapıldı.")
    
    class ScrollableFrame(ctk.CTkScrollableFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)
            self.grid_columnconfigure(0, weight=1)
    
    class CustomTable(ctk.CTkFrame):
        def __init__(self, master, rows, columns, headers=None, on_row_click=None, **kwargs):
            super().__init__(master, **kwargs)
            
            self.rows = rows
            self.columns = columns
            self.cells = []
            self.on_row_click = on_row_click
            self.last_click_time = 0 
        
            self.scroll_frame = ScrollableFrame(self)
            self.scroll_frame.pack(fill="both", expand=True)
            
            if headers:
                header_row = []
                for col, header in enumerate(headers):
                    label = ctk.CTkLabel(self.scroll_frame, text=header,
                                       font=("Segoe UI", 12, "bold"))
                    label.grid(row=0, column=col, padx=2, pady=2, sticky="nsew")
                    header_row.append(label)
                    self.scroll_frame.grid_columnconfigure(col, weight=1)
            
            for row in range(rows):
                row_cells = []
                row_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
                row_frame.grid(row=row + (1 if headers else 0), column=0,
                             columnspan=columns, padx=5, pady=3, sticky="nsew")
                
                bar_frame = ctk.CTkFrame(row_frame, fg_color="#2b2b2b",
                                       corner_radius=6)
                bar_frame.pack(fill="both", expand=True, padx=0, pady=0)
                
                bar_frame.grid_columnconfigure((0,1,2,3,4,5), weight=1)
                
                for col in range(columns):
                    label = ctk.CTkLabel(bar_frame, text="",
                                       font=("Segoe UI", 12))
                    label.grid(row=0, column=col, padx=10, pady=8, sticky="nsew")
                    
                    if self.on_row_click:
                        label.bind("<Double-Button-1>", lambda e, r=row: self.handle_click(r))
                        bar_frame.bind("<Double-Button-1>", lambda e, r=row: self.handle_click(r))
                    
                    row_cells.append(label)
                
                self.cells.append((row_cells, bar_frame))
        
        def handle_click(self, row):
            if self.on_row_click:
                self.on_row_click(row)
        
        def set(self, row, col, value):
            if 0 <= row < self.rows and 0 <= col < self.columns:
                cells, bar_frame = self.cells[row]
                cells[col].configure(text=value)
                
                if col == 2 and value:
                    try:
                        change = float(value.replace('%', ''))
                        if change > 0:
                            bar_frame.configure(fg_color="#1e3d2d")  # Koyu yeşil
                        elif change < 0:
                            bar_frame.configure(fg_color="#3d1e1e")  # Koyu kırmızı
                        else:
                            bar_frame.configure(fg_color="#2b2b2b")  # Nötr
                    except ValueError:
                        bar_frame.configure(fg_color="#2b2b2b")  # Nötr
    
    class StockAnalysisWindow(ctk.CTkToplevel):
        def __init__(self, symbol):
            super().__init__()
            self.title(f"{symbol} Hisse Analizi")
            self.geometry("1000x800")
            
            self.symbol = symbol
            self.stock = yf.Ticker(f"{symbol}.IS")
            self.selected_range = ctk.StringVar(value="1y")
            
            self.create_widgets()
            
        def create_widgets(self):
            container = ctk.CTkFrame(self)
            container.pack(fill="both", expand=True, padx=20, pady=20)
            
            top_frame = ctk.CTkFrame(container)
            top_frame.pack(fill="x", pady=(0, 20))
            
            info = self.stock.info
            company_name = info.get('longName', self.symbol)
            ctk.CTkLabel(top_frame, text=f"{self.symbol} - {company_name}",
                        font=("Segoe UI", 24, "bold")).pack(side="left")
            
            price_frame = ctk.CTkFrame(top_frame)
            price_frame.pack(side="right")
            
            current_price = info.get('currentPrice', 0)
            previous_close = info.get('previousClose', 0)
            change = ((current_price - previous_close) / previous_close) * 100
            
            price_text = f"₺{current_price:,.2f}"
            change_text = f"(%{change:+.2f})"
            
            ctk.CTkLabel(price_frame, text=price_text,
                        font=("Segoe UI", 24, "bold")).pack(side="left", padx=5)
            
            change_color = "#2ecc71" if change > 0 else "#e74c3c"
            ctk.CTkLabel(price_frame, text=change_text,
                        font=("Segoe UI", 18, "bold"),
                        text_color=change_color).pack(side="left")
            
            controls_frame = ctk.CTkFrame(container)
            controls_frame.pack(fill="x", pady=(0, 10))
            
            ranges = [
                ("1 Ay", "1mo"),
                ("3 Ay", "3mo"),
                ("6 Ay", "6mo"),
                ("1 Yıl", "1y"),
                ("5 Yıl", "5y"),
                ("Tümü", "max")
            ]
            
            for text, value in ranges:
                ctk.CTkRadioButton(controls_frame, text=text, value=value,
                                 variable=self.selected_range,
                                 command=self.update_chart).pack(side="left", padx=10)
            
            chart_frame = ctk.CTkFrame(container)
            chart_frame.pack(fill="both", expand=True, pady=10)
            
            self.fig = Figure(figsize=(10, 6), facecolor='#2b2b2b')
            self.ax = self.fig.add_subplot(111)
            self.ax.set_facecolor('#2b2b2b')
            
            self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
            self.canvas.get_tk_widget().pack(fill="both", expand=True)
            
            details_frame = ctk.CTkFrame(container)
            details_frame.pack(fill="x", pady=20)
            
            left_details = ctk.CTkFrame(details_frame)
            left_details.pack(side="left", fill="both", expand=True, padx=(0, 10))
            
            basic_info = [
                ("Piyasa Değeri", info.get('marketCap', 0), "TL"),
                ("Günlük Hacim", info.get('volume', 0), "Lot"),
                ("F/K Oranı", info.get('trailingPE', 0), ""),
                ("Beta", info.get('beta', 0), ""),
                ("52H En Yüksek", info.get('fiftyTwoWeekHigh', 0), "TL"),
                ("52H En Düşük", info.get('fiftyTwoWeekLow', 0), "TL")
            ]
            
            for i, (label, value, unit) in enumerate(basic_info):
                row_frame = ctk.CTkFrame(left_details)
                row_frame.pack(fill="x", pady=2)
                
                ctk.CTkLabel(row_frame, text=f"{label}:",
                            font=("Segoe UI", 12)).pack(side="left")
                
                if isinstance(value, (int, float)):
                    if unit == "TL":
                        formatted_value = f"₺{value:,.2f}"
                    elif unit == "Lot":
                        formatted_value = f"{value:,.0f}"
                    else:
                        formatted_value = f"{value:.2f}"
                else:
                    formatted_value = str(value)
                
                if unit and unit not in formatted_value:
                    formatted_value = f"{formatted_value} {unit}"
                
                ctk.CTkLabel(row_frame, text=formatted_value,
                            font=("Segoe UI", 12, "bold")).pack(side="right")
            
            right_details = ctk.CTkFrame(details_frame)
            right_details.pack(side="right", fill="both", expand=True, padx=(10, 0))
            
            hist = self.stock.history(period="50d")
            
            if not hist.empty:
                sma20 = hist['Close'].rolling(window=20).mean().iloc[-1]
                sma50 = hist['Close'].rolling(window=50).mean().iloc[-1]
                rsi = self.calculate_rsi(hist['Close'])
                
                technical_info = [
                    ("20 Günlük Ortalama", sma20, "TL"),
                    ("50 Günlük Ortalama", sma50, "TL"),
                    ("RSI (14)", rsi, ""),
                    ("Günlük Değişim", change, "%"),
                    ("Açılış", info.get('open', 0), "TL"),
                    ("Kapanış", info.get('previousClose', 0), "TL")
                ]
                
                for i, (label, value, unit) in enumerate(technical_info):
                    row_frame = ctk.CTkFrame(right_details)
                    row_frame.pack(fill="x", pady=2)
                    
                    ctk.CTkLabel(row_frame, text=f"{label}:",
                                font=("Segoe UI", 12)).pack(side="left")
                    
                    if isinstance(value, (int, float)):
                        if unit == "TL":
                            formatted_value = f"₺{value:,.2f}"
                        elif unit == "%":
                            formatted_value = f"%{value:+.2f}"
                        else:
                            formatted_value = f"{value:.2f}"
                    else:
                        formatted_value = str(value)
                    
                    if unit and unit not in formatted_value and unit != "%":
                        formatted_value = f"{formatted_value} {unit}"
                    
                    ctk.CTkLabel(row_frame, text=formatted_value,
                                font=("Segoe UI", 12, "bold")).pack(side="right")
            
            self.update_chart()
        
        def calculate_rsi(self, prices, periods=14):
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi.iloc[-1]
        
        def update_chart(self):
            self.ax.clear()
            
            hist = self.stock.history(period=self.selected_range.get())
            
            if not hist.empty:
                self.ax.plot(hist.index, hist['Close'], color='#3498db', linewidth=2)
                
                if len(hist) >= 50:
                    ma20 = hist['Close'].rolling(window=20).mean()
                    ma50 = hist['Close'].rolling(window=50).mean()
                    self.ax.plot(hist.index, ma20, color='#2ecc71', linewidth=1,
                               linestyle='--', label='20 Günlük Ort.')
                    self.ax.plot(hist.index, ma50, color='#e74c3c', linewidth=1,
                               linestyle='--', label='50 Günlük Ort.')
                    self.ax.legend(facecolor='#2b2b2b', edgecolor='#2b2b2b',
                                 labelcolor='white')
                
                self.ax.set_facecolor('#2b2b2b')
                self.ax.set_title(f"{self.symbol} Hisse Fiyat Grafiği",
                                color='white', pad=20)
                self.ax.set_xlabel("Tarih", color='white')
                self.ax.set_ylabel("Fiyat (TL)", color='white')
                self.ax.grid(True, linestyle='--', alpha=0.3)
                self.ax.tick_params(colors='white')
                
                self.fig.tight_layout()
                self.canvas.draw()

    class CompareStocksWindow(ctk.CTkToplevel):
        def __init__(self, symbol1=None, symbol2=None):
            super().__init__()
            self.title("Hisse Karşılaştırma")
            self.geometry("1200x800")
            
            self.symbol1 = symbol1
            self.symbol2 = symbol2
            self.stock1 = None
            self.stock2 = None
            
            self.available_stocks = [
                'AKBNK', 'ARCLK', 'ASELS', 'BIMAS', 'EKGYO', 
                'EREGL', 'GARAN', 'HEKTS', 'ISCTR', 'KCHOL',
                'KOZAA', 'KOZAL', 'KRDMD', 'PETKM', 'PGSUS',
                'SAHOL', 'SASA', 'SISE', 'TAVHL', 'TCELL',
                'THYAO', 'TOASO', 'TUPRS', 'VAKBN', 'YKBNK'
            ]
            
            self.selected_range = ctk.StringVar(value="1y")
            
            self.stock1_var = ctk.StringVar(value=symbol1 if symbol1 else "")
            self.stock2_var = ctk.StringVar(value=symbol2 if symbol2 else "")
            
            self.search1_var = ctk.StringVar()
            self.search2_var = ctk.StringVar()
            
            self.filtered_stocks1 = []
            self.filtered_stocks2 = []
            
            self.create_widgets()
            
            if symbol1 and symbol2:
                self.load_stocks()
        
        def create_widgets(self):
            container = ctk.CTkFrame(self)
            container.pack(fill="both", expand=True, padx=20, pady=20)
            
            top_frame = ctk.CTkFrame(container)
            top_frame.pack(fill="x", pady=(0, 20))
            
            stock1_frame = ctk.CTkFrame(top_frame)
            stock1_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
            
            ctk.CTkLabel(stock1_frame, text="1. Hisse:",
                        font=("Segoe UI", 12)).pack(side="left", padx=5)
            
            self.search1_entry = ctk.CTkEntry(stock1_frame, 
                                            textvariable=self.search1_var,
                                            width=120,
                                            placeholder_text="Hisse Ara...")
            self.search1_entry.pack(side="left", padx=5)
            
            self.selected1_label = ctk.CTkLabel(stock1_frame, 
                                              textvariable=self.stock1_var,
                                              font=("Segoe UI", 12, "bold"))
            self.selected1_label.pack(side="left", padx=10)
            
            self.stocks1_frame = ctk.CTkFrame(stock1_frame)
            self.stocks1_frame.pack(side="left", padx=5)
            
            stock2_frame = ctk.CTkFrame(top_frame)
            stock2_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))
            
            ctk.CTkLabel(stock2_frame, text="2. Hisse:",
                        font=("Segoe UI", 12)).pack(side="left", padx=5)
            
            self.search2_entry = ctk.CTkEntry(stock2_frame, 
                                            textvariable=self.search2_var,
                                            width=120,
                                            placeholder_text="Hisse Ara...")
            self.search2_entry.pack(side="left", padx=5)
            
            self.selected2_label = ctk.CTkLabel(stock2_frame, 
                                              textvariable=self.stock2_var,
                                              font=("Segoe UI", 12, "bold"))
            self.selected2_label.pack(side="left", padx=10)
            
            self.stocks2_frame = ctk.CTkFrame(stock2_frame)
            self.stocks2_frame.pack(side="left", padx=5)
            
            ctk.CTkButton(top_frame, text="Karşılaştır",
                         command=self.load_stocks).pack(side="right", padx=20)
            
            self.search1_var.trace_add("write", lambda *args: self.filter_stocks(1))
            self.search2_var.trace_add("write", lambda *args: self.filter_stocks(2))
            
            controls_frame = ctk.CTkFrame(container)
            controls_frame.pack(fill="x", pady=(0, 10))
            
            ranges = [
                ("1 Ay", "1mo"),
                ("3 Ay", "3mo"),
                ("6 Ay", "6mo"),
                ("1 Yıl", "1y"),
                ("5 Yıl", "5y"),
                ("Tümü", "max")
            ]
            
            for text, value in ranges:
                ctk.CTkRadioButton(controls_frame, text=text, value=value,
                                 variable=self.selected_range,
                                 command=self.update_charts).pack(side="left", padx=10)
            
            content_frame = ctk.CTkFrame(container)
            content_frame.pack(fill="both", expand=True)
            
            self.left_frame = ctk.CTkFrame(content_frame)
            self.left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
            
            self.right_frame = ctk.CTkFrame(content_frame)
            self.right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        def filter_stocks(self, search_box):
            search_var = self.search1_var if search_box == 1 else self.search2_var
            stocks_frame = self.stocks1_frame if search_box == 1 else self.stocks2_frame
            stock_var = self.stock1_var if search_box == 1 else self.stock2_var
            
            for widget in stocks_frame.winfo_children():
                widget.destroy()
            
            search_term = search_var.get().upper()
            if not search_term:
                return
            
            filtered = [stock for stock in self.available_stocks 
                       if search_term in stock]
            
            for stock in filtered[:5]:
                btn = ctk.CTkButton(stocks_frame, text=stock,
                                  width=70, height=25,
                                  command=lambda s=stock: self.select_stock(s, search_box))
                btn.pack(pady=2)
        
        def select_stock(self, symbol, search_box):
            if search_box == 1:
                self.stock1_var.set(symbol)
                self.search1_var.set("")
                for widget in self.stocks1_frame.winfo_children():
                    widget.destroy()
            else:
                self.stock2_var.set(symbol)
                self.search2_var.set("")
                for widget in self.stocks2_frame.winfo_children():
                    widget.destroy()
            
            if self.stock1_var.get() and self.stock2_var.get():
                self.load_stocks()
        
        def load_stocks(self):
            symbol1 = self.stock1_var.get()
            symbol2 = self.stock2_var.get()
            
            if not symbol1 or not symbol2:
                return
            
            try:
                self.symbol1 = symbol1
                self.symbol2 = symbol2
                self.stock1 = yf.Ticker(f"{symbol1}.IS")
                self.stock2 = yf.Ticker(f"{symbol2}.IS")
                
                self.update_charts()
                self.update_details()
                
            except Exception as e:
                print(f"Hata: {str(e)}")
                traceback.print_exc()
        
        def update_charts(self):
            try:
                for widget in self.left_frame.winfo_children():
                    widget.destroy()
                for widget in self.right_frame.winfo_children():
                    widget.destroy()
                
                fig1 = Figure(figsize=(6, 4), facecolor='#2b2b2b')
                ax1 = fig1.add_subplot(111)
                ax1.set_facecolor('#2b2b2b')
                
                hist1 = self.stock1.history(period=self.selected_range.get())
                if not hist1.empty:
                    normalized1 = hist1['Close'] / hist1['Close'].iloc[0] * 100
                    ax1.plot(hist1.index, normalized1, color='#3498db', linewidth=2,
                            label=self.symbol1)
                    
                    ax1.set_facecolor('#2b2b2b')
                    ax1.set_title(f"{self.symbol1} Fiyat Grafiği (Normalize)",
                                color='white', pad=20)
                    ax1.set_xlabel("Tarih", color='white')
                    ax1.set_ylabel("Normalize Fiyat (%)", color='white')
                    ax1.grid(True, linestyle='--', alpha=0.3)
                    ax1.tick_params(colors='white')
                    ax1.legend(facecolor='#2b2b2b', edgecolor='#2b2b2b',
                             labelcolor='white')
                
                canvas1 = FigureCanvasTkAgg(fig1, master=self.left_frame)
                canvas1.draw()
                canvas1.get_tk_widget().pack(fill="both", expand=True)
                
                fig2 = Figure(figsize=(6, 4), facecolor='#2b2b2b')
                ax2 = fig2.add_subplot(111)
                ax2.set_facecolor('#2b2b2b')
                
                hist2 = self.stock2.history(period=self.selected_range.get())
                if not hist2.empty:
                    normalized2 = hist2['Close'] / hist2['Close'].iloc[0] * 100
                    ax2.plot(hist2.index, normalized2, color='#e74c3c', linewidth=2,
                            label=self.symbol2)
                    
                    ax2.plot(hist1.index, normalized1, color='#3498db', linewidth=2,
                            label=self.symbol1)
                    
                    ax2.set_facecolor('#2b2b2b')
                    ax2.set_title("Karşılaştırmalı Grafik (Normalize)",
                                color='white', pad=20)
                    ax2.set_xlabel("Tarih", color='white')
                    ax2.set_ylabel("Normalize Fiyat (%)", color='white')
                    ax2.grid(True, linestyle='--', alpha=0.3)
                    ax2.tick_params(colors='white')
                    ax2.legend(facecolor='#2b2b2b', edgecolor='#2b2b2b',
                             labelcolor='white')
                
                canvas2 = FigureCanvasTkAgg(fig2, master=self.right_frame)
                canvas2.draw()
                canvas2.get_tk_widget().pack(fill="both", expand=True)
                
                self.update_details()
                
            except Exception as e:
                print(f"Grafik güncelleme hatası: {str(e)}")
                traceback.print_exc()
        
        def update_details(self):
            try:
                details_frame1 = ctk.CTkFrame(self.left_frame)
                details_frame1.pack(fill="x", pady=10, side="bottom")
                
                info1 = self.stock1.info
                self.create_info_table(details_frame1, info1, self.symbol1)
                
                details_frame2 = ctk.CTkFrame(self.right_frame)
                details_frame2.pack(fill="x", pady=10, side="bottom")
                
                info2 = self.stock2.info
                self.create_info_table(details_frame2, info2, self.symbol2)
                
            except Exception as e:
                print(f"Detay güncelleme hatası: {str(e)}")
                traceback.print_exc()
        
        def create_info_table(self, parent, info, symbol):
            ctk.CTkLabel(parent, text=f"{symbol} Detayları",
                        font=("Segoe UI", 16, "bold")).pack(pady=5)
            
            metrics = [
                ("Fiyat", 'currentPrice', "₺"),
                ("Değişim", 'regularMarketChangePercent', "%"),
                ("Hacim", 'volume', ""),
                ("Piyasa Değeri", 'marketCap', "₺"),
                ("F/K", 'trailingPE', ""),
                ("52H En Yüksek", 'fiftyTwoWeekHigh', "₺"),
                ("52H En Düşük", 'fiftyTwoWeekLow', "₺")
            ]
            
            for label, key, unit in metrics:
                row = ctk.CTkFrame(parent)
                row.pack(fill="x", padx=10, pady=2)
                
                ctk.CTkLabel(row, text=f"{label}:",
                            font=("Segoe UI", 12)).pack(side="left")
                
                value = info.get(key, 0)
                if isinstance(value, (int, float)):
                    if unit == "₺":
                        formatted = f"₺{value:,.2f}"
                    elif unit == "%":
                        formatted = f"%{value:+.2f}"
                    else:
                        formatted = f"{value:,.2f}"
                else:
                    formatted = str(value)
                
                if unit and unit not in formatted and unit != "%":
                    formatted = f"{formatted} {unit}"
                
                ctk.CTkLabel(row, text=formatted,
                            font=("Segoe UI", 12, "bold")).pack(side="right")

    class ModernBistApp(ctk.CTk):
        def __init__(self):
            super().__init__()
            print("Ana uygulama başlatılıyor...")
            
            self.title("BIST Piyasa Takip")
            self.geometry("1200x800")
            
            self.cached_data = []
            self.last_update = None
            self.update_interval = 30
            self.is_updating = False
            
            self.analysis_window = None
            
            self.bist_tickers = [
                'AKBNK.IS', 'ARCLK.IS', 'ASELS.IS', 'BIMAS.IS', 'EKGYO.IS', 
                'EREGL.IS', 'GARAN.IS', 'HEKTS.IS', 'ISCTR.IS', 'KCHOL.IS',
                'KOZAA.IS', 'KOZAL.IS', 'KRDMD.IS', 'PETKM.IS', 'PGSUS.IS',
                'SAHOL.IS', 'SASA.IS', 'SISE.IS', 'TAVHL.IS', 'TCELL.IS',
                'THYAO.IS', 'TOASO.IS', 'TUPRS.IS', 'VAKBN.IS', 'YKBNK.IS'
            ]
            
            self.ticker_groups = [self.bist_tickers[i:i+5] for i in range(0, len(self.bist_tickers), 5)]
            
            print("Widget'lar oluşturuluyor...")
            self.create_widgets()
            print("Veriler güncelleniyor...")
            self.update_data()
            
            self.after(1000, self.check_update)
            print("Uygulama hazır!")

        def check_update(self):
            """Periyodik güncelleme kontrolü"""
            if not self.is_updating and (
                self.last_update is None or 
                (datetime.now() - self.last_update).seconds >= self.update_interval
            ):
                self.update_data()
            self.after(1000, self.check_update)

        def update_data(self):
            if self.is_updating:
                return
            
            self.is_updating = True
            self.status_var.set("Veriler güncelleniyor...")
            self.update()
            
            try:
                all_data = []
                
                for group in self.ticker_groups:
                    try:
                        group_data = self.fetch_group_data(group)
                        all_data.extend(group_data)
                    except Exception as e:
                        print(f"Grup hatası: {str(e)}")
                        continue
                
                if all_data:
                    all_data.sort(key=lambda x: x['change'], reverse=True)
                    self.cached_data = all_data
                    self.last_update = datetime.now()
                    
                    self.update_ui(all_data)
                    
                    self.status_var.set(f"Son Güncelleme: {self.last_update.strftime('%H:%M:%S')}")
                else:
                    self.status_var.set("Güncelleme başarısız!")
                
            except Exception as e:
                print(f"Genel hata: {str(e)}")
                self.status_var.set("Güncelleme başarısız!")
            
            finally:
                self.is_updating = False

        def fetch_group_data(self, tickers):
            """Bir grup hissenin verilerini çeker"""
            group_data = []
            for ticker in tickers:
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.fast_info 
                    current_price = info.last_price
                    previous_close = info.previous_close
                    
                    if current_price and previous_close:
                        change = ((current_price - previous_close) / previous_close) * 100
                        group_data.append({
                            'symbol': ticker.replace('.IS', ''),
                            'price': current_price,
                            'change': round(change, 2),
                            'volume': info.last_volume,
                            'bid': current_price * 0.999,
                            'ask': current_price * 1.001
                        })
                except Exception as e:
                    print(f"Hata ({ticker}): {str(e)}")
                    continue
            return group_data

        def update_ui(self, data):
            """Tüm arayüz güncellemelerini yap"""
            self.update_market_table(data)
            
            for i, stock in enumerate(data[:10]):
                row = [
                    stock['symbol'],
                    f"{stock['price']:.2f}",
                    f"{stock['change']}%"
                ]
                for j, value in enumerate(row):
                    self.gainers_tree.set(i, j, value)
            
            for i, stock in enumerate(data[-10:]):
                row = [
                    stock['symbol'],
                    f"{stock['price']:.2f}",
                    f"{stock['change']}%"
                ]
                for j, value in enumerate(row):
                    self.losers_tree.set(i, j, value)

        def create_widgets(self):
            container = ctk.CTkFrame(self)
            container.pack(fill="both", expand=True, padx=20, pady=20)
            
            header_frame = ctk.CTkFrame(container)
            header_frame.pack(fill="x", pady=(0, 20))
            
            ctk.CTkLabel(header_frame, text="BIST Piyasa Takip",
                        font=("Segoe UI", 24, "bold")).pack(side="left")
            
            ctk.CTkButton(header_frame, text="Hisse Karşılaştır",
                         command=self.show_compare_window).pack(side="left", padx=20)
            
            search_frame = ctk.CTkFrame(header_frame)
            search_frame.pack(side="right", pady=10)
            
            self.search_var = ctk.StringVar()
            self.search_var.trace_add("write", self.filter_market_data)
            
            search_entry = ctk.CTkEntry(search_frame, textvariable=self.search_var,
                                      width=200, placeholder_text="Hisse Ara...")
            search_entry.pack(side="left", padx=5)
            
            self.status_var = ctk.StringVar()
            ctk.CTkLabel(header_frame, textvariable=self.status_var,
                        font=("Segoe UI", 10)).pack(side="right", padx=20)
            
            content_frame = ctk.CTkFrame(container)
            content_frame.pack(fill="both", expand=True)
            
            left_frame = ctk.CTkFrame(content_frame)
            left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
            
            ctk.CTkLabel(left_frame, text="Tüm Piyasa",
                        font=("Segoe UI", 16, "bold")).pack(pady=(0, 10))
            
            table_frame = ctk.CTkFrame(left_frame)
            table_frame.pack(fill="both", expand=True)
            
            columns = ('Hisse', 'Son', 'Değişim %', 'Hacim', 'Alış', 'Satış')
            self.market_tree = CustomTable(table_frame, rows=25, columns=6,
                                         headers=columns,
                                         on_row_click=self.on_market_row_click)
            self.market_tree.pack(fill="both", expand=True)
            
            right_frame = ctk.CTkFrame(content_frame)
            right_frame.pack(side="right", fill="both", padx=(10, 0))
            
            ctk.CTkLabel(right_frame, text="En Çok Yükselenler",
                        font=("Segoe UI", 16, "bold")).pack(pady=(0, 10))
            
            gainers_columns = ('Hisse', 'Son', 'Değişim %')
            self.gainers_tree = CustomTable(right_frame, rows=10, columns=3,
                                          headers=gainers_columns,
                                          on_row_click=self.on_gainer_row_click)
            self.gainers_tree.pack(fill="x", pady=(0, 20))
            
            ctk.CTkLabel(right_frame, text="En Çok Düşenler",
                        font=("Segoe UI", 16, "bold")).pack(pady=(0, 10))
            
            self.losers_tree = CustomTable(right_frame, rows=10, columns=3,
                                         headers=gainers_columns,
                                         on_row_click=self.on_loser_row_click)
            self.losers_tree.pack(fill="x")
            
            ctk.CTkButton(container, text="Verileri Yenile",
                         command=self.update_data).pack(pady=20)

        def filter_market_data(self, *args):
            search_term = self.search_var.get().upper()
            
            for i in range(25):
                for j in range(6):
                    self.market_tree.set(i, j, "")
            
            filtered_data = [
                stock for stock in self.cached_data
                if not search_term or search_term in stock['symbol']
            ]
            
            self.update_market_table(filtered_data)
        
        def update_market_table(self, data):
            for i, stock in enumerate(data):
                if i < 25: 
                    row = [
                        stock['symbol'],
                        f"{stock['price']:.2f}",
                        f"{stock['change']}%",
                        f"{stock['volume']:,.0f}",
                        f"{stock['bid']:.2f}",
                        f"{stock['ask']:.2f}"
                    ]
                    for j, value in enumerate(row):
                        self.market_tree.set(i, j, value)
        
        def show_stock_analysis(self, symbol):
            if self.analysis_window is not None:
                self.analysis_window.destroy()
            
            self.analysis_window = StockAnalysisWindow(symbol)
            
            self.analysis_window.protocol("WM_DELETE_WINDOW", self.on_analysis_window_close)
        
        def on_analysis_window_close(self):
            if self.analysis_window is not None:
                self.analysis_window.destroy()
                self.analysis_window = None
        
        def on_market_row_click(self, row):
            if row < len(self.cached_data):
                symbol = self.cached_data[row]['symbol']
                self.show_stock_analysis(symbol)
        
        def on_gainer_row_click(self, row):
            if self.cached_data and row < 10:
                symbol = self.cached_data[row]['symbol']
                self.show_stock_analysis(symbol)
        
        def on_loser_row_click(self, row):
            if self.cached_data and row < 10:
                symbol = self.cached_data[-(row+1)]['symbol']
                self.show_stock_analysis(symbol)

        def show_compare_window(self):
            compare_window = CompareStocksWindow()
            compare_window.focus()

    print("Uygulama başlatılıyor...")
    app = ModernBistApp()
    print("Ana döngü başlıyor...")
    app.mainloop()
    print("Uygulama kapandı.")
    
except Exception as e:
    print("\nBir hata oluştu:")
    print(str(e))
    print("\nDetaylı hata mesajı:")
    traceback.print_exc()
    input("\nProgramı kapatmak için Enter'a basın...") 
