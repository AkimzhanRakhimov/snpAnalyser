import pysam
import pandas as pd

class SNPAnalyzer:
    def __init__(self, vcf_file):
        self.vcf_file = vcf_file
        self.variants = []

    def parse_vcf(self):
        """Parsing the VCF file using pysam"""
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

        # Convert the list of dictionaries to a DataFrame with explicit columns
        if not self.variants:
            raise ValueError("No data to parse from the VCF file.")
        
        columns = ['Chromosome', 'Position', 'Reference', 'Alternative', 'Quality', 'Filter']
        return pd.DataFrame(self.variants, columns=columns)

    def filter_snps(self, min_quality=20):
        """Filter SNPs based on quality"""
        df = pd.DataFrame(self.variants)
        df['Quality'] = pd.to_numeric(df['Quality'], errors='coerce')
        filtered_df = df[df['Quality'] >= min_quality]
        return filtered_df

    def save_results(self, output_file='snp_results.csv'):
        """Save the results to a CSV file with proper delimiter"""
        df = pd.DataFrame(self.variants)
        df.to_csv(output_file, index=False, sep=';', encoding='utf-8')

if __name__ == "__main__":
    snp_analyzer = SNPAnalyzer('example.vcf')
    try:
        data = snp_analyzer.parse_vcf()
        print("Total variants:", len(data))
        filtered_data = snp_analyzer.filter_snps(min_quality=30)
        print("Filtered variants:", len(filtered_data))
        snp_analyzer.save_results()
    except Exception as e:
        print(f"An error occurred: {e}")
