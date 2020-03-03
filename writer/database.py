from config import Config
import pyodbc as db
from abc import ABC, abstractmethod
import logging


class AbstractDatabase(ABC):

    
    def __init__(self, config):
        self.config = config
        logging.warning('*** database class initialized  ***')


    @abstractmethod 
    def insert(self, tablesToBeInserted: dict) -> bool:
        pass


class MsSQL(AbstractDatabase):


    def insert(self, tablesToBeInserted: dict):

        #Connect to database
        connectionString = self._getDatabaseConnectionString(self.config)
        logging.warning(connectionString)
        connection = db.connect(connectionString)
        cursor = connection.cursor()

        #Add try / catch logic here


        for table in tablesToBeInserted:
            
            insertStatement = "INSERT INTO {} ({}) VALUES ({})".format(
                    table['table'], 
                    ",".join(str(x) for x in table['columns']),
                    ",".join("?" for x in table['columns']))

            logging.warning(insertStatement)
            logging.warning(table['values'])
            cursor.executemany(insertStatement,table['values'])
            connection.commit()


        cursor.close()
        connection.close()



    def _getDatabaseConnectionString(self, config ):
        
        return "DRIVER={{{}}};SERVER={};DATABASE={};UID={};PWD={}".format(
            config.ODBC_DRIVER,
            config.DB_HOST, 
            config.DB_NAME, 
            config.DB_USERNAME, 
            config.DB_PASSWORD
        )


    def _wrapStringsWithQuotes(self, value):
        # SQL server insert statements wrap quotes around strings 
        # but omit quotes if for numbers.

        if(str(type(value)) == "<class 'str'>"):
            return "'{}'".format(value)

        return str(value)