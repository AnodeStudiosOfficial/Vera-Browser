import json
import fnmatch

class VeraPolicyEngine:
    def __init__(self, policy_file_path="vera_policy.json"):
        self.policy_file_path = policy_file_path
        self.policies = self.load_policies()

    def load_policies(self):
        try:
            with open(self.policy_file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"[HATA] Politika dosyası bulunamadı: {self.policy_file_path}")
            return {}

    def get_security_flags(self):
        """Tarayıcının başlangıç güvenlik parametrelerini döndürür."""
        return self.policies.get("security_policies", {})

    def check_url_access(self, url: str) -> bool:
        """Girilen URL'nin politika kurallarına uygun olup olmadığını kontrol eder."""
        access_control = self.policies.get("access_control", {})
        mode = access_control.get("mode", "blacklist")
        
        if mode == "whitelist":
            for pattern in access_control.get("whitelist", []):
                if fnmatch.fnmatch(url, f"*{pattern}*"):
                    return True
            return False
            
        elif mode == "blacklist":
            for pattern in access_control.get("blacklist", []):
                if fnmatch.fnmatch(url, f"*{pattern}*"):
                    return False
            return True
            
        return False

if __name__ == "__main__":
    engine = VeraPolicyEngine()
    print("--- Vera Güvenlik Bayrakları ---")
    print(json.dumps(engine.get_security_flags(), indent=4, ensure_ascii=False))
    
    print("\n--- URL Erişim Testleri ---")
    test_urls = [
        "https://www.eba.gov.tr/ders",
        "https://www.socialmedia.com/feed",
        "https://msb.gov.tr/duyuru",
        "https://www.gaming-portal.com/play"
    ]
    for url in test_urls:
        allowed = engine.check_url_access(url)
        status = "✅ İZİN VERİLDİ" if allowed else "❌ ENGELLENDİ"
        print(f"{status} -> {url}")
