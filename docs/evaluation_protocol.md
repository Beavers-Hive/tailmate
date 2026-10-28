# Planned evaluation protocol

This is a preregistration-style plan. It contains no measured results. `results/trials_template.csv` is intentionally empty except for its header.

## Primary retrieval trial

Run 60 trials: 3 objects × 2 distances × 2 backgrounds × 5 repeats. Objects: empty eyeglass case, key pouch, cloth. Distances: 0.5 m and 1.0 m. Use two marked mat backgrounds and randomize trial order before evaluation.

Success requires the requested item to arrive in the marked floor-level tray, without visible damage or manual assistance after initial confirmation. Wrong object, dropped object, timeout, route failure or manual intervention counts as failure. Declare a timeout before the first measured trial. Keep all attempts in the log, including interrupted attempts, with their termination reason.

The proposed acceptance target is at least 45 successful trials out of 60. Report counts by object, distance and background, alongside overall n/N. A selected highlight video cannot establish success rate.

## Perception and latency

Measure from timestamped camera input to candidate display and report p50/p95 with sample count. The proposed p95 target is at most 2 seconds. Record cold start separately. Add distractor and absent-target trials separately from the 60 retrieval trials and report false acceptance and abstention counts. The current replay examples are not latency measurements.

## Stop behavior

Plan 20 interruption tests: physical stop, stale camera, lost robot tracking and blocked path, five repeats each. Record triggering time, motor-power removal time where relevant, observed stopping time/distance, and result. The desired target is 20/20 successful stops within a predeclared safe envelope. Choose the envelope from measured speed, clearance and mechanics before testing. A test count alone is not a safety certification.

## Local execution and resources

Disconnect internet after provisioning. Document network interfaces and capture the inference process's traffic or an equivalent verification. Record whole-system wall power and host/accelerator configuration. Distinguish vendor specifications, software-only checks and actual measurements.

## User and business validation

Seek five interviews with robotics or assistive-technology teams and two supervised pilot commitments. These are future discovery goals. Any user trials require an appropriate protocol and agreement, and should not begin with unvalidated body support or stair interaction. Compare an appropriate retrieval task with a handheld reacher and record completion, required assistance and user effort without asserting clinical outcomes.
