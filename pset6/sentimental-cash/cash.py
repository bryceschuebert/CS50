from cs50 import get_float

def get_money():
    while True:
        n = get_float("Change owed: ")
        if n > 0:
            break
    return n

change = get_money() * 100
numCoins = 0

while change >= 25:
    change -= 25
    numCoins += 1;
while change >= 10:
    change -= 10
    numCoins += 1
while change >= 5:
    change -= 5
    numCoins += 1
while change >= 1:
    change -= 1
    numCoins += 1

print(f"{numCoins}\n")

