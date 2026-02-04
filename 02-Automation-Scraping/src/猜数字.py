import random


def guess_number_game():
    # 生成1到100之间的随机数
    secret_number = random.randint(1, 10000)
    attempts = 0
    max_attempts = 100

    print("欢迎来到猜数字游戏!")
    print(f"我已经想好了一个1到10000之间的数字，你有{max_attempts}次机会猜出它。")

    while attempts < max_attempts:
        # 计算剩余次数
        remaining = max_attempts - attempts

        # 获取用户输入并处理可能的错误
        try:
            guess = input(f"请输入你的猜测（还剩{remaining}次）: ")
            guess = int(guess)
        except ValueError:
            print("请输入一个有效的数字!")
            continue

        # 增加尝试次数
        attempts += 1

        # 检查猜测是否正确
        if guess < secret_number:
            print("太小了! 再试试更大的数字。")
        elif guess > secret_number:
            print("太大了! 再试试更小的数字。")
        else:
            print(f"恭喜你! 你猜对了，答案就是{secret_number}!")
            print(f"你用了{attempts}次猜出了正确答案。")
            return

    # 如果用完了所有机会
    print(f"很遗憾，你已经用完了所有{max_attempts}次机会。")
    print(f"正确答案是{secret_number}。")


# 运行游戏
if __name__ == "__main__":
    guess_number_game()
