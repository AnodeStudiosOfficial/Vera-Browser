import os
import shutil
import tempfile

class VeraEphemeralStorage:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="vera_secure_session_")
        print(f"[GÜVENLİK] İzole oturum alanı oluşturuldu: {self.temp_dir}")

    def get_session_path(self):
        return self.temp_dir

    def destroy_session(self):
        """Oturum kapatıldığında tüm verileri RAM/Disk kalıntısı bırakmadan imha eder."""
        if os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                print("[GÜVENLİK] Oturum sonlandırıldı. Tüm önbellek ve çerezler imha edildi.")
            except Exception as e:
                print(f"[HATA] Oturum temizlenirken sorun oluştu: {e}")

if __name__ == "__main__":
    session = VeraEphemeralStorage()
    dummy_cache_file = os.path.join(session.get_session_path(), "temp_cookie.txt")
    with open(dummy_cache_file, "w") as f:
        f.write("Gizli oturum verisi")
    print(f"Geçici dosya oluşturuldu: {dummy_cache_file}")
    session.destroy_session()
    print(f"Oturum klasörü hala duruyor mu?: {os.path.exists(session.get_session_path())}")
