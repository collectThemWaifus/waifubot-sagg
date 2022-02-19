import random

randomNum = random.randint(0,60)
rank = ''
match randomNum:
    case 1:
       rank = 'SSS'
    case randomNum if randomNum <= 3:
        rank = 'SS'
    case randomNum if randomNum <= 8:
        rank = 'S'
    case randomNum if randomNum <= 14:
        rank = 'A'
    case randomNum if randomNum <= 22:
        rank = 'B'
    case randomNum if randomNum <= 31:
        rank = 'C'
    case _:
        rank = 'D'
print (f"random Num :{randomNum}\n Rank: {rank}")