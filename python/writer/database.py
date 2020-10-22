import pyodbc as db
import logging
from python.writer.config import Config
from python.writer.mapper import Mapper
import python.common.message as msg

logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)


def write(**args):
    config = args.get('config')
    message = args.get('message')
    mapper = Mapper(config)
    tables_for_insert = mapper.convert_to_tables(message)
    is_successful, error = insert(config, tables_for_insert)
    if is_successful:
        return True, args
    logging.warning('database write failed: {}'.format(error))
    args['message'] = msg.add_error_to_message(message, error)
    return False, args


def insert(config, tables_to_be_inserted: list) -> tuple:
    """
    The database insert method is responsible for connecting to the
    database, adding records to one or more tables and closing the
    connection.
    """
    # Connect to database
    logging.info('insert called')
    logging.info(config.DB_HOST)
    connection_string = _get_database_connection_string(config)
    logging.debug(connection_string)
    connection = _get_database_connection(connection_string)
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
            return False, dict({error_string: str(error)})

    connection.commit()
    cursor.close()
    connection.close()
    return True, {}


def _get_database_connection(connection_string):
    # Infinite loop until connection established
    while True:
        try:
            connection = db.connect(connection_string)
            return connection
        except Exception as error:
            logging.warning("Unable to connect")
            logging.warning(str(error))


def _get_database_connection_string(config):
    return "DRIVER={{{}}};SERVER={};DATABASE={};UID={};PWD={}".format(
        config.ODBC_DRIVER,
        config.DB_HOST, 
        config.DB_NAME, 
        config.DB_USERNAME, 
        config.DB_PASSWORD
    )


def _wrap_strings_with_quotes(value):
    """
    SQL server insert statements wrap quotes around strings
    but omit quotes if numbers.
    """
    if str(type(value)) == "<class 'str'>":
        return "'{}'".format(value)
    return str(value)
