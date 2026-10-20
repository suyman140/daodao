"""Create the original vector bouquet and cheerful instrumental, using Python only."""
from pathlib import Path
from array import array
import math
import random
import wave

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)


def make_bouquet():
    parts = ['''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 660" fill="none">
<defs>
  <linearGradient id="paper" x1="140" y1="330" x2="430" y2="630" gradientUnits="userSpaceOnUse"><stop stop-color="#f5cdb2"/><stop offset="1" stop-color="#e8a781"/></linearGradient>
  <linearGradient id="back" x1="100" y1="300" x2="440" y2="600" gradientUnits="userSpaceOnUse"><stop stop-color="#ffeed8"/><stop offset="1" stop-color="#f4d5ae"/></linearGradient>
  <linearGradient id="leaf"><stop stop-color="#88a478"/><stop offset="1" stop-color="#3e684c"/></linearGradient>
  <radialGradient id="sunflower"><stop stop-color="#e59b29"/><stop offset="1" stop-color="#f6cc46"/></radialGradient>
  <radialGradient id="rose"><stop stop-color="#a63f3d"/><stop offset=".55" stop-color="#d95f53"/><stop offset="1" stop-color="#ee8c77"/></radialGradient>
  <radialGradient id="pink"><stop stop-color="#c25465"/><stop offset="1" stop-color="#ed9c9d"/></radialGradient>
  <radialGradient id="purple"><stop stop-color="#82639d"/><stop offset="1" stop-color="#b8a0cb"/></radialGradient>
  <radialGradient id="heart"><stop stop-color="#745338"/><stop offset="1" stop-color="#4c3a2c"/></radialGradient>
</defs>
<path d="M92 304 181 261 295 366 429 246 522 313 436 541 318 642 190 550Z" fill="url(#back)"/>
<path d="m92 304 203 62-105 184Z" fill="#f7e2c3"/>
<path d="m522 313-227 53 141 175Z" fill="#efd1aa"/>
''']

    def leaf(x, y, scale=1, rotation=0, color="url(#leaf)"):
        parts.append(f'<g transform="translate({x} {y}) rotate({rotation}) scale({scale})"><path d="M0 0C-46-5-66-35-61-64-27-62-2-31 0 0Z" fill="{color}"/><path d="M-2-3-50-53" stroke="#e4e9c8" stroke-opacity=".32" stroke-width="1.3"/></g>')

    # Curved stems and tall eucalyptus branches.
    stems = [(160, 140), (218, 116), (307, 177), (395, 119), (445, 206), (166, 255), (242, 290), (370, 306), (457, 308), (129, 310)]
    for x, y in stems:
        parts.append(f'<path d="M310 558Q{(x+310)/2-30} 345 {x} {y}" stroke="#557d51" stroke-width="6" stroke-linecap="round"/>')
    for x, y, rot in [(160, 185, -27), (397, 201, 38), (466, 283, 48), (132, 294, -55)]:
        parts.append(f'<g transform="translate({x} {y}) rotate({rot})"><path d="M0 80Q-8-38 3-119" stroke="#5e825c" stroke-width="3"/>')
        for j in range(5):
            yy = -100 + j * 31
            parts.append(f'<ellipse cx="{-14 if j%2 else 16}" cy="{yy}" rx="19" ry="12" transform="rotate({-30 if j%2 else 30} {-14 if j%2 else 16} {yy})" fill="{["#93ac83", "#77956b", "#a2b591"][j%3]}"/>')
        parts.append('</g>')
    for args in [(205, 299, 1.2, -25), (220, 225, .9, 25), (410, 329, 1.25, 105), (146, 347, .8, -35), (376, 198, .85, 95), (295, 366, .9, -5), (453, 351, .9, 125), (244, 124, .7, -25)]:
        leaf(*args)

    # Baby's-breath sprigs give the arrangement a light, irregular silhouette.
    for x, y in [(205, 64), (301, 84), (459, 140), (107, 225), (486, 255), (199, 338)]:
        parts.append(f'<path d="M{x+10} {y+90}Q{x+5} {y+40} {x} {y}" stroke="#89a078" stroke-width="2"/>')
        for dx, dy in [(-14, 6), (9, 17), (-3, 35), (23, 36), (-20, 44)]:
            parts.append(f'<path d="M{x+4} {y+55} {x+dx} {y+dy}" stroke="#89a078" stroke-width="1.5"/><circle cx="{x+dx}" cy="{y+dy}" r="6" fill="#fff8de"/><circle cx="{x+dx+2}" cy="{y+dy-2}" r="3" fill="#fffdf2"/>')

    def flower(x, y, radius, kind, rotate=0):
        parts.append(f'<g transform="translate({x} {y}) rotate({rotate})">')
        if kind == "sun":
            for layer, count, length, width, cy, color in [(0, 16, radius*.62, radius*.18, -radius*.56, "#efb631"), (1, 16, radius*.61, radius*.17, -radius*.55, "url(#sunflower)")]:
                for i in range(count):
                    angle = i*360/count + layer*11
                    parts.append(f'<ellipse cx="0" cy="{cy}" rx="{width}" ry="{length}" transform="rotate({angle})" fill="{color}"/>')
            parts.append(f'<circle r="{radius*.45}" fill="url(#heart)"/>')
            for i in range(55):
                a = i*2.39996
                r = math.sqrt(i/55)*radius*.39
                parts.append(f'<circle cx="{math.cos(a)*r:.2f}" cy="{math.sin(a)*r:.2f}" r="1.6" fill="{["#b18a4c", "#9b783e", "#c7a258"][i%3]}"/>')
        elif kind in ("rose", "pink"):
            colors = ["#e68272", "#e8968e", "#d86962", "#bd5150"] if kind == "rose" else ["#eeafb0", "#e58f9b", "#da7c8c", "#c15f77"]
            for layer, count in enumerate([9, 8, 6, 4]):
                size = radius*(1-layer*.22)
                for i in range(count):
                    parts.append(f'<ellipse cx="0" cy="{-size*.29}" rx="{size*.42}" ry="{size*.69}" transform="rotate({i*360/count+layer*23})" fill="{colors[layer]}" stroke="#fff1df" stroke-opacity=".19" stroke-width="1.5"/>')
            parts.append(f'<path d="M-8 3Q-10-12 5-10T11 4Q0-6-5 5T8 12" stroke="#994c4b" stroke-width="3" stroke-linecap="round"/>')
        elif kind == "daisy":
            for i in range(13):
                parts.append(f'<ellipse cx="0" cy="{-radius*.51}" rx="{radius*.21}" ry="{radius*.57}" transform="rotate({i*360/13})" fill="{["#fffdf0", "#f5e9c9", "#fffae8"][i%3]}" stroke="#eadbb9" stroke-width=".7"/>')
            parts.append(f'<circle r="{radius*.29}" fill="#e9b743"/>')
            for i in range(16):
                a=i*2.4; r=math.sqrt(i/16)*radius*.22
                parts.append(f'<circle cx="{math.cos(a)*r:.2f}" cy="{math.sin(a)*r:.2f}" r="1.1" fill="#bd8b2c"/>')
        elif kind == "purple":
            for i in range(8):
                parts.append(f'<path d="M0 3C-28-8-34-33-17-44Q-9-51 0-43 12-51 20-38C30-21 17-5 0 3Z" transform="rotate({i*45}) scale({radius/47})" fill="{["#b49bc9", "#ad8dc0", "#c2a9d4", "#9c7bb5"][i%4]}"/>')
            parts.append(f'<circle r="{radius*.2}" fill="#f1cc6f"/><circle r="{radius*.09}" fill="#c49138"/>')
        parts.append('</g>')

    flower(218, 131, 55, "rose", -12)
    flower(390, 117, 49, "pink", 18)
    flower(305, 205, 69, "sun", -7)
    flower(146, 239, 49, "purple", 10)
    flower(444, 223, 49, "daisy", 13)
    flower(230, 285, 41, "daisy", -4)
    flower(378, 303, 50, "rose", 15)
    flower(472, 311, 31, "pink", -8)
    flower(136, 325, 30, "sun", 8)
    flower(302, 323, 28, "purple", 18)
    leaf(190, 371, 1, -30)
    leaf(425, 382, 1.1, 100)
    parts.append('''<path d="m111 354 189 68 192-78-67 203-109 91-105-85Z" fill="url(#paper)"/>
<path d="m111 354 189 68 16 216-105-85Z" fill="#f3c4a8"/>
<path d="m300 422 192-78-160 202-16 92Z" fill="#efb996"/>
<path d="m111 354 205 284-16-216Z" fill="#f7d4ba" fill-opacity=".6"/>
<path d="m492 344-160 202 93 1Z" fill="#dfa078" fill-opacity=".35"/>
<path d="m210 416 68 165m92-150-37 144" stroke="#dba080" stroke-width="1.5" stroke-opacity=".6"/>
<path d="M247 538Q309 523 376 539L365 557Q305 546 252 556Z" fill="#c95447"/>
<path d="M311 543C257 490 206 506 230 539c16 18 56 14 81 4Z" fill="#e16d5a" stroke="#bf4b42" stroke-width="2"/>
<path d="M315 543C363 490 411 509 390 536c-16 19-47 17-75 7Z" fill="#e67c65" stroke="#bf4b42" stroke-width="2"/>
<path d="M309 546c-28 18-48 48-57 79l32-12 16 14c-5-31 4-53 17-75Z" fill="#d96150"/>
<path d="M318 547c22 13 38 30 53 57l-29-7-10 19c-1-32-11-51-24-66Z" fill="#c95145"/>
<ellipse cx="313" cy="546" rx="14" ry="12" transform="rotate(-9 313 546)" fill="#e68167"/>
<path d="M235 524q34-7 65 17m27-2q35-21 57-15" stroke="#f6ab8d" stroke-width="2" stroke-linecap="round"/>
<path d="M406 417q-8 25-24 37" stroke="#ab7555" stroke-width="1.5"/>
<rect x="369" y="445" width="58" height="41" rx="2" transform="rotate(13 369 445)" fill="#fff1d8"/>
<circle cx="395" cy="466" r="7" stroke="#d9835e" stroke-width="1"/>
<path d="M395 453v3m0 20v3m-13-13h3m20 0h3m-22-9 2 2m14 14 2 2m-18 0 2-2m14-14 2-2" stroke="#d9835e" stroke-width="1.2"/>
</svg>''')
    (ASSETS / "bouquet.svg").write_text("\n".join(parts), encoding="utf-8")


