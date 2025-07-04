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
player = "playerA"

while num < 31:
    count = brGame()  

    for i in range(count):
        num += 1
        print(f"{player} : {num}")
        if num >= 31:
            if player == "playerA":
                print("playerB win!")
            else:
                print("playerA win!")
            break

    if num >= 31:
        break

    if player == "playerA":
        player = "playerB"
    else:
        player = "playerA"
