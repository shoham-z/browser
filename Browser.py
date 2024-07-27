import tkinter

from funcs import lex, WIDTH, HEIGHT, VSTEP, HSTEP, layout, update_WIDTH, update_HEIGHT

SCROLL_STEP = 100


class Browser:
    def __init__(self):
        self.text = None
        self.display_list = None
        self.window = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.window,
            width=WIDTH,
            height=HEIGHT
        )
        self.canvas.pack(fill=tkinter.BOTH, expand=1)
        self.scroll = 0

        self.window.bind("<Down>", self.scrolldown)
        self.window.bind("<Up>", self.scrollup)
        self.window.bind("<MouseWheel>", self.mouse_wheel)
        self.window.bind("<Configure>", self.resize)

    # ===================== DRAW TO WINDOW SECTION =====================

    def load(self, url):
        body = url.request()
        self.text = lex(body)
        self.render()

    def render(self, ):
        self.display_list = layout(self.text)
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            if y > self.scroll + HEIGHT:
                continue
            if y + VSTEP < self.scroll:
                continue
            self.canvas.create_text(x, y - self.scroll, text=c)

    # ===================== END - DRAW TO WINDOW SECTION =====================

    # ===================== HANDLE EVENT SECTION =====================
    def resize(self, e):
        update_WIDTH(e.width)
        update_HEIGHT(e.height)
        self.render()
        print("========================================================")
        print("new width = " + str(e.width))
        print("old width = " + str(WIDTH))
        print("new height = " + str(e.height))
        print("old height = " + str(HEIGHT))
        print("========================================================\n\n")

    def scrolldown(self, e):
        self.scroll += SCROLL_STEP
        self.draw()

    def scrollup(self, e):
        self.scroll -= SCROLL_STEP
        if self.scroll < 0:
            self.scroll = 0
        self.draw()

    def mouse_wheel(self, e):
        if e.num == 5 or e.delta == -120:
            self.scrolldown(e)
        if e.num == 4 or e.delta == 120:
            self.scrollup(e)

    # ===================== END - HANDLE EVENT SECTION =====================
