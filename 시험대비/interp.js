/* ===== 미니 Python 인터프리터 (배열·반복문·조건문 수준) ===== */
class PyError extends Error { constructor(msg, line) { super(msg); this.line = line; } }
class PFloat { constructor(v) { this.v = v; } }
class PTuple { constructor(items) { this.items = items; } }
class PDict { constructor() { this.m = new Map(); } }
class PFunc { constructor(name, params, body) { this.name = name; this.params = params; this.body = body; } }
class PBuiltin { constructor(name, fn) { this.name = name; this.fn = fn; } }
class Env {
  constructor(parent) { this.vars = new Map(); this.parent = parent || null; }
  get(n) { if (this.vars.has(n)) return this.vars.get(n); return this.parent ? this.parent.get(n) : undefined; }
  has(n) { return this.vars.has(n) || (this.parent ? this.parent.has(n) : false); }
  set(n, v) { this.vars.set(n, v); }
}

const KEYWORDS = new Set(['if', 'elif', 'else', 'for', 'while', 'in', 'not', 'and', 'or', 'def', 'return', 'break', 'continue', 'pass', 'True', 'False', 'None', 'is', 'global']);
const OPS3 = ['**=', '//=', '<<=', '>>='];
const OPS2 = ['**', '//', '==', '!=', '<=', '>=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<', '>>'];
const OPS1 = '+-*/%<>=()[]{},:.&|^~';

function readString(line, i, lineno) {
  const q = line[i]; let j = i + 1; let s = '';
  while (j < line.length) {
    const c = line[j];
    if (c === '\\') {
      const n = line[j + 1];
      const map = { n: '\n', t: '\t', '\\': '\\', "'": "'", '"': '"', '0': '\0' };
      s += (n in map) ? map[n] : n; j += 2; continue;
    }
    if (c === q) return { s, end: j + 1 };
    s += c; j++;
  }
  throw new PyError('SyntaxError: 문자열이 닫히지 않았습니다', lineno);
}

function tokenize(src) {
  const lines = src.replace(/\r/g, '').split('\n');
  const toks = []; const indents = [0]; let depth = 0;
  for (let li = 0; li < lines.length; li++) {
    const line = lines[li]; const lineno = li + 1;
    if (depth === 0) {
      const t = line.trim();
      if (t === '' || t.startsWith('#')) continue;
      const ind = line.match(/^[ \t]*/)[0].replace(/\t/g, '    ').length;
      if (ind > indents[indents.length - 1]) { indents.push(ind); toks.push({ t: 'INDENT', line: lineno }); }
      else {
        while (ind < indents[indents.length - 1]) { indents.pop(); toks.push({ t: 'DEDENT', line: lineno }); }
        if (ind !== indents[indents.length - 1]) throw new PyError('IndentationError: 들여쓰기가 맞지 않습니다', lineno);
      }
    }
    let i = 0;
    while (i < line.length) {
      const c = line[i];
      if (c === ' ' || c === '\t') { i++; continue; }
      if (c === '#') break;
      if (c === '\\' && line.slice(i + 1).trim() === '') { i = line.length; break; }
      if ((c === 'f' || c === 'F') && (line[i + 1] === '"' || line[i + 1] === "'")) {
        const r = readString(line, i + 1, lineno); toks.push({ t: 'FSTR', v: r.s, line: lineno }); i = r.end; continue;
      }
      if (c === '"' || c === "'") { const r = readString(line, i, lineno); toks.push({ t: 'STR', v: r.s, line: lineno }); i = r.end; continue; }
      if (/[0-9]/.test(c) || (c === '.' && /[0-9]/.test(line[i + 1] || ''))) {
        const m = line.slice(i).match(/^(\d+\.\d*|\.\d+|\d+)([eE][+-]?\d+)?/); const s = m[0];
        toks.push({ t: 'NUM', v: /[.eE]/.test(s) ? new PFloat(parseFloat(s)) : parseInt(s, 10), line: lineno }); i += s.length; continue;
      }
      if (/[A-Za-z_À-￿]/.test(c)) {
        const m = line.slice(i).match(/^[A-Za-z_À-￿][A-Za-z0-9_À-￿]*/); const s = m[0];
        toks.push({ t: KEYWORDS.has(s) ? 'KW' : 'NAME', v: s, line: lineno }); i += s.length; continue;
      }
      let op = null;
      const s3 = line.slice(i, i + 3), s2 = line.slice(i, i + 2);
      if (OPS3.includes(s3)) op = s3; else if (OPS2.includes(s2)) op = s2; else if (OPS1.includes(c)) op = c;
      if (!op) throw new PyError(`SyntaxError: 알 수 없는 문자 '${c}'`, lineno);
      if ('([{'.includes(op)) depth++; if (')]}'.includes(op)) depth = Math.max(0, depth - 1);
      toks.push({ t: 'OP', v: op, line: lineno }); i += op.length;
    }
    if (depth === 0) toks.push({ t: 'NEWLINE', line: lineno });
  }
  if (depth > 0) throw new PyError('SyntaxError: 괄호가 닫히지 않았습니다', lines.length);
  while (indents.length > 1) { indents.pop(); toks.push({ t: 'DEDENT', line: lines.length }); }
  toks.push({ t: 'EOF', line: lines.length });
  return toks;
}

