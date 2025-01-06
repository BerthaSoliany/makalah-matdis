# Define a character
define b = Character("Bob")

# Define image
image bg room = im.Scale("bg room.jpeg", config.screen_width, config.screen_height)
image Abyssal_Mark = "memories/Abyssal_Mark.png"
image Floof_Attack = "memories/Floof_Attack.png"
image Fluffy_Treatment = "memories/Fluffy_Treatment.png"
image Goodcat_Code = "memories/Goodcat_Code.png"
image Seething_Flames = "memories/Seething_Flames.png"
image Snowfall_Encounter = "memories/Snowfall_Encounter.png"
image Temple_Promise = "memories/Temple_Promise.png"
image Tender_Night = "memories/Tender_Night.png"
image Unforgettable_Adventure = "memories/Unforgettable_Adventure.png"
image Blossoms = "memories/Blossoms.png"
image Business_Trip = "memories/Business_Trip.png"
image Captivating_Flavor = "memories/Captivating_Flavor.png"
image Cozy_Afternoon = "memories/Cozy_Afternoon.png"
image Deep_Sea_Riches = "memories/Deep_Sea_Riches.png"
image Fluffy_Trap = "memories/Fluffy_Trap.png"
image Fragment_Of_Time = "memories/Fragment_Of_Time.png"
image Gentle_Twilight = "memories/Gentle_Twilight.png"
image Immobilized = "memories/Immobilized.png"
image Nightplumes = "memories/Nightplumes.png"
image Precious_Bonfire = "memories/Precious_Bonfire.png"
image Promise_Everlasting = "memories/Promise_Everlasting.png"
image Sparkling_Traces = "memories/Sparkling_Traces.jpg"
image A_Day_Of_Snow = "memories/A_Day_Of_Snow.png"
image A_Long_Night = "memories/A_Long_Night.png"
image Beginning = "memories/Beginning.png"
image Hidden_Shadow = "memories/Hidden_Shadow.png"
image Lost_Signal = "memories/Lost_Signal.png"
image Razors_Dance = "memories/Razors_Dance.png"
image Sapphire_Scar = "memories/Sapphire_Scar.png"
image Scorching_Rain = "memories/Scorching_Rain.png"
image Spring_Remnants = "memories/Spring_Remnants.png"
image Starry_Sound = "memories/Starry_Sound.png"
image Tender_Curve = "memories/Tender_Curve.png"
image Wild_Gaze = "memories/Wild_Gaze.png"
image Backlight = "memories/Backlight.jpg"
image Clean_Up = "memories/Clean_Up.png"
image Guardian = "memories/Guardian.png"
image Just_Encounter = "memories/Just_Encounter.jpg"
image Lame_Party = "memories/Lame_Party.jpg"
image Listen = "memories/Listen.png"
image My_Decision = "memories/My_Decision.jpg"
image Nestle = "memories/Nestle.png"
image Shoo_In = "memories/Shoo_In.jpeg"
image Social_Occasion = "memories/Social_Occasion.jpg"
image Sweet_Burden = "memories/Sweet_Burden.png"
image Thoughts = "memories/Thoughts.png"

transform custom:
    yalign 0.6
    xalign 0.5
    xsize 600
    ysize 600

transform custom2:
    yalign 0.5
    xalign 0.5
    xsize 600
    ysize 800

transform memory_zoom:
    yalign 0.5
    xalign 0.5
    zoom 0.5
    linear 0.5 zoom 1.0


