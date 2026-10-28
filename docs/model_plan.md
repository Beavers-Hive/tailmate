# Candidate model and deployment plan

**No model inference has been run or benchmarked for this submission package.**

## Candidate

Hailo's official application guide lists Qwen2-VL-2B-Instruct for Hailo-10H visual question answering. Use this as a candidate crop-verification model. It does not establish that the model identifies transparent glasses reliably or runs with acceptable latency on the allocated UGen300 variant.

## Deployment gate

1. Confirm the allocated UGen300 model and supported host configuration.
2. Install the organizer-recommended driver/runtime from vendor sources.
3. Select a compatible compiled model HEF and record its checksum.
4. Run the vendor example before adding any robot task logic.
5. Confirm actual image preprocessing and prompt formatting against the installed release.
6. Evaluate empty eyeglass-case crops and distractors before fragile glasses.
7. Record p50/p95 latency, failure cases and memory use. Set a timeout and abstain on malformed responses.

If the candidate is incompatible or misses latency targets, validate a smaller supported model or a detector for the constrained object set. Declare the actual final method. Do not silently replace the accelerator with cloud inference.

## Reproducibility record

Record model identifier, weights/HEF source URL, version, SHA-256, license and redistribution conditions, runtime, firmware, driver, host OS, accelerator variant, image resolution, prompts and inference settings. Do not upload vendor model files until redistribution rights are checked. Model and dataset licenses are separate from this project's code.

Sources checked October 17, 2026:

- https://github.com/hailo-ai/hailo-apps
- https://github.com/hailo-ai/hailo-apps/blob/main/.hailo/instructions/gen-ai-development.md
- https://www.asus.com/uk/motherboards-components/ai-accelerator/ugen/ugen300-usb-8g/
