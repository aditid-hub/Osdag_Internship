import numpy as np
from osdagbridge.core.utils.common import (
    KEY_CARRIAGEWAY_WIDTH,
    KEY_INCLUDE_MEDIAN,
    KEY_SKEW_ANGLE,
    KEY_SPAN,
    VALUES_FOOTPATH_PRESSURE_MODE,
)
from osdagbridge.core.bridge_types.plate_girder.validator import BridgeInputValidator
from osdagbridge.core.bridge_types.plate_girder.results_data import (
    get_transverse_member_groups,
    extract_transverse_member_response,
)


def test_task2_custom_mode_labels():
    assert "Custom" in VALUES_FOOTPATH_PRESSURE_MODE
    assert "User-defined" not in VALUES_FOOTPATH_PRESSURE_MODE


def test_task1_basic_validation():
    validator = BridgeInputValidator()
    assert validator.validate_basic_inputs(KEY_SPAN, {KEY_SPAN: "25.0"}) is None
    assert validator.validate_basic_inputs(KEY_SKEW_ANGLE, {KEY_SKEW_ANGLE: "15.0"}) is None
    assert validator.validate_basic_inputs(KEY_SPAN, {KEY_SPAN: "-5"}) is not None
    err_cw = validator.validate_basic_inputs(
        KEY_CARRIAGEWAY_WIDTH,
        {KEY_CARRIAGEWAY_WIDTH: "5.5", KEY_INCLUDE_MEDIAN: "Yes"},
    )
    assert err_cw is not None


def test_task3_transverse_member_groups_disjoint_and_extraction():
    mock_data = {
        "nodes": {
            "1": [0.0, 0.0, 0.0],
            "2": [0.0, 0.0, 2.5],
            "3": [5.0, 0.0, 0.0],
            "4": [5.0, 0.0, 2.5],
            "5": [10.0, 0.0, 0.0],
            "6": [10.0, 0.0, 2.5],
        },
        "members": {
            "1": [1, 2],
            "2": [3, 4],
            "3": [5, 6],
            "11": [1, 3],
            "12": [2, 4],
        },
        "groups": {
            "start_edge": [1],
            "end_edge": [3],
            "transverse_slab": [2],
        },
        "longitudinal_members": [11, 12],
        "transverse_members": [1, 2, 3],
        "forces": {
            "girder self weight": {
                "1": {"Vx_i": 10.0, "Vx_j": -10.0, "Vy_i": 12.0, "Vy_j": -12.0, "Vz_i": 0.0, "Vz_j": 0.0,
                      "Mx_i": 1.5, "Mx_j": 1.5, "My_i": 0.0, "My_j": 0.0, "Mz_i": 0.0, "Mz_j": 30.0},
                "2": {"Vx_i": 5.0, "Vx_j": -5.0, "Vy_i": 8.0, "Vy_j": -8.0, "Vz_i": 0.0, "Vz_j": 0.0,
                      "Mx_i": 0.8, "Mx_j": 0.8, "My_i": 0.0, "My_j": 0.0, "Mz_i": 0.0, "Mz_j": 18.5},
                "3": {"Vx_i": 10.0, "Vx_j": -10.0, "Vy_i": 12.0, "Vy_j": -12.0, "Vz_i": 0.0, "Vz_j": 0.0,
                      "Mx_i": 1.5, "Mx_j": 1.5, "My_i": 0.0, "My_j": 0.0, "Mz_i": 0.0, "Mz_j": 30.0},
            }
        },
        "displacements": {
            "girder self weight": {
                "1": {"x": 0.0, "y": -0.002, "z": 0.0},
                "2": {"x": 0.0, "y": -0.003, "z": 0.0},
                "3": {"x": 0.0, "y": -0.005, "z": 0.0},
                "4": {"x": 0.0, "y": -0.006, "z": 0.0},
            }
        },
    }
    t_groups = get_transverse_member_groups(mock_data)
    assert t_groups["End Diaphragms"] == [1, 3]
    assert t_groups["Intermediate Cross Bracings"] == [2]

    long_set = set(mock_data["longitudinal_members"])
    trans_set = set(t_groups["End Diaphragms"]) | set(t_groups["Intermediate Cross Bracings"])
    assert long_set.isdisjoint(trans_set)
    assert long_set | trans_set == {int(k) for k in mock_data["members"]}

    for qty in ("Fx", "Vy", "Vz", "Tx", "My", "Mz", "Dx", "Dy", "Dz"):
        xs, ys = extract_transverse_member_response(mock_data, "End Diaphragms", "girder self weight", qty)
        assert len(xs) == 2
        assert len(ys) == 2
