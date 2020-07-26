from cs50 import *

LOWER_BOUND = 1
UPPER_BOUND = 8
BLOCK_SIGN = "#"
SPACE_SIGN = " "
GAP = 2

# Ask user for pyramid height
while True:
    height = get_int("Height: ")
    if (LOWER_BOUND <= height) and (height <= UPPER_BOUND):
        break
# Draw pyramid
for i in range(height):
    space_num = height - i - 1
    block_num = i + 1
    print(SPACE_SIGN * space_num + BLOCK_SIGN * block_num + SPACE_SIGN * GAP + BLOCK_SIGN * block_num)