"""Synthetic task replay. No AI inference, device access or robot control."""
from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Observation:
    at_ms: int
    captured_ms: int
    target_id: str
    identity_match: bool
    pose_xy_m: tuple[float, float]
    calibrated: bool
    tracking_ok: bool
    path_clear: bool
    stop_pressed: bool
    user_confirmed: bool
    approach_complete: bool
    grasp_verified: bool
    tray_reached: bool

    @classmethod
    def parse(cls, raw: dict) -> "Observation":
        if not isinstance(raw, dict):
            raise ValueError("Observation must be an object")
        fields = cls.__dataclass_fields__
        if set(raw) != set(fields):
            raise ValueError("Missing or unexpected observation fields")
        for name in ("at_ms", "captured_ms"):
            if type(raw[name]) is not int or raw[name] < 0:
                raise ValueError("Timestamps must be non-negative integer milliseconds")
        if not isinstance(raw["target_id"], str) or not raw["target_id"].strip():
            raise ValueError("A target identifier is required")
        xy = raw["pose_xy_m"]
        if not isinstance(xy, (list, tuple)) or len(xy) != 2:
            raise ValueError("Pose must contain x and y")
        if any(type(v) not in (int, float) or not math.isfinite(v) for v in xy):
            raise ValueError("Pose must be finite numeric data")
        booleans = set(fields) - {"at_ms", "captured_ms", "target_id", "pose_xy_m"}
        if any(type(raw[k]) is not bool for k in booleans):
            raise ValueError("Flags must be JSON booleans")
        return cls(**{**raw, "pose_xy_m": tuple(xy)})


class Supervisor:
    """Illustrative task contract. Always dry run, never a hardware safety loop."""

    def __init__(self):
        self.state = "IDLE"
        self.target_id = None
        self.confirmed_pose = None
        self.last_ms = -1

    def step(self, raw: dict) -> dict:
        if self.state == "STOPPED":
            return self._event("STOP", "latched stop; construct a new run to reset")
        try:
            o = Observation.parse(raw)
        except (TypeError, ValueError) as error:
            return self._stop(str(error))
        if o.at_ms <= self.last_ms:
            return self._stop("non-monotonic observation timestamp")
        self.last_ms = o.at_ms
        if o.stop_pressed:
            return self._stop("stop requested")
        age = o.at_ms - o.captured_ms
        if not 0 <= age <= 500:
            return self._stop("camera observation is stale or from the future")
        if not (o.calibrated and o.tracking_ok and o.path_clear and o.identity_match):
            return self._stop("calibration, tracking, path or identity check failed")
        x, y = o.pose_xy_m
        if not (0 <= x <= 1.2 and 0 <= y <= 1.2):
            return self._stop("target outside the example test area")
        if self.target_id is not None and o.target_id != self.target_id:
            return self._stop("target changed after candidate selection")
        if self.confirmed_pose is not None:
            drift = math.dist(o.pose_xy_m, self.confirmed_pose)
            if drift > 0.05:
                return self._stop("target moved beyond the illustrative pose tolerance")
        if self.state == "IDLE":
            self.target_id = o.target_id
            self.state = "AWAITING_CONFIRMATION"
            return self._event("SHOW_CANDIDATE", "display target before accepting confirmation")
        if self.state == "AWAITING_CONFIRMATION":
            if not o.user_confirmed:
                return self._event("WAIT", "user has not confirmed this candidate")
            self.confirmed_pose = o.pose_xy_m
            self.state = "APPROACHING"
            return self._event("SIMULATED_APPROACH", "target confirmed")
        if self.state == "APPROACHING":
            if not o.approach_complete:
                return self._event("WAIT", "waiting for simulated approach completion")
            self.state = "GRASPING"
            return self._event("SIMULATED_GRASP", "simulated approach completed")
        if self.state == "GRASPING":
            if not o.grasp_verified:
                return self._event("WAIT", "waiting for synthetic grasp verification")
            self.state = "RETURNING"
            return self._event("SIMULATED_RETURN", "synthetic grasp check passed")
        if self.state == "RETURNING":
            if not o.tray_reached:
                return self._event("WAIT", "waiting for synthetic tray signal")
            self.state = "DONE"
            return self._event("SIMULATED_HANDOVER", "synthetic tray signal received")
        return self._event("DONE", "dry-run sequence complete")

    def _event(self, action: str, reason: str) -> dict:
        return {"mode": "DRY_RUN", "state": self.state, "action": action, "reason": reason}

    def _stop(self, reason: str) -> dict:
        self.state = "STOPPED"
        return self._event("STOP", reason)


def main() -> None:
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "examples/success.json"
    observations = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(observations, list):
        raise ValueError("Replay input must be a JSON list")
    supervisor = Supervisor()
    for item in observations:
        print(json.dumps(supervisor.step(item), ensure_ascii=False))


if __name__ == "__main__":
    main()
