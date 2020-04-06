from dungeons_and_pythons.logic import Dungeon
from dungeons_and_pythons.models import Human
from dungeons_and_pythons.models import Hero
from dungeons_and_pythons.models import Enemy
from dungeons_and_pythons.models import Weapon
from dungeons_and_pythons.models import Spell
from dungeons_and_pythons.models import Armor
from dungeons_and_pythons.models import Potion

def demo():
    h = Hero(name="Bron", title="Dragonslayer", health=100, mana=100, mana_regeneration_rate=2)

    w = Weapon(name="The Axe of Destiny", damage=20)
    h.equip(w)

    s = Spell(name="Fireball", damage=30, mana_cost=50, cast_range=2)
    h.equip(s)

    map = Dungeon("level1.txt")
    map.spawn(h)

    map.move_hero("right")

    map.move_hero("down")

    map.hero_attack(by="magic")

    map.move_hero("down")
    map.move_hero("down")

    map.move_hero("right")

    map.move_hero("right")
    map.move_hero("right")
    map.move_hero("right")
    map.move_hero("up")
    map.move_hero("up")
    map.move_hero("up")
    map.move_hero("right")
    map.move_hero("right")
    map.move_hero("right")
    map.move_hero("right")
    map.move_hero("down")
    map.move_hero("down")
    map.move_hero("down")
    map.move_hero("down")

def main():
    demo()

if __name__ == '__main__':
    main()
    