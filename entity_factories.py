import xml.etree.ElementTree as ET
from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from entity import Actor, Item, Chest
from components.skill_list import SkillList
from typing import Tuple
import random

class EntityFactories:
    def __init__(self, engine, gamemap, xml_file="data\items.xml"):
        # Initializing lists
        self.monsters = []
        self.items = []
        self.key_items = []
        self.chests = []
        self.engine = engine
        self.gamemap = gamemap
        
        # Initialize Player
        self.player = Actor(
            char="@",
            color=(50, 20, 20),
            name="Player",
            ai_cls=HostileEnemy,
            equipment=Equipment(),
            fighter=Fighter(hp=30, base_defense=1, base_power=2),
            inventory=Inventory(capacity=26, max_weight=55),
            skill_list=SkillList(parent=gamemap, engine=engine),  # Actor itself is the parent for its own data
        )
        
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
            color=(77, 77, 15),
            name="Caixa",
            locked=False,
            chest_id=0,
            breakable=True,
            items=[],
        )
        self.chests.append(self.chest)

        # Load data from XML
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Create consumables
        for consumable in root.find("consumables").findall("item"):
            item = self.create_consumable(consumable)
            item.consumable.parent = item
            self.items.append(item)

        # Create equipables
        for equipable in root.find("equipables").findall("item"):
            item = self.create_equipable(equipable)
            item.equippable.parent = item
            self.items.append(item)
            
        #temp
        # Initialize Monsters and add to the monsters list
        self.vagabundo = Actor(
            char="v",
            color=(127, 63, 63),
            name="Vagabundo",
            ai_cls=HostileEnemy,
            equipment=Equipment(),
            fighter=Fighter(hp=10, base_defense=0, base_power=3),
            inventory=Inventory(capacity=26, max_weight=55),
            skill_list=SkillList(parent=gamemap, engine=engine),
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
            skill_list=SkillList(parent=gamemap, engine=engine),
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
            skill_list=SkillList(parent=gamemap, engine=engine),
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
            skill_list=SkillList(parent=gamemap, engine=engine),
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
            skill_list=SkillList(parent=gamemap, engine=engine),
        )
        self.monsters.append(self.mecanico)
        
    def parse_color(self, color_str: str) -> Tuple[int, int, int]:
        """Parse a color string like '255,0,0' into a tuple (255, 0, 0)."""
        return tuple(map(int, color_str.split(",")))

    def create_consumable(self, data) -> Item:
        """Create a consumable item from XML data."""
        name = data.find("name").text
        char = data.find("char").text
        color = self.parse_color(data.find("color").text)
        weight = float(data.find("weight").text)

        # Dynamically get the consumable class
        consumable_class = getattr(consumable, data.find("consumableClass").text)

        # Gather arguments dynamically
        consumable_args = {}
        for arg in data:
            if arg.tag not in {"name", "char", "color", "consumableClass", "weight"}:
                consumable_args[arg.tag] = float(arg.text) if "." in arg.text else int(arg.text)

        return Item(
            char=char,
            color=color,
            name=name,
            consumable=consumable_class(parent=None, **consumable_args),
            weight=weight,
        )

    def create_equipable(self, data) -> Item:
        """Create an equipable item from XML data."""
        name = data.find("name").text
        char = data.find("char").text
        color = self.parse_color(data.find("color").text)
        weight = float(data.find("weight").text)

        # Dynamically get the equippable class
        equippable_class = getattr(equippable, data.find("equippableClass").text)

        return Item(
            char=char,
            color=color,
            name=name,
            equippable=equippable_class(parent=None),
            weight=weight,
        )  
        
        
        