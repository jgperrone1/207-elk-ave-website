"""Static site renderer and asset verifier for 207 Elk Ave S."""

from __future__ import annotations

import html
import json
import shutil
from pathlib import Path
from typing import Any

from src.elk_ave.catalog import build_property_listing
from src.elk_ave.models import PropertyListing

STATIC_SOURCE_DIR = Path(__file__).resolve().parent / "static"
REPO_ROOT_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_STATIC_PREFIX = "src/elk_ave/static"


class AssetVerificationError(FileNotFoundError):
    """Raised when a required image or static asset is missing on disk."""


def _esc(val: Any) -> str:
    """HTML-escape any value safely."""
    return html.escape(str(val), quote=True)


def _prefix_asset(rel_path: str, asset_prefix: str = "") -> str:
    """Prefix a relative asset path when rendering for a non-dist root (e.g. GitHub Pages)."""
    clean_prefix = asset_prefix.strip().strip("/")
    clean_path = rel_path.strip().lstrip("/")
    if not clean_prefix:
        return clean_path
    return f"{clean_prefix}/{clean_path}"


def _strip_provenance(obj: Any) -> Any:
    """Recursively strip internal provenance objects from serialized public JSON."""
    if isinstance(obj, dict):
        return {k: _strip_provenance(v) for k, v in obj.items() if k != "provenance"}
    if isinstance(obj, (list, tuple)):
        return [_strip_provenance(item) for item in obj]
    return obj


def build_json_ld(listing: PropertyListing) -> dict[str, Any]:
    """Build Schema.org JSON-LD metadata for medical commercial real estate."""
    return {
        "@context": "https://schema.org",
        "@type": "RealEstateListing",
        "name": f"{listing.street_address} — {listing.headline}",
        "description": listing.subheadline,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": listing.street_address,
            "addressLocality": listing.city,
            "addressRegion": listing.state,
            "postalCode": listing.postal_code,
            "addressCountry": "US",
        },
        "additionalProperty": [
            {"@type": "PropertyValue", "name": "Total Above-Grade Gross Building Area", "value": "~20,256 GSF"},
            {"@type": "PropertyValue", "name": "Plumbed Clinical & Exam Rooms", "value": "35+"},
            {"@type": "PropertyValue", "name": "Dedicated Procedure Suites", "value": "7"},
            {"@type": "PropertyValue", "name": "Restrooms", "value": "12"},
            {"@type": "PropertyValue", "name": "Dedicated Parking Lot Acres", "value": "~0.5"},
        ],
        "seller": {
            "@type": "Person",
            "name": listing.contact.name,
            "jobTitle": f"{listing.contact.role}, {listing.contact.entity}",
            "email": listing.contact.email,
        },
    }