class Parser {
  constructor(toks) { this.toks = toks; this.p = 0; this.noIn = false; }
  peek(o = 0) { return this.toks[Math.min(this.p + o, this.toks.length - 1)]; }
  next() { return this.toks[this.p++]; }
  at(t, v) { const k = this.peek(); return k.t === t && (v === undefined || k.v === v); }
  atOp(v) { return this.at('OP', v); }
  atKw(v) { return this.at('KW', v); }
  expect(t, v) {
    const k = this.next();
    if (k.t !== t || (v !== undefined && k.v !== v)) {
      const want = v !== undefined ? `'${v}'` : ({ NEWLINE: '줄 바꿈', INDENT: '들여쓰기', NAME: '이름' }[t] || t);
      const got = k.t === 'NEWLINE' ? '줄 끝' : k.t === 'EOF' ? '코드 끝' : k.t === 'INDENT' ? '들여쓰기' : k.t === 'DEDENT' ? '들여쓰기 해제' : `'${k.v}'`;
      throw new PyError(`SyntaxError: ${want}이(가) 필요한데 ${got}이(가) 있습니다`, k.line);
    }
    return k;
  }
  parseProgram() { const body = []; while (!this.at('EOF')) { if (this.at('NEWLINE')) { this.next(); continue; } body.push(this.parseStmt()); } return body; }
  parseBlock() {
    this.expect('NEWLINE'); this.expect('INDENT'); const body = [];
    while (!this.at('DEDENT') && !this.at('EOF')) { if (this.at('NEWLINE')) { this.next(); continue; } body.push(this.parseStmt()); }
    if (this.at('DEDENT')) this.next();
    return body;
  }
  parseSuite() { if (this.at('NEWLINE')) return this.parseBlock(); return [this.parseStmt()]; }
  endSimple() {
    if (this.at('NEWLINE')) { this.next(); return; }
    if (this.at('EOF') || this.at('DEDENT')) return;
    const k = this.peek(); throw new PyError(`SyntaxError: '${k.v}' 앞에서 문장이 끝나야 합니다`, k.line);
  }
  parseStmt() {
    const k = this.peek(); const line = k.line;
    if (k.t === 'KW') {
      switch (k.v) {
        case 'if': return this.parseIf();
        case 'for': {
          this.next(); const target = this.parseTargetList(); this.expect('KW', 'in'); const iter = this.parseExprList(); this.expect('OP', ':');
          const body = this.parseSuite(); let orelse = [];
          if (this.atKw('else')) { this.next(); this.expect('OP', ':'); orelse = this.parseSuite(); }
          return { k: 'For', target, iter, body, orelse, line };
        }
        case 'while': {
          this.next(); const test = this.parseExpr(); this.expect('OP', ':'); const body = this.parseSuite(); let orelse = [];
          if (this.atKw('else')) { this.next(); this.expect('OP', ':'); orelse = this.parseSuite(); }
          return { k: 'While', test, body, orelse, line };
        }
        case 'def': {
          this.next(); const name = this.expect('NAME').v; this.expect('OP', '('); const params = [];
          while (!this.atOp(')')) { const pn = this.expect('NAME').v; let def = null; if (this.atOp('=')) { this.next(); def = this.parseExpr(); } params.push({ name: pn, def }); if (this.atOp(',')) this.next(); }
          this.expect('OP', ')'); this.expect('OP', ':'); const body = this.parseSuite();
          return { k: 'Def', name, params, body, line };
        }
        case 'return': { this.next(); let e = null; if (!this.at('NEWLINE') && !this.at('EOF')) e = this.parseExprList(); this.endSimple(); return { k: 'Return', e, line }; }
        case 'break': this.next(); this.endSimple(); return { k: 'Break', line };
        case 'continue': this.next(); this.endSimple(); return { k: 'Continue', line };
        case 'pass': this.next(); this.endSimple(); return { k: 'Pass', line };
        case 'global': { this.next(); const names = [this.expect('NAME').v]; while (this.atOp(',')) { this.next(); names.push(this.expect('NAME').v); } this.endSimple(); return { k: 'Global', names, line }; }
        case 'elif': case 'else': throw new PyError(`SyntaxError: '${k.v}'는 짝이 되는 if 없이 쓸 수 없습니다 (들여쓰기를 확인하세요)`, line);
      }
    }
    const e = this.parseExprList();
    if (this.atOp('=')) {
      const chain = [e];
      while (this.atOp('=')) { this.next(); chain.push(this.parseExprList()); }
      const value = chain.pop(); this.endSimple();
      for (const t of chain) this.checkTarget(t);
      return { k: 'Assign', targets: chain, value, line };
    }
    const aug = this.peek();
    if (aug.t === 'OP' && /^([+\-*\/%&|^]|\*\*|\/\/|<<|>>)=$/.test(aug.v)) {
      this.next(); const value = this.parseExprList(); this.endSimple(); this.checkTarget(e);
      return { k: 'Aug', target: e, op: aug.v.slice(0, -1), value, line };
    }
    this.endSimple();
    return { k: 'Expr', e, line };
  }
  checkTarget(t) {
    if (t.k === 'Name' || t.k === 'Index') return;
    if (t.k === 'Tuple' || t.k === 'List') { t.elts.forEach(x => this.checkTarget(x)); return; }
    throw new PyError('SyntaxError: 여기에는 값을 대입할 수 없습니다', t.line);
  }
  parseIf() {
    const line = this.next().line; const test = this.parseExpr(); this.expect('OP', ':'); const body = this.parseSuite(); let orelse = [];
    if (this.atKw('elif')) orelse = [this.parseIf()];
    else if (this.atKw('else')) { this.next(); this.expect('OP', ':'); orelse = this.parseSuite(); }
    return { k: 'If', test, body, orelse, line };
  }
  canStartExpr() {
    const k = this.peek();
    if (k.t === 'NUM' || k.t === 'STR' || k.t === 'FSTR' || k.t === 'NAME') return true;
    if (k.t === 'KW') return ['True', 'False', 'None', 'not'].includes(k.v);
    if (k.t === 'OP') return ['(', '[', '{', '-', '+', '~'].includes(k.v);
    return false;
  }
  parseExprList() {
    const line = this.peek().line; const e = this.parseExpr();
    if (!this.atOp(',')) return e;
    const elts = [e];
    while (this.atOp(',')) { this.next(); if (!this.canStartExpr()) break; elts.push(this.parseExpr()); }
    return { k: 'Tuple', elts, line };
  }
  parseTargetList() { const prev = this.noIn; this.noIn = true; try { return this.parseExprList(); } finally { this.noIn = prev; } }
  parseExpr() {
    const line = this.peek().line; const e = this.parseOr();
    if (this.atKw('if')) {
      this.next(); const test = this.parseOr(); this.expect('KW', 'else'); const orelse = this.parseExpr();
      return { k: 'IfExp', test, body: e, orelse, line };
    }
    return e;
  }
  parseOr() { let l = this.parseAnd(); while (this.atKw('or')) { const line = this.next().line; l = { k: 'BoolOp', op: 'or', l, r: this.parseAnd(), line }; } return l; }
  parseAnd() { let l = this.parseNot(); while (this.atKw('and')) { const line = this.next().line; l = { k: 'BoolOp', op: 'and', l, r: this.parseNot(), line }; } return l; }
  parseNot() { if (this.atKw('not')) { const line = this.next().line; return { k: 'UnOp', op: 'not', e: this.parseNot(), line }; } return this.parseCompare(); }
  parseCompare() {
    const line = this.peek().line; const first = this.parseBitOr(); const ops = [], rest = [];
    for (;;) {
      const k = this.peek(); let op = null;
      if (k.t === 'OP' && ['<', '>', '==', '>=', '<=', '!='].includes(k.v)) { op = k.v; this.next(); }
      else if (k.t === 'KW' && k.v === 'in' && !this.noIn) { op = 'in'; this.next(); }
      else if (k.t === 'KW' && k.v === 'not' && this.peek(1).t === 'KW' && this.peek(1).v === 'in' && !this.noIn) { op = 'not in'; this.next(); this.next(); }
      else if (k.t === 'KW' && k.v === 'is') { this.next(); if (this.atKw('not')) { this.next(); op = 'is not'; } else op = 'is'; }
      if (!op) break;
      ops.push(op); rest.push(this.parseBitOr());
    }
    return ops.length ? { k: 'Compare', first, ops, rest, line } : first;
  }
  binLevel(nextFn, opsList) {
    let l = nextFn();
    while (this.peek().t === 'OP' && opsList.includes(this.peek().v)) { const t = this.next(); l = { k: 'BinOp', op: t.v, l, r: nextFn(), line: t.line }; }
    return l;
  }
  parseBitOr() { return this.binLevel(() => this.parseBitXor(), ['|']); }
  parseBitXor() { return this.binLevel(() => this.parseBitAnd(), ['^']); }
  parseBitAnd() { return this.binLevel(() => this.parseShift(), ['&']); }
  parseShift() { return this.binLevel(() => this.parseArith(), ['<<', '>>']); }
  parseArith() { return this.binLevel(() => this.parseTerm(), ['+', '-']); }
  parseTerm() { return this.binLevel(() => this.parseFactor(), ['*', '/', '//', '%']); }
  parseFactor() {
    const k = this.peek();
    if (k.t === 'OP' && ['-', '+', '~'].includes(k.v)) { this.next(); return { k: 'UnOp', op: k.v, e: this.parseFactor(), line: k.line }; }
    return this.parsePower();
  }
  parsePower() {
    const base = this.parsePostfix();
    if (this.atOp('**')) { const t = this.next(); return { k: 'BinOp', op: '**', l: base, r: this.parseFactor(), line: t.line }; }
    return base;
  }
  parsePostfix() {
    let e = this.parseAtom();
    for (;;) {
      const k = this.peek();
      if (k.t !== 'OP') break;
      if (k.v === '(') {
        this.next(); const args = [], kwargs = [];
        while (!this.atOp(')')) {
          if (this.at('NAME') && this.peek(1).t === 'OP' && this.peek(1).v === '=') { const name = this.next().v; this.next(); kwargs.push({ name, value: this.parseExpr() }); }
          else if (this.atOp('*')) { const t = this.next(); args.push({ k: 'Star', e: this.parseExpr(), line: t.line }); }
          else {
            let a = this.parseExpr();
            if (this.atKw('for')) a = { k: 'ListComp', elt: a, gens: this.parseComps(), line: a.line };
            args.push(a);
          }
          if (this.atOp(',')) this.next(); else break;
        }
        this.expect('OP', ')');
        e = { k: 'Call', fn: e, args, kwargs, line: k.line };
      } else if (k.v === '[') {
        this.next(); let idx;
        if (this.atOp(':')) idx = this.parseSliceRest(null, k.line);
        else { const lo = this.parseExpr(); if (this.atOp(':')) idx = this.parseSliceRest(lo, k.line); else idx = lo; }
        this.expect('OP', ']');
        e = { k: 'Index', obj: e, idx, line: k.line };
      } else if (k.v === '.') {
        this.next(); const name = this.expect('NAME').v; e = { k: 'Attr', obj: e, name, line: k.line };
      } else break;
    }
    return e;
  }
  parseSliceRest(lo, line) {
    this.expect('OP', ':'); let hi = null, step = null;
    if (!this.atOp(':') && !this.atOp(']')) hi = this.parseExpr();
    if (this.atOp(':')) { this.next(); if (!this.atOp(']')) step = this.parseExpr(); }
    return { k: 'Slice', lo, hi, step, line };
  }
  parseComps() {
    const gens = [];
    while (this.atKw('for')) {
      this.next(); const target = this.parseTargetList(); this.expect('KW', 'in'); const iter = this.parseOr(); const ifs = [];
      while (this.atKw('if')) { this.next(); ifs.push(this.parseOr()); }
      gens.push({ target, iter, ifs });
    }
    return gens;
  }
  parseAtom() {
    const k = this.next(); const line = k.line;
    switch (k.t) {
      case 'NUM': return { k: 'Num', v: k.v, line };
      case 'STR': { let s = k.v; while (this.at('STR')) s += this.next().v; return { k: 'Str', v: s, line }; }
      case 'FSTR': return { k: 'FStr', parts: parseFString(k.v, line), line };
      case 'NAME': return { k: 'Name', id: k.v, line };
      case 'KW':
        if (k.v === 'True') return { k: 'Const', v: true, line };
        if (k.v === 'False') return { k: 'Const', v: false, line };
        if (k.v === 'None') return { k: 'Const', v: null, line };
        throw new PyError(`SyntaxError: 여기에 '${k.v}'를 쓸 수 없습니다`, line);
      case 'OP':
        if (k.v === '(') {
          if (this.atOp(')')) { this.next(); return { k: 'Tuple', elts: [], line }; }
          const e = this.parseExpr();
          if (this.atKw('for')) { const g = this.parseComps(); this.expect('OP', ')'); return { k: 'ListComp', elt: e, gens: g, line }; }
          if (this.atOp(',')) { const elts = [e]; while (this.atOp(',')) { this.next(); if (this.atOp(')')) break; elts.push(this.parseExpr()); } this.expect('OP', ')'); return { k: 'Tuple', elts, line }; }
          this.expect('OP', ')'); return e;
        }
        if (k.v === '[') {
          if (this.atOp(']')) { this.next(); return { k: 'List', elts: [], line }; }
          const e = this.parseExpr();
          if (this.atKw('for')) { const g = this.parseComps(); this.expect('OP', ']'); return { k: 'ListComp', elt: e, gens: g, line }; }
          const elts = [e];
          while (this.atOp(',')) { this.next(); if (this.atOp(']')) break; elts.push(this.parseExpr()); }
          this.expect('OP', ']'); return { k: 'List', elts, line };
        }
        if (k.v === '{') {
          const keys = [], values = [];
          while (!this.atOp('}')) { keys.push(this.parseExpr()); this.expect('OP', ':'); values.push(this.parseExpr()); if (this.atOp(',')) this.next(); else break; }
          this.expect('OP', '}'); return { k: 'Dict', keys, values, line };
        }
        break;
      case 'NEWLINE': case 'EOF': throw new PyError('SyntaxError: 식이 끝나지 않았습니다 (빈칸이 비어 있지 않은지 확인하세요)', line);
      case 'INDENT': throw new PyError('IndentationError: 예상치 못한 들여쓰기', line);
    }
    throw new PyError(`SyntaxError: '${k.v ?? k.t}' 위치에 올 수 없는 토큰입니다`, line);
  }
}

