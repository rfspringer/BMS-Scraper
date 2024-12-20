import os
import re
import csv
import logging
from typing import List, Dict, Union
import pytesseract
from pdf2image import convert_from_path
from datetime import datetime
from pathlib import Path
import pandas as pd


class PDFDataProcessor:
    def __init__(self, log_level=logging.INFO):
        """
        Initialize the processor with optional logging and regex patterns.

        Args:
            log_level (int): Logging level, defaults to INFO
        """
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # Compile regex patterns for efficiency
        self.patterns = self._compile_patterns()

    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """
        Compile regex patterns used for extracting specific information from the PDFs.

        Returns:
            dict: Dictionary containing compiled regex patterns for various fields.
        """
        return {
            'Unit Name': re.compile(r'(?:falling\s+within\s+the\s+appropriate\s+unit\s*(?:of)?:|Page Two\s*)\s*(?:[^A]\d{3}.*?\n)*?(All.*?)(?=(?:The Maintenance|STATE OF MINNESOTA|An Equal Opportunity|Commissioner|1380))', re.DOTALL),            'Case Number': re.compile(r'BMS Case No\. (\S+)'),
            'Num. Eligible Employees': re.compile(r'ELIGIBLE EMPLOYEES \((\d+)\)'),
            'Total Votes': re.compile(r'TOTAL VOTES TABULATED \((\d+)\)'),
            'Document Date': re.compile(r'(\w+ \d{1,2}, \d{4})'),
            'Issuance Date': re.compile(r'issued by the Bureau on (\w+ \d{1,2}, \d{4})'),
            'Petition Type': re.compile(r'IN THE MATTER OF A PETITION FOR\s+(.*?)(?=\s+\b[A-Za-z]+\s+\d{1,2}, \d{4}\b)', re.DOTALL),
        }

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from a PDF using OCR.

        Args:
            pdf_path (str): Path to the PDF file.

        Returns:
            str: Extracted text from the PDF.
        """
        images = convert_from_path(pdf_path)
        full_text = ""

        for page_number, image in enumerate(images, start=1):
            page_text = pytesseract.image_to_string(image)
            if page_text.strip():
                full_text += page_text + "\n"
            else:
                self.logger.warning(f"No text extracted from page {page_number}")

        return full_text

    def _clean_extracted_patterns(self, text: str, key):
        text = re.sub(r'\n+', ' ', text)  # Replace multiple newlines with a single space
        text = re.sub(r' +', ' ', text)  # Replace multiple spaces with a single space

        # Convert numeric values to int if applicable
        if text.isdigit():
            return int(text)
        # Convert dates to a standard format if applicable
        elif key in {'Document Date', 'Issuance Date'}:
            try:
                return datetime.strptime(text, '%B %d, %Y').date()
            except ValueError:
                pass  # Leave the value as is if parsing fails

        return text

    def _get_unit_location_from_unit_name(self, unit_name_text: str):
        pattern = re.compile(
            r'\b([A-Za-z\s\-]+,\s*Minnesota)\b',
            re.IGNORECASE | re.DOTALL
        )
        match = pattern.search(unit_name_text)
        if match:
            location = match.group(1).strip()
            location = self._clean_extracted_patterns(location, 'Unit Location')
            return location
        else:
            return None

    def _extract_matching_patterns(self, text: str) -> Dict[str, Union[str, int]]:
        """
        Extract specific matching patterns from the text using regex patterns.

        Args:
            text (str): Extracted text from the PDF.

        Returns:
            dict: Dictionary of extracted values.
        """
        results = {}

        for key, pattern in self.patterns.items():
            match = pattern.search(text)
            if match:
                value = match.group(1).strip()
                value = self._clean_extracted_patterns(value, key)
                results[key] = value

        if 'Unit Name' in results:
            results['Unit Location'] = self._get_unit_location_from_unit_name(results['Unit Name'])
        else:
            pass
        return results

    def _extract_voting_results(self, text: str) -> Dict[str, Union[str, int]]:
        """
        Extract voting results from the text.

        Args:
            text (str): Extracted text from the PDF.

        Returns:
            dict: Dictionary containing voting results.
        """
        voting_section_match = re.search(r'ELIGIBLE EMPLOYEES\s*\((\d+)\)(.*?)TOTAL VOTES TABULATED', text, re.DOTALL)
        if not voting_section_match:
            return {}

        voting_section = voting_section_match.group(2).replace('\n', ' ').strip()
        vote_pattern = r'(.*?)\s*\(\s*(\d+)\s*\)'

        votes = re.findall(vote_pattern, voting_section)
        result = {f'Group {i}': None for i in range(1, 4)}
        result.update({f'Group {i} Votes': None for i in range(1, 4)})
        result['No Representative Votes'] = None

        group_index = 1
        for group, vote_count in votes:
            group = group.strip()
            group = re.sub(r'^VOTES FOR\s*', '', group, flags=re.IGNORECASE)

            if 'no representative' in group.lower():
                result['No Representative Votes'] = int(vote_count)
                break
            else:
                result[f'Group {group_index}'] = group
                result[f'Group {group_index} Votes'] = int(vote_count)
                group_index += 1

        return result

    def _extract_representation_results(self, text: str) -> Dict[str, Union[str, bool]]:
        """
        Extract the representation status and group name from the text.

        Args:
            text (str): Extracted text from the PDF.

        Returns:
            dict: Dictionary containing representation results.
        """
        pattern = re.compile(
            r'CERTIFIED\s+THAT\s+(.*?)\s*,?\s*is?\s*(NOT\s+)?\s*the\s+exclusive\s+representative',
            re.IGNORECASE | re.DOTALL
        )
        match = pattern.search(text)

        if match:
            group_name = match.group(1).strip().replace("\n", " ").split(',', 1)[0].strip()
            is_exclusive = match.group(2) is None
            return {
                "Chose Representative": is_exclusive,
                "Result": group_name if is_exclusive else 'No Representative'
            }

        return {}

    def _get_pdf_link(self, pdf_path):
        file_name = Path(pdf_path).name
        return 'https://mn.gov/bms/assets/' + file_name

    def process_single_pdf(self, pdf_path: str) -> Dict[str, Union[str, int]]:
        """
        Process a single PDF and extract data.

        Args:
            pdf_path (str): Path to the PDF file.

        Returns:
            dict: Extracted data.
        """
        text = self._extract_text_from_pdf(pdf_path)
        results = {}

        results['PDF Link'] = self._get_pdf_link(pdf_path)
        results.update(self._extract_matching_patterns(text))
        results.update(self._extract_voting_results(text))
        results.update(self._extract_representation_results(text))

        return results

    def process_pdfs_in_folder(self, folder_path: str) -> List[Dict[str, Union[str, int]]]:
        """
        Process all PDFs in a folder and extract data.

        Args:
            folder_path (str): Path to the folder containing PDFs.

        Returns:
            list: List of dictionaries containing election data from each PDF.
        """
        pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
        all_results = []

        for pdf_file in pdf_files:
            pdf_path = os.path.join(folder_path, pdf_file)
            self.logger.info(f"Processing file: {pdf_file}")
            result = self.process_single_pdf(pdf_path)
            all_results.append(result)

        return all_results

    def save_results_to_csv(self, results: List[Dict[str, Union[str, int]]], output_file: str) -> None:
        """
        Save the extracted results to a CSV file.

        Args:
            results (list): List of dictionaries containing extracted election data.
            output_file (str): Path to the CSV file to save the results.

        Returns:
            None
        """
        if not results:
            self.logger.warning("No results to save.")
            return

        headers = ['Case Number', 'Document Date', 'Unit Name', 'Unit Location', 'Petition Type', 'Issuance Date',
                   'Num. Eligible Employees', 'Group 1', 'Group 2', 'Group 3', 'Group 1 Votes', 'Group 2 Votes', 'Group 3 Votes',
                   'No Representative Votes', 'Total Votes', 'Result', 'Chose Representative', 'PDF Link']

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(results)

        # Ensure that all the necessary columns are in the DataFrame (fill missing columns with empty strings or None)
        for header in headers:
            if header not in df.columns:
                df[header] = None

        # Reorder columns to match the header list
        df = df[headers]

        # Write to CSV
        df.to_csv(output_file, index=False, encoding='utf-8')

        self.logger.info(f"Results saved to {output_file}")


def main():
    folder_path = './downloads'
    processor = PDFDataProcessor()

    results = processor.process_pdfs_in_folder(folder_path)
    processor.save_results_to_csv(results, 'outputs.csv')


    for result in results:
        print(result)


if __name__ == "__main__":
    main()


    # RUN ALL INTO DOC
