import os
import pandas as pd
from app.core.config import settings
from app.services.image_downloader import download_images_from_filtered_data
import asyncio

async def load_invalid_ids(company_name):
    """
    Loads the invalid IDs from the invalid_ids.csv file asynchronously.
    Returns the list of invalid IDs.
    """
    invalid_ids_path = os.path.join(settings.DATA_OUTPUT_FOLDER, company_name, "invalid_ids.csv")
    if os.path.exists(invalid_ids_path):
        invalid_ids_df = pd.read_csv(invalid_ids_path)
        return invalid_ids_df['id'].tolist()
    else:
        raise FileNotFoundError(f"{invalid_ids_path} not found.")

async def filter_invalid_ids(final_dataset_path, invalid_ids):
    """
    Loads the final dataset and removes the invalid IDs asynchronously.
    Returns a DataFrame with the filtered dataset.
    """
    final_data_df = pd.read_csv(final_dataset_path)
    filtered_df = final_data_df[~final_data_df['id'].isin(invalid_ids)]
    return filtered_df

async def prepare_text_data(filtered_df):
    """
    Prepares the text dataset by combining columns and filling NaN values asynchronously.
    Returns the processed DataFrame.
    """
    # Specify the columns to keep
    columns_to_keep = ['id', 'headline', 'addresses', 'textFree', 'textEstate', 'textLocation', 'typeoflocation', 'access']
    filtered_df = filtered_df.loc[:, columns_to_keep]

    # Replace NaN values with an empty string
    filtered_df.fillna(',', inplace=True)

    # Combine text fields together
    filtered_df['Combined_Text'] = filtered_df['headline'] + filtered_df['addresses'] + filtered_df['textFree'] + filtered_df['textEstate'] + filtered_df['textLocation'] + filtered_df['typeoflocation'] + filtered_df['access']

    return filtered_df

async def add_image_paths(filtered_df, image_output_folder):
    """
    Adds the image paths to the filtered DataFrame asynchronously.
    """
    filtered_df['Image'] = image_output_folder + filtered_df['id'] + "_image_1.jpg"
    return filtered_df

async def save_final_dataset(filtered_df, output_file):
    """
    Saves the final prepared dataset to a CSV file asynchronously.
    """
    filtered_df.to_csv(output_file, index=False)
    print(f"Final dataset saved to {output_file}")

async def prepare_and_save_dataset(token: str, company_name: str):
    """
    Main async function to load the final dataset, remove invalid IDs, prepare text and image data,
    and save the cleaned dataset to a CSV. Then, download images for the filtered dataset.
    """
    try:
        # Step 1: Define company-specific paths
        company_folder = os.path.join(settings.DATA_OUTPUT_FOLDER, company_name)
        os.makedirs(company_folder, exist_ok=True)
        final_dataset_path = os.path.join(company_folder, "final_dataset.csv")
        output_file = os.path.join(company_folder, "filtered_final_dataset.csv")
        image_output_folder = os.path.join(settings.IMAGE_OUTPUT_PATH, company_name)

        # Step 2: Load invalid IDs
        invalid_ids = await load_invalid_ids(company_name)
        
        # Step 3: Load final dataset and filter out invalid IDs
        filtered_df = await filter_invalid_ids(final_dataset_path, invalid_ids)
        
        # Step 4: Prepare text data
        filtered_df = await prepare_text_data(filtered_df)

        # Step 5: Add image paths
        filtered_df = await add_image_paths(filtered_df, image_output_folder + "/")

        # Step 6: Save the final prepared dataset
        await save_final_dataset(filtered_df, output_file)

        # Step 7: Download images for the filtered IDs
        await download_images_from_filtered_data(filtered_df, token, company_name)
    
    except Exception as e:
        print(f"Error during dataset preparation: {e}")
