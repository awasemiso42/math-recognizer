"""Checks that every expression prompt is LaTeX that math-engine's TeXInput reads.

usage: python3 tools/check_prompts.py MATH_ENGINE_JAR [PROMPTS_JSON]
"""
import json
import subprocess
import sys
from pathlib import Path


def engine_string(text):
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    if len(sys.argv) not in (2, 3):
        sys.exit(__doc__.strip())
    jar = sys.argv[1]
    path = Path(sys.argv[2] if len(sys.argv) == 3 else Path(__file__).parent.parent / "data/prompts/v1.json")
    prompts = json.loads(path.read_text(encoding="utf-8"))["prompts"]
    ids = [p["id"] for p in prompts]
    if len(ids) != len(set(ids)):
        sys.exit("duplicate prompt ids")
    failures = 0
    for prompt in prompts:
        if prompt["kind"] != "expression":
            continue
        source = "ToString(ToExpression(%s,TeXForm,HoldForm))" % engine_string(prompt["latex"])
        run = subprocess.run(["java", "-jar", jar, source], capture_output=True, text=True, encoding="utf-8")
        if run.returncode != 0:
            failures += 1
            print("FAIL %s %s: %s" % (prompt["id"], prompt["latex"], run.stderr.strip().splitlines()[-1]))
        else:
            print("ok   %s %s -> %s" % (prompt["id"], prompt["latex"], run.stdout.strip()))
    if failures:
        sys.exit("%d prompts are not readable by TeXInput" % failures)


if __name__ == "__main__":
    main()
