import pandas as pd
import boto3
from datetime import date

# load raw csv from local resource
path = r"Mlops_house_predication_raw_data.csv"

data = pd.read_csv(path)
df = pd.DataFrame(data)

print("=========== Before Cleaning ============")
print(df.isnull().sum())
print(f"Shape Before : {df.shape}")

print()

# data cleaning
df_clean = df.dropna()

print("=========== After Cleaning ============")
print(df_clean.isnull().sum())
print(f"Shape After : {df_clean.shape}")

# saved cleaned CSV locally
clean_path = r"C:\Users\ruhi singh\Desktop\MLOPS\Mlops_house_predication_clean_v2.csv"


df_clean.to_csv(clean_path, index=False)

print(f"\nCleaned file saved at: {clean_path}")


# upload to S3 as processed version
s3 = boto3.client("s3")

BUCKET = "mlopsruhi-s3-bucket"


def upload_processed_data(local_path):

    key = f"processed/{date.today()}/Mlops_house_predication_clean_v2.csv"

    try:
        s3.upload_file(
            local_path,
            BUCKET,
            key
        )

        print(f"\nUploaded to s3://{BUCKET}/{key}")

        return key

    except FileNotFoundError:
        print(f"File not found: {local_path}")

    except Exception as e:
        print(f"S3 upload failed: {e}")


upload_processed_data(clean_path)

