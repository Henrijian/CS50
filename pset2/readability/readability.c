#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // get user input (in this case, text)
    string text = get_string("Text: ");
    printf("%s\n", text);
    // get the count of letters in text
    int letters_count = count_letters(text);
    // get the count of words in text
    int words_count = count_words(text);
    // get the count of sentences in text
    int sentences_count = count_sentences(text);
    /*
       calculate the value of Coleman-Liau index
       index = 0.0588 * L - 0.296 * S - 15.8
       L: average number of letters per 100 words in the text
       S: average number of sentences per 100 words in the text
    */
    double L = (double) letters_count / (double) words_count * 100.0;
    double S = (double) sentences_count / (double) words_count * 100.0;
    double index = 0.0588 * L - 0.296 * S - 15.8;
    // round the value of index to integer
    int round_index = round(index);
    // according to the value of index, show different message
    if (round_index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (round_index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", round_index);
    }
}

int count_letters(string text)
{
    int letters_count = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if isalpha(text[i])
        {
            letters_count++;
        }
    }
    return letters_count;
}

int count_words(string text)
{
    int words_count = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            words_count++;
        }
    }
    words_count += 1; //because of the end of the text is not a space
    return words_count;
}

int count_sentences(string text)
{
    int sentences_count = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        char each_char = text[i];
        if (each_char == '.' || each_char == '!' || each_char == '?')
        {
            sentences_count++;
        }
    }
    return sentences_count;
}