import datetime
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
        result = self.processor.process_single_pdf(pdf_path)
        return result

    # Test for case_number in both PDFs
    def test_case_number(self):
        # Arrowhead PDF
        pdf_path = self.test_files["Arrowhead"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Case Number"], "13PRE0212")

        # BMS PDF
        pdf_path = self.test_files["BMS"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Case Number"], "24PDE0353")

    def test_total_votes(self):
        # Arrowhead PDF
        pdf_path = self.test_files["Arrowhead"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Total Votes"], 109)

        # BMS PDF
        pdf_path = self.test_files["BMS"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Total Votes"], 20)

    def test_document_date(self):
        # Arrowhead PDF
        pdf_path = self.test_files["Arrowhead"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Document Date"], datetime.date(2012, 11, 7))

        # BMS PDF
        pdf_path = self.test_files["BMS"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Document Date"], datetime.date(2023, 11, 7))

    def test_issue_date(self):
        # Arrowhead PDF
        pdf_path = self.test_files["Arrowhead"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Issuance Date"], datetime.date(2012, 9, 17))

        # BMS PDF
        pdf_path = self.test_files["BMS"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Issuance Date"], datetime.date(2023, 9, 11))

    # def test_unit_name(self):
    #     # Arrowhead PDF
    #     pdf_path = self.test_files["Arrowhead"]
    #     result = self.process_pdf(pdf_path)
    #     self.assertEqual(result["Unit Name"], "All employees employed by the Arrowhead Regional Corrections Board, Duluth, Minnesota, who are public employees within the meaning of Minn. Stat. 179A.03, subd. 14, excluding supervisory, confidential and essential employees.")
    #
    #     # BMS PDF
    #     pdf_path = self.test_files["BMS"]
    #     result = self.process_pdf(pdf_path)
    #     self.assertEqual(result["Issue Date"], "All employees of Independent School District No. 2159, ... FILL IN")

    # Test for group_1 in both PDFs
    def test_group_1_name(self):
        # Arrowhead PDF
        pdf_path = self.test_files["Arrowhead"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Group 1"], "MINNESOTA PUBLIC EMPLOYEES ASSOCIATION")

        # BMS PDF
        pdf_path = self.test_files["BMS"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Group 1"], "AMERICAN FEDERATION OF STATE, COUNTY AND MUNICIPAL EMPLOYEES, COUNCIL 65")

    # Test for num_votes_group_1 in both PDFs
    def test_num_votes_group_1(self):
        # Arrowhead PDF
        pdf_path = self.test_files["Arrowhead"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Group 1 Votes"], 55)

        # BMS PDF
        pdf_path = self.test_files["BMS"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Group 1 Votes"], 6)

    # Test for group_2 in both PDFs
    def test_group_2_name(self):
        # Arrowhead PDF
        pdf_path = self.test_files["Arrowhead"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Group 2"], "AFSCME MINNESOTA COUNCIL 5")

        # BMS PDF
        pdf_path = self.test_files["BMS"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Group 2"], None)

    # Test for num_votes_group_2 in both PDFs
    def test_num_votes_group_2(self):
        # Arrowhead PDF
        pdf_path = self.test_files["Arrowhead"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Group 2 Votes"], 54)

        # BMS PDF
        pdf_path = self.test_files["BMS"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Group 2 Votes"], None)

    # Test for num_votes_no_rep in both PDFs
    def test_num_votes_no_rep(self):
        # Arrowhead PDF
        pdf_path = self.test_files["Arrowhead"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["No Representative Votes"], None)

        # BMS PDF
        pdf_path = self.test_files["BMS"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["No Representative Votes"], 14)

    # Test for total_votes_tabulated in both PDFs
    def test_total_votes_tabulated(self):
        # Arrowhead PDF
        pdf_path = self.test_files["Arrowhead"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Total Votes"], 109)

        # BMS PDF
        pdf_path = self.test_files["BMS"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Total Votes"], 20)

    def test_result(self):
        # Arrowhead PDF
        pdf_path = self.test_files["Arrowhead"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Result"], "MINNESOTA PUBLIC EMPLOYEES ASSOCIATION")
        self.assertEqual(result["Chose Representative"], True)

        # BMS PDF
        pdf_path = self.test_files["BMS"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Result"], None)
        self.assertEqual(result["Chose Representative"], False)

    def test_petition_type(self):
        # Arrowhead PDF
        pdf_path = self.test_files["Arrowhead"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Petition Type"], "DETERMINATION OF AN APPROPRIATE UNIT AND CERTIFICATION AS EXCLUSIVE REPRESENTATIVE")

        # BMS PDF
        pdf_path = self.test_files["BMS"]
        result = self.process_pdf(pdf_path)
        self.assertEqual(result["Petition Type"], "DECERTIFICATION AS EXCLUSIVE REPRESENTATIVE")

    # def test_chose_law_enforcement_union(self):
    #     pdf_path = self.test_files["Arrowhead"]
    #     result, _ = self.process_pdf(pdf_path)
    #     self.assertEqual(result["Chose Law Enforcement Union"], False)
    #
    #     # BMS PDF
    #     pdf_path = self.test_files["BMS"]
    #     result, _ = self.process_pdf(pdf_path)
    #     self.assertEqual(result["Chose Law Enforcement Union"], False)

        # print("NEED TO TEST WITH ONES THAT DO INCLUDE IT THOUGH")

    # ADD TESTS FOR RESULT, 0, 1, or 2
    # ADD TESTS FOR UNIT
    # ADD TESTS FOR IS LAW ENFORCEMENT UNION? or checking for that?
    # ADD TESTS FOR ISSUANCE DATE

    # ADD TESTS FOR PETITION TYPE
    # locatioon, unit name

if __name__ == "__main__":
    unittest.main()



    # CURRENTLY: CAN ONLY GET TEXT FROM SOME PDFS
