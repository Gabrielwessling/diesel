# skills.py
from skill import Skill
from entity import *
from components.equippable import *

# Definindo as habilidades no script separado
SKILLS = [
    Skill(name="Knifology", level_up_base=200),         #0 "xp up when dealing damage using Swords"
    Skill(name="Swordsman", level_up_base=200),         #0 "xp up when dealing damage using Swords"
    Skill(name="Thrusting", level_up_base=200),         #0 "xp up when dealing damage using Swords"
    Skill(name="Smack Logic", level_up_base=200),         #0 "xp up when dealing damage using Swords"
    Skill(name="Slicing", level_up_base=200),         #0 "xp up when dealing damage using Swords"
    Skill(name="Archery", level_up_base=200),         #0 "xp up when dealing damage using Swords"
    Skill(name="Pistol Mastering", level_up_base=200),         #0 "xp up when dealing damage using Swords"
    Skill(name="Assaulting", level_up_base=200),         #0 "xp up when dealing damage using Swords"
    Skill(name="Sending", level_up_base=200),         #0 "xp up when dealing damage using Swords"
    Skill(name="Throwing", level_up_base=200),         #0 "xp up when dealing damage using Swords"
    Skill(name="Gadgeting", level_up_base=200),         #1 "xp up when using active items"
    Skill(name="Martial Arts", level_up_base=200),      #2 "xp up when attacking, even if not doing damage or missing"
    Skill(name="First Aid", level_up_base=200),         #3 "xp up when healing"
    Skill(name="Pain Mastering", level_up_base=200)     #4 "xp up when receiving damage"
]

# Mapeamento entre skills e classes de armas
WEAPON_SKILL_MAP = {
    "Knifology": Dagger,          # Facas
    "Swordsman": Sword,           # Espadas
    "Thrusting": Spear,           # Lanças
    "Smack Logic": Hammer,        # Martelos
    "Slicing": Axe,               # Machados
    "Archery": Bow,               # Arcos
    "Pistol Mastering": Pistol,   # Pistolas
    "Assaulting": Rifle,          # Rifles
    "Sending": Launcher,          # Lançadores
    "Throwing": Throwable         # Armas arremessáveis
}
