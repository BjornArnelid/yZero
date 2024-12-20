from random import randint


def roll_from_list(choices):
    return choices[randint(0, len(choices) - 1)]


def roll_dice(sides):
    return randint(1, sides)


def roll_d66():
    return roll_dice(6) * 10 + roll_dice(6)


def roll_dice_pool_success(number_of_dices, sides):
    success = 0
    for i in range(number_of_dices):
        if roll_dice(sides) == sides:
            success += 1
    return success