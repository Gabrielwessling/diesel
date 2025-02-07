import json
from components.ai import HostileEnemy
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.spawn_curve import SpawnCurve
from components.inventory import Inventory
from entity import Actor, Item, Chest
from components.skill_list import SkillList
from typing import Tuple

class EntityFactories:
    def __init__(self, engine, gamemap, json_file="data/items.json", enemies_json="data/enemies.json"):
        # Initializing lists
        self.monsters = []
        self.items = []
        self.key_items = []
        self.chests = []
        self.engine = engine
        self.gamemap = gamemap
        
        # Initialize Player
        self.player = Actor(
            char=chr(500),
            color=(255, 255, 255),
            name="Player",
            ai_cls=HostileEnemy,
            equipment=Equipment(),
            fighter=Fighter(hp=30, base_defense=1, base_power=2),
            spawn_curve=None,
            inventory=Inventory(capacity=26, max_weight=55),
            skill_list=SkillList(parent=gamemap, engine=engine),  # Actor itself is the parent for its own data
        )
        
        # Initialize Key Items and add to the key_items list
        self.key = Item(
            char=chr(868),
            color=(255, 255, 255),
            name="Key",
            weight=0.01,
            key_id=0
        )
        self.key_items.append(self.key)

        # Initialize Chests and add to the chests list
        self.container = Chest(
            char=chr(1069),
            color=(255, 255, 255),
            name="Container",
            locked=False,
            chest_id=0,
            breakable=True,
            items=[],
        )
        self.chests.append(self.container)

        # Load data from JSON for items
        with open(json_file, "r") as file:
            data = json.load(file)
        
        # Create consumables
        for consumable_data in data["items"]["consumables"]:
            item = self.create_consumable(consumable_data)
            item.consumable.parent = item
            self.items.append(item)

        # Create equipables
        for equipable_data in data["items"]["equipables"]:
            item = self.create_equipable(equipable_data)
            item.equippable.parent = item
            self.items.append(item)
        
        # Load enemies data
        with open(enemies_json, "r") as file:
            enemies_data = json.load(file)["enemies"]

        # Initialize Monsters and add to the monsters list
        for enemy_data in enemies_data:
            monster = Actor(
                char=chr(int(enemy_data["char"])),
                color=(255,255,255),
                name=enemy_data["name"],
                ai_cls=HostileEnemy,
                equipment=Equipment(),
                fighter=Fighter(hp=enemy_data["fighter"]["hp"], 
                                base_defense=enemy_data["fighter"]["base_defense"], 
                                base_power=enemy_data["fighter"]["base_power"]),
                inventory=Inventory(capacity=enemy_data["inventory"]["capacity"], 
                                     max_weight=enemy_data["inventory"]["max_weight"]),
                skill_list=SkillList(parent=gamemap, engine=engine),
                spawn_curve=SpawnCurve(min_prob=enemy_data["min_prob"], peak_prob=enemy_data["peak_prob"], start_floor=enemy_data["start_floor"],
                                       peak_floor=enemy_data["peak_floor"], end_floor=enemy_data["end_floor"])
            )
            self.monsters.append(monster)
        
    def parse_color(self, color_str: str) -> Tuple[int, int, int]:
        """Parse a color string like '255,0,0' into a tuple (255, 0, 0)."""
        return (255,255,255)

    def create_consumable(self, data) -> Item:
        """Create a consumable item from JSON data."""
        name = data["name"]
        char = chr(int(data["char"]))
        color = (255,255,255)
        weight = float(data["weight"])

        # Dynamically get the consumable class
        consumable_class = getattr(consumable, data["consumableClass"])

        # Gather arguments dynamically for the consumable
        consumable_args = {}
        for key, value in data.items():
            if key not in {"name", "char", "color", "consumableClass", "weight"}:
                consumable_args[key] = float(value) if "." in str(value) else int(value)

        return Item(
            char=char,
            color=color,
            name=name,
            consumable=consumable_class(parent=None, **consumable_args),
            weight=weight,
        )

    def create_equipable(self, data) -> Item:
        """Create an equipable item from JSON data."""
        name = data["name"]
        char = chr(int(data["char"]))
        color = self.parse_color(data["color"])
        weight = float(data["weight"])

        # Dynamically get the equippable class
        equippable_class = getattr(equippable, data["equippableClass"])

        return Item(
            char=char,
            color=color,
            name=name,
            equippable=equippable_class(parent=None),
            weight=weight,
        )