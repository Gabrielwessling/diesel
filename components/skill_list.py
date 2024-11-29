from components.base_component import BaseComponent
from skill import Skill  # Corrigido para importar a classe Skill corretamente
from typing import List
from entity import *
from skills import SKILLS  # Suponho que você tenha uma lista de habilidades em skills.py
from engine import Engine

class SkillList(BaseComponent):
    skills = SKILLS
    def __init__(self, parent: Actor, engine: Engine):
        # Inicializa a lista de habilidades com as habilidades definidas no arquivo skills.py
        self.parent = parent
        self._engine = engine  # Use uma variável interna para armazenar o engine
        self.skills = SKILLS
        for skill in self.skills:
            skill.parent = parent
            skill.engine = engine

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, value: Engine):
        self._engine = value

    def add_skill(self, skill: Skill) -> None:
        """Adiciona uma habilidade à lista."""
        self.skills.append(skill)

    def remove_skill(self, skill: Skill) -> None:
        """Remove uma habilidade da lista."""
        if skill in self.skills:
            self.skills.remove(skill)

    def get_skill_by_name(self, name: str) -> Skill:
        """Obtém uma habilidade pelo nome."""
        for skill in self.skills:
            if skill.name == name:
                return skill
        return None  # Caso não encontre a habilidade

    def level_up_all(self) -> None:
        """Aumenta o nível de todas as habilidades que precisam de level up."""
        for skill in self.skills:
            if skill.requires_level_up:
                skill.increase_level()

    def list_skills(self) -> List[Skill]:
        return self.skills