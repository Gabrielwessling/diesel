from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from entity import Actor, Item, Chest
from components.skill_list import SkillList
import random

class EntityFactories:
    def __init__(self, engine):
        # Initializing lists
        self.monsters = []
        self.items = []
        self.key_items = []
        self.chests = []

        # Initialize Player
        self.player = Actor(
            char="@",
            color=(50, 20, 20),
            name="Player",
            ai_cls=HostileEnemy,
            equipment=Equipment(),
            fighter=Fighter(hp=30, base_defense=1, base_power=2),
            inventory=Inventory(capacity=26, max_weight=55),
            skill_list=SkillList(parent=None, engine=engine),  # Actor itself is the parent for its own data
        )

        # Initialize Monsters and add to the monsters list
        self.vagabundo = Actor(
            char="v",
            color=(127, 63, 63),
            name="Vagabundo",
            ai_cls=HostileEnemy,
            equipment=Equipment(),
            fighter=Fighter(hp=10, base_defense=0, base_power=3),
            inventory=Inventory(capacity=26, max_weight=55),
            skill_list=SkillList(parent=None, engine=engine),
        )
        self.monsters.append(self.vagabundo)

        self.bandido = Actor(
            char="b",
            color=(120, 70, 40),
            name="Bandido",
            ai_cls=HostileEnemy,
            equipment=Equipment(),
            fighter=Fighter(hp=5, base_defense=1, base_power=1),
            inventory=Inventory(capacity=26, max_weight=55),
            skill_list=SkillList(parent=None, engine=engine),
        )
        self.monsters.append(self.bandido)

        self.viciado = Actor(
            char="V",
            color=(0, 127, 0),
            name="Viciado",
            ai_cls=HostileEnemy,
            equipment=Equipment(),
            fighter=Fighter(hp=16, base_defense=1, base_power=3),
            inventory=Inventory(capacity=26, max_weight=55),
            skill_list=SkillList(parent=None, engine=engine),
        )
        self.monsters.append(self.viciado)

        self.cachorro = Actor(
            char="c",
            color=(120, 60, 30),
            name="Cao Sarnento",
            ai_cls=HostileEnemy,
            equipment=Equipment(),
            fighter=Fighter(hp=1, base_defense=0, base_power=5),
            inventory=Inventory(capacity=1, max_weight=30),
            skill_list=SkillList(parent=None, engine=engine),
        )
        self.monsters.append(self.cachorro)

        self.mecanico = Actor(
            char="m",
            color=(120, 60, 120),
            name="Mecânico Louco",
            ai_cls=HostileEnemy,
            equipment=Equipment(),
            fighter=Fighter(hp=20, base_defense=-2, base_power=1),
            inventory=Inventory(capacity=26, max_weight=55),
            skill_list=SkillList(parent=None, engine=engine),
        )
        self.monsters.append(self.mecanico)

        ################################################################################################################
        # Initialize Items
        self.cachaca = Item(
            char="!",
            color=(255, 0, 100),
            name="Garrafa de 51",
            consumable=None,  # Initially set to None, will update later
            weight=1.45
        )
        # Assign the consumable to the item after initialization
        self.cachaca.consumable = consumable.HealingConsumable(amount=4, parent=self.cachaca)
        self.items.append(self.cachaca)

        self.bateria_estragada = Item(
            char="}",
            color=(200, 200, 0),
            name="Pilha Estragada",
            consumable=None,  # Initially set to None, will update later
            weight=0.07
        )
        # Assign the consumable to the item after initialization
        self.bateria_estragada.consumable = consumable.LightningDamageConsumable(damage=15, maximum_range=5, parent=self.bateria_estragada)
        self.items.append(self.bateria_estragada)

        self.lancador_de_crack = Item(
            char="=",
            color=(207, 63, 255),
            name="Lancador de Crack",
            consumable=None,  # Initially set to None, will update later
            weight=1.34
        )
        # Assign the consumable to the item after initialization
        self.lancador_de_crack.consumable = consumable.ConfusionConsumable(number_of_turns=10, parent=self.lancador_de_crack)
        self.items.append(self.lancador_de_crack)

        self.molotov = Item(
            char="~",
            color=(255, 0, 0),
            name="Coquetel Molotov",
            consumable=None,  # Initially set to None, will update later
            weight=1.65
        )
        # Assign the consumable to the item after initialization
        self.molotov.consumable = consumable.FireballDamageConsumable(damage=12, radius=3, parent=self.molotov)
        self.items.append(self.molotov)

        # The rest of your initialization code follows as normal
        # Initialize Equipment Items, Key Items, Chests, etc.

        ################################################################################## EQUIPS
        self.faca_desafiada = Item(
            char="/",
            color=(150,150,150),
            name="Faca Sem Fio",
            equippable=equippable.Dagger(),
            weight=0.15,
        )
        self.items.append(self.faca_desafiada)

        self.espada_fundo_de_garagem = Item(
            char="/",
            color=(215,200,150),
            name="Espada Fundo de Garagem",
            equippable=equippable.Sword(),
            weight=0.4,
        )
        self.items.append(self.espada_fundo_de_garagem)

        self.porrete = Item(
            char="\\",
            color=(15,15,55),
            name="Porrete Ex-Policial",
            equippable=equippable.Hammer(),
            weight=0.5,
        )
        self.items.append(self.porrete)

        self.espeto = Item(
            char="|",
            color=(255,50,200),
            name="Espeta Otario",
            equippable=equippable.Spear(),
            weight=0.7,
        )
        self.items.append(self.espeto)

        self.machado_de_assis = Item(
            char="+",
            color=(255,70,80),
            name="Machado 'Diassis'",
            equippable=equippable.Axe(),
            weight=0.4,
        )
        self.items.append(self.machado_de_assis)

        self.pedra = Item(
            char="o",
            color=(30,30,55),
            name="Pedra",
            equippable=equippable.Rock(),
            weight=0.15,
        )
        self.items.append(self.pedra)

        self.arco = Item(
            char="/",
            color=(200,200,100),
            name="Apenas Arco",
            equippable=equippable.Bow(),
            weight=0.3,
        )
        self.items.append(self.arco)

        self.mugger_73 = Item(
            char="¬",
            color=(150,150,150),
            name="Pistola Mugger-73",
            equippable=equippable.Pistol(),
            weight=0.4,
        )
        self.items.append(self.mugger_73)

        # Initialize Key Items and add to the key_items list
        self.chave = Item(
            char=";",
            color=(100, 100, 100),
            name="Chave",
            weight=0.01,
            key_id=0
        )
        self.key_items.append(self.chave)

        # Initialize Chests and add to the chests list
        self.chest = Chest(
            char="C",
            color=(150, 150, 50),
            name="Caixa",
            locked=False,
            chest_id=0,
            breakable=True,
            items=[],
        )
        self.chests.append(self.chest)