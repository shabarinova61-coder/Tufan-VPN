from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.scrollview import MDScrollView
from kivy.clock import Clock
from kivy.lang import Builder
import os, sys, time, json, subprocess, threading, platform, signal
from datetime import datetime

# ===================== KivyMD Interface (KV) =====================
KV = '''
MDScreen:
    md_bg_color: 0.95, 0.95, 0.95, 1
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "TUFAN VPN SYSTEM"
            elevation: 4
            pos_hint: {"top": 1}
            left_action_items: [["menu", lambda x: print("Menu")]]
            right_action_items: [["robot", lambda x: print("Robot")]]

        MDBoxLayout:
            padding: "20dp"
            spacing: "20dp"
            orientation: 'vertical'
            
            # قسم الحالة والعداد
            MDCard:
                orientation: 'vertical'
                padding: "15dp"
                size_hint_y: None
                height: "180dp"
                radius: [15, 15, 15, 15]
                elevation: 3
                MDLabel:
                    id: status_label
                    text: "الحالة: غير متصل"
                    halign: "center"
                    font_style: "H6"
                    theme_text_color: "Custom"
                    text_color: 1, 0, 0, 1 # أحمر
                MDLabel:
                    id: timer_label
                    text: "00:00:00"
                    halign: "center"
                    font_style: "H4"
                MDLabel:
                    id: server_label
                    text: "السيرفر: لم يتم الاختيار"
                    halign: "center"
                    font_style: "Subtitle1"

            # أزرار التحكم
            MDBoxLayout:
                size_hint_y: None
                height: "60dp"
                spacing: "15dp"
                MDRaisedButton:
                    id: connect_btn
                    text: "اتصال"
                    icon: "play"
                    size_hint_x: .5
                    on_release: app.connect_vpn()
                MDRaisedButton:
                    id: disconnect_btn
                    text: "قطع الاتصال"
                    icon: "stop"
                    size_hint_x: .5
                    md_bg_color: 1, 0.3, 0.3, 1
                    on_release: app.disconnect_vpn()
                    disabled: True

            # قائمة السيرفرات
            MDLabel:
                text: "قائمة السيرفرات المتاحة"
                halign: "right"
                font_style: "Subtitle1"
                size_hint_y: None
                height: "30dp"
            
            MDCard:
                radius: [15, 15, 15, 15]
                elevation: 2
                MDScrollView:
                    MDList:
                        id: server_list
'''

# ===================== configuration =====================
CONFIG_DIR = os.path.expanduser("~/.vpn_client")
LOG_FILE = os.path.join(CONFIG_DIR, "vpn.log")
SERVERS_FILE = os.path.join(CONFIG_DIR, "servers.json")
DEFAULT_SERVERS = [
    {"name": "سيرفر أمريكا (US)", "config": "us.ovpn", "country_code": "us"},
    {"name": "سيرفر أوروبا (EU)", "config": "eu.ovpn", "country_code": "de"},
    {"name": "سيرفر آسيا (Asia)", "config": "asia.ovpn", "country_code": "sg"}
]
os.makedirs(CONFIG_DIR, exist_ok=True)

class TufanVPNApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.process = None
        self.connected = False
        self.connection_start_time = None
        self.current_server = None
        return Builder.load_string(KV)

    def on_start(self):
        self.load_servers()
        # فحص وجود OpenVPN
        if subprocess.call(["which", "openvpn"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            self.root.ids.status_label.text = "خطأ: OpenVPN غير مثبت"
            self.root.ids.connect_btn.disabled = True

    # ===================== VPN Logic =====================
    def load_servers(self):
        servers = DEFAULT_SERVERS
        if os.path.exists(SERVERS_FILE):
            with open(SERVERS_FILE, "r") as f:
                servers = json.load(f)
        else:
            with open(SERVERS_FILE, "w") as f:
                json.dump(DEFAULT_SERVERS, f, indent=4)
        
        # إضافة السيرفرات للقائمة
        for srv in servers:
            item = OneLineAvatarIconListItem(text=srv["name"], on_release=lambda x, s=srv: self.select_server(s))
            icon = IconLeftWidget(icon=f"flag-{srv['country_code']}")
            item.add_widget(icon)
            self.root.ids.server_list.add_widget(item)

    def select_server(self, server):
        self.current_server = server
        self.root.ids.server_label.text = f"السيرفر: {server['name']}"
        self.root.ids.status_label.text = "جاهز للاتصال"
        self.root.ids.status_label.text_color = [0, 0, 1, 1] # أزرق

    def connect_vpn(self):
        if not self.current_server:
            self.root.ids.status_label.text = "اختر سيرفر أولاً!"
            return

        config_file = self.current_server["config"]
        # محاولة البحث عن الملف في المجلد الافتراضي
        full_path = os.path.join(CONFIG_DIR, config_file)
        if not os.path.exists(full_path):
            self.root.ids.status_label.text = f"ملف {config_file} غير موجود!"
            return

        # أمر تشغيل OpenVPN (يحتاج صلاحيات root على أندرويد حقيقي)
        cmd = ["sudo", "openvpn", "--config", full_path, "--daemon", "--log", LOG_FILE]
        
        try:
            self.root.ids.status_label.text = "جاري الاتصال..."
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # انتظر قليلاً للتحقق من الاتصال
            Clock.schedule_once(self.check_connection, 5)
        except Exception as e:
            self.root.ids.status_label.text = f"خطأ في البدء: {e}"

    def check_connection(self, dt):
        # التحقق من أن العملية مازالت تعمل
        if self.process and self.process.poll() is None:
            self.connected = True
            self.connection_start_time = datetime.now()
            self.root.ids.status_label.text = "متصل بنجاح ✓"
            self.root.ids.status_label.text_color = [0, 0.6, 0, 1] # أخضر
            self.root.ids.connect_btn.disabled = True
            self.root.ids.disconnect_btn.disabled = False
            # بدء العداد
            Clock.schedule_interval(self.update_timer, 1)
        else:
            self.root.ids.status_label.text = "فشل الاتصال!"
            self.root.ids.status_label.text_color = [1, 0, 0, 1]

    def disconnect_vpn(self):
        if self.process:
            subprocess.call(["sudo", "killall", "openvpn"])
            self.process = None
        self.connected = False
        self.root.ids.status_label.text = "غير متصل"
        self.root.ids.status_label.text_color = [1, 0, 0, 1]
        self.root.ids.connect_btn.disabled = False
        self.root.ids.disconnect_btn.disabled = True
        self.root.ids.timer_label.text = "00:00:00"
        Clock.unschedule(self.update_timer)

    def update_timer(self, dt):
        if self.connected and self.connection_start_time:
            elapsed = datetime.now() - self.connection_start_time
            # تنسيق الوقت ليكون HH:MM:SS
            time_str = str(elapsed).split('.')[0].zfill(8)
            self.root.ids.timer_label.text = time_str

if __name__ == "__main__":
    TufanVPNApp().run()



