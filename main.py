import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PyPDF2 import PdfReader
import re


class PDFScraper:
    def __init__(self, base_url="https://mn.gov/bms/representation/elections/", num_pages=9, download_folder="downloads"):
        self.base_url = base_url
        self.download_folder = download_folder
        self.pdf_urls = []  # Store the list of downloaded PDFs
        self.num_pages = num_pages

        # Create download folder if it doesn't exist
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)


    def fetch_page(self, page_num):
        """
        Fetches the HTML content of a specific page.
        """
        page_url = f"{self.base_url}/#/list/appId/1/filterType//filterValue//page/{page_num}/sort//order/"
        response = requests.get(page_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return BeautifulSoup(response.content, 'html.parser')

    def extract_pdf_urls(self, soup, base_url):
        """
        Extracts PDF URLs from the HTML content.
        """
        pdf_links = soup.find_all('a', href=True)
        return [urljoin(base_url, link['href']) for link in pdf_links if link['href'].endswith('.pdf')]

    def download_pdf(self, pdf_url):
        """
        Downloads a PDF from a given URL and saves it to the specified folder.
        """
        pdf_name = os.path.basename(pdf_url)
        pdf_path = os.path.join(self.download_folder, pdf_name)
        print(f"Downloading: {pdf_name}")

        response = requests.get(pdf_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        with open(pdf_path, 'wb') as pdf_file:
            pdf_file.write(response.content)
        print(f"Downloaded: {pdf_name}")
        return pdf_path

    def scrape(self):
        """
        Scrapes PDFs from multiple pages and saves them to the specified folder.
        """
        print(f"Total number of pages to scrape: {self.num_pages}")

        for page_num in range(1, self.num_pages + 1):
            print(f"Scraping pages {page_num}")
            soup = self.fetch_page(page_num)
            pdf_page_urls = self.extract_pdf_urls(soup, self.base_url)
            self.pdf_urls.extend(pdf_page_urls)

            for pdf_url in pdf_page_urls:
                self.download_pdf(pdf_url)

        print(f"All PDFs from {self.num_pages} pages have been downloaded.")

    # def parse_pdfs(self):
    #     """
    #     Parses the downloaded PDFs and extracts relevant data.
    #     """
    #
    #     return pdf_data

    def save_to_spreadsheet(self, data, output_file="output.csv"):
        """
        Save parsed data to a spreadsheet.
        """
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")


# Example usage:
base_url = "https://mn.gov/bms/representation/elections/"

# Create an instance of the PDFScraper class
scraper = PDFScraper(base_url, num_pages=9)

# Step 1: Scrape PDFs
scraper.scrape()

# # Step 2: Parse the downloaded PDFs into dictionaries
# pdf_data = scraper.parse_pdfs()
#
# # Step 3: Save the parsed data to a spreadsheet
# scraper.save_to_spreadsheet(pdf_data)
