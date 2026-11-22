# Osdag_Internship
# OsdagBridge

OsdagBridge is a desktop structural engineering plugin for Osdag focused on the analysis and design of short-span steel plate-girder bridges in accordance with Indian Roads Congress (IRC) and IS 800 standards. Built on Python, PySide6, OpenSeesPy, and `ospgrillage`, it provides parametric 2D/3D CAD visualization, automated grillage modeling, load placement, and structural verification.

---

## Key Enhancements Implemented

### 1. Interactive 2D CAD Parameter Editing (Task I)
- **Inline Dimension Editing:** Double-clicking editable dimension labels in the 2D CAD views spawns a pre-filled `QLineEdit` overlay directly over the label:
  - **Cross-Section View (`cad_cross_section.py`):** `Carriageway Width`, `Girder Spacing`, and `Deck Thickness`
  - **Top/Plan View (`cad_top_view.py`):** `Span Length`
- **Locked Derived Parameters:** `Overhang`, `Overall Bridge Width`, and `Bracing Spacing` are locked against direct edits and dynamically recompute upon redraw.
- **Validation & Sync:** Committing via `Enter` or focus-out (with an idempotent commit guard) validates inputs through `BridgeInputValidator`, updates the main UI input dock and dictionaries (`KEY_*` from `common.py`), and triggers an immediate CAD redraw. Pressing `Esc` cancels without modifying state.

### 2. Additional Inputs Validation & Unsaved Changes Guard (Task II)
- **Pre-Save Custom Validation (`additional_inputs.py`):** Intercepts the **Save** action across all tabs using central `KEY_*` mappings (`CUSTOM_FIELD_SPECS`). If any dropdown/selector is set to `Custom` while its paired input field is empty, saving is halted and `CustomMessageBox` displays:
  > `Error: The custom value for '[Parameter Name]' cannot be empty.`
- **Dirty Tracking & Close Confirmation:** Tracks user edits across `QLineEdit`, `QComboBox`, and `QCheckBox` controls (`self.is_modified`, suppressed during programmatic population and reset after a successful save). Closing the dialog with unsaved edits triggers a warning dialog (`Discard` / `Cancel`):
  > `You have unsaved changes. Closing this window will discard them. Do you want to proceed?`

### 3. Transverse Member Result Extraction & Plotting (Task III)
- **Grillage Element Partitioning (`results_data.py`):** Added `get_transverse_member_groups()` and `extract_transverse_member_response()` to extract real `ospgrillage` transverse element groups (`start_edge` + `end_edge` as **End Diaphragms**, and `transverse_slab` as **Intermediate Cross Bracings**) strictly disjoint from `longitudinal_members`.
- **2D Results Plotting (`graph_engine.py`, `girder_2d_plots.py`, `steel_design_analysis.py`):** Extended the member selection dropdowns with `End Diaphragms` and `Intermediate Cross Bracings`, supporting all 9 force and displacement components (`Fx`, `Vy`, `Vz`, `Tx`, `My`, `Mz`, `Dx`, `Dy`, `Dz`) across load cases along the transverse direction.

---

## Project Structure

```text
OsdagBridge/
├── docs/
│   ├── DISCOVERY.md                  # Phase 0 architecture and widget discovery notes
│   └── REPORT.md                     # Detailed implementation report for Tasks I–III
├── src/
│   ├── osdagbridge/
│   │   ├── core/
│   │   │   ├── bridge_types/plate_girder/
│   │   │   │   ├── graph_engine.py   # Data extraction & Matplotlib rendering engine
│   │   │   │   ├── results_data.py   # Grillage result extraction & transverse grouping
│   │   │   │   └── validator.py      # IRC/IS parametric input validation
│   │   │   └── utils/common.py       # Central KEY_* constants and option lists
│   │   └── desktop/
│   │       └── ui/
│   │           ├── dialogs/
│   │           │   ├── additional_input/additional_inputs.py
│   │           │   ├── girder_2d_plots.py
│   │           │   └── tabs/steel_design_analysis.py
│   │           └── docks/
│   │               ├── cad_cross_section.py
│   │               └── cad_top_view.py
│   └── ospgrillage/                  # Grillage mesh & OpenSeesPy analysis wrapper
├── tests/
│   ├── unit/
│   │   └── test_audit_trail_fixes.py
│   └── integration/
│       └── test_task3_plotting_integration.py
├── environment.yml
└── pyproject.toml
