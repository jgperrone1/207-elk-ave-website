"""Canonical property catalog for 207 Elk Ave S, Fayetteville, TN.

All facts, spatial counts, and strategic advantages derive from
`references/207 Elk Ave for TWU.pdf` (Pages 1-30) and are generalized for
prospective medical, dental, specialty clinical, behavioral health, outpatient
procedure, and healthcare training tenants.
"""

from __future__ import annotations

from src.elk_ave.models import (
    AdvantagePillar,
    AdvantagePoint,
    ContactProfile,
    FloorSpec,
    GalleryAsset,
    MetricHighlight,
    PropertyListing,
    Provenance,
    SpaceZone,
    TenantArchetype,
    TransformationPair,
)

SOURCE_PDF = "207-elk-ave-s-property-briefing-deck"


def build_property_listing() -> PropertyListing:
    """Return the canonical, generalized property dataset for 207 Elk Ave S."""
    contact = ContactProfile(
        name="Shaz Perrone",
        title="Commercial Real Estate Development",
        role="Principal / Owner",
        entity="207 ELK LLC (207 Elk Ave S)",
        phone_display="",
        phone_uri="",
        email="Shaz.Perrone@gmail.com",
        portrait_image="assets/images/owner-shaz-perrone.jpg",
        credentials_summary=(
            "Commercial real estate principal with a Master of Science in Finance, "
            "backed by a multidisciplinary ownership team rooted in clinical medicine, "
            "healthcare administration, academia, and engineering."
        ),
        provenance=Provenance(
            source_document=SOURCE_PDF,
            source_pages=(2, 18, 29, 30),
            derivation_note="Extracted directly from Owner contact slides and executive summary.",
        ),
    )

    metrics = (
        MetricHighlight(
            id="clinical-rooms",
            value="35+",
            unit_or_label="Plumbed Clinical & Exam Rooms",
            detail="24+ ground-floor private exam suites plus 11 upper-level sink-equipped clinical rooms.",
            category="Clinical Capacity",
            provenance=Provenance(SOURCE_PDF, (16, 20), "Sum of 24+ ground exam rooms and 11 upper clinical rooms."),
        ),
        MetricHighlight(
            id="procedure-suites",
            value="7",
            unit_or_label="Dedicated Procedure Rooms",
            detail="Specialized ground-floor procedure suites plus X-Ray, EKG, Blood Draw, and clinical labs.",
            category="Specialty Care",
            provenance=Provenance(SOURCE_PDF, (16, 20), "Page 20 Point 2 & Page 16 1st Floor Plan."),
        ),
        MetricHighlight(
            id="restrooms-ada",
            value="12",
            unit_or_label="Restrooms & Central Elevator",
            detail="8 ground-floor, 4 second-floor, commercial elevator.",
            category="Accessibility",
            provenance=Provenance(SOURCE_PDF, (14, 16, 22), "Page 22 Point 8 & Page 14 Elevator photo."),
        ),
        MetricHighlight(
            id="dedicated-parking",
            value="~0.5",
            unit_or_label="Acre Dedicated Parking Parcel",
            detail="Private off-street lot directly across Elk Ave S (Tract 2: 0.45 AC) plus on-site ADA parking.",
            category="Parking & Access",
            provenance=Provenance(SOURCE_PDF, (11, 15, 24), "Page 15 Survey Tract 1 (0.39 AC) & Tract 2 (0.45 AC); Page 24 Point 14."),
        ),
        MetricHighlight(
            id="campus-scale",
            value="~20,256 GSF",
            unit_or_label="Total Above-Grade Clinical Footprint",
            detail="Elevator-connected two-story above-grade medical facility (plus basement mechanical/utility level) on a 0.84-acre total downtown campus.",
            category="Campus Scale",
            provenance=Provenance(SOURCE_PDF, (3, 11, 15), "Two-story above-grade building (~20,256 GSF: 1st Floor ~12,874 GSF + 2nd Floor ~7,382 GSF per tax/appraiser records) and 0.84-acre campus."),
        ),
        MetricHighlight(
            id="zoning-campus",
            value="0.84 AC",
            unit_or_label="Downtown Medical Campus (C-1)",
            detail="Two-tract downtown campus (Tract 1: 0.39 AC building parcel + Tract 2: 0.45 AC parking lot) under C-1 commercial zoning.",
            category="Zoning & Campus",
            provenance=Provenance(SOURCE_PDF, (11, 15), "Page 15 Survey Tract 1 (0.39 AC) + Tract 2 (0.45 AC) under C-1 commercial zoning."),
        ),
    )

    floors = (
        FloorSpec(
            level=1,
            name="Ground Level (1st Floor)",
            tagline="High-Density Outpatient Clinical, Diagnostic & Procedure Wing (~12,874 GSF)",
            summary=(
                "Engineered for high-throughput outpatient care with dual waiting rooms, "
                "dedicated check-in/check-out reception, 24+ plumbed exam rooms, 7 procedure suites, "
                "4 nurse workstations, dedicated diagnostic imaging & laboratory infrastructure rooms, and separate exterior access doors."
            ),
            floorplan_image="assets/images/floorplan-level-1.png",
            exam_and_clinical_rooms=24,
            procedure_rooms=7,
            restrooms=8,
            exterior_egress_doors=7,
            elevator_served=True,
            key_features=(
                "24+ private exam rooms with functional wet walls and sinks",
                "7 dedicated procedure rooms (including Med/Peds procedure suite)",
                "Dual waiting lounges: Main Waiting Room + Dedicated Pediatric / Specialty Sub-Waiting",
                "Dedicated Reception, 2 private Intake Offices, and high-density Medical File Room",
                "Dedicated on-site X-Ray suite with adjacent Reading Room and Dressing Room infrastructure (equipment not included)",
                "Dedicated Blood Draw station, Clinical Laboratory room, and EKG infrastructure",
                "4 centralized Nurse Workstations distributed across clinical corridors",
                "8 Ground-Floor Restrooms (ADA-accessible restroom facilities) + central stainless commercial elevator",
            ),
            zones=(
                SpaceZone(
                    id="l1-front-of-house",
                    name="Patient Arrival, Dual Waiting & Intake Suite",
                    floor_level=1,
                    category="Front of House",
                    room_count_label="Lobby + 2 Waiting Rooms + 3 Intake/Admin Rooms",
                    plumbing_equipped=False,
                    highlights=(
                        "Covered main entry vestibule off Elk Ave S with adjacent ADA parking",
                        "Main Waiting Room & separate Pediatric/Sub-Waiting Lounge to isolate patient cohorts",
                        "Dedicated Check-In / Check-Out Reception window, 2 Intake Offices, and secure File Room",
                    ),
                    ideal_uses=(
                        "Multi-provider check-in",
                        "Well-child vs. sick-visit waiting separation",
                        "Spacious patient arrival lobby and intake reception counter",
                    ),
                ),
                SpaceZone(
                    id="l1-clinical-exam",
                    name="Primary & Specialty Exam Pod Corridors",
                    floor_level=1,
                    category="Clinical Exam",
                    room_count_label="24+ Private Exam Suites",
                    plumbing_equipped=True,
                    highlights=(
                        "24+ private exam rooms arranged in efficient double-loaded clinical pods",
                        "Existing cabinetry, sinks, wet-wall plumbing, and medical-grade electrical layouts",
                        "Existing wet-wall plumbing and direct subfloor/basement utility access for streamlined clinical or dental equipment installation.",
                    ),
                    ideal_uses=(
                        "Primary Care & Family Medicine",
                        "Multi-specialty outpatient clinics",
                        "Dental & clinical hygiene operatories",
                    ),
                ),
                SpaceZone(
                    id="l1-procedure-diagnostics",
                    name="Procedure, Imaging & Diagnostic Wing",
                    floor_level=1,
                    category="Procedures & Diagnostics",
                    room_count_label="7 Procedure Suites + Dedicated Diagnostic & Lab Rooms",
                    plumbing_equipped=True,
                    highlights=(
                        "7 specialized procedure rooms along the southern and central clinical wings",
                        "Dedicated X-Ray suite with private Dressing Room and diagnostic Reading Room infrastructure (equipment not included)",
                        "Dedicated Blood Draw station, Clinical Lab room, EKG suite, and Med/Supply closets",
                    ),
                    ideal_uses=(
                        "Outpatient dermatology, aesthetics & clinical procedures",
                        "Urgent care & orthopedic walk-in diagnostics",
                        "On-site phlebotomy and point-of-care testing",
                    ),
                ),
                SpaceZone(
                    id="l1-nurse-support",
                    name="Nurse Stations & Clinical Operations Core",
                    floor_level=1,
                    category="Clinical Support",
                    room_count_label="4 Nurse Stations + 6 Private Physician Offices + 8 Restrooms",
                    plumbing_equipped=True,
                    highlights=(
                        "4 strategically positioned Nurse Workstations and Work Alcoves with sightlines down exam corridors",
                        "6 private physician/provider consultation offices distributed across clinical pods",
                        "Central passenger elevator, 3 interior stairwells, and separate exterior access doors",
                    ),
                    ideal_uses=(
                        "Care team charting & triage",
                        "Provider dictation & telemedicine consults",
                        "Efficient staff circulation and provider consultation",
                    ),
                ),
            ),
            provenance=Provenance(
                source_document=SOURCE_PDF,
                source_pages=(16, 20, 21, 22),
                derivation_note="Derived from 1st Floor architectural plan (p. 16) and clinical infrastructure points 1-9 (pp. 20-22).",
            ),
        ),
        FloorSpec(
            level=2,
            name="Upper Level (2nd Floor)",
            tagline="Behavioral Health, Outpatient Therapy, Executive Offices & Multi-Purpose Wing (~7,382 GSF)",
            summary=(
                "Flexible second-story layout accessible via central commercial elevator and three interior stairwells, "
                "featuring 11 sink-equipped clinical rooms, a built-in laboratory suite (#235), a 576 sq ft "
                "clear-span multi-purpose conference hall (#222), a secondary conference/break lounge, "
                "16+ private behavioral health, therapy, or administrative offices, and 4 dedicated restrooms."
            ),
            floorplan_image="assets/images/floorplan-level-2.png",
            exam_and_clinical_rooms=11,
            procedure_rooms=1,
            restrooms=4,
            exterior_egress_doors=2,
            elevator_served=True,
            key_features=(
                "11 sink-equipped upper-level clinical exam and treatment rooms",
                "Built-in laboratory suite (#235) with existing clinical cabinetry and wet walls",
                "576 sq ft (24 x 24 ft) clear-span Multi-Purpose Conference / Collaboration Hall (#222) plus secondary Conference Lounge",
                "Dedicated upper-floor Waiting Lounge and Reception desk right off the elevator lobby",
                "16+ private executive, behavioral health, counseling, or administrative offices along the perimeter",
                "2 staff kitchens/breakrooms, abundant archive storage, and 4 dedicated restrooms",
            ),
            zones=(
                SpaceZone(
                    id="l2-clinical-lab",
                    name="Upper Clinical & Built-In Laboratory Suite",
                    floor_level=2,
                    category="Clinical & Lab",
                    room_count_label="11 Sink-Equipped Rooms + Lab Suite (#235)",
                    plumbing_equipped=True,
                    highlights=(
                        "11 plumbed exam/clinical rooms ideal for specialty practice or clinical treatment suites",
                        "Built-Out Laboratory (#235) with built-in cabinetry and plumbing",
                        "Dedicated upper Waiting Room and Reception station adjacent to elevator shaft",
                    ),
                    ideal_uses=(
                        "Specialty clinic or independently leased 2nd-floor practice",
                        "Physical/occupational therapy & rehabilitation gym",
                        "Clinical consultation & procedural support",
                    ),
                ),
                SpaceZone(
                    id="l2-conference-training",
                    name="Clear-Span Multi-Purpose Conference & Staff Lounge Core",
                    floor_level=2,
                    category="Conference & Collaboration",
                    room_count_label="576 SF Hall (#222) + Lounge + 2 Kitchens",
                    plumbing_equipped=True,
                    highlights=(
                        "Suite #222 offers a 24 x 24 ft (576 sq ft) clear-span collaboration, boardroom, or group therapy hall",
                        "Expansive 2nd-floor Breakroom / Staff Lounge with natural window light and kitchen cabinetry",
                        "Supports small-group provider meetings & clinical case conferences",
                    ),
                    ideal_uses=(
                        "Small-group provider meetings & clinical case conferences",
                        "Group behavioral therapy or cardiac/pulmonary rehab",
                        "Physician lounge & staff wellness suite",
                    ),
                ),
                SpaceZone(
                    id="l2-executive-behavioral",
                    name="Executive, Behavioral Health & Administrative Wing",
                    floor_level=2,
                    category="Executive & Counseling",
                    room_count_label="16+ Private Perimeter Offices",
                    plumbing_equipped=False,
                    highlights=(
                        "Quiet perimeter wing with 16+ private windowed offices and central storage",
                        "Acoustically separated from ground-floor acute clinical traffic",
                        "Direct stairwell and central elevator connectivity",
                    ),
                    ideal_uses=(
                        "Outpatient behavioral health, psychiatry & counseling suites",
                        "Healthcare administration, billing & telehealth hub",
                        "Multi-disciplinary medical group headquarters",
                    ),
                ),
            ),
            provenance=Provenance(
                source_document=SOURCE_PDF,
                source_pages=(10, 16, 20, 21, 22),
                derivation_note="Derived from 2nd Floor architectural plan (p. 16), Breakroom slide (p. 10), and points 1, 3, 4, 8 (pp. 20-22).",
            ),
        ),
    )

    transformations = (
        TransformationPair(
            id="exterior-facade",
            title="Architectural Exterior & Street Presence",
            subtitle="207 Elk Ave S — Historic Brick Character Meets Modern Medical Identity",
            category="Exterior",
            before_label="Current Clinical Exterior",
            before_image="assets/images/exterior-original.jpg",
            after_label="Renovated Architectural Concept",
            after_image="assets/images/exterior_wellness_no_cafe.png",
            alt_image="assets/images/aerial-front-facade.jpg",
            alt_label="Aerial Campus Perspective",
            description=(
                "Positioned one block off Fayetteville's historic Town Square, the building combines "
                "classic two-story masonry architecture with a single-story clinical wing, storefront glass, "
                "and immediate curbside and off-street patient parking."
            ),
            clinical_value=(
                "High-visibility corner presence at Elk Ave S & Campbell St E with custom tenant signage "
                "opportunities and zero structural demolition required."
            ),
            provenance=Provenance(SOURCE_PDF, (4, 5, 11, 17), "Pages 4 & 5 Original vs Renovated exterior."),
        ),
        TransformationPair(
            id="waiting-lounge",
            title="Primary Patient Waiting Lounge",
            subtitle="High-Capacity Patient Seating with Warm Acoustic Finishes",
            category="Waiting Lounge",
            before_label="Existing Waiting Room",
            before_image="assets/images/waiting-room-original.jpg",
            after_label="Modernized Lounge Concept",
            after_image="assets/images/Gemini_No_Cafe.jpeg",
            alt_image="assets/images/practice-pediatric-waiting.jpg",
            alt_label="Secondary / Pediatric Waiting Room",
            description=(
                "Supported by decorative architectural columns and generous ceiling heights, the primary "
                "waiting room accommodates large patient volumes while a separate secondary waiting room "
                "allows dedicated pediatric, urgent care, or specialty cohort separation."
            ),
            clinical_value=(
                "Dual waiting areas (Waiting 1 & Waiting 2) prevent cross-traffic between sick visits, "
                "elective procedures, and specialty consultations."
            ),
            provenance=Provenance(SOURCE_PDF, (7, 13, 14, 21), "Page 7 Waiting Room Original vs Renovated & Page 21 Point 5."),
        ),
        TransformationPair(
            id="exam-procedure-suite",
            title="Private Exam & Specialty Procedure Suites",
            subtitle="35+ Plumbed Clinical Rooms Ready for Streamlined Finish Customization",
            category="Exam & Procedure",
            before_label="Existing Plumbed Exam Room",
            before_image="assets/images/exam-room-original.jpg",
            after_label="Renovated Clinical Suite",
            after_image="assets/images/exam-room-renovated.jpg",
            alt_image="assets/images/exam-room-procedure-derm.jpg",
            alt_label="Specialty Derm / Procedure Setup",
            description=(
                "Every exam and procedure room features intact partition walls, solid-core doors, "
                "wet-wall plumbing with sinks, and medical-grade electrical distribution—upgradable "
                "with luxury vinyl plank flooring and custom millwork."
            ),
            clinical_value=(
                "Intact wet walls and clinical infrastructure allow rapid fixture connection "
                "and customization without extensive structural alterations."
            ),
            provenance=Provenance(SOURCE_PDF, (8, 20, 21, 22), "Page 8 Exam Room Original, Renovated & Derm Exam Room."),
        ),
        TransformationPair(
            id="nurses-station",
            title="Centralized Nurse Workstations & Triage Hubs",
            subtitle="4 Ground-Floor Stations Engineered for Care Team Efficiency",
            category="Clinical Core",
            before_label="Existing Nurse Station",
            before_image="assets/images/nurses-station-original.jpg",
            after_label="Renovated Triage & Charting Hub",
            after_image="assets/images/nurses-station-renovated.jpg",
            alt_image="assets/images/practice-clinical-corridor-station.jpg",
            alt_label="Corridor Care Team Station",
            description=(
                "Wrap-around counters, overhead cabinetry, natural daylight windows, and multi-terminal "
                "data/power drops position clinical support staff at the heart of each exam pod."
            ),
            clinical_value=(
                "Minimizes clinician footsteps per patient encounter and supports team-based care coordination."
            ),
            provenance=Provenance(SOURCE_PDF, (9, 13, 20), "Page 9 Nurses Station Original vs Renovated."),
        ),
        TransformationPair(
            id="upper-breakroom-conference",
            title="2nd Floor Conference, Lounge & Collaboration Suite",
            subtitle="Clear-Span Collaboration Space for Providers, Staff & Clinical Teams",
            category="Executive & Conference",
            before_label="Existing 2nd Floor Space",
            before_image="assets/images/breakroom-2nd-floor-original.jpg",
            after_label="Renovated Conference & Lounge",
            after_image="assets/images/breakroom-2nd-floor-renovated.jpg",
            alt_image="assets/images/practice-multipurpose-room.jpg",
            alt_label="Additional Multi-Purpose Room",
            description=(
                "Generous clear-span dimensions and perimeter windows on the second floor create "
                "an inviting setting for staff dining, provider board meetings, telehealth operations, "
                "or multidisciplinary clinical case conferences."
            ),
            clinical_value=(
                "Supports staff retention, multi-disciplinary case reviews, and professional clinical "
                "collaboration under the same roof."
            ),
            provenance=Provenance(SOURCE_PDF, (10, 12, 21), "Page 10 2nd Floor Breakroom Original vs Renovated & Page 21 Point 4."),
        ),
    )

    archetypes = (
        TenantArchetype(
            id="multi-specialty-outpatient",
            specialty="Primary Care & Multi-Specialty Medical Group",
            icon_name="stethoscope",
            headline="Built-Out Outpatient Clinic with Proven Community Heritage",
            recommended_configuration="Ground Floor (~12,874 GSF) or Full ~20,256 GSF Two-Story Campus",
            target_rooms=24,
            why_it_fits=(
                "Known throughout Lincoln County as a trusted primary care destination (formerly HH Lincoln Health Primary Care), offering immediate patient recognition.",
                "24+ ground-floor exam rooms, 7 procedure rooms, and 4 nurse stations allow 6 to 10+ providers to run concurrent schedules without bottlenecks.",
                "Minutes from Lincoln Medical Center for seamless hospitalist, imaging, and specialist referrals.",
            ),
            infrastructure_match=(
                "Dual waiting rooms (Main + Pediatric/Sub-Waiting)",
                "Dedicated diagnostic rooms: X-Ray suite, Reading Room, EKG, Blood Draw & Lab",
                "Dedicated ~0.5-acre parking lot across the street + curbside ADA spaces",
            ),
            provenance=Provenance(SOURCE_PDF, (4, 16, 20, 25, 26), "Generalized from clinical density and healthcare heritage points."),
        ),
        TenantArchetype(
            id="urgent-care-diagnostics",
            specialty="Urgent Care, Orthopedic Walk-In & Occupational Medicine",
            icon_name="activity",
            headline="Rapid Patient Triage with Dedicated Diagnostic Rooms, Procedure Suites & Separate Access Doors",
            recommended_configuration="Ground Floor (Full or Phased Wing)",
            target_rooms=16,
            why_it_fits=(
                "Dedicated X-Ray suite with adjacent Reading Room and Dressing Room infrastructure eliminates expensive radiology vault construction (equipment not included).",
                "7 dedicated procedure rooms support laceration repair, splinting/casting, IV hydration, and occupational drug testing.",
                "Dedicated ground-floor entry/exit doors allow separate ambulance/stretcher transfer or contagious-symptom isolation pathways.",
            ),
            infrastructure_match=(
                "Dedicated diagnostic rooms: X-Ray suite, Phlebotomy Blood Draw & Clinical Lab infrastructure",
                "7 procedure suites + 4 centralized nurse triage stations",
                "Direct access off Elk Ave S in downtown Fayetteville",
            ),
            provenance=Provenance(SOURCE_PDF, (16, 20, 21, 22), "Derived from 1st floor plan diagnostics & egress specs."),
        ),
        TenantArchetype(
            id="dental-oral-health",
            specialty="Dental & Hygiene Clinic",
            icon_name="smile",
            headline="Built-Out Plumbed Operatories for Rapid Practice Launch",
            recommended_configuration="Ground Floor, Upper Floor, or Multi-Level Clinic",
            target_rooms=18,
            why_it_fits=(
                "Existing wet walls and in-place clinical plumbing allow dental chairs, water lines, and clinical utilities to connect efficiently.",
                "Dual waiting rooms and separate intake/check-out windows keep high-turnover hygiene patients separated from private treatment consultations.",
                "Built-in sterilization/lab suites on both floors (#235 on Level 2 plus Ground Floor Lab) streamline instrument processing.",
            ),
            infrastructure_match=(
                "Existing clinical plumbing + 35+ plumbed rooms across both levels",
                "Sterilization & laboratory cabinetry already installed",
                "High-capacity ~0.5-acre parking lot for patient and staff vehicles",
            ),
            provenance=Provenance(SOURCE_PDF, (19, 20, 21, 26), "Generalized from dental hygiene & plumbing points 2, 3, 5, 6."),
        ),
        TenantArchetype(
            id="dermatology-aesthetics",
            specialty="Dermatology, Aesthetics & MedSpa",
            icon_name="sparkles",
            headline="Elevated Hospitality Arrival Paired with Dedicated Procedure & Laser Suites",
            recommended_configuration="Ground Floor or Custom Phased Suite",
            target_rooms=14,
            why_it_fits=(
                "7 specialized ground-floor procedure rooms accommodate skin examinations, aesthetic treatments, and laser/energy devices.",
                "Front lobby and waiting lounge easily accommodate an upscale patient arrival desk and dedicated clinical consultation suites.",
                "Walkable historic downtown square location attracts affluent regional patients across the Huntsville–Fayetteville corridor.",
            ),
            infrastructure_match=(
                "Procedure suites with medical-grade electrical & wet walls",
                "Dedicated patient arrival reception with separate private check-out",
                "24+ exam rooms for simultaneous medical and cosmetic tracks",
            ),
            provenance=Provenance(SOURCE_PDF, (5, 6, 7, 8, 20, 24, 25), "Derived from Derm Exam Room rendering (p. 8) and Wellness Cafe concepts (pp. 5-7)."),
        ),
        TenantArchetype(
            id="rehab-physical-therapy",
            specialty="Physical, Occupational & Pediatric Rehabilitation",
            icon_name="heart-pulse",
            headline="Accessible Multi-Suite Layout for Adult Mobility & Pediatric Developmental Therapy",
            recommended_configuration="Ground Floor Wing or Upper Level Clinical Suite",
            target_rooms=12,
            why_it_fits=(
                "Accessible campus with 12 restrooms (including ADA-accessible restroom facilities), accessible ground-level entries, wide clinical corridors, and a central commercial passenger elevator.",
                "576 sq ft clear-span room (#222) plus multi-purpose rooms support open therapeutic exercise, balance training, and ADL simulation.",
                "Private plumbed exam rooms accommodate 1-on-1 manual therapy, speech/swallow therapy, and pediatric sensory fieldwork.",
            ),
            infrastructure_match=(
                "Central stainless elevator + ground-level access doors",
                "576 sq ft clear-span suite + private treatment rooms",
                "Dedicated Pediatric Waiting Room with built-in aquarium window",
            ),
            provenance=Provenance(SOURCE_PDF, (13, 14, 16, 21, 22, 27), "Generalized from ADA, clear-span, and occupational therapy points 4, 8, 9, 22."),
        ),
        TenantArchetype(
            id="behavioral-health",
            specialty="Behavioral Health, Psychiatry & Counseling Center",
            icon_name="brain",
            headline="Private Consultation Offices, Group Therapy Halls & Discreet Patient Flow",
            recommended_configuration="Upper Level (~7,382 GSF) or Integrated Multi-Floor Suite",
            target_rooms=16,
            why_it_fits=(
                "Second floor provides 16+ private windowed consultation offices plus 11 clinical rooms for medication management and psychiatric evaluations.",
                "Two large conference/group rooms on Level 2 support intensive outpatient programs (IOP), family counseling, and clinical supervision.",
                "Multiple exterior doors and dual waiting areas enable discreet patient arrival and departure.",
            ),
            infrastructure_match=(
                "16+ private perimeter offices + 11 upper clinical rooms",
                "2 group therapy / conference halls + 2 staff kitchens",
                "Dedicated exterior access doors for private patient circulation",
            ),
            provenance=Provenance(SOURCE_PDF, (16, 20, 21, 23, 27), "Generalized from 2nd floor plan and behavioral health vision point 23."),
        ),
        TenantArchetype(
            id="academic-health-sciences",
            specialty="Healthcare Administration, Executive & Telehealth Center",
            icon_name="briefcase",
            headline="Dedicated Clinical Management, Telehealth Hub & Private Practice Suites",
            recommended_configuration="Upper Level (~7,382 GSF), Ground Level, or Combined Suites",
            target_rooms=16,
            why_it_fits=(
                "Upper suite #222 provides a 576 sq ft clear-span multi-purpose room alongside built-in lab suite #235 and 11 sink-equipped clinical rooms.",
                "16+ private windowed offices create a quiet, dedicated environment for healthcare administration, billing, clinical telehealth, and behavioral therapy.",
                "Separation of ground-floor acute care and second-floor administrative suites supports efficient provider workflow and compliant low-density outpatient operations.",
            ),
            infrastructure_match=(
                "16+ private executive & administrative offices",
                "576 sq ft clear-span multi-purpose conference suite + built-in lab",
                "Approx. 0.5-acre dedicated parking parcel directly across Elk Ave S",
            ),
            provenance=Provenance(SOURCE_PDF, (18, 19, 20, 21, 22, 23, 24, 26), "Derived from points 1-12 and 19-23."),
        ),
    )

    pillars = (
        AdvantagePillar(
            id="turnkey-clinical",
            title="Existing Clinical Infrastructure & Speed to Market",
            subtitle="Bypass Protracted Redesign Cycles & Open on Schedule",
            summary=(
                "Intact clinical partition walls, solid-core doors, medical-grade electrical layouts, "
                "wet-wall plumbing in 35+ rooms, and dual waiting suites eliminate 12 to 18 months of "
                "architectural reconstruction."
            ),
            points=(
                AdvantagePoint(
                    number=1,
                    title="Multi-Level Selection Flexibility",
                    description="Total footprint flexibility to lease the ground floor (~12,874 GSF), upper level (~7,382 GSF), or the full ~20,256 GSF two-story above-grade campus tailored to exact square footage and clinical program needs.",
                    pillar_id="turnkey-clinical",
                    provenance=Provenance(SOURCE_PDF, (20,), "Point 1 generalized for all medical tenants."),
                ),
                AdvantagePoint(
                    number=2,
                    title="Existing Ground-Floor Clinical Density",
                    description="24+ private ground-floor exam rooms, 7 specialized procedure rooms, dedicated diagnostic imaging (X-Ray) and laboratory infrastructure rooms, and 4 central nurse stations—all with functional wet walls and sinks.",
                    pillar_id="turnkey-clinical",
                    provenance=Provenance(SOURCE_PDF, (16, 20), "Point 2 & 1st Floor Plan."),
                ),
                AdvantagePoint(
                    number=3,
                    title="Built-Out Upper-Floor Clinical, Lab & Executive Layout",
                    description="11 sink-equipped second-floor clinical rooms, a built-in laboratory with cabinetry (#235), 16+ private perimeter offices, and 4 dedicated restrooms.",
                    pillar_id="turnkey-clinical",
                    provenance=Provenance(SOURCE_PDF, (16, 20), "Point 3 & 2nd Floor Plan."),
                ),
                AdvantagePoint(
                    number=4,
                    title="Dedicated Clear-Span Conference & Collaboration Space",
                    description="Upper suite #222 provides a 24 x 24 ft (576 sq ft) clear-span hall—plus a secondary conference/break lounge—ideal for provider meetings, patient education, rehab, or clinical case conferences.",
                    pillar_id="turnkey-clinical",
                    provenance=Provenance(SOURCE_PDF, (10, 16, 21), "Point 4 generalized."),
                ),
                AdvantagePoint(
                    number=5,
                    title="Built-Out Patient Reception & Dual Waiting Suites",
                    description="Fully built-out front-of-house featuring a main lobby, dual waiting rooms (Main Waiting & Pediatric/Specialty Sub-Waiting), dedicated check-in/out reception, two intake offices, and a high-density file room.",
                    pillar_id="turnkey-clinical",
                    provenance=Provenance(SOURCE_PDF, (16, 21), "Point 5 generalized."),
                ),
                AdvantagePoint(
                    number=6,
                    title="Accelerated Speed to Market",
                    description="Intact clinical partitions, solid-core doors, drop ceilings, medical electrical distribution, and extensive plumbing allow tenants to bypass protracted construction cycles and launch on schedule.",
                    pillar_id="turnkey-clinical",
                    provenance=Provenance(SOURCE_PDF, (22,), "Point 7 generalized."),
                ),
                AdvantagePoint(
                    number=7,
                    title="Comprehensive Restroom & Central Commercial Elevator",
                    description="12 total restrooms across both floors (8 on Ground, 4 on Upper Level) with ADA-accessible restroom facilities and central commercial elevator access, ensuring adequate fixture capacity for patients and staff.",
                    pillar_id="turnkey-clinical",
                    provenance=Provenance(SOURCE_PDF, (14, 22), "Point 8."),
                ),
            ),
        ),
        AdvantagePillar(
            id="parking-location",
            title="Unmatched Parking, Downtown Walkability & Regional Reach",
            subtitle="Dedicated ~0.5-Acre Parking Lot + Regional Highway Crossroads",
            summary=(
                "Rare downtown medical campus combining immediate walkability to Fayetteville's historic "
                "Town Square with a dedicated half-acre private parking parcel directly across Elk Ave S."
            ),
            points=(
                AdvantagePoint(
                    number=8,
                    title="Immediate Proximity to Historic Downtown Square",
                    description="Situated as the premier commercial medical building directly behind Fayetteville's historic downtown square, offering providers, staff, and patients walkable access to dining, pharmacies, and civic amenities.",
                    pillar_id="parking-location",
                    provenance=Provenance(SOURCE_PDF, (3, 11, 24), "Point 13."),
                ),
                AdvantagePoint(
                    number=9,
                    title="Dedicated ~0.5-Acre Private Parking Lot Across the Street",
                    description="In addition to curbside and on-site building parking (Tract 1: 0.39 AC), ownership provides a dedicated 0.45-acre (~0.5 AC) paved parking parcel directly across Elk Ave S (Tract 2), eliminating parking constraints.",
                    pillar_id="parking-location",
                    provenance=Provenance(SOURCE_PDF, (11, 15, 24), "Point 14 & Page 15 Survey."),
                ),
                AdvantagePoint(
                    number=10,
                    title="Geographic Core for a Multi-County Regional Catchment",
                    description="Centrally situated in Lincoln County along the US-64 / US-231 / US-431 crossroads to draw patients and clinical staff seamlessly across Lincoln, Moore, Giles, Franklin, Coffee, and Bedford counties.",
                    pillar_id="parking-location",
                    provenance=Provenance(SOURCE_PDF, (24,), "Point 15 generalized."),
                ),
                AdvantagePoint(
                    number=11,
                    title="Proximity to HH Lincoln Medical Center",
                    description="Located minutes from Lincoln Medical Center (Huntsville Hospital Health System), facilitating seamless physician hospital privileges, diagnostic coordination, and regional referral networks.",
                    pillar_id="parking-location",
                    provenance=Provenance(SOURCE_PDF, (25,), "Point 17 generalized."),
                ),
                AdvantagePoint(
                    number=12,
                    title="Positioned in the High-Growth Huntsville / Rocket City Corridor",
                    description="Located directly north of the booming Huntsville, AL metro corridor, capturing rapid cross-border residential growth and accelerating demand for accessible outpatient specialty care.",
                    pillar_id="parking-location",
                    provenance=Provenance(SOURCE_PDF, (18, 25), "Point 18 & Executive Summary."),
                ),
            ),
        ),
        AdvantagePillar(
            id="partnership-vision",
            title="Healthcare Heritage & Ownership Partnership",
            subtitle="Flexible Lease Structures Backed by Ownership",
            summary=(
                "Formerly home to HH Lincoln Health Primary Care, 207 Elk Ave S benefits from established "
                "recognition and familiarity by the community, backed by an ownership team committed to long-term tenant success."
            ),
            points=(
                AdvantagePoint(
                    number=13,
                    title="Established Community Healthcare Heritage",
                    description="Recognized throughout Lincoln County as an established medical facility, providing new tenants with immediate local awareness, patient familiarity, and organic community recognition.",
                    pillar_id="partnership-vision",
                    provenance=Provenance(SOURCE_PDF, (4, 12, 13, 14, 26), "Point 19 generalized."),
                ),
                AdvantagePoint(
                    number=14,
                    title="Multi-Specialty & Interprofessional Campus Synergy",
                    description="Substantial clinical capacity across two floors allows a single anchor health system or complementary co-tenants (primary care, dental, rehab, behavioral health, diagnostics) to cross-refer on site.",
                    pillar_id="partnership-vision",
                    provenance=Provenance(SOURCE_PDF, (26, 27), "Points 20-23 generalized."),
                ),
                AdvantagePoint(
                    number=15,
                    title="Assistance Seeking Local Incentives",
                    description="Ownership provides assistance to tenants seeking applicable local municipal programs and downtown revitalization incentives.",
                    pillar_id="partnership-vision",
                    provenance=Provenance(SOURCE_PDF, (28,), "Point 24 generalized."),
                ),
                AdvantagePoint(
                    number=16,
                    title="Flexible Expansion Horizon & Custom Lease Frameworks",
                    description="Cooperative lease structures (Base Rent + pro-rata building expense share / NNN pass-throughs) with expansion options across two floors—supported by an ownership team rooted in finance, medicine, and engineering.",
                    pillar_id="partnership-vision",
                    provenance=Provenance(SOURCE_PDF, (18, 28, 29), "Points 25-28 generalized."),
                ),
            ),
        ),
    )

    gallery = (
        GalleryAsset(
            id="gal-ext-renovated",
            title="Renovated Exterior Architectural Rendering",
            caption="Modernized brick & dark architectural bronze facade along Elk Ave S (illustrative visualization).",
            category="Exterior & Aerial",
            image_path="assets/images/exterior_wellness_no_cafe.png",
            provenance=Provenance(SOURCE_PDF, (5, 17), "Page 5 Renovated Exterior."),
            is_conceptual=True,
        ),
        GalleryAsset(
            id="gal-ext-original",
            title="Current Street-Level Exterior (207 Elk Ave S)",
            caption="Existing two-story brick & clinical wing facade with curbside and side-lot ADA parking.",
            category="Exterior & Aerial",
            image_path="assets/images/exterior-original.jpg",
            provenance=Provenance(SOURCE_PDF, (4,), "Page 4 Original Exterior."),
            is_conceptual=False,
        ),
        GalleryAsset(
            id="gal-aerial-front",
            title="Drone View — Elk Ave S Frontage & ADA Parking",
            caption="Oblique aerial showing main entrance, side ADA parking lot, and covered drive-under bay.",
            category="Exterior & Aerial",
            image_path="assets/images/aerial-front-facade.jpg",
            provenance=Provenance(SOURCE_PDF, (11,), "Page 11 Aerial View 1."),
            is_conceptual=False,
        ),
        GalleryAsset(
            id="gal-aerial-campus",
            title="Drone View — Full Medical Building Footprint",
            caption="Overview of the two-story brick core and single-story clinical exam wing.",
            category="Exterior & Aerial",
            image_path="assets/images/aerial-campus-oblique.jpg",
            provenance=Provenance(SOURCE_PDF, (11,), "Page 11 Aerial View 2."),
            is_conceptual=False,
        ),
        GalleryAsset(
            id="gal-aerial-parking-pin",
            title="Dedicated ~0.5-Acre Parking Parcel Across Elk Ave S",
            caption="Private off-street parking lot (Tract 2: 0.45 AC) directly across the street for patients and staff.",
            category="Exterior & Aerial",
            image_path="assets/images/aerial-parking-parcel-pin.jpg",
            provenance=Provenance(SOURCE_PDF, (11,), "Page 11 Aerial View 3."),
            is_conceptual=False,
        ),
        GalleryAsset(
            id="gal-aerial-building-boundary",
            title="Tract 1 Building Parcel Boundary (0.39 Acres)",
            caption="Overhead boundary view of the medical building and on-site parking apron.",
            category="Exterior & Aerial",
            image_path="assets/images/aerial-building-boundary.jpg",
            provenance=Provenance(SOURCE_PDF, (11,), "Page 11 Aerial View 5."),
            is_conceptual=False,
        ),
        GalleryAsset(
            id="gal-aerial-parking-boundary",
            title="Tract 2 Dedicated Parking Lot Boundary (0.45 Acres)",
            caption="Overhead boundary view of the dedicated parking parcel directly across Elk Ave S.",
            category="Exterior & Aerial",
            image_path="assets/images/aerial-parking-lot-boundary.jpg",
            provenance=Provenance(SOURCE_PDF, (11,), "Page 11 Aerial View 6."),
            is_conceptual=False,
        ),
        GalleryAsset(
            id="gal-exam-renovated",
            title="Renovated Private Exam Suite",
            caption="Plumbed clinical exam room with wood-tone flooring, custom cabinetry, and wet-wall sink (conceptual rendering).",
            category="Clinical Interiors",
            image_path="assets/images/exam-room-renovated.jpg",
            provenance=Provenance(SOURCE_PDF, (8,), "Page 8 Exam Room Renovated."),
            is_conceptual=True,
        ),
        GalleryAsset(
            id="gal-exam-derm",
            title="Specialty Procedure & Dermatology Suite",
            caption="Renovation rendering showing procedure room configuration with clinical procedure lighting, power exam chair, and laser/device cart (not actual existing condition).",
            category="Clinical Interiors",
            image_path="assets/images/exam-room-procedure-derm.jpg",
            provenance=Provenance(SOURCE_PDF, (8,), "Page 8 Derm Exam Room."),
            is_conceptual=True,
        ),
        GalleryAsset(
            id="gal-nurses-renovated",
            title="Renovated Central Nurse Workstation",
            caption="Modernized care-team triage and charting station with natural window daylight (conceptual rendering).",
            category="Clinical Interiors",
            image_path="assets/images/nurses-station-renovated.jpg",
            provenance=Provenance(SOURCE_PDF, (9,), "Page 9 Nurses Station Renovated."),
            is_conceptual=True,
        ),
        GalleryAsset(
            id="gal-elevator",
            title="Central Commercial Stainless Elevator Lobby",
            caption="Commercial stainless passenger elevator connecting Ground Level and 2nd Floor clinical wings.",
            category="Clinical Interiors",
            image_path="assets/images/practice-central-elevator.jpg",
            provenance=Provenance(SOURCE_PDF, (14,), "Page 14 Elevator Lobby."),
            is_conceptual=False,
        ),
        GalleryAsset(
            id="gal-waiting-renovated",
            title="Hospitality-Inspired Patient Waiting Lounge",
            caption="Warm biophilic waiting room visualization with wood flooring and comfortable seating (conceptual rendering).",
            category="Lobby & Waiting",
            image_path="assets/images/Gemini_No_Cafe.jpeg",
            provenance=Provenance(SOURCE_PDF, (7,), "Page 7 Waiting Room Renovated."),
            is_conceptual=True,
        ),
        GalleryAsset(
            id="gal-main-waiting",
            title="Existing Primary Waiting Room & Brick Archway",
            caption="Spacious ground-floor waiting lounge with direct sightlines to reception and sub-waiting.",
            category="Lobby & Waiting",
            image_path="assets/images/practice-main-waiting-archway.jpg",
            provenance=Provenance(SOURCE_PDF, (14,), "Page 14 Main Waiting Room."),
            is_conceptual=False,
        ),
        GalleryAsset(
            id="gal-peds-waiting",
            title="Second Floor Waiting Room",
            caption="Bright, comfortable second-floor waiting lounge featuring natural window light and direct elevator lobby access for patients and visitors.",
            category="Lobby & Waiting",
            image_path="assets/images/practice-pediatric-waiting.jpg",
            provenance=Provenance(SOURCE_PDF, (13,), "Page 13 Pediatric Waiting Room."),
            is_conceptual=False,
        ),
        GalleryAsset(
            id="gal-breakroom-renovated",
            title="2nd Floor Executive Conference & Staff Lounge",
            caption="Clear-span 2nd floor lounge with full cabinetry, conference table, and presentation screen (conceptual rendering).",
            category="Executive & Administrative",
            image_path="assets/images/breakroom-2nd-floor-renovated.jpg",
            provenance=Provenance(SOURCE_PDF, (10,), "Page 10 2nd Floor Breakroom Renovated."),
            is_conceptual=True,
        ),
        GalleryAsset(
            id="gal-exec-office-furnished",
            title="Executive Office Suite",
            caption="Private executive office suite at 207 Elk Ave S featuring rich hardwood cabinetry, executive workstation desk, natural daylight window, and quiet administrative ambiance (shown furnished for illustration; furnishings not included).",
            category="Executive & Administrative",
            image_path="assets/images/executive-office-furnished.jpg",
            provenance=Provenance(SOURCE_PDF, (10, 13), "Actual property interior photograph."),
            is_conceptual=False,
        ),
        GalleryAsset(
            id="gal-admin-office",
            title="Business & Intake Office Suite",
            caption="Multi-workstation administrative and patient billing office with pass-through window.",
            category="Executive & Administrative",
            image_path="assets/images/practice-intake-business-office.jpg",
            provenance=Provenance(SOURCE_PDF, (13,), "Page 13 Intake/Business Office."),
            is_conceptual=False,
        ),
        GalleryAsset(
            id="gal-town-square",
            title="Historic Downtown Fayetteville Town Square (1 Block Away)",
            caption="Walkable historic courthouse square immediately adjacent to 207 Elk Ave S.",
            category="Downtown & Community",
            image_path="assets/images/downtown-town-square-aerial.jpg",
            provenance=Provenance(SOURCE_PDF, (3,), "Page 3 Town Square."),
            is_conceptual=False,
        ),
        GalleryAsset(
            id="gal-main-ave",
            title="Downtown Fayetteville Main Avenue Streetscape",
            caption="Vibrant local dining, retail, and historic architecture steps from the medical campus.",
            category="Downtown & Community",
            image_path="assets/images/downtown-main-ave.jpg",
            provenance=Provenance(SOURCE_PDF, (3,), "Page 3 Main Ave."),
            is_conceptual=False,
        ),
        GalleryAsset(
            id="gal-survey-tracts",
            title="Boundary Survey — Tract 1 (0.39 AC) & Tract 2 (0.45 AC)",
            caption="Certified boundary survey showing the building parcel and dedicated parking lot across Elk Ave S.",
            category="Floorplans & Surveys",
            image_path="assets/images/survey-two-tracts.png",
            provenance=Provenance(SOURCE_PDF, (15,), "Page 15 2-Tract Survey."),
            is_conceptual=False,
        ),
    )

    return PropertyListing(
        property_id="207-elk-ave-s",
        headline="Medical & Executive Office Campus in Historic Downtown Fayetteville",
        subheadline=(
            "35+ plumbed clinical & exam suites, 7 procedure rooms, on-site diagnostic & lab infrastructure, "
            "and a dedicated ~0.5-acre parking lot—engineered for streamlined multi-specialty outpatient clinics "
            "and healthcare practices."
        ),
        street_address="207 Elk Ave S",
        campus_alias="207 Elk Ave S Medical Campus",
        city="Fayetteville",
        state="TN",
        postal_code="37334",
        county="Lincoln County",
        occupancy_classification="Outpatient Medical & Executive Office",
        building_lot_acres=0.39,
        parking_lot_acres=0.45,
        total_campus_acres=0.84,
        executive_summary=(
            "Securing built-out clinical space in Southern Middle Tennessee and the North Huntsville growth "
            "corridor—without incurring $150 to $250+ per square foot in speculative shell build-out costs "
            "or 18-month architectural delays—is one of the greatest challenges facing expanding medical groups.",
            "207 Elk Ave S (formerly HH Lincoln Health Primary Care) delivers a capital-efficient, "
            "spatially versatile clinical facility for multi-specialty outpatient clinics and healthcare practices.",
            "Backed by 35+ sink-equipped clinical rooms across two elevator-served floors (~20,256 GSF above-grade), 7 procedure suites, "
            "dedicated diagnostic and laboratory infrastructure rooms, 12 restrooms (with ADA-accessible facilities), and a dedicated ~0.5-acre private parking lot "
            "directly across the street, 207 Elk Ave S provides unmatched speed to market and long-term operational stability.",
        ),
        metrics=metrics,
        floors=floors,
        transformations=transformations,
        archetypes=archetypes,
        pillars=pillars,
        gallery=gallery,
        contact=contact,
        metadata={
            "corridor": "Huntsville / Rocket City North Growth Corridor (US-231 / US-64 / US-431)",
            "nearby_hospital": "HH Lincoln Medical Center (Minutes Away)",
            "catchment_counties": ["Lincoln", "Moore", "Giles", "Franklin", "Coffee", "Bedford", "Madison (AL)"],
            "lease_structures": [
                "Ground Floor Clinical Wing (~12,874 GSF)",
                "Upper Level Specialty / Executive Wing (~7,382 GSF)",
                "Phased Multi-Floor Custom Suite",
                "Full Two-Story Campus (~20,256 GSF)",
            ],
        },
    )
