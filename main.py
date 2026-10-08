

# notes
# each kill increases damage stats
# not high enough and u die at the end to dragon shit


# imports

import random

# variables

NOM_MONSTRES = ["Gobelin", "Loup", "Dragon"]
DAYS_UNTIL_BOSS = 10
HERO_MAX_HEALTH = 20
BOSS_HEALTH = 30
BOSS_DMG = 10




day = 0
number_of_times_ran_away = 0
hero = None
current_monster = None


# classes

class Heros():
    """
    Class represantent le heros du jeu avec sa vie
    """
    def __init__(self, health):
        self.health = health
        self.damage_mod = 1
        

    
    def attack(self, monster):
        """
        Fonction qui permet au heros d'attaquer un monstre
        """
        damage = random.randint(1 + self.damage_mod, 5 + self.damage_mod) 
        monster.health -= damage
        print(f"Vous avez infligé {damage} points de dégats à {monster.name} !")
        if monster.health <= 0:
            print(f"Vous avez tué {monster.name} !")
            self.damage_mod += random.randint(0, 3)
            print("Vous vous sentez plus fort !")
            
    def take_damage(self, damage):
        """
        Fonction qui permet au heros de prendre des dégats
        """
        if damage < 0:
            damage = 0
        self.health -= damage
        print(f"Vous avez pris {damage} points de dégats !")

           
    def dont_fight(self):
        """
        Fonction qui permet au heros de ne pas combattre un monstre
        """
        global number_of_times_ran_away
        number_of_times_ran_away += 1
        print(f"Vous vous êtes enfui du combat !")
    

    def is_alive(self):
        """
        Fonction qui permet de savoir si le heros est vivant
        """
        return self.health > 0

    def afficher_etat(self):
        """
        Fonction qui permet d'afficher l'état du heros
        """
        print(f"Vous avez {self.health} points de vie et {self.damage_mod} puissance !")


class Monster():
    """
    Class represantent le monstre du jeu avec ses vie et ses points de degats
    """
    def __init__(self, health, damage, name):
        self.health = health
        self.damage = damage
        self.name = name
    def attack(self, hero):
        """
        Fonction qui permet au monstre d'attaquer le heros
        """
        if self.name == "Sorcière":
            if self.health < 10:
                move_choice = random.randint(1, 2)
                if move_choice == 1:
                    print(f"{self.name} utilise sa magie pour se soigner !")
                    self.health += random.randint(5, 10)
                    return False
                else:
                    hero.take_damage(self.damage + random.randint(-2, 2))
                    return True
            else:
                hero.take_damage(self.damage + random.randint(-2, 2))
                return True
        else:
            hero.take_damage(self.damage + random.randint(-2, 2))
            return True
    def take_damage(self, damage):
        """
        Fonction qui permet au monstre de prendre des dégats
        """
        self.health -= damage
        print(f"{self.name} a pris {damage} points de dégats !")
        if self.health <= 0:
            print(f"{self.name} est mort !")
        

def créer_monstre():
    """
    Fonction qui permet de créer un monstre aléatoire
    """
    health = random.randint(5, 15)
    damage = random.randint(1, 5)
    name = random.choice(NOM_MONSTRES)
    return Monster(health, damage, name)

# functions


def setup():
    """
    Setup du jeu, initialisation du heros et des variables 
    """
    global hero, day, number_of_times_ran_away, current_monster
    day = 0
    number_of_times_ran_away = 0
    current_monster = None
    hero = Heros(20)

def combat(hero, monster):
    """
    Fonction qui permet de gérer le combat entre le heros et le monstre
    """
    while monster.health > 0 and hero.health > 0:
        hero.attack(monster)
        if monster.health > 0:
            monster.attack(hero)
    if hero.health <= 0:
        print("Vous êtes mort !")
    return



playing = True

while playing:
    setup()
    loop = True
    voir_regles = input("Voulez-vous voir les règles du jeu ? (1) Oui (2) Non : ")    # Règles du jeu
    if voir_regles == "1":
        print("\n\n\n")
        print("Vous êtes un héros qui doit combattre des monstres pour survivre.")
        print("Chaque jour, vous pouvez rencontrer un monstre aléatoire.")
        print("Vous pouvez choisir de combattre le monstre, de fuir ou d'afficher votre état.")
        print("Si vous choisissez de combattre, vous et le monstre vous infligez des dégâts jusqu'à ce que l'un de vous soit mort.")
        print("Si vous fuyez, vous perdez des points de vie.")
        print("Après 10 jours, vous affronterez le boss final, la Sorcière. Bonne chance !")
        input("Appuyez sur Entrée pour continuer...")
        print("\n\n\n")
    while loop:
        day += 1
        print(f"--------------------------------- Jour {day} : ---------------------------------")

        heal = random.randint(-1, 5)
        if heal > 0 and not day == 1:     # Le héros récupère des points de vie chaque jour sauf le premier
            print(f"Vous récupérez {heal} points de vie avec un bon nuit de sommeil !")
            hero.health += heal
        if hero.health > HERO_MAX_HEALTH:   
            hero.health = HERO_MAX_HEALTH   # Prévenir que la vie du héros dépasse 20
        print(f"Vous avez {hero.health} points de vie .")
        if not day == DAYS_UNTIL_BOSS:
            current_monster = créer_monstre() # Créer un monstre aléatoire
            while current_monster.health > 0 and hero.health > 0:
                try:
                    choice : int = input(f"Un {current_monster.name} est apparu ! Que voulez-vous faire ? (1) Combattre (2) Fuir (3) Afficher l'état : ")
                    choice = int(choice)
                except ValueError:
                    print("Entrée invalide !")
                    continue
                if choice == 1:
                    while hero.health > 0 and current_monster.health > 0: 
                        combat(hero, current_monster)
                    if not hero.is_alive():
                       loop = False # Joueur est mort :(
                       break

                if choice == 2:
                    hero.dont_fight() # Joueur fuit le combat
                    break
                if choice == 3:
                    hero.afficher_etat()    
        else:
            print("Un Sorcière est apparu ! C'est le boss final !")
            if number_of_times_ran_away >= 5:
                print(f"Sorcière : 'Vous avez fui de mes monstres {number_of_times_ran_away} fois. Bonne chance...'")
            current_monster = Monster(BOSS_HEALTH, BOSS_DMG, "Sorcière")
            while current_monster.health > 0 and hero.health > 0:
                combat(hero, current_monster)
            if not hero.is_alive():
                loop = False # Joueur est mort :(
                break
            else:
                print("Vous avez vaincu le boss final ! Vous avez gagné !")
                loop = False
                break
    choice = 0
    while choice != 1 and choice != 2:
        try:
            choice : int = input(f"Voulez-vous rejouer ? (1) Oui (2) Non : ")
            choice = int(choice)
        except ValueError:
            print("Entrée invalide !")
            continue
    if choice == 2:
        playing = False
        print("Merci d'avoir joué !")
