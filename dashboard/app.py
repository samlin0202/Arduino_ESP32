from flask import Flask, send_from_directory
import os
import matplotlib.pyplot as plt

app = Flask(__name__)

# 確保 static 存在
os.makedirs("static", exist_ok=True)


@app.route("/")
def home():

    # ======================
    # 📊 讀取統計
    # ======================
    stats = ""
    labels = []
    values = []

    if os.path.exists("result.txt"):
        with open("result.txt", "r", encoding="utf-8") as f:
            for line in f:
                if ":" in line:
                    k, v = line.strip().split(":")
                    stats += f"{k}: {v}\n"
                    labels.append(k)
                    values.append(int(v))

    # ======================
    # 📈 圖表
    # ======================
    if labels:
        plt.figure(figsize=(6, 4))
        plt.bar(labels, values)
        plt.title("YOLO 辨識統計")
        plt.xlabel("類別")
        plt.ylabel("數量")
        plt.tight_layout()
        plt.savefig("static/chart.png")
        plt.close()

    # ======================
    # 🖼️ 圖片
    # ======================
    img_folder = "data/detected_images"
    images = os.listdir(img_folder) if os.path.exists(img_folder) else []

    img_html = """
    <div class="grid">
    """

    for img in images:
        img_html += f"""
        <div class="card">
            <img src="/img/{img}">
            <p>{img}</p>
        </div>
        """

    img_html += "</div>"

    # ======================
    # 🌐 HTML + CSS UI
    # ======================
    html = f"""
    <html>
    <head>
        <title>YOLO Dashboard</title>

        <style>
            body {{
                margin: 0;
                font-family: "Segoe UI", sans-serif;
                background: linear-gradient(135deg, #0f172a, #1e1b4b, #0f172a);
                color: white;
            }}

            h1 {{
                text-align: center;
                padding: 20px;
                font-size: 32px;
            }}

            h2 {{
                margin-top: 30px;
                border-left: 5px solid #6366f1;
                padding-left: 10px;
                margin-left: 20px;
            }}

            pre {{
                background: rgba(255,255,255,0.08);
                padding: 15px;
                margin: 20px;
                border-radius: 12px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 30px rgba(0,0,0,0.3);
            }}

            .chart-box {{
                text-align: center;
            }}

            .chart-box img {{
                width: 500px;
                max-width: 90%;
                border-radius: 12px;
                box-shadow: 0 8px 25px rgba(0,0,0,0.4);
            }}

            .grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 20px;
                padding: 20px;
            }}

            .card {{
                background: rgba(255, 255, 255, 0.08);
                backdrop-filter: blur(12px);
                border-radius: 16px;
                padding: 10px;
                text-align: center;
                box-shadow: 0 8px 30px rgba(0,0,0,0.3);
                transition: 0.3s;
            }}

            .card:hover {{
                transform: translateY(-8px);
                box-shadow: 0 12px 40px rgba(0,0,0,0.5);
            }}

            .card img {{
                width: 100%;
                border-radius: 12px;
            }}

            .refresh {{
                text-align: center;
                font-size: 12px;
                opacity: 0.6;
                margin-bottom: 20px;
            }}
        </style>
    </head>

    <body>

        <h1>🚀 YOLO 垃圾辨識系統 Dashboard</h1>

        <h2>📊 統計結果</h2>
        <pre>{stats}</pre>

        <h2>📈 圖表分析</h2>
        <div class="chart-box">
            <img src="/static/chart.png">
        </div>

        <h2>🖼️ 辨識圖片</h2>
        {img_html}

        <div class="refresh">🔄 每 5 秒自動更新</div>

        <script>
            setTimeout(() => {{
                location.reload();
            }}, 5000);
        </script>

    </body>
    </html>
    """

    return html


@app.route("/img/<filename>")
def get_image(filename):
    return send_from_directory("data/detected_images", filename)


if __name__ == "__main__":
    app.run(debug=True)