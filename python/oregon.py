#!/usr/bin/env python3
# PROGRAM NAME - OREGON        VERSION:01/01/78
# ORIGINAL PROGRAMMING BY BILL HEINEMANN - 1971
# SUPPORT RESEARCH AND MATERIALS BY DON RAVITSCH
# MINNESOTA EDUCATIONAL COMPUTING CONSORTIUM STAFF
# CDC CYBER 70/73-26      BASIC 3.1
# DOCUMENTATION BOOKLET 'OREGON' AVAILABLE FROM
#    MECC SUPPORT SERVICES
#    2520 BROADWAY DRIVE
#    ST. PAUL, MN  55113
#
# CONVERTED TO PYTHON - 2026

import random
import time
import math
import sys


def get_input(prompt="? "):
    """Get input from user, handling EOF gracefully."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)


def get_number(prompt="? "):
    """Get a numeric input from user."""
    while True:
        try:
            return float(get_input(prompt))
        except ValueError:
            print("PLEASE ENTER A NUMBER")


def shooting_routine(d9):
    """Shooting sub-routine. Returns response time adjusted by skill."""
    words = ["BANG", "BLAM", "POW", "WHAM"]
    word = random.choice(words)
    print(f"TYPE {word}")
    start = time.time()
    response = get_input()
    elapsed = time.time() - start
    b1 = elapsed * 3600 - (d9 - 1)
    print()
    if b1 < 0:
        b1 = 0
    if response.strip().upper() != word:
        b1 = 9
    return b1


def get_purchase(cash):
    """Fort purchase sub-routine. Returns (amount_received, remaining_cash)."""
    p = get_number()
    if p < 0:
        return 0, cash
    if cash - p < 0:
        print("YOU DON'T HAVE THAT MUCH--KEEP YOUR SPENDING DOWN")
        print("YOU MISS YOUR CHANCE TO SPEND ON THAT ITEM")
        return 0, cash
    return p, cash - p


def illness_routine(e, m, m1):
    """Illness sub-routine. Returns (mileage, misc_supplies, sick_flag, died)."""
    s4 = 0
    if 100 * random.random() < 10 + 35 * (e - 1):
        print("MILD ILLNESS---MEDICINE USED")
        m -= 5
        m1 -= 2
    elif 100 * random.random() < 100 - (40 / 4 ** (e - 1)):
        print("BAD ILLNESS---MEDICINE USED")
        m -= 5
        m1 -= 5
    else:
        print("SERIOUS ILLNESS---")
        print("YOU MUST STOP FOR MEDICAL ATTENTION")
        m1 -= 10
        s4 = 1
    if m1 < 0:
        print("YOU RAN OUT OF MEDICAL SUPPLIES")
        return m, m1, s4, True  # died
    return m, m1, s4, False


def print_game_over(c_response):
    """Print the game over / death sequence."""
    print()
    print("DUE TO YOUR UNFORTUNATE SITUATION, THERE ARE A FEW")
    print("FORMALITIES WE MUST GO THROUGH")
    print()
    print("WOULD YOU LIKE A MINISTER?")
    get_input()
    print("WOULD YOU LIKE A FANCY FUNERAL?")
    get_input()
    print("WOULD YOU LIKE US TO INFORM YOUR NEXT OF KIN?")
    resp = get_input()
    if resp.strip().upper() == "YES":
        print("THAT WILL BE $4.50 FOR THE TELEGRAPH CHARGE.")
        print()
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


def print_victory(f, b, c, m1, t, d3, m, m2, e):
    """Print the victory sequence."""
    f9 = (2040 - m2) / (m - m2)
    f_food = f + (1 - f9) * (8 + 5 * e)
    print()
    print("YOU FINALLY ARRIVED AT OREGON CITY")
    print("AFTER 2040 LONG MILES---HOORAY!!!!!")
    print("A REAL PIONEER!")
    print()
    f9_days = int(f9 * 14)
    d3_total = d3 * 14 + f9_days
    day_of_week = f9_days + 1
    if day_of_week >= 8:
        day_of_week -= 7

    days = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY",
            "FRIDAY", "SATURDAY", "SUNDAY"]
    if 1 <= day_of_week <= 7:
        print(f"{days[day_of_week - 1]} ", end="")

    if d3_total <= 124:
        print(f"JULY {d3_total - 93} 1847")
    elif d3_total <= 155:
        print(f"AUGUST {d3_total - 124} 1847")
    elif d3_total <= 185:
        print(f"SEPTEMBER {d3_total - 155} 1847")
    elif d3_total <= 216:
        print(f"OCTOBER {d3_total - 185} 1847")
    elif d3_total <= 246:
        print(f"NOVEMBER {d3_total - 216} 1847")
    else:
        print(f"DECEMBER {d3_total - 246} 1847")

    print()
    b = max(0, int(b))
    c = max(0, int(c))
    m1 = max(0, int(m1))
    t = max(0, int(t))
    f_food = max(0, int(f_food))
    print(f"{'FOOD':<14}{'BULLETS':<14}{'CLOTHING':<14}{'MISC. SUPP.':<14}{'CASH'}")
    print(f"{f_food:<14}{b:<14}{c:<14}{m1:<14}{t}")
    print()
    print("           PRESIDENT JAMES K. POLK SENDS YOU HIS")
    print("                 HEARTIEST CONGRATULATIONS")
    print()
    print("           AND WISHES YOU A PROSPEROUS LIFE AHEAD")
    print()
    print("                      AT YOUR NEW HOME")


def main():
    random.seed()

    print("DO YOU NEED INSTRUCTIONS  (YES/NO)")
    resp = get_input()
    if resp.strip().upper() != "NO":
        print()
        print()
        print("THIS PROGRAM SIMULATES A TRIP OVER THE OREGON TRAIL FROM")
        print("INDEPENDENCE, MISSOURI TO OREGON CITY, OREGON IN 1847.")
        print("YOUR FAMILY OF FIVE WILL COVER THE 2040 MILE OREGON TRAIL")
        print("IN 5-6 MONTHS --- IF YOU MAKE IT ALIVE.")
        print()
        print("YOU HAD SAVED $900 TO SPEND FOR THE TRIP, AND YOU'VE JUST")
        print("   PAID $200 FOR A WAGON.")
        print("YOU WILL NEED TO SPEND THE REST OF YOUR MONEY ON THE")
        print("   FOLLOWING ITEMS:")
        print()
        print("     OXEN - YOU CAN SPEND $200-$300 ON YOUR TEAM")
        print("            THE MORE YOU SPEND, THE FASTER YOU'LL GO")
        print("            BECAUSE YOU'LL HAVE BETTER ANIMALS")
        print()
        print("     FOOD - THE MORE YOU HAVE, THE LESS CHANCE THERE")
        print("            IS OF GETTING SICK")
        print()
        print("AMMUNITION - $1 BUYS A BELT OF 50 BULLETS")
        print("            YOU WILL NEED BULLETS FOR ATTACKS BY ANIMALS")
        print("            AND BANDITS, AND FOR HUNTING FOOD")
        print()
        print("CLOTHING - THIS IS ESPECIALLY IMPORTANT FOR THE COLD")
        print("            WEATHER YOU WILL ENCOUNTER WHEN CROSSING")
        print("            THE MOUNTAINS")
        print()
        print("MISCELLANEOUS SUPPLIES - THIS INCLUDES MEDICINE AND")
        print("            OTHER THINGS YOU WILL NEED FOR SICKNESS")
        print("            AND EMERGENCY REPAIRS")
        print()
        print()
        print("YOU CAN SPEND ALL YOUR MONEY BEFORE YOU START YOUR TRIP -")
        print("OR YOU CAN SAVE SOME OF YOUR CASH TO SPEND AT FORTS ALONG")
        print("THE WAY WHEN YOU RUN LOW. HOWEVER, ITEMS COST MORE AT")
        print("THE FORTS. YOU CAN ALSO GO HUNTING ALONG THE WAY TO GET")
        print("MORE FOOD.")
        print("WHENEVER YOU HAVE TO USE YOUR TRUSTY RIFLE ALONG THE WAY,")
        print("YOU WILL BE TOLD TO TYPE IN A WORD (ONE THAT SOUNDS LIKE A")
        print("GUN SHOT). THE FASTER YOU TYPE IN THAT WORD AND HIT THE")
        print('"RETURN" KEY, THE BETTER LUCK YOU\'LL HAVE WITH YOUR GUN.')
        print()
        print("AT EACH TURN, ALL ITEMS ARE SHOWN IN DOLLAR AMOUNTS")
        print("EXCEPT BULLETS")
        print('WHEN ASKED TO ENTER MONEY AMOUNTS, DON\'T USE A "$".')
        print()
        print("GOOD LUCK!!!")

    print()
    print()
    print("HOW GOOD A SHOT ARE YOU WITH YOUR RIFLE?")
    print("  (1) ACE MARKSMAN,  (2) GOOD SHOT,  (3) FAIR TO MIDDLIN'")
    print("         (4) NEED MORE PRACTICE,  (5) SHAKY KNEES")
    print("ENTER ONE OF THE ABOVE -- THE BETTER YOU CLAIM YOU ARE, THE")
    print("FASTER YOU'LL HAVE TO BE WITH YOUR GUN TO BE SUCCESSFUL.")
    d9 = get_number()
    if d9 > 5:
        d9 = 0

    # Initial purchases
    x1 = -1
    k8 = 0
    s4 = 0
    f1 = 0
    f2 = 0
    m = 0
    m9 = 0
    d3 = 0

    while True:
        print()
        print()
        while True:
            print("HOW MUCH DO YOU WANT TO SPEND ON YOUR OXEN TEAM", end="")
            a = get_number()
            if a < 200:
                print("NOT ENOUGH")
            elif a > 300:
                print("TOO MUCH")
            else:
                break

        while True:
            print("HOW MUCH DO YOU WANT TO SPEND ON FOOD", end="")
            f = get_number()
            if f < 0:
                print("IMPOSSIBLE")
            else:
                break

        while True:
            print("HOW MUCH DO YOU WANT TO SPEND ON AMMUNITION", end="")
            b = get_number()
            if b < 0:
                print("IMPOSSIBLE")
            else:
                break

        while True:
            print("HOW MUCH DO YOU WANT TO SPEND ON CLOTHING", end="")
            c = get_number()
            if c < 0:
                print("IMPOSSIBLE")
            else:
                break

        while True:
            print("HOW MUCH DO YOU WANT TO SPEND ON MISCELLANEOUS SUPPLIES", end="")
            m1 = get_number()
            if m1 < 0:
                print("IMPOSSIBLE")
            else:
                break

        t = 700 - a - f - b - c - m1
        if t >= 0:
            break
        print("YOU OVERSPENT--YOU ONLY HAD $700 TO SPEND.  BUY AGAIN")

    b = 50 * b
    print(f"AFTER ALL YOUR PURCHASES, YOU NOW HAVE {int(t)} DOLLARS LEFT")
    print()
    print("MONDAY MARCH 29 1847")
    print()

    # Main game loop
    first_turn = True
    while True:
        # Set date (except first turn)
        if not first_turn:
            if m >= 2040:
                # Final turn - victory
                print_victory(f, b, c, m1, t, d3, m, m2, e)
                return
            d3 += 1
            print()
            dates = [
                "APRIL 12", "APRIL 26", "MAY 10", "MAY 24",
                "JUNE 7", "JUNE 21", "JULY 5", "JULY 19",
                "AUGUST 2", "AUGUST 16", "AUGUST 31",
                "SEPTEMBER 13", "SEPTEMBER 27", "OCTOBER 11",
                "OCTOBER 25", "NOVEMBER 8", "NOVEMBER 22",
                "DECEMBER 6", "DECEMBER 20"
            ]
            if d3 <= len(dates):
                print(f"MONDAY {dates[d3 - 1]} 1847")
            else:
                print("YOU HAVE BEEN ON THE TRAIL TOO LONG  ------")
                print("YOUR FAMILY DIES IN THE FIRST BLIZZARD OF WINTER")
                print_game_over(None)
                return
            print()

        # Begin turn
        f = max(0, f)
        b = max(0, b)
        c = max(0, c)
        m1 = max(0, m1)
        if f < 13:
            print("YOU'D BETTER DO SOME HUNTING OR BUY FOOD AND SOON!!!!")
        f = int(f)
        b = int(b)
        c = int(c)
        m1 = int(m1)
        t = int(t)
        m = int(m)
        m2 = m

        if s4 == 1 or k8 == 1:
            t -= 20
            if t < 0:
                t = 0
                print("YOU CAN'T AFFORD A DOCTOR")
                print(f"YOU DIED OF {'INJURIES' if k8 == 1 else 'PNEUMONIA'}")
                print_game_over(None)
                return
            print("DOCTOR'S BILL IS $20")
            k8 = 0
            s4 = 0

        if m9 == 1:
            print("TOTAL MILEAGE IS 950")
            m9 = 0
        else:
            print(f"TOTAL MILEAGE IS {m}")

        print(f"{'FOOD':<14}{'BULLETS':<14}{'CLOTHING':<14}{'MISC. SUPP.':<14}{'CASH'}")
        print(f"{f:<14}{b:<14}{c:<14}{m1:<14}{t}")

        if x1 == -1 and first_turn:
            # No fort option on first turn
            while True:
                print("DO YOU WANT TO (1) HUNT, OR (2) CONTINUE")
                x = get_number()
                x = int(x)
                if x != 1:
                    x = 2
                x += 1
                if x == 2:
                    if b <= 39:
                        print("TOUGH---YOU NEED MORE BULLETS TO GO HUNTING")
                        continue
                break
            x1 *= -1
            first_turn = False
        elif x1 == -1:
            # No fort option
            while True:
                print("DO YOU WANT TO (1) HUNT, OR (2) CONTINUE")
                x = get_number()
                x = int(x)
                if x != 1:
                    x = 2
                x += 1
                if x == 2:
                    if b <= 39:
                        print("TOUGH---YOU NEED MORE BULLETS TO GO HUNTING")
                        continue
                break
            x1 *= -1
        else:
            x1 *= -1
            print("DO YOU WANT TO (1) STOP AT THE NEXT FORT, (2) HUNT, ", end="")
            print("OR (3) CONTINUE")
            x = get_number()
            x = int(x)
            if x < 1 or x > 2:
                x = 3

        # Do action
        if x == 1:
            # Stop at fort
            print("ENTER WHAT YOU WISH TO SPEND ON THE FOLLOWING")
            print("FOOD", end="")
            p, t = get_purchase(t)
            f += 2 / 3 * p
            print("AMMUNITION", end="")
            p, t = get_purchase(t)
            b = int(b + 2 / 3 * p * 50)
            print("CLOTHING", end="")
            p, t = get_purchase(t)
            c += 2 / 3 * p
            print("MISCELLANEOUS SUPPLIES", end="")
            p, t = get_purchase(t)
            m1 += 2 / 3 * p
            m -= 45
        elif x == 2:
            # Go hunting
            if b <= 39:
                print("TOUGH---YOU NEED MORE BULLETS TO GO HUNTING")
                # Fall through to fort option - redirect to action choice
                print("DO YOU WANT TO (1) STOP AT THE NEXT FORT, (2) HUNT, ", end="")
                print("OR (3) CONTINUE")
                x = get_number()
                x = int(x)
                if x < 1 or x > 2:
                    x = 3
                if x == 1:
                    print("ENTER WHAT YOU WISH TO SPEND ON THE FOLLOWING")
                    print("FOOD", end="")
                    p, t = get_purchase(t)
                    f += 2 / 3 * p
                    print("AMMUNITION", end="")
                    p, t = get_purchase(t)
                    b = int(b + 2 / 3 * p * 50)
                    print("CLOTHING", end="")
                    p, t = get_purchase(t)
                    c += 2 / 3 * p
                    print("MISCELLANEOUS SUPPLIES", end="")
                    p, t = get_purchase(t)
                    m1 += 2 / 3 * p
                    m -= 45
                # else continue
            else:
                m -= 45
                b1 = shooting_routine(d9)
                if b1 <= 1:
                    print("RIGHT BETWEEN THE EYES---YOU GOT A BIG ONE!!!!")
                    print("FULL BELLIES TONIGHT!")
                    f += 52 + random.random() * 6
                    b -= 10 + random.random() * 4
                elif 100 * random.random() < 13 * b1:
                    print("YOU MISSED---AND YOUR DINNER GOT AWAY.....")
                else:
                    f += 48 - 2 * b1
                    print("NICE SHOT--RIGHT ON TARGET--GOOD EATIN' TONIGHT!!")
                    b -= 10 + 3 * b1

        # Continue travel
        if f < 13:
            print("YOU RAN OUT OF FOOD AND STARVED TO DEATH")
            print_game_over(None)
            return

        # Eating
        while True:
            print("DO YOU WANT TO EAT (1) POORLY  (2) MODERATELY")
            print("OR (3) WELL", end="")
            e = get_number()
            e = int(e)
            if e < 1 or e > 3:
                continue
            food_cost = 8 + 5 * e
            if f - food_cost < 0:
                print("YOU CAN'T EAT THAT WELL")
                continue
            f -= food_cost
            break

        m += 200 + (a - 220) / 5 + 10 * random.random()
        l1 = 0
        c1 = 0

        # Riders attack check
        rider_check = random.random() * 10 * ((m / 100 - 4) ** 2 + 72) / ((m / 100 - 4) ** 2 + 12)
        skip_events = False

        if rider_check <= 1:
            s5 = 0
            print("RIDERS AHEAD.  THEY ", end="")
            if random.random() < 0.8:
                print("DON'T ", end="")
                s5 = 1
            print("LOOK HOSTILE")
            print("TACTICS")
            print("(1) RUN  (2) ATTACK  (3) CONTINUE  (4) CIRCLE WAGONS")
            if random.random() > 0.2:
                pass  # s5 stays the same
            else:
                s5 = 1 - s5

            while True:
                t1 = get_number()
                t1 = int(t1)
                if 1 <= t1 <= 4:
                    break

            if s5 == 1:
                # Friendly riders
                if t1 == 1:
                    m += 15
                    a -= 10
                elif t1 == 2:
                    m -= 5
                    b -= 100
                elif t1 == 3:
                    pass
                elif t1 == 4:
                    m -= 20
            else:
                # Hostile riders
                if t1 == 1:
                    m += 20
                    m1 -= 15
                    b -= 150
                    a -= 40
                elif t1 == 2:
                    b1 = shooting_routine(d9)
                    b -= b1 * 40 + 80
                    if b1 <= 1:
                        print("NICE SHOOTING---YOU DROVE THEM OFF")
                    elif b1 > 4:
                        print("LOUSY SHOT---YOU GOT KNIFED")
                        k8 = 1
                        print("YOU HAVE TO SEE OL' DOC BLANCHARD")
                    else:
                        print("KINDA SLOW WITH YOUR COLT .45")
                elif t1 == 3:
                    if random.random() > 0.8:
                        print("THEY DID NOT ATTACK")
                        skip_events = False
                        # Go directly to events
                    else:
                        b -= 150
                        m1 -= 15
                elif t1 == 4:
                    b1 = shooting_routine(d9)
                    b -= b1 * 30 + 80
                    m -= 25
                    if b1 <= 1:
                        print("NICE SHOOTING---YOU DROVE THEM OFF")
                    elif b1 > 4:
                        print("LOUSY SHOT---YOU GOT KNIFED")
                        k8 = 1
                        print("YOU HAVE TO SEE OL' DOC BLANCHARD")
                    else:
                        print("KINDA SLOW WITH YOUR COLT .45")

            if s5 == 1:
                print("RIDERS WERE FRIENDLY, BUT CHECK FOR POSSIBLE LOSSES")
            else:
                print("RIDERS WERE HOSTILE--CHECK FOR LOSSES")

            if b < 0:
                print("YOU RAN OUT OF BULLETS AND GOT MASSACRED BY THE RIDERS")
                print_game_over(None)
                return

        # Selection of events
        event_thresholds = [6, 11, 13, 15, 17, 22, 32, 35, 37, 42, 44, 54, 64, 69, 95]
        r1 = 100 * random.random()

        event = 16  # default: helpful indians
        for i, threshold in enumerate(event_thresholds):
            if r1 <= threshold:
                event = i + 1
                break

        go_to_illness = False
        after_illness_goto = "after_events"  # or "check_mileage"

        if event == 16:
            print("HELPFUL INDIANS SHOW YOU WHERE TO FIND MORE FOOD")
            f += 14
        elif event == 1:
            print("WAGON BREAKS DOWN--LOSE TIME AND SUPPLIES FIXING IT")
            m -= 15 + 5 * random.random()
            m1 -= 8
        elif event == 2:
            print("OX INJURES LEG---SLOWS YOU DOWN REST OF TRIP")
            m -= 25
            a -= 20
        elif event == 3:
            print("BAD LUCK---YOUR DAUGHTER BROKE HER ARM")
            print("YOU HAD TO STOP AND USE SUPPLIES TO MAKE A SLING")
            m -= 5 + 4 * random.random()
            m1 -= 2 + 3 * random.random()
        elif event == 4:
            print("OX WANDERS OFF---SPEND TIME LOOKING FOR IT")
            m -= 17
        elif event == 5:
            print("YOUR SON GETS LOST---SPEND HALF THE DAY LOOKING FOR HIM")
            m -= 10
        elif event == 6:
            print("UNSAFE WATER--LOSE TIME LOOKING FOR CLEAN SPRING")
            m -= 10 * random.random() + 2
        elif event == 7:
            if m > 950:
                print("COLD WEATHER---BRRRRRRR!---YOU ", end="")
                if c > 22 + 4 * random.random():
                    print("HAVE ENOUGH CLOTHING TO KEEP YOU WARM")
                else:
                    print("DON'T HAVE ENOUGH CLOTHING TO KEEP YOU WARM")
                    c1 = 1
                    go_to_illness = True
            else:
                print("HEAVY RAINS---TIME AND SUPPLIES LOST")
                f -= 10
                b -= 500
                m1 -= 15
                m -= 10 * random.random() + 5
        elif event == 8:
            print("BANDITS ATTACK")
            b1 = shooting_routine(d9)
            b -= 20 * b1
            if b < 0:
                print("YOU RAN OUT OF BULLETS---THEY GET LOTS OF CASH")
                t = t / 3
            elif b1 <= 1:
                print("QUICKEST DRAW OUTSIDE OF DODGE CITY!!!")
                print("YOU GOT 'EM!")
                go_to_illness = False
                # skip bandit injury, go to after_events
            else:
                pass  # fall through to bandit injury

            if b < 0 or (b >= 0 and b1 > 1):
                print("YOU GOT SHOT IN THE LEG AND THEY TOOK ONE OF YOUR OXEN")
                k8 = 1
                print("BETTER HAVE A DOC LOOK AT YOUR WOUND")
                m1 -= 5
                a -= 20
        elif event == 9:
            print("THERE WAS A FIRE IN YOUR WAGON--FOOD AND SUPPLIES DAMAGE")
            f -= 40
            b -= 400
            m1 -= random.random() * 8 + 3
            m -= 15
        elif event == 10:
            print("LOSE YOUR WAY IN HEAVY FOG---TIME IS LOST")
            m -= 10 + 5 * random.random()
        elif event == 11:
            print("YOU KILLED A POISONOUS SNAKE AFTER IT BIT YOU")
            b -= 10
            m1 -= 5
            if m1 < 0:
                print("YOU DIE OF SNAKEBITE SINCE YOU HAVE NO MEDICINE")
                print_game_over(None)
                return
        elif event == 12:
            print("WAGON GETS SWAMPED FORDING RIVER--LOSE FOOD AND CLOTHES")
            f -= 30
            c -= 20
            m -= 20 + 20 * random.random()
        elif event == 13:
            print("WILD ANIMALS ATTACK!")
            b1 = shooting_routine(d9)
            if b <= 39:
                print("YOU WERE TOO LOW ON BULLETS--")
                print("THE WOLVES OVERPOWERED YOU")
                k8 = 1
                print(f"YOU DIED OF INJURIES")
                print_game_over(None)
                return
            if b1 <= 2:
                print("NICE SHOOTIN' PARTNER---THEY DIDN'T GET MUCH")
            else:
                print("SLOW ON THE DRAW---THEY GOT AT YOUR FOOD AND CLOTHES")
            b -= 20 * b1
            c -= b1 * 4
            f -= b1 * 8
        elif event == 14:
            print("HAIL STORM---SUPPLIES DAMAGED")
            m -= 5 + random.random() * 10
            b -= 200
            m1 -= 4 + random.random() * 3
        elif event == 15:
            if e == 1:
                go_to_illness = True
            elif e == 3:
                if random.random() < 0.5:
                    go_to_illness = True
            else:
                if random.random() > 0.25:
                    go_to_illness = True

        if go_to_illness:
            m, m1, s4_new, died = illness_routine(e, m, m1)
            if s4_new:
                s4 = s4_new
            if died:
                print(f"YOU DIED OF {'INJURIES' if k8 == 1 else 'PNEUMONIA'}")
                print_game_over(None)
                return
            if l1 == 1:
                # After blizzard illness, go to check_mileage
                if m > 950:
                    continue  # back to set date
                m9 = 1
                continue

        # Mountains
        if m <= 950:
            continue  # back to set date

        mountain_check = random.random() * 10 * ((9 - ((m / 100 - 15) ** 2 + 72)) / ((m / 100 - 15) ** 2 + 12))
        if mountain_check <= 0:
            r = random.random()
            if r <= 0.1:
                print("RUGGED MOUNTAINS")
                print("YOU GOT LOST---LOSE VALUABLE TIME TRYING TO FIND TRAIL!")
                m -= 60
            elif r <= 0.11 + 0.1:
                print("RUGGED MOUNTAINS")
                print("WAGON DAMAGED!---LOSE TIME AND SUPPLIES")
                m1 -= 5
                b -= 200
                m -= 20 + 30 * random.random()
            else:
                print("RUGGED MOUNTAINS")
                print("THE GOING GETS SLOW")
                m -= 45 + random.random() / 0.02

        # Check passes
        if f1 == 0:
            f1 = 1
            if random.random() >= 0.8:
                print("YOU MADE IT SAFELY THROUGH SOUTH PASS--NO SNOW")
            else:
                # Blizzard
                print("BLIZZARD IN MOUNTAIN PASS--TIME AND SUPPLIES LOST")
                l1 = 1
                f -= 25
                m1 -= 10
                b -= 300
                m -= 30 + 40 * random.random()
                if c < 18 + 2 * random.random():
                    m, m1, s4_new, died = illness_routine(e, m, m1)
                    if s4_new:
                        s4 = s4_new
                    if died:
                        print(f"YOU DIED OF {'INJURIES' if k8 == 1 else 'PNEUMONIA'}")
                        print_game_over(None)
                        return
                # Check mileage after blizzard
                if m > 950:
                    continue
                m9 = 1
                continue
        elif m >= 1700 and f2 == 0:
            f2 = 1
            if random.random() >= 0.7:
                pass  # safe through blue mountains
            else:
                # Blizzard
                print("BLIZZARD IN MOUNTAIN PASS--TIME AND SUPPLIES LOST")
                l1 = 1
                f -= 25
                m1 -= 10
                b -= 300
                m -= 30 + 40 * random.random()
                if c < 18 + 2 * random.random():
                    m, m1, s4_new, died = illness_routine(e, m, m1)
                    if s4_new:
                        s4 = s4_new
                    if died:
                        print(f"YOU DIED OF {'INJURIES' if k8 == 1 else 'PNEUMONIA'}")
                        print_game_over(None)
                        return
                # Check mileage after blizzard
                if m > 950:
                    continue
                m9 = 1
                continue

        # Check mileage
        if m > 950:
            continue  # back to set date
        m9 = 1
        continue  # back to set date


if __name__ == "__main__":
    main()
