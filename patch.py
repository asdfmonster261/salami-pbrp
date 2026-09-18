#!/usr/bin/env python3
# Source patcher for this device tree: applies the string rewrites declared in
# subpatch/*.py to the recovery source the tree is checked out in. Matching is
# whitespace-flexible and idempotent: an already-applied change is skipped, and an
# unmatched one exits nonzero so a build never runs on silently unpatched source.

import argparse
import importlib.util
import re
import sys
from pathlib import Path


class PatchManager:
    def __init__(self, base_path):
        self.base_path = Path(base_path).resolve()
        self.subpatches_dir = self.base_path / "subpatch"
        # device/<vendor>/<codename>/patch.py -> the source tree root
        self.source_root = self.base_path.parents[2]

    def load_subpatches(self):
        subpatches = []
        if not self.subpatches_dir.exists():
            return subpatches
        if str(self.base_path) not in sys.path:
            sys.path.insert(0, str(self.base_path))
        for file in sorted(self.subpatches_dir.glob("*.py")):
            if file.name == "__init__.py":
                continue
            spec = importlib.util.spec_from_file_location(file.stem, file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "SubPatch"):
                subpatches.append(module.SubPatch(self))
        return subpatches

    def run(self):
        parser = argparse.ArgumentParser(description="device tree source patcher")
        parser.add_argument("--check", action="store_true", help="report status only")
        parser.add_argument("--mod", action="store_true", help="apply the changes")
        args = parser.parse_args()
        if not (args.check or args.mod):
            parser.error("pass --check or --mod")

        subpatches = self.load_subpatches()
        if not subpatches:
            print("no subpatches found")
            return 0

        ok = True
        for patch in subpatches:
            print(f">>> {patch.name}")
            ok = (patch.mod() if args.mod else patch.check()) and ok
        return 0 if ok else 1


class BaseSubPatch:
    def __init__(self, manager):
        self.manager = manager
        self.name = ""
        self.target_file = ""
        self.CHANGES = []

    # Tokenize a code block and join with \s* so whitespace differences never
    # break the match.
    def _regex(self, text):
        tokens = re.findall(r"\w+|[^\w\s]", text.strip())
        return r"\s*".join(re.escape(t) for t in tokens if t)

    def _status(self, text, original, modified):
        mod_re = self._regex(modified)
        if mod_re and re.search(mod_re, text, re.MULTILINE | re.DOTALL):
            return "applied", None
        match = re.search(self._regex(original), text, re.MULTILINE | re.DOTALL)
        return ("ready", match) if match else ("missing", None)

    def _read(self):
        path = self.manager.source_root / self.target_file
        if not path.is_file():
            print(f"  FAIL: no such file {self.target_file}")
            return None, None
        return path, path.read_text(errors="ignore")

    def check(self):
        path, text = self._read()
        if path is None:
            return False
        ok = True
        for orig, mod in self.CHANGES:
            status, _ = self._status(text, orig, mod)
            print(f"  {status}: {self.target_file}")
            ok = ok and status != "missing"
        return ok

    def mod(self):
        path, text = self._read()
        if path is None:
            return False
        ok, changed = True, False
        for orig, mod in self.CHANGES:
            status, match = self._status(text, orig, mod)
            if status == "ready":
                text = text[:match.start()] + mod.strip() + text[match.end():]
                changed = True
                print(f"  patched: {self.target_file}")
            elif status == "applied":
                print(f"  skipped (already applied): {self.target_file}")
            else:
                print(f"  FAIL: no match in {self.target_file}")
                ok = False
        if changed:
            path.write_text(text)
        return ok


if __name__ == "__main__":
    sys.exit(PatchManager(Path(__file__).parent).run())
