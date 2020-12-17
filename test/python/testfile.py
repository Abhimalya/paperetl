"""
File tests
"""

import sqlite3

# pylint: disable=E0401
from paperetl.file.execute import Execute

from testprocess import TestProcess
from utils import Utils

class TestFile(TestProcess):
    """
    File tests
    """

    @classmethod
    def setUpClass(cls):
        """
        One-time initialization. Run File ETL process for the test dataset.
        """

        # Build articles database
        Execute.run(Utils.FILE + "/data", Utils.FILE + "/models", Utils.PATH + "/study")

    def setUp(self):
        """
        Initialization run before each test. Opens a database connection.
        """

        # Connect to articles database
        self.db = sqlite3.connect(Utils.FILE + "/models/articles.sqlite")

        # Create database cursor
        self.cur = self.db.cursor()

    def testArticleCount(self):
        """
        Test number of articles
        """

        self.articleCount(10)

    def testArticles(self):
        """
        Test article metadata
        """

        hashes = {"00398e4c637f5e5447e35e63669187f0239c0357": "3d33d69c9000a17a458d9295ab1e7457",
                  "00c4c8c42473d25ebb38c4a8a14200c6900be2e9": "0285f5accebeff1397fbdd5aa9ee51c4",
                  "17a845a8681cca77a4497462e797172148448d7d": "dcedb273321b4e936bcc0c7b8b85488c",
                  "1d6a755d67e76049551898de66c95f77b9420b0c": "0346bb2747c4d4c1e06284cdba67c5df",
                  "3d2fb136bbd9bd95f86fc49bdcf5ad08ada6913b": "54c9504e3b83b23cdd973d501528f5be",
                  "5ea7c57e339a078196ec69223c4681fd7a5aab8b": "e3374c8a38f198c136e553642ca4a747",
                  "6cb7a79749913fa0c2c3748cbfee2f654d5cea36": "ff7ef702bdc5908009c37bdb6b5fd1d5",
                  "a09f0fcf41e01f2cdb5685b5000964797f679132": "1ef532b4d24ce367f5a1600ee9c93bef",
                  "b9f6e3d2dd7d18902ac3a538789d836793dd48b2": "4f60700131c5015cee997b7a1b74948f",
                  "dff0088d65a56e2673d11ad2f7a180687cab6f70": "d6a6cf1830e6088b8e63fb897edc7a2c"}

        self.articles(hashes)

    def testSectionCount(self):
        """
        Test number of sections
        """

        self.sectionCount(3592)

    def testSections(self):
        """
        Test section content
        """

        hashes = {"00398e4c637f5e5447e35e63669187f0239c0357": "d6e428814a980bdbed5f50b2669f6785",
                  "00c4c8c42473d25ebb38c4a8a14200c6900be2e9": "cfd8bf5cffec86b836e497ac4973ea05",
                  "17a845a8681cca77a4497462e797172148448d7d": "422895ced816b2686ed4ea34c62e0f3a",
                  "1d6a755d67e76049551898de66c95f77b9420b0c": "644e14e17727715a205f1f92a5d98d83",
                  "3d2fb136bbd9bd95f86fc49bdcf5ad08ada6913b": "a3429b2fce7efa296282cf8923a37fe6",
                  "5ea7c57e339a078196ec69223c4681fd7a5aab8b": "4ec8a19839db5adf64c50b250d8c1081",
                  "6cb7a79749913fa0c2c3748cbfee2f654d5cea36": "d9f536cbca1abaab53682423d0b51af5",
                  "a09f0fcf41e01f2cdb5685b5000964797f679132": "f04bb10cd15dea0180e9ae610a8ada9a",
                  "b9f6e3d2dd7d18902ac3a538789d836793dd48b2": "79581ee4ec2f6b6339afba4df559c927",
                  "dff0088d65a56e2673d11ad2f7a180687cab6f70": "d214010dbae4fff941875b4dfe57ee71"}

        self.sections(hashes)
