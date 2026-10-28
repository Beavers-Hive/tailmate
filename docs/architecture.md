# Proposed integration architecture

The current package implements a synthetic task supervisor only. All components below require real integration and validation.

## Perception and geometry

A fixed calibrated camera covers a flat marked test mat. The Linux host selects object crops with scene segmentation and tracks the robot's fiducial markers. The UGen300 runs a compatible VLM to help decide whether a crop matches the user-requested object. The host maps image coordinates to the calibrated plane. Natural-language model output never directly defines servo angles or distance.

For the first demo, the user selects an image candidate and confirms a task. Voice input is optional future work. Multiple matches, uncertain labels, missing calibration or lost robot markers stop the task. A VLM's self-reported confidence is not a calibrated probability.

## Control boundary

The host supervisor chooses a bounded named behavior. A microcontroller runs a validated gait, enforces joint limits and supervises a heartbeat. A separate physical stop cuts servo power. A soft gripper needs contact sensing and release behavior before fragile-object trials.

Initial object positions remain in a marked 0.5–1 m route. The reference software uses illustrative 1.2 × 1.2 m coordinate bounds, a 500 ms observation-age check and 5 cm target drift tolerance. These are software examples, not validated hardware thresholds. Real camera error, speed, stopping distance and mechanical clearance must determine deployment thresholds.

The dry run does not implement real-time scheduling, an independent watchdog, servo current limits, timeouts for each motion, geometry transforms, grasp sensing or a physical stop. It cannot provide a safety guarantee. Never attach it directly to servo hardware without a separate, reviewed and measured control layer.

## Resources

Use a supported Linux x86 or ARM host and the allocated USB or M.2 UGen300 variant. The accelerator has its own runtime and memory. It needs a host and does not supply robot actuation power. Verify connector, power delivery, kernel, driver, HailoRT, firmware and model HEF compatibility on the exact assigned device.

## Offline behavior

After model and software provisioning, all proposed inference runs locally. Disable internet during evaluation and record the verification method. Do not claim zero power, zero latency, or whole-system consumption based on the accelerator's typical chip power specification.
