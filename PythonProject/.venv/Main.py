from graphics import Canvas
from Intro import intro
from Names import names
from Date_Profiles import profiles
from Scenes import first_date_scenes, scenes
import random
from Mini_Arcs import mini_arcs

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
START_X = 20
START_Y = 50
FONT_SIZE = 18
MAIN_BUTTON_COLOR = "brown"
SECONDARY_BUTTON_COLOR = "red"


def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    background = canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, 'black')
    # full_game_intro(canvas, intro, START_X, CANVAS_HEIGHT, FONT_SIZE)
    score = [0, 0, 0]

    invitation_to_start(canvas, CANVAS_WIDTH, CANVAS_HEIGHT, FONT_SIZE, "Starting the game...")
    message1 = "Step 1 of 1. Choose your dating partner"
    step_1 = create_text(canvas, START_X, START_Y, FONT_SIZE, message1)
    message1_1 = "by clicking on their name:"
    step1_1 = create_text(canvas, START_X, START_Y + FONT_SIZE + 5, FONT_SIZE, message1_1)
    partner_name = select_partner_name(canvas, START_X, START_Y, FONT_SIZE, names)
    canvas.set_hidden(step_1, True)
    canvas.set_hidden(step1_1, True)
    partner_profile = get_partner_profile(profiles, partner_name)
    endings = partner_profile['ending']
    date_or_show_overview(canvas, START_X, START_Y, FONT_SIZE, partner_name, partner_profile)
    invitation_to_start(canvas, CANVAS_WIDTH, CANVAS_HEIGHT, FONT_SIZE, "Stage 1 of 5. The First Date...")
    show_scene(canvas, START_X, START_Y, FONT_SIZE, first_date_scenes)
    partner_introduction(canvas, START_X, START_Y, FONT_SIZE, partner_profile)
    # Num of stages is 5
    date_result = ""
    for i in range(5):
        a = i + 1
        date_result = the_date(canvas, START_X, START_Y, FONT_SIZE, partner_profile, a, score)
        if date_result == "bad":
            show_the_ending(canvas, START_X, START_Y, FONT_SIZE, endings["bad"])
            return
        elif date_result == "neutral":
            show_the_ending(canvas, START_X, START_Y, FONT_SIZE, endings["neutral"])
            return

        if a == 1 or a == 2 or a == 3 or a == 4 or a == 5:
            to_show = show_mini_arc(canvas, START_X, START_Y, FONT_SIZE)
            if to_show:
                play_out_mini_arc(canvas, START_X, START_Y, FONT_SIZE, mini_arcs)

        # For next stage
        n = i + 2
        title = "Stage " + str(n) + " of 5..."
        if a < 5:  # less than 5 so it won't show this again after stage 5
            invitation_to_start(canvas, CANVAS_WIDTH, CANVAS_HEIGHT, FONT_SIZE, title)
            show_scene(canvas, START_X, START_Y, FONT_SIZE, scenes)

    if date_result != "bad" or date_result != "neutral":
        show_the_ending(canvas, START_X, START_Y, FONT_SIZE, endings["good"])


def full_game_intro(canvas, intro, x, y, size):
    for message in intro:
        game_intro(canvas, message, x, y, size)


def game_intro(canvas, message, x, y, size):
    intro = canvas.create_text(
        x,
        y / 2 - size,
        text=message,
        font='Arial',
        font_size=size,
        color='white'
    )
    time.sleep(1.8)
    canvas.set_hidden(intro, True)


def invitation_to_start(canvas, x, y, size, message):
    invitation = canvas.create_text(
        x / 4 + size / 2,
        y / 2 - size,
        text=message,
        font='Arial',
        font_size=size,
        color='white'
    )
    time.sleep(2)
    canvas.set_hidden(invitation, True)


