import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# === ユーザー入力 ===
csv_file = input("📂 入力CSVファイル名（例: complex_dummy_emg.csv）: ").strip()
summary_file = input("📄 出力する統計CSVファイル名（例: summary.csv）: ").strip()
graph_file = input("🖼️ 時系列グラフ画像ファイル名（例: graph.png）: ").strip()
fft_file = input("📊 FFTスペクトル画像ファイル名（例: fft.png）: ").strip()
peak_file = input("📄 ピーク検出CSVファイル名（例: peaks.csv）: ").strip()

# === パラメータ設定 ===
smoothing_window = 5
diff_threshold = 0.8

try:
    print("📥 データ読み込み中...")
    df = pd.read_csv(csv_file)
    df['smoothed'] = df['value'].rolling(window=smoothing_window, center=True).mean().fillna(method='bfill').fillna(method='ffill')

    # === 統計量 ===
    average = df['smoothed'].mean()
    rms = np.sqrt(np.mean(df['smoothed']**2))
    max_val = df['smoothed'].max()
    min_val = df['smoothed'].min()
    max_time = df.loc[df['smoothed'].idxmax(), 'time']
    min_time = df.loc[df['smoothed'].idxmin(), 'time']

    # === 急変検出 ===
    diff = df['smoothed'].diff().abs()
    sudden_changes = df[diff > diff_threshold]

    # === ピーク検出 ===
    peaks, _ = find_peaks(df['smoothed'], distance=10, prominence=0.2)
    peak_df = pd.DataFrame({
        'peak_time': df['time'].iloc[peaks].values,
        'peak_value': df['smoothed'].iloc[peaks].values
    })
    peak_df.to_csv(peak_file, index=False)
    print(f"🔺 ピークデータを {peak_file} に保存しました")

    # === FFT（スペクトル解析） ===
    time = df['time'].values
    signal = df['smoothed'].values
    dt = time[1] - time[0]
    n = len(signal)
    freq = np.fft.fftfreq(n, d=dt)[:n//2]
    fft_vals = np.fft.fft(signal)
    fft_mag = 2.0/n * np.abs(fft_vals[:n//2])

    # === 統計CSV出力 ===
    summary_df = pd.DataFrame({
        'metric': ['average', 'RMS', 'maximum', 'minimum', 'sudden_changes'],
        'value': [average, rms, max_val, min_val, len(sudden_changes)],
        'time(s)': ['-', '-', f"{max_time:.2f}", f"{min_time:.2f}", '-']
    })
    summary_df.to_csv(summary_file, index=False)
    print(f"📄 統計情報を {summary_file} に保存しました")

    # === グラフ1：時系列（ピーク＋急変） ===
    plt.figure(figsize=(12, 5))
    plt.plot(df['time'], df['smoothed'], label='Smoothed', color='blue')
    plt.scatter(max_time, max_val, color='red', label='Max')
    plt.scatter(min_time, min_val, color='green', label='Min')
    plt.scatter(sudden_changes['time'], sudden_changes['smoothed'], color='orange', label='Sudden Changes')
    plt.plot(df['time'].iloc[peaks], df['smoothed'].iloc[peaks], "ro", label='Peaks')
    plt.xlabel('Time (s)')
    plt.ylabel('Value')
    plt.title('Sensor Data Visualization with Peaks')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(graph_file)
    plt.close()
    print(f"🖼️ グラフ画像を {graph_file} に保存しました")

    # === グラフ2：FFTスペクトル ===
    plt.figure(figsize=(10, 4))
    plt.plot(freq, fft_mag)
    plt.title('FFT Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(fft_file)
    plt.close()
    print(f"📊 FFTスペクトル画像を {fft_file} に保存しました")

except FileNotFoundError:
    print(f"❌ ファイル '{csv_file}' が見つかりません。")
except Exception as e:
    print("⚠️ エラーが発生しました：", e)
