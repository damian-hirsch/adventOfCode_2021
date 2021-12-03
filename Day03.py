import numpy as np


def get_input():
    with open('Input/Day03.txt', 'r') as file:
        data = file.read().splitlines()
    return data


def part_one(data: list) -> int:
    s = ''
    gamma_rate = ''
    epsilon_rate = ''
    for i in range(len(data[0])):
        for j in range(len(data)):
            s += data[j][i]
        if s.count('1') > len(s)/2:
            gamma_rate += '1'
            epsilon_rate += '0'
        else:
            gamma_rate += '0'
            epsilon_rate += '1'
        s = ''

    return int(gamma_rate, base=2) * int(epsilon_rate, base=2)


def part_two(data: list) -> int:
    list_oxy = []
    for i in range(len(data)):
        list_oxy.append(list(data[i]))
    list_co2 = list_oxy.copy()

    counter_oxy = 0
    while len(list_oxy) > 1:
        s = ''
        for j in range(len(list_oxy)):
            s += list_oxy[j][counter_oxy]
        if s.count('1') >= len(s)/2:
            for k in range(len(list_oxy) - 1, -1, -1):
                if list_oxy[k][counter_oxy] == '0':
                    list_oxy.pop(k)
        else:
            for k in range(len(list_oxy) - 1, -1, -1):
                if list_oxy[k][counter_oxy] == '1':
                    list_oxy.pop(k)
        counter_oxy += 1

    counter_co2 = 0
    while len(list_co2) > 1:
        s = ''
        for j in range(len(list_co2)):
            s += list_co2[j][counter_co2]
        if s.count('0') <= len(s) / 2:
            for k in range(len(list_co2) - 1, -1, -1):
                if list_co2[k][counter_co2] == '1':
                    list_co2.pop(k)
        else:
            for k in range(len(list_co2) - 1, -1, -1):
                if list_co2[k][counter_co2] == '0':
                    list_co2.pop(k)
        counter_co2 += 1

    oxy = [''.join(ele) for ele in list_oxy]
    co2 = [''.join(ele) for ele in list_co2]
    return int(oxy[0], base=2) * int(co2[0], base=2)


def main():
    print('The power consumption of the submarine is:', part_one(get_input()))
    print('The life support rating of the submarine is:', part_two(get_input()))


if __name__ == '__main__':
    main()