function parseFString(s, line) {
  const parts = []; let i = 0, text = '';
  while (i < s.length) {
    const c = s[i];
    if (c === '{') {
      if (s[i + 1] === '{') { text += '{'; i += 2; continue; }
      if (text) { parts.push({ text }); text = ''; }
      let depth = 1, j = i + 1;
      while (j < s.length && depth > 0) { if (s[j] === '{') depth++; else if (s[j] === '}') depth--; if (depth > 0) j++; }
      if (depth !== 0) throw new PyError('SyntaxError: f-string의 중괄호가 닫히지 않았습니다', line);
      let inner = s.slice(i + 1, j); let spec = null, conv = null;
      const m = inner.match(/^(.*?)(![rs])?(:[^:]*)?$/);
      if (m && (m[2] || m[3])) { inner = m[1]; conv = m[2] ? m[2][1] : null; spec = m[3] ? m[3].slice(1) : null; }
      const toks = tokenize(inner.trim()); const p = new Parser(toks); const expr = p.parseExpr();
      parts.push({ expr, spec, conv }); i = j + 1; continue;
    }
    if (c === '}' && s[i + 1] === '}') { text += '}'; i += 2; continue; }
    text += c; i++;
  }
  if (text) parts.push({ text });
  return parts;
}

/* ---- 값 처리 ---- */
const isNum = v => typeof v === 'number' || typeof v === 'boolean' || v instanceof PFloat;
const isFloat = v => v instanceof PFloat;
const num = v => v instanceof PFloat ? v.v : (typeof v === 'boolean' ? (v ? 1 : 0) : v);
const mkNum = (v, fl) => fl ? new PFloat(v) : v;
const isList = v => Array.isArray(v);
const typeName = v => v === null ? 'NoneType' : typeof v === 'boolean' ? 'bool' : typeof v === 'number' ? 'int' : v instanceof PFloat ? 'float' : typeof v === 'string' ? 'str' : Array.isArray(v) ? 'list' : v instanceof PTuple ? 'tuple' : v instanceof PDict ? 'dict' : (v instanceof PFunc || v instanceof PBuiltin) ? 'function' : 'object';

