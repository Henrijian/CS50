from cs50 import *

# Get text from user
input_text = get_string("Text: ")

WORDS_SEP = " "
SENTENCE_SEPS = [".", "!", "?"]

# Calculate number of words
words_count = len(input_text.split(WORDS_SEP))
# Initialize count number of letter and sentences
letters_count = 0
sentences_count = 0
# Calculate number of letters and sentences
for c in input_text:
    if c.isalpha():
        # Calculate number of letters
        letters_count += 1
    elif c in SENTENCE_SEPS:
        # Calculate number of sentences
        sentences_count += 1

# print(f"Words count: {words_count}")
# print(f"Letters count: {letters_count}")
# print(f"Sentences count: {sentences_count}")
# Calculate Coleman-Liau index: 0.0588 * L - 0.296 * S - 15.8
L = letters_count / words_count * 100 # L is the average number of letters per 100 words in the text.
S = sentences_count / words_count * 100 # S is the average number of sentences per 100 words in the text.
index = round(0.0588 * L - 0.296 * S - 15.8)

# According to the value of index print out string
if index < 1:
    print("Before Grade 1")
elif index >= 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")