import main
import unittest
import csv
from main import processReads
from main import Loci
from main import Read

class TestMethods(unittest.TestCase):
    # tests sample input files in processReads against expected output
    def test_processReads(self):
        processReads('test_reads1.csv', 'test_loci1.csv', 'test_loci2.csv')
        with open('test_loci2.csv') as output_file:
            reader = csv.reader(output_file, delimiter=',')
            next(reader)
            loci_list = []
            for row in reader:
                loci = Loci(int(row[0]))
                loci.coverage = int(row[1])
                loci_list.append(loci)
            loci_list.sort()
            self.assertEqual(loci_list[0].position, 1)
            self.assertEqual(loci_list[0].coverage, 1)
            self.assertEqual(loci_list[1].position, 2)
            self.assertEqual(loci_list[1].coverage, 2)
            self.assertEqual(loci_list[2].position, 3)
            self.assertEqual(loci_list[2].coverage, 2)
            self.assertEqual(loci_list[3].position, 7)
            self.assertEqual(loci_list[3].coverage, 2)

if __name__ == '__main__':
    unittest.main()