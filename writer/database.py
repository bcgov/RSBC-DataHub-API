from config import Config
import pyodbc as db
from abc import ABC, abstractmethod
import logging


class AbstractDatabase(ABC):

    
    def __init__(self, config):
        self.config = config
        logging.basicConfig(level=config.WRITER_LOG_LEVEL)
        logging.warning('*** database class initialized  ***')


    @abstractmethod 
    def insert(self, tablesToBeInserted: dict) -> bool:
        pass


class MsSQL(AbstractDatabase):


    def insert(self, tablesToBeInserted: dict ) -> dict:

        #Connect to database
        logging.warning('insert called')
        logging.warning(self.config.DB_HOST)
        connectionString = self._getDatabaseConnectionString(self.config)
        logging.debug(connectionString)
        connection = self._getDatabaseConnection(connectionString)
        cursor = connection.cursor()


        for table in tablesToBeInserted:
            
            insertStatement = "INSERT INTO {} ({}) VALUES ({})".format(
                    table['table'], 
                    ",".join(str(x) for x in table['columns']),
                    ",".join("?" for x in table['columns']))

            logging.warning(insertStatement)
            logging.warning(table['values'])

            try:
                cursor.executemany(insertStatement,table['values'])

            except Exception as error:
                errorString = error.__class__.__name__
                logging.warning("Write to db failed: " + errorString)
                logging.warning(str(error))

                return {
                    'isSuccessful': False,
                    'error_type': errorString,
                    'error_description': str(error)
                }

            connection.commit()

        cursor.close()
        connection.close()
        return { 'isSuccessful': True }


    def _getDatabaseConnection(self, connectionString):
        
        # Infinite loop until connection established

        while True:
            try:
                connection = db.connect(connectionString)
                return connection
            except Exception as error:
                logging.warning("Unable to connect")
                logging.warning(str(error))




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