def date_or_show_overview(canvas, x, y, size, partner_name, partner_profile):
    message = "You've chosen to date:"
    acknowledgement = create_text(canvas, x, y, size, message)
    show_name = create_text(canvas, x + 10, y + 50, size + 10, partner_name)
    chosen_option = choose_an_option(canvas, x, y, size)

    if chosen_option:
        canvas.set_hidden(acknowledgement, True)
        canvas.set_hidden(show_name, True)

    if chosen_option == 1:
        return
    elif chosen_option == 2:
        show_partner_overview(canvas, x, y, size, partner_name, partner_profile)


def choose_an_option(canvas, x, y, size):
    option_1 = "A. Let's go on a first date!"
    show_option_1 = create_text(canvas, x + 10, y + 50 + size + 10 + 25, size, option_1)
    option_2 = "B. Show my date's personal background"
    show_option_2 = create_text(canvas, x + 10, y + 50 + size + 10 + 25 + 5 + size, size, option_2)
    canvas.wait_for_click()
    click = canvas.get_new_mouse_clicks()
    # as flag - to make sure the player clicks on valid elements
    i = 0

    while i != 1:
        if len(click) != 0:
            clicked_option_1 = click[0][0] >= x + 10 and click[0][0] <= 232 and click[0][
                1] >= y + 50 + size + 10 + 25 and click[0][1] <= y + 50 + (2 * size) + 10 + 25
            clicked_option_2 = click[0][0] >= x + 10 and click[0][0] <= 352 and click[0][1] >= y + 50 + (
                    2 * size) + 10 + 25 + 5 and click[0][1] <= y + 50 + (3 * size) + 10 + 25

            if clicked_option_1:
                i = 1
                canvas.set_hidden(show_option_1, True)
                canvas.set_hidden(show_option_2, True)
                return 1
            elif clicked_option_2:
                i = 1
                canvas.set_hidden(show_option_1, True)
                canvas.set_hidden(show_option_2, True)
                return 2
            else:
                i = 0
        click = canvas.get_new_mouse_clicks()


def create_text(canvas, x, y, size, message):
    text = canvas.create_text(
        x,
        y,
        text=message,
        font='Arial',
        font_size=size,
        color="white"
    )
    return text


def select_partner_name(canvas, x, y, size, names):
    y = y + 50 + size + 5
    y1 = y
    a = 0
    options = []
    while a != len(names):
        for name in names:
            n = a + 1
            message = str(n) + ". " + name
            option = create_text(canvas, x, y1, size, message)
            options.append(option)
            a += 1
            y1 += size + 5
    canvas.wait_for_click()
    click = canvas.get_new_mouse_clicks()
    # as flag - to make sure the player clicks on valid elements
    i = 0
    while i != 1:
        if len(click) != 0:

            clicked_option_1 = click[0][0] >= x and click[0][0] <= 256 and click[0][1] >= y and click[0][1] <= y + size
            clicked_option_2 = click[0][0] >= x and click[0][0] <= 217 and click[0][1] >= y + size + 5 and click[0][
                1] <= y + (2 * size) + 5
            """
            clicked_option_3 = click[0][0] >= x and click[0][0] <= 211 and click[0][1] >= y + (2 * (size + 5)) and \
                               click[0][1] <= y + (3 * size) + (2 * 5)
            clicked_option_4 = click[0][0] >= x and click[0][0] <= 210 and click[0][1] >= y + (3 * (size + 5)) and \
                               click[0][1] <= y + (4 * size) + (3 * 5)
            clicked_option_5 = click[0][0] >= x and click[0][0] <= 190 and click[0][1] >= y + (4 * (size + 5)) and \
                               click[0][1] <= y + (5 * size) + (4 * 5)
            clicked_option_6 = click[0][0] >= x and click[0][0] <= 227 and click[0][1] >= y + (5 * (size + 5)) and \
                               click[0][1] <= y + (6 * size) + (5 * 5)
            """
            if clicked_option_1:
                i = 1
                for option in options:
                    canvas.set_hidden(option, True)
                return names[0]
            elif clicked_option_2:
                i = 1
                for option in options:
                    canvas.set_hidden(option, True)
                return names[1]
            else:
                i = 0
        click = canvas.get_new_mouse_clicks()


