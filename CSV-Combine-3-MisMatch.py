import os
import pandas as pd

def combine_csv_files(input_folder, output_filename):
    # List all CSV files in the input folder
    csv_files = [file for file in os.listdir(input_folder) if file.endswith('.csv')]

    if not csv_files:
        print("No CSV files found in the specified folder.")
        return

    # Initialize an empty list to store DataFrames
    data_frames = []

    # Iterate through each CSV file and append its data to the list
    for csv_file in csv_files:
        file_path = os.path.join(input_folder, csv_file)
        df = pd.read_csv(file_path, header=None)
        data_frames.append(df)

    # Find the maximum number of columns among all DataFrames
    max_columns = max(df.shape[1] for df in data_frames)

    # Fill missing columns with NaN and concatenate DataFrames
    combined_data = pd.concat([df.reindex(columns=range(max_columns)) for df in data_frames], ignore_index=True)

    # Save the combined data to a new CSV file
    output_path = os.path.join(input_folder, output_filename)
    combined_data.to_csv(output_path, index=False, header=False)  # No header in the output file

    print(f"Data has been successfully combined and saved to '{output_filename}'.")

if __name__ == "__main__":
    # Get input folder and output filename from the user
    input_folder = input("Enter the path to the folder containing CSV files: ")
    output_filename = input("Enter the desired name for the combined CSV file (including .csv extension): ")

    # Call the function to combine CSV files
    combine_csv_files(input_folder, output_filename)
