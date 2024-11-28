from components.ai import HostileEnemy
from components import consumable
from components.fighter import Fighter
from components.inventory import Inventory
from entity import Actor, Item, Chest
from components.skill_list import SkillList
import random

monsters = []
items = []
key_items = []
chests = []

#---------------------------------PLAYER
player = Actor(
    char="@",
    color=(50, 20, 20),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, defense=2, power=5),
    inventory=Inventory(capacity=26, max_weight=55),
    skill_list=SkillList,
)
#---------------------------------MONSTERS
vagabundo = Actor(
    char="v",
    color=(127, 63, 63),
    name="Vagabundo",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=0, power=3),
    inventory=Inventory(capacity=26, max_weight=55),
    skill_list=SkillList,
)
bandido = Actor(
    char="b",
    color=(120, 70, 40),
    name="Bandido",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=5, defense=4, power=1),
    inventory=Inventory(capacity=26, max_weight=55),
    skill_list=SkillList,
)
viciado = Actor(
    char="V",
    color=(0, 127, 0),
    name="Viciado",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, defense=1, power=3),
    inventory=Inventory(capacity=26, max_weight=55),
    skill_list=SkillList,
)
cachorro = Actor(
    char="c",
    color=(120, 60, 30),
    name="Cao Sarnento",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=1, defense=0, power=5),
    inventory=Inventory(capacity=1, max_weight=30),
    skill_list=SkillList,
)
mecanico = Actor(
    char="m",
    color=(120, 60, 120),
    name="Mecânico Louco",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=20, defense=-2, power=1),
    inventory=Inventory(capacity=26, max_weight=55),
    skill_list=SkillList(),
)
#---------------------------------ITEMS
cachaca = Item(
    char="!",
    color=(255, 0, 100),
    name="Garrafa de 51",
    consumable=consumable.HealingConsumable(amount=4),
    weight=1.45
)
bateria_estragada = Item(
    char="}",
    color=(200, 200, 0),
    name="Pilha Estragada",
    consumable=consumable.LightningDamageConsumable(damage=15, maximum_range=5),
    weight=0.07
)
lancador_de_crack = Item(
    char="=",
    color=(207, 63, 255),
    name="Lancador de Crack",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
    weight=1.34
)
molotov = Item(
    char="~",
    color=(255, 0, 0),
    name="Coquetel Molotov",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
    weight=1.65
)
#---------------------------------KEY ITEMS
chave = Item(
    char=";",
    color=(100, 100, 100),
    name="Chave",
    consumable=consumable.HealingConsumable(0),
    weight=0.01,
    key_id=0
)
#---------------------------------CHESTS
chest = Chest(
    char="C",
    color=(150, 150, 50),
    name="Caixa",
    locked=False,
    chest_id=0,
    breakable=True,
    items=[],
)


#APPENDS
monsters.append(vagabundo)
monsters.append(bandido)
monsters.append(viciado)
monsters.append(cachorro)

items.append(cachaca)
items.append(bateria_estragada)
items.append(lancador_de_crack)
items.append(molotov)

key_items.append(chave)

chests.append(chest)