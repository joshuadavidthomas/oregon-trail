#!/usr/bin/env python3
"""
PROGRAM NAME - OREGON        VERSION:01/01/78
ORIGINAL PROGRAMMING BY BILL HEINEMANN - 1971
SUPPORT RESEARCH AND MATERIALS BY DON RAVITSCH
MINNESOTA EDUCATIONAL COMPUTING CONSORTIUM STAFF
CDC CYBER 70/73-26      BASIC 3.1

CONVERTED TO PYTHON 3.10+ - 2026
"""

import random
import sys
import time
from dataclasses import dataclass, field
from enum import IntEnum


class Skill(IntEnum):
    ACE_MARKSMAN = 1
    GOOD_SHOT = 2
    FAIR = 3
    NEED_PRACTICE = 4
    SHAKY_KNEES = 5


class EatingLevel(IntEnum):
    POORLY = 1
    MODERATELY = 2
    WELL = 3


class Action(IntEnum):
    FORT = 1
    HUNT = 2
    CONTINUE = 3


class Tactic(IntEnum):
    RUN = 1
    ATTACK = 2
    CONTINUE = 3
    CIRCLE_WAGONS = 4


DATES = [
    "MARCH 29",
    "APRIL 12", "APRIL 26", "MAY 10", "MAY 24",
    "JUNE 7", "JUNE 21", "JULY 5", "JULY 19",
    "AUGUST 2", "AUGUST 16", "AUGUST 31",
    "SEPTEMBER 13", "SEPTEMBER 27", "OCTOBER 11",
    "OCTOBER 25", "NOVEMBER 8", "NOVEMBER 22",
    "DECEMBER 6", "DECEMBER 20",
]

EVENT_THRESHOLDS = [6, 11, 13, 15, 17, 22, 32, 35, 37, 42, 44, 54, 64, 69, 95]

INSTRUCTIONS = """\

THIS PROGRAM SIMULATES A TRIP OVER THE OREGON TRAIL FROM
INDEPENDENCE, MISSOURI TO OREGON CITY, OREGON IN 1847.
YOUR FAMILY OF FIVE WILL COVER THE 2040 MILE OREGON TRAIL
IN 5-6 MONTHS --- IF YOU MAKE IT ALIVE.

YOU HAD SAVED $900 TO SPEND FOR THE TRIP, AND YOU'VE JUST
   PAID $200 FOR A WAGON.
YOU WILL NEED TO SPEND THE REST OF YOUR MONEY ON THE
   FOLLOWING ITEMS:

     OXEN - YOU CAN SPEND $200-$300 ON YOUR TEAM
            THE MORE YOU SPEND, THE FASTER YOU'LL GO
            BECAUSE YOU'LL HAVE BETTER ANIMALS

     FOOD - THE MORE YOU HAVE, THE LESS CHANCE THERE
            IS OF GETTING SICK

AMMUNITION - $1 BUYS A BELT OF 50 BULLETS
            YOU WILL NEED BULLETS FOR ATTACKS BY ANIMALS
            AND BANDITS, AND FOR HUNTING FOOD

CLOTHING - THIS IS ESPECIALLY IMPORTANT FOR THE COLD
            WEATHER YOU WILL ENCOUNTER WHEN CROSSING
            THE MOUNTAINS

MISCELLANEOUS SUPPLIES - THIS INCLUDES MEDICINE AND
            OTHER THINGS YOU WILL NEED FOR SICKNESS
            AND EMERGENCY REPAIRS


YOU CAN SPEND ALL YOUR MONEY BEFORE YOU START YOUR TRIP -
OR YOU CAN SAVE SOME OF YOUR CASH TO SPEND AT FORTS ALONG
THE WAY WHEN YOU RUN LOW. HOWEVER, ITEMS COST MORE AT
THE FORTS. YOU CAN ALSO GO HUNTING ALONG THE WAY TO GET
MORE FOOD.
WHENEVER YOU HAVE TO USE YOUR TRUSTY RIFLE ALONG THE WAY,
YOU WILL BE TOLD TO TYPE IN A WORD (ONE THAT SOUNDS LIKE A
GUN SHOT). THE FASTER YOU TYPE IN THAT WORD AND HIT THE
"RETURN" KEY, THE BETTER LUCK YOU'LL HAVE WITH YOUR GUN.

AT EACH TURN, ALL ITEMS ARE SHOWN IN DOLLAR AMOUNTS
EXCEPT BULLETS
WHEN ASKED TO ENTER MONEY AMOUNTS, DON'T USE A "$".

GOOD LUCK!!!"""