function fmtFloat(x) {
  if (x === Infinity) return 'inf'; if (x === -Infinity) return '-inf'; if (Number.isNaN(x)) return 'nan';
  if (Number.isInteger(x) && Math.abs(x) < 1e16) return x.toFixed(1);
  let s = String(x);
  if (Math.abs(x) >= 1e16 || (Math.abs(x) < 1e-4 && x !== 0)) s = x.toExponential().replace(/e([+-])(\d)$/, 'e$10$2');
  return s;
}
function pyrepr(v) {
  if (v === null) return 'None';
  if (typeof v === 'boolean') return v ? 'True' : 'False';
  if (typeof v === 'number') return String(v);
  if (v instanceof PFloat) return fmtFloat(v.v);
  if (typeof v === 'string') return v.includes("'") && !v.includes('"') ? `"${v}"` : `'${v.replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/\n/g, '\\n')}'`;
  if (Array.isArray(v)) return '[' + v.map(pyrepr).join(', ') + ']';
  if (v instanceof PTuple) return v.items.length === 1 ? `(${pyrepr(v.items[0])},)` : '(' + v.items.map(pyrepr).join(', ') + ')';
  if (v instanceof PDict) return '{' + [...v.m.values()].map(([k, x]) => pyrepr(k) + ': ' + pyrepr(x)).join(', ') + '}';
  if (v instanceof PFunc) return `<function ${v.name}>`;
  if (v instanceof PBuiltin) return `<built-in function ${v.name}>`;
  return String(v);
}
function pystr(v) { return typeof v === 'string' ? v : pyrepr(v); }
function truthy(v) {
  if (v === null || v === false || v === 0 || v === '') return false;
  if (v instanceof PFloat) return v.v !== 0;
  if (Array.isArray(v)) return v.length > 0;
  if (v instanceof PTuple) return v.items.length > 0;
  if (v instanceof PDict) return v.m.size > 0;
  return true;
}
function dictKey(k) {
  if (typeof k === 'number' || typeof k === 'boolean') return 'n:' + num(k);
  if (k instanceof PFloat) return 'n:' + k.v;
  if (typeof k === 'string') return 's:' + k;
  if (k instanceof PTuple) return 't:' + pyrepr(k);
  if (k === null) return 'None';
  throw new PyError(`TypeError: ${typeName(k)} 타입은 딕셔너리 키로 쓸 수 없습니다`);
}
function eq(a, b) {
  if (isNum(a) && isNum(b)) return num(a) === num(b);
  if (typeof a === 'string' && typeof b === 'string') return a === b;
  if (Array.isArray(a) && Array.isArray(b)) return a.length === b.length && a.every((x, i) => eq(x, b[i]));
  if (a instanceof PTuple && b instanceof PTuple) return eq(a.items, b.items);
  if (a instanceof PDict && b instanceof PDict) return a.m.size === b.m.size && [...a.m.keys()].every(k => b.m.has(k) && eq(a.m.get(k)[1], b.m.get(k)[1]));
  return a === b;
}
function cmp(a, b, line) {
  if (isNum(a) && isNum(b)) { const x = num(a), y = num(b); return x < y ? -1 : x > y ? 1 : 0; }
  if (typeof a === 'string' && typeof b === 'string') return a < b ? -1 : a > b ? 1 : 0;
  const la = Array.isArray(a) ? a : a instanceof PTuple ? a.items : null;
  const lb = Array.isArray(b) ? b : b instanceof PTuple ? b.items : null;
  if (la && lb && (Array.isArray(a) === Array.isArray(b))) {
    for (let i = 0; i < Math.min(la.length, lb.length); i++) { const c = cmp(la[i], lb[i], line); if (c !== 0) return c; }
    return la.length - lb.length;
  }
  throw new PyError(`TypeError: '${typeName(a)}'와 '${typeName(b)}'는 크기를 비교할 수 없습니다`, line);
}
function copyVal(v) {
  if (Array.isArray(v)) return v.map(copyVal);
  if (v instanceof PTuple) return new PTuple(v.items.map(copyVal));
  if (v instanceof PDict) { const d = new PDict(); for (const [k, e] of v.m) d.m.set(k, [e[0], copyVal(e[1])]); return d; }
  return v;
}
function toIter(v, line) {
  if (Array.isArray(v)) return v;
  if (typeof v === 'string') return [...v];
  if (v instanceof PTuple) return v.items;
  if (v instanceof PDict) return [...v.m.values()].map(e => e[0]);
  throw new PyError(`TypeError: '${typeName(v)}' 타입은 반복(iterate)할 수 없습니다`, line);
}
function normIndex(i, len, line, what) {
  if (!isNum(i) || isFloat(i)) throw new PyError(`TypeError: ${what} 인덱스는 정수여야 합니다 (${typeName(i)} 사용)`, line);
  let n = num(i); if (n < 0) n += len;
  if (n < 0 || n >= len) throw new PyError(`IndexError: ${what} 인덱스 ${num(i)}은(는) 범위를 벗어났습니다 (길이 ${len})`, line);
  return n;
}
function applySlice(seq, lo, hi, step, line) {
  const len = seq.length; step = step === null ? 1 : num(step);
  if (step === 0) throw new PyError('ValueError: 슬라이스 step은 0이 될 수 없습니다', line);
  const clampIdx = (v, dflt) => { if (v === null) return dflt; let n = num(v); if (n < 0) n += len; return n; };
  let out = [];
  if (step > 0) {
    let s = Math.max(0, Math.min(len, clampIdx(lo, 0))), e = Math.max(0, Math.min(len, clampIdx(hi, len)));
    for (let i = s; i < e; i += step) out.push(seq[i]);
  } else {
    let s = clampIdx(lo, len - 1), e = clampIdx(hi, -len - 1);
    s = Math.min(len - 1, s); if (hi === null) e = -1;
    for (let i = s; i > e; i += step) if (i >= 0 && i < len) out.push(seq[i]);
  }
  return out;
}
function formatSpec(v, spec) {
  if (!spec) return pystr(v);
  const m = spec.match(/^(?:(.)?([<>^]))?([+\- ])?(0)?(\d+)?(,)?(?:\.(\d+))?([dfs%])?$/);
  if (!m) return pystr(v);
  const [, fill0, align0, sign, zero, width, comma, prec, type] = m;
  let s, isN = isNum(v) && typeof v !== 'boolean';
  if (type === 'f' || type === '%') { let x = num(v); if (type === '%') x *= 100; s = x.toFixed(prec !== undefined ? +prec : 6); if (type === '%') s += '%'; }
  else if (type === 'd') s = String(Math.trunc(num(v)));
  else if (isN && prec !== undefined) s = num(v).toFixed(+prec);
  else s = pystr(v);
  if (comma && isN) { const [ip, fp] = s.split('.'); s = ip.replace(/\B(?=(\d{3})+(?!\d))/g, ',') + (fp !== undefined ? '.' + fp : ''); }
  if (sign === '+' && isN && num(v) >= 0) s = '+' + s;
  const w = width ? +width : 0;
  if (s.length < w) {
    const fill = fill0 || (zero ? '0' : ' '); const align = align0 || (isN ? '>' : '<'); const pad = w - s.length;
    if (align === '>') s = fill.repeat(pad) + s; else if (align === '<') s = s + fill.repeat(pad); else s = fill.repeat(Math.floor(pad / 2)) + s + fill.repeat(pad - Math.floor(pad / 2));
  }
  return s;
}

