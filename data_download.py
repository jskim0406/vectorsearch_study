import tarfile
import json
import pandas as pd
import os
import requests
import gzip
import logging

# 로그 설정
log_dir = './logs'
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'data_processing.log')

# BasicConfig를 활용한 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('DataProcessingLogger')

# Step 1: 데이터셋 다운로드
def download_abo_dataset(url: str, output_path: str):
    """
    Downloads the ABO dataset tar file from the specified URL and saves it to the given output path.

    Args:
        url (str): The URL to download the dataset from.
        output_path (str): The path where the downloaded tar file will be saved.

    Raises:
        Exception: If the download fails, an exception with the status code is raised.

    Returns:
        None
    """
    logger.info("[STEP 1] Starting download from %s", url)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        logger.info("[STEP 1] Downloaded dataset to %s", output_path)
    else:
        logger.error("[STEP 1] Failed to download dataset. Status code: %s", response.status_code)
        raise Exception(f"Failed to download dataset. Status code: {response.status_code}")

# Step 2: tar 파일 추출
def extract_tar_file(tar_path: str, extract_to: str):
    """
    Extracts the contents of a tar file to a specified directory.

    Args:
        tar_path (str): The path to the tar file to be extracted.
        extract_to (str): The directory where the contents will be extracted.

    Raises:
        FileNotFoundError: If the specified tar file does not exist.

    Returns:
        None
    """
    logger.info("[STEP 2] Extracting %s to %s", tar_path, extract_to)
    if not os.path.exists(tar_path):
        logger.error("[STEP 2] Tar file %s does not exist.", tar_path)
        raise FileNotFoundError(f"Tar file {tar_path} does not exist.")
    with tarfile.open(tar_path, 'r') as tar:
        tar.extractall(path=extract_to)
    logger.info("[STEP 2] Extracted tar file to %s", extract_to)

# Step 3: 압축된 JSON 파일 로드 및 데이터 탐색
def load_and_explore_gzipped_json(directory: str, sample_size: int = 5):
    """
    Loads gzipped JSON files from a specified directory and combines them into a DataFrame.

    Args:
        directory (str): The path to the directory containing gzipped JSON files.
        sample_size (int, optional): The number of sample records to display in the logs. Defaults to 5.

    Raises:
        FileNotFoundError: If no gzipped JSON files are found in the specified directory.
        ValueError: If no data is loaded from the JSON files.

    Returns:
        pd.DataFrame: A DataFrame containing the loaded data.
    """
    logger.info("[STEP 3] Loading gzipped JSON files from %s", directory)
    all_data = []

    json_files = [file for file in os.listdir(directory) if file.endswith('.json.gz')]
    if not json_files:
        logger.error("[STEP 3] No gzipped JSON files found in directory %s", directory)
        raise FileNotFoundError(f"No gzipped JSON files found in directory {directory}")

    for file_name in json_files:
        file_path = os.path.join(directory, file_name)
        logger.info("[STEP 3] Processing file: %s", file_path)

        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    all_data.append(data)
                except json.JSONDecodeError as e:
                    logger.error("[STEP 3] Error decoding JSON in %s: %s", file_path, e)

    if not all_data:
        logger.error("[STEP 3] No data loaded from the JSON files.")
        raise ValueError("No data loaded from the JSON files.")

    df = pd.DataFrame(all_data)
    logger.info("[STEP 3] Loaded data with %d records.", len(df))
    logger.info("[STEP 3] Sample data: %s", df.head(sample_size).to_dict(orient='records'))
    logger.info("[STEP 3] Available columns: %s", df.columns.tolist())

    return df

# Step 4: 데이터를 CSV로 저장하여 Elasticsearch 인덱싱 준비
def save_to_csv(df: pd.DataFrame, output_path: str):
    """
    Saves a DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): The DataFrame containing preprocessed data.
        output_path (str): The path where the CSV file will be saved.

    Returns:
        None
    """
    logger.info("[STEP 5] Saving preprocessed data to %s", output_path)
    df.to_csv(output_path, index=False)
    logger.info("[STEP 5] Saved preprocessed data to %s", output_path)

# Main execution
if __name__ == "__main__":
    dataset_url = "https://amazon-berkeley-objects.s3.amazonaws.com/archives/abo-listings.tar"
    tar_file_path = "abo-listings.tar"
    extract_path = "./abo-listings"
    metadata_path = os.path.join(extract_path, "listings", "metadata")
    output_csv_path = "preprocessed_abo_listings.csv"

    try:
        # Step 1: 데이터셋 다운로드
        download_abo_dataset(dataset_url, tar_file_path)

        # Step 2: tar 파일 추출
        extract_tar_file(tar_file_path, extract_path)

        # Step 3: JSON 파일 로드 및 탐색
        df = load_and_explore_gzipped_json(metadata_path)

        # Step 4: 데이터를 CSV로 저장
        save_to_csv(df, output_csv_path)

        logger.info("Data processing completed successfully.")
        print("Data processing completed successfully.")

    except Exception as e:
        logger.error("An error occurred: %s", e)
        print(f"An error occurred: {e}")