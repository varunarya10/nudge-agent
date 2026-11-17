#!/usr/bin/env python3
"""PreToolUse hook: stop Claude Code from touching .env files (.env.example is allowed).

Standard library only and Python 3.9 compatible, since it runs with the system python3.
"""
import json
import re
import sys

# The tool_input fields that hold a path, glob pattern or shell command, per tool.
# Content fields (Write's "content", Edit's "new_string") are deliberately not checked,
# so documentation or code that merely mentions ".env" can still be written.
FIELDS = {
    "Read": ("file_path",),
    "Edit": ("file_path",),
    "Write": ("file_path",),
    "Grep": ("path", "glob"),
    "Glob": ("path", "pattern"),
    "Bash": ("command",),
}

# ".env" not preceded by a filename character (so "settings.env" or "dotenv" don't match),
# followed by an optional suffix such as ".local", "*" or ".example".
ENV_RE = re.compile(r"(?<![\w.-])\.env([\w.*?\[\]{},-]*)", re.IGNORECASE)


def refers_to_env_file(text):
    for match in ENV_RE.finditer(text):
        suffix = match.group(1).lower()
        if suffix == ".example":
            continue
        # "" is .env itself; ".x" is .env.x; "*", "?", "[", "{" are globs that can match .env.
        # A letter (e.g. ".envrc", ".environment") is a different file, so it's allowed.
        if suffix == "" or suffix[0] in ".*?[{":
            return True
    return False


def main():
    try:
        data = json.load(sys.stdin)
    except ValueError:
        # Fail closed: if we can't read the input, we can't prove the call is safe.
        print("block_env hook: could not parse hook input; blocking.", file=sys.stderr)
        sys.exit(2)

    tool_input = data.get("tool_input") or {}
    for field in FIELDS.get(data.get("tool_name"), ()):
        value = tool_input.get(field)
        if isinstance(value, str) and refers_to_env_file(value):
            print("Blocked: access to .env files is not allowed (.env.example is fine).", file=sys.stderr)
            sys.exit(2)
    sys.exit(0)


if __name__ == "__main__":
    main()