def get_partner_profile(profiles, partner_name):
    for i in range(len(profiles)):
        is_chosen = profiles[i]["profile"]["nickname"] == partner_name
        if is_chosen:
            return profiles[i]["profile"]


def show_partner_overview(canvas, x, y, size, partner_name, partner_profile):
    overviews = partner_profile['background']['overview']

    header = partner_name + " Overview"
    title = create_text(canvas, x, y, size + 3, header)
    y1 = y + 40
    texts = []
    for overview in overviews:
        text = create_text(canvas, x + 5, y1, size, overview)
        texts.append(text)
        y1 += 23

    button1 = add_button(canvas, 180, 315, 180, 30, SECONDARY_BUTTON_COLOR)
    read_next = create_text(canvas, 185, 320, size, "Read next page →")

    button2 = add_button(canvas, 180, 350, 180, 30, MAIN_BUTTON_COLOR)
    go_on_a_date = create_text(canvas, 185, 355, size, "Go on a first date →")
    canvas.wait_for_click()
    click = canvas.get_new_mouse_clicks()
    chosen_button = navigate(canvas, click, texts)

    if chosen_button == 2:
        canvas.set_hidden(title, True)
        canvas.set_hidden(button1, True)
        canvas.set_hidden(button2, True)
        canvas.set_hidden(read_next, True)
        canvas.set_hidden(go_on_a_date, True)
        return

    elif chosen_button == 1:
        relationships = partner_profile["background"]["relationship_history"]

        header1 = "Relationship History:"
        title1 = create_text(canvas, x + 5, y + size + 20, size + 1, header1)
        y2 = y + 50 + size + 3
        texts1 = []
        for relationship in relationships:
            text = create_text(canvas, x + 5, y2, size, relationship)
            texts1.append(text)
            y2 += 23
        canvas.wait_for_click()
        click = canvas.get_new_mouse_clicks()
        chosen_button_1 = navigate(canvas, click, texts1)

        if chosen_button_1 == 2:
            canvas.set_hidden(title, True)
            canvas.set_hidden(title1, True)
            canvas.set_hidden(button1, True)
            canvas.set_hidden(button2, True)
            canvas.set_hidden(read_next, True)
            canvas.set_hidden(go_on_a_date, True)
            return

        elif chosen_button_1 == 1:
            canvas.set_hidden(title1, True)
            for text in texts1:
                canvas.set_hidden(text, True)

            viewpoints = partner_profile["background"]["friends_see_them_as"]
            header2 = "Friends see them as:"
            title2 = create_text(canvas, x + 5, y + size + 20, size + 1, header2)
            y3 = y + 50 + size + 3
            texts2 = []
            for viewpoint in viewpoints:
                text = create_text(canvas, x + 5, y3, size, viewpoint)
                texts2.append(text)
                y3 += 23
            canvas.wait_for_click()
            click = canvas.get_new_mouse_clicks()
            chosen_button_1_1 = navigate(canvas, click, texts2)

            if chosen_button_1_1 == 2:
                canvas.set_hidden(title, True)
                canvas.set_hidden(title2, True)
                canvas.set_hidden(button1, True)
                canvas.set_hidden(button2, True)
                canvas.set_hidden(read_next, True)
                canvas.set_hidden(go_on_a_date, True)
                return

            elif chosen_button_1_1 == 1:
                canvas.set_hidden(button1, True)
                canvas.set_hidden(read_next, True)
                canvas.set_hidden(title2, True)
                for text in texts2:
                    canvas.set_hidden(text, True)
                secret_feelings = partner_profile["background"]["they_secretly_feel"]
                header3 = "They secretly feel:"
                title3 = create_text(canvas, x + 5, y + size + 20, size + 1, header3)
                y4 = y + 50 + size + 3
                texts3 = []
                for secret in secret_feelings:
                    text = create_text(canvas, x + 5, y4, size, secret)
                    texts3.append(text)
                    y4 += 23
                canvas.wait_for_click()
                click = canvas.get_new_mouse_clicks()
                go_to_first_date = one_button_navigate(canvas, click, texts3, 180, 180 + 180, 350, 350 + 30)
                if go_to_first_date:
                    canvas.set_hidden(title, True)
                    canvas.set_hidden(title3, True)
                    canvas.set_hidden(button2, True)
                    canvas.set_hidden(go_on_a_date, True)
                    return


