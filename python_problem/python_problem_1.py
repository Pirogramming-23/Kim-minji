import random

def brGame():
    while True:
        try:
            count = int(input("부를 숫자의 개수를 입력하세요(1, 2, 3만 입력 가능) : "))
            if count in [1, 2, 3]:
                return count
            else:
                print("1, 2, 3 중 하나를 입력하세요.")
        except ValueError:
            print("정수를 입력하세요.")

num = 0
player = "computer"  

while num < 31:
    if player == "player":
        count = brGame()
    else:
        count = random.randint(1, 3)

    for _ in range(count):
        num += 1
        print(f"{player} : {num}")
        if num >= 31:
            if player == "player":
                print("computer win!")
            else:
                print("player win!")
            break

    if num >= 31:
        break

    # 다음 차례로 넘어감
    player = "player" if player == "computer" else "computer"
