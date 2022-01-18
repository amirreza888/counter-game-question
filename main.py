def standard_time(string_time):
    mm, ss, ttt = map(int, string_time.split(":"))
    return 60 * 1000 * mm + 1000 * ss + ttt


class Player():
    usernames_map = dict()

    def __init__(self, username, team, time):
        if (self.__initialized):
            return
        self.__initialized = True
        self.username = username
        self.money = 1000
        self.team = team
        self.kill_count = 0
        self.killed_count = 0
        self.heavy = None
        self.pistol = None
        self.knife = gun_map.get("knife")
        self.health = 100
        if standard_time(time) >= standard_time("00:03:00"):
            self.health = 0

    def __new__(cls, username, *args, **kwargs):
        if not cls.usernames_map.get(username):
            cls.usernames_map[username] = super(Player, cls).__new__(cls)
            cls.usernames_map[username].__initialized = False
            return cls.usernames_map.get(username)
        return None

    @classmethod
    def get_user(cls, user_name, ):
        player = cls.usernames_map.get(user_name)
        if not player:
            print("invalid username")
        return player

    @classmethod
    def get_money(cls, user_name, *arg):
        player = cls.get_user(user_name)
        if player:
            print(player.money)

    @classmethod
    def get_health(cls, user_name, *arg):
        player = cls.get_user(user_name)
        if player:
            print(player.health)

    @classmethod
    def attack(cls, attacker_user_name, attacked_username, gun_type, time):
        attacker = cls.get_user(attacker_user_name)
        if not attacker:
            return

        attacked = cls.get_user(attacked_username)
        if not attacked:
            return

        if attacker.health == 0:
            print("attacker is dead")
        elif attacked.health == 0:
            print("attacked is dead")
        elif not attacker.__getattribute__(gun_type):
            print("no such gun")
        elif attacker.team == attacked.team:
            print("friendly fire")
        else:
            print("nice shot")
            attacker_gun = attacker.__getattribute__(gun_type)
            attacked.health -= attacker_gun.damage
            if attacked.health <= 0:
                attacked.health = 0
                attacked.heavy = None
                attacked.pistol = None
                attacked.killed_count += 1
                attacker.kill_count += 1
                attacker.money += attacker_gun.reward_amount
                attacker.money = min(attacker.money, 10_000)

    @classmethod
    def buy_gun(cls, user_name, gun_name, time):
        player = cls.get_user(user_name)
        gun_instance = gun_map[gun_name]
        if player:
            if player.health:
                if standard_time(time) < standard_time("00:45:00"):
                    if player.team in gun_instance.teams:
                        if not player.__getattribute__(gun_instance.gun_type):
                            if player.money >= gun_instance.price:
                                print("I hope you can use it")
                                player.money -= gun_instance.price
                                player.__setattr__(gun_instance.gun_type, gun_instance)
                            else:
                                print("no enough money")
                        else:
                            print(f"you have a {gun_instance.gun_type}")
                    else:
                        print("invalid category gun")
                else:
                    print("you are out of time")
            else:
                print("deads can not buy")

    @classmethod
    def start_new_round(cls):
        for k in cls.usernames_map.keys():
            cls.usernames_map[k].health = 100


class Team():
    team_name_map = dict()

    def __init__(self, name):
        if (self.__initialized):
            return
        self.__initialized = True
        self.name = name
        self.players = list()
        self.won_count = 0

    def __new__(cls, name, *args, **kwargs):
        if not cls.team_name_map.get(name):
            cls.team_name_map[name] = super(Team, cls).__new__(cls)
            cls.team_name_map[name].__initialized = False
        return cls.team_name_map[name]

    def add_player(self, user_name, time):
        if Player.usernames_map.get(user_name):
            print("you are already in this game")
        elif len(self.players) == 10:
            print("this team is full")
        else:
            print(f"this user added to {self.name}")
            player = Player(username=user_name, team=self, time= time)
            Player.usernames_map[user_name] = player
            self.players.append(player)

    def win(self):
        for player in self.players:
            player.money += 2700
            if player.money > 10_000:
                player.money = 10_000

    def loss(self):
        for player in self.players:
            player.money += 2400
            if player.money > 10_000:
                player.money = 10_000

    def show_board(self):
        print(f"{self.name}-Players:")
        self.players.sort(key= lambda x:(x.kill_count, -x.killed_count,))
        for i, player in enumerate(self.players):
            print(i+1, player.username, player.kill_count, player.killed_count)


class Gun():

    def __init__(self, name, damage, price, reward_amount, gun_type, teams):
        self.name = name
        self.damage = damage
        self.price = price
        self.reward_amount = reward_amount
        self.gun_type = gun_type
        self.teams = []
        for team in teams:
            self.teams.append(Team(name=team))


gun_map = {
    "AK": Gun(name="AK", damage=31, price=2700, reward_amount=100, gun_type="heavy", teams=["Terrorist"]),
    "AWP": Gun(name="AWP", damage=110, price=4300, reward_amount=50, gun_type="heavy", teams=["Terrorist", "Counter-Terrorist"]),
    "Revolver": Gun(name="Revolver", damage=51, price=600, reward_amount=150, gun_type="pistol", teams=["Terrorist"]),
    "Glock-18": Gun(name="Glock-18", damage=11, price=300, reward_amount=200, gun_type="pistol",teams=["Terrorist"]),
    "knife": Gun(name="knife", damage=43, price=None, reward_amount=500, gun_type="knife", teams=["Terrorist", "Counter-Terrorist"]),
    "M4A1": Gun(name="M4A1", damage=29, price=2700, reward_amount=100, gun_type="heavy", teams=["Counter-Terrorist"]),
    "Desert-Eagle": Gun(name="Desert-Eagle", damage=53, price=600, reward_amount=175, gun_type="pistol",teams=["Counter-Terrorist"]),
    "UPS-S": Gun(name="UPS-S", damage=13, price=300, reward_amount=225, gun_type="pistol", teams=["Counter-Terrorist"]),
}

R = int(input())

round_number = 0

while round_number < R:
    round_number += 1
    n = int(input().split()[1])
    Player.start_new_round()
    for i in range(n):
        input_command = input().split()
        if input_command[0] == "ADD-USER":
            _, user_name, team_name, time = input_command
            Team(team_name).add_player(user_name, time)
        elif input_command[0] == "GET-MONEY":
            _, user_name, time = input_command
            Player.get_money(user_name)
        elif input_command[0] == "GET-HEALTH":
            _, user_name, time = input_command
            Player.get_health(user_name)
        elif input_command[0] == "TAP":
            _, attacker, attacked, gun_type, time = input_command
            Player.attack(attacker, attacked, gun_type, time)
        elif input_command[0] == "BUY":
            _, username, gun_name, time = input_command
            Player.buy_gun(username, gun_name, time)
        elif input_command[0] == "SCORE-BOARD":
            Team("Counter-Terrorist").show_board()
            Team("Terrorist").show_board()

    ct_lives_count = sum(x.health > 0 for x in Team("Counter-Terrorist").players)
    tr_lives_count = sum(x.health > 0 for x in Team("Terrorist").players)

    if ct_lives_count and not tr_lives_count:
        print("Counter-Terrorist won")
        Team("Counter-Terrorist").win()
        Team("Terrorist").loss()
    elif not ct_lives_count and tr_lives_count:
        print("Terrorist won")
        Team("Terrorist").win()
        Team("Counter-Terrorist").loss()
    else:
        print("Counter-Terrorist won")
        Team("Counter-Terrorist").win()
        Team("Terrorist").loss()