def navigate(canvas, click, texts):
    i = 0
    while i != 1:
        if len(click) != 0:

            clicked_button_1 = click[0][0] >= 180 and click[0][0] <= 180 + 180 and click[0][1] >= 315 and click[0][
                1] <= 315 + 30
            clicked_button_2 = click[0][0] >= 180 and click[0][0] <= 180 + 180 and click[0][1] >= 350 and click[0][
                1] <= 350 + 30

            if clicked_button_1:
                i = 1
                for text in texts:
                    canvas.set_hidden(text, True)
                return 1
            elif clicked_button_2:
                i = 1
                for text in texts:
                    canvas.set_hidden(text, True)
                return 2
            else:
                i = 0

        click = canvas.get_new_mouse_clicks()


def one_button_navigate(canvas, click, texts, x1, x2, y1, y2):
    i = 0
    while i != 1:
        if len(click) != 0:

            clicked_button = click[0][0] >= x1 and click[0][0] <= x2 and click[0][1] >= y1 and click[0][
                1] <= y2

            if clicked_button:
                i = 1
                for text in texts:
                    canvas.set_hidden(text, True)
                return True
            else:
                i = 0

        click = canvas.get_new_mouse_clicks()


def add_button(canvas, x, y, a, b, color):
    button = canvas.create_rectangle(x, y, x + a, y + b, color)
    return button


def show_scene(canvas, x, y, size, date_scene):
    chosen_scene = random.choice(date_scene)
    date_scene.remove(chosen_scene)
    title = chosen_scene["title"]
    descriptions = chosen_scene["description"]
    title_text = create_text(canvas, x, y, size + 3, title)
    descriptions_list = []
    y1 = y + size + 3 + 30
    for description in descriptions:
        description_text = create_text(canvas, x, y1, size, description)
        descriptions_list.append(description_text)
        y1 += size + 5
        time.sleep(1)
    time.sleep(1)
    confirm = add_button(canvas, CANVAS_WIDTH / 2 - 150 / 2, CANVAS_WIDTH / 2 + 100, 150, 30, MAIN_BUTTON_COLOR)
    response = create_text(canvas, CANVAS_WIDTH / 2 - 100 / 2 + 15, CANVAS_WIDTH / 2 + 100 + 5, size, "I love it.")
    canvas.wait_for_click()
    click = canvas.get_new_mouse_clicks()
    clicked_love_it = one_button_navigate(canvas, click, descriptions_list, CANVAS_WIDTH / 2 - 150 / 2,
                                          CANVAS_WIDTH / 2 - 150 / 2 + 150, CANVAS_WIDTH / 2 + 100,
                                          CANVAS_WIDTH / 2 + 100 + 30)
    if clicked_love_it:
        canvas.set_hidden(title_text, True)
        canvas.set_hidden(confirm, True)
        canvas.set_hidden(response, True)


def partner_introduction(canvas, x, y, size, partner_profile):
    name = partner_profile["name"] + ":"
    introductions = partner_profile["character_intro"]
    texts = []
    name_text = create_text(canvas, x, y, size + 3, name)
    y += 50
    for introduction in introductions:
        text = create_text(canvas, x, y, size, introduction)
        texts.append(text)
        y += size + 5
        time.sleep(1)
    time.sleep(1)
    confirm = add_button(canvas, CANVAS_WIDTH / 2 - 150 / 2, CANVAS_WIDTH / 2, 150, 30, MAIN_BUTTON_COLOR)
    response = create_text(canvas, CANVAS_WIDTH / 2 - 100 / 2 + 5, CANVAS_WIDTH / 2 + 5, size, "Thank you.")
    canvas.wait_for_click()
    click = canvas.get_new_mouse_clicks()
    clicked_thank_you = one_button_navigate(canvas, click, texts, CANVAS_WIDTH / 2 - 150 / 2,
                                            CANVAS_WIDTH / 2 - 150 / 2 + 150, CANVAS_WIDTH / 2, CANVAS_WIDTH / 2 + 30)
    if clicked_thank_you:
        canvas.set_hidden(confirm, True)
        canvas.set_hidden(response, True)
        canvas.set_hidden(name_text, True)


