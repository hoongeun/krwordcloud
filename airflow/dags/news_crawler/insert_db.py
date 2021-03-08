import platform
import os
import sys
from pyhive import hive
from exceptions import *

class Database(object):
    def __init__(self):
        self.conn = hive.Connection(host="localhost", port=10000, username="hive", password='hive', database="news", auth="CUSTOM")
        print ('db is opened')
        self.cursor = self.conn.cursor()
        
    def initialize_data(self, data_dir, category_name, date, file_name, hash_name):
        self.date = date
        self.category_name = category_name
        self.path = os.path.join(data_dir, 'output', self.category_name+'_'+self.date.strftime('%Y%m%d')+'.tsv')
        self.hash_path = os.path.join(data_dir, 'output', self.category_name+'_'+self.date.strftime('%Y%m%d')+'.sha1')
        
    def checker(self):
        self.cursor.execute("SELECT hash_data FROM Verify_Table WHERE news_date = '"+str(self.date)+"' and category = '"+self.category_name+"'")
        if self.cursor.fetchall():
            return True
        else:
            return False
        
    def data_insert(self):
        self.cursor.execute("SELECT * FROM Article_Table WHERE news_date = '"+str(self.date)+"' and category = '"+self.category_name+"'")
        if self.cursor.fetchall():
        	self.cursor.execute("DELETE * FROM Article_Table WHERE news_date = '"+str(self.date)+"' and category ='"+self.category_name+"'")
        print ('start input file data to db')
        self.cursor.execute("load data local inpath '"+self.path+"' into table Article_Table")
        #self.cursor.execute("INSERT INTO Article_Table VALUES ('"+self.date+"', '"+self.category_name+"', '"+data.written_times+"', '"+data.times_name+"', '"+data.headline+"', '"+data.contents+"', '"+data.url+"'") 
    
    def hash_insert(self):
        print ('start input hash data to db')
        self.cursor.execute("load data local inpath '"+self.hash_path+"' into table Verify_Table")
        #self.cursor.execute("INSERT INTO Verify_Table VALUES ('"+self.date+"', '"+self.category_name+"', '"+data.hash+"', '"+data.size+"'")
