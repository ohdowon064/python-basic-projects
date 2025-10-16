import random
import time

# --- 클래스(Class) 정의: 게임 세계의 설계도 ---


class Character:
    """
    모든 캐릭터(플레이어, 몬스터)의 기본이 되는 부모 클래스임.
    속성: 이름(name), 체력(hp), 공격력(power)
    메서드: attack(), is_alive(), show_status()
    """

    # 생성자: 객체가 만들어질 때 기본적인 능력치를 설정함.
    def __init__(self, name, hp, power):
        self.name = name  # 이름
        self.max_hp = hp  # 최대 체럭
        self.hp = hp  # 현재 체력
        self.power = power  # 공격력

    # attack 메서드: 대상을 공격하는 기능임.
    def attack(self, target):
        # 공격력은 power 값 기준으로 랜덤하게 정해짐.
        damage = random.randint(self.power - 2, self.power + 2)
        target.hp -= damage
        print(f"{self.name}의 공격! {target.name}에게 {damage}의 데미지를 입혔음.")
        # f-string을 사용해 공격 로그를 실감 나게 출력함.

    # is_alive 메서드: 캐릭터의 생존 여부(True/False)를 반환함.
    def is_alive(self):
        return self.hp > 0

    # show_status 메서드: 현재 상태를 보여줌.
    def show_status(self):
        print(f"[{self.name}] HP: {self.hp}/{self.max_hp}")


class Player(Character):
    """
    Character 클래스를 상속받는 플레이어 클래스임.
    추가 속성: 레벨(level), 경험치(exp), 마나(mp)
    추가 메서드: gain_exp(), use_skill()
    """

    def __init__(self, name, hp, power):
        # super()를 이용해 부모 클래스의 생성자를 호출함.
        super().__init__(name, hp, power)
        self.level = 1  # 레벨
        self.exp = 0  # 현재 경험치
        self.max_exp = 10 * self.level  # 레벨업 경험치
        self.max_mp = 30  # 최대 마나
        self.mp = 30  # 현재 마나

    # use_skill 메서드: 스킬을 사용하는 기능임.
    def use_skill(self, target):
        skill_cost = 10
        # if 조건문: 마나가 충분한지 확인함.
        if self.mp >= skill_cost:
            self.mp -= skill_cost
            damage = self.power * 2  # 스킬은 일반 공격의 2배 데미지
            target.hp -= damage
            print(f"✨ {self.name}의 스킬! '강력한 일격' 발동! (MP {skill_cost} 소모)")
            print(f"{target.name}에게 {damage}의 엄청난 데미지를 입혔음.")
            return True  # 스킬 사용 성공
        else:
            print("MP가 부족하여 스킬을 사용할 수 없음.")
            return False  # 스킬 사용 실패

    # gain_exp 메서드: 경험치를 얻고 레벨업을 처리함.
    def gain_exp(self, amount):
        self.exp += amount
        print(f"{amount}의 경험치를 획득했음. (현재 경험치: {self.exp}/{self.max_exp})")

        # while 반복문: 경험치가 충분하면 여러 번 레벨업 가능하도록 수정
        while self.exp >= self.max_exp:
            self.level += 1
            self.exp -= self.max_exp
            self.max_exp = 10 * self.level
            # 레벨업 보상 강화
            self.max_hp += 20
            self.hp = self.max_hp  # 체력 전체 회복
            self.power += 3
            self.max_mp += 5
            self.mp = self.max_mp  # 마나 전체 회복
            print(
                f"🎉 레벨 업! {self.level}레벨이 되었음. 모든 능력치가 상승하고 체력과 마나가 회복됨."
            )

    # 메서드 오버라이딩: 부모의 show_status를 재정의해서 추가 정보 출력.
    def show_status(self):
        print(
            f"[{self.name} (Lv.{self.level})] HP: {self.hp}/{self.max_hp} | MP: {self.mp}/{self.max_mp} | EXP: {self.exp}/{self.max_exp}"
        )


class Monster(Character):
    """
    Character 클래스를 상속받는 몬스터 클래스임.
    추가 속성: 처치 시 얻는 경험치(exp_reward)
    """

    def __init__(self, name, hp, power, exp_reward):
        super().__init__(name, hp, power)
        self.exp_reward = exp_reward


