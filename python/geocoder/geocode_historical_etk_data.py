import logging
import json
import python.writer.database as database
import python.writer.middleware as middleware
from python.writer.config import Config
from pydash import objects


logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)


def main(config):
    data = dict()
    data['config'] = config
    connection_string = database.get_database_connection_string(config)
    logging.debug(connection_string)
    logging.debug(config.GEOCODER_API_URI)
    connection = database.get_database_connection(connection_string)
    is_success, records = select_issuance_records_with_geolocation_data(connection)
    if is_success and len(records) > 0:
        print('number of records found: {}'.format(len(records)))
        for etk_issuance in records:
            logging.info("---------------------------------------------------")
            logging.info("processing ticket_number: {}".format(etk_issuance[0]))
            data['business_id'] = etk_issuance[0]  # ticket_number
            data['address_raw'] = etk_issuance[1]
            is_okay, data = middleware.clean_up_address(**data)
            is_okay, data = middleware.build_payload_to_send_to_geocoder(**data)
            is_okay, data = middleware.callout_to_geocoder_api(**data)
            is_okay, data = middleware.transform_geocoder_response(**data)
            is_okay, data = build_tables_to_insert(**data)
            is_okay, data = write(**data)
            print(" ")
    else:
        print('---- no records found ----')
        return

    print('---- success: end of script ----')
    return


def select_issuance_records_with_geolocation_data(connection) -> tuple:
    """
    The database insert method is responsible for connecting to the
    database, adding records to one or more tables and closing the
    connection.
    """
    # Connect to database
    logging.info('getting database records')
    cursor = connection.cursor()

    sql = "SELECT TOP 500 i.ticket_number, CONCAT(i.violation_highway_desc,', ',i.violation_city_name)" + \
        " FROM etk.issuances i" + \
        " LEFT JOIN gis.geolocations g ON i.ticket_number = g.business_id" + \
        " WHERE g.business_id is NULL and i.violation_highway_desc IS NOT NULL" + \
        " ORDER BY i.ticket_number;"

    try:
        cursor.execute(sql)
    except Exception as error:
        error_string = error.__class__.__name__
        logging.warning("Read from db failed: " + error_string)
        logging.warning(str(error))
        return False, dict({error_string: str(error)})

    records = cursor.fetchall()
    cursor.close()
    connection.close()
    return True, records


def build_tables_to_insert(**args) -> tuple:
    geolocation = args.get('geolocation')
    tables = list()
    table = {'columns': [], 'values': [], 'table': 'gis.geolocations'}
    for attribute in geolocation:
        value = objects.get(geolocation, attribute)
        if value:
            table['columns'].append(attribute)
            table['values'].append(value)
    tables.append(table)
    args['tables_for_insert'] = tables
    return True, args


def write(**args) -> tuple:
    config = args.get('config')
    tables_for_insert = args.get('tables_for_insert')
    logging.debug(json.dumps(tables_for_insert))
    is_successful, error = database.insert(config, tables_for_insert)
    if is_successful:
        return True, args
    logging.warning('database write failed: {}'.format(error))
    return False, args


if __name__ == "__main__":
    print("invoking main()")
    main(Config())
