import json
from functools import reduce
import operator


class Mapper:

    def __init__(self, config):
        self.mappings = self.getMappings(config.MAPPER_PATH + config.MAPPER_CONFIG_FILENAME)

    def getMappings(self, fileName) -> dict:
        with open(fileName, 'r') as f:
            data = f.read()
        
        return json.loads(data)

    # This convertToTables() method converts the json message
    # into one or more data tables according to the mapping 
    # instructions in the mapper.json config file.
    def convertToTables(self, message: dict ) -> list:

        # The message's datatype determines how it should
        # be converted into tables.
        messageDatatype = message['event_type']

        mapping = next(dataType for dataType in self.mappings['data_types'] if dataType["name"] == messageDatatype)

        tables = []

        for tableMap in mapping['tables']:
            table = {}
            table['table'] = tableMap['name']
            #table['relationship'] = tableMap['relationship']

            if tableMap['relationship'] == 'one-to-one':
                table['columns'] = self._createOneHeaderRecord(tableMap)
                table['values'] = self._createOneDataRecord(tableMap, message)

            if tableMap['relationship'] == 'one-to-many':
                table['columns'] = self._createManyHeaderRecord(tableMap)
                table['values'] = self._createManyDataRecords(tableMap, message)

            tables.append(table)

        return tables

    def _createOneHeaderRecord(self, tableMap) -> list:

        header = []

        for field in tableMap['fields']:
            header.append(field['destination_name'])

        return header

    def _createOneDataRecord(self, tableMap, message) -> list:
        
        collection = []
        data = []

        for field in tableMap['fields']:
            value = self._getFromDict(message,field['json_name'])
            data.append(value)

        collection.append(data)
        return collection

    def _createManyHeaderRecord(self, tableMap) -> list:

        header = []

        # Add the key id that joins the child table to the parent
        header.append(tableMap['many_details']['key_field']['destination_name'])

        for field in tableMap['fields']:
            header.append(field['destination_name'])

        return header

    def _createManyDataRecords(self, tableMap, message) -> list:
        
        collection = []
        records = self._getFromDict(message,tableMap['many_details']['itterate_on'])

        for record in records:
            singleRecord = []

            # Add the child table's key ID
            value = self._getFromDict(message,tableMap['many_details']['key_field']['json_name'])
            singleRecord.append(value)
            for field in tableMap['fields']:
                value = self._getFromDict(record,field['json_name'])
                singleRecord.append(value)
            collection.append(singleRecord)

        
        return collection

    def _getFromDict(self, dataDict: dict, itemToGetInDotNotation: str):
        mapList = itemToGetInDotNotation.split('.')
        return reduce(operator.getitem, mapList, dataDict)

