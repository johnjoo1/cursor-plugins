#!/usr/bin/env python3
"""Screenshot every slide and flag layout problems.

    pip install playwright && playwright install chromium
    python3 qa.py                 # -> shots/s01.png ... plus an audit report

Set CHROME_PATH to use a browser you already have instead of a downloaded one.
"""
import os
import sys
from playwright.sync_api import sync_playwright

DECK = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "Anomalo-Roadmap.html")
OUT = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else "shots")

AUDIT = """() => {
  const sl = document.querySelector('.slide.on');
  const sr = sl.getBoundingClientRect();
  const bad = [];
  if (sl.scrollHeight > sl.clientHeight + 1)
    bad.push({k: 'SLIDE-SCROLL', d: sl.scrollHeight - sl.clientHeight, t: ''});
  if (sl.scrollWidth > sl.clientWidth + 1)
    bad.push({k: 'SLIDE-WIDE', d: sl.scrollWidth - sl.clientWidth, t: ''});
  sl.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) return;
    const txt = (el.textContent || '').trim().slice(0, 60);
    if (el.scrollHeight > el.clientHeight + 2 && getComputedStyle(el).overflow !== 'visible')
      bad.push({k: 'CLIPPED', d: el.scrollHeight - el.clientHeight, t: txt});
    if (r.bottom > sr.bottom - 6 || r.top < sr.top - 1 ||
        r.left < sr.left - 1 || r.right > sr.right + 1) {
      if (!el.closest('.foot'))
        bad.push({k: 'ESCAPES', d: Math.round(Math.max(
          r.bottom - (sr.bottom - 6), sr.top - r.top,
          sr.left - r.left, r.right - sr.right)), t: txt});
    }
  });
  return bad;
}"""


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith(".png"):
            os.remove(os.path.join(OUT, f))

    launch = {"args": ["--force-color-profile=srgb", "--font-render-hinting=none"]}
    if os.environ.get("CHROME_PATH"):
        launch["executable_path"] = os.environ["CHROME_PATH"]

    report = []
    with sync_playwright() as p:
        b = p.chromium.launch(**launch)
        pg = b.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=1.5)
        pg.goto("file://" + DECK)
        pg.wait_for_timeout(1500)
        pg.evaluate("try{localStorage.clear()}catch(e){}")
        n = pg.evaluate("document.querySelectorAll('.slide').length")
        print("slides:", n)

        for i in range(n):
            pg.evaluate("""(i) => {
              [...document.querySelectorAll('.slide')]
                .forEach((el, k) => el.classList.toggle('on', k === i));
              document.getElementById('notes').classList.remove('up');
            }""", i)
            pg.wait_for_timeout(120)
            pg.screenshot(path=os.path.join(OUT, "s%02d.png" % (i + 1)))
            seen = set()
            for r in pg.evaluate(AUDIT):
                key = (r["k"], r["t"])
                if key not in seen:
                    seen.add(key)
                    report.append((i + 1, r["k"], round(r["d"]), r["t"]))
        b.close()

    print("\n=== LAYOUT AUDIT ===")
    if not report:
        print("clean")
    for r in report:
        print("slide %-3d %-13s %-6s %s" % r)
    return 1 if report else 0


if __name__ == "__main__":
    sys.exit(main())
