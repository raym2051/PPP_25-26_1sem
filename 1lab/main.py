if __name__ == "__main__":
    from random import *

    dano = [i for i in range(1, *sample(range(2,1000), 1))]

    n = sample(range(2,1000),1)

    count = 0
    ans = set()

    for _ in range(n[0]):
        shuffle(dano)
        for number in dano:
            if dano.index(number) + 1 == number:
                count += 1
                ans.add(number)

    ans = sorted(ans)

    print(f'Частота попадания числа на свое место, при {n[0]} тусовках = {round(count / len(dano),2) * 100:.0f} раз')
    print(f'Вероятность, что число попадет на свое место = {round(len(ans)/len(dano),2) * 100:.0f}%')
    print(f'Числа которые повторялись от 1 до {max(dano)}: {ans}.')
