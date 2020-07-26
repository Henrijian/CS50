// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 125000;

// Hash table
node *table[N];

// Number of words in dictionary
unsigned int dict_size = 0;

// Whether dictionary is loaded
bool loaded = false;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    unsigned word_len = strlen(word);
    char lower_word[word_len + 1];
    for (int i = 0; i < word_len + 1; i++)
    {
        if (isalpha(word[i]))
        {
            lower_word[i] = tolower(word[i]);
        }
        else
        {
            lower_word[i] = word[i];
        }
    }
    int hash_code = hash(lower_word);
    node *word_node = table[hash_code];
    bool found_word = false;
    while (word_node != NULL)
    {
        if (strcmp(lower_word, word_node->word) == 0)
        {
            found_word = true;
            break;
        }
        else
        {
            word_node = word_node->next;
        }
    }
    return found_word;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    unsigned int hash_code = 0;
    int n;
    for (int i = 0; word[i] != '\0'; i++)
    {
        if (isalpha(word[i]))
        {
            n = word[i] - 'a' + 1;
        }
        else
        {
            n = 27;
        }
        hash_code = (hash_code << 3) + n;
    }
    return hash_code % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // TODO
    // Initialize table
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }
    dict_size = 0;
    // Open dictionary file for loading into data structure
    FILE *file = fopen(dictionary, "r");
    // Check whether the file is opened successfully
    if (file == NULL)
        return false;
    // Iterater each byte in file to get each character, while encounter '\n' store the word in hash table
    node *word_node = NULL;
    unsigned int index = 0;
    unsigned int hash_code;
    for (int c = fgetc(file); c != EOF; c = fgetc(file))
    {
        if (c == '\n')
        {
            hash_code = hash(word_node->word);
            word_node->next = table[hash_code];
            table[hash_code] = word_node;
            index = 0;
            dict_size++;
        }
        else
        {
            if (index == 0)
            {
                word_node = malloc(sizeof(node));
                memset(word_node->word, '\0', LENGTH + 1);
                word_node->next = NULL;
            }
            word_node->word[index] = c;
            index++;
        }
    }
    // Check whether there was an error
    if (ferror(file))
    {
        fclose(file);
        return false;
    }
    loaded = true;
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    return dict_size;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    if (loaded)
    {
        for (int i = 0; i < N; i++)
        {
            node *word_node = table[i];
            while (word_node != NULL)
            {
                node *tmp_node = word_node->next;
                free(word_node);
                word_node = tmp_node;
            }
        }
        loaded = false;
        return true;
    }
    else
    {
        return false;
    }
}