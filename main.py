import random

KICK_SUCCESS_RATE = 70
SAN_RATE = 60

def throw_dice(x: int, y: int) -> int:
    a = [random.randint(1, y) for _ in range(x)]
    return a

def battle(is_print: bool = True) -> int:
    my_sp = throw_dice(1, 100)[0]
    if is_print:
        print(f"自分の雇うSPの数(1d100) > {my_sp}")
    my_true_sp = throw_dice(1, my_sp)[0]
    if is_print:
        print(f"ちゃんと働く味方SPの数(1d{my_sp}) > {my_true_sp}")

    enemy_sp = throw_dice(1, 500)[0]
    if is_print:
        print(f"敵の雇うSPの数(1d500) > {enemy_sp}")
    enemy_true_sp = throw_dice(1, enemy_sp)[0]
    if is_print:
        print(f"ちゃんと働く敵SPの数(1d{enemy_sp}) > {enemy_true_sp}")

    round = 0
    while True:
        round += 1
        if is_print:
            print(f"\n---Round{round:2d}---")

        # 味方のSANチェック
        my_san_num = len([a for a in throw_dice(my_true_sp, 100) if a <= SAN_RATE])
        if is_print:
            print(f"怯えない味方SPの数 > {my_san_num}")

        # 敵のSANチェック
        enemy_san_num = len([a for a in throw_dice(enemy_true_sp, 100) if a <= SAN_RATE])
        if is_print:
            print(f"怯えない敵SPの数 > {enemy_san_num}")

        # 味方攻撃判定
        my_success_kick_num = len([a for a in throw_dice(my_san_num, 100) if a <= KICK_SUCCESS_RATE])
        if is_print:
            print(f"味方のキック成功数 > {my_success_kick_num}")

        # 敵攻撃判定
        enemy_success_kick_num = len([a for a in throw_dice(enemy_san_num, 100) if a <= KICK_SUCCESS_RATE])
        if is_print:
            print(f"敵のキック成功数 > {enemy_success_kick_num}")

        enemy_true_sp -= my_success_kick_num
        my_true_sp -= enemy_success_kick_num

        if is_print:
            print(f"残りSP 味方: {my_true_sp} 敵: {enemy_true_sp}")
        if my_true_sp <= 0 or enemy_true_sp <= 0:
            break

    if my_true_sp <= 0 and enemy_true_sp > 0:
        if is_print:
            print(f"味方が全滅しました。。。(敵の残りSP: {enemy_true_sp})")
        return 0
    elif my_true_sp > 0 and enemy_true_sp <= 0:
        if is_print:
            print(f"貴方の組が勝ちました！(味方の残りSP: {my_true_sp})")
        return 1
    else:
        if is_print:
            print("全滅しました。(引き分け)")
        return 2


if __name__ == "__main__":
    # BATTLE_NUM = 10000
    # battle_result = [battle(False) for _ in range(BATTLE_NUM)]
    # win_num = len([a for a in battle_result if a == 1])
    # lose_num = len([a for a in battle_result if a == 0])
    # draw_num = len([a for a in battle_result if a == 2])
    # print(f"{win_num}勝 {lose_num}負 {draw_num}分")

    # print(f"勝率: {win_num / BATTLE_NUM * 100}%")
    battle()