@dataclass
class GameState:
    oxen: float = 0
    food: float = 0
    bullets: float = 0
    clothing: float = 0
    misc: float = 0
    cash: float = 0
    mileage: int = 0
    prev_mileage: int = 0
    skill: float = 0
    turn: int = 0
    injured: bool = False
    sick: bool = False
    south_pass_cleared: bool = False
    blue_mountains_cleared: bool = False
    fort_toggle: bool = False
    mileage_override: bool = False

    def clamp_supplies(self):
        """Ensure no supply goes below zero and truncate to int."""
        self.food = int(max(0, self.food))
        self.bullets = int(max(0, self.bullets))
        self.clothing = int(max(0, self.clothing))
        self.misc = int(max(0, self.misc))
        self.cash = int(self.cash)
        self.mileage = int(self.mileage)

    def print_status(self):
        if self.mileage_override:
            print("TOTAL MILEAGE IS 950")
            self.mileage_override = False
        else:
            print(f"TOTAL MILEAGE IS {self.mileage}")
        print(f"{'FOOD':<14}{'BULLETS':<14}{'CLOTHING':<14}{'MISC. SUPP.':<14}{'CASH'}")
        print(f"{self.food:<14}{self.bullets:<14}{self.clothing:<14}{self.misc:<14}{self.cash}")

    def death_cause(self) -> str:
        return "INJURIES" if self.injured else "PNEUMONIA"


# --- I/O helpers ---

def get_input(prompt: str = "? ") -> str:
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)


def get_number(prompt: str = "? ") -> float:
    while True:
        try:
            return float(get_input(prompt))
        except ValueError:
            print("PLEASE ENTER A NUMBER")


def get_choice(lo: int, hi: int) -> int:
    while True:
        val = int(get_number())
        if lo <= val <= hi:
            return val


def get_positive(label: str) -> float:
    while True:
        print(f"HOW MUCH DO YOU WANT TO SPEND ON {label}", end="")
        val = get_number()
        if val >= 0:
            return val
        print("IMPOSSIBLE")


# --- Shooting ---

def shoot(skill: float) -> float:
    word = random.choice(["BANG", "BLAM", "POW", "WHAM"])
    print(f"TYPE {word}")
    start = time.time()
    response = get_input()
    elapsed = time.time() - start
    result = max(0.0, elapsed * 3600 - (skill - 1))
    print()
    if response.strip().upper() != word:
        result = 9
    return result


def handle_shoot_result(result: float, gs: GameState) -> bool:
    """Print and apply shoot outcome for combat. Returns True if knifed."""
    match result:
        case r if r <= 1:
            print("NICE SHOOTING---YOU DROVE THEM OFF")
        case r if r > 4:
            print("LOUSY SHOT---YOU GOT KNIFED")
            gs.injured = True
            print("YOU HAVE TO SEE OL' DOC BLANCHARD")
            return True
        case _:
            print("KINDA SLOW WITH YOUR COLT .45")
    return False


# --- Fort trading ---

def fort_purchase(gs: GameState) -> float:
    """Buy one item at a fort. Returns amount received (at 2/3 value)."""
    amount = get_number()
    if amount < 0:
        return 0
    if gs.cash - amount < 0:
        print("YOU DON'T HAVE THAT MUCH--KEEP YOUR SPENDING DOWN")
        print("YOU MISS YOUR CHANCE TO SPEND ON THAT ITEM")
        return 0
    gs.cash -= amount
    return 2 / 3 * amount


def visit_fort(gs: GameState):
    print("ENTER WHAT YOU WISH TO SPEND ON THE FOLLOWING")
    print("FOOD", end="")
    gs.food += fort_purchase(gs)
    print("AMMUNITION", end="")
    gs.bullets = int(gs.bullets + fort_purchase(gs) * 50)
    print("CLOTHING", end="")
    gs.clothing += fort_purchase(gs)
    print("MISCELLANEOUS SUPPLIES", end="")
    gs.misc += fort_purchase(gs)
    gs.mileage -= 45


