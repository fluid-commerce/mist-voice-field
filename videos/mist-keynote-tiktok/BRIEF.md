---
workflow: general-video
flow: automation
storyboard: yes
message: "Mist answers your business question in real time, live on the wall"
destination: tiktok
aspect: 1080x1920
language: en
audience: Fluid customers and prospects scrolling TikTok; ecommerce operators
length: 60s
angle: event-recap
voice: none
---

## Intent

A well-produced 60-second vertical TikTok from the Mist keynote. The presenter is on stage
asking Mist a real business question; the LED wall behind him listens, thinks, and answers
with live stats. It should feel like someone filmed the best minute of the event and cut it
with taste: music bed, on-screen captions carrying the words, no voiceover. The wall's
visual language (white pixel M, pink-violet ring, glossy black stage with reflections) is
the star; the presenter and room make it real.

## Assets

- ../../stage.html (served at http://localhost:5231/stage.html) — the live three.js keynote stage; footage is recorded from it (wide, presenter, screen-only, reflection-low angles).
- ../../index.html (http://localhost:5231/index.html) — the flat 2D visualizer; can be recorded full-frame for clean inserts of the wall (?embed=1 hides UI; state/layout via keys or URL).
- Palette: white core, blush → pink → violet → indigo (index.html STOPS), near-black background.

## Customizations

- No music for now (confirmed 2026-09-09). No narration. Captions carry the presenter's words as designed type.
- Plan approved on the board 2026-09-09; sketch pass skipped, straight to build.
- Rendered 2026-09-09: out/mist-keynote-tiktok.mp4 (master) and out/mist-keynote-tiktok-web.mp4 (upload copy). Stats are placeholders pending real numbers.
- The wall must visibly move through listening → thinking → answering, with the answer cards (query steps + summary) readable in the vertical frame.
- Stats shown on the wall should be plausible ecommerce numbers, presented as Mist's answer.

## Notes

- Storyboard reviewed and approved; building scene by scene with the board as progress surface.
- Presenter body is a placeholder avatar; shoot him small or in silhouette when possible.
- Footage is recorded from the live scene via headless Chrome; the stage runs realtime, so record clips, then place them as video.