def the_date(canvas, x, y, size, partner_profile, a, score):
    stage_num = str(a)

    all_stage_questions = partner_profile[stage_num]
    for i in range(5):
        n = str(i + 1)
        questions = all_stage_questions[n]["question"]
        choice_1 = all_stage_questions[n]["choice_1"]
        choice_2 = all_stage_questions[n]["choice_2"]
        choice_3 = all_stage_questions[n]["choice_3"]
        reaction_for_choice_1 = all_stage_questions[n]["reaction_for_choice_1"]
        reaction_for_choice_2 = all_stage_questions[n]["reaction_for_choice_2"]
        reaction_for_choice_3 = all_stage_questions[n]["reaction_for_choice_3"]
        choice_1_score = all_stage_questions[n]["choice_1_score"]
        choice_2_score = all_stage_questions[n]["choice_2_score"]
        choice_3_score = all_stage_questions[n]["choice_3_score"]
        player_chosen_answer_and_score = show_the_question(canvas, x, y, size, questions, choice_1, choice_2, choice_3,
                                                           score, choice_1_score, choice_2_score, choice_3_score)
        early_exit = player_chosen_answer_and_score[2]
        if early_exit == "bad":
            return "bad"
        elif early_exit == "neutral":
            return "neutral"
        else:
            score = player_chosen_answer_and_score[1]
            player_chosen_answer = player_chosen_answer_and_score[0]
            process_player_answer(canvas, x, y, size, player_chosen_answer, reaction_for_choice_1,
                                  reaction_for_choice_2, reaction_for_choice_3)


# Returns player choice and current score
def show_the_question(canvas, x, y, size, questions, choice_1, choice_2, choice_3, score, choice_1_score,
                      choice_2_score, choice_3_score):
    y1 = y
    questions_list = []
    for question in questions:
        q = create_text(canvas, x, y1, size + 1, question)
        questions_list.append(q)
        y1 += size + 5
    time.sleep(3)
    divider = create_text(canvas, x, y1, size, "-----------------------------------------------------")
    player_answer_and_score = show_the_choices(canvas, x, size, choice_1, choice_2, choice_3, score, choice_1_score,
                                               choice_2_score, choice_3_score)
    player_answer = player_answer_and_score[0]
    score = player_answer_and_score[1]
    early_exit = player_answer_and_score[2]
    for question in questions_list:
        canvas.set_hidden(question, True)
    canvas.set_hidden(divider, True)
    return [player_answer, score, early_exit]


# Returns player choice and current score
def show_the_choices(canvas, x, size, choice_1, choice_2, choice_3, score, choice_1_score, choice_2_score,
                     choice_3_score):
    y2 = 145
    instruction_container = add_button(canvas, x, y2, 220, 28, MAIN_BUTTON_COLOR)
    instruction = create_text(canvas, x + 5, y2 + 5, size - 2, "Please click on your answer.")
    time.sleep(1)
    y2 = 180
    choice_1_list = []
    for choice in choice_1:
        c = create_text(canvas, x, y2, size, choice)
        choice_1_list.append(c)
        y2 += size + 5
    time.sleep(2)

    y2 += 20
    choice_2_list = []
    for choice in choice_2:
        c = create_text(canvas, x, y2, size, choice)
        choice_2_list.append(c)
        y2 += size + 5
    time.sleep(2)

    y2 += 20
    choice_3_list = []
    for choice in choice_3:
        c = create_text(canvas, x, y2, size, choice)
        choice_3_list.append(c)
        y2 += size + 5

    canvas.wait_for_click()
    click = canvas.get_new_mouse_clicks()
    answer_and_score = choose_an_answer_option(canvas, x, 180, click, size, choice_1_list, choice_2_list, choice_3_list,
                                               score, choice_1_score, choice_2_score, choice_3_score)
    answer = answer_and_score[0]
    score = answer_and_score[1]
    canvas.set_hidden(instruction, True)
    canvas.set_hidden(instruction_container, True)
    # logic function that takes in the score as parameter
    early_exit = check_if_early_exit(score)

    return [answer, score, early_exit]


