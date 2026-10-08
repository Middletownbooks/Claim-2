#!/bin/bash
# Compile openai/math's Zarankiewicz crossing-number formalization (family 165) in a minimal Lake
# project: openai/math's own toolchain and Mathlib commit, and only the 339 files under
# OAI/Combinatorics/Crossing, which import nothing but Mathlib. See ../LEAN_CHECK_165.md.
#
#   usage: ./run.sh /path/to/openai/math /path/to/workdir
#
# Route that worked from this container on 8 Oct 2026 (the default elan route did not):
#   - releases.lean-lang.org and cache.mathlib.org are denied by the egress proxy (403), so
#     `elan toolchain install` and `lake exe cache get` both fail;
#   - the toolchain tarball is fetched from GitHub release assets and linked into elan;
#   - Mathlib is built from source (MATHLIB_NO_CACHE_ON_UPDATE=1 stops the post-update hook
#     from retrying the cache).
set -euo pipefail
SRC=${1:?path to an openai/math clone}; W=${2:?work directory}
HERE=$(cd "$(dirname "$0")" && pwd)
TC=$(cat "$HERE/lean-toolchain"); VER=${TC#leanprover/lean4:v}
export PATH=$HOME/.elan/bin:$PATH
command -v elan >/dev/null || { curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh -s -- -y --default-toolchain none; }
if ! elan toolchain list | grep -q "$TC"; then
  mkdir -p "$W/tc" && curl -sSfL -o "$W/tc/lean.tar.zst" \
    "https://github.com/leanprover/lean4/releases/download/v$VER/lean-$VER-linux.tar.zst"
  python3 -c "import zstandard, tarfile, sys
with open(sys.argv[1],'rb') as fh:
    tarfile.open(fileobj=zstandard.ZstdDecompressor().stream_reader(fh), mode='r|').extractall(sys.argv[2])" \
    "$W/tc/lean.tar.zst" "$W/tc"
  elan toolchain link "$TC" "$W/tc/lean-$VER-linux"
fi
mkdir -p "$W/OAI/Combinatorics"
cp "$HERE/lakefile.lean" "$HERE/lean-toolchain" "$HERE/Check.lean" "$W/"
rm -rf "$W/OAI/Combinatorics/Crossing" && cp -r "$SRC/lean/OAI/Combinatorics/Crossing" "$W/OAI/Combinatorics/"
cd "$W"
date -u +"start %FT%TZ"
MATHLIB_NO_CACHE_ON_UPDATE=1 lake update 2>&1 | tail -3
lake build OAI.Combinatorics.Crossing.Main 2>&1 | tail -20
date -u +"built %FT%TZ"
lake env lean Check.lean
date -u +"end %FT%TZ"
