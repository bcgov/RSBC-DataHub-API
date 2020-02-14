from config import Config
from abc import ABC, abstractmethod
import logging


class AbstractDatabase(ABC):

    
    def __init__(self, config):
        self.config = config
        logging.warning('*** database initialized  ***')


    @abstractmethod 
    def insert(self, tablesToBeInserted: dict) -> bool:
        pass




class MsSQL(AbstractDatabase):


    def insert(self, tablesToBeInserted: dict) -> bool:

        #Add try / catch logic here

        for table in tablesToBeInserted:
            logging.warning("INSERT INTO {} ({}) VALUES ({})".format(
                table['table'],
                ','.join(map(str, table['columns'])),
                ','.join(map(str, table['values']))
            )) 

        #If insert is successful, return true; otherwise false
        
    
  