# --- Illness ---

def illness(gs: GameState, eating: int) -> bool:
    """Apply illness effects. Returns True if player died."""
    roll = 100 * random.random()
    match roll:
        case r if r < 10 + 35 * (eating - 1):
            print("MILD ILLNESS---MEDICINE USED")
            gs.mileage -= 5
            gs.misc -= 2
        case r if r < 100 - (40 / 4 ** (eating - 1)):
            print("BAD ILLNESS---MEDICINE USED")
            gs.mileage -= 5
            gs.misc -= 5
        case _:
            print("SERIOUS ILLNESS---")
            print("YOU MUST STOP FOR MEDICAL ATTENTION")
            gs.misc -= 10
            gs.sick = True
    if gs.misc < 0:
        print("YOU RAN OUT OF MEDICAL SUPPLIES")
        return True
    return False


# --- End game sequences ---

def game_over():
    print()
    print("DUE TO YOUR UNFORTUNATE SITUATION, THERE ARE A FEW")
    print("FORMALITIES WE MUST GO THROUGH")
    print()
    print("WOULD YOU LIKE A MINISTER?")
    get_input()
    print("WOULD YOU LIKE A FANCY FUNERAL?")
    get_input()
    print("WOULD YOU LIKE US TO INFORM YOUR NEXT OF KIN?")
    if get_input().strip().upper() == "YES":
        print("THAT WILL BE $4.50 FOR THE TELEGRAPH CHARGE.")
    else:
        print("BUT YOUR AUNT SADIE IN ST. LOUIS IS REALLY WORRIED ABOUT YOU")
    print()
    print("WE THANK YOU FOR THIS INFORMATION AND WE ARE SORRY YOU")
    print("DIDN'T MAKE IT TO THE GREAT TERRITORY OF OREGON")
    print("BETTER LUCK NEXT TIME")
    print()
    print()
    print("                              SINCERELY")
    print()
    print("                 THE OREGON CITY CHAMBER OF COMMERCE")


def die(gs: GameState, message: str | None = None):
    if message:
        print(message)
    game_over()


def victory(gs: GameState, eating: int):
    fraction = (2040 - gs.prev_mileage) / (gs.mileage - gs.prev_mileage)
    final_food = gs.food + (1 - fraction) * (8 + 5 * eating)
    print()
    print("YOU FINALLY ARRIVED AT OREGON CITY")
    print("AFTER 2040 LONG MILES---HOORAY!!!!!")
    print("A REAL PIONEER!")
    print()

    fraction_days = int(fraction * 14)
    total_days = gs.turn * 14 + fraction_days
    day_of_week = (fraction_days + 1 - 1) % 7  # 0-indexed

    weekdays = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY",
                "FRIDAY", "SATURDAY", "SUNDAY"]
    print(f"{weekdays[day_of_week]} ", end="")

    months = [(93, "JULY"), (124, "AUGUST"), (155, "SEPTEMBER"),
              (185, "OCTOBER"), (216, "NOVEMBER"), (246, "DECEMBER")]
    for offset, name in months:
        if total_days <= offset + 31:
            print(f"{name} {total_days - offset} 1847")
            break

    print()
    vals = {k: max(0, int(v)) for k, v in [
        ("FOOD", final_food), ("BULLETS", gs.bullets), ("CLOTHING", gs.clothing),
        ("MISC. SUPP.", gs.misc), ("CASH", gs.cash),
    ]}
    print(f"{'FOOD':<14}{'BULLETS':<14}{'CLOTHING':<14}{'MISC. SUPP.':<14}{'CASH'}")
    print(f"{vals['FOOD']:<14}{vals['BULLETS']:<14}{vals['CLOTHING']:<14}{vals['MISC. SUPP.']:<14}{vals['CASH']}")
    print()
    print("           PRESIDENT JAMES K. POLK SENDS YOU HIS")
    print("                 HEARTIEST CONGRATULATIONS")
    print()
    print("           AND WISHES YOU A PROSPEROUS LIFE AHEAD")
    print()
    print("                      AT YOUR NEW HOME")


# --- Event handlers ---

