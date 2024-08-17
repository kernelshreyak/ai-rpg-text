from ai_rpg_core.game_templates import *

class RPGBasicRandom(GameTemplate):
    def __init__(self,inventory:str):
        super().__init__(inventory=inventory)
        self.template = RPG_BASE
        self.template += RPG_STATS.replace("{player_inventory_initial}", inventory)
        self.template += RPG_OPEN_WORLD
        self.template += RPG_STORY_GEN
        self.template += "\nThe world contains a wide range of characters including humanoid, undead, giants and other monsters, not all of which are hostile. Some of the enemies can have special abilities and attacks/armour.\n"
        self.template += RPG_GUARDRAILS
        self.template += RPG_END

class RPGFixedCampaign(GameTemplate):
    def __init__(self,inventory:str,backstory:str):
        super().__init__(is_fixed = True,inventory = inventory)
        self.template = RPG_BASE
        self.template += backstory.replace("{player_inventory_initial}", inventory)
        self.template += RPG_OPEN_WORLD
        self.template += RPG_GUARDRAILS
        self.template += RPG_END