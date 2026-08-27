#!/usr/bin/env python3
"""Build the roadmap deck.

    slides.html  +  talk-track.md  +  fonts.css  ->  Anomalo-Roadmap.html

Run `python3 build.py` after editing either source. No dependencies.
"""
import re
import sys
import html
from pathlib import Path

HERE = Path(__file__).parent
SLIDES = HERE / "slides.html"
TRACK = HERE / "talk-track.md"
FONTS = HERE / "fonts.css"
OUT = HERE / "Anomalo-Roadmap.html"

HEAD = re.compile(r"^##\s+(\d+)\s+.\s+(.*?)\s+.\s+(\d+:\d{2})\s*$")


def parse_track(text):
    """-> {slide_number: (duration, [spoken], [cues])}, in file order."""
    slides, cur = {}, None
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block:
            continue
        first = block.splitlines()[0]
        m = HEAD.match(first)
        if m:
            cur = int(m.group(1))
            if cur in slides:
                sys.exit("talk-track.md: slide %d appears twice" % cur)
            slides[cur] = (m.group(3), [], [])
            continue
        if cur is None:
            continue  # preamble above the first heading
        one = " ".join(l.strip() for l in block.splitlines())
        if one.startswith(">"):
            slides[cur][2].append(one.lstrip("> ").strip())
        else:
            slides[cur][1].append(one)  # "!" prefix is handled at render time
    return slides


def esc(t):
    """Markdown paragraph -> HTML. **bold** and *italic* survive; the rest is literal."""
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\*\w])\*([^*]+?)\*(?![\*\w])", r"<em>\1</em>", t)
    return t


def main():
    slides_html = SLIDES.read_text(encoding="utf-8")
    track = parse_track(TRACK.read_text(encoding="utf-8"))

    n_slides = slides_html.count('<section class="slide')
    missing = [i for i in range(1, n_slides + 1) if i not in track]
    extra = [i for i in track if i > n_slides]
    if missing or extra:
        sys.exit("talk-track.md is out of sync with slides.html%s%s" % (
            "\n  no script for slide(s): %s" % missing if missing else "",
            "\n  script for nonexistent slide(s): %s" % extra if extra else ""))

    blocks = []
    for i in range(1, n_slides + 1):
        dur, say, cue = track[i]
        parts = ['<b data-dur="%s"></b>' % dur]
        parts += ['<p class="%s">%s</p>' % ("demo" if p.startswith("!") else "say",
                                             esc(p.lstrip("! ")))
                  for p in say]
        if cue:
            parts.append('<p class="cuehd">Watch for</p>')
            parts += ['<p class="cue">%s</p>' % esc(c) for c in cue]
        blocks.append('<section data-n="%d">%s</section>' % (i, "".join(parts)))
    store = '<div id="script-src" hidden>%s</div>\n\n' % "".join(blocks)

    out = re.sub(r'<div id="script-src" hidden>[\s\S]*?</div>\n\n', "", slides_html)
    out = out.replace('<div class="zone l"', store + '<div class="zone l"', 1)

    # The page ships without a charset declaration of its own, so escape every
    # non-ASCII character outside <script> as a numeric entity. Inside <script>
    # entities would not be decoded, so that block must already be ASCII.
    script = re.search(r"<script>[\s\S]*?</script>", out)
    if script:
        bad = sorted(set(c for c in script.group(0) if ord(c) > 127))
        if bad:
            sys.exit("non-ASCII inside <script>, use \\uXXXX escapes: %s" % bad)
        token = "@@SCRIPT@@"
        out = out.replace(script.group(0), token)
    out = "".join(c if ord(c) < 128 else "&#%d;" % ord(c) for c in out)
    if script:
        out = out.replace(token, script.group(0))

    out = out.replace("/*__FONTS__*/", FONTS.read_text(encoding="utf-8"), 1)
    OUT.write_text(out, encoding="utf-8")

    def secs(d):
        m, s = d.split(":")
        return int(m) * 60 + int(s)

    main_total = sum(secs(track[i][0]) for i in range(1, min(16, n_slides + 1)))
    apx = n_slides - 15
    print("%s  %d KB" % (OUT.name, len(out) / 1024))
    print("main deck: 15 slides, %d min %02d sec   (+%d appendix)"
          % (main_total // 60, main_total % 60, apx))


if __name__ == "__main__":
    main()
