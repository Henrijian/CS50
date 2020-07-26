from cs50 import *
from enum import Enum

class Coin(Enum):
    Quarter = 25
    Dime = 10
    Nickle = 5
    Penny = 1

# Get changes from user
while True:
    change_dollars = get_float("Change owned: ")
    if 0 <= change_dollars:
        break

# Calculate the minimun number of coin to make the changes
change_cents = change_dollars * 100 # 1 dollar = 100 cents
total_num = 0
for coin in Coin:
    coin_num = change_cents // coin.value
    change_cents = change_cents - coin.value * coin_num
    total_num += int(coin_num)
print(total_num)