def handle_riders(gs: GameState):
    """Handle rider encounter. Returns True if player died."""
    friendly = random.random() < 0.8
    print("RIDERS AHEAD.  THEY ", end="")
    if friendly:
        print("DON'T ", end="")
    print("LOOK HOSTILE")
    print("TACTICS")
    print("(1) RUN  (2) ATTACK  (3) CONTINUE  (4) CIRCLE WAGONS")

    # 20% chance the appearance was deceiving
    if random.random() <= 0.2:
        friendly = not friendly

    tactic = Tactic(get_choice(1, 4))

    if friendly:
        match tactic:
            case Tactic.RUN:
                gs.mileage += 15
                gs.oxen -= 10
            case Tactic.ATTACK:
                gs.mileage -= 5
                gs.bullets -= 100
            case Tactic.CONTINUE:
                pass
            case Tactic.CIRCLE_WAGONS:
                gs.mileage -= 20
        print("RIDERS WERE FRIENDLY, BUT CHECK FOR POSSIBLE LOSSES")
    else:
        match tactic:
            case Tactic.RUN:
                gs.mileage += 20
                gs.misc -= 15
                gs.bullets -= 150
                gs.oxen -= 40
            case Tactic.ATTACK:
                result = shoot(gs.skill)
                gs.bullets -= result * 40 + 80
                handle_shoot_result(result, gs)
            case Tactic.CONTINUE:
                if random.random() > 0.8:
                    print("THEY DID NOT ATTACK")
                else:
                    gs.bullets -= 150
                    gs.misc -= 15
            case Tactic.CIRCLE_WAGONS:
                result = shoot(gs.skill)
                gs.bullets -= result * 30 + 80
                gs.mileage -= 25
                handle_shoot_result(result, gs)
        print("RIDERS WERE HOSTILE--CHECK FOR LOSSES")

    if gs.bullets < 0:
        print("YOU RAN OUT OF BULLETS AND GOT MASSACRED BY THE RIDERS")
        game_over()
        return True
    return False


