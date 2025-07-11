# organize_tcga.py

import pandas as pd
import os

def map_stage_to_label(stage_text):
    """ Map tumor stage text to numerical class label. """
    if pd.isna(stage_text):
        return None  # if no stage info
    stage_text = stage_text.lower()
    if 'normal' in stage_text or 'no cancer' in stage_text:
        return 0
    elif 'stage i' in stage_text and not 'stage ii' in stage_text:
        return 1
    elif 'stage ii' in stage_text and not 'stage iii' in stage_text:
        return 2
    elif 'stage iii' in stage_text or 'stage iv' in stage_text:
        return 3
    else:
        return None  # optional: handle other cases

def organize_tcga_metadata():
    # Input and output paths
    input_file = os.path.join('..', 'data', 'tcga_brca', 'sampleMap_BRCA_clinicalMatrix.csv')
    output_dir = os.path.join('..', 'outputs')
    output_file = os.path.join(output_dir, 'tcga_brca_mapped_labels.csv')

    # Load metadata
    df = pd.read_csv(input_file)

    # Print available columns
    print("Original columns:", list(df.columns))

    # Find sample ID column
    if 'sampleID' in df.columns:
        sample_col = 'sampleID'
    elif 'bcr_sample_barcode' in df.columns:
        sample_col = 'bcr_sample_barcode'
    else:
        raise ValueError("No sample ID column found! Tried 'sampleID' and 'bcr_sample_barcode'.")

    # Find tumor stage column
    if 'AJCC_Stage_nature2012' in df.columns:
        stage_col = 'AJCC_Stage_nature2012'
    elif 'Converted_Stage_nature2012' in df.columns:
        stage_col = 'Converted_Stage_nature2012'
    elif 'ajcc_pathologic_stage' in df.columns:
        stage_col = 'ajcc_pathologic_stage'
    else:
        raise ValueError("No stage column found! Tried 'AJCC_Stage_nature2012', 'Converted_Stage_nature2012', 'ajcc_pathologic_stage'.")

    # Create output DataFrame
    df_out = pd.DataFrame()
    df_out['sample_id'] = df[sample_col]
    df_out['class_label'] = df[stage_col].apply(map_stage_to_label)

    # Drop rows where class_label could not be mapped
    df_out = df_out.dropna()

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save organized metadata
    df_out.to_csv(output_file, index=False)

    print(f"✅ Final mapped labels saved to: {output_file}")

if __name__ == "__main__":
    organize_tcga_metadata()