from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivy.clock import Clock
from kivy.lang import Builder
from datetime import datetime
import os, json, time

KV = '''
MDScreen:
    md_bg_color: 0.95, 0.95, 0.95, 1
    MDBoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            title: "TUFAN VPN SYSTEM"
            elevation: 4
            pos_hint: {"top": 1}
        
        MDBoxLayout:
            padding: "20dp"
            spacing: "20dp"
            orientation: 'vertical'
            
            MDBoxLayout:
                orientation: 'vertical'
                padding: "15dp"
                spacing: "10dp"
                
                MDLabel:
                    id: status_label
                    text: "الحالة: غير متصل"
                    halign: "center"
                    font_style: "H6"
                    text_color: 1, 0, 0, 1
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

            MDBoxLayout:
                size_hint_y: None
                height: "60dp"
                spacing: "15dp"
                MDRaisedButton:
                    id: connect_btn
                    text: "اتصال"
                    on_release: app.connect_vpn()
                MDRaisedButton:
                    id: disconnect_btn
                    text: "قطع الاتصال"
                    md_bg_color: 1,0.3,0.3,1
                    on_release: app.disconnect_vpn()
                    disabled: True

            MDLabel:
                text: "قائمة السيرفرات المتاحة"
                halign: "right"
                size_hint_y: None
                height: "30dp"
            
            MDScrollView:
                MDList:
                    id: server_list
'''

SERVERS = [
    {"name": "سيرفر أمريكا (US)", "country_code": "us"},
    {"name": "سيرفر أوروبا (EU)", "country_code": "de"},
    {"name": "سيرفر آسيا (Asia)", "country_code": "sg"}
]

class TufanVPNApp(MDApp):
    def build(self):
        self.connected = False
        self.connection_start_time = None
        self.current_server = None
        return Builder.load_string(KV)

    def on_start(self):
        # إضافة السيرفرات للقائمة
        for srv in SERVERS:
            item = OneLineAvatarIconListItem(text=srv["name"], on_release=lambda x, s=srv: self.select_server(s))
            icon = IconLeftWidget(icon=f"flag-{srv['country_code']}")
            item.add_widget(icon)
            self.root.ids.server_list.add_widget(item)

    def select_server(self, server):
        self.current_server = server
        self.root.ids.server_label.text = f"السيرفر: {server['name']}"
        self.root.ids.status_label.text = "جاهز للاتصال"
        self.root.ids.status_label.text_color = [0,0,1,1]

    def connect_vpn(self):
        if not self.current_server:
            self.root.ids.status_label.text = "اختر سيرفر أولاً!"
            return
        # محاكاة اتصال VPN بدون روت
        self.connected = True
        self.connection_start_time = datetime.now()
        self.root.ids.status_label.text = "متصل بنجاح ✓"
        self.root.ids.status_label.text_color = [0,0.6,0,1]
        self.root.ids.connect_btn.disabled = True
        self.root.ids.disconnect_btn.disabled = False
        Clock.schedule_interval(self.update_timer, 1)

    def disconnect_vpn(self):
        self.connected = False
        self.root.ids.status_label.text = "غير متصل"
        self.root.ids.status_label.text_color = [1,0,0,1]
        self.root.ids.connect_btn.disabled = False
        self.root.ids.disconnect_btn.disabled = True
        self.root.ids.timer_label.text = "00:00:00"
        Clock.unschedule(self.update_timer)

    def update_timer(self, dt):
        if self.connected and self.connection_start_time:
            elapsed = datetime.now() - self.connection_start_time
            self.root.ids.timer_label.text = str(elapsed).split('.')[0].zfill(8)

if __name__ == "__main__":
    TufanVPNApp().run()
