import os
import re
import pandas as pd
import PyPDF2
from typing import List, Dict, Union
import logging
import camelot


class PDFDataProcessor:
    def __init__(self, log_level=logging.INFO):
        """
        Initialize the processor with optional logging.

        Args:
            log_level (int): Logging level, defaults to INFO
        """
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # Compile regex patterns for efficiency
        self.patterns = {
            'case_number': re.compile(r'BMS Case No\. (\S+)'),
            'eligible_employees': re.compile(r'ELIGIBLE EMPLOYEES \((\d+)\)'),
            'total_votes': re.compile(r'TOTAL VOTES TABULATED \((\d+)\)'),
            'date': re.compile(r'(\w+ \d{1,2}, \d{4})')
        }

    def extract_table(self, pdf_path: str) -> pd.DataFrame:
        """
        Extract tables from the PDF file.

        Args:
            pdf_path (str): Path to the PDF file

        Returns:
            pd.DataFrame: DataFrame containing extracted table data
        """
        try:
            tables = camelot.read_pdf(pdf_path, pages="all", flavor="stream")  # Change flavor to "lattice" if PDF has gridlines
            if tables:
                self.logger.info(f"Extracted {len(tables)} tables from {pdf_path}")
                # Combine all tables into a single DataFrame
                combined_table = pd.concat([table.df for table in tables], ignore_index=True)
                return combined_table
            else:
                self.logger.warning(f"No tables found in {pdf_path}")
                return pd.DataFrame()
        except Exception as e:
            self.logger.error(f"Error extracting tables from {pdf_path}: {e}")
            return pd.DataFrame()

    def parse_votes_from_table(self, table: pd.DataFrame) -> Dict[str, Union[str, int]]:
        """
        Parse vote information from the extracted table.

        Args:
            table (pd.DataFrame): DataFrame containing the table data

        Returns:
            Dict: Parsed vote information
        """
        votes_data = {
            'group_1': '',
            'group_2': '',
            'num_votes_group_1': 0,
            'num_votes_group_2': 0,
            'num_votes_no_rep': 0
        }

        # Iterate over rows and look for vote-related information
        for _, row in table.iterrows():
            row_text = " ".join(row.astype(str)).lower()
            if "votes for" in row_text:
                group_name = re.search(r'votes for (.+?) \(\d+\)', row_text)
                votes_count = re.search(r'\((\d+)\)', row_text)

                if group_name and votes_count:
                    group_name = group_name.group(1).strip()
                    votes_count = int(votes_count.group(1))
                    if "no representative" in group_name.lower():
                        votes_data['num_votes_no_rep'] = votes_count
                    elif not votes_data['group_a']:
                        votes_data['group_a'] = group_name
                        votes_data['num_votes_group_1'] = votes_count
                    elif not votes_data['group_b']:
                        votes_data['group_b'] = group_name
                        votes_data['num_votes_group_2'] = votes_count

        return votes_data

    def process_single_pdf(self, pdf_path: str, failed_pdfs: List[str]) -> Dict[str, Union[str, int]]:
        """
        Process a single PDF file and extract election data.

        Args:
            pdf_path (str): Path to the PDF file
            failed_pdfs (List[str]): List to record failed PDFs

        Returns:
            dict: Extracted election data
        """
        try:
            table = self.extract_table(pdf_path)
            if table.empty:
                raise ValueError("No table data extracted")

            votes_data = self.parse_votes_from_table(table)

            # Combine results
            data = {
                'filename': os.path.basename(pdf_path),
                'case_number': self.extract_case_number(' '.join(table.astype(str).values.flatten())),
                'date': self.extract_issue_date(' '.join(table.astype(str).values.flatten())),
                'petition_type': 'Unknown',  # Adjust if you have logic to extract this
                **votes_data
            }

            self.logger.info(f"Successfully processed {pdf_path}")
            return data

        except Exception as e:
            self.logger.error(f"Error processing {pdf_path}: {e}")
            failed_pdfs.append(pdf_path)
            return {}

    def extract_case_number(self, text: str) -> str:
        match = self.patterns['case_number'].search(text)
        return match.group(1) if match else ''

    def extract_issue_date(self, text: str) -> str:
        match = self.patterns['date'].search(text)
        return match.group(1) if match else ''

    # Other helper functions remain the same

# Example usage
def main():
    processor = PDFDataProcessor()
    # Example: processor.process_single_pdf('/path/to/pdf', [])
    pass

if __name__ == "__main__":
    main()


    # mark if is "law enforcement union"
    # print last date

