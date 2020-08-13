import json
from pydash import objects


class Mapper:
    """
    The Mapper is responsible for converting the message into a
    list of tables for insertion into a database.  Each table includes
    data record(s) to be inserted.
    """

    def __init__(self, config):
        self.mappings = self.get_mappings(config.MAPPER_CONFIG_FILENAME)

    @staticmethod
    def get_mappings(file_name) -> dict:
        with open(file_name, 'r') as f:
            data = f.read()
        return json.loads(data)

    def convert_to_tables(self, message: dict) -> list:
        """
            This convert_to_tables() method converts the json message
            into one or more data tables according to the mapping
            instructions in the mapper.json config file.
        """
        # The message's datatype determines how it should
        # be converted into tables.
        message_datatype = message['event_type']
        # Lookup the data mappings from the mapper.json file
        mapping = next(dataType for dataType in self.mappings['data_types'] if dataType["name"] == message_datatype)
        tables = []
        for table in mapping['tables']:
            if table['relationship'] == 'one-to-one':
                tables.append(self._create_one_to_one_record(table, message))
            if table['relationship'] == 'one-to-many':
                records = objects.get(message, table['many_details']['iterate_on'])
                for record in records:
                    single_table = self._create_one_to_one_record(table, record)
                    key_id = objects.get(message, table['many_details']['key_field']['json_name'])
                    key_field_name = table['many_details']['key_field']['destination_name']
                    tables.append(self._add_key(single_table, key_id, key_field_name))
        return tables

    @staticmethod
    def _create_one_to_one_record(table_name, message) -> dict:
        """
        Build a dictionary with a list for the field names
         (columns) and the associated values
        :param table_name:
        :param message:
        :return:
        """
        table = {'columns': [], 'values': [], 'table': table_name['name']}
        for field in table_name['fields']:
            value = objects.get(message, field['json_name'])
            if value:
                table['columns'].append(field['destination_name'])
                table['values'].append(value)
        return table

    @staticmethod
    def _add_key(record, key_id, key_field_name) -> dict:
        record['columns'].append(key_field_name)
        record['values'].append(key_id)
        return record
