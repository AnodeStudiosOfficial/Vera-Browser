import tkinter as tk
from tkinter import messagebox
import json
import os
import sys

# Politika motorumuzu içe aktaralım (Eğer aynı dizindeyse)
try:
    from policy_engine import VeraPolicyEngine
    from ephemeral_storage import VeraEphemeralStorage
except ImportError:
    # Dosyalar henüz import edilemezse dummy sınıf tanımlayalım
    VeraPolicyEngine = None
    VeraEphemeralStorage = None

class VeraBrowserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vera Secure Browser - Ephemeral Session")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e2e")

        # Güvenlik ve Politika Motoru Başlatma
        if VeraEphemeralStorage:
            self.session = VeraEphemeralStorage()
        else:
            self.session = None

        if VeraPolicyEngine:
            self.policy_engine = VeraPolicyEngine()
        else:
            self.policy_engine = None

        self.create_widgets()

    def create_widgets(self):
        # Üst Araç Çubuğu (Toolbar)
        toolbar = tk.Frame(self.root, bg="#252538", height=50)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Adres Çubuğu (URL Entry)
        self.url_entry = tk.Entry(toolbar, font=("Arial", 12), bg="#313148", fg="#ffffff", insertbackground="white")
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
        self.url_entry.insert(0, "https://www.eba.gov.tr")
        self.url_entry.bind("<Return>", lambda event: self.navigate())

        # Git Butonu
        go_btn = tk.Button(toolbar, text="Git / Doğrula", command=self.navigate, bg="#4f46e5", fg="white", font=("Arial", 10, "bold"), relief=tk.FLAT, padx=10)
        go_btn.pack(side=tk.LEFT, padx=5, pady=10)

        # Orta Alan (Tarayıcı İçerik / Simülasyon Ekranı)
        self.content_frame = tk.Frame(self.root, bg="#11111b")
        self.content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.info_label = tk.Label(
            self.content_frame, 
            text="🛡️ VERA SECURE BROWSER\nRAM-Disk Ephemeral Sandbox Aktif\nTüm çerezler ve geçmiş kapatılmıştır.", 
            bg="#11111b", 
            fg="#a6adc8", 
            font=("Arial", 14)
        )
        self.info_label.pack(expand=True)

        # Alt Güvenlik Durum Çubuğu (Status Bar)
        status_bar = tk.Frame(self.root, bg="#181825", height=30)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_text = tk.Label(status_bar, text=" Durum: Güvenli Oturum | Bloklar: Aktif", bg="#181825", fg="#a6e3a1", font=("Arial", 9))
        self.status_text.pack(side=tk.LEFT, padx=10, pady=5)

    def navigate(self):
        target_url = self.url_entry.get().strip()
        
        # Politika motoru ile URL kontrolü yapalım
        if self.policy_engine:
            is_allowed = self.policy_engine.check_url_access(target_url)
            if not is_allowed:
                messagebox.showerror("Erişim Engellendi", f"Bu site merkezi güvenlik politikaları gereği engellenmiştir:\n\n{target_url}")
                self.status_text.config(text=f" Durum: Engellendi -> {target_url}", fg="#f38ba8")
                return

        messagebox.showinfo("Güvenli Bağlantı", f"Adrese gidiliyor: {target_url}\n(Veriler diske yazılmıyor)")
        self.status_text.config(text=f" Durum: Bağlanıldı -> {target_url}", fg="#a6e3a1")

    def on_close(self):
        # Oturum kapatıldığında RAM'i temizle
        if self.session:
            self.session.destroy_session()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VeraBrowserApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()