def check_if_early_exit(score):
    if score[2] > 20:
        return "bad"
    elif score[1] > 30:
        return "neutral"


# Returns player choice and current score
def choose_an_answer_option(canvas, x, y2, click, size, choice_1_list, choice_2_list, choice_3_list, score,
                            choice_1_score, choice_2_score, choice_3_score):
    position_y_1_1 = y2
    position_y_1_2 = y2 + (2 * (size + 5))
    position_y_2_1 = y2 + (2 * (size + 5)) + 20
    position_y_2_2 = y2 + (4 * (size + 5)) + 20 / 2
    position_y_3_1 = y2 + (4 * (size + 5)) + (2 * 20)
    position_y_3_2 = y2 + (6 * (size + 5)) + (2 * 20)

    i = 0
    while i != 1:
        if len(click) != 0:

            y_position = canvas.get_mouse_y()

            clicked_choice_1 = click[0][0] >= x and click[0][0] <= 270 and click[0][1] >= position_y_1_1 and click[0][
                1] <= position_y_1_2
            clicked_choice_2 = click[0][0] >= x and click[0][0] <= 270 and click[0][1] >= position_y_2_1 and click[0][
                1] <= position_y_2_2
            clicked_choice_3 = click[0][0] >= x and click[0][0] <= 270 and click[0][1] >= position_y_3_1 and click[0][
                1] <= position_y_3_2

            if clicked_choice_1:
                i = 1
                for choice in choice_1_list:
                    canvas.set_hidden(choice, True)
                for choice in choice_2_list:
                    canvas.set_hidden(choice, True)
                for choice in choice_3_list:
                    canvas.set_hidden(choice, True)
                score[0] += choice_1_score
                return [1, score]
            elif clicked_choice_2:
                i = 1
                for choice in choice_1_list:
                    canvas.set_hidden(choice, True)
                for choice in choice_2_list:
                    canvas.set_hidden(choice, True)
                for choice in choice_3_list:
                    canvas.set_hidden(choice, True)
                score[1] += choice_2_score
                return [2, score]
            elif clicked_choice_3:
                i = 1
                for choice in choice_1_list:
                    canvas.set_hidden(choice, True)
                for choice in choice_2_list:
                    canvas.set_hidden(choice, True)
                for choice in choice_3_list:
                    canvas.set_hidden(choice, True)
                score[2] += choice_3_score
                return [3, score]
            else:
                i = 0

        click = canvas.get_new_mouse_clicks()


def process_player_answer(canvas, x, y, size, player_chosen_answer, reaction_for_choice_1, reaction_for_choice_2,
                          reaction_for_choice_3):
    y = y + 80
    reactions = []
    if player_chosen_answer == 1:
        for reaction in reaction_for_choice_1:
            r = create_text(canvas, x, y, size, reaction)
            reactions.append(r)
            y += size + 5
            time.sleep(2)
    elif player_chosen_answer == 2:
        for reaction in reaction_for_choice_2:
            r = create_text(canvas, x, y, size, reaction)
            reactions.append(r)
            y += size + 5
            time.sleep(2)
    elif player_chosen_answer == 3:
        for reaction in reaction_for_choice_3:
            r = create_text(canvas, x, y, size, reaction)
            reactions.append(r)
            y += size + 5
            time.sleep(2)
    time.sleep(1)
    for reaction in reactions:
        canvas.set_hidden(reaction, True)


