from unittest.mock import MagicMock
import numpy as np
import pandas as pd

from osdagbridge.core.bridge_types.plate_girder.graph_engine import GirderGraphEngine
from osdagbridge.core.bridge_types.plate_girder.results_data import (
    get_transverse_member_groups,
)


class _DummyAnalysisResults:
    def __init__(self, data: dict):
        self.data = data

    def _get_girder_paths_df(self, girder_filter=None):
        return pd.DataFrame({"Girder": ["EB1", "G1", "G2", "EB2"]})


def _sample_grillage_output() -> dict:
    return {
        "nodes": {
            "1": [0.0, 0.0, 0.0],
            "2": [0.0, 0.0, 2.75],
            "3": [5.0, 0.0, 0.0],
            "4": [5.0, 0.0, 2.75],
            "5": [10.0, 0.0, 0.0],
            "6": [10.0, 0.0, 2.75],
        },
        "members": {
            "1": [1, 2],
            "2": [3, 4],
            "3": [5, 6],
            "11": [1, 3],
            "12": [2, 4],
            "13": [3, 5],
            "14": [4, 6],
        },
        "groups": {
            "start_edge": [1],
            "end_edge": [3],
            "transverse_slab": [2],
        },
        "longitudinal_members": [11, 12, 13, 14],
        "transverse_members": [1, 2, 3],
        "forces": {
            "girder self weight": {
                "1": {"Vx_i": 12.0, "Vx_j": -12.0, "Vy_i": 15.0, "Vy_j": -15.0, "Vz_i": 1.0, "Vz_j": -1.0,
                      "Mx_i": 2.1, "Mx_j": 2.1, "My_i": 0.5, "My_j": -0.5, "Mz_i": 0.0, "Mz_j": 35.0},
                "2": {"Vx_i": 6.0, "Vx_j": -6.0, "Vy_i": 9.0, "Vy_j": -9.0, "Vz_i": 0.4, "Vz_j": -0.4,
                      "Mx_i": 1.1, "Mx_j": 1.1, "My_i": 0.2, "My_j": -0.2, "Mz_i": 0.0, "Mz_j": 21.0},
                "3": {"Vx_i": 12.0, "Vx_j": -12.0, "Vy_i": 15.0, "Vy_j": -15.0, "Vz_i": 1.0, "Vz_j": -1.0,
                      "Mx_i": 2.1, "Mx_j": 2.1, "My_i": 0.5, "My_j": -0.5, "Mz_i": 0.0, "Mz_j": 35.0},
            },
            "live load": {
                "1": {"Vx_i": 24.0, "Vx_j": -24.0, "Vy_i": 31.0, "Vy_j": -31.0, "Vz_i": 2.2, "Vz_j": -2.2,
                      "Mx_i": 4.5, "Mx_j": 4.5, "My_i": 1.1, "My_j": -1.1, "Mz_i": 0.0, "Mz_j": 74.0},
                "2": {"Vx_i": 14.0, "Vx_j": -14.0, "Vy_i": 19.0, "Vy_j": -19.0, "Vz_i": 0.9, "Vz_j": -0.9,
                      "Mx_i": 2.3, "Mx_j": 2.3, "My_i": 0.6, "My_j": -0.6, "Mz_i": 0.0, "Mz_j": 44.0},
                "3": {"Vx_i": 24.0, "Vx_j": -24.0, "Vy_i": 31.0, "Vy_j": -31.0, "Vz_i": 2.2, "Vz_j": -2.2,
                      "Mx_i": 4.5, "Mx_j": 4.5, "My_i": 1.1, "My_j": -1.1, "Mz_i": 0.0, "Mz_j": 74.0},
            },
        },
        "displacements": {
            "girder self weight": {
                "1": {"x": 0.0001, "y": -0.002, "z": 0.0002},
                "2": {"x": 0.0001, "y": -0.003, "z": 0.0002},
                "3": {"x": 0.0002, "y": -0.005, "z": 0.0003},
                "4": {"x": 0.0002, "y": -0.006, "z": 0.0003},
                "5": {"x": 0.0001, "y": -0.002, "z": 0.0002},
                "6": {"x": 0.0001, "y": -0.003, "z": 0.0002},
            },
            "live load": {
                "1": {"x": 0.0003, "y": -0.006, "z": 0.0005},
                "2": {"x": 0.0003, "y": -0.008, "z": 0.0005},
                "3": {"x": 0.0005, "y": -0.012, "z": 0.0007},
                "4": {"x": 0.0005, "y": -0.014, "z": 0.0007},
                "5": {"x": 0.0003, "y": -0.006, "z": 0.0005},
                "6": {"x": 0.0003, "y": -0.008, "z": 0.0005},
            },
        },
    }


def test_task3_end_to_end_engine_and_loadcases():
    data = _sample_grillage_output()
    handler = _DummyAnalysisResults(data)
    engine = GirderGraphEngine(
        MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock(),
        result_handler=handler,
    )

    keys = engine.get_girder_keys()
    assert "End Diaphragms" in keys
    assert "Intermediate Cross Bracings" in keys

    groups = get_transverse_member_groups(data)
    long_tags = set(data["longitudinal_members"])
    trans_tags = set(groups["End Diaphragms"]) | set(groups["Intermediate Cross Bracings"])
    assert long_tags.isdisjoint(trans_tags)
    assert long_tags | trans_tags == {int(k) for k in data["members"]}

    quantities = ("Fx", "Vy", "Vz", "Tx", "My", "Mz", "Dx", "Dy", "Dz")
    for member in ("End Diaphragms", "Intermediate Cross Bracings"):
        res_dl = engine.extract_transverse_results(member, "girder self weight")
        res_ll = engine.extract_transverse_results(member, "live load")
        assert res_dl is not None and res_ll is not None
        xs_dl, _, _, _, all_dl = res_dl
        xs_ll, _, _, _, all_ll = res_ll
        assert len(xs_dl) == 2 and len(xs_ll) == 2
        for qty in quantities:
            assert qty in all_dl and qty in all_ll
            assert not np.allclose(all_dl[qty], all_ll[qty]), f"{member} {qty} did not vary with loadcase"
