# This script modifies the print_layout.json file to
# create a PDF with different dimensions.

import logging
import json
from python.common.helper import load_json_into_dict

ORIGINAL_JSON_FILE_PATH = '/home/jlonge/scratch/print_layout_original.json'
OUTPUT_JSON_FILE_PATH = './web_app/src/config/print_layout.json'


def main():
    # logging.warning("inside main()")
    input_dict = load_json_into_dict(ORIGINAL_JSON_FILE_PATH)
    output = load_json_into_dict(ORIGINAL_JSON_FILE_PATH)
    logging.warning(str(input_dict))
    for template in ['12Hour']:
        for field in input_dict[template]['fields'].keys():
            logging.warning("template: {} field: {}".format(template, field))
            starting_coordinate = input_dict[template]['fields'][field]['start']
            # print("OLD: {} - {}".format(template, str(starting_coordinate)))
            converted_coordinate = convert_notice(starting_coordinate)
            output[template]['fields'][field]['start'] = converted_coordinate
            # print("NEW: {} - {}".format(template, str(converted_coordinate)))
    print(json.dumps(output))


def convert_notice(coordinate) -> dict:
    # the Notice is on the left side of the new, two-page document
    return {
        "x": round((coordinate['x'] * 1), 1),
        "y": round((coordinate['y'] * 1) - 8, 1)
    }


# def convert_report(coordinate) -> dict:
#     # the Report is the right side of the new, two-page document
#     return {
#         "x": round((coordinate['x'] * 1.05) + 108, 1),
#         "y": round((coordinate['y'] * 0.9) - 25, 1)
#     }


if __name__ == "__main__":
    main()