class Dungeon:
    """
    던전의 상태를 관리하는 클래스임.
    속성: 현재 층(current_floor), 최대 층(max_floor)
    메서드: next_floor(), generate_monster(), is_cleared()
    """

    def __init__(self):
        self.current_floor = 1
        self.max_floor = 10

    def next_floor(self):
        self.current_floor += 1
        print(f"\n던전 {self.current_floor}층으로 내려갔음.")

    def generate_monster(self):
        # 층이 깊어질수록 강한 몬스터가 나옴.
        if self.current_floor <= 3:
            base_hp = 30 + self.current_floor * 5
            base_power = 5 + self.current_floor
            hp = random.randint(int(base_hp * 0.9), int(base_hp * 1.1))
            power = random.randint(int(base_power * 0.9), int(base_power * 1.1))
            monster = Monster("슬라임", hp, power, 5 * self.current_floor)
        elif self.current_floor <= 7:
            base_hp = 50 + self.current_floor * 8
            base_power = 8 + self.current_floor
            hp = random.randint(int(base_hp * 0.9), int(base_hp * 1.1))
            power = random.randint(int(base_power * 0.9), int(base_power * 1.1))
            monster = Monster("고블린", hp, power, 10 * self.current_floor)
        elif self.current_floor < self.max_floor:
            base_hp = 80 + self.current_floor * 12
            base_power = 12 + self.current_floor
            hp = random.randint(int(base_hp * 0.9), int(base_hp * 1.1))
            power = random.randint(int(base_power * 0.9), int(base_power * 1.1))
            monster = Monster("오크", hp, power, 15 * self.current_floor)
        else:  # 마지막 10층 보스
            base_hp = 300
            base_power = 40
            hp = random.randint(int(base_hp * 0.9), int(base_hp * 1.1))
            power = random.randint(int(base_power * 0.9), int(base_power * 1.1))
            monster = Monster("던전의 지배자 드래곤", hp, power, 100)
        return monster

    def is_cleared(self):
        return self.current_floor > self.max_floor


# --- 함수(Function) 정의: 게임의 각 기능을 담당하는 부품 ---


def start_battle(player, monster):
    """
    전투를 진행하는 함수.
    플레이어와 몬스터 객체를 인자로 받음.
    플레이어가 승리하면 True, 패배하거나 도망치면 False를 반환함.
    """
    print(f"\n야생의 {monster.name}이(가) 나타났다!")

    # while 반복문: 둘 중 하나가 쓰러질 때까지 전투를 반복함.
    while player.is_alive() and monster.is_alive():
        print("\n--- 전투 메뉴 ---")
        player.show_status()
        monster.show_status()

        # try-except 예외 처리: 사용자가 숫자 외의 값을 입력했을 때 프로그램이 멈추지 않도록 함.
        try:
            choice = input("어떻게 할까? (1. 공격 | 2. 스킬 | 3. 도망가기)\n> ")

            player_turn_ended = False
            # if/elif/else 조건문: 사용자의 선택에 따라 다른 동작을 함.
            if choice == "1":
                # 플레이어의 턴
                player.attack(monster)
                player_turn_ended = True

            elif choice == "2":
                # 플레이어의 스킬 턴
                if player.use_skill(monster):
                    player_turn_ended = True

            elif choice == "3":
                print("무사히 도망쳤다.")
                return False  # 도망은 패배로 간주

            else:
                print("잘못된 입력입니다.")

            # 플레이어의 턴이 유효하게 끝났을 때만 몬스터가 공격함
            if player_turn_ended:
                # 몬스터 생존 확인
                if not monster.is_alive():
                    print(f"{monster.name}을(를) 물리쳤다!")
                    player.gain_exp(monster.exp_reward)
                    return True  # 플레이어 승리

                time.sleep(1)  # 잠시 멈춰서 게임 진행 속도를 조절함.

                # 몬스터의 턴
                monster.attack(player)
                if not player.is_alive():
                    print("눈앞이 깜깜해졌다...")
                    return False  # 플레이어 패배

        except Exception as e:
            print(f"예상치 못한 오류가 발생했습니다: {e}")

    return False  # 비정상적인 경우 패배 처리


# --- 메인 게임 실행 부분 ---


def main():
    """
    게임의 전체적인 흐름을 관리하는 메인 함수.
    """
    player_name = input("플레이어의 이름을 입력하세요: ")
    # Player 클래스로 플레이어 객체를 생성함.
    player = Player(player_name, 100, 10)
    # Dungeon 클래스로 던전 객체를 생성함.
    dungeon = Dungeon()

    print(f"\n용사 {player.name}님, 던전에 오신 것을 환영합니다.")

    # while 반복문: 게임의 메인 루프. 사용자가 종료를 원할 때까지 계속됨.
    while True:
        print("\n--- 메인 메뉴 ---")
        # 현재 던전 층수를 메뉴에 표시함.
        menu = input(
            f"어디로 갈까? (1. 던전 {dungeon.current_floor}층 탐험 | 2. 내 정보 보기 | 3. 종료)\n> "
        )

        if menu == "1":
            # 던전 객체를 통해 현재 층에 맞는 몬스터를 생성함.
            monster = dungeon.generate_monster()

            battle_won = start_battle(player, monster)

            # 전투 후 플레이어의 생존 여부를 확인.
            if not player.is_alive():
                print("\nGAME OVER")
                break

            # 전투에서 승리했을 경우에만 다음 층으로 이동함.
            if battle_won:
                dungeon.next_floor()
                # 던전 클리어 여부 확인
                if dungeon.is_cleared():
                    print("\n마침내 던전의 지배자를 물리쳤다!")
                    print("던전을 탈출하고 현실세계로 돌아왔습니다.")
                    print("GAME CLEAR!")
                    break

        elif menu == "2":
            player.show_status()

        elif menu == "3":
            print("게임을 종료합니다.")
            break

        else:
            print("잘못된 입력입니다.")


# 이 스크립트 파일이 직접 실행될 때만 main() 함수를 호출함.
if __name__ == "__main__":
    main()
