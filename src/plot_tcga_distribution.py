# plot_tcga_distribution.py

import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_distribution():
    # Path to the mapped labels CSV
    input_file = os.path.join('..', 'outputs', 'tcga_brca_mapped_labels.csv')

    # Load the data
    df = pd.read_csv(input_file)

    # Mapping numeric labels to text labels
    label_map = {
        0: 'Normal',
        1: 'Stage I',
        2: 'Stage II',
        3: 'Stage III/IV'
    }
    df['class_name'] = df['class_label'].map(label_map)

    # Plot
    counts = df['class_name'].value_counts()
    plt.figure(figsize=(8,6))
    counts.plot(kind='bar', color=['green', 'blue', 'orange', 'red'])
    plt.title('TCGA BRCA Dataset - Tumor Stage Distribution')
    plt.xlabel('Tumor Stage')
    plt.ylabel('Number of Samples')
    plt.grid(axis='y')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_distribution()
