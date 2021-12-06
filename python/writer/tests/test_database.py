import pytest
import python.writer.database as database


single_row = [
    [
        {
            "table": "gis.geolocations",
            "columns": [
                "business_program",
                "business_type",
                "business_id",
            ],
            "values": [
                "ETK",
                "violation",
                "EA85000034",
            ],
        },
        'INSERT INTO gis.geolocations (business_program,business_type,business_id) VALUES (?,?,?)'
        ]
]


@pytest.mark.parametrize("dictionary_in, expected_sql", single_row)
def test_create_insert_statement_method_can_handle_a_single_row(dictionary_in, expected_sql):
    sql = database.create_insert_statement(dictionary_in)
    assert sql == expected_sql


multi_row = [
    [
        {
            "table": "gis.geolocations",
            "columns": [
                "business_program",
                "business_type",
                "business_id",
            ],
            "values": [
                [
                    "ETK",
                    "violation",
                    "EA85000034",
                ],
                [
                    "ETK2",
                    "violation2",
                    "EA8507777",
                ]
            ],
        },
        'INSERT INTO gis.geolocations (business_program,business_type,business_id) VALUES (?,?,?)'
        ]
]


@pytest.mark.parametrize("dictionary_in, expected_sql", multi_row)
def test_create_insert_statement_method_can_handle_a_multiple_rows(dictionary_in, expected_sql):
    sql = database.create_insert_statement(dictionary_in)
    assert sql == expected_sql
