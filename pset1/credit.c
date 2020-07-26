#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    long card_num;
    do
    {
        card_num = get_long("Number: ");
    }
    while (card_num < 0);

    // get card number length
    int card_len = 0;
    do
    {
        card_len++;
    } while (card_num > pow(10, card_len));
    if (card_len != 13 && card_len != 15 && card_len != 16) {
        printf("INVALID\n");
        return -1;
    }

    // get checksum of card number
    int checksum = 0;
    for (int i = 0; i < card_len; i++) {
        long lower_mutipler = pow(10, i);
        long digit = (card_num / lower_mutipler) % 10;
        if (i % 2 == 1) {
            checksum = checksum + (digit * 2) / 10 + (digit * 2) % 10;
        } else {
            checksum = checksum + digit;
        }
    }
    if (checksum % 10 != 0) {
        printf("INVALID\n");
        return -1;
    }

    // get prefix 2 digit of car number
    int start_two_digit = card_num / pow(10, card_len - 2);
    if ((start_two_digit == 34 || start_two_digit == 37) && card_len == 15) {
        printf("AMEX\n");
    } else if ((51 <= start_two_digit && start_two_digit <= 55) && card_len == 16) {
        printf("MASTERCARD\n");
    } else if (start_two_digit / 10 == 4 && (card_len == 13 || card_len == 16)) {
        printf("VISA\n");
    } else {
        printf("INVALID\n");
    }
}
