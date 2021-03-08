#only use test
import csv
import platform
import os
import sys

class Writer(object):
    def __init__(self, category_name, crawling_date):
        self.category_name = category_name
        self.crawling_date = crawling_date
        self.dir = os.path.join(os.getcwd(), "..", "..", "output")

    def initialize_file(self, category_name, date, write_row_handler=None, write_meta_handler=None):
        self.write_row_handler = write_row_handler
        self.write_meta_handler = write_meta_handler
        
        self.file_name = os.path.join(self.dir, f"{self.category_name}_{self.crawling_date.strftime('%Y%m%d')}.tsv")

        self.file_open = 0
        self.file_size = 0
        
        if os.path.exists(self.dir) is not True:
            os.mkdir(self.dir)
            
        self.file = open(self.file_name, 'a+', encoding='utf-8', newline='')
        self.file_open = 1
        self.tsv_writer = csv.writer(self.file, delimiter='\t')

    def write_row(self, row):
        for col in row:
            self.file_size += sys.getsizeof(col)

        self.tsv_writer.writerow(row)
        self.write_row_handler = row
        
        self.file_size -= sys.getsizeof('\n')
    
    #For file close 
    def is_open(self):
        return self.file_open
        
    def get_row_handler(self):
        return self.write_row_handler
        
    def get_meta_handler(self):
        return self.write_meta_handler

    #assert가 더 나은가?
    def close(self):
        #assert self.file.close()
        if self.is_open():
            self.file.close()
            self.file_open = 0
            self.file = None
