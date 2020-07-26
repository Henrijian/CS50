#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    /* check the number of command-line arguments,
       if not just having a single commaind-line argument,
       return error code and show error message */
    if (argc == 2)
    {
        /* check the length of a key (1st command-line argument),
           if its length is not 26,
           return error code and show error message */
        string key = argv[1];
        if (strlen(key) == 26)
        {
            /* initialize substitution table for replacing plain text's character */
            const int substitution_length = 26;
            int substitution_table[substitution_length];
            for (int i = 0; i < substitution_length; i++)
            {
                substitution_table[i] = -1;
            }
            /* iterate each character of key */
            bool is_valid_key = true;
            const int a_ascii_num = (int) 'a';
            const int A_ascii_num = (int) 'A';
            for (int i = 0; i < strlen(key); i++)
            {
                char each_char = key[i];
                /* if it is a non-alphabetic character or repeated character in key,
                   return error code and show error message */
                if (isalpha(each_char))
                {
                    int alphabetic_order;
                    if (isupper(each_char))
                    {
                        alphabetic_order = each_char - A_ascii_num;
                    }
                    else
                    {
                        alphabetic_order = each_char - a_ascii_num;
                    }
                    for (int j = 0; j < substitution_length; j++)
                    {
                        if (alphabetic_order == substitution_table[j])
                        {
                            is_valid_key = false;
                            break;
                        }
                    }
                    if (is_valid_key)
                    {
                        substitution_table[i] = alphabetic_order;
                    }
                    else
                    {
                        break;
                    }
                }
                else
                {
                    is_valid_key = false;
                    break;
                }
            }
            if (is_valid_key)
            {
                /* prompt to user for getting plain text */
                string plain_text = get_string("plaintext:  ");
                printf("ciphertext: ");
                /* iterate each character of plain text */
                for (int i = 0; i < strlen(plain_text); i++)
                {
                    char each_char = plain_text[i];
                    if (isalpha(each_char))
                    {
                        /* if it is an alphabetic character, find a mapped character in substitution table and remain it case then print it out */
                        char cipher_char;
                        if (isupper(each_char))
                        {
                            int alphabetic_order = each_char - A_ascii_num;
                            cipher_char = toupper(A_ascii_num + substitution_table[alphabetic_order]);
                        }
                        else
                        {
                            int alphabetic_order = each_char - a_ascii_num;
                            cipher_char = tolower(a_ascii_num + substitution_table[alphabetic_order]);
                        }
                        printf("%c", cipher_char);
                    }
                    else
                    {
                        /* if it is not an alphabetic character, print it out */
                        printf("%c", each_char);
                    }
                }
                printf("\n");
                return 0;
            }
            else
            {
                printf("Key cannot contain repeated letters.\n");
                return 1;
            }
        }
        else
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }
    }
    else
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
}