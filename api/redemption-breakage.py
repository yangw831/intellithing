# /api/redemption-breakage.py
from http.server import BaseHTTPRequestHandler
from io import BytesIO
import json
import matplotlib
matplotlib.use("Agg")  # non-GUI backend for serverless
import matplotlib.pyplot as plt

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body_raw = self.rfile.read(content_length) if content_length > 0 else b"{}"
            body = json.loads(body_raw.decode("utf-8"))

            earned = float(body.get("total_earned", 0))
            redeemed = float(body.get("total_redeemed", 0))
            
            if earned <= 0 or redeemed < 0 or redeemed > earned:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "invalid totals (earned <= 0, redeemed < 0, or redeemed > earned)"
                }).encode())
                return

            broken = max(earned - redeemed, 0.0)
            labels = ["Redeemed", "Broken"]
            sizes = [redeemed, broken]

            plt.figure(figsize=(5.2, 5.2))
            plt.pie(
                sizes, labels=labels, autopct="%1.1f%%",
                colors=["#2F6FED", "#F5A623"], startangle=90,
                textprops={"color": "#222", "fontsize": 10}
            )
            plt.title("Points Redeemed vs. Broken", fontsize=12)
            plt.tight_layout()

            buf = BytesIO()
            plt.savefig(buf, format="png", dpi=200)
            plt.close()

            png = buf.getvalue()
            
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Cache-Control", "public, max-age=600, s-maxage=600")
            self.end_headers()
            self.wfile.write(png)

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"server error: {str(e)}"}).encode())
