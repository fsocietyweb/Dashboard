import tkinter as tk
import customtkinter as ctk
import requests
import threading
import time
import random
import platform
import psutil
import webbrowser

# Force strict dark mode configuration
ctk.set_appearance_mode("dark")

class IntegratedUtilityApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Frame configuration
        self.title("Dashboard.py")
        self.geometry("980x660")
        self.resizable(False, False)
        
        # Super Black Window Background Override
        self.configure(fg_color="#000000")

        # 1x2 Core Layout Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------- SYSTEM COLOR PALETTE (MONOCHROME) ----------------
        self.bg_super_black = "#000000"
        self.bg_dark_grey   = "#121212"
        self.bg_card_grey   = "#1C1C1C"
        self.accent_white   = "#FFFFFF"
        self.text_muted     = "#888888"
        self.btn_grey       = "#2A2A2A"
        self.btn_hover      = "#404040"

        # ---------------- SIDEBAR NAVIGATION ----------------
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=self.bg_dark_grey)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Row 5 will act as a flexible spacer pushing everything below it to the bottom
        self.sidebar.grid_rowconfigure(5, weight=1)

        self.side_title = ctk.CTkLabel(
            self.sidebar, text="Dashboard", text_color=self.accent_white, font=ctk.CTkFont(size=18, weight="bold")
        )
        self.side_title.grid(row=0, column=0, padx=20, pady=25)

        # Main Navigation Controls (Top half)
        self.btn_home_view = ctk.CTkButton(
            self.sidebar, text="Home", text_color=self.accent_white,
            fg_color="transparent", hover_color=self.btn_hover, command=self.show_home_page
        )
        self.btn_home_view.grid(row=1, column=0, padx=15, pady=8, sticky="ew")

        self.btn_weather_view = ctk.CTkButton(
            self.sidebar, text="Weather & IP Lookup", text_color=self.accent_white,
            fg_color="transparent", hover_color=self.btn_hover, command=self.show_weather_page
        )
        self.btn_weather_view.grid(row=2, column=0, padx=15, pady=8, sticky="ew")

        self.btn_webhook_view = ctk.CTkButton(
            self.sidebar, text="Webhook Sender", text_color=self.accent_white,
            fg_color="transparent", hover_color=self.btn_hover, command=self.show_webhook_page
        )
        self.btn_webhook_view.grid(row=3, column=0, padx=15, pady=8, sticky="ew")

        self.btn_diag_view = ctk.CTkButton(
            self.sidebar, text="System Diagnostics", text_color=self.accent_white,
            fg_color="transparent", hover_color=self.btn_hover, command=self.show_diag_page
        )
        self.btn_diag_view.grid(row=4, column=0, padx=15, pady=8, sticky="ew")

        # Bottom Navigation Controls (Pushed down by Row 5 spacer)
        self.btn_about_view = ctk.CTkButton(
            self.sidebar, text="About App", text_color=self.accent_white,
            fg_color="transparent", hover_color=self.btn_hover, command=self.show_about_page
        )
        self.btn_about_view.grid(row=6, column=0, padx=15, pady=8, sticky="ew")

        self.btn_github_view = ctk.CTkButton(
            self.sidebar, 
            text="GitHub", 
            text_color=self.accent_white,
            fg_color="transparent", 
            hover_color=self.btn_hover, 
            command=lambda: webbrowser.open("https://github.com/fsocietyweb")
        )
        self.btn_github_view.grid(row=7, column=0, padx=15, pady=8, sticky="ew")

        self.version_lbl = ctk.CTkLabel(
            self.sidebar, text="v1.8.0 (Stable)", text_color=self.text_muted, font=ctk.CTkFont(size=11)
        )
        self.version_lbl.grid(row=8, column=0, padx=20, pady=15)

        # ---------------- PAGE FRAME CONTAINERS ----------------
        self.home_frame    = ctk.CTkFrame(self, corner_radius=0, fg_color=self.bg_super_black)
        self.weather_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=self.bg_super_black)
        self.webhook_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=self.bg_super_black)
        self.diag_frame    = ctk.CTkFrame(self, corner_radius=0, fg_color=self.bg_super_black)
        self.about_frame   = ctk.CTkFrame(self, corner_radius=0, fg_color=self.bg_super_black)

        # Initialize visual components
        self.setup_home_ui()
        self.setup_weather_ui()
        self.setup_webhook_ui()
        self.setup_diag_ui()
        self.setup_about_ui()

        # Default to showing the Home page on launch
        self.show_home_page()

    # ---------------- VIEW CONTROLLER LOGIC ----------------
    def reset_nav_highlights(self):
        self.btn_home_view.configure(fg_color="transparent")
        self.btn_weather_view.configure(fg_color="transparent")
        self.btn_webhook_view.configure(fg_color="transparent")
        self.btn_diag_view.configure(fg_color="transparent")
        self.btn_about_view.configure(fg_color="transparent")

    def show_home_page(self):
        self.weather_frame.grid_forget()
        self.webhook_frame.grid_forget()
        self.diag_frame.grid_forget()
        self.about_frame.grid_forget()
        self.home_frame.grid(row=0, column=1, padx=25, pady=25, sticky="nsew")
        self.reset_nav_highlights()
        self.btn_home_view.configure(fg_color=self.btn_grey)

    def show_weather_page(self):
        self.home_frame.grid_forget()
        self.webhook_frame.grid_forget()
        self.diag_frame.grid_forget()
        self.about_frame.grid_forget()
        self.weather_frame.grid(row=0, column=1, padx=25, pady=25, sticky="nsew")
        self.reset_nav_highlights()
        self.btn_weather_view.configure(fg_color=self.btn_grey)

    def show_webhook_page(self):
        self.home_frame.grid_forget()
        self.weather_frame.grid_forget()
        self.diag_frame.grid_forget()
        self.about_frame.grid_forget()
        self.webhook_frame.grid(row=0, column=1, padx=25, pady=25, sticky="nsew")
        self.reset_nav_highlights()
        self.btn_webhook_view.configure(fg_color=self.btn_grey)

    def show_diag_page(self):
        self.home_frame.grid_forget()
        self.weather_frame.grid_forget()
        self.webhook_frame.grid_forget()
        self.about_frame.grid_forget()
        self.diag_frame.grid(row=0, column=1, padx=25, pady=25, sticky="nsew")
        self.reset_nav_highlights()
        self.btn_diag_view.configure(fg_color=self.btn_grey)
        self.trigger_diag_refresh()

    def show_about_page(self):
        self.home_frame.grid_forget()
        self.weather_frame.grid_forget()
        self.webhook_frame.grid_forget()
        self.diag_frame.grid_forget()
        self.about_frame.grid(row=0, column=1, padx=25, pady=25, sticky="nsew")
        self.reset_nav_highlights()
        self.btn_about_view.configure(fg_color=self.btn_grey)

    # ---------------- HOME VIEW SETUP ----------------
    def setup_home_ui(self):
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_header_frame = ctk.CTkFrame(self.home_frame, fg_color="transparent")
        self.home_header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        self.home_header_frame.grid_columnconfigure(0, weight=1)

        self.home_title = ctk.CTkLabel(self.home_header_frame, text="Home Workspace", text_color=self.accent_white, font=ctk.CTkFont(size=20, weight="bold"))
        self.home_title.grid(row=0, column=0, sticky="w")

        # Static Information Card Banner Layout
        self.home_card = ctk.CTkFrame(self.home_frame, fg_color=self.bg_card_grey, corner_radius=6)
        self.home_card.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        # CLEANER & MORE DETAILED DESCRIPTION:
        static_content = (
            "Welcome to the Central Administration Dashboard\n\n"
            "This workspace serves as an integrated control terminal containing multi-threaded operations "
            "and active diagnostic tracking tools. Use the sidebar navigation menu to seamlessly toggle "
            "between different engine modules.\n\n"
            "Available Utility Pipelines:\n"
            " • Network & Weather Engine: Trace geographic network locations and real-time environment metrics. IMPORTANT Its Scanning The Weather with Your IP so if you use a VPN you see the VPN's IP Location\n"
            " • Webhook Sender: Dispatch bulk HTTP API data streams complete with built-in rate limit mitigation protocols.\n"
            " • Hardware Diagnostics: Query processes, live CPU utilization, and available memory logs instantly."
        )

        self.lbl_static_text = ctk.CTkLabel(
            self.home_card, text=static_content, text_color=self.accent_white, 
            font=ctk.CTkFont(size=13), justify="left", wraplength=660
        )
        self.lbl_static_text.pack(anchor="w", padx=25, pady=25)

    # ---------------- WEATHER VIEW SETUP ----------------
    def setup_weather_ui(self):
        self.weather_frame.grid_columnconfigure(0, weight=1)
        self.weather_frame.grid_columnconfigure(1, weight=1)

        self.w_title = ctk.CTkLabel(self.weather_frame, text="Network Location & Weather Insights", text_color=self.accent_white, font=ctk.CTkFont(size=20, weight="bold"))
        self.w_title.grid(row=0, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w")

        self.btn_fetch_data = ctk.CTkButton(
            self.weather_frame, text="Analyze Environment Profiles", text_color=self.accent_white,
            fg_color=self.btn_grey, hover_color=self.btn_hover, command=self.run_weather_thread
        )
        self.btn_fetch_data.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.info_box = ctk.CTkFrame(self.weather_frame, fg_color="transparent")
        self.info_box.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        
        self.ip_display_lbl = ctk.CTkLabel(self.info_box, text="Detected Host IP: Unknown", text_color=self.accent_white, font=ctk.CTkFont(size=14, weight="bold"))
        self.ip_display_lbl.pack(anchor="w", pady=1)
        
        self.loc_display_lbl = ctk.CTkLabel(self.info_box, text="Geographic Location: Pending parsing...", font=ctk.CTkFont(size=13), text_color=self.text_muted)
        self.loc_display_lbl.pack(anchor="w", pady=1)

        self.weather_tabs = ctk.CTkTabview(self.weather_frame, fg_color="transparent", segmented_button_selected_color=self.btn_grey, segmented_button_unselected_hover_color=self.btn_hover)
        self.weather_tabs.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.weather_frame.grid_rowconfigure(3, weight=1)

        tab_grid = self.weather_tabs.add("Standard Metrics")
        tab_ascii = self.weather_tabs.add("ASCII Structured Overview")

        tab_grid.grid_columnconfigure((0, 1), weight=1)
        tab_grid.grid_rowconfigure((0, 1), weight=1)

        self.temp_card = ctk.CTkFrame(tab_grid, fg_color=self.bg_card_grey, corner_radius=6)
        self.temp_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.temp_card, text="Temperature", text_color=self.text_muted).pack(pady=(12, 0))
        self.temp_val = ctk.CTkLabel(self.temp_card, text="-- °C", text_color=self.accent_white, font=ctk.CTkFont(size=24, weight="bold"))
        self.temp_val.pack(pady=(4, 12))

        self.cond_card = ctk.CTkFrame(tab_grid, fg_color=self.bg_card_grey, corner_radius=6)
        self.cond_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.cond_card, text="Condition Profile", text_color=self.text_muted).pack(pady=(12, 0))
        self.cond_val = ctk.CTkLabel(self.cond_card, text="--", text_color=self.accent_white, font=ctk.CTkFont(size=18, weight="bold"))
        self.cond_val.pack(pady=(6, 12))

        self.wind_card = ctk.CTkFrame(tab_grid, fg_color=self.bg_card_grey, corner_radius=6)
        self.wind_card.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.wind_card, text="Wind Velocity", text_color=self.text_muted).pack(pady=(12, 0))
        self.wind_val = ctk.CTkLabel(self.wind_card, text="-- km/h", text_color=self.accent_white, font=ctk.CTkFont(size=18, weight="bold"))
        self.wind_val.pack(pady=(6, 12))

        self.humid_card = ctk.CTkFrame(tab_grid, fg_color=self.bg_card_grey, corner_radius=6)
        self.humid_card.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(self.humid_card, text="Relative Humidity", text_color=self.text_muted).pack(pady=(12, 0))
        self.humid_val = ctk.CTkLabel(self.humid_card, text="-- %", text_color=self.accent_white, font=ctk.CTkFont(size=18, weight="bold"))
        self.humid_val.pack(pady=(6, 12))

        tab_ascii.grid_columnconfigure(0, weight=1)
        tab_ascii.grid_rowconfigure(0, weight=1)
        self.ascii_text_box = ctk.CTkTextbox(tab_ascii, fg_color=self.bg_dark_grey, border_color=self.btn_grey, text_color=self.accent_white, font=("Courier New", 11))
        self.ascii_text_box.grid(row=0, column=0, sticky="nsew")
        self.ascii_text_box.insert("0.0", "Execute environment profiling tracking routine to generate raw canvas logs.")
        self.ascii_text_box.configure(state="disabled")

    # ---------------- WEBHOOK SENDER VIEW SETUP ----------------
    def setup_webhook_ui(self):
        self.webhook_frame.grid_columnconfigure((0, 1), weight=1)

        self.wh_title = ctk.CTkLabel(self.webhook_frame, text="Webhook Alert Sender Channel", text_color=self.accent_white, font=ctk.CTkFont(size=20, weight="bold"))
        self.wh_title.grid(row=0, column=0, columnspan=2, padx=10, pady=(0, 15), sticky="w")

        self.url_entry = ctk.CTkEntry(self.webhook_frame, placeholder_text="Enter Active Webhook API Target URL Connection Address...", fg_color=self.bg_card_grey, border_color=self.btn_grey, text_color=self.accent_white)
        self.url_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=6, sticky="ew")

        self.msg_entry = ctk.CTkEntry(self.webhook_frame, placeholder_text="Enter clear text transmission body payload content here...", fg_color=self.bg_card_grey, border_color=self.btn_grey, text_color=self.accent_white)
        self.msg_entry.grid(row=2, column=0, columnspan=2, padx=10, pady=6, sticky="ew")

        self.lbl_count = ctk.CTkLabel(self.webhook_frame, text="Transmission Limit Count:", text_color=self.text_muted)
        self.lbl_count.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        
        self.count_spinner = ctk.CTkEntry(self.webhook_frame, width=120, fg_color=self.bg_card_grey, border_color=self.btn_grey, text_color=self.accent_white)
        self.count_spinner.grid(row=3, column=0, padx=(180, 10), pady=5, sticky="w")
        self.count_spinner.insert(0, "1")

        self.btn_send_wh = ctk.CTkButton(
            self.webhook_frame, text="Execute Remote Data Dispatch", text_color=self.accent_white,
            fg_color=self.btn_grey, hover_color=self.btn_hover, command=self.run_webhook_thread
        )
        self.btn_send_wh.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.console_lbl = ctk.CTkLabel(self.webhook_frame, text="Execution Tracking Log Stream:", text_color=self.text_muted)
        self.console_lbl.grid(row=5, column=0, columnspan=2, padx=10, pady=(5, 2), sticky="w")

        self.console_log = ctk.CTkTextbox(self.webhook_frame, height=240, fg_color=self.bg_dark_grey, border_color=self.btn_grey, text_color=self.accent_white, font=("Courier New", 12))
        self.console_log.grid(row=6, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="ew")
        self.console_log.configure(state="disabled")

    # ---------------- SYSTEM DIAGNOSTICS VIEW SETUP ----------------
    def setup_diag_ui(self):
        self.diag_frame.grid_columnconfigure((0, 1), weight=1)

        self.diag_title = ctk.CTkLabel(self.diag_frame, text="Local Hardware Monitor Profiles", text_color=self.accent_white, font=ctk.CTkFont(size=20, weight="bold"))
        self.diag_title.grid(row=0, column=0, columnspan=2, padx=10, pady=(0, 15), sticky="w")

        self.diag_panel = ctk.CTkFrame(self.diag_frame, fg_color=self.bg_card_grey, corner_radius=6)
        self.diag_panel.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.lbl_os = ctk.CTkLabel(self.diag_panel, text="Operating System: Checking...", text_color=self.accent_white, font=ctk.CTkFont(size=13))
        self.lbl_os.pack(anchor="w", padx=20, pady=(15, 6))

        self.lbl_cpu = ctk.CTkLabel(self.diag_panel, text="Processor Architecture: Checking...", text_color=self.accent_white, font=ctk.CTkFont(size=13))
        self.lbl_cpu.pack(anchor="w", padx=20, pady=6)

        self.lbl_ram = ctk.CTkLabel(self.diag_panel, text="Available Memory Matrix: Checking...", text_color=self.accent_white, font=ctk.CTkFont(size=13))
        self.lbl_ram.pack(anchor="w", padx=20, pady=6)

        self.lbl_latency = ctk.CTkLabel(self.diag_panel, text="Network Cloud Gateway Latency: Measuring...", text_color=self.accent_white, font=ctk.CTkFont(size=13))
        self.lbl_latency.pack(anchor="w", padx=20, pady=(6, 15))

        self.proc_lbl = ctk.CTkLabel(self.diag_frame, text="Top Resource Consuming Active Tasks (CPU/RAM Loading):", text_color=self.text_muted)
        self.proc_lbl.grid(row=2, column=0, columnspan=2, padx=10, pady=(10, 2), sticky="w")

        self.proc_box = ctk.CTkTextbox(self.diag_frame, height=180, fg_color=self.bg_dark_grey, border_color=self.btn_grey, text_color=self.accent_white, font=("Courier New", 12))
        self.proc_box.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.proc_box.configure(state="disabled")

        self.btn_refresh_diag = ctk.CTkButton(
            self.diag_frame, text="Re-Scan Host Infrastructure Profiles", text_color=self.accent_white,
            fg_color=self.btn_grey, hover_color=self.btn_hover, command=self.trigger_diag_refresh
        )
        self.btn_refresh_diag.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    # ---------------- ABOUT VIEW SETUP ----------------
    def setup_about_ui(self):
        self.about_frame.grid_columnconfigure(0, weight=1)

        self.about_title = ctk.CTkLabel(self.about_frame, text="About This Software Bundle", text_color=self.accent_white, font=ctk.CTkFont(size=20, weight="bold"))
        self.about_title.grid(row=0, column=0, padx=10, pady=(0, 20), sticky="w")

        # Decorative Monochrome Information Card Banner Layout
        self.about_card = ctk.CTkFrame(self.about_frame, fg_color=self.bg_card_grey, corner_radius=6)
        self.about_card.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        about_desc = (
            "Central Administration Dashboard\n\n"
            "An integrated core utility module engineered using CustomTkinter and asynchronous thread "
            "handling processors. This distribution provides tools for monitoring remote system APIs, "
            "validating hardware load levels, and executing bulk diagnostic network transfers cleanly.\n\n"
            "Key Integrated Toolsets:\n"
            " • Network & Weather Engine: Parses geographic coordinates and maps multi-layer atmospheric cards.\n"
            " • Webhook Queue System: Multi-threaded dispatch channel with built-in HTTP-429 rate mitigation rules.\n"
            " • Local Hardware Diagnostic: Inspects execution tables and tracks process metrics directly."
        )

        self.lbl_desc = ctk.CTkLabel(
            self.about_card, text=about_desc, text_color=self.accent_white, 
            font=ctk.CTkFont(size=13), justify="left", wraplength=660
        )
        self.lbl_desc.pack(anchor="w", padx=25, pady=25)

        # Application Specs Section
        self.specs_box = ctk.CTkTextbox(self.about_frame, height=180, fg_color=self.bg_dark_grey, border_color=self.btn_grey, text_color=self.text_muted, font=("Courier New", 12))
        self.specs_box.grid(row=2, column=0, padx=10, pady=20, sticky="ew")
        
        system_specs = (
            "APPLICATION CONFIGURATION COMPLIANCE PROFILES:\n"
            f"--------------------------------------------------\n"
            f"[-] Interface Backend Layout : CustomTkinter UI v5.2.0+\n"
            f"[-] Graphical Environment     : Monochrome Strict Dark-Mode\n"
            f"[-] Active Thread Safety      : Asynchronous Worker Engine Pattern\n"
            f"[-] Client Privacy Safeguards : IPv4 Octet Masking Subroutine Enabled\n"
            f"[-] System Baseline Engine    : Python {platform.python_version()} Framework"
        )
        self.specs_box.insert("0.0", system_specs)
        self.specs_box.configure(state="disabled")

    # ---------------- INTERFACE OPERATIONS LOGIC ----------------
    def append_console(self, text):
        self.console_log.configure(state="normal")
        self.console_log.insert("end", f"[{time.strftime('%H:%M:%S')}] {text}\n")
        self.console_log.see("end")
        self.console_log.configure(state="disabled")

    def run_weather_thread(self):
        self.btn_fetch_data.configure(state="disabled", text="Reading Environment Data streams...")
        threading.Thread(target=self.execute_weather_logic, daemon=True).start()

    def run_webhook_thread(self):
        url = self.url_entry.get().strip()
        msg = self.msg_entry.get().strip()
        try:
            loops = int(self.count_spinner.get().strip())
            if loops <= 0: raise ValueError
        except ValueError:
            self.append_console("ERROR: Dispatch limits configuration count must be a positive integer value.")
            return

        if not url or not msg:
            self.append_console("ERROR: Mandatory targeting input entries must be present.")
            return
            
        self.btn_send_wh.configure(state="disabled", text="Transmitting Post Content Payload...")
        threading.Thread(target=self.execute_webhook_logic, args=(url, msg, loops), daemon=True).start()

    def trigger_diag_refresh(self):
        self.btn_refresh_diag.configure(state="disabled", text="Interrogating Hardware Devices...")
        threading.Thread(target=self.execute_diag_logic, daemon=True).start()

    # Weather Processing Engine
    def execute_weather_logic(self):
        try:
            ip_res = requests.get("https://api.ipify.org?format=json", timeout=10).json()
            actual_ip = ip_res.get("ip", "Unavailable")
            
            try:
                segments = actual_ip.split('.')
                masked_ip = f"{segments[0]}.***.***.{segments[3]}" if len(segments) == 4 else actual_ip
            except Exception:
                masked_ip = "Filtering Error"
                
            self.ip_display_lbl.configure(text=f"Detected Host IP: {masked_ip}")

            geo_res = requests.get(f"https://ipapi.co/{actual_ip}/json/", timeout=10).json()
            city = geo_res.get("city", "Unknown City")
            region = geo_res.get("region", "Unknown Region")
            country = geo_res.get("country_name", "Unknown Country")
            lat, lon = geo_res.get("latitude"), geo_res.get("longitude")
            self.loc_display_lbl.configure(text=f"Geographic Location: {city}, {region} ({country})")

            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&relative_humidity_2m=true"
            weather_res = requests.get(weather_url, timeout=10).json()
            current = weather_res.get("current_weather", {})
            
            weather_code = current.get("weathercode", 0)
            condition_mapping = {
                0: "Clear Sky", 1: "Mainly Clear", 2: "Partly Cloudy", 3: "Overcast",
                45: "Foggy", 51: "Light Drizzle", 61: "Light Rain", 63: "Moderate Rain",
                71: "Light Snow", 80: "Rain Showers", 95: "Thunderstorm"
            }
            
            hourly = weather_res.get("hourly", {})
            humidity_list = hourly.get("relative_humidity_2m", ["--"])
            humidity_val = f"{humidity_list[0]} %" if humidity_list else "-- %"

            self.temp_val.configure(text=f"{current.get('temperature', '--')} °C")
            self.cond_val.configure(text=condition_mapping.get(weather_code, f"Code {weather_code}"))
            self.wind_val.configure(text=f"{current.get('windspeed', '--')} km/h")
            self.humid_val.configure(text=humidity_val)

            try:
                ascii_url = f"https://v2.wttr.in/{city.replace(' ', '+')}?u&q&F&Q"
                ascii_res = requests.get(ascii_url, timeout=12, headers={"User-Agent": "curl"})
                cleaned_ascii_lines = [line for line in ascii_res.text.split('\n') if "Follow" not in line and "Location" not in line]
                final_ascii_canvas = '\n'.join(cleaned_ascii_lines[:25])
                
                self.ascii_text_box.configure(state="normal")
                self.ascii_text_box.delete("0.0", "end")
                self.ascii_text_box.insert("0.0", final_ascii_canvas)
                self.ascii_text_box.configure(state="disabled")
            except Exception as ascii_err:
                print(f"Canvas layout stream interrupt: {ascii_err}")

        except Exception as err:
            self.cond_val.configure(text="Fetch Error")
            print(f"Data channel exception: {err}")
        
        self.btn_fetch_data.configure(state="normal", text="Analyze Environment Profiles")

    # Webhook Operations Engine
    def execute_webhook_logic(self, url, message, total_loops):
        def generate_progress_bar(completed, total, length=24):
            ratio = completed / total
            filled = int(length * ratio)
            return f"[{'#' * filled}{'-' * (length - filled)}] {int(ratio * 100)}%"

        payload = {"content": message}
        successful_dispatches = 0

        self.append_console(f"INITIALIZING QUEUE STREAM: Enqueuing {total_loops} message transfers...")

        for current_run in range(1, total_loops + 1):
            try:
                response = requests.post(url, json=payload, timeout=10)
                
                if response.status_code == 204:
                    successful_dispatches += 1
                    progress = generate_progress_bar(current_run, total_loops)
                    self.append_console(f"{progress} Run {current_run}: Request Accepted (204).")
                    time.sleep(0.8)
                    
                elif response.status_code == 429:
                    try:
                        retry_window = response.json().get("retry_after", 3.0)
                    except Exception:
                        retry_window = 3.0
                    progress = generate_progress_bar(current_run - 1, total_loops)
                    self.append_console(f"{progress} WARNING (429): Rate Limited. Standing down for {retry_window}s...")
                    time.sleep(retry_window)
                    
                else:
                    progress = generate_progress_bar(current_run - 1, total_loops)
                    self.append_console(f"{progress} FAILED: Target responded with code {response.status_code}. Pausing...")
                    time.sleep(4.0)

            except Exception as stream_err:
                progress = generate_progress_bar(current_run - 1, total_loops)
                self.append_console(f"{progress} EXCEPTION: Connectivity broken -> {stream_err}")
                time.sleep(4.0)

        self.append_console(f"QUEUE DISCHARGE COMPLETE: {successful_dispatches}/{total_loops} tasks processed successfully.")
        self.btn_send_wh.configure(state="normal", text="Execute Remote Data Dispatch")

    # Hardware Interrogation Operations Engine
    def execute_diag_logic(self):
        try:
            os_profile = f"{platform.system()} {platform.release()} ({platform.machine()})"
            cpu_profile = f"{platform.processor()} ({psutil.cpu_count(logical=False)} Cores / {psutil.cpu_count(logical=True)} Threads)"
            
            ram = psutil.virtual_memory()
            ram_profile = f"{ram.available / (1024**3):.2f} GB Free / {ram.total / (1024**3):.2f} GB Total Pool"

            t_start = time.perf_counter()
            requests.get("https://1.1.1.1", timeout=5)
            t_end = time.perf_counter()
            latency_profile = f"{((t_end - t_start) * 1000):.1f} ms response time via edge gateway cloud"

            self.lbl_os.configure(text=f"Operating System: {os_profile}")
            self.lbl_cpu.configure(text=f"Processor Architecture: {cpu_profile}")
            self.lbl_ram.configure(text=f"Available Memory Matrix: {ram_profile}")
            self.lbl_latency.configure(text=f"Network Cloud Gateway Latency: {latency_profile}")

            process_pool = []
            for running_process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
                try:
                    cpu_use = running_process.info['cpu_percent'] or 0.0
                    mem_use = (running_process.info['memory_info'].rss / (1024**2)) if running_process.info['memory_info'] else 0.0
                    process_pool.append((running_process.info['pid'], running_process.info['name'], cpu_use, mem_use))
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

            process_pool.sort(key=lambda item: item[3], reverse=True)
            
            table_string = f"{'PID':<8}{'PROCESS NAME':<28}{'CPU %':<10}{'RAM USAGE':<12}\n"
            table_string += f"{'-'*58}\n"
            for row in process_pool[:5]:
                table_string += f"{row[0]:<8}{row[1][:24]:<28}{row[2]:<10.1f}{row[3]:<10.1f} MB\n"

            self.proc_box.configure(state="normal")
            self.proc_box.delete("0.0", "end")
            self.proc_box.insert("0.0", table_string)
            self.proc_box.configure(state="disabled")

        except Exception as e:
            self.lbl_latency.configure(text="Network Cloud Gateway Latency: Offline")
            print(f"Diagnostics reading fault encountered: {e}")

        self.btn_refresh_diag.configure(state="normal", text="Re-Scan Host Infrastructure Profiles")


if __name__ == "__main__":
    app = IntegratedUtilityApp()
    app.mainloop()