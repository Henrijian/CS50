from cs50 import *
from enum import Enum

class CreditCard(Enum):
    AmericanExpress = 'AMEX'
    MasterCard = 'MASTERCARD'
    Visa = 'VISA'
    Undefined = ''

CARD_LEN = {
    CreditCard.AmericanExpress: [15],
    CreditCard.MasterCard: [16],
    CreditCard.Visa: [13, 16]
}

CARD_PREFIX = {
    CreditCard.AmericanExpress: ["34", "37"],
    CreditCard.MasterCard: ["51", "52", "53", "54", "55"],
    CreditCard.Visa: ["4"]
}

def main():
    card_number = get_int("Number: ")
    card_number_str = str(card_number)
    card_type = get_card_type(card_number_str)
    if card_type != CreditCard.Undefined:
        print(card_type.value)
    else:
        print("INVALID")

def get_checksum(number_str):
    error_val = -1
    result = 0
    # Check type
    if not isinstance(number_str, str):
        return error_val
    # Check string is a positive number string
    try:
        test_num = int(number_str)
        if test_num < 0:
            return error_val
    except:
        return error_val
    # Calculate checksum
    for i, c in enumerate(reversed(number_str)):
        if (i % 2) == 0:
            num = int(c)
        else:
            num = int(c) * 2
        result += (num % 10)
        if num >= 10:
            result += (num // 10)
    return result

def get_card_type(card_number_str):
    # Check type
    if not isinstance(card_number_str, str):
        return CreditCard.Undefined
    # Check card number length and prefix
    result = CreditCard.Undefined
    card_len = len(card_number_str)
    for card_type in CreditCard:
        if not (card_type in CARD_LEN):
            continue
        if not (card_len in CARD_LEN[card_type]):
            continue
        found = False
        if not (card_type in CARD_PREFIX):
            continue
        for card_prefix in CARD_PREFIX[card_type]:
            if card_number_str.startswith(card_prefix):
                found = True
                break
        if found:
            result = card_type
            break
    # If length and prefix of card number is invalid, skip checksum test
    if result == CreditCard.Undefined:
        return CreditCard.Undefined
    # Check the checksum of card number
    checksum = get_checksum(card_number_str)
    if (checksum % 10) == 0:
        return result
    else:
        return CreditCard.Undefined

if __name__ == "__main__":
    main()