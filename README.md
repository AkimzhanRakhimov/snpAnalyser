# SNPAnalyzer

## Overview
SNPAnalyzer is a Python tool designed to parse, filter, and export SNP (Single Nucleotide Polymorphism) data from VCF (Variant Call Format) files. It uses the `pysam` library to handle genomic data and `pandas` for data manipulation.

## Features
- Parses VCF files to extract SNP data (chromosome, position, reference, alternative, quality, filter).
- Filters SNPs based on quality scores.
- Saves the results as a CSV file.

## Requirements
This script is designed to run on **WSL (Windows Subsystem for Linux)**. It won't work directly on native Windows.

### Dependencies
- Python 3
- `pysam`
- `pandas`

## Installation

### 1. Install WSL
1. Open **PowerShell** as Administrator and run:
    ```bash
    wsl --install
    ```
    This installs Ubuntu and WSL.

2. Restart your computer.

3. Launch **Ubuntu** from the Start Menu.

4. Update your packages:
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```

### 2. Install Python and packages
1. Install Python and pip:
    ```bash
    sudo apt install python3 python3-pip -y
    ```

2. Install required libraries:
    ```bash
    pip install pysam pandas
    ```

### 3. Clone the repository
    ```bash
    git clone https://github.com/YourUsername/SNPAnalyzer.git
    cd SNPAnalyzer
    ```

## Usage

### 1. Run the script
```bash
python3 snp_analyzer.py
```

### 2. Example
If your VCF file is named `example.vcf`, the script will:
- Parse the file
- Filter SNPs with a quality threshold of 30
- Save results to `snp_results.csv`

```bash
python3 snp_analyzer.py
```

## Code Breakdown

### Class Initialization
```python
class SNPAnalyzer:
    def __init__(self, vcf_file):
        self.vcf_file = vcf_file
        self.variants = []
```
- Initializes the analyzer with the path to a VCF file.
- Prepares an empty list to store parsed variants.

### VCF Parsing
```python
    def parse_vcf(self):
        vcf_reader = pysam.VariantFile(self.vcf_file)
        for record in vcf_reader:
            variant = {
                'Chromosome': record.chrom,
                'Position': record.pos,
                'Reference': record.ref,
                'Alternative': ','.join(map(str, record.alts)),
                'Quality': record.qual if record.qual is not None else 0,
                'Filter': ','.join(record.filter.keys()) if record.filter else 'PASS'
            }
            self.variants.append(variant)
```
- Reads each record in the VCF file.
- Extracts chromosome, position, reference allele, alternative alleles, quality, and filter status.
- If no quality is given, defaults to 0.

### Filtering SNPs
```python
    def filter_snps(self, min_quality=20):
        df = pd.DataFrame(self.variants)
        df['Quality'] = pd.to_numeric(df['Quality'], errors='coerce')
        return df[df['Quality'] >= min_quality]
```
- Converts data to a DataFrame.
- Filters SNPs based on a minimum quality score (default 20).

### Saving Results
```python
    def save_results(self, output_file='snp_results.csv'):
        df = pd.DataFrame(self.variants)
        df.to_csv(output_file, index=False, sep=';', encoding='utf-8')
```
- Saves parsed and filtered SNP data to a CSV file with `;` as the delimiter.

### Error Handling
```python
try:
    data = snp_analyzer.parse_vcf()
    print("Total variants:", len(data))
    filtered_data = snp_analyzer.filter_snps(min_quality=30)
    print("Filtered variants:", len(filtered_data))
    snp_analyzer.save_results()
except Exception as e:
    print(f"An error occurred: {e}")
```
- Catches errors like missing files or invalid data and reports them gracefully.

## License
This project is licensed under the MIT License.



