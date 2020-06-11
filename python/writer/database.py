import pyodbc as db
import logging


class MsSQL:

    def __init__(self, config):
        self.config = config
        logging.basicConfig(level=config.LOG_LEVEL)
        logging.warning('*** database class initialized  ***')

    def insert(self, tables_to_be_inserted: dict) -> dict:
        # Connect to database
        logging.info('insert called')
        logging.info(self.config.DB_HOST)
        connection_string = self._get_database_connection_string(self.config)
        logging.debug(connection_string)
        connection = self._get_database_connection(connection_string)
        cursor = connection.cursor()

        for table in tables_to_be_inserted:
            insert_statement = "INSERT INTO {} ({}) VALUES ({})".format(
                    table['table'], 
                    ",".join(str(x) for x in table['columns']),
                    ",".join("?" for x in table['columns']))

            logging.info(insert_statement)
            logging.info(table['values'])

            try:
                cursor.execute(insert_statement, table['values'])
            except Exception as error:
                error_string = error.__class__.__name__
                logging.warning("Write to db failed: " + error_string)
                logging.warning(str(error))

                return {
                    'isSuccessful': False,
                    'error_type': error_string,
                    'error_description': str(error)
                }

        connection.commit()

        cursor.close()
        connection.close()
        return {'isSuccessful': True}

    @staticmethod
    def _get_database_connection(connection_string):
        # Infinite loop until connection established
        while True:
            try:
                connection = db.connect(connection_string)
                return connection
            except Exception as error:
                logging.warning("Unable to connect")
                logging.warning(str(error))

    @staticmethod
    def _get_database_connection_string(config):
        return "DRIVER={{{}}};SERVER={};DATABASE={};UID={};PWD={}".format(
            config.ODBC_DRIVER,
            config.DB_HOST, 
            config.DB_NAME, 
            config.DB_USERNAME, 
            config.DB_PASSWORD
        )

    @staticmethod
    def _wrap_strings_with_quotes(value):
        """
            SQL server insert statements wrap quotes around strings
            but omit quotes if numbers.
        :param value:
        :return:
        """
        if str(type(value)) == "<class 'str'>":
            return "'{}'".format(value)
        return str(value)
