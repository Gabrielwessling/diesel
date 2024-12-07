from components.base_component import BaseComponent
from skill import Skill  # Corrigido para importar a classe Skill corretamente
from typing import List, Dict
from entity import *
from categories.skills import SKILLS  # Suponho que você tenha uma lista de habilidades em skills.py
from engine import Engine

class SkillList(BaseComponent):
    skills = SKILLS
    def __init__(self, parent: Actor, engine: Engine):
        self.skills: Dict[str, Skill] = {}  # Mapeia o nome da habilidade para o objeto Skill
        self.parent = parent
        self._engine = engine  # Use uma variável interna para armazenar o engine
        self.start_skill_list()
        
        for skill, value in self.skills.items():
            self.skills[skill].parent = parent
            self.skills[skill].engine = engine

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, value: Engine):
        self._engine = value

    def start_skill_list(self):
        for skill in SKILLS:
            self.add_skill(skill)
    
    def add_skill(self, skill: Skill) -> None:
        """Adiciona uma habilidade ao dicionário."""
        self.skills[skill.name] = skill
        skill.parent = self.parent
        skill.engine = self.engine

    def get_skill_by_name(self, name: str) -> Skill:
        """Obtém uma habilidade pelo nome."""
        for skill in self.skills:
            if self.skills[skill].name == name:
                return skill
        return None  # Caso não encontre a habilidade