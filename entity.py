from __future__ import annotations # Primeiro

import copy # imports aleatorios
import math

from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING, Union, List

from render_order import RenderOrder # imports de dentro
import exceptions
from game_map import GameMap

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.consumable import Consumable
    from components.equippable import Equippable
    from components.equipment import Equipment
    from components.fighter import Fighter
    from components.inventory import Inventory
    from components.skill_list import SkillList

T = TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    parent: Union[GameMap, Inventory]

    def __init__(
        self,
        parent: Optional[GameMap] = None,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        render_order: RenderOrder = RenderOrder.CORPSE,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if parent:
            # If parent isn't provided now then it will be set later.
            self.parent = parent
            parent.entities.add(self)
            
    @property
    def key_items(self) -> dict[int, Item]:
        return {item.key_id: item for item in self.inventory.items if item.key_id is not None}
    
    @property
    def gamemap(self) -> GameMap:
        if isinstance(self.parent, GameMap):
            return self.parent
        #raise AttributeError(f"{self.name} não tem um GameMap associado.")

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        self.x = x
        self.y = y
        if hasattr(self, "parent") and self.parent is not None:
            if isinstance(self.parent, GameMap):
                if self.parent.entities.__contains__(self):
                    self.parent.entities.remove(self)
        self.parent = gamemap
        gamemap.entities.add(self)

    def distance(self, x: int, y: int) -> float:
        """
        Return the distance between the current entity and the given (x, y) coordinate.
        """
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

class Actor(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "",
        ai_cls: Type[BaseAI],
        equipment: Equipment,
        fighter: Fighter,
        inventory: Inventory,
        skill_list: SkillList,
        parent: Optional[GameMap] = None,
    ):
        # Inicializa a classe pai Entity, mas sem atribuir o gamemap
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
            parent=parent
        )

        # Inicializa o AI e Fighter
        self.ai: Optional[BaseAI] = ai_cls(self)

        self.fighter = fighter
        self.fighter.parent = self

        self.equipment: Equipment = equipment
        self.equipment.parent = self

        self.inventory = inventory
        self.inventory.parent = self

        self.skill_list = skill_list
        self.skill_list.parent = self

        

    @property
    def is_alive(self) -> bool:
        """Retorna True enquanto esse ator pode realizar ações."""
        return bool(self.ai)
    @property
    def hasnt_won(self) -> bool:
        monsters = []
        for entity in set(self.parent.gamemap.actors) - {self.ai.engine.player}:
            monsters.append(entity)
        if len(monsters) == 0:
            return False
        return True
    
class Item(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        consumable: Optional[Consumable] = None,
        equippable: Optional[Equippable] = None,
        weight: float = 0,
        key_id: Optional[int] = None,
        parent: Optional[GameMap] = None, 
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
            parent=parent
        )

        self.consumable = consumable

        self.equippable = equippable

        self.weight = weight
        self.key_id = key_id

class Chest(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "C",  # Representação do baú no mapa.
        color: Tuple[int, int, int] = (139, 69, 19),  # Marrom, cor típica de baús.
        name: str = "Caixa",
        locked: bool = False,  # Indica se o baú está trancado.
        breakable: bool = False,  # Indica se o baú pode ser quebrado.
        chest_id: Optional[int] = None,  # ID necessário para baús trancados.
        items: Optional[List[Item]] = None,  # Lista de itens armazenados no baú.
    ):
        # Inicializa a classe pai Entity, mas sem atribuir o gamemap
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )
        self.locked = locked
        self.breakable = breakable
        self.chest_id = chest_id
        self.items = items or []

    def open(self, actor: Actor) -> List[Item]:
        """
        Tenta abrir o baú.
        
        Args:
            actor (Actor): O ator tentando abrir o baú.
            
        Returns:
            List[Item]: A lista de itens no baú se for aberto.
        """
        if self.locked:
            if not self._player_has_key(actor):
                raise exceptions.Impossible(f"O(a) {self.name} precisa de chave.")
        
        items = self.items
        self.items = []  # Esvazia o baú.
        self.blocks_movement = False  # O baú agora não bloqueia movimento.
        self.char = "%"
        self.name = "Bau aberto"
        self.color = (100, 100, 40)
        self.blocks_movement = False
        self.breakable = False
        self.locked = False
        self.render_order = RenderOrder.CORPSE
        return items

    def break_chest(self, actor: Actor) -> List[Item]:
        """
        Quebra o baú para acessar os itens, se for quebrável.
        
        Args:
            actor (Actor): O ator quebrando o baú.
            
        Returns:
            List[Item]: Os itens no baú.
        """
        if not self.breakable:
            raise exceptions.Impossible("Este container nao pode ser quebrado.")
        
        items = self.items
        self.items = []  # Esvazia o baú.
        self.blocks_movement = False  # O baú agora não bloqueia movimento.
        self.char = "%"
        self.name = "Bau quebrado"
        self.color = (100, 100, 40)
        self.blocks_movement = False
        self.breakable = False
        self.locked = False
        self.render_order = RenderOrder.CORPSE
        return items

    def _player_has_key(self, actor: Actor) -> bool:
        return self.chest_id in actor.inventory.key_items