def render_index_html(listing: PropertyListing, asset_prefix: str = "") -> str:
    """Render the complete semantic HTML5 document for 207 Elk Ave S."""
    json_ld_str = json.dumps(build_json_ld(listing), indent=2)
    embedded_data_str = json.dumps(_strip_provenance(listing.to_dict()))

    def _asset(rel_path: str) -> str:
        return _prefix_asset(rel_path, asset_prefix)

    clean_prefix = asset_prefix.strip().strip("/")
    html_prefix_attr = f' data-asset-prefix="{_esc(clean_prefix)}"' if clean_prefix else ""

    # Metric Bento Cards
    metrics_html = "\n".join(
        f"""
        <article class="metric-card">
          <div>
            <div class="metric-category">{_esc(m.category)}</div>
            <div class="metric-value">{_esc(m.value)}</div>
            <h3 class="metric-label">{_esc(m.unit_or_label)}</h3>
          </div>
          <p class="metric-detail">{_esc(m.detail)}</p>
        </article>
        """
        for m in listing.metrics
    )

    # Archetype Pills & Default Active Stage
    first_arch = listing.archetypes[0]
    archetype_pills_html = "\n".join(
        f"""<button type="button" class="archetype-pill{' active' if idx == 0 else ''}" data-archetype-id="{_esc(a.id)}">{_esc(a.specialty)}</button>"""
        for idx, a in enumerate(listing.archetypes)
    )
    first_arch_why = "\n".join(
        f"<li><span>{_esc(pt)}</span></li>" for pt in first_arch.why_it_fits
    )
    first_arch_infra = "\n".join(
        f'<span class="infra-tag">{_esc(tag)}</span>'
        for tag in first_arch.infrastructure_match
    )

    # Transformation Studio Tabs & Default Active Pair
    first_tr = listing.transformations[0]
    studio_tab_labels = {
        "exterior-facade": "Exterior: Architectural Exterior",
        "waiting-lounge": "Waiting Lounge: Primary Patient Lounge",
        "exam-procedure-suite": "Exam & Procedure Suites",
        "nurses-station": "Clinical Core: Nurse Workstations",
        "upper-breakroom-conference": "2nd Floor Conference & Lounge",
    }
    studio_tabs_html = "\n".join(
        f"""<button type="button" class="studio-tab{' active' if idx == 0 else ''}" data-transform-id="{_esc(t.id)}">{_esc(studio_tab_labels.get(t.id, t.title))}</button>"""
        for idx, t in enumerate(listing.transformations)
    )

    # Floor Explorer Default Level 1
    first_floor = listing.floors[0]
    floor_tabs_html = "\n".join(
        f"""<button type="button" class="floor-tab-btn{' active' if idx == 0 else ''}" data-floor-level="{f.level}">{_esc(f.name)}</button>"""
        for idx, f in enumerate(listing.floors)
    )
    first_floor_zones_html = "\n".join(
        f"""
        <article class="zone-card">
          <div class="zone-card-header">
            <h4 class="zone-title">{_esc(z.name)}</h4>
            <span class="zone-badge">{_esc(z.room_count_label)}</span>
          </div>
          <ul class="zone-highlights">
            {"".join(f"<li>{_esc(h)}</li>" for h in z.highlights)}
          </ul>
          <div class="infra-tags">
            {"".join(f'<span class="infra-tag">{_esc(u)}</span>' for u in z.ideal_uses)}
          </div>
        </article>
        """
        for z in first_floor.zones
    )

    # Calculator Specialty Options
    calc_options_html = "\n".join(
        f'<option value="{_esc(a.id)}">{_esc(a.specialty)}</option>'
        for a in listing.archetypes
    )

    # Strategic Pillars (21 Generalized Points)
    pillars_html = "\n".join(
        f"""
        <article class="pillar-card">
          <div class="pillar-subtitle">{_esc(p.subtitle)}</div>
          <h3 class="pillar-title">{_esc(p.title)}</h3>
          <p style="font-size: 0.92rem; color: var(--text-secondary);">{_esc(p.summary)}</p>
          <ul class="pillar-points">
            {"".join(
                f'''
                <li class="pillar-point">
                  <span class="point-num">{pt.number:02d}</span>
                  <div class="point-body">
                    <strong>{_esc(pt.title)}</strong>
                    <p>{_esc(pt.description)}</p>
                  </div>
                </li>
                '''
                for pt in p.points
            )}
          </ul>
        </article>
        """
        for p in listing.pillars
    )

    # Gallery Categories & Items
    gallery_categories = ["All"] + sorted({g.category for g in listing.gallery})
    gallery_filters_html = "\n".join(
        f"""<button type="button" class="archetype-pill{' active' if cat == 'All' else ''}" data-gallery-cat="{_esc(cat)}">{_esc(cat)}</button>"""
        for cat in gallery_categories
    )

    def _render_gallery_card(g: GalleryAsset) -> str:
        type_class = "conceptual" if g.is_conceptual else "actual"
        type_label = "Conceptual Renovation" if g.is_conceptual else "Actual Photo"
        return f"""
        <article class="gallery-item" data-gallery-item="{_esc(g.id)}" data-item-category="{_esc(g.category)}" data-item-type="{type_class}">
          <div class="gallery-thumb">
            <span class="gallery-card-badge gallery-card-badge--{type_class}">
              {type_label}
            </span>
            <img src="{_esc(_asset(g.image_path))}" alt="{_esc(g.title)}" loading="lazy" />
          </div>
          <div class="gallery-meta">
            <div class="gallery-cat">{_esc(g.category)}</div>
            <h3 class="gallery-title">{_esc(g.title)}</h3>
            <p class="gallery-caption">{_esc(g.caption)}</p>
          </div>
        </article>
        """

    actual_gallery_cards = "\n".join(_render_gallery_card(g) for g in listing.gallery if not g.is_conceptual)
    conceptual_gallery_cards = "\n".join(_render_gallery_card(g) for g in listing.gallery if g.is_conceptual)
    actual_count = sum(1 for g in listing.gallery if not g.is_conceptual)
    conceptual_count = sum(1 for g in listing.gallery if g.is_conceptual)

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light"{html_prefix_attr}>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{_esc(listing.street_address)} | Clinical &amp; Executive Space for Lease — Fayetteville, TN</title>
  <meta name="description" content="{_esc(listing.subheadline)}" />
  <meta property="og:title" content="{_esc(listing.street_address)} — Clinical &amp; Executive Space for Lease" />
  <meta property="og:description" content="{_esc(listing.subheadline)}" />
  <meta property="og:type" content="website" />
  <meta property="og:image" content="https://jgperrone1.github.io/207-elk-ave-website/src/elk_ave/static/assets/images/exterior_wellness_no_cafe.png" />
  <link rel="stylesheet" href="{_esc(_asset('styles.css'))}" />
  <script type="application/ld+json">{json_ld_str}</script>
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>

  <!-- Sticky Glassmorphic Navigation -->
  <header class="site-header" role="banner">
    <div class="container header-inner">
      <a href="#top" class="brand" aria-label="207 Elk Ave S Home">
        <span class="brand-mark">207</span>
        <span class="brand-text">
          <span class="brand-name">207 Elk Ave S</span>
          <span class="brand-location">Fayetteville, TN · Medical Campus</span>
        </span>
      </a>

      <nav id="primary-navigation" class="header-nav" aria-label="Primary Navigation">
        <ul class="nav-links">
          <li><a href="#overview">Overview</a></li>
          <li><a href="#specialties">Specialties</a></li>
          <li><a href="#transformations">Renovations</a></li>
          <li><a href="#floorplans">Floorplans</a></li>
          <li><a href="#advantages">Advantages</a></li>
          <li><a href="#location">Parking</a></li>
          <li><a href="#gallery">Gallery</a></li>
          <li><a href="#disclosures" class="nav-disclosure-link">Disclosures</a></li>
        </ul>
      </nav>

      <div class="header-actions">
        <a href="#contact" class="btn btn--primary btn--sm header-contact-btn">Contact For Info</a>
        <button type="button" id="theme-toggle-btn" class="icon-btn" aria-label="Toggle color theme">🌙</button>
        <button
          type="button"
          id="mobile-menu-btn"
          class="icon-btn mobile-menu-toggle"
          aria-label="Toggle navigation menu"
          aria-expanded="false"
          aria-controls="primary-navigation"
        >
          <span class="hamburger-icon" aria-hidden="true">
            <span></span>
            <span></span>
            <span></span>
          </span>
        </button>
      </div>
    </div>
  </header>

  <main id="main-content">
    <!-- Hero Section -->
    <section id="top" class="hero">
      <div class="container">
        <div class="hero-header-full">
          <div class="hero-coming-soon-bubble">
            <span class="coming-soon-pulse"></span>
            <span>Coming Soon!</span>
          </div>
          <h1 class="hero-title hero-title--full">
            <span class="hero-title-line">Clinical Office Space for Lease</span>
            <span class="hero-title-subline">Downtown Fayetteville, TN</span>
          </h1>
        </div>

        <div class="hero-grid">
          <div class="hero-copy">
            <p class="hero-lead">
              {_esc(listing.subheadline)} Formerly home to <strong>HH Lincoln Health Primary Care</strong>
              at 207 Elk Ave S, one block off Fayetteville’s historic Town Square.
            </p>

            <div class="hero-cta-row">
              <a href="#floorplans" class="btn btn--primary">Explore Interactive Floorplans</a>
              <a href="#contact" class="btn btn--secondary">Contact For Info</a>
            </div>

            <div class="hero-quick-facts">
              <div>
                <div class="quick-fact-val">35+ Rooms</div>
                <div class="quick-fact-lbl">Sink-equipped exam &amp; clinical suites across 2 levels</div>
              </div>
              <div>
                <div class="quick-fact-val">~0.5 Acre</div>
                <div class="quick-fact-lbl">Dedicated private parking lot directly across Elk Ave S</div>
              </div>
              <div>
                <div class="quick-fact-val">Minimal Trenching</div>
                <div class="quick-fact-lbl">Intact wet walls, direct subfloor/basement utility access, X-ray &amp; lab rooms</div>
              </div>
            </div>
          </div>

          <div class="hero-showcase">
            <div class="hero-image-frame">
              <img
                id="hero-main-image"
                src="{_esc(_asset('assets/images/exterior_wellness_no_cafe.png'))}"
                alt="207 Elk Ave S Renovated Medical &amp; Executive Exterior Concept"
              />
            </div>
            <div class="hero-view-switcher">
              <div class="hero-view-caption">
                <strong id="hero-view-label">Renovated Architectural Concept</strong>
                <span id="hero-view-sub">Modernized brick &amp; dark architectural bronze facade along Elk Ave S</span>
              </div>
              <div class="segmented-control" role="group" aria-label="Exterior View Selector">
                <button type="button" class="segmented-btn active" data-hero-view="renovated">Renovated</button>
                <button type="button" class="segmented-btn" data-hero-view="original">Current</button>
                <button type="button" class="segmented-btn" data-hero-view="aerial">Aerial</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Executive Overview & Bento Metrics -->
    <section id="overview" class="section section--alt">
      <div class="container">
        <div class="section-header">
          <span class="eyebrow">Executive Overview</span>
          <h2 class="section-title">Clinical Infrastructure Readiness</h2>
          <p class="section-subtitle">
            {_esc(listing.executive_summary[0])} {_esc(listing.executive_summary[1])}
          </p>
        </div>

        <div class="bento-metrics">
          {metrics_html}
        </div>
      </div>
    </section>

    <!-- Interactive Specialty Fit Explorer -->
    <section id="specialties" class="section">
      <div class="container">
        <div class="section-header">
          <span class="eyebrow">Clinical Adaptability</span>
          <h2 class="section-title">Engineered for Multi-Specialty Practices</h2>
          <p class="section-subtitle">
            Select your clinical discipline below to inspect how 207 Elk Ave S’s existing wet walls,
            procedure rooms, dual waiting lounges, and upper administrative/therapy suites align with your practice.
          </p>
        </div>

        <div class="archetype-pills" role="tablist" aria-label="Medical Specialty Profiles">
          {archetype_pills_html}
        </div>

        <div class="archetype-stage" role="tabpanel">
          <div>
            <span class="eyebrow" id="arch-specialty">{_esc(first_arch.specialty)}</span>
            <h3 class="archetype-headline" id="arch-headline">{_esc(first_arch.headline)}</h3>
            <ul class="archetype-list" id="arch-why-list">
              {first_arch_why}
            </ul>
            <div style="display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 1.5rem;">
              <a href="#contact" id="arch-inquire-btn" class="btn btn--primary">
                Inquire About This Specialty Layout →
              </a>
              <a href="#contact" class="btn btn--secondary">Request Custom Space Plan</a>
            </div>
          </div>

          <div class="archetype-meta-box">
            <div class="archetype-meta-row">
              <div class="archetype-meta-label">Recommended Footprint Selection</div>
              <div class="archetype-meta-val" id="arch-config">{_esc(first_arch.recommended_configuration)}</div>
            </div>
            <div class="archetype-meta-row">
              <div class="archetype-meta-label">Typical Clinical Suite Allocation</div>
              <div class="archetype-meta-val" id="arch-rooms">{first_arch.target_rooms} Plumbed Clinical / Exam Rooms</div>
            </div>
            <div>
              <div class="archetype-meta-label">Built-Out Infrastructure Match</div>
              <div class="infra-tags" id="arch-infra-tags">
                {first_arch_infra}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Interactive Before / After Transformation Studio -->
    <section id="transformations" class="section section--dark">
      <div class="container">
        <div class="section-header">
          <span class="eyebrow">Renovation Concepts</span>
          <h2 class="section-title">Before &amp; After Architectural Concepts</h2>
          <p class="section-subtitle">
            Drag the interactive split-screen slider across five key property zones to see how cosmetic
            millwork, lighting, and flooring upgrades transform the intact clinical footprint.
          </p>
        </div>

        <div class="studio-tabs" role="tablist" aria-label="Transformation Spaces">
          {studio_tabs_html}
        </div>

        <div class="studio-layout">
          <div class="comparison-viewer">
            <span class="comparison-badge comparison-badge--before" id="studio-before-badge">
              {_esc(first_tr.before_label)}
            </span>
            <span class="comparison-badge comparison-badge--after" id="studio-after-badge">
              {_esc(first_tr.after_label)}
            </span>

            <div class="comparison-layer comparison-after">
              <img id="studio-after-img" src="{_esc(_asset(first_tr.after_image))}" alt="{_esc(first_tr.after_label)}" />
            </div>
            <div class="comparison-layer comparison-before" id="studio-before-layer">
              <img id="studio-before-img" src="{_esc(_asset(first_tr.before_image))}" alt="{_esc(first_tr.before_label)}" />
            </div>

            <div class="comparison-handle" id="studio-handle">
              <div class="comparison-knob">↔</div>
            </div>

            <input
              type="range"
              id="studio-range"
              class="comparison-range"
              min="0"
              max="100"
              value="50"
              aria-label="Before and after image comparison slider"
            />
          </div>

          <div class="studio-details">
            <div class="studio-subtitle" id="studio-subtitle">{_esc(first_tr.subtitle)}</div>
            <h3 class="studio-title" id="studio-title">{_esc(first_tr.title)}</h3>
            <p class="studio-desc" id="studio-desc">{_esc(first_tr.description)}</p>
            <div class="studio-clinical-box" id="studio-clinical">
              {_esc(first_tr.clinical_value)}
            </div>
            <div class="studio-preset-row">
              <button type="button" class="studio-tab" data-slider-pos="100">Show Existing (100%)</button>
              <button type="button" class="studio-tab" data-slider-pos="50">50/50 Split</button>
              <button type="button" class="studio-tab" data-slider-pos="0">Show Renovated (100%)</button>
              <button type="button" class="studio-tab" id="studio-alt-btn">View {_esc(first_tr.alt_label or 'Alternate')}</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Interactive Dual-Level Architectural Floorplan Explorer -->
    <section id="floorplans" class="section">
      <div class="container">
        <div class="floor-switcher-bar">
          <div>
            <span class="eyebrow">Floorplans</span>
            <h2 class="section-title" style="margin-bottom: 0.25rem;">Dual-Level Floorplan Explorer</h2>
            <p class="section-subtitle">
              Lease flexible clinical suites, the Ground Floor (~12,874 GSF), the Upper Level (~7,382 GSF), or combine both elevator-connected levels (~20,256 GSF) into a custom medical campus.
            </p>
          </div>
          <div class="floor-tabs" role="tablist" aria-label="Building Floor Selector">
            {floor_tabs_html}
          </div>
        </div>

        <div class="floor-explorer-grid">
          <div class="floorplan-card">
            <div class="floorplan-toolbar">
              <div>
                <strong id="floorplan-name" style="font-size: 1.1rem;">{_esc(first_floor.name)}</strong>
                <div id="floorplan-tagline" style="font-size: 0.82rem; color: #4b5c63;">{_esc(first_floor.tagline)}</div>
              </div>
              <button type="button" id="floorplan-zoom-btn" class="btn btn--secondary btn--sm" style="color:#11191c; background:#f3f7f6;">
                🔍 Fullscreen Schematic
              </button>
            </div>

            <div class="floorplan-canvas" id="floorplan-canvas-wrap" title="Click to enlarge architectural schematic">
              <img id="floorplan-img" src="{_esc(_asset(first_floor.floorplan_image))}" alt="{_esc(first_floor.name)} Floorplan" />
            </div>

            <p id="floorplan-summary" style="font-size: 0.88rem; color: #3f4f56; margin-top: 1rem;">
              {_esc(first_floor.summary)}
            </p>

            <div class="floor-stats-strip">
              <div>
                <div class="floor-stat-num" id="floor-stat-exam">{first_floor.exam_and_clinical_rooms}+</div>
                <div class="floor-stat-lbl">Plumbed Exam Rooms</div>
              </div>
              <div>
                <div class="floor-stat-num" id="floor-stat-proc">{first_floor.procedure_rooms}</div>
                <div class="floor-stat-lbl">Procedure Suites</div>
              </div>
              <div>
                <div class="floor-stat-num" id="floor-stat-rest">{first_floor.restrooms}</div>
                <div class="floor-stat-lbl" id="floor-stat-rest-lbl">Ground-Floor Restrooms</div>
                <div class="floor-stat-sub" style="font-size:0.75rem; color:var(--text-muted);">ADA-Accessible Restroom Facilities</div>
              </div>
            </div>
          </div>

          <div class="zone-cards-stack" id="floor-zones-container">
            {first_floor_zones_html}
          </div>
        </div>
      </div>
    </section>

    <!-- Key Strategic Advantages -->
    <section id="advantages" class="section">
      <div class="container">
        <div class="section-header">
          <span class="eyebrow">Strategic Advantages</span>
          <h2 class="section-title">Key Strategic Advantages</h2>
        </div>

        <div class="pillars-grid">
          {pillars_html}
        </div>
      </div>
    </section>

    <!-- Location, Dedicated ~0.5-Acre Parking & Certified Surveys -->
    <section id="location" class="section section--alt">
      <div class="container">
        <div class="section-header">
          <span class="eyebrow">Parking &amp; Location</span>
          <h2 class="section-title">Dedicated Off-Street Parking &amp; Campus Location</h2>
          <p class="section-subtitle">
            Unlike typical downtown buildings with constrained street parking, 207 Elk Ave S includes both
            on-site ADA parking on <strong>Tract 1 (0.39 AC)</strong> and a dedicated <strong>0.45-acre (~0.5 AC) paved parking lot (Tract 2)</strong>
            directly across Elk Ave S.
          </p>
        </div>

        <div class="campus-location-grid">
          <div>
            <div class="floorplan-card">
              <div class="floorplan-toolbar">
                <strong>Certified Two-Tract Boundary Survey (Tract 1 &amp; Tract 2)</strong>
                <span class="zone-badge">0.84 Total Campus Acres</span>
              </div>
              <img src="{_esc(_asset('assets/images/survey-two-tracts.png'))}" alt="Certified Two-Tract Survey for 207 Elk Ave S" />
              <p style="font-size:0.84rem; color:#4b5c63; margin-top:0.75rem;">
                Survey by Michael R. Gooding PE, RLS — showing Tract 1 (0.39 AC Medical Building at Elk Ave S &amp; Campbell St E)
                and Tract 2 (0.45 AC Dedicated Parking Lot directly across Elk Ave S).
              </p>
            </div>
          </div>

          <div style="display:flex; flex-direction:column; justify-content:space-between;">
            <div>
              <h3 style="font-family:var(--font-serif); font-size:2rem; margin-bottom:0.75rem;">
                Strategic Regional Healthcare Hub
              </h3>
              <p style="color:var(--text-secondary); margin-bottom:1rem;">
                Positioned one block behind Fayetteville’s historic Courthouse Square and minutes from
                <strong>HH Lincoln Medical Center</strong>, 207 Elk Ave S sits at the geographic center of a
                multi-county catchment area directly north of the booming <strong>Huntsville / Rocket City</strong> corridor.
              </p>
              <ul class="archetype-list">
                <li><span><strong>Walkable Downtown Amenities:</strong> Immediate access to Main Avenue dining, pharmacies, banking, and municipal services for providers and patients.</span></li>
                <li><span><strong>Dedicated ~0.5-Acre Parking Parcel:</strong> Eliminates parking bottlenecks for outpatient clinics and staff shifts.</span></li>
                <li><span><strong>Hospital &amp; Referral Synergy:</strong> Minutes from Lincoln Medical Center (Huntsville Hospital Health System) for imaging, lab, and inpatient coordination.</span></li>
              </ul>
            </div>

            <div class="parcel-cards">
              <div class="parcel-card">
                <img src="{_esc(_asset('assets/images/aerial-building-boundary.jpg'))}" alt="Tract 1 Building Boundary Aerial" loading="lazy" />
                <div class="parcel-card-body">
                  <strong style="font-size:0.92rem;">Tract 1: Medical Building (0.39 AC)</strong>
                  <p style="font-size:0.8rem; color:var(--text-secondary);">2-story brick core + 1-story clinical wing + curbside &amp; side ADA parking.</p>
                </div>
              </div>
              <div class="parcel-card">
                <img src="{_esc(_asset('assets/images/aerial-parking-lot-boundary.jpg'))}" alt="Tract 2 Dedicated Parking Lot Boundary Aerial" loading="lazy" />
                <div class="parcel-card-body">
                  <strong style="font-size:0.92rem;">Tract 2: Dedicated Parking (0.45 AC)</strong>
                  <p style="font-size:0.8rem; color:var(--text-secondary);">Expansive paved private lot directly across Elk Ave S.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Filterable High-Resolution Property Gallery -->
    <section id="gallery" class="section">
      <div class="container">
        <div class="section-header">
          <span class="eyebrow">Media Gallery</span>
          <h2 class="section-title">Property &amp; Campus Gallery</h2>
          <p class="section-subtitle">
            Explore authentic property photographs of 207 Elk Ave S alongside conceptual architectural renovation concepts. Click any card to inspect in fullscreen.
          </p>
        </div>

        <div class="gallery-controls-bar">
          <div class="gallery-segment-control" role="group" aria-label="Photo Type Selector">
            <button type="button" class="gallery-segment-btn active" data-gallery-type="all">
              All Views ({len(listing.gallery)})
            </button>
            <button type="button" class="gallery-segment-btn" data-gallery-type="actual">
              <span class="segment-indicator segment-indicator--actual"></span>
              Actual Property Photos ({actual_count})
            </button>
            <button type="button" class="gallery-segment-btn" data-gallery-type="conceptual">
              <span class="segment-indicator segment-indicator--conceptual"></span>
              Conceptual Renovations ({conceptual_count})
            </button>
          </div>

          <div class="gallery-filters" role="group" aria-label="Gallery Category Filter">
            {gallery_filters_html}
          </div>
        </div>

        <div class="gallery-groups-container">
          <!-- Actual Property Photographs Section -->
          <div class="gallery-group" id="gallery-actual-group" data-group-type="actual">
            <div class="gallery-group-header">
              <div class="gallery-group-pill gallery-group-pill--actual">
                ● Actual Property Photographs (Existing Condition)
              </div>
              <h3 class="gallery-group-title">Authentic Interior, Exterior, Aerial &amp; Campus Views</h3>
              <p class="gallery-group-desc">
                Current photography showing the intact clinical exam suites, furnished executive offices, commercial elevator lobby, waiting rooms, campus streetscape, and certified boundary surveys.
              </p>
            </div>
            <div class="gallery-grid" id="gallery-actual-grid">
              {actual_gallery_cards}
            </div>
          </div>

          <!-- Conceptual Renovations Section -->
          <div class="gallery-group" id="gallery-conceptual-group" data-group-type="conceptual">
            <div class="gallery-group-header">
              <div class="gallery-group-pill gallery-group-pill--conceptual">
                ✦ Conceptual Renovations (Illustrative Only)
              </div>
              <h3 class="gallery-group-title">Architectural Renovation &amp; Modernization Concepts</h3>
              <p class="gallery-group-desc">
                Conceptual renderings showing potential cosmetic millwork, lighting, flooring, and care-team station upgrades across patient care suites (actual delivery condition governed by lease terms).
              </p>
            </div>
            <div class="gallery-grid" id="gallery-conceptual-grid">
              {conceptual_gallery_cards}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Prominent Disclosure & Disclaimer Section -->
    <section id="disclosures" class="section section--alt">
      <div class="container">
        <div class="section-header">
          <span class="eyebrow">Disclosures</span>
          <h2 class="section-title">Ownership &amp; Legal Disclosures</h2>
          <p class="section-subtitle">
            Mandatory disclosures, statutory notices, and property disclaimers for prospective commercial tenants.
          </p>
        </div>

        <div class="disclosure-grid">
          <article class="disclosure-card">
            <div class="disclosure-badge">Owner-Principal Disclosure</div>
            <h3 class="disclosure-title">Owner-Principal &amp; License Disclosure</h3>
            <div class="disclosure-body">
              <p>
                Offered directly by Owner, 207 ELK LLC. Managing Principal holds an active real estate sales associate license in the State of Florida (Lic. #SL3651002) and is not acting as a licensed Tennessee real estate broker or agent.
              </p>
            </div>
          </article>

          <article class="disclosure-card">
            <div class="disclosure-badge">Conceptual Advisory</div>
            <h3 class="disclosure-title">Conceptual Renderings Disclaimer</h3>
            <div class="disclosure-body">
              <p>
                All renovated exterior/interior renderings, architectural concepts, and before-and-after visualizations are for illustrative purposes only. Actual build-out, finishes, signage, and delivery condition are governed solely by an executed lease agreement and applicable municipal approvals.
              </p>
            </div>
          </article>

          <article class="disclosure-card">
            <div class="disclosure-badge">Spatial Verification</div>
            <h3 class="disclosure-title">Approximate Measurements &amp; Errors/Omissions</h3>
            <div class="disclosure-body">
              <p>
                All square footage figures (~20,256 GSF above-grade), room counts, floorplans, and parcel dimensions (Tract 2: 0.45 AC; 0.84 AC total campus) are approximate and subject to independent tenant verification. Information is deemed reliable but not guaranteed and is subject to change or withdrawal without notice.
              </p>
            </div>
          </article>

          <article class="disclosure-card">
            <div class="disclosure-badge">Infrastructure Condition</div>
            <h3 class="disclosure-title">As-Is Clinical Infrastructure &amp; Tenant Compliance</h3>
            <div class="disclosure-body">
              <p>
                Existing plumbing, wet walls, electrical systems, X-ray room shielding, and laboratory rough-ins are offered as-is, where-is. Specialty equipment installation, radiation shielding certification, medical gas, and all practice-specific healthcare licensing and inspections are the sole responsibility of the tenant.
              </p>
            </div>
          </article>

          <article class="disclosure-card">
            <div class="disclosure-badge">Historical Context</div>
            <h3 class="disclosure-title">No Affiliation with Former Tenant</h3>
            <div class="disclosure-body">
              <p>
                207 ELK LLC is an independent property owner and is not affiliated with, endorsed by, or sponsored by Huntsville Hospital Health System or Lincoln Health. References to prior medical occupancy are provided strictly for historical context.
              </p>
            </div>
          </article>
        </div>
      </div>
    </section>

    <!-- Direct Principal / Owner Contact & Tour Request Builder -->
    <section id="contact" class="section section--dark">
      <div class="container">
        <div class="section-header">
          <span class="eyebrow">Direct Leasing</span>
          <h2 class="section-title">Contact Ownership Directly</h2>
          <p class="section-subtitle">
            Work directly with ownership to structure a single-floor, phased,
            or full-building medical lease tailored to your clinical timeline and program goals (Base Rent + pro-rata building expense share / NNN pass-throughs).
          </p>
        </div>

        <div class="contact-grid">
          <div class="owner-card">
            <div class="owner-header">
              <img
                src="{_esc(_asset(listing.contact.portrait_image))}"
                alt="{_esc(listing.contact.name)}"
                class="owner-avatar"
              />
              <div>
                <div style="font-size:0.78rem; text-transform:uppercase; letter-spacing:0.08em; color:#5eead4; font-weight:700;">
                  {_esc(listing.contact.role)} · {_esc(listing.contact.entity)}
                </div>
                <h3 style="font-family:var(--font-serif); font-size:2rem; line-height:1.15;">
                  {_esc(listing.contact.name)}
                </h3>
                <div style="font-size:0.9rem; color:var(--text-on-dark-muted);">
                  {_esc(listing.contact.title)}
                </div>
              </div>
            </div>

            <p style="font-size:0.95rem; color:#d5e3e0; line-height:1.65;">
              {_esc(listing.contact.credentials_summary)}
            </p>

            <div class="owner-contact-links">
              <a href="mailto:{_esc(listing.contact.email)}" class="owner-contact-link">
                <span>✉️</span>
                <div>
                  <div style="font-size:0.75rem; color:var(--text-on-dark-muted);">Direct Email</div>
                  <div>{_esc(listing.contact.email)}</div>
                </div>
              </a>
              <a
                href="https://www.google.com/maps/search/?api=1&amp;query=207+Elk+Ave+S,+Fayetteville,+TN+37334"
                target="_blank"
                rel="noopener noreferrer"
                class="owner-contact-link"
              >
                <span>📍</span>
                <div>
                  <div style="font-size:0.75rem; color:var(--text-on-dark-muted);">Property Location (Google Maps ↗)</div>
                  <div>207 Elk Ave S, Fayetteville, TN 37334</div>
                </div>
              </a>
            </div>

            <div style="font-size:0.82rem; color:var(--text-on-dark-muted); border-top:1px solid var(--border-on-dark); padding-top:1rem;">
              Ownership provides assistance to tenants seeking applicable local municipal programs and downtown revitalization incentives.
            </div>
          </div>

          <div class="inquiry-card">
            <h3 style="font-family:var(--font-serif); font-size:1.85rem; margin-bottom:0.35rem;">
              Generate Custom Leasing Briefing
            </h3>
            <p style="font-size:0.9rem; color:var(--text-secondary); margin-bottom:1.25rem;">
              Select your clinical specialty and desired suite footprint below. A customized leasing briefing will synchronize in real time for direct discussion with ownership.
            </p>

            <div class="form-row-2" style="margin-bottom:1rem;">
              <div>
                <label class="calc-label" for="inq-name">Your Name &amp; Title</label>
                <input type="text" id="inq-name" class="calc-input" placeholder="e.g., Dr. Sarah Jenkins, MD / VP Operations" />
              </div>
              <div>
                <label class="calc-label" for="inq-org">Medical Practice or Organization</label>
                <input type="text" id="inq-org" class="calc-input" placeholder="e.g., Southern Middle TN Specialty Group" />
              </div>
            </div>

            <div class="form-row-2" style="margin-bottom:1rem;">
              <div>
                <label class="calc-label" for="inq-specialty">Specialty / Clinical Profile</label>
                <select id="inq-specialty" class="calc-select">
                  <option value="Primary Care &amp; Multi-Specialty Medical Group">Primary Care &amp; Multi-Specialty</option>
                  <option value="Urgent Care, Walk-In &amp; Occupational Medicine">Urgent Care &amp; Occupational Medicine</option>
                  <option value="Dental Practice &amp; Oral Health Clinic">Dental &amp; Oral Health</option>
                  <option value="Dermatology &amp; Aesthetics Clinic">Dermatology &amp; Aesthetics</option>
                  <option value="Physical, Occupational &amp; Pediatric Rehabilitation">Physical &amp; Pediatric Rehabilitation</option>
                  <option value="Behavioral Health, Psychiatry &amp; Counseling">Behavioral Health &amp; Psychiatry</option>
                  <option value="Healthcare Administration, Executive &amp; Telehealth Center">Healthcare Administration &amp; Telehealth</option>
                  <option value="Outpatient Medical &amp; Executive Office Suite">Other Outpatient / Medical Specialty</option>
                </select>
              </div>
              <div>
                <label class="calc-label" for="inq-footprint">Target Footprint Configuration</label>
                <select id="inq-footprint" class="calc-select">
                  <option value="Full Ground Floor Clinical Wing (24+ Plumbed Exam Rooms, 7 Proc Suites, ~12,874 GSF)">Full Ground Floor Wing (24+ Rooms, 7 Proc Suites, ~12,874 GSF)</option>
                  <option value="Ground Floor Phased Clinical Pod (12–16 Plumbed Rooms)">Ground Floor Clinical Pod (12–16 Rooms)</option>
                  <option value="Upper Level Executive &amp; Clinical Suite (11 Plumbed Rooms, 16 Offices, ~7,382 GSF)">Upper Level Suite (11 Rooms, 16 Offices, ~7,382 GSF)</option>
                  <option value="Full Two-Story Medical Campus (35+ Plumbed Rooms, ~20,256 GSF)">Full Campus (35+ Plumbed Rooms, ~20,256 GSF)</option>
                </select>
              </div>
            </div>

            <div class="form-row-2" style="margin-bottom:1rem;">
              <div>
                <label class="calc-label" for="inq-timeline">Target Occupancy Horizon</label>
                <input type="text" id="inq-timeline" class="calc-input" value="" placeholder="e.g., Q1 / Q2 2027 or Within 3–6 Months" />
              </div>
              <div>
                <label class="calc-label" for="inq-notes">Specific Clinical or Lease Notes</label>
                <input type="text" id="inq-notes" class="calc-input" placeholder="e.g., Ground floor wing + diagnostic suite access" />
              </div>
            </div>

            <div style="margin-bottom:1.25rem;">
              <label class="calc-label" for="inquiry-preview-box">Auto-Generated Leasing Briefing Preview</label>
              <textarea
                id="inquiry-preview-box"
                class="calc-input"
                rows="8"
                readonly
                style="font-family:var(--font-mono); font-size:0.8rem; line-height:1.45;"
              ></textarea>
            </div>

            <div style="display:flex; flex-wrap:wrap; gap:0.75rem;">
              <button type="button" id="inq-mailto-btn" class="btn btn--primary">
                ✉️ Open in Email Client to Shaz Perrone
              </button>
              <button type="button" id="inq-copy-btn" class="btn btn--secondary">
                📋 Copy Briefing to Clipboard
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>

  <!-- Lightbox Modal -->
  <div id="lightbox-modal" class="lightbox" role="dialog" aria-modal="true" aria-hidden="true" aria-label="Image Lightbox">
    <div class="lightbox-content">
      <div class="lightbox-img-wrap">
        <img id="lightbox-image" src="{_esc(_asset('assets/images/exterior_wellness_no_cafe.png'))}" alt="Enlarged Property View" />
      </div>
      <div class="lightbox-bar">
        <div>
          <strong id="lightbox-title" style="display:block; font-size:1.05rem;">Property Image</strong>
          <span id="lightbox-caption" style="font-size:0.85rem; color:#a9babf;"></span>
        </div>
        <div style="display:flex; gap:0.5rem;">
          <button type="button" id="lightbox-prev" class="btn btn--secondary btn--sm" style="background:#1b272c; color:#fff;">← Prev</button>
          <button type="button" id="lightbox-next" class="btn btn--secondary btn--sm" style="background:#1b272c; color:#fff;">Next →</button>
          <button type="button" id="lightbox-close" class="btn btn--primary btn--sm">Close ✕</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <footer class="site-footer">
    <div class="container" style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:1rem;">
      <div>
        <a
          href="https://www.google.com/maps/search/?api=1&amp;query=207+Elk+Ave+S,+Fayetteville,+TN+37334"
          target="_blank"
          rel="noopener noreferrer"
          style="color:#ffffff; font-weight:700; text-decoration:underline; text-underline-offset:3px;"
        >207 Elk Ave S · Fayetteville, TN 37334 (Google Maps ↗)</a>
        <p style="margin-top:0.25rem;">Owned &amp; Managed by 207 ELK LLC · Principal/Owner: Shaz Perrone · Shaz.Perrone@gmail.com</p>
      </div>
      <div style="text-align:right;">
        <a href="#disclosures" class="footer-disclosure-link" style="color:var(--text-on-dark-muted); text-decoration:underline;">Real Estate Licensing Disclosure &amp; Disclaimers</a>
      </div>
    </div>
  </footer>

  <!-- Embedded Canonical Property Data -->
  <script id="property-data-json" type="application/json">{embedded_data_str}</script>
  <script src="{_esc(_asset('app.js'))}"></script>
</body>
</html>
"""


def build_root_pages_entry(
    repo_root: Path = REPO_ROOT_DIR,
    asset_prefix: str = ROOT_STATIC_PREFIX,
) -> Path:
    """Write root-level index.html and .nojekyll for direct GitHub Pages branch deployment."""
    listing = build_property_listing()
    verify_static_assets(listing, STATIC_SOURCE_DIR)
    repo_root.mkdir(parents=True, exist_ok=True)
    root_index = repo_root / "index.html"
    root_index.write_text(
        render_index_html(listing, asset_prefix=asset_prefix),
        encoding="utf-8",
    )
    (repo_root / ".nojekyll").write_text("", encoding="utf-8")
    return root_index


def verify_static_assets(listing: PropertyListing, root_dir: Path = STATIC_SOURCE_DIR) -> list[Path]:
    """Verify that all image assets referenced in the listing exist on disk."""
    referenced_paths: set[str] = {listing.contact.portrait_image}
    for floor in listing.floors:
        referenced_paths.add(floor.floorplan_image)
    for tr in listing.transformations:
        referenced_paths.add(tr.before_image)
        referenced_paths.add(tr.after_image)
        if tr.alt_image:
            referenced_paths.add(tr.alt_image)
    for gal in listing.gallery:
        referenced_paths.add(gal.image_path)

    verified: list[Path] = []
    for rel_path in sorted(referenced_paths):
        full_path = root_dir / rel_path
        if not full_path.is_file() or full_path.stat().st_size == 0:
            raise AssetVerificationError(
                f"Missing or empty required property asset: '{rel_path}' (expected at {full_path})."
            )
        verified.append(full_path)
    return verified


def build_static_site(output_dir: Path) -> dict[str, Any]:
    """Build the complete static site into output_dir and return build manifest."""
    listing = build_property_listing()
    verified_assets = verify_static_assets(listing, STATIC_SOURCE_DIR)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Copy CSS, JS, and image assets
    shutil.copy2(STATIC_SOURCE_DIR / "styles.css", output_dir / "styles.css")
    shutil.copy2(STATIC_SOURCE_DIR / "app.js", output_dir / "app.js")

    assets_dst = output_dir / "assets" / "images"
    assets_dst.mkdir(parents=True, exist_ok=True)
    for src_img in (STATIC_SOURCE_DIR / "assets" / "images").glob("*"):
        if src_img.is_file():
            shutil.copy2(src_img, assets_dst / src_img.name)

    # Write index.html and property-data.json to output_dir
    index_html = render_index_html(listing)
    (output_dir / "index.html").write_text(index_html, encoding="utf-8")
    (output_dir / "property-data.json").write_text(
        json.dumps(listing.to_dict(), indent=2), encoding="utf-8"
    )

    return {
        "property_id": listing.property_id,
        "output_dir": str(output_dir.resolve()),
        "verified_asset_count": len(verified_assets),
        "html_bytes": len(index_html.encode("utf-8")),
    }