def handle_event(gs: GameState, eating: int) -> bool | None:
    """Process a random event. Returns True if player died, None otherwise."""
    r1 = 100 * random.random()
    event = next(
        (i + 1 for i, threshold in enumerate(EVENT_THRESHOLDS) if r1 <= threshold),
        16,
    )

    trigger_illness = False

    match event:
        case 1:
            print("WAGON BREAKS DOWN--LOSE TIME AND SUPPLIES FIXING IT")
            gs.mileage -= 15 + 5 * random.random()
            gs.misc -= 8
        case 2:
            print("OX INJURES LEG---SLOWS YOU DOWN REST OF TRIP")
            gs.mileage -= 25
            gs.oxen -= 20
        case 3:
            print("BAD LUCK---YOUR DAUGHTER BROKE HER ARM")
            print("YOU HAD TO STOP AND USE SUPPLIES TO MAKE A SLING")
            gs.mileage -= 5 + 4 * random.random()
            gs.misc -= 2 + 3 * random.random()
        case 4:
            print("OX WANDERS OFF---SPEND TIME LOOKING FOR IT")
            gs.mileage -= 17
        case 5:
            print("YOUR SON GETS LOST---SPEND HALF THE DAY LOOKING FOR HIM")
            gs.mileage -= 10
        case 6:
            print("UNSAFE WATER--LOSE TIME LOOKING FOR CLEAN SPRING")
            gs.mileage -= 10 * random.random() + 2
        case 7:
            if gs.mileage > 950:
                print("COLD WEATHER---BRRRRRRR!---YOU ", end="")
                if gs.clothing > 22 + 4 * random.random():
                    print("HAVE ENOUGH CLOTHING TO KEEP YOU WARM")
                else:
                    print("DON'T HAVE ENOUGH CLOTHING TO KEEP YOU WARM")
                    trigger_illness = True
            else:
                print("HEAVY RAINS---TIME AND SUPPLIES LOST")
                gs.food -= 10
                gs.bullets -= 500
                gs.misc -= 15
                gs.mileage -= 10 * random.random() + 5
        case 8:
            print("BANDITS ATTACK")
            result = shoot(gs.skill)
            gs.bullets -= 20 * result
            if gs.bullets < 0:
                print("YOU RAN OUT OF BULLETS---THEY GET LOTS OF CASH")
                gs.cash /= 3
                print("YOU GOT SHOT IN THE LEG AND THEY TOOK ONE OF YOUR OXEN")
                gs.injured = True
                print("BETTER HAVE A DOC LOOK AT YOUR WOUND")
                gs.misc -= 5
                gs.oxen -= 20
            elif result <= 1:
                print("QUICKEST DRAW OUTSIDE OF DODGE CITY!!!")
                print("YOU GOT 'EM!")
            else:
                print("YOU GOT SHOT IN THE LEG AND THEY TOOK ONE OF YOUR OXEN")
                gs.injured = True
                print("BETTER HAVE A DOC LOOK AT YOUR WOUND")
                gs.misc -= 5
                gs.oxen -= 20
        case 9:
            print("THERE WAS A FIRE IN YOUR WAGON--FOOD AND SUPPLIES DAMAGE")
            gs.food -= 40
            gs.bullets -= 400
            gs.misc -= random.random() * 8 + 3
            gs.mileage -= 15
        case 10:
            print("LOSE YOUR WAY IN HEAVY FOG---TIME IS LOST")
            gs.mileage -= 10 + 5 * random.random()
        case 11:
            print("YOU KILLED A POISONOUS SNAKE AFTER IT BIT YOU")
            gs.bullets -= 10
            gs.misc -= 5
            if gs.misc < 0:
                print("YOU DIE OF SNAKEBITE SINCE YOU HAVE NO MEDICINE")
                game_over()
                return True
        case 12:
            print("WAGON GETS SWAMPED FORDING RIVER--LOSE FOOD AND CLOTHES")
            gs.food -= 30
            gs.clothing -= 20
            gs.mileage -= 20 + 20 * random.random()
        case 13:
            print("WILD ANIMALS ATTACK!")
            result = shoot(gs.skill)
            if gs.bullets <= 39:
                print("YOU WERE TOO LOW ON BULLETS--")
                print("THE WOLVES OVERPOWERED YOU")
                gs.injured = True
                die(gs, "YOU DIED OF INJURIES")
                return True
            if result <= 2:
                print("NICE SHOOTIN' PARTNER---THEY DIDN'T GET MUCH")
            else:
                print("SLOW ON THE DRAW---THEY GOT AT YOUR FOOD AND CLOTHES")
            gs.bullets -= 20 * result
            gs.clothing -= result * 4
            gs.food -= result * 8
        case 14:
            print("HAIL STORM---SUPPLIES DAMAGED")
            gs.mileage -= 5 + random.random() * 10
            gs.bullets -= 200
            gs.misc -= 4 + random.random() * 3
        case 15:
            match eating:
                case EatingLevel.POORLY:
                    trigger_illness = True
                case EatingLevel.WELL:
                    trigger_illness = random.random() < 0.5
                case _:
                    trigger_illness = random.random() > 0.25
        case 16:
            print("HELPFUL INDIANS SHOW YOU WHERE TO FIND MORE FOOD")
            gs.food += 14

    if trigger_illness:
        if illness(gs, eating):
            die(gs, f"YOU DIED OF {gs.death_cause()}")
            return True

    return None


def handle_mountains(gs: GameState, eating: int) -> bool | None:
    """Handle mountain terrain. Returns True if player died."""
    terrain_check = (
        random.random() * 10
        * ((9 - ((gs.mileage / 100 - 15) ** 2 + 72))
           / ((gs.mileage / 100 - 15) ** 2 + 12))
    )
    if terrain_check <= 0:
        r = random.random()
        print("RUGGED MOUNTAINS")
        match r:
            case _ if r <= 0.1:
                print("YOU GOT LOST---LOSE VALUABLE TIME TRYING TO FIND TRAIL!")
                gs.mileage -= 60
            case _ if r <= 0.21:
                print("WAGON DAMAGED!---LOSE TIME AND SUPPLIES")
                gs.misc -= 5
                gs.bullets -= 200
                gs.mileage -= 20 + 30 * random.random()
            case _:
                print("THE GOING GETS SLOW")
                gs.mileage -= 45 + random.random() / 0.02
    return None


