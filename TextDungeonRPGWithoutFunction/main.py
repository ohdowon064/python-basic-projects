import random

# 1. 딕셔너리: 플레이어 상태 정의
player = {
    "name": "모험가",
    "HP": 100,
    "Max_HP": 100,
    "Attack": 20,
    "Defense": 5,
    "Gold": 500,
    "Inventory": [],  # 2. 리스트: 인벤토리 (아이템 이름 저장)
}

# 3. 리스트 of 딕셔너리: 상점 목록
shop_items = [
    {"name": "포션", "price": 100, "heal": 30},
    {"name": "강철 검", "price": 300, "attack": 15},
    {"name": "방패", "price": 200, "defense": 5},
]

# 4. 리스트 of 딕셔너리: 몬스터 목록
monsters = [
    {"name": "슬라임", "HP": 30, "Attack": 8, "Gold": 50},
    {"name": "고블린", "HP": 60, "Attack": 15, "Gold": 120},
    {"name": "트롤", "HP": 120, "Attack": 25, "Gold": 300},
]

# --- 메인 게임 루프 시작 ---
print("--- 텍스트 기반 시뮬레이터 ---")
player["name"] = input("캐릭터 이름을 입력하세요: ")
print(f"\n환영합니다, {player['name']} 님! 모험을 시작합니다.")

game_running = True

