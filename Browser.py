import tkinter
import tkinter.font

from HTMLParser import HTMLParser
from Text import Text
from Element import Element
from Layout import Layout, VSTEP, WIDTH, HEIGHT, update_WIDTH, update_HEIGHT

SCROLL_STEP = 100


def lex(body):
    # parse the web page

    out = []
    buffer = ""
    in_tag = False
    for c in body:
        if c == "<":
            in_tag = True
            if buffer:
                out.append(Text(buffer))
            buffer = ""
        elif c == ">":
            in_tag = False
            out.append(Element(buffer))
            buffer = ""
        else:
            buffer += c
    if not in_tag and buffer:
        out.append(Text(buffer))
    return out


class Browser:
    def __init__(self):
        self.display_list = None
        self.nodes = None
        self.scroll = 0

        self.window = tkinter.Tk()

        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack(fill=tkinter.BOTH, expand=True)

        # define keybinds
        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<MouseWheel>", self.mouse_wheel)
        self.window.bind("<Configure>", self.resizewindow)

        # define font
        self.bi_times = tkinter.font.Font(
            family="Times",
            size=16,
            weight="bold",
            slant="italic",
        )

    # ===================== DRAW TO WINDOW SECTION =====================
    def draw(self):
        self.canvas.delete("all")
        for x, y, c, f in self.display_list:
            if y > self.scroll + HEIGHT:
                continue
            if y + VSTEP < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=c, font=f, anchor='nw')

    def load(self, url):
        # get response from server and get the text
        body = url.request()
        self.nodes = HTMLParser(body).parse()

        self.render()

    def render(self):
        self.display_list = Layout(self.nodes).display_list
        self.draw()
    # ===================== END - DRAW TO WINDOW SECTION =====================

    # ===================== HANDLE EVENT SECTION =====================
    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        self.draw()

    def scrollup(self, e):
        self.scroll -= SCROLL_STEP
        if self.scroll < 0:
            self.scroll = 0
        self.draw()

    def resizewindow(self, e):
        global WIDTH, HEIGHT
        if WIDTH == e.width and HEIGHT == e.height:
            return
        update_WIDTH(e.width)
        update_HEIGHT(e.height)
        self.render()

    def mouse_wheel(self, e):
        if e.num == 5 or e.delta == -120:
            self.scrolldown(e)
        if e.num == 4 or e.delta == 120:
            self.scrollup(e)
    # ===================== END - HANDLE EVENT SECTION =====================
