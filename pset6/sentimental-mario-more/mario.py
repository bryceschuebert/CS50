from cs50 import get_int

def get_height():
    while True:
        n = get_int("Height: ")
        if n < 9 and n > 0:
            break
    return n

height = get_height()

for row in range(height):
    for spaces in range(height-row-1, 0, -1):
        print(" ", end="")
    for left_hashes in range(row+1):
        print("#", end="")
    # Set concrete double space
    print("  ", end="")
    for right_hashes in range(row+1):
        print("#", end="")
    print("\n", end="")
