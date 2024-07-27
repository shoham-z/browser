HSTEP, VSTEP = 13, 18
WIDTH, HEIGHT = 800, 600


def update_WIDTH(w):
    global WIDTH
    WIDTH = w


def update_HEIGHT(h):
    global HEIGHT
    HEIGHT = h


def lex(body):
    text = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
        elif c == ">":
            in_tag = False
        elif not in_tag:
            text += c

    return text


def layout(text):
    display_list = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
        display_list.append((cursor_x, cursor_y, c))

        cursor_x += HSTEP

        # make sure text doesn't flow off right side
        if cursor_x >= WIDTH - HSTEP:
            cursor_y += VSTEP
            cursor_x = HSTEP
    return display_list
