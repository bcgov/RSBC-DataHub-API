import json


def load_json_into_dict(file_name) -> dict:
    with open(file_name, 'r') as f:
        data = f.read()
    return json.loads(data)


def validate_form_number(number: str) -> bool:
    """
    Validate check digit used in IRP, VI and UL forms
    :param number:
    :return:
    """
    number_list = list(number)
    check_digit = int(number_list.pop())

    n = list()
    for element in number_list:
        # cast each element to an int
        n.append(int(element))

    # ignore the first two digits, sum the number
    # using a special formula
    number_sum = (
            n[2] +
            _times_2(n[3]) +
            n[4] +
            _times_2(n[5]) +
            n[6] +
            _times_2(n[7]))

    # compare modulus of the sum with check digit
    return number_sum % 10 == check_digit


def _times_2(number: int) -> int:
    """
    If number * 2 is greater than 9, return 1
    otherwise return the number * 2
    :param number:
    :return:
    """
    return int(list(str(number * 2))[0])
