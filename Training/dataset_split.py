import splitfolders

RAW_DATA_DIR = "/content/drive/MyDrive/Road_damage_cnn_project/CNN_Road_Data/data_flat"
OUTPUT_DIR = "/content/drive/MyDrive/Road_damage_cnn_project/CNN_Road_Data/split_data"

if __name__ == "__main__":
    splitfolders.ratio(
        input=RAW_DATA_DIR,
        output=OUTPUT_DIR, 
        seed=42,
        ratio=(0.8, 0.1, 0.1),  # train, val, test
    )
    print("Dataset split complete.")