"""Find every container whose direct children include 2+ button-like links/buttons."""
import re, sys, glob
from html.parser import HTMLParser

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr", "path", "line", "polyline", "circle", "rect", "polygon", "ellipse", "stop", "use"}


def is_button(tag, attrs, styles):
    if tag not in ("a", "button"):
        return False
    st = attrs.get("style", "") or ""
    cls = attrs.get("class", "") or ""
    st = st + ";" + styles.get(cls, "")
    if re.search(r"(btn|cta)", cls, re.I):
        return True
    has_pad = re.search(r"padding:\s*\d", st) is not None
    boxed = re.search(r"background:\s*#|border:\s*1", st) is not None
    upper = "uppercase" in st
    return has_pad and boxed and upper


class P(HTMLParser):
    def __init__(self, src):
        super().__init__(convert_charrefs=False)
        self.src = src
        self.lines = [0]
        for m in re.finditer("\n", src):
            self.lines.append(m.end())
        self.stack = []
        self.found = []
        self.skip = 0

    def off(self):
        l, c = self.getpos()
        return self.lines[l - 1] + c

    def handle_starttag(self, tag, attrs):
        if tag in ("style", "script"):
            self.skip += 1
        a = dict(attrs)
        node = dict(tag=tag, attrs=a, start=self.off(), kids=[])
        if self.stack:
            self.stack[-1]["kids"].append(node)
        if tag in VOID:
            return
        self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        node = dict(tag=tag, attrs=dict(attrs), start=self.off(), kids=[])
        if self.stack:
            self.stack[-1]["kids"].append(node)

    def handle_endtag(self, tag):
        if tag in ("style", "script"):
            self.skip = max(0, self.skip - 1)
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                node = self.stack[i]
                del self.stack[i:]
                btns = [k for k in node["kids"] if is_button(k["tag"], k["attrs"], {})]
                if len(btns) >= 2:
                    self.found.append((node, btns))
                return


def text_of(src, start):
    m = re.search(r">(.*?)</(a|button)>", src[start:start + 3000], re.S)
    t = re.sub(r"<[^>]+>|\{\{[^}]*\}\}", " ", m.group(1)) if m else ""
    return " ".join(t.split())[:40]


if __name__ == "__main__":
    for f in sys.argv[1:]:
        src = open(f, encoding="utf-8").read()
        p = P(src)
        p.feed(src)
        for node, btns in p.found:
            line = src.count("\n", 0, node["start"]) + 1
            print(f"{f}:{line} <{node['tag']} class='{node['attrs'].get('class','')}'> -> " + " | ".join(text_of(src, b["start"]) for b in btns))
