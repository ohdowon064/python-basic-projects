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
        self.name = name
        self.hp = hp
        self.power = power

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
        print(f"[{self.name}] HP: {self.hp}")


class Player(Character):
    """
    Character 클래스를 상속받는 플레이어 클래스임.
    추가 속성: 레벨(level), 경험치(exp)
    추가 메서드: gain_exp()
    """

    def __init__(self, name, hp, power):
        # super()를 이용해 부모 클래스의 생성자를 호출함.
        super().__init__(name, hp, power)
        self.level = 1
        self.exp = 0
        self.max_exp = 10 * self.level

    # gain_exp 메서드: 경험치를 얻고 레벨업을 처리함.
    def gain_exp(self, amount):
        self.exp += amount
        print(f"{amount}의 경험치를 획득했음. (현재 경험치: {self.exp}/{self.max_exp})")

        # if 조건문: 경험치가 레벨업 요구치를 넘었는지 확인함.
        if self.exp >= self.max_exp:
            self.level += 1
            self.exp = 0
            self.max_exp = 10 * self.level
            self.hp += 10  # 레벨업 보상
            self.power += 2
            print(f"레벨 업! {self.level}레벨이 되었음.")

    # 메서드 오버라이딩: 부모의 show_status를 재정의해서 추가 정보 출력.
    def show_status(self):
        print(
            f"[{self.name} (Lv.{self.level})] HP: {self.hp} | EXP: {self.exp}/{self.max_exp}"
        )


class Monster(Character):
    """
    Character 클래스를 상속받는 몬스터 클래스임.
    추가 속성: 처치 시 얻는 경험치(exp_reward)
    """

    def __init__(self, name, hp, power, exp_reward):
        super().__init__(name, hp, power)
        self.exp_reward = exp_reward


# --- 함수(Function) 정의: 게임의 각 기능을 담당하는 부품 ---


def start_battle(player, monster):
    """
    전투를 진행하는 함수.
    플레이어와 몬스터 객체를 인자로 받음.
    """
    print(f"\n야생의 {monster.name}이(가) 나타났다!")

    # while 반복문: 둘 중 하나가 쓰러질 때까지 전투를 반복함.
    while player.is_alive() and monster.is_alive():
        print("\n--- 전투 메뉴 ---")
        player.show_status()
        monster.show_status()

        # try-except 예외 처리: 사용자가 숫자 외의 값을 입력했을 때 프로그램이 멈추지 않도록 함.
        try:
            choice = input("어떻게 할까? (1. 공격 | 2. 도망가기)\n> ")

            # if/elif/else 조건문: 사용자의 선택에 따라 다른 동작을 함.
            if choice == "1":
                # 플레이어의 턴
                player.attack(monster)
                if not monster.is_alive():
                    print(f"{monster.name}을(를) 물리쳤다!")
                    player.gain_exp(monster.exp_reward)
                    break

                time.sleep(1)  # 잠시 멈춰서 게임 진행 속도를 조절함.

                # 몬스터의 턴
                monster.attack(player)
                if not player.is_alive():
                    print("눈앞이 깜깜해졌다...")
                    break

            elif choice == "2":
                print("무사히 도망쳤다.")
                return  # 함수를 종료하여 전투를 끝냄.

            else:
                print("잘못된 입력입니다.")

        except Exception as e:
            print(f"예상치 못한 오류가 발생했습니다: {e}")


# --- 메인 게임 실행 부분 ---


def main():
    """
    게임의 전체적인 흐름을 관리하는 메인 함수.
    """
    player_name = input("플레이어의 이름을 입력하세요: ")
    # Player 클래스로 플레이어 객체를 생성함.
    player = Player(player_name, 100, 10)

    print(f"\n용사 {player.name}님, 던전에 오신 것을 환영합니다.")

    # while 반복문: 게임의 메인 루프. 사용자가 종료를 원할 때까지 계속됨.
    while True:
        print("\n--- 메인 메뉴 ---")
        menu = input("어디로 갈까? (1. 던전 탐험 | 2. 내 정보 보기 | 3. 종료)\n> ")

        if menu == "1":
            # 몬스터를 랜덤으로 생성함.
            monster_list = [
                Monster("슬라임", 30, 5, 5),
                Monster("고블린", 50, 8, 10),
                Monster("오크", 80, 12, 15),
            ]
            monster = random.choice(monster_list)

            start_battle(player, monster)

            # 전투 후 플레이어의 생존 여부를 확인.
            if not player.is_alive():
                print("\nGAME OVER")
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
