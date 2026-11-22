# Phase 0 Discovery Note

1. **2D CAD Rendering (`CrossSectionCADWidget` & `TopViewCADWidget`):**
   - Drawn via `QPainter` on `QWidget` in `src/osdagbridge/desktop/ui/docks/cad_cross_section.py` and `cad_top_view.py`, hosted inside `BridgeDualCADWidget` (`cad_dual_view.py`).
   - Dimension labels (`Carriageway Width`, `Girder Spacing`, `Deck Thickness`, `Span Length`, `Overhang`, `Overall Bridge Width`, `Bracing Spacing`) are rendered via `draw_text_with_background(...)`.
2. **Input Dictionaries & Sync:**
   - Stored in `CustomWindow.input_dict` (`template_page.py`) and `AdditionalInputs.working_input_dict` / `default_input_dict` (`additional_inputs.py`), keyed by `KEY_*` constants from `src/osdagbridge/core/utils/common.py`.
3. **Additional Inputs Dialog (`AdditionalInputs`):**
   - Located in `src/osdagbridge/desktop/ui/dialogs/additional_input/additional_inputs.py`, built from `ADDITIONAL_INPUTS_SCHEMA` (`ui_fields_additional_input.py`).
4. **Error & Warning Dialogs:**
   - `CustomMessageBox(title, text, buttons=[...], dialogType=MessageBoxType.Warning | MessageBoxType.Critical | MessageBoxType.Success)` in `src/osdagbridge/desktop/ui/dialogs/custom_messagebox.py`.
5. **Results & Member Tagging (`plate_girder/results_data.py` & `girder_2d_plots.py`):**
   - `restructure_data()` partitions element tags into `longitudinal_members` and `groups` (`start_edge`, `end_edge` for End Diaphragms; `transverse_slab` for Intermediate Cross Bracings).
