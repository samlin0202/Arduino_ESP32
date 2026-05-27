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
                k, v = line.strip().split(":")
                stats += f"{k}: {v}\n"
                labels.append(k)
                values.append(int(v))

    # ======================
    # 📈 建立圖表（重點）
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
    # 🖼️ 讀圖片
    # ======================
    img_folder = "data/detected_images"
    images = os.listdir(img_folder) if os.path.exists(img_folder) else []

    # ======================
    # 🧱 滿版圖片排版（重點）
    # ======================
    img_html = """
    <style>
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }

        .card {
            text-align: center;
            padding: 10px;
            border-radius: 12px;
            box-shadow: 0 0 10px #ddd;
        }

        img {
            width: 100%;
            border-radius: 10px;
        }
    </style>

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
    # 🌐 HTML
    # ======================
    html = f"""
    <html>
    <head>
        <title>YOLO Dashboard</title>
    </head>

    <body style="font-family:Arial; margin:20px;">

        <h1>🚀 YOLO 垃圾辨識系統</h1>

        <h2>📊 統計結果</h2>
        <pre>{stats}</pre>

        <h2>📈 圖表</h2>
        <img src="/static/chart.png" width="500">

        <h2>🖼️ 辨識圖片</h2>
        {img_html}

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