# Copilot Instructions for web-midi-listener (BandMaster Listener)

## Overview

A minimal web app for an Android tablet (Chrome): it listens on a MIDI input via WebMIDI and
shows the PDF sheet music whose filename starts with the received song number, full-screen.
It is the companion of **BandMaster** (repo `Heinz`), which sends the song numbers.
Used on stage: must be robust against MIDI noise (clock, active sensing, …), work offline,
and be operable by touch.

## Structure

- `index.html` – the complete app (HTML + CSS + vanilla JS in one file, no build step).
  Uses PDF.js 3.11 from cdnjs, `navigator.requestMIDIAccess`, `showDirectoryPicker`,
  settings in `localStorage`.
- `sw.js` – service worker for offline use (cache name `CACHE`).
- `serve.py` / `serve.bat` – local HTTPS dev server (self-signed cert, needs `cryptography`).
- `.github/workflows/deploy.yml` – deploys the repo root to **GitHub Pages on every push to `main`**.

## Build, Run & Test

```powershell
python serve.py           # https://localhost:8080/ (and LAN address for the tablet)
```

- No build and no automated tests. Verify changes manually in Chrome (desktop and Android).
  Describe exact manual steps in the task **Checkpoints** and in the review's "Manual Checks".
- Stress test with MIDI noise: `python ..\Heinz\bandmaster\keyboard_simulation.py`.

## Conventions

- Keep it a single self-contained `index.html`; no frameworks, bundlers or new dependencies
  without explicit approval.
- When `index.html` or cached assets change, bump the cache name in `sw.js`
  (e.g. `bml-v1` → `bml-v2`) so installed clients update.
- Keep the PDF filename matching rules from [README.md](../README.md) backward compatible.
- Pushing to `main` publishes the app; never push unless asked.
- Update [README.md](../README.md) for user-visible changes.

## UI Conventions

- Touch-first, large controls, dark/full-screen friendly; the sheet music view must stay
  uncluttered.
- Reuse the existing CSS variables/classes in `index.html`; mockups as standalone HTML.

## Spec-Driven Development

Non-trivial features follow the SDD workflow (agents `sdd-orchestrator`, `sdd-spec-writer`,
`sdd-ui-designer`, `sdd-planner`, `sdd-implementer`, `sdd-reviewer`; conventions in the
`spec-driven-development` skill). Specs live in [specs/](../specs/README.md).
Small fixes may skip the workflow.
