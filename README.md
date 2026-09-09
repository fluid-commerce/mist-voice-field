# Mist voice field

Voice-reactive pixel visualizer for Fluid's **Mist** presentation mode, plus a Three.js keynote stage to preview it on an LED wall. Everything is static HTML: serve the folder and open a page.

```bash
python3 -m http.server 5231
```

## Pages

| Page | What it is |
| --- | --- |
| `index.html` | The visualizer. Grid-locked pixel M (from the interactive logo), halo ring, board, states, layouts, looks. |
| `stage.html` | Three.js stage: LED wall showing `index.html`, presenter, audience, glossy reflective stage. State machine panel at the top. `?src=orb` puts `orb.html` on the wall instead. |
| `orb.html` | Orbloom lab (vendored `orbloom` 0.1.0, MIT). Parked for now. |
| `mist-logo-original.html` | The original interactive M logo the visualizer is derived from. Reference only. |

## Visualizer keys (work on the stage too)

- `Q W E R` states: idle, listening, thinking, speaking. `U` quiet voice. `P` demo script.
- `1-5` variants (Halo is the default). `Y` vibe (calm / pulse / orbit / bloom / wild).
- `L` layout (center / high / left / answer). `G` grid density. `B` board. `C` dot shape. `O` color. `K` look.
- `S` simulated voice, `M` microphone. `H` hide UI. `F` fullscreen.
- Still capture: `index.html?still=1&v=0&state=speaking&t=2.4`.

Stage only: `V` camera views, `T` presenter clip, `N` hide the corner monitor.

## States

- **listening**: M centered, bloom ring, board pulses leave the ring on syllables.
- **thinking**: no ring; the M draws itself in along the stroke (the logo's wipe), holds, un-writes, repeats.
- **answering** (speaking + answer layout): M glides bottom right, cards mid screen, the frame is the literal screen edge shedding inward.

## Layout

- `blender/` headless scene builder (`build_scene.py`) that exports `stage.glb`.
- `stills/` reference captures from along the way.
- `videos/mist-keynote-tiktok/` HyperFrames project for the 60 s 9:16 keynote cut. Footage and renders are gitignored; `tools/record-all.sh` re-records the clips from the running pages, then `npx hyperframes render`.
- `vendor/orbloom/` vendored orb package.