def make_music():
    # An original, 16-bar, 112 BPM marimba / plucked-string instrumental.
    # Exact bar boundaries and overlapping tails make the WAV loop seamless.
    rate = 22050
    beat = 60 / 112
    bars = 16
    duration = bars * 4 * beat
    samples = array("f", [0.0]) * round(duration * rate)

    def note(midi, start_beat, length_beats, amplitude, instrument="pluck"):
        if midi is None:
            return
        freq = 440 * 2 ** ((midi - 69) / 12)
        start = round(start_beat * beat * rate)
        length = length_beats * beat
        total = round((length + .16) * rate)
        for j in range(total):
            t = j / rate
            envelope = min(1, t / .006) * math.exp(-t * (4.6 if instrument == "bell" else 6.5))
            envelope *= min(1, max(0, (length + .16 - t) / .09))
            phase = 2 * math.pi * freq * t
            if instrument == "bass":
                value = math.sin(phase) + .16 * math.sin(phase * 2)
                envelope = min(1, t / .015) * math.exp(-t * 3.3) * min(1, max(0, (length + .16 - t) / .12))
            elif instrument == "bell":
                value = math.sin(phase) + .22 * math.sin(phase * 2.01) * math.exp(-t * 5) + .12 * math.sin(phase * 4.02) * math.exp(-t * 12)
            else:
                value = math.sin(phase) + .30 * math.sin(phase * 2) + .12 * math.sin(phase * 3) + .055 * math.sin(phase * 4)
            samples[(start + j) % len(samples)] += value * envelope * amplitude

    chords = [(60, 64, 67, 48), (67, 71, 74, 43), (69, 72, 76, 45), (65, 69, 72, 41)]
    melody = [
        [(76, 0, .5), (79, .75, .5), (81, 1.5, .5), (79, 2.25, .5), (76, 3, .75)],
        [(74, 0, .5), (76, .75, .5), (79, 1.5, .75), (74, 2.5, .5), (71, 3.25, .5)],
        [(72, 0, .5), (76, .75, .5), (81, 1.5, .75), (79, 2.5, .5), (76, 3.25, .5)],
        [(77, 0, .75), (76, 1, .5), (74, 1.75, .5), (72, 2.5, 1)],
        [(76, 0, .5), (79, .5, .5), (84, 1.5, .75), (81, 2.5, .5), (79, 3.25, .5)],
        [(74, 0, .5), (79, .75, .75), (83, 1.75, .5), (81, 2.5, .5), (79, 3.25, .5)],
        [(81, 0, .5), (79, .75, .5), (76, 1.5, .5), (72, 2.25, .75), (76, 3.25, .5)],
        [(77, 0, .75), (74, 1, .5), (72, 2, 1.5)],
    ]
    rng = random.Random(2010)
    for bar in range(bars):
        chord = chords[bar % 4]
        for b in range(4):
            note(chord[3] + (7 if b % 2 else 0), bar * 4 + b, .5, .105, "bass")
            for k, pitch in enumerate(chord[:3]):
                note(pitch, bar * 4 + b + .47 + k*.022, .35, .055)
        for pitch, offset, length in melody[bar % 8]:
            note(pitch, bar * 4 + offset, length, .13 if bar < 8 else .145, "bell")
        if bar >= 8:
            for b in [0.5, 1.5, 2.5, 3.5]:
                note(chord[0]+12, bar*4+b, .2, .028, "bell")
        # Soft shaker, no external samples.
        for half in range(8):
            start = round((bar*4 + half*.5) * beat * rate)
            for j in range(round(.055 * rate)):
                samples[(start+j) % len(samples)] += rng.uniform(-1, 1) * .014 * math.exp(-j / (rate * .012))
    peak = max(abs(s) for s in samples)
    pcm = array("h", [round(math.tanh(s / peak * 1.1) * 26000) for s in samples])
    target = ASSETS / "audio" / "mot-chut-nang.wav"
    target.parent.mkdir(exist_ok=True)
    with wave.open(str(target), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes(pcm.tobytes())
    print(f"Original instrumental: {duration:.1f}s, {target.stat().st_size:,} bytes")


if __name__ == "__main__":
    make_bouquet()
    make_music()
    print("Original bouquet and music generated.")
