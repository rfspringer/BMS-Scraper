import unittest
from PDFDataProcessor import PDFDataProcessor

class TestElectionDataProcessor(unittest.TestCase):

    def setUp(self):
        """
        Set up the ElectionDataProcessor and test files for each test case.
        """
        self.processor = PDFDataProcessor()
        self.test_files = {
            "Arrowhead": "downloads/13PRE0212-Arrowhead_tcm1075-237291.pdf",
            "BMS": "downloads/BMS Case No. 24PDE0353_tcm1075-614651.pdf"
        }

    def process_pdf(self, pdf_path):
        """
        Helper function to process a PDF and return the result.
        """
        failed_pdfs = []
        result = self.processor.process_single_pdf(pdf_path, failed_pdfs)
        return result, failed_pdfs

    # Test for case_number in both PDFs
    def test_case_number(self):
        # Arrowhead PDF
        pdf_path = self.test_files["Arrowhead"]
        result, _ = self.process_pdf(pdf_path)
        self.assertEqual(result["case_number"], "13PRE0212")

        # BMS PDF
        pdf_path = self.test_files["BMS"]
        result, _ = self.process_pdf(pdf_path)
        self.assertEqual(result["case_number"], "24PDE0353")

    # Test for group_1 in both PDFs
    def test_group_1(self):
        # Arrowhead PDF
        pdf_path = self.test_files["Arrowhead"]
        result, _ = self.process_pdf(pdf_path)
        self.assertEqual(result["group_1"], "MINNESOTA PUBLIC EMPLOYEES ASSOCIATION")

        # BMS PDF
        pdf_path = self.test_files["BMS"]
        result, _ = self.process_pdf(pdf_path)
        self.assertEqual(result["group_1"], "AMERICAN FEDERATION OF STATE, COUNTY AND MUNICIPAL EMPLOYEES, COUNCIL 65")

    # Test for num_votes_group_1 in both PDFs
    def test_num_votes_group_1(self):
        # Arrowhead PDF
        pdf_path = self.test_files["Arrowhead"]
        result, _ = self.process_pdf(pdf_path)
        self.assertEqual(result["num_votes_group_1"], 55)

        # BMS PDF
        pdf_path = self.test_files["BMS"]
        result, _ = self.process_pdf(pdf_path)
        self.assertEqual(result["num_votes_group_1"], 6)

    # Test for group_2 in both PDFs
    def test_group_2(self):
        # Arrowhead PDF
        pdf_path = self.test_files["Arrowhead"]
        result, _ = self.process_pdf(pdf_path)
        self.assertEqual(result["group_2"], "AFSCME MINNESOTA COUNCIL 5")

        # BMS PDF
        pdf_path = self.test_files["BMS"]
        result, _ = self.process_pdf(pdf_path)
        self.assertEqual(result["group_2"], None)

    # Test for num_votes_group_2 in both PDFs
    def test_num_votes_group_2(self):
        # Arrowhead PDF
        pdf_path = self.test_files["Arrowhead"]
        result, _ = self.process_pdf(pdf_path)
        self.assertEqual(result["num_votes_group_2"], 54)

        # BMS PDF
        pdf_path = self.test_files["BMS"]
        result, _ = self.process_pdf(pdf_path)
        self.assertEqual(result["num_votes_group_2"], None)

    # Test for num_votes_no_rep in both PDFs
    def test_num_votes_no_rep(self):
        # Arrowhead PDF
        pdf_path = self.test_files["Arrowhead"]
        result, _ = self.process_pdf(pdf_path)
        self.assertEqual(result["num_votes_no_rep"], 0)

        # BMS PDF
        pdf_path = self.test_files["BMS"]
        result, _ = self.process_pdf(pdf_path)
        self.assertEqual(result["num_votes_no_rep"], 14)

    # Test for total_votes_tabulated in both PDFs
    def test_total_votes_tabulated(self):
        # Arrowhead PDF
        pdf_path = self.test_files["Arrowhead"]
        result, _ = self.process_pdf(pdf_path)
        self.assertEqual(result["total_votes_tabulated"], 109)

        # BMS PDF
        pdf_path = self.test_files["BMS"]
        result, _ = self.process_pdf(pdf_path)
        self.assertEqual(result["total_votes_tabulated"], 20)

    # ADD TESTS FOR RESULT, 0, 1, or 2
    # ADD TESTS FOR UNIT
    # ADD TESTS FOR IS LAW ENFORCEMENT UNION
    # ADD TESTS FOR ISSUANCE DATE
    # ADD TESTS FOR PETITION TYPE

if __name__ == "__main__":
    unittest.main()
