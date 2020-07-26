// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include "dictionary.h"

// Node length in trie node
const unsigned N = 27;

// Represents a node in a trie
typedef struct node
{
    char word[LENGTH + 1];
    struct node *node_table[N];
}
node;

// Trie
node *trie;

// Number of words in dictionary
unsigned int dict_size = 0;

// Whether dictionary is loaded
bool loaded = false;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // return true;
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
    bool found = true;
    unsigned int char_hash;
    node *cur_node = trie;
    node *check_node;
    for (int i = 0; i < word_len; i++)
    {
        char_hash = hash(lower_word[i]);
        check_node = cur_node->node_table[char_hash];
        if (check_node != NULL)
        {
            cur_node = check_node;
        }
        else
        {
            found = false;
            break;
        }
    }
    if (found)
    {
        if (strcmp(cur_node->word, lower_word) != 0)
        {
            found = false;
        }
    }
    return found;
}

// Hashes character to a number
unsigned int hash(const char c)
{
    if (isalpha(c))
    {
        return c - 'a';
    }
    else
    {
        return N - 1;
    }
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize trie
    trie = malloc(sizeof(node));
    memset(trie->word, '\0', LENGTH + 1);
    for (int i = 0; i < N; i++)
    {
        trie->node_table[i] = NULL;
    }

    dict_size = 0;
    // Open dictionary file for loading into data structure
    FILE *file = fopen(dictionary, "r");
    // Check whether the file is opened successfully
    if (file == NULL)
        return false;
    // Iterater each byte in file to get each character, while encounter '\n' store the word in hash table
    node *cur_word_node = trie;
    char cur_word[LENGTH + 1];
    unsigned int char_idx = 0;
    unsigned int char_hash;
    node *char_node;
    for (int c = fgetc(file); c != EOF; c = fgetc(file))
    {
        if (c == '\n')
        {
            for (int i = 0; i < char_idx; i++)
            {
                cur_word_node->word[i] = cur_word[i];
            }
            cur_word_node = trie;
            char_idx = 0;
            dict_size++;
        }
        else
        {
            char_hash = hash(c);
            char_node = cur_word_node->node_table[char_hash];
            if (char_node == NULL)
            {
                char_node = malloc(sizeof(node));
                memset(char_node->word, '\0', LENGTH + 1);
                for (int i = 0; i < N; i++)
                {
                    char_node->node_table[i] = NULL;
                }
                cur_word_node->node_table[char_hash] = char_node;
            }
            cur_word_node = char_node;
            cur_word[char_idx] = c;
            char_idx++;
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

void free_trie(node *trie_node)
{
    if (trie_node == NULL)
    {
        return;
    }
    else
    {
        for (int i = 0; i < N; i++)
        {
            free_trie(trie_node->node_table[i]);
        }
        free(trie_node);
    }
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    if (loaded)
    {
        free_trie(trie);
        loaded = false;
        return true;
    }
    else
    {
        return false;
    }
}