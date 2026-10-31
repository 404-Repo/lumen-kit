# lumen-kit

The entry point is `await main.generate(image, seed, witness)`. It receives the
original image bytes, the round seed and an `AsyncWitnessClient`, and returns a
Three.js module or `None`. The caller owns witness authentication and submission.

## Runtime

Use Python **3.13.0**. `requirements.txt` pins the runtime packages, including
Pillow **13.0.0**, witness client **0.2.15** and renderer client **0.1.4**.
Generation and replay must use the same runtime and native codec builds; package
version pins alone do not guarantee identical encoded image bytes across platforms.

The SDK clients are built from the public source revision
`404-Repo/404-gen-subnet@7c5d2ffbb72a8b5ec3f499ac0d62b13aad28e7ea`.
Build their native proof library with Go **1.27.3** and a C compiler before
installing. From this repository, on macOS:

```sh
git clone https://github.com/404-Repo/404-gen-subnet.git ../lumen-kit-sdk
git -C ../lumen-kit-sdk checkout --detach 7c5d2ffbb72a8b5ec3f499ac0d62b13aad28e7ea
(cd ../lumen-kit-sdk/witness-client/native && \
  go build -trimpath -buildmode=c-shared -o ../src/witness_client/libwitnessproof.dylib .)
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt \
  ../lumen-kit-sdk/renderer-client ../lumen-kit-sdk/witness-client
.venv/bin/python -m pip check
```

On Linux, build `libwitnessproof.so` instead of `libwitnessproof.dylib`.
The SDK also requires matching public proof parameters and gateway configuration,
provided by the execution host.
