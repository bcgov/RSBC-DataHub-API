import logging
import json
import python.writer.database as database
import python.writer.middleware as middleware
from python.common.helper import middle_logic
from python.writer.config import Config
from pydash import objects


logging.basicConfig(level=Config.LOG_LEVEL, format=Config.LOG_FORMAT)
MAX_INSERT_RECORD_COUNT = 50


def main(config):
    data = dict()
    data['config'] = config
    connection_string = database.get_database_connection_string(config)
    logging.debug(connection_string)
    logging.debug(config.GEOCODER_API_URI)
    connection = database.get_database_connection(connection_string)
    is_success, records = select_issuance_records_with_geolocation_data(connection)
    while is_success and len(records) > 0:
        logging.info('number of records found: {}'.format(len(records)))
        data['rows_to_insert'] = list()
        for etk_issuance in records:
            logging.info("---------------------------------------------------")
            logging.info("processing ticket_number: {}".format(etk_issuance[0]))
            data['business_id'] = etk_issuance[0]  # ticket_number
            data['address_raw'] = etk_issuance[1]
            data = middle_logic(business_rules(), **data)
            print(" ")
        logging.info("---- no more records in this batch to geocode ----")
        is_okay, data = create_table_to_insert(**data)
        if len(data.get('rows_to_insert')) > 0:
            logging.info('---- writing remaining records to the database ----')
            is_okay, data = write(**data)
        logging.info('---- getting a new batch of records ----')
        connection = database.get_database_connection(connection_string)
        is_success, records = select_issuance_records_with_geolocation_data(connection)
    logging.info('---- success: end of script ----')
    print('---- no records found ----')
    return


def business_rules():
    return [
        {"try": middleware.clean_up_address, "fail": []},
        {"try": middleware.build_payload_to_send_to_geocoder, "fail": []},
        {"try": middleware.callout_to_geocoder_api, "fail": []},
        {"try": middleware.transform_geocoder_response, "fail": []},
        {"try": add_row_to_list, "fail": []},
        {"try": too_few_records_to_write_to_database, "fail": [
            {"try": create_table_to_insert, "fail": []},
            {"try": write, "fail": []},
            {"try": delete_temporary_table, "fail": []},
        ]},
    ]


def select_issuance_records_with_geolocation_data(connection) -> tuple:
    """
    Connect to the database and retrieve 200 records that require historical geocoding.
    """
    # Connect to database
    logging.info('getting database records')
    cursor = connection.cursor()

    sql = "SELECT TOP 200 i.ticket_number, CONCAT(i.violation_highway_desc,', ',i.violation_city_name)" + \
        " FROM etk.issuances i" + \
        " LEFT JOIN gis.geolocations g ON i.ticket_number = g.business_id" + \
        " WHERE g.business_id is NULL and i.violation_highway_desc IS NOT NULL;"

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


def too_few_records_to_write_to_database(**args) -> tuple:
    row_count = len(args.get('rows_to_insert'))
    return row_count < MAX_INSERT_RECORD_COUNT, args


def create_table_to_insert(**args) -> tuple:
    tables = list()
    geolocation = args.get('geolocation')
    table = {
        'columns': [],
        'values': args.get('rows_to_insert'),
        'table': 'gis.geolocations'}
    for attribute in geolocation:
        value = objects.get(geolocation, attribute)
        if value:
            table['columns'].append(attribute)
    tables.append(table)
    args['tables_for_insert'] = tables
    return True, args


def add_row_to_list(**args) -> tuple:
    rows_to_insert = args.get('rows_to_insert')
    geolocation = args.get('geolocation')
    values = list()
    for attribute in geolocation:
        value = objects.get(geolocation, attribute)
        if value:
            values.append(value)
    rows_to_insert.append(values)
    args['rows_to_insert'] = rows_to_insert
    return True, args


def delete_temporary_table(**args) -> tuple:
    args['rows_to_insert'] = list()
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
