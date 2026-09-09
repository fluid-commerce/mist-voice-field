---
name: Mist keynote TikTok
colors:
  bg: "#07060b"
  ink: "#f4f1fa"
  ink_dim: "#9a93a8"
  accent: "#ff6fd8"
  accent_2: "#a855f7"
  accent_3: "#6366f1"
  panel: "rgba(10,9,16,0.72)"
  panel_border: "#23202e"
typography:
  display: { family: Montserrat, weights: [800, 900], tracking: "-0.02em" }
  body: { family: Montserrat, weights: [500], size: "34-44px", line_height: 1.15 }
  mono: { family: JetBrains Mono, weights: [400, 700], size: "22-28px", tracking: "0.18em", case: upper }
spacing:
  frame: 1080x1920
  safe: { sides: 90, top: 220, bottom: 300 }
components:
  panel: { fill: "rgba(10,9,16,0.72)", border: "2px solid #23202e", radius: 18 }
  stat: { number: "Montserrat 900 150px", label: "JetBrains Mono 24px upper" }
---

# frame.md — Mist keynote TikTok

Concept angle: a filmed minute of the keynote, cut with taste. The wall is the star; the type is the
narrator. Everything on screen is either the room or the words.

## Palette

- bg: #07060b (near-black, violet-tinted; matches the wall's black)
- ink: #f4f1fa (warm white; the M is pure white, type sits just under it)
- ink-dim: #9a93a8
- accent: #ff6fd8 (pink; the ring's high end)
- accent-2: #a855f7 (violet; the ring's low end)
- accent-3: #6366f1 (indigo; deep end, used sparingly)
- panel: rgba(10,9,16,0.72) with a 2px #23202e border

## Type

- Display: Montserrat 800 / 900 (embedded). Headlines 72–120px in the vertical frame, tight tracking (-0.02em).
- Labels / metadata: JetBrains Mono 400 / 700 (embedded), 22–28px, letter-spacing 0.18em, uppercase.
- Body / captions: Montserrat 500, 34–44px, line-height 1.15.
- One expressive face per scene (Montserrat), mono recedes.

## Layout feel

- 1080x1920. Safe area: 90px sides, 220px top, 300px bottom (TikTok UI).
- Footage is full-bleed and slightly graded darker at the edges (radial vignette) so type reads.
- Type anchors to the lower third or the upper third, never dead center over the M.
- Stats are big numbers in Montserrat 900 with a mono label under them, left-aligned in a stack.
- Panels are dark glass, not white cards.

## Motion feel

- Grid-locked world on the wall; the type moves with weight: 0.4–0.7s, power3/expo eases, small
  overshoot on payoffs only. Words swap by hard cut or type-on; nothing floats.
- Slow push-ins on footage (1.00 → 1.06 over the clip) to keep held shots alive.

## Don'ts

- No gradient text. No neon glow on type. No stock icons. No white flashes.
- Never cover the M with a panel.
