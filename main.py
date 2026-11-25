#!/usr/bin/env python3
"""One Line, Big Laugh — make.fun entry.

Writes a single funny line (1-200 characters, exactly one line) to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt), where the
competition's gate scorer reads it.

Pure standard library, deterministic: every run writes the same bytes.
"""

import os
import tempfile

LINE = "I asked my smart speaker to play something relaxing, so it started reading my browser history out loud."


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = (LINE + "\n").encode("utf-8")
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    # Self-check: re-read and verify the gate (1-200 chars, one line).
    with open(path, encoding="utf-8") as f:
        text = f.read()
    assert text.count("\n") == 1, "must be exactly one line"
    assert 1 <= len(text.strip()) <= 200, "line out of gate range"
    assert text.rstrip("\n") == LINE


if __name__ == "__main__":
    main()
