# 207 Elk Ave S — Leasing Website

Interactive commercial medical and executive office leasing platform for **207 Elk Ave S** (located in historic downtown **Fayetteville, TN 37334**), owned and managed by **207 Elk LLC** (Principal/Owner: Shaz Perrone).

Designed with Apple/Google-caliber editorial UI/UX, this application generalizes the property's turnkey clinical capabilities, dual-level architectural schematics, renovation concepts, and capital-preservation advantages for prospective medical, dental, specialty outpatient, urgent care, rehabilitation, behavioral health, and healthcare clinical administration tenants.

---

## Implemented Capabilities

1. **Cinematic Hero & Exterior Switcher**:
   - Instant toggle between the **Renovated Architectural Concept**, **Current Clinical Exterior** (formerly HH Lincoln Health Primary Care), and **Aerial Campus Perspective**.
   - Full-width announcement header: *"Coming Soon!  Turnkey Clinical Office Space for Lease in Downtown Fayetteville, TN"*.
   - Key facts strip (`35+ Rooms`, `~0.5 Acre Dedicated Parking`, `Minimal Trenching`).
2. **Bento-Grid Executive Metrics**:
   - Highlights `35+` plumbed exam/clinical suites, `7` dedicated procedure rooms, `12` Restrooms & Central Elevator (8 ground-floor, 4 second-floor, commercial elevator), `~0.5-acre` dedicated private parking parcel across Elk Ave S, `7` ground-floor egress doors, and `~20,256 GSF` total above-grade footprint.
3. **Interactive Specialty Fit Explorer**:
   - Dynamic profile switcher tailored to 7 medical tenant archetypes:
     - *Primary Care & Multi-Specialty Medical Group*
     - *Urgent Care, Orthopedic Walk-In & Occupational Medicine*
     - *Dental Group, Oral Surgery & Hygiene Clinic*
     - *Dermatology, Mohs Surgery, Aesthetics & MedSpa*
     - *Physical, Occupational & Pediatric Rehabilitation*
     - *Behavioral Health, Psychiatry & Counseling Center*
     - *Healthcare Administration, Executive & Telehealth Center*
4. **Interactive Before / After Architectural Transformation Studio**:
   - Draggable split-screen comparison slider across 6 property zones: *Exterior Facade*, *Main Lobby & Hospitality Arrival*, *Primary Waiting Lounge*, *Private Exam & Specialty Procedure Suites*, *Centralized Nurse Workstations*, and *2nd Floor Conference, Lounge & Collaboration Suite*.
5. **Interactive Dual-Level Floorplan & Suite Explorer**:
   - Switch between **Ground Level (1st Floor · ~12,874 SF)** and **Upper Level (2nd Floor · ~7,382 SF)** schematics with fullscreen zoom modal and zone-by-zone clinical breakdowns.
6. **Key Strategic Advantages Briefing**:
   - Structured across 3 strategic pillars: *Turnkey Clinical Infrastructure & Speed to Market*, *Unmatched Parking, Downtown Walkability & Regional Reach*, and *Healthcare Heritage, Incentives & Long-Term Ownership Partnership*.
7. **Two-Tract Certified Survey & Filterable Media Gallery**:
   - Fullscreen keyboard-navigable Lightbox (`Esc`, `←`, `→`) and category filtering across property photos, renderings, drone aerials, floorplans, and surveys.
8. **Compliance & Legal Disclosures**:
   - Five comprehensive disclosures covering Owner-Principal licensing (FL Lic. #SL3651002), conceptual renderings, approximate measurements (~20,256 GSF above-grade), as-is infrastructure, and non-affiliation with former tenants.
9. **Direct Ownership Leasing Briefing Generator**:
   - Auto-synchronizes specialty and footprint selections into a formatted leasing inquiry for Principal/Owner **Shaz Perrone** (`(973) 271-5324`, `Shaz.Perrone@gmail.com`) with 1-click clipboard copy and `mailto:` launch.

---

## Repository Structure

```text
201-elk-ave-website/
├── index.html                   # Root static entrypoint for GitHub Pages (references src/elk_ave/static/)
├── .nojekyll                    # Bypasses Jekyll processing on GitHub Pages
├── main.py                      # Thin CLI entrypoint (build, check, serve)
├── pyproject.toml               # Python project metadata (zero external runtime dependencies)
├── AGENTS.md                    # Repository engineering & architecture rules
├── README.md                    # Project documentation
├── docs/
│   └── completion-report.md     # Development & validation completion report
├── src/
│   └── elk_ave/
│       ├── __init__.py
│       ├── models.py            # Immutable domain dataclasses & provenance models
│       ├── catalog.py           # Canonical generalized property dataset
│       ├── calculator.py        # Pure deterministic TI & footprint calculator
│       ├── renderer.py          # Static HTML5, JSON-LD & asset builder/verifier
│       ├── server.py            # Local HTTP preview server & JSON API (/api/*)
│       └── static/              # Source CSS, JS, and extracted property images
└── tests/
    └── test_elk_ave.py          # Automated unit & integration test suite
```

---

## Quick Start (Local Build & Preview)

This repository uses Python 3.9+ standard library modules only and requires zero external runtime packages.

### 1. Validate Catalog & Asset Integrity

```bash
uv run python3 main.py check
```

### 2. Build Static Site (`dist/` & GitHub Pages Root Entrypoint)

```bash
uv run python3 main.py build
```

This generates:
- A self-contained static bundle in `dist/index.html` (which can be opened directly or served via the local HTTP server).
- Synchronized root-level `index.html` and `.nojekyll` files configured with `data-asset-prefix="src/elk_ave/static"` so GitHub Pages branch deployments from `/` (root) load all stylesheets, scripts, and images directly without asset duplication.

### 3. Run Local Preview Server

```bash
uv run python3 main.py serve --host 127.0.0.1 --port 8000
```

Then visit `http://127.0.0.1:8000` in your browser. The server also exposes:

- `GET /api/health` — Server health check
- `GET /api/property` — Full canonical property dataset (`JSON`)
- `GET /api/estimate?specialty_id=dental-oral-health&rooms=18&patients=110&tier=modern-clinical` — Deterministic TI capital preservation estimate (`JSON`)

### 4. Run Automated Tests

```bash
uv run python3 -m unittest discover -s tests -v
```