def handle_blizzard(gs: GameState, eating: int) -> bool:
    """Apply blizzard effects. Returns True if player died."""
    print("BLIZZARD IN MOUNTAIN PASS--TIME AND SUPPLIES LOST")
    gs.food -= 25
    gs.misc -= 10
    gs.bullets -= 300
    gs.mileage -= 30 + 40 * random.random()
    if gs.clothing < 18 + 2 * random.random():
        if illness(gs, eating):
            die(gs, f"YOU DIED OF {gs.death_cause()}")
            return True
    if gs.mileage <= 950:
        gs.mileage_override = True
    return False


def handle_passes(gs: GameState, eating: int) -> bool | None:
    """Handle South Pass / Blue Mountains. Returns True if died."""
    if not gs.south_pass_cleared:
        gs.south_pass_cleared = True
        if random.random() >= 0.8:
            print("YOU MADE IT SAFELY THROUGH SOUTH PASS--NO SNOW")
        else:
            return handle_blizzard(gs, eating)
    elif gs.mileage >= 1700 and not gs.blue_mountains_cleared:
        gs.blue_mountains_cleared = True
        if random.random() < 0.7:
            return handle_blizzard(gs, eating)
    return None


# --- Main game ---

def buy_supplies() -> GameState:
    """Run the initial shopping phase. Returns populated GameState."""
    print()
    print("HOW GOOD A SHOT ARE YOU WITH YOUR RIFLE?")
    print("  (1) ACE MARKSMAN,  (2) GOOD SHOT,  (3) FAIR TO MIDDLIN'")
    print("         (4) NEED MORE PRACTICE,  (5) SHAKY KNEES")
    print("ENTER ONE OF THE ABOVE -- THE BETTER YOU CLAIM YOU ARE, THE")
    print("FASTER YOU'LL HAVE TO BE WITH YOUR GUN TO BE SUCCESSFUL.")
    skill = get_number()
    if skill > 5:
        skill = 0

    while True:
        print()
        print()
        while True:
            print("HOW MUCH DO YOU WANT TO SPEND ON YOUR OXEN TEAM", end="")
            oxen = get_number()
            match oxen:
                case o if o < 200:
                    print("NOT ENOUGH")
                case o if o > 300:
                    print("TOO MUCH")
                case _:
                    break

        food = get_positive("FOOD")
        ammo = get_positive("AMMUNITION")
        clothing = get_positive("CLOTHING")
        misc = get_positive("MISCELLANEOUS SUPPLIES")

        cash = 700 - oxen - food - ammo - clothing - misc
        if cash >= 0:
            break
        print("YOU OVERSPENT--YOU ONLY HAD $700 TO SPEND.  BUY AGAIN")

    gs = GameState(
        oxen=oxen,
        food=food,
        bullets=50 * ammo,
        clothing=clothing,
        misc=misc,
        cash=cash,
        skill=skill,
    )
    print(f"AFTER ALL YOUR PURCHASES, YOU NOW HAVE {int(cash)} DOLLARS LEFT")
    return gs


def choose_action(gs: GameState, first_turn: bool) -> Action:
    """Get the player's turn action choice."""
    if not gs.fort_toggle and first_turn:
        # No fort option on odd turns / first turn
        while True:
            print("DO YOU WANT TO (1) HUNT, OR (2) CONTINUE")
            choice = int(get_number())
            action = Action.HUNT if choice == 1 else Action.CONTINUE
            if action == Action.HUNT and gs.bullets <= 39:
                print("TOUGH---YOU NEED MORE BULLETS TO GO HUNTING")
                continue
            return action

    if not gs.fort_toggle:
        while True:
            print("DO YOU WANT TO (1) HUNT, OR (2) CONTINUE")
            choice = int(get_number())
            action = Action.HUNT if choice == 1 else Action.CONTINUE
            if action == Action.HUNT and gs.bullets <= 39:
                print("TOUGH---YOU NEED MORE BULLETS TO GO HUNTING")
                continue
            return action

    print("DO YOU WANT TO (1) STOP AT THE NEXT FORT, (2) HUNT, ", end="")
    print("OR (3) CONTINUE")
    choice = int(get_number())
    match choice:
        case 1:
            return Action.FORT
        case 2:
            return Action.HUNT
        case _:
            return Action.CONTINUE


