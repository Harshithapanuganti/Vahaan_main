
import pandas as pd
import os

BASE_DIR = "vahan_data"


def extract_metadata(path):
    parts = path.split(os.sep)

    # example path:
    # vahan_data/State/RTO/Yaxis_Xaxis/year.csv
    try:
        state = parts[1]
        rto = parts[2]
        axis = parts[3]
        year = parts[4].replace(".csv", "")
    except IndexError:
        state, rto, axis, year = "unknown", "unknown", "unknown", "unknown"

    return state, rto, axis, year


def merge_files():
    all_data = []

    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)

                try:
                    df = pd.read_csv(file_path)

                    state, rto, axis, year = extract_metadata(file_path)

                    df["state"] = state
                    df["rto"] = rto
                    df["axis"] = axis
                    df["year"] = year

                    all_data.append(df)

                except Exception as e:
                    print(f"Skipping {file_path}: {e}")

    # ✅ ADD THIS FIX
    if not all_data:
        print("❌ No CSV files found in vahan_data folder. Skipping merge.")
        return

    # ✅ Safe now
    final_df = pd.concat(all_data, ignore_index=True)

    final_df.to_csv("final_merged_data.csv", index=False)

    print("✅ Saved: final_merged_data.csv")

    print("✅ Saved: final_merged_data.csv")


if __name__ == "__main__":
    merge_files()
