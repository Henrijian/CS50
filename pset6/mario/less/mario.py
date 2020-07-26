from cs50 import *

LOWER_BOUND = 1
UPPER_BOUND = 8
while True:
    height = get_int("Height: ")
    if (LOWER_BOUND <= height) and (height <= UPPER_BOUND):
        break

for i in range(height):
    space_num = height - i - 1
    block_num = i + 1
    print(" " * space_num + "#" * block_num)
