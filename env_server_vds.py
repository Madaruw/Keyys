#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MadExternal .env Server - VDS Version
Bu sunucu .env dosyasını HTTP üzerinden serve eder.
VDS'de çalıştırılır, EXE'ler bu sunucudan .env dosyasını okuyacak.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json

PORT = 8080
ENV_FILE = "config.env"  # .env dosyasının yolu (env_server.py ile aynı klasörde)

class EnvHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/env' or self.path == '/env.txt':
            # .env dosyasını oku
            try:
                env_path = os.path.join(os.path.dirname(__file__), ENV_FILE)
                if os.path.exists(env_path):
                    with open(env_path, 'r', encoding='utf-8') as f:
                        env_content = f.read()
                    
                    # CORS headers
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/plain; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Access-Control-Allow-Methods', 'GET')
                    self.end_headers()
                    self.wfile.write(env_content.encode('utf-8'))
                    print(f"[{self.address_string()}] ✅ GET /env - 200 OK")
                else:
                    self.send_response(404)
                    self.send_header('Content-Type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(b'.env file not found')
                    print(f"[{self.address_string()}] ❌ GET /env - 404 Not Found")
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(f'Error: {str(e)}'.encode('utf-8'))
                print(f"[{self.address_string()}] ❌ GET /env - 500 Error: {e}")
        elif self.path == '/' or self.path == '/status':
            # Status endpoint
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'MadExternal .env Server is running!\nUse /env endpoint to get config.')
            print(f"[{self.address_string()}] ✅ GET {self.path} - 200 OK")
        else:
            self.send_response(404)
            self.end_headers()
            print(f"[{self.address_string()}] ❌ GET {self.path} - 404 Not Found")
    
    def log_message(self, format, *args):
        # Log mesajları zaten yukarıda print ediliyor
        pass

def run_server():
    server_address = ('0.0.0.0', PORT)  # 0.0.0.0 = tüm ağ arayüzlerinde dinle
    httpd = HTTPServer(server_address, EnvHandler)
    
    # .env dosyasının varlığını kontrol et
    env_path = os.path.join(os.path.dirname(__file__), ENV_FILE)
    if not os.path.exists(env_path):
        print(f"⚠️  UYARI: {ENV_FILE} dosyası bulunamadı!")
        print(f"📁 Aranan konum: {env_path}")
        print(f"💡 Lütfen {ENV_FILE} dosyasını script ile aynı klasöre koyun.\n")
    else:
        print(f"✅ {ENV_FILE} dosyası bulundu: {env_path}")
    
    print(f"\n🚀 MadExternal .env Server başlatıldı!")
    print(f"📡 Port: {PORT}")
    print(f"🌐 Dinlenen adres: 0.0.0.0:{PORT} (tüm ağ arayüzleri)")
    print(f"🌐 Local test: http://localhost:{PORT}/env")
    print(f"🌐 External URL: http://35.205.146.21:{PORT}/env")
    print(f"\n✅ Sunucu çalışıyor ve istekleri bekliyor...")
    print(f"⚠️  Sunucuyu kapatmak için Ctrl+C basın\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n🛑 Sunucu kapatılıyor...")
        httpd.server_close()
        print("✅ Sunucu kapatıldı")
    except Exception as e:
        print(f"\n❌ HATA: Sunucu başlatılamadı: {e}")
        print(f"💡 Port {PORT} zaten kullanılıyor olabilir veya yetki sorunu var.")

if __name__ == '__main__':
    run_server()
