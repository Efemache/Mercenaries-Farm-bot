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
    bat1 = "bat1"
    bat2 = "bat2"
    bat3 = "bat3"
    bat4 = "bat4"
    bat5 = "bat5"
    battle = "battle"
    Blackrock = "Blackrock"
    blue = "blue"
    boss = "boss"
    bounties = "bounties"
    campfire = "campfire"
    encounter_battle = "encounter_battle"
    Felwood = "Felwood"
    free_battle = "free_battle"
    green = "green"
    group = "group"
    hourglass = "hourglass"
    heroic = "heroic"
    lose = "lose"
    mystery = "mystery"
    noclass = "noclass"
    noclass2 = "noclass2"
    normal = "normal"
    Onyxia = "Onyxia"
    prev = "prev"
    red = "red"
    replace_grey = "take_grey"
    reward_chest = "reward_chest"
    sob = "sob"
    spirithealer = "spirithealer"
    startbat = "startbat"
    take_grey = "take_grey"
    task_completed = "task_completed"
    team_selection = "team_selection"
    travelpoint = "travelpoint"
    view_party = "view_party"
    visitor = "visitor"
    win = "win"
    win_final = "win_final"
    Winterspring = "Winterspring"
    your_party = "your_party"


class Button(ImageFragment):
    _dir_name = "buttons"

    allready = "allready"
    back = "back"
    campfire_claim = "campfire_claim"
    campfire_completed_task = "campfire_completed_task"
    choose_level = "choose_level"
    choose_task = "choose_task"
    choose_team = "choose_team"
    choose_travel = "choose_travel"
    confirm = "confirm"
    continue_button = "continue"
    done = "done"
    fight = "fight"
    finishok = "finishok"
    arrow_prev = "arrow_prev"
    arrow_next = "arrow_next"
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
    ready = "ready"
    replace = "take"
    retire = "retire"
    reveal = "reveal"
    startbattle1 = "startbattle1"
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
