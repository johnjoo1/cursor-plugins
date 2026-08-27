"""Fetch latin-subset woff2 for the deck's faces and emit an inline @font-face block."""
import re, base64, urllib.request, sys

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/120.0.0.0 Safari/537.36")

FAMILIES = [
    ("Archivo", "wght@600;700"),
    ("IBM+Plex+Sans", "ital,wght@0,400;0,500;0,600;1,400"),
    ("IBM+Plex+Mono", "wght@400;500;600"),
]

# keep only the plain-latin subset (no accents/vietnamese/cyrillic/greek)
LATIN = "U+0000-00FF"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=60).read()


out = []
total = 0
for fam, axis in FAMILIES:
    url = "https://fonts.googleapis.com/css2?family=%s:%s&display=swap" % (fam, axis)
    css = get(url).decode("utf-8")
    blocks = re.findall(r"@font-face\s*\{[^}]*\}", css)
    for b in blocks:
        if LATIN not in b:
            continue
        family = re.search(r"font-family:\s*'([^']+)'", b).group(1)
        style = re.search(r"font-style:\s*(\w+)", b).group(1)
        weight = re.search(r"font-weight:\s*(\d+)", b).group(1)
        src = re.search(r"url\((https://[^)]+\.woff2)\)", b)
        if not src:
            continue
        data = get(src.group(1))
        total += len(data)
        b64 = base64.b64encode(data).decode("ascii")
        out.append(
            "@font-face{font-family:'%s';font-style:%s;font-weight:%s;font-display:swap;"
            "src:url(data:font/woff2;base64,%s) format('woff2');}"
            % (family, style, weight, b64))
        print("  %-16s %-7s %-4s %6.1f KB" % (family, style, weight, len(data) / 1024),
              file=sys.stderr)

print("TOTAL raw %.1f KB / base64 ~%.1f KB" % (total / 1024, total * 1.34 / 1024), file=sys.stderr)
open("fonts.css", "w").write("\n".join(out))
