import math
import unittest
from replay import Supervisor


def observation(at_ms=1000, **changes):
    data = dict(at_ms=at_ms, captured_ms=at_ms - 20, target_id="empty-case-1",
                identity_match=True, pose_xy_m=[0.5, 0.5], calibrated=True,
                tracking_ok=True, path_clear=True, stop_pressed=False,
                user_confirmed=False, approach_complete=False,
                grasp_verified=False, tray_reached=False)
    data.update(changes)
    return data


class ReplayContractTests(unittest.TestCase):
    def test_synthetic_sequence(self):
        s = Supervisor()
        self.assertEqual(s.step(observation())["action"], "SHOW_CANDIDATE")
        self.assertEqual(s.step(observation(1100, user_confirmed=True))["action"], "SIMULATED_APPROACH")
        self.assertEqual(s.step(observation(1200, approach_complete=True))["action"], "SIMULATED_GRASP")
        self.assertEqual(s.step(observation(1300, grasp_verified=True))["action"], "SIMULATED_RETURN")
        event = s.step(observation(1400, tray_reached=True))
        self.assertEqual(event["action"], "SIMULATED_HANDOVER")
        self.assertEqual(event["mode"], "DRY_RUN")

    def test_candidate_must_be_shown_before_confirmation(self):
        s = Supervisor()
        self.assertEqual(s.step(observation(user_confirmed=True))["action"], "SHOW_CANDIDATE")
        self.assertEqual(s.step(observation(1100))["action"], "WAIT")

    def test_no_movement_without_confirmation(self):
        s = Supervisor()
        s.step(observation())
        self.assertEqual(s.step(observation(1100, approach_complete=True))["action"], "WAIT")

    def test_failed_interlocks_stop(self):
        for changes in [dict(calibrated=False), dict(tracking_ok=False), dict(path_clear=False),
                        dict(identity_match=False), dict(stop_pressed=True), dict(captured_ms=0),
                        dict(captured_ms=1001), dict(pose_xy_m=[1.3, 0]), dict(pose_xy_m=[math.nan, 0]),
                        dict(pose_xy_m=[math.inf, 0]), dict(tracking_ok="true")]:
            with self.subTest(changes=changes):
                self.assertEqual(Supervisor().step(observation(**changes))["action"], "STOP")

    def test_stop_latches(self):
        s = Supervisor()
        s.step(observation(stop_pressed=True))
        self.assertEqual(s.step(observation(1100, user_confirmed=True))["state"], "STOPPED")

    def test_target_change_stops(self):
        s = Supervisor()
        s.step(observation())
        self.assertEqual(s.step(observation(1100, user_confirmed=True, target_id="other"))["action"], "STOP")

    def test_pose_change_after_confirmation_stops(self):
        s = Supervisor()
        s.step(observation())
        s.step(observation(1100, user_confirmed=True))
        self.assertEqual(s.step(observation(1200, pose_xy_m=[0.8, 0.5]))["action"], "STOP")

    def test_tracking_loss_during_motion_stops(self):
        s = Supervisor()
        s.step(observation())
        s.step(observation(1100, user_confirmed=True))
        self.assertEqual(s.step(observation(1200, tracking_ok=False))["action"], "STOP")

    def test_timestamps_must_advance(self):
        s = Supervisor()
        s.step(observation())
        self.assertEqual(s.step(observation())["action"], "STOP")

    def test_missing_input_field_stops(self):
        data = observation()
        del data["stop_pressed"]
        self.assertEqual(Supervisor().step(data)["action"], "STOP")


if __name__ == "__main__":
    unittest.main()