while game_running:
    # ----------------------------------------------------
    # 1. 상태 출력 (f-string, for)
    print("\n" + "=" * 40)
    print(f"✨ **{player['name']}** 상태")
    print(
        f"HP: {player['HP']}/{player['Max_HP']}, 공격력: {player['Attack']}, 방어력: {player['Defense']}"
    )
    print(f"💰 골드: {player['Gold']}")

    # 인벤토리 출력 (for)
    print("인벤토리:", end=" ")
    if player["Inventory"]:
        for item_name in player["Inventory"]:
            print(item_name, end=" | ")
        print()
    else:
        print("비어 있음")
    print("=" * 40)

    # ----------------------------------------------------
    # 2. 메인 메뉴 선택 (input, if)

    print("\n--- 메인 메뉴 ---")
    print("1. 상점 방문 | 2. 사냥터 가기 | 3. 아이템 사용 | 4. 종료")
    choice = input("번호를 입력하세요: ")

    # ----------------------------------------------------
    # 2-1. 상점 방문 로직 (if, for, 딕셔너리, 리스트)
    if choice == "1":
        print("\n--- 상점 ---")

        # 상점 목록 출력 (for, 딕셔너리 활용)
        i = 0
        for item in shop_items:
            print(f"[{i + 1}] {item['name']} (가격: {item['price']} 골드)")
            i += 1

        buy_choice = input("구매할 아이템 번호 (취소: 0): ")

        if buy_choice != "0":
            try:
                item_index = int(buy_choice) - 1

                if 0 <= item_index < len(shop_items):
                    selected_item = shop_items[item_index]

                    # if: 골드 체크
                    if player["Gold"] >= selected_item["price"]:
                        player["Gold"] -= selected_item["price"]

                        # if: 무기/방어구 구매 시 능력치 상승 (딕셔너리 값 변경)
                        if "attack" in selected_item:
                            player["Attack"] += selected_item["attack"]
                            print(
                                f"'{selected_item['name']}'을(를) 장착하여 공격력이 {selected_item['attack']} 증가했습니다."
                            )
                        elif "defense" in selected_item:
                            player["Defense"] += selected_item["defense"]
                            print(
                                f"'{selected_item['name']}'을(를) 장착하여 방어력이 {selected_item['defense']} 증가했습니다."
                            )
                        else:
                            player["Inventory"].append(selected_item["name"])
                            print(
                                f"'{selected_item['name']}'을(를) 구매했습니다. 인벤토리에 추가됨."
                            )

                    else:
                        print("💰 골드가 부족합니다.")
                else:
                    print("⚠️ 잘못된 번호입니다.")
            except ValueError:
                print("⚠️ 숫자를 입력해주세요.")

    # ----------------------------------------------------
    # 2-2. 사냥터 가기 로직 (while, if, for, 딕셔너리)
    elif choice == "2":
        # 몬스터 무작위 선택
        monster_template = random.choice(monsters)
        current_monster = monster_template.copy()

        print(
            f"\n🔥 야생의 **{current_monster['name']}** (HP: {current_monster['HP']}) 이(가) 나타났습니다!"
        )

        # 전투 루프 (while)
        battle_running = True
        while battle_running and player["HP"] > 0 and current_monster["HP"] > 0:
            print("\n--- 전투 중 ---")
            print(f"당신의 HP: {player['HP']} | 몬스터 HP: {current_monster['HP']}")

            action = input("행동을 선택하세요 (1: 공격, 2: 아이템 사용): ")

            if action == "1":
                # 플레이어 공격
                player_damage = max(1, player["Attack"] + random.randint(-5, 5))
                current_monster["HP"] -= player_damage
                print(
                    f"🗡️ 공격! {current_monster['name']}에게 {player_damage} 피해를 입혔습니다."
                )

                # if: 몬스터 사망 확인
                if current_monster["HP"] <= 0:
                    print(f"\n🎉 **{current_monster['name']}** 를(을) 물리쳤습니다!")
                    player["Gold"] += current_monster["Gold"]
                    print(
                        f"💰 골드 {current_monster['Gold']} 획득! 현재 골드: {player['Gold']}"
                    )
                    battle_running = False  # 전투 종료
                    continue  # 다음 메인 루프로 이동

                # 몬스터 반격
                monster_damage = max(
                    1,
                    current_monster["Attack"]
                    - player["Defense"]
                    + random.randint(-2, 2),
                )
                player["HP"] -= monster_damage
                print(
                    f"💥 {current_monster['name']}의 반격! {monster_damage} 피해를 입었습니다."
                )

            elif action == "2":
                # 전투 중 아이템 사용 로직 (인벤토리/딕셔너리 사용)

                # 인벤토리 목록 출력 (for)
                print("\n--- 인벤토리 목록 ---")

                # 임시 인덱스 및 출력용 변수 설정
                idx = 0
                for item_name in player["Inventory"]:
                    print(f"[{idx + 1}] {item_name}", end=" ")
                    idx += 1
                print()

                use_choice = input("사용할 아이템 번호 (취소: 0): ")

                if use_choice != "0":
                    try:
                        item_index = int(use_choice) - 1

                        if 0 <= item_index < len(player["Inventory"]):
                            item_to_use = player["Inventory"][item_index]

                            # 포션 아이템 정보를 shop_items에서 찾기 (for, if, 딕셔너리)
                            potion_data = None
                            for item in shop_items:
                                if item["name"] == item_to_use and "heal" in item:
                                    potion_data = item
                                    break

                            if potion_data:
                                heal_amount = potion_data["heal"]
                                player["HP"] = min(
                                    player["Max_HP"], player["HP"] + heal_amount
                                )
                                print(
                                    f"💖 포션을 사용하여 HP {heal_amount} 회복! 현재 HP: {player['HP']}"
                                )
                                player["Inventory"].pop(item_index)
                            else:
                                print(f"'{item_to_use}'는 사용할 수 없는 아이템입니다.")
                        else:
                            print("⚠️ 잘못된 번호입니다.")
                    except ValueError:
                        print("⚠️ 숫자를 입력해주세요.")

            else:
                print("⚠️ 잘못된 입력입니다. (1 또는 2)")

        # if: 플레이어 사망 시 게임 오버
        if player["HP"] <= 0:
            print("\n|☠️게임 오버☠️| 다음에 더 강해져서 돌아오세요.")
            game_running = False  # 메인 while 루프 종료

    # ----------------------------------------------------
    # 2-3. 메인 메뉴에서 아이템 사용 로직 (if, for, 딕셔너리, 리스트)
    elif choice == "3":
        print("\n--- 아이템 사용 ---")
        if not player["Inventory"]:
            print("인벤토리가 비어 있습니다.")
            continue

        # 인벤토리 목록 출력 (for)
        idx = 0
        for item_name in player["Inventory"]:
            print(f"[{idx + 1}] {item_name}", end=" ")
            idx += 1
        print()

        use_choice = input("사용할 아이템 번호 (취소: 0): ")

        if use_choice != "0":
            try:
                item_index = int(use_choice) - 1

                if 0 <= item_index < len(player["Inventory"]):
                    item_to_use = player["Inventory"][item_index]

                    potion_data = None
                    for item in shop_items:
                        if item["name"] == item_to_use and "heal" in item:
                            potion_data = item
                            break

                    if potion_data:
                        heal_amount = potion_data["heal"]
                        player["HP"] = min(player["Max_HP"], player["HP"] + heal_amount)
                        print(
                            f"💖 포션을 사용하여 HP {heal_amount} 회복! 현재 HP: {player['HP']}"
                        )
                        player["Inventory"].pop(item_index)
                    else:
                        print(f"'{item_to_use}'는 사용할 수 없는 아이템입니다.")
                else:
                    print("⚠️ 잘못된 번호입니다.")
            except ValueError:
                print("⚠️ 숫자를 입력해주세요.")

    # ----------------------------------------------------
    # 2-4. 종료 로직 (if)
    elif choice == "4":
        print("👋 게임을 종료합니다.")
        game_running = False

    else:
        print("⚠️ 잘못된 선택입니다. 1, 2, 3, 4 중 하나를 입력해주세요.")
