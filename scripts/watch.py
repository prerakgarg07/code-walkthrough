"""Print each new comment from the reader, resuming from the last line read (saved in .seen) so a restart misses nothing.

    python3 -u watch.py <code folder>
"""

import sys
import time
from pathlib import Path

DATA = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve() / ".walkthrough"
log, seen_file = DATA / "comments.jsonl", DATA / ".seen"
seen = int(seen_file.read_text()) if seen_file.exists() else 0
while True:
    lines = log.read_text().splitlines() if log.exists() else []
    for line in lines[seen:]:
        if '"who": "Me"' in line:
            print(line, flush=True)
    if len(lines) != seen:
        seen = len(lines)
        seen_file.write_text(str(seen))
    time.sleep(2)