init python:
    import random
    from collections import defaultdict
    import time

    # Define gacha system
    class GachaSystem:
        def __init__(self, initial_coins):
            # PRNG Parameters
            self.a = 1664525
            self.c = 1013904223
            self.m = 2**32  # Large prime modulus
            self.seed = int(time.time() * 1000) % self.m  # Initial seed
            self.coins = initial_coins
            self.cost_per_pull = 150
            self.normal_pity_count = 0
            self.event_pity_count = 0
            self.event_soft_pity_count = 0
            self.pity_threshold = 30
            self.tier_probabilities = {
                "Five-star": {"event": 2, "normal": 3},  # 2% event, 3% normal Five-star
                "Four-star": 15,
                "Three-star": 80,
            }

            self.memories_by_tier = {
                "Five-star": [
                    "Blossoms",
                    "Business Trip",
                    "Captivating Flavor",
                    "Cozy Afternoon",
                    "Deep Sea Riches",
                    "Fluffy Trap",
                    "Fragment Of Time",
                    "Gentle Twilight",
                    "Immobilized",
                    "Nightplumes",
                    "Precious Bonfire",
                    "Promise Everlasting",
                    "Sparkling Traces"
                ],
                "Four-star": [
                    "A Day Of Snow",
                    "A Long Night",
                    "Beginning",
                    "Hidden Shadow",
                    "Lost Signal",
                    "Razor's Dance",
                    "Sapphire Scar",
                    "Scorching Rain",
                    "Spring Remnants",
                    "Starry Sound",
                    "Tender Curve",
                    "Wild Gaze"
                ],
                "Three-star": [
                    "Backlight",
                    "Clean Up",
                    "Guardian",
                    "Just Encounter",
                    "Lame Party",
                    "Listen",
                    "My Decision",
                    "Nestle",
                    "Shoo In",
                    "Social Occasion",
                    "Sweet Burden",
                    "Thoughts"
                ],
            }

            self.event_memory = ["Abyssal Mark", "Floof Attack", "Fluffy Treatment", "Goodcat Code", "Seething Flames", "Snowfall Encounter", "Temple Promise", "Tender Night", "Unforgettable Adventure"]


        def prng(self):
            self.seed = (self.a * self.seed + self.c) % self.m
            return self.seed / self.m

        def can_afford(self, pulls):
            return self.coins >= pulls * self.cost_per_pull

        def deduct_coins(self, pulls):
            self.coins -= pulls * self.cost_per_pull

        def get_card_tier(self, card_name):
            for tier, cards in self.memories_by_tier.items():
                if card_name in cards:
                    return tier
            if card_name in self.event_memory:
                return "Event (Five-star)"
            return "Unknown"


        def draw(self, banner="normal", pulls=1):
            if not self.can_afford(pulls):
                return ["You do not have enough diamonds to pull."]

            self.deduct_coins(pulls)
            results = []
            for _ in range(pulls):
                result = self.draw_single(banner=banner)
                results.append(result)
            return results


        def draw_single(self, banner):
            pity_count = self.normal_pity_count if banner == "normal" else self.event_pity_count

            if pity_count >= self.pity_threshold:
                if banner == "normal":
                    self.normal_pity_count = 0
                    return random.choice(self.memories_by_tier["Five-star"])
                elif banner == "event":
                    self.event_pity_count = 0
                    self.event_soft_pity_count += 1  # Increment event pity counter

                    # Soft pity logic for event banner
                    if self.event_soft_pity_count == 2:  # Even soft pity: guarantee event memory
                        self.event_soft_pity_count = 0  # Reset event soft pity
                        return random.choice(self.event_memory)
                    else:  # Odd soft pity: random Five-star
                        return random.choice(self.memories_by_tier["Five-star"] + [self.event_memory])

            rand_num = self.prng() * 100  # Scale to [0, 100)
            cumulative = 0
            selected_tier = None

            for tier, probability in self.tier_probabilities.items():
                if isinstance(probability, dict):
                    probability = sum(probability.values())
                cumulative += probability
                if rand_num < cumulative:
                    selected_tier = tier
                    break

            if isinstance(self.tier_probabilities[selected_tier], dict):
                tier_probability = self.tier_probabilities[selected_tier][banner]
            else:
                tier_probability = self.tier_probabilities[selected_tier]

            memories = self.memories_by_tier[selected_tier]
            # tier_probability = self.tier_probabilities[selected_tier]
            total_memories = len(memories)

            per_memory_probability = tier_probability / total_memories
            probabilities = {memory: per_memory_probability for memory in memories}

            rand_num = self.prng() * tier_probability
            cumulative = 0

            for memory, probability in probabilities.items():
                cumulative += probability
                if rand_num < cumulative:
                    if selected_tier == "Five-star":
                        if banner == "normal":
                            self.normal_pity_count = 0  # Reset normal pity if Five-star drawn
                        elif banner == "event" and memory == self.event_memory:
                            self.event_pity_count = 0  # Reset event pity if event memory drawn
                    else:
                        if banner == "normal":
                            self.normal_pity_count += 1
                        elif banner == "event":
                            self.event_pity_count += 1
                    return memory

            return "Error"

    # Create a global gacha system instance
    gacha = GachaSystem(initial_coins=3000)
    results = defaultdict(int)
    obtained_memories = defaultdict(int)
    memory_images = {
        "Abyssal Mark": "Abyssal_Mark",
        "Floof Attack": "Floof_Attack",
        "Fluffy Treatment": "Fluffy_Treatment",
        "Goodcat Code": "Goodcat_Code",
        "Seething Flames": "Seething_Flames",
        "Snowfall Encounter": "Snowfall_Encounter",
        "Temple Promise": "Temple_Promise",
        "Tender Night": "Tender_Night",
        "Unforgettable Adventure": "Unforgettable_Adventure",
        "Blossoms": "Blossoms",
        "Business Trip": "Business_Trip",
        "Captivating Flavor": "Captivating_Flavor",
        "Cozy Afternoon": "Cozy_Afternoon",
        "Deep Sea Riches": "Deep_Sea_Riches",
        "Fluffy Trap": "Fluffy_Trap",
        "Fragment Of Time": "Fragment_Of_Time",
        "Gentle Twilight": "Gentle_Twilight",
        "Immobilized": "Immobilized",
        "Nightplumes": "Nightplumes",
        "Precious Bonfire": "Precious_Bonfire",
        "Promise Everlasting": "Promise_Everlasting",
        "Sparkling Traces": "Sparkling_Traces",
        "A Day Of Snow": "A_Day_Of_Snow",
        "A Long Night": "A_Long_Night",
        "Beginning": "Beginning",
        "Hidden Shadow": "Hidden_Shadow",
        "Lost Signal": "Lost_Signal",
        "Razor's Dance": "Razors_Dance",
        "Sapphire Scar": "Sapphire_Scar",
        "Scorching Rain": "Scorching_Rain",
        "Spring Remnants": "Spring_Remnants",
        "Starry Sound": "Starry_Sound",
        "Tender Curve": "Tender_Curve",
        "Wild Gaze": "Wild_Gaze",
        "Backlight": "Backlight",
        "Clean Up": "Clean_Up",
        "Guardian": "Guardian",
        "Just Encounter": "Just_Encounter",
        "Lame Party": "Lame_Party",
        "Listen": "Listen",
        "My Decision": "My_Decision",
        "Nestle": "Nestle",
        "Shoo In": "Shoo_In",
        "Social Occasion": "Social_Occasion",
        "Sweet Burden": "Sweet_Burden",
        "Thoughts": "Thoughts"
    }

