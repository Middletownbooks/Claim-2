"""Mine the ten-proofs corpus for upstreamable lemmas and cross-development
duplicates.

Each development is a single .lean file over `import Mathlib`, so any
identifier not declared locally is library vocabulary.  A declaration is
EXPORTABLE when its statement mentions no locally-declared name: it is a
statement about mathlib objects that happens to live in this repo.
"""
import re, os, json, collections, hashlib

DECL = re.compile(r'^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*'
                  r'(theorem|lemma|def|abbrev|structure|inductive|instance|class)\s+'
                  r'([A-Za-z_][A-Za-z0-9_.\'!?]*)', re.M)
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_.']*")
KEYWORDS = set("""theorem lemma def abbrev structure inductive instance class
forall fun let in with do if then else match at by exact intro apply refine
simp rw ring omega linarith norm_num constructor obtain rcases rintro use
have show from this and or not iff true false Type Prop Sort where deriving
open namespace end section variable universe import set_option attribute""".split())

def split_decls(text):
    """yield (kind, name, signature) — signature is header text up to the
    top-level ':=' or ' by ' that starts the proof."""
    marks = [(m.start(), m.group(1), m.group(2)) for m in DECL.finditer(text)]
    for i, (pos, kind, name) in enumerate(marks):
        end = marks[i+1][0] if i+1 < len(marks) else len(text)
        body = text[pos:end]
        depth = 0
        cut = len(body)
        j = 0
        while j < len(body):
            c = body[j]
            if c in '([{⟨': depth += 1
            elif c in ')]}⟩': depth -= 1
            elif depth == 0 and body.startswith(':=', j): cut = j; break
            elif depth == 0 and body.startswith(' by\n', j): cut = j; break
            elif depth == 0 and body.startswith(' by ', j): cut = j; break
            j += 1
        yield kind, name, body[:cut]

def analyse(path):
    text = open(path, encoding='utf-8', errors='replace').read()
    decls = list(split_decls(text))
    local = {n for k, n, _ in decls}
    # also local namespace prefixes, so Foo.bar counts as local when Foo is
    ns = set(re.findall(r'^namespace\s+([A-Za-z_][\w.\']*)', text, re.M))
    def is_local(tok):
        if tok in local: return True
        head = tok.split('.')[0]
        if head in local or head in ns: return True
        for n in ns:
            if tok.startswith(n + '.'): return True
        return False
    out = []
    for kind, name, sig in decls:
        if kind not in ('theorem', 'lemma'): continue
        toks = [t for t in IDENT.findall(sig) if t not in KEYWORDS]
        toks = [t for t in toks if len(t) > 1]        # drop binder letters
        body = sig.split(None, 2)
        stmt = body[2] if len(body) > 2 else ''
        exportable = not any(is_local(t) for t in toks)
        out.append(dict(name=name, exportable=exportable, sig=sig.strip(),
                        stmt=stmt.strip(), ntok=len(set(toks))))
    return out, local, ns

def norm(s):
    """normalise a statement for cross-file comparison: collapse whitespace,
    drop the binder names by replacing single-char identifiers."""
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r"\b[a-zA-Z]'?\b", '_', s)          # binder-ish single letters
    return s

if __name__ == '__main__':
    root = '/home/user/ten-proofs'
    data = {}
    for f in sorted(os.listdir(root)):
        if not f.endswith('.lean') or f == 'All.lean': continue
        name = f[:-5]
        decls, local, ns = analyse(os.path.join(root, f))
        data[name] = decls
        ex = [d for d in decls if d['exportable']]
        print("%-28s %5d theorems, %5d exportable (%.1f%%)"
              % (name, len(decls), len(ex), 100*len(ex)/max(1, len(decls))))
    json.dump({k: v for k, v in data.items()}, open('decls.json', 'w'))
