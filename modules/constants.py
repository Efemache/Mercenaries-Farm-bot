from enum import Enum, auto


class StrEnum(str, Enum):
    def __new__(cls, value, *args, **kwargs):
        if not isinstance(value, (str, auto)):
            raise TypeError(
                f"Values of StrEnums must be strings: {value!r} is a {type(value)}"
            )
        return super().__new__(cls, value, *args, **kwargs)

    def __str__(self):
        return str(self.value)

    def _generate_next_value_(name, *_):
        return name


class ImageFragment(StrEnum):
    @property
    def filename(self):
        return f"{self._dir_name}/{self.value}.png"


class UIElement(ImageFragment):
    _dir_name = "UI_elements"

    Alterac = "Alterac"
    Barrens = "Barrens"
    Blackrock = "Blackrock"
    Darkshore = "Darkshore"
    Darkmoon = "Darkmoon"
    Felwood = "Felwood"
    Onyxia = "Onyxia"
    Sunken = "Sunken"
    Winterspring = "Winterspring"
    battle = "battle"
    blue = "blue"
    encounter_booncaster = "encounter_booncaster"
    encounter_boonfighter = "encounter_boonfighter"
    encounter_boonprotector = "encounter_boonprotector"
    encounter_caster = "encounter_caster"
    encounter_fighter = "encounter_fighter"
    encounter_protector = "encounter_protector"
    encounter_elite = "encounter_elite"
    boss = "boss"
    bounties = "bounties"
    campfire = "campfire"
    encounter_card = "encounter_card"
    free_battle = "free_battle"
    green = "green"
    heroic = "heroic"
    hourglass = "hourglass"
    lose = "lose"
    mystery = "mystery"
    noclass = "noclass"
    noclass2 = "noclass2"
    normal = "normal"
    quests = "quests"
    red = "red"
    replace_grey = "take_grey"
    reward_chest = "reward_chest"
    sob = "sob"
    spirithealer = "spirithealer"
    take_grey = "take_grey"
    task_completed = "task_completed"
    task_event_completed = "task_event_completed"
    task_expansion_completed = "task_expansion_completed"
    team_selection = "team_selection"
    travelpoint = "travelpoint"
    treasure_passive = "treasure_passive"
    view_party = "view_party"
    win = "win"
    win_final = "win_final"
    your_party = "your_party"


class Button(ImageFragment):
    _dir_name = "buttons"

    allready = "allready"
    arrow_prev = "arrow_prev"
    arrow_next = "arrow_next"
    back = "back"
    campfire_claim = "campfire_claim"
    campfire_completed_task = "campfire_completed_task"
    campfire_completed_eventtask = "campfire_completed_event-task"
    campfire_completed_partytask = "campfire_completed_party-task"
    campfire_completed_expansiontask = "campfire_completed_expansion-task"
    campfire_hiddenparty = "campfire_hidden-party"
    campfire_hiddenvisitors = "campfire_hidden-visitors"
    choose_level = "choose_level"
    choose_team = "choose_team"
    choose_travel = "choose_travel"
    done = "done"
    done_bonus = "done_bonus"
    fight = "fight"
    finishok = "finishok"
    group_name = "group_name"
    join_button = "join_button"
    keep = "take"
    lockin = "lockin"
    num = "num"
    ok = "ok"
    onedie = "num"
    pick = "pick"
    play = "play"
    portal_warp = "portal_warp"
    replace = "take"
    retire = "retire"
    reveal = "reveal"
    take = "take"
    tavern = "tavern"
    view_party = "view_party"
    visit = "visit"


class Action(StrEnum):
    screenshot = "1"
    move = "2"
    get_coords_part_screen = "12"
    move_and_click = "14"
    get_coords = "15"