# The game starts here.

label start:
    scene bg room
    show chicken at custom

    # These display lines of dialogue.
    b "Oh, hello there!"
    b "I'm Bob, the chicken."
    b "I'm here to guide you through this game."
    b "Well, I say 'game', but it's more of a demo."
    b "I hope you enjoy it anyway!"
    b "First, Let's start by explaining this game."
    b "This demo is for studying purposes and it is for you to enjoy the beauty of gacha games."
    b "The title for my paper is 'The Mathematics of Luck: Number Theory in the Gacha System of Love and DeepSpace'."
    b "Yes, as you can see, I'm using Love and Deepspace gacha system as a case study for my paper. Because of that, in this demo, you will be able to try the gacha system of Love and Deepspace."
    b "FYI, I use number theory to simulated it."
    b "You can get a memory by spending a certain amount of diamonds. The currency is called 'diamonds' and cards are called 'memories'."
    b "In this demo, you can get one memory by spending 150 diamonds or 1500 for ten memories."
    b "I will give you 3000 diamonds to start with."
    b "Now, what type of memory banner you want to try? Normal or Event?"
    b "With the Event Banner, you can get a special memory that is only available during the event. While with the Normal Banner, you can get a memory that is always available."
    b "There is also a tier system for the memorys. The higher the tier, the better the memory. But of course, the higher the tier, the lower the chance to get it."

    call bannerType
    return

