# python3
from __future__ import annotations
import re
from typing import Any, Dict, List, Optional, Tuple, Set

# Try to import your real classes for precise checks.
try:
    from miser import ob as ObBase, c as PairC, e as EncE, L as LindyL, Individual
except Exception:
    ObBase = object
    PairC = EncE = LindyL = Individual = type(None)

def racket_id(name: str) -> str:
    name = name.lstrip("^")
    name = re.sub(r"[^A-Za-z0-9_]", "_", name)
    return name or "x"

def racket_string(s: str) -> str:
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return f"\"{s}\""

class ObExporter:
    def __init__(self):
        self._result_cache: Dict[int, str] = {}
        self._in_progress: Set[int] = set()

    def to_racket(self, x: Any) -> str:
        xid = id(x)

        # Already finished
        if xid in self._result_cache:
            return self._result_cache[xid]

        # Cycle detected (self-loop or mutual)
        if xid in self._in_progress:
            # represent cycles safely; theory allows only singleton self-loop,
            # but we don't assume that here.
            return "NIL  ;<cycle>"

        self._in_progress.add(xid)
        try:
            out = self._to_racket_inner(x)
            self._result_cache[xid] = out
            return out
        finally:
            self._in_progress.remove(xid)

    def _to_racket_inner(self, x: Any) -> str:
        # Pair
        if isinstance(x, PairC) or x.__class__.__name__ == "c":
            ra = self.to_racket(x.a)
            rb = self.to_racket(x.b)
            return f"(c {ra} {rb})"

        # Enclosure / singleton
        if isinstance(x, EncE) or x.__class__.__name__ == "e":
            ra = self.to_racket(x.a)
            return f"(e {ra})"

        # Lindy
        if isinstance(x, LindyL) or getattr(x, "is_lindy", False) or x.__class__.__name__ == "L":
            s = getattr(x, "name", None)
            if s is None:
                s = str(x)
            return f"(L {racket_string(str(s))})"

        # Primitive Individual
        if isinstance(x, Individual) or x.__class__.__name__.endswith("_") or hasattr(x, "name"):
            n = getattr(x, "name", None)
            if isinstance(n, str):
                return racket_id(n).upper()

        # Fallback: stringify safely
        return racket_id(str(x))

def export_namespace(
    namespace: Dict[str, Any],
    provide_all: bool = True,
    require_runtime: str = "omiser/runtime",
    order: Optional[List[str]] = None,
) -> str:
    exp = ObExporter()

    # Only export actual obs
    items = [(k, v) for k, v in namespace.items() if isinstance(v, ObBase)]

    if order:
        ordered = []
        remaining = dict(items)
        for k in order:
            if k in remaining:
                ordered.append((k, remaining.pop(k)))
        ordered.extend(sorted(remaining.items(), key=lambda kv: kv[0]))
        items = ordered
    else:
        items = sorted(items, key=lambda kv: kv[0])

    provides = [racket_id(k) for k, _ in items]

    lines: List[str] = []
    lines.append("#lang racket/base")
    lines.append(f"(require {require_runtime})")
    lines.append("")
    if provide_all:
        lines.append("(provide")
        for p in provides:
            lines.append(f"  {p}")
        lines.append("  namespace)")
        lines.append("")

    for name, obval in items:
        rid = racket_id(name)
        rexpr = exp.to_racket(obval)
        lines.append(f"(define {rid}")
        lines.append(f"  {rexpr})")
        lines.append("")

    lines.append("(define namespace")
    lines.append("  (hash")
    for name, _ in items:
        rid = racket_id(name)
        lines.append(f"   '{rid} {rid}")
    lines.append("   ))")
    lines.append("")
    return "\n".join(lines)

if __name__ == "__main__":
    # Point this import at the module where your stdlib obs live.
    # Example if they are in library.py:
    from library import namespace  # <-- adjust if needed

    racket_src = export_namespace(
        namespace,
        order=[
            "cI","cK","cSpart","cS","cREV",
            "cB0","cB","cC","cD","cT","cUobAB",
            "cW0","cW","cY",
            "hasX","has","simpleSwap","swap","dup",
            "bTRUE","bFALSE","bNOT","bOR","bAND","bXOR","bSAY",
            "isIndividual"
        ],
    )
    with open("stdlib.rkt", "w", encoding="utf-8") as f:
        f.write(racket_src)
    print("Wrote stdlib.rkt")
