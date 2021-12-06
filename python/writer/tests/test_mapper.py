import json
from python.writer.config import Config as WriterConfig
from python.writer.mapper import Mapper
from python.common.helper import load_json_into_dict


# To override the config class for testing
class Config(WriterConfig):
    MAPPER_CONFIG_FILENAME = 'python/writer/mapper.json'
    

class TestMapper:

    @staticmethod
    def convert_to_tables(filename):
        mapper = Mapper(WriterConfig())
        sample_message = load_json_into_dict('python/common/tests/sample_data/etk/' + filename)
        return mapper.convert_to_tables(sample_message)

    def test_sample_message_creates_multiple_tables_with_common_dict_structure(self):
        for table in self.convert_to_tables('event_issuance.json'):
            assert 'columns' in table
            assert 'table' in table
            assert 'values' in table

    def test_event_issuance_message_creates_three_tables(self):
        table_names = [table['table'] for table in self.convert_to_tables('event_issuance.json')]
        assert table_names[0] == 'etk.events'
        assert table_names[1] == 'etk.issuances'
        assert table_names[2] == 'etk.violations'
        assert table_names[3] == 'gis.geolocations'
        assert len(table_names) == 4

    def test_event_issuance_message_creates_an_events_table(self):
        event = next(x for x in self.convert_to_tables('event_issuance.json') if x["table"] == 'etk.events')
        assert event['columns'][0] == 'id'
        assert event['columns'][1] == 'date_time'
        assert event['columns'][2] == 'version'
        assert event['columns'][3] == 'type'

    def test_event_issuance_message_creates_an_issuance_table(self):
        issuance = next(x for x in self.convert_to_tables('event_issuance.json') if x["table"] == 'etk.issuances')
        assert issuance['columns'][0] == 'event_id'
        assert issuance['columns'][1] == 'ticket_number'
        assert issuance['columns'][2] == 'offender_type_code'
        assert issuance['columns'][3] == 'violation_date'
        assert issuance['columns'][4] == 'violation_time'

    def test_vt_payments_message_creates_two_tables(self):
        table_names = [table['table'] for table in self.convert_to_tables('vt_payment.json')]
        assert table_names[0] == 'etk.events'
        assert table_names[1] == 'etk.payments'
        assert len(table_names) == 2

    def test_vt_query_message_creates_two_tables(self):
        table_names = [table['table'] for table in self.convert_to_tables('vt_query.json')]
        assert table_names[0] == 'etk.events'
        assert table_names[1] == 'etk.queries'
        assert len(table_names) == 2

    def test_vt_dispute_message_creates_two_tables(self):
        table_names = [table['table'] for table in self.convert_to_tables('vt_dispute.json')]
        assert table_names[0] == 'etk.events'
        assert table_names[1] == 'etk.disputes'
        assert len(table_names) == 2

    def test_vt_dispute_findings_message_creates_two_tables(self):
        table_names = [table['table'] for table in self.convert_to_tables('vt_dispute_finding.json')]
        assert table_names[0] == 'etk.events'
        assert table_names[1] == 'etk.dispute_findings'
        assert len(table_names) == 2

    def test_vt_dispute_status_updates_message_creates_two_tables(self):
        table_names = [table['table'] for table in self.convert_to_tables('vt_dispute_status_update.json')]
        assert table_names[0] == 'etk.events'
        assert table_names[1] == 'etk.dispute_status_updates'
        assert len(table_names) == 2