def show_the_ending(canvas, x, y, size, ending):
    verdicts = ending["verdict"]
    lessons = ending["lesson_for_player"]

    y1 = y
    verdicts_list = []
    for verdict in verdicts:
        v = create_text(canvas, x, y1, size + 1, verdict)
        verdicts_list.append(v)
        y1 += size + 5
        time.sleep(2)
    time.sleep(2)
    for v in verdicts_list:
        canvas.set_hidden(v, True)

    lesson_header = create_text(canvas, x, y, size + 3, "Dr. Love wants to tell you:")
    time.sleep(1)
    lessons_list = []
    y2 = y + size + 3 + 15
    for lesson in lessons:
        l = create_text(canvas, x, y2, size + 1, lesson)
        lessons_list.append(l)
        y2 += size + 5
        time.sleep(2)
    time.sleep(5)


def show_mini_arc(canvas, x, y, size):
    invite = create_text(canvas, x, y + 100, size + 3, "You've unlocked a mini arc.")
    button1 = add_button(canvas, 180, 315, 180, 30, SECONDARY_BUTTON_COLOR)
    take_me_to_mini_arc = create_text(canvas, 185, 320, size, "Take me there →")

    button2 = add_button(canvas, 180, 350, 180, 30, MAIN_BUTTON_COLOR)
    return_to_date = create_text(canvas, 185, 355, size, "← Return to date")
    canvas.wait_for_click()
    click = canvas.get_new_mouse_clicks()
    chosen_button = navigate(canvas, click, [invite, button1, button2, return_to_date, take_me_to_mini_arc])

    if chosen_button == 1:
        return True
    elif chosen_button == 2:
        return False


def play_out_mini_arc(canvas, x, y, size, mini_arcs):
    mini_arc = random.choice(mini_arcs)
    mini_arcs.remove(mini_arc)

    y1 = y
    y2 = y + (2 * (size + 1 + 15))
    title = mini_arc["name"] + " Mini Arc"
    title_text = create_text(canvas, x, y1, size + 1, title)
    time.sleep(1)
    divider = create_text(canvas, x, y1 + size + 1 + 15, size, "-----------------------------------------------------")

    contexts = mini_arc["context"]
    contexts_list = []
    for context in contexts:
        c = create_text(canvas, x, y2, size, context)
        contexts_list.append(c)
        y2 += size + 5
        time.sleep(2)
    time.sleep(1)
    for context in contexts_list:
        canvas.set_hidden(context, True)

    for context in contexts:
        canvas.set_hidden(context, True)
    conversations = mini_arc["conversations"]
    dialogues_list = []
    y3 = y + (2 * (size + 1 + 15))
    for i in range(len(conversations)):
        dialogues = conversations[i]["dialogue"]
        for dialogue in dialogues:
            d = create_text(canvas, x, y3, size, dialogue)
            dialogues_list.append(d)
            y3 += size + 5
            time.sleep(2)
        y3 = y + (2 * (size + 1 + 15))
        time.sleep(2)
        for dialogue in dialogues_list:
            canvas.set_hidden(dialogue, True)

    canvas.set_hidden(title_text, True)
    canvas.set_hidden(divider, True)
    exit_info = ["You did it!", "Mini arc completed.", "Now exiting..."]
    exit_list = []
    y4 = y + 50
    for e in exit_info:
        exit = create_text(canvas, x, y4, size + 3, e)
        exit_list.append(exit)
        y4 += size + 5
        time.sleep(1)
    time.sleep(3)
    for e in exit_list:
        canvas.set_hidden(e, True)
    return

"""
for select partner name
            elif clicked_option_3:
                i = 1
                for option in options:
                    canvas.set_hidden(option, True)
                return names[2]
            elif clicked_option_4:
                i = 1
                for option in options:
                    canvas.set_hidden(option, True)
                return names[3]
            elif clicked_option_5:
                i = 1
                for option in options:
                    canvas.set_hidden(option, True)
                return names[4]
            elif clicked_option_6:
                i = 1
                for option in options:
                    canvas.set_hidden(option, True)
                return names[5]
            """


if __name__ == '__main__':
    main()