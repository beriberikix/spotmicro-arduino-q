# Build guide site

The step-by-step assembly guide, published at <https://beriberikix.github.io/spotmicro-arduino-q/> by
`.github/workflows/pages.yml` on every push to `main` that touches `site/`.

Built with [Astro Starlight](https://starlight.astro.build/).

```sh
cd site
npm install
npm run dev      # http://localhost:4321/spotmicro-arduino-q/
npm run build    # site/dist
```

## Layout

| Path | What |
| ---- | ---- |
| `src/content/docs/` | One `.mdx` page per step; the sidebar order is in `astro.config.mjs` |
| `src/components/` | `Render` (step animation/exploded/assembled), `Parts` (you-need box), `Done` and `Checklist` (check-offs saved in localStorage), `Todo` (draft photo/video placeholders), `ServoMap`, `AngleTable`, `PowerDiagram`, `ModelViewer`, `Progress` |
| `src/data/servos.ts` | Servo channel map and assembly angles; keep in sync with `firmware/servo_tool/servo_tool.ino` |
| `src/data/checks.ts` | Every check-off, for the progress bar on the home page |
| `public/renders/` | Step renders: `<id>.png` (exploded), `<id>-done.png`, `<id>.mp4` |
| `public/models/` | glTF model for the 3D viewer |

## Renders

Generated from `cad/SpotUnoQ.FCStd` in the FreeCAD GUI. Steps are defined in `scripts/guide_steps.py`.

```python
# FreeCAD Python console
GUIDE_ONLY = ["knee-horn"]      # optional: just these steps
GUIDE_NO_VIDEO = True           # optional: stills only
exec(open("/path/to/spotmicro-arduino-q/scripts/render_guide.FCMacro").read())
```

About 40 s per step with video. Needs `ffmpeg`.

## Photos and videos

`<Todo id="..." kind="photo|video">` boxes mark shots still to take; `/reference/media-todo/` lists them all. Build with
`PUBLIC_HIDE_TODO=1` to hide them.