def do_hunt(gs: GameState):
    """Execute a hunting action."""
    gs.mileage -= 45
    result = shoot(gs.skill)
    match result:
        case r if r <= 1:
            print("RIGHT BETWEEN THE EYES---YOU GOT A BIG ONE!!!!")
            print("FULL BELLIES TONIGHT!")
            gs.food += 52 + random.random() * 6
            gs.bullets -= 10 + random.random() * 4
        case r if 100 * random.random() < 13 * r:
            print("YOU MISSED---AND YOUR DINNER GOT AWAY.....")
        case _:
            gs.food += 48 - 2 * result
            print("NICE SHOT--RIGHT ON TARGET--GOOD EATIN' TONIGHT!!")
            gs.bullets -= 10 + 3 * result


def choose_eating(gs: GameState) -> int:
    """Get eating choice and deduct food."""
    while True:
        print("DO YOU WANT TO EAT (1) POORLY  (2) MODERATELY")
        print("OR (3) WELL", end="")
        choice = int(get_number())
        if choice not in (1, 2, 3):
            continue
        food_cost = 8 + 5 * choice
        if gs.food - food_cost < 0:
            print("YOU CAN'T EAT THAT WELL")
            continue
        gs.food -= food_cost
        return choice


def main():
    random.seed()

    print("DO YOU NEED INSTRUCTIONS  (YES/NO)")
    if get_input().strip().upper() != "NO":
        print(INSTRUCTIONS)

    print()
    gs = buy_supplies()
    print()
    print("MONDAY MARCH 29 1847")
    print()

    first_turn = True
    eating = EatingLevel.MODERATELY

    while True:
        # Advance date (skip on first turn)
        if not first_turn:
            if gs.mileage >= 2040:
                victory(gs, eating)
                return

            gs.turn += 1
            print()
            if gs.turn < len(DATES):
                print(f"MONDAY {DATES[gs.turn]} 1847")
            else:
                print("YOU HAVE BEEN ON THE TRAIL TOO LONG  ------")
                print("YOUR FAMILY DIES IN THE FIRST BLIZZARD OF WINTER")
                game_over()
                return
            print()

        # Prepare turn
        gs.clamp_supplies()
        gs.prev_mileage = gs.mileage
        if gs.food < 13:
            print("YOU'D BETTER DO SOME HUNTING OR BUY FOOD AND SOON!!!!")

        # Doctor visit for injuries/illness
        if gs.sick or gs.injured:
            gs.cash -= 20
            if gs.cash < 0:
                gs.cash = 0
                print("YOU CAN'T AFFORD A DOCTOR")
                die(gs, f"YOU DIED OF {gs.death_cause()}")
                return
            print("DOCTOR'S BILL IS $20")
            gs.injured = False
            gs.sick = False

        gs.print_status()

        # Choose and execute action
        action = choose_action(gs, first_turn)
        gs.fort_toggle = not gs.fort_toggle
        first_turn = False

        match action:
            case Action.FORT:
                visit_fort(gs)
            case Action.HUNT:
                if gs.bullets <= 39:
                    print("TOUGH---YOU NEED MORE BULLETS TO GO HUNTING")
                    print("DO YOU WANT TO (1) STOP AT THE NEXT FORT, (2) HUNT, ", end="")
                    print("OR (3) CONTINUE")
                    fallback = int(get_number())
                    if fallback == 1:
                        visit_fort(gs)
                else:
                    do_hunt(gs)
            case Action.CONTINUE:
                pass

        # Starvation check
        if gs.food < 13:
            die(gs, "YOU RAN OUT OF FOOD AND STARVED TO DEATH")
            return

        # Eating
        eating = choose_eating(gs)

        # Travel
        gs.mileage += 200 + (gs.oxen - 220) / 5 + 10 * random.random()

        # Rider encounter
        rider_chance = (
            random.random() * 10
            * ((gs.mileage / 100 - 4) ** 2 + 72)
            / ((gs.mileage / 100 - 4) ** 2 + 12)
        )
        if rider_chance <= 1:
            if handle_riders(gs):
                return

        # Random event
        if handle_event(gs, eating):
            return

        # Mountains
        if gs.mileage <= 950:
            continue

        if handle_mountains(gs, eating):
            return

        if handle_passes(gs, eating):
            return


if __name__ == "__main__":
    main()
