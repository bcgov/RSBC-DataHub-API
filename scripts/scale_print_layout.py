# This script modifies the print_layout.json file to
# create a PDF with different dimensions.

import logging
import json
from python.common.helper import load_json_into_dict

ORIGINAL_JSON_FILE_PATH = '/home/jlonge/scratch/print_layout_original.json'
OUTPUT_JSON_FILE_PATH = './web_app/src/config/print_layout.json'
X_OFFSET = 25
Y_OFFSET = 25
X_SCALE = .82
Y_SCALE = .82


def main():
    # logging.warning("inside main()")
    input_dict = load_json_into_dict(ORIGINAL_JSON_FILE_PATH)
    output = load_json_into_dict(ORIGINAL_JSON_FILE_PATH)
    # logging.warning(str(input_dict))
    for template in ['12Hour']:
        # logging.warning(str(input_dict[template]['fields']))
        for field in input_dict[template]['fields']:
            starting_coordinate = input_dict[template]['fields'][field]['start']
            # print("OLD: {} - {}".format(template, str(starting_coordinate)))
            converted_coordinate = convert(starting_coordinate)
            output[template]['fields'][field]['start'] = converted_coordinate
            # print("NEW: {} - {}".format(template, str(converted_coordinate)))
    print(json.dumps(output))


def convert(coordinate) -> dict:
    return {
        "x": round((coordinate['x'] * X_SCALE) + X_OFFSET, 1),
        "y": round((coordinate['y'] * Y_SCALE) + Y_OFFSET, 1)
    }


if __name__ == "__main__":
    main()
