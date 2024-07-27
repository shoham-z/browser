import tkinter
from Browser import Browser
from HTMLParser import HTMLParser, print_tree
from URL import URL

if __name__ == "__main__":
    import sys

    body = URL(sys.argv[1]).request()
    Browser().load(URL(sys.argv[1]))
    tkinter.mainloop()