class Interp {
  constructor(opts = {}) {
    this.stdin = (opts.stdin || '').replace(/\r/g, '').split('\n'); this.stdinPos = 0;
    this.maxSteps = opts.maxSteps || 3000;
    this.out = ''; this.steps = []; this.acc = []; this.curLine = 0; this.depth = 0; this.error = null;
    this.globalEnv = new Env(null); this.frames = [{ name: null, env: this.globalEnv }];
    this.builtins = this.makeBuiltins();
  }
  run(src) {
    try {
      const ast = new Parser(tokenize(src)).parseProgram();
      this.execBlock(ast, this.globalEnv);
    } catch (e) {
      if (e instanceof PyError) this.error = { msg: e.message, line: e.line || this.curLine };
      else if (e instanceof RangeError) this.error = { msg: 'RecursionError: 재귀 호출이 너무 깊습니다', line: this.curLine };
      else this.error = { msg: '내부 오류: ' + e.message, line: this.curLine };
    }
    this.pushSnapshot(this.error ? this.error.line : null, true);
    return this;
  }
  pushSnapshot(line, done = false) {
    const frames = this.frames.map(f => ({ name: f.name, vars: [...f.env.vars].filter(([, v]) => !(v instanceof PFunc || v instanceof PBuiltin)).map(([k, v]) => [k, copyVal(v)]) }));
    this.steps.push({ line, frames, acc: this.acc, outLen: this.out.length, done, error: done ? this.error : null });
    this.acc = [];
  }
  record(line) {
    if (this.steps.length >= this.maxSteps) throw new PyError(`실행 단계가 ${this.maxSteps}회를 넘었습니다. 무한 루프가 아닌지, 반복 범위가 너무 크지 않은지 확인하세요.`, line);
    this.pushSnapshot(line);
  }
  /* ---- 문장 ---- */
  execBlock(stmts, env) { for (const s of stmts) { const r = this.execStmt(s, env); if (r) return r; } return null; }
  execStmt(s, env) {
    this.curLine = s.line;
    switch (s.k) {
      case 'Expr': this.evalExpr(s.e, env); this.record(s.line); return null;
      case 'Assign': { const v = this.evalExpr(s.value, env); for (const t of s.targets) this.assign(t, v, env); this.record(s.line); return null; }
      case 'Aug': { const cur = this.evalExpr(s.target, env); const v = this.binop(s.op, cur, this.evalExpr(s.value, env), s.line); this.assign(s.target, v, env); this.record(s.line); return null; }
      case 'If': { const t = truthy(this.evalExpr(s.test, env)); this.record(s.line); return this.execBlock(t ? s.body : s.orelse, env); }
      case 'While': {
        for (;;) {
          this.curLine = s.line; const t = truthy(this.evalExpr(s.test, env)); this.record(s.line);
          if (!t) break;
          const r = this.execBlock(s.body, env);
          if (r === 'break') return null; if (r && r !== 'continue') return r;
        }
        return this.execBlock(s.orelse, env);
      }
      case 'For': {
        const items = toIter(this.evalExpr(s.iter, env), s.line).slice();
        for (const it of items) {
          this.curLine = s.line; this.assign(s.target, it, env); this.record(s.line);
          const r = this.execBlock(s.body, env);
          if (r === 'break') return null; if (r && r !== 'continue') return r;
        }
        return this.execBlock(s.orelse, env);
      }
      case 'Break': return 'break';
      case 'Continue': return 'continue';
      case 'Pass': this.record(s.line); return null;
      case 'Global': return null;
      case 'Return': { const v = s.e ? this.evalExpr(s.e, env) : null; this.record(s.line); return { ret: v }; }
      case 'Def': env.set(s.name, new PFunc(s.name, s.params, s.body)); this.record(s.line); return null;
    }
    throw new PyError('내부 오류: 알 수 없는 문장 ' + s.k, s.line);
  }
  pathOf(node) {
    if (node.k === 'Name') return { name: node.id, path: [] };
    if (node.k === 'Index' && node._i !== undefined) { const p = this.pathOf(node.obj); if (!p) return null; p.path.push(node._i); return p; }
    return null;
  }
  assign(t, v, env) {
    if (t.k === 'Name') { env.set(t.id, v); return; }
    if (t.k === 'Tuple' || t.k === 'List') {
      const items = toIter(v, t.line);
      if (items.length !== t.elts.length) throw new PyError(`ValueError: 값 ${items.length}개를 변수 ${t.elts.length}개에 나눠 담을 수 없습니다`, t.line);
      t.elts.forEach((e, i) => this.assign(e, items[i], env)); return;
    }
    if (t.k === 'Index') {
      const obj = this.evalExpr(t.obj, env);
      if (t.idx.k === 'Slice') throw new PyError('슬라이스 대입은 지원하지 않습니다', t.line);
      const i = this.evalExpr(t.idx, env);
      if (Array.isArray(obj)) {
        const n = normIndex(i, obj.length, t.line, 'list'); obj[n] = v; t._i = n;
        const p = this.pathOf(t); if (p) this.acc.push({ name: p.name, path: p.path, w: true });
      } else if (obj instanceof PDict) { obj.m.set(dictKey(i), [i, v]); t._i = undefined; }
      else if (typeof obj === 'string') throw new PyError('TypeError: 문자열은 변경할 수 없습니다 (str은 immutable)', t.line);
      else if (obj instanceof PTuple) throw new PyError('TypeError: 튜플은 변경할 수 없습니다 (tuple은 immutable)', t.line);
      else throw new PyError(`TypeError: '${typeName(obj)}' 타입에는 인덱스로 대입할 수 없습니다`, t.line);
      return;
    }
    throw new PyError('SyntaxError: 여기에는 값을 대입할 수 없습니다', t.line);
  }
  /* ---- 식 ---- */
  lookup(id, env, line) {
    const v = env.get(id);
    if (v !== undefined) return v;
    if (id in this.builtins) return this.builtins[id];
    throw new PyError(`NameError: '${id}'라는 이름이 정의되지 않았습니다`, line);
  }
  evalExpr(n, env) {
    switch (n.k) {
      case 'Num': return n.v;
      case 'Str': return n.v;
      case 'Const': return n.v;
      case 'FStr': return n.parts.map(p => p.text !== undefined ? p.text : formatSpec(p.conv === 'r' ? pyrepr(this.evalExpr(p.expr, env)) : this.evalExpr(p.expr, env), p.spec)).join('');
      case 'Name': return this.lookup(n.id, env, n.line);
      case 'List': return n.elts.map(e => this.evalExpr(e, env));
      case 'Tuple': return new PTuple(n.elts.map(e => this.evalExpr(e, env)));
      case 'Dict': { const d = new PDict(); n.keys.forEach((k, i) => { const kv = this.evalExpr(k, env); d.m.set(dictKey(kv), [kv, this.evalExpr(n.values[i], env)]); }); return d; }
      case 'Index': {
        const obj = this.evalExpr(n.obj, env);
        if (n.idx.k === 'Slice') {
          const lo = n.idx.lo ? this.evalExpr(n.idx.lo, env) : null, hi = n.idx.hi ? this.evalExpr(n.idx.hi, env) : null, st = n.idx.step ? this.evalExpr(n.idx.step, env) : null;
          n._i = undefined;
          if (Array.isArray(obj)) return applySlice(obj, lo, hi, st, n.line);
          if (typeof obj === 'string') return applySlice([...obj], lo, hi, st, n.line).join('');
          if (obj instanceof PTuple) return new PTuple(applySlice(obj.items, lo, hi, st, n.line));
          throw new PyError(`TypeError: '${typeName(obj)}'는 슬라이스할 수 없습니다`, n.line);
        }
        const i = this.evalExpr(n.idx, env);
        if (Array.isArray(obj)) {
          const k = normIndex(i, obj.length, n.line, 'list'); n._i = k;
          const p = this.pathOf(n); if (p) this.acc.push({ name: p.name, path: p.path, w: false });
          return obj[k];
        }
        if (typeof obj === 'string') { n._i = undefined; return obj[normIndex(i, obj.length, n.line, 'string')]; }
        if (obj instanceof PTuple) { n._i = undefined; return obj.items[normIndex(i, obj.items.length, n.line, 'tuple')]; }
        if (obj instanceof PDict) { n._i = undefined; const e = obj.m.get(dictKey(i)); if (!e) throw new PyError(`KeyError: ${pyrepr(i)} 키가 없습니다`, n.line); return e[1]; }
        throw new PyError(`TypeError: '${typeName(obj)}' 타입은 인덱싱할 수 없습니다`, n.line);
      }
      case 'Attr': throw new PyError(`'.${n.name}'은(는) 메서드 호출 형태로만 지원합니다`, n.line);
      case 'Call': {
        const kwargs = {}; for (const kw of n.kwargs) kwargs[kw.name] = this.evalExpr(kw.value, env);
        const evalArgs = () => { const out = []; for (const a of n.args) { if (a.k === 'Star') out.push(...toIter(this.evalExpr(a.e, env), a.line)); else out.push(this.evalExpr(a, env)); } return out; };
        if (n.fn.k === 'Attr') {
          const obj = this.evalExpr(n.fn.obj, env); const args = evalArgs();
          return this.callMethod(obj, n.fn.name, args, kwargs, n);
        }
        const f = this.evalExpr(n.fn, env); const args = evalArgs();
        return this.callFunction(f, args, kwargs, n.line);
      }
      case 'BinOp': return this.binop(n.op, this.evalExpr(n.l, env), this.evalExpr(n.r, env), n.line);
      case 'UnOp': {
        const v = this.evalExpr(n.e, env);
        if (n.op === 'not') return !truthy(v);
        if (!isNum(v)) throw new PyError(`TypeError: '${n.op}' 연산은 ${typeName(v)}에 쓸 수 없습니다`, n.line);
        if (n.op === '-') return mkNum(-num(v), isFloat(v));
        if (n.op === '+') return mkNum(num(v), isFloat(v));
        if (n.op === '~') return ~num(v);
        break;
      }
      case 'BoolOp': { const l = this.evalExpr(n.l, env); if (n.op === 'and') return truthy(l) ? this.evalExpr(n.r, env) : l; return truthy(l) ? l : this.evalExpr(n.r, env); }
      case 'Compare': {
        let left = this.evalExpr(n.first, env);
        for (let i = 0; i < n.ops.length; i++) {
          const right = this.evalExpr(n.rest[i], env);
          if (!this.compare(n.ops[i], left, right, n.line)) return false;
          left = right;
        }
        return true;
      }
      case 'IfExp': return truthy(this.evalExpr(n.test, env)) ? this.evalExpr(n.body, env) : this.evalExpr(n.orelse, env);
      case 'ListComp': {
        const out = []; const scope = new Env(env);
        const rec = (gi) => {
          if (gi === n.gens.length) { out.push(this.evalExpr(n.elt, scope)); return; }
          const g = n.gens[gi]; const items = toIter(this.evalExpr(g.iter, scope), n.line).slice();
          for (const it of items) {
            this.assign(g.target, it, scope);
            if (g.ifs.every(c => truthy(this.evalExpr(c, scope)))) rec(gi + 1);
            if (out.length > 200000) throw new PyError('MemoryError: 리스트가 너무 큽니다', n.line);
          }
        };
        rec(0); return out;
      }
    }
    throw new PyError('내부 오류: 알 수 없는 식 ' + n.k, n.line);
  }
  compare(op, a, b, line) {
    switch (op) {
      case '==': return eq(a, b);
      case '!=': return !eq(a, b);
      case '<': return cmp(a, b, line) < 0;
      case '>': return cmp(a, b, line) > 0;
      case '<=': return cmp(a, b, line) <= 0;
      case '>=': return cmp(a, b, line) >= 0;
      case 'in': case 'not in': {
        let r;
        if (typeof b === 'string') { if (typeof a !== 'string') throw new PyError(`TypeError: 'in <str>'의 왼쪽은 문자열이어야 합니다`, line); r = b.includes(a); }
        else if (b instanceof PDict) r = b.m.has(dictKey(a));
        else r = toIter(b, line).some(x => eq(x, a));
        return op === 'in' ? r : !r;
      }
      case 'is': return a === b || (a === null && b === null);
      case 'is not': return !(a === b);
    }
  }
  binop(op, a, b, line) {
    if (isNum(a) && isNum(b)) {
      const x = num(a), y = num(b), fl = isFloat(a) || isFloat(b);
      switch (op) {
        case '+': return mkNum(x + y, fl);
        case '-': return mkNum(x - y, fl);
        case '*': return mkNum(x * y, fl);
        case '/': if (y === 0) throw new PyError('ZeroDivisionError: 0으로 나눌 수 없습니다', line); return new PFloat(x / y);
        case '//': if (y === 0) throw new PyError('ZeroDivisionError: 0으로 나눌 수 없습니다', line); return mkNum(Math.floor(x / y), fl);
        case '%': if (y === 0) throw new PyError('ZeroDivisionError: 0으로 나눌 수 없습니다', line); return mkNum(x - Math.floor(x / y) * y, fl);
        case '**': { const r = Math.pow(x, y); return mkNum(r, fl || y < 0); }
        case '&': case '|': case '^': case '<<': case '>>': {
          if (fl) throw new PyError(`TypeError: 비트 연산 '${op}'은 정수에만 쓸 수 있습니다`, line);
          if (op === '&') return Number(BigInt(x) & BigInt(y));
          if (op === '|') return Number(BigInt(x) | BigInt(y));
          if (op === '^') return Number(BigInt(x) ^ BigInt(y));
          if (op === '<<') { if (y < 0) throw new PyError('ValueError: 음수만큼 시프트할 수 없습니다', line); return x * Math.pow(2, y); }
          if (op === '>>') { if (y < 0) throw new PyError('ValueError: 음수만큼 시프트할 수 없습니다', line); return Math.floor(x / Math.pow(2, y)); }
        }
      }
    }
    if (op === '+') {
      if (typeof a === 'string' && typeof b === 'string') return a + b;
      if (Array.isArray(a) && Array.isArray(b)) return a.concat(b);
      if (a instanceof PTuple && b instanceof PTuple) return new PTuple(a.items.concat(b.items));
      if (typeof a === 'string' || typeof b === 'string') throw new PyError(`TypeError: 문자열과 ${typeName(typeof a === 'string' ? b : a)}은(는) 바로 더할 수 없습니다. str()로 바꿔서 붙이세요`, line);
    }
    if (op === '*') {
      const rep = (seq, n) => { if (!isNum(n) || isFloat(n)) return undefined; const k = Math.max(0, num(n)); if (seq.length * k > 200000) throw new PyError('MemoryError: 시퀀스가 너무 큽니다', line); let o = []; for (let i = 0; i < k; i++) o = o.concat(seq); return o; };
      if (typeof a === 'string' && isNum(b)) return a.repeat(Math.max(0, num(b)));
      if (typeof b === 'string' && isNum(a)) return b.repeat(Math.max(0, num(a)));
      if (Array.isArray(a) && isNum(b)) { const r = rep(a, b); if (r) return r.map(copyValShallow); }
      if (Array.isArray(b) && isNum(a)) { const r = rep(b, a); if (r) return r.map(copyValShallow); }
      if (a instanceof PTuple && isNum(b)) { const r = rep(a.items, b); if (r) return new PTuple(r); }
    }
    if (op === '%' && typeof a === 'string') { const args = a instanceof PTuple ? b.items : (b instanceof PTuple ? b.items : [b]); let i = 0; return a.replace(/%[sd]/g, () => pystr(args[i++])); }
    throw new PyError(`TypeError: '${op}' 연산은 ${typeName(a)}와 ${typeName(b)} 사이에 쓸 수 없습니다`, line);
  }
  callFunction(f, args, kwargs, line) {
    if (f instanceof PBuiltin) return f.fn(args, kwargs, line);
    if (f instanceof PFunc) {
      if (this.depth > 150) throw new PyError('RecursionError: 재귀 호출이 너무 깊습니다', line);
      const local = new Env(this.globalEnv);
      if (args.length > f.params.length) throw new PyError(`TypeError: ${f.name}()은 인자를 ${f.params.length}개 받는데 ${args.length}개가 전달되었습니다`, line);
      f.params.forEach((p, i) => {
        if (i < args.length) local.set(p.name, args[i]);
        else if (p.name in kwargs) local.set(p.name, kwargs[p.name]);
        else if (p.def) local.set(p.name, this.evalExpr(p.def, this.globalEnv));
        else throw new PyError(`TypeError: ${f.name}()에 '${p.name}' 인자가 빠졌습니다`, line);
      });
      this.frames.push({ name: f.name, env: local }); this.depth++;
      const callerLine = this.curLine;
      try {
        const r = this.execBlock(f.body, local);
        return r && r.ret !== undefined ? r.ret : null;
      } finally { this.frames.pop(); this.depth--; this.curLine = callerLine; }
    }
    throw new PyError(`TypeError: '${typeName(f)}' 타입은 호출할 수 없습니다`, line);
  }
  callMethod(obj, name, args, kwargs, n) {
    const line = n.line;
    const need = (k) => { if (args.length !== k) throw new PyError(`TypeError: ${name}()은 인자 ${k}개가 필요합니다`, line); };
    if (Array.isArray(obj)) {
      const mark = (idx, w) => { const p = this.pathOf(n.fn.obj); if (p) this.acc.push({ name: p.name, path: idx === null ? p.path : p.path.concat([idx]), w }); };
      switch (name) {
        case 'append': need(1); obj.push(args[0]); mark(obj.length - 1, true); return null;
        case 'pop': { if (!obj.length) throw new PyError('IndexError: 빈 리스트에서 pop할 수 없습니다', line); const i = args.length ? normIndex(args[0], obj.length, line, 'list') : obj.length - 1; mark(i, true); return obj.splice(i, 1)[0]; }
        case 'insert': need(2); { let i = num(args[0]); if (i < 0) i = Math.max(0, i + obj.length); i = Math.min(i, obj.length); obj.splice(i, 0, args[1]); mark(i, true); return null; }
        case 'remove': need(1); { const i = obj.findIndex(x => eq(x, args[0])); if (i < 0) throw new PyError(`ValueError: ${pyrepr(args[0])}이(가) 리스트에 없습니다`, line); obj.splice(i, 1); mark(null, true); return null; }
        case 'extend': need(1); obj.push(...toIter(args[0], line)); mark(null, true); return null;
        case 'index': { const i = obj.findIndex(x => eq(x, args[0])); if (i < 0) throw new PyError(`ValueError: ${pyrepr(args[0])}이(가) 리스트에 없습니다`, line); return i; }
        case 'count': need(1); return obj.filter(x => eq(x, args[0])).length;
        case 'sort': { const rev = kwargs.reverse !== undefined && truthy(kwargs.reverse); if (kwargs.key) { const key = kwargs.key; obj.sort((a, b) => cmp(this.callFunction(key, [a], {}, line), this.callFunction(key, [b], {}, line), line)); } else obj.sort((a, b) => cmp(a, b, line)); if (rev) obj.reverse(); mark(null, true); return null; }
        case 'reverse': obj.reverse(); mark(null, true); return null;
        case 'copy': return obj.slice();
        case 'clear': obj.length = 0; mark(null, true); return null;
      }
      throw new PyError(`AttributeError: 리스트에는 '${name}' 메서드가 없습니다`, line);
    }
    if (typeof obj === 'string') {
      switch (name) {
        case 'split': { if (!args.length || args[0] === null) return obj.trim().split(/\s+/).filter(s => s !== ''); return obj.split(pystr(args[0])); }
        case 'join': need(1); return toIter(args[0], line).map(x => { if (typeof x !== 'string') throw new PyError(`TypeError: join()은 문자열만 이어붙일 수 있습니다 (${typeName(x)} 포함)`, line); return x; }).join(obj);
        case 'strip': return args.length ? obj.replace(new RegExp(`^[${escapeRe(args[0])}]+|[${escapeRe(args[0])}]+$`, 'g'), '') : obj.trim();
        case 'lstrip': return obj.replace(/^\s+/, ''); case 'rstrip': return obj.replace(/\s+$/, '');
        case 'upper': return obj.toUpperCase(); case 'lower': return obj.toLowerCase();
        case 'replace': need(2); return obj.split(args[0]).join(args[1]);
        case 'count': need(1); return args[0] === '' ? obj.length + 1 : obj.split(args[0]).length - 1;
        case 'find': return obj.indexOf(args[0]);
        case 'index': { const i = obj.indexOf(args[0]); if (i < 0) throw new PyError('ValueError: 부분 문자열을 찾을 수 없습니다', line); return i; }
        case 'isdigit': return obj.length > 0 && /^[0-9]+$/.test(obj);
        case 'isalpha': return obj.length > 0 && /^[A-Za-z가-힣]+$/.test(obj);
        case 'isupper': return /[A-Z]/.test(obj) && obj === obj.toUpperCase();
        case 'islower': return /[a-z]/.test(obj) && obj === obj.toLowerCase();
        case 'startswith': return obj.startsWith(args[0]); case 'endswith': return obj.endsWith(args[0]);
        case 'zfill': return obj.padStart(num(args[0]), '0');
        case 'format': { let i = 0; return obj.replace(/\{(\d*)(?::([^}]*))?\}/g, (_, k, spec) => formatSpec(args[k === '' ? i++ : +k], spec)); }
      }
      throw new PyError(`AttributeError: 문자열에는 '${name}' 메서드가 없습니다`, line);
    }
    if (obj instanceof PDict) {
      switch (name) {
        case 'get': { const e = obj.m.get(dictKey(args[0])); return e ? e[1] : (args.length > 1 ? args[1] : null); }
        case 'keys': return [...obj.m.values()].map(e => e[0]);
        case 'values': return [...obj.m.values()].map(e => e[1]);
        case 'items': return [...obj.m.values()].map(e => new PTuple([e[0], e[1]]));
        case 'pop': { const k = dictKey(args[0]); const e = obj.m.get(k); if (!e) { if (args.length > 1) return args[1]; throw new PyError(`KeyError: ${pyrepr(args[0])}`, line); } obj.m.delete(k); return e[1]; }
      }
      throw new PyError(`AttributeError: 딕셔너리에는 '${name}' 메서드가 없습니다`, line);
    }
    throw new PyError(`AttributeError: '${typeName(obj)}' 타입에는 '${name}' 메서드가 없습니다`, line);
  }
  makeBuiltins() {
    const B = {}; const def = (name, fn) => { B[name] = new PBuiltin(name, fn); };
    const argN = (name, args, lo, hi) => { if (args.length < lo || args.length > hi) throw new PyError(`TypeError: ${name}()의 인자 개수가 잘못되었습니다 (${args.length}개)`, this.curLine); };
    def('print', (args, kw) => { const sep = kw.sep !== undefined ? pystr(kw.sep) : ' ', end = kw.end !== undefined ? pystr(kw.end) : '\n'; this.out += args.map(pystr).join(sep) + end; if (this.out.length > 200000) throw new PyError('출력이 너무 많습니다', this.curLine); return null; });
    def('range', (args, kw, line) => {
      argN('range', args, 1, 3);
      args.forEach(a => { if (!isNum(a) || isFloat(a)) throw new PyError(`TypeError: range()의 인자는 정수여야 합니다 (${typeName(a)} 사용)`, line); });
      let [s, e, st] = args.length === 1 ? [0, num(args[0]), 1] : [num(args[0]), num(args[1]), args.length === 3 ? num(args[2]) : 1];
      if (st === 0) throw new PyError('ValueError: range()의 step은 0이 될 수 없습니다', line);
      const len = Math.max(0, Math.ceil((e - s) / st)); if (len > 1000000) throw new PyError('range()가 너무 큽니다', line);
      const out = new Array(len); for (let i = 0; i < len; i++) out[i] = s + i * st; return out;
    });
    def('len', (args, kw, line) => { argN('len', args, 1, 1); const v = args[0]; if (typeof v === 'string' || Array.isArray(v)) return v.length; if (v instanceof PTuple) return v.items.length; if (v instanceof PDict) return v.m.size; throw new PyError(`TypeError: '${typeName(v)}' 타입은 len()을 쓸 수 없습니다`, line); });
    const minmax = (name, sign) => (args, kw, line) => {
      let items = args.length === 1 ? toIter(args[0], line) : args;
      if (!items.length) throw new PyError(`ValueError: ${name}()에 빈 시퀀스가 전달되었습니다`, line);
      const key = kw.key; const kv = x => key ? this.callFunction(key, [x], {}, line) : x;
      let best = items[0], bk = kv(best);
      for (let i = 1; i < items.length; i++) { const k = kv(items[i]); if (cmp(k, bk, line) * sign > 0) { best = items[i]; bk = k; } }
      return best;
    };
    def('max', minmax('max', 1)); def('min', minmax('min', -1));
    def('sum', (args, kw, line) => { argN('sum', args, 1, 2); let acc = args.length > 1 ? args[1] : 0; for (const x of toIter(args[0], line)) acc = this.binop('+', acc, x, line); return acc; });
    def('abs', (args, kw, line) => { argN('abs', args, 1, 1); if (!isNum(args[0])) throw new PyError(`TypeError: abs()는 숫자에만 쓸 수 있습니다`, line); return mkNum(Math.abs(num(args[0])), isFloat(args[0])); });
    def('int', (args, kw, line) => { argN('int', args, 0, 2); if (!args.length) return 0; const v = args[0]; if (typeof v === 'string') { const s = v.trim(); const base = args.length > 1 ? num(args[1]) : 10; const n = parseInt(s, base); if (Number.isNaN(n) || !new RegExp(base === 10 ? '^[+-]?\\d+$' : '^[+-]?[0-9a-zA-Z]+$').test(s)) throw new PyError(`ValueError: '${v}'는 정수로 바꿀 수 없습니다`, line); return n; } if (isNum(v)) return Math.trunc(num(v)); throw new PyError(`TypeError: ${typeName(v)}은(는) int()로 바꿀 수 없습니다`, line); });
    def('float', (args, kw, line) => { argN('float', args, 0, 1); if (!args.length) return new PFloat(0); const v = args[0]; if (typeof v === 'string') { const s = v.trim().toLowerCase(); if (s === 'inf' || s === '+inf' || s === 'infinity') return new PFloat(Infinity); if (s === '-inf' || s === '-infinity') return new PFloat(-Infinity); const f = Number(s); if (s === '' || Number.isNaN(f)) throw new PyError(`ValueError: '${v}'는 실수로 바꿀 수 없습니다`, line); return new PFloat(f); } if (isNum(v)) return new PFloat(num(v)); throw new PyError(`TypeError: ${typeName(v)}은(는) float()로 바꿀 수 없습니다`, line); });
    def('str', (args) => args.length ? pystr(args[0]) : '');
    def('bool', (args) => args.length ? truthy(args[0]) : false);
    def('list', (args, kw, line) => args.length ? toIter(args[0], line).slice() : []);
    def('tuple', (args, kw, line) => new PTuple(args.length ? toIter(args[0], line).slice() : []));
    def('dict', () => new PDict());
    def('enumerate', (args, kw, line) => { const s = args.length > 1 ? num(args[1]) : (kw.start !== undefined ? num(kw.start) : 0); return toIter(args[0], line).map((x, i) => new PTuple([i + s, x])); });
    def('sorted', (args, kw, line) => { const a = toIter(args[0], line).slice(); const key = kw.key; if (key) a.sort((x, y) => cmp(this.callFunction(key, [x], {}, line), this.callFunction(key, [y], {}, line), line)); else a.sort((x, y) => cmp(x, y, line)); if (kw.reverse !== undefined && truthy(kw.reverse)) a.reverse(); return a; });
    def('reversed', (args, kw, line) => toIter(args[0], line).slice().reverse());
    def('zip', (args, kw, line) => { const ls = args.map(a => toIter(a, line)); const n = ls.length ? Math.min(...ls.map(l => l.length)) : 0; const out = []; for (let i = 0; i < n; i++) out.push(new PTuple(ls.map(l => l[i]))); return out; });
    def('map', (args, kw, line) => { argN('map', args, 2, 2); return toIter(args[1], line).map(x => this.callFunction(args[0], [x], {}, line)); });
    def('filter', (args, kw, line) => { argN('filter', args, 2, 2); return toIter(args[1], line).filter(x => args[0] === null ? truthy(x) : truthy(this.callFunction(args[0], [x], {}, line))); });
    def('any', (args, kw, line) => toIter(args[0], line).some(truthy));
    def('all', (args, kw, line) => toIter(args[0], line).every(truthy));
    def('round', (args, kw, line) => { argN('round', args, 1, 2); const x = num(args[0]); if (args.length === 1 || args[1] === null) { const r = Math.round(x); return (Math.abs(x % 1) === 0.5 && r % 2 !== 0) ? r - 1 : r; } const p = Math.pow(10, num(args[1])); return new PFloat(Math.round(x * p) / p); });
    def('divmod', (args, kw, line) => new PTuple([this.binop('//', args[0], args[1], line), this.binop('%', args[0], args[1], line)]));
    def('pow', (args, kw, line) => args.length === 3 ? Number(BigInt(num(args[0])) ** BigInt(num(args[1])) % BigInt(num(args[2]))) : this.binop('**', args[0], args[1], line));
    def('ord', (args) => args[0].codePointAt(0)); def('chr', (args) => String.fromCodePoint(num(args[0])));
    def('type', (args) => `<class '${typeName(args[0])}'>`);
    def('isinstance', (args) => { const t = args[1]; const tn = typeName(args[0]); const names = (Array.isArray(t) ? t : t instanceof PTuple ? t.items : [t]).map(x => x instanceof PBuiltin ? x.name : x); return names.includes(tn) || (tn === 'bool' && names.includes('int')); });
    def('input', (args) => { if (args.length) this.out += pystr(args[0]); if (this.stdinPos >= this.stdin.length) throw new PyError('EOFError: 더 읽을 입력이 없습니다 (입력 칸을 확인하세요)', this.curLine); return this.stdin[this.stdinPos++]; });
    return B;
  }
}
function copyValShallow(v) { return v; }
function escapeRe(s) { return s.replace(/[.*+?^${}()|[\]\\-]/g, '\\$&'); }

if (typeof module !== 'undefined') module.exports = { Interp, tokenize, Parser, PyError, PFloat, PTuple, PDict, pyrepr, pystr };
