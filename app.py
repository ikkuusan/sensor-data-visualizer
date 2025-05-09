import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === ユーザー入力 ===
csv_file = input("📂 入力CSVファイル名を入力してください（例: complex_dummy_emg.csv）: ").strip()
summary_file = input("📄 出力する統計CSVファイル名（例: summary_v2.csv）: ").strip()
graph_file = input("🖼️ 出力するグラフ画像ファイル名（例: graph_v2.png）: ").strip()

# === パラメータ ===
smoothing_enabled = True
smoothing_window = 5
diff_threshold = 0.8  # 急変判定のしきい値

try:
    print("📥 データ読み込み中...")
    df = pd.read_csv(csv_file)
    print("✅ 読み込み成功")

    # 移動平均処理
    if smoothing_enabled:
        df['smoothed'] = df['value'].rolling(window=smoothing_window, center=True).mean()
        df['smoothed'] = df['smoothed'].fillna(method='bfill').fillna(method='ffill')
    else:
        df['smoothed'] = df['value']

    # 統計量計算
    average = df['smoothed'].mean()
    rms = np.sqrt(np.mean(df['smoothed']**2))
    max_val = df['smoothed'].max()
    min_val = df['smoothed'].min()
    max_time = df.loc[df['smoothed'].idxmax(), 'time']
    min_time = df.loc[df['smoothed'].idxmin(), 'time']

    # 急激な変化の検出
    diff = df['smoothed'].diff().abs()
    sudden_changes = df[diff > diff_threshold]

    print("\n📊 統計情報")
    print(f"平均値：{average:.3f}")
    print(f"実効値（RMS）：{rms:.3f}")
    print(f"最大値：{max_val:.3f}（{max_time:.2f} 秒）")
    print(f"最小値：{min_val:.3f}（{min_time:.2f} 秒）")
    print(f"急変ポイント検出数：{len(sudden_changes)}")

    # 統計CSV保存
    summary_df = pd.DataFrame({
        'metric': ['average', 'RMS', 'maximum', 'minimum', 'sudden_changes'],
        'value': [average, rms, max_val, min_val, len(sudden_changes)],
        'time(s)': ['-', '-', f"{max_time:.2f}", f"{min_time:.2f}", '-']
    })
    summary_df.to_csv(summary_file, index=False)
    print(f"📄 統計情報 {summary_file} を保存しました")

    # グラフ描画・保存
    plt.figure(figsize=(12, 5))
    plt.plot(df['time'], df['smoothed'], label='Smoothed Value', color='blue')
    plt.scatter(max_time, max_val, color='red', label='Max', zorder=5)
    plt.scatter(min_time, min_val, color='green', label='Min', zorder=5)
    plt.scatter(sudden_changes['time'], sudden_changes['smoothed'], color='orange', label='Sudden Change', zorder=5)
    plt.xlabel('Time (s)')
    plt.ylabel('Sensor Value')
    plt.title('Advanced Sensor Data Visualization')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(graph_file)
    plt.show()

    print(f"🖼️ グラフ画像 {graph_file} を保存しました")

except FileNotFoundError:
    print(f"❌ ファイル '{csv_file}' が見つかりません。")
except Exception as e:
    print("⚠️ エラーが発生しました：", e)
