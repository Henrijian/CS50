#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    // check the number of command-line arguments is valid (in this case, two arguments)
    // if not, return error code and show error message
    if (argc == 2)
    {
        // iterate the character of user input argument to check is it a number
        // if not, return error code and show error message
        string first_arg = argv[1];
        bool is_first_arg_positive_num = true;
        for (int i = 0; i < strlen(first_arg); i++)
        {
            if (! isdigit(first_arg[i]))
            {
                is_first_arg_positive_num = false;
                break;
            }
        }
        if (is_first_arg_positive_num)
        {
            // convert user input argument to integer
            int key = atoi(first_arg);
            // prompt for inputing plain text for encryption
            string plain_text = get_string("plaintext:  ");

            printf("ciphertext: ");
            // iterate each character in plain text
            char each_char;
            const int shift_pos = key % 26;
            const int A_ascii_num = (int) 'A';
            const int a_ascii_num = (int) 'a';
            int ascii_shift_pos;
            int ascii_num;
            for (int i = 0; i < strlen(plain_text); i++)
            {
                each_char = plain_text[i];
                if (isupper(each_char))
                {
                    // if the character is a letter, shift it and remain it case then print it out
                    ascii_shift_pos = (each_char + shift_pos - A_ascii_num) % 26;
                    ascii_num = A_ascii_num + ascii_shift_pos;
                    printf("%c", ascii_num);
                }
                else if (islower(each_char))
                {
                    // if the character is a letter, shift it and remain it case then print it out
                    ascii_shift_pos = (each_char + shift_pos - a_ascii_num) % 26;
                    ascii_num = a_ascii_num + ascii_shift_pos;
                    printf("%c", ascii_num);
                }
                else
                {
                    // if the character is not a letter, print it out
                    printf("%c", each_char);
                }
            }
            printf("\n");
            return 0;
        }
        else
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
}