label bannerType:  
    show chicken at custom

    b "So, what type of banner do you want to try?"

    menu:
        "Normal":
            jump normal
        "Event":
            jump event
        "Exit":
            jump end
    return

label menu:
    show chicken at custom
    b "What would you like to do?"
    menu:
        "Check Pity":
            jump show_pity
        "Pull one time":
            $ pulls = 1
            jump pull
        "Pull ten times":
            $ pulls = 10
            jump pull
        "I changed my mind":
            jump bannerType
    return


label normal:
    show chicken at custom

    b "Great choice!"
    b "You will now experience the Normal Banner of Love and Deepspace."

    $ banner = "normal"

    call menu
    return

label event:
    show chicken at custom

    b "Great choice!"
    b "You will now experience the Event Banner of Love and Deepspace."

    $ banner = "event"

    call menu
    return

label pull:
    if gacha.can_afford(pulls):
        python:
            results = gacha.draw(banner=banner, pulls=pulls)
            for result in results:
                if result == "You do not have enough diamonds to pull.":
                    renpy.say(None, result)
                    break
                obtained_memories[result] += 1
                memory_tier = gacha.get_card_tier(result)

                if result in memory_images:
                    renpy.show(memory_images[result], at_list=(custom2, memory_zoom))
                    renpy.say(None, f"You got a {memory_tier} memory: {result}!")
                    renpy.pause(1.5)
                    renpy.hide(memory_images[result])


                # renpy.say(None, f"You got a {memory_tier} memory: {result}!")
                # if result in memory_images:
                #     renpy.show(memory_images[result], at_list=(custom2, memory_zoom))
                #     renpy.pause(3)
                #     renpy.hide(memory_images[result])
            renpy.say(None, f"You now have {gacha.coins} diamonds remaining.")
    else:
        "You do not have enough diamonds to pull."
        call coin    

    call menu
    return

label show_pity:
    show chicken at custom

    if banner == "normal":
        b "Normal Banner: [gacha.normal_pity_count]/[gacha.pity_threshold]"
    elif banner == "event":
        b "Event Banner: [gacha.event_pity_count]/[gacha.pity_threshold] (Soft Pity Count: [gacha.event_soft_pity_count])"

    call menu
    return

label coin:
    show chicken at custom

    b "Do you want to try again? You can get 10000 diamonds for free."

    menu:
        "Yes":
            $ gacha.coins = gacha.coins + 10000
            return
        "No":
            return

label end:
    show chicken at custom

    b "Thank you for playing this demo!"
    b "I hope you enjoyed it."

    python:
        if not obtained_memories:
            renpy.say(None, "You did not obtain any memories.")
        else:
            renpy.say(None, "Here are the memories you collected during this demo:")
            for memory, count in obtained_memories.items():
                if memory in memory_images:
                    renpy.show(memory_images[memory], at_list=(custom2, memory_zoom))
                    renpy.say(None, f"{memory}: {count} time(s).")
                    renpy.pause(3)
                    renpy.hide(memory_images[memory])

    b "If you have any feedback, feel free to share it with me."
    b "Do you want to reset the game?"

    menu:
        "Restart the game":
            jump reset_game
        "Exit":
            b "Thank you for playing! See you next time!"
            return 
    return

label reset_game:
    python:
        gacha.coins = 3000
        obtained_memories.clear()
        
    b "The game has been reset. Enjoy playing again!"
    jump start
