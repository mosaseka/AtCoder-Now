D = str(input())
DIRECTION = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
CHECK = DIRECTION.index(D)

print(DIRECTION[(CHECK + 4) % 8])