# lumen-kit

The entry point is `await main.generate(image, seed, witness)`. It receives the
original image bytes, the round seed and an `AsyncWitnessClient`, and returns a
Three.js module or `None`. The caller owns witness authentication and submission.

## Runtime

Use Python **3.13.0**. `requirements.txt` pins the runtime packages, including
Pillow **13.0.0**, witness client **0.2.17**, renderer client **0.1.4** and miner
runtime **0.1.5**. The base miner uses the same SDK release and shared
`miner_runtime.batch.run` runner.
Generation and replay must use the same runtime and native codec builds; package
version pins alone do not guarantee identical encoded image bytes across platforms.

Install the immutable GitHub release wheels on Linux x86_64 with glibc 2.34+ or
macOS 13+ arm64. Their URLs include SHA-256 pins. Keep a checkout for the matching
public proof parameters:

```sh
git clone --branch miner-runtime-v0.1.5 --depth 1 \
  https://github.com/404-Repo/404-gen-subnet.git ../lumen-kit-sdk
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pip check
```

The leader index uses `GenerationsAdapter` from `shared/` in this same tagged
checkout. Set `PYTHONPATH` to that directory for the operator launcher:

```sh
PYTHONPATH="$(cd ../lumen-kit-sdk/shared && pwd)" .venv/bin/python run.py
```

Configure the proof-parameter directory and gateway for the execution host.
`run.py` loads the frozen prompts and submitted generator, calls the shared batch
runner, and exports the validated leader index. Its wallet, input and output
paths are set in the launcher. Running or importing it starts the batch.
