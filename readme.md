# 📊 Sensor Data Visualizer（ターミナル版）

Pythonで開発した、センサーデータ（例：筋電など）の可視化・統計解析・異常検出ツールです。  
CSVファイルからデータを読み込み、平滑化・統計計算・ピーク検出・FFT（周波数解析）などを行い、グラフ・CSVで出力する実用的なツールです。

---

## 🚀 特徴

- ✅ 入出力ファイル名をターミナルで指定可能
- ✅ 移動平均によるノイズ除去（自動適用）
- ✅ 平均・最大・最小・RMS（実効値）の計算
- ✅ 急激な変化（しきい値超過）を自動検出・可視化
- ✅ ピーク検出（局所最大）＋CSV保存
- ✅ FFT（高速フーリエ変換）による周波数解析
- ✅ 統計・ピーク情報のCSV出力
- ✅ 時系列グラフ・FFTスペクトルをPNG形式で保存

---

## 📦 必要環境

- Python 3.x
- pandas
- matplotlib
- numpy
- scipy

---

## ▶️ 使い方（Usage）

### 1. ライブラリをインストール

```bash
pip install pandas matplotlib numpy scipy
```

---

### 2. プログラムを実行

```bash
python app_terminal_v3.py
```

---

### 3. ファイル名を入力（例）

```
📂 入力CSVファイル名（例: complex_dummy_emg.csv）:
📄 出力する統計CSVファイル名（例: summary.csv）:
🖼️ 時系列グラフ画像ファイル名（例: graph.png）:
📊 FFTスペクトル画像ファイル名（例: fft.png）:
📄 ピーク検出CSVファイル名（例: peaks.csv）:
```

---

### 4. 出力ファイル一覧

| ファイル名 | 説明 |
|------------|------|
| `summary.csv` | 統計情報（平均・最大・最小・RMS・急変回数） |
| `graph.png`   | 時系列グラフ＋ピーク・急変点付き |
| `fft.png`     | 周波数スペクトル（FFT解析） |
| `peaks.csv`   | ピーク時刻とその値一覧 |

---

## 📂 サンプルデータ

このリポジトリには、人工的に作成した筋電風センサーデータを含みます：

- `complex_dummy_emg.csv`  
　⤷ sin波 + 高周波 + ノイズ + 異常ピーク付き

---

## 📌 ファイル構成

```text
├── app_terminal_v3.py         # メインスクリプト（FFT・ピーク検出対応）
├── complex_dummy_emg.csv      # サンプルデータ
├── summary.csv                # 統計出力例
├── peaks.csv                  # ピーク出力例
├── graph.png                  # 時系列グラフ例
├── fft.png                    # FFTスペクトル例
└── README.md                  # この説明ファイル
```

---

## 👨‍💻 制作意図・背景

大学での演習で得た知識を応用し、センサーデータの処理・可視化を体系的に学ぶために個人で開発しました。  

---

## 🪪 ライセンス

MIT License（改変・商用利用自由）

---

## 🙋‍♂️ 作者

- 瀧上 壱空（Ritsumeikan University / 情報理工学部）
- GitHub: [ikkuusan]
