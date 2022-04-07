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
    _dir_name = "UI_ellements"

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
    choose_team = "choose_team"
    encounter_battle = "encounter_battle"
    Felwood = "Felwood"
    free_battle = "free_battle"
    green = "green"
    group = "group"
    heroic = "heroic"
    noclass = "noclass"
    noclass2 = "noclass2"
    normal = "normal"
    Onyxia = "Onyxia"
    pick = "pick"
    presents_thing = "presents_thing"
    prev = "prev"
    red = "red"
    replace_grey = "take_grey"
    sob = "sob"
    spirithealer = "spirithealer"
    startbat = "startbat"
    surprise = "surprise"
    take_grey = "take_grey"
    task_completed = "task_completed"
    travelpoint = "travelpoint"
    view_party = "view_party"
    visitor = "visitor"
    Winterspring = "Winterspring"
    your_party = "your_party"


class Button(ImageFragment):
    _dir_name = "buttons"

    allready = "allready"
    back = "back"
    campfire_claim = "campfire_claim"
    campfire_completed_task = "campfire_completed_task"
    choose_task = "choose_task"
    choose_travel = "choose_travel"
    confirm = "confirm"
    continue_button = "continue"
    done = "done"
    fight = "fight"
    finishok = "finishok"
    fir = "fir"
    join_button = "join_button"
    keep = "take"
    lockin = "lockin"
    num = "num"
    ok = "ok"
    onedie = "onedie"
    play = "play"
    portal_warp = "portal-warp"
    ready = "ready"
    replace = "take"
    retire = "retire"
    reveal = "reveal"
    sec = "sec"
    start = "start"
    start1 = "start1"
    startbattle1 = "startbattle1"
    take = "take"
    view_party = "view_party"
    visit = "visit"


class Checker(ImageFragment):
    _dir_name = "chekers"

    cords_search = "cords-search"
    drop = "drop"
    empty_check = "empty_check"
    find = "find"
    goto = "goto"
    group_find = "group_find"
    hourglass = "hourglass"
    ifrename = "ifrename"
    levelstarted = "levelstarted"
    lose = "lose"
    lv301 = "301"
    lv302 = "302"
    lv303 = "303"
    lvl1_30 = "30lvl1"
    lvl2_30 = "30lvl2"
    lvl30 = "30lvl"
    win_final = "win_final"
    menu = "menu"
    nextlvlcheck = "nextlvlcheck"
    party = "party"
    rename = "rename"
    shab = "shab"
    taken = "taken"
    text = "text"
    win = "win"


class Action(StrEnum):
    screenshot = "1"
    move = "2"
    get_coords_part_screen = "12"
    move_and_click = "14"
    get_coords = "15"
