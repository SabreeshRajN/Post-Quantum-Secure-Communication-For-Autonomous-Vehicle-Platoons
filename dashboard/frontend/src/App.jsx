import React from 'react'

/* ------------------------------------------------------------------ *
 *  V2V Platoon Monitor
 *  Pixel-for-pixel port of "Claude Design/V2V Platoon Monitor.dc.html".
 *
 *  The scripted simulation below (SCEN) drives every visual — arena,
 *  telemetry, matrix console — exactly as the design canvas does.
 *  Pressing a scenario also fires the real backend endpoint so the
 *  post-quantum crypto actually executes server-side.
 * ------------------------------------------------------------------ */

const API = 'http://localhost:8000'
const SCENARIO_ENDPOINT = { 1: 'handshake', 2: 'mitm', 3: 'mitm_off', 4: 'replay' }

/* Parse a CSS text block into a React style object so the design's
 * literal declarations can be copied across verbatim. */
function s(css) {
  const out = {}
  css.split(';').forEach((decl) => {
    const i = decl.indexOf(':')
    if (i < 0) return
    const key = decl.slice(0, i).trim()
    const val = decl.slice(i + 1).trim()
    if (!key) return
    out[key.replace(/-([a-z])/g, (_, c) => c.toUpperCase())] = val
  })
  return out
}

const C = { info: '#a8a29e', step: '#67e8f9', ok: '#4ade80', danger: '#ec3013', blocked: '#f59e0b', title: '#22d3ee', dim: '#78716c' }

const SCEN = {
  1: { label: 'SCENARIO 1', status: 'secure', steps: [
    [0, 'title', 'SCENARIO 1 :: AUTHENTICATED KEY EXCHANGE & SESSION SETUP', null, false, '', 'Both vehicles will prove who they are, then agree on a shared secret key.'],
    [220, 'info', '[CA] provisioning platoon identities: leader, follower-1', null, false, 'SETUP', 'Trusted authority issues each vehicle its certificate.'],
    [420, 'step', '[leader] sent HELLO + nonce (a3f9c1e2...)', { r: 'l2f', c: '#22d3ee' }, false, 'CONNECT', 'Leader opens the conversation with a random challenge.'],
    [520, 'info', '[follower-1] got HELLO + nonce (a3f9c1e2...)', null, false, 'CONNECT', 'Follower receives the challenge.'],
    [420, 'step', "[follower-1] sent cert 'follower-1' + Kyber public key (1184 B) + signature", { r: 'f2l', c: '#4ade80' }, false, 'AUTH', 'Follower proves its identity and shares its public key.'],
    [520, 'info', "[leader] got follower cert 'follower-1' + Kyber public key (1184 B)", null, false, 'AUTH', 'Leader receives the proof.'],
    [420, 'ok', '[leader] follower certificate verified against CA  [OK]', null, false, 'AUTH OK', 'Certificate checks out — it really is follower-1.'],
    [420, 'ok', '[leader] follower signature over its Kyber key verified  [OK]  <- blocks MITM', null, false, 'AUTH OK', 'Signature matches — this key was not swapped in transit.'],
    [420, 'step', '[leader] encapsulated shared secret; derived session key via HKDF-SHA256', null, false, 'KEY EXCHANGE', 'Leader locks a secret to the follower’s public key.'],
    [380, 'step', '[leader] sent leader cert + ciphertext + signature (mutual auth)', { r: 'l2f', c: '#22d3ee' }, false, 'KEY EXCHANGE', 'Leader sends its own proof plus the locked secret.'],
    [520, 'ok', '[follower-1] leader certificate verified against CA  [OK]', null, false, 'AUTH OK', 'Follower confirms this really is the leader.'],
    [380, 'step', '[follower-1] decapsulated shared secret; derived matching session key', null, false, 'KEY EXCHANGE', 'Follower unlocks the same secret — keys now match.'],
    [380, 'ok', '== secure session established -- both sides hold the same AES-256-GCM key ==', null, false, 'SECURE', 'Encrypted channel is live.'],
    [520, 'step', '[leader] TX AEAD datagram: "SET GAP 20m"  (seq 1)', { r: 'l2f', c: '#22d3ee' }, false, 'MESSAGE', 'Leader sends an encrypted command.'],
    [600, 'ok', "[follower-1] ACK 'SET GAP 20m' by follower-1   (RTT 3.41 ms)", { r: 'f2l', c: '#4ade80' }, false, 'MESSAGE OK', 'Follower decrypts it correctly and confirms.'],
    [420, 'info', '[leader] session closed (BYE). 0 auth failures.', null, false, 'CLOSE', 'Clean session end.'],
  ] },
  2: { label: 'SCENARIO 2', status: 'blocked', steps: [
    [0, 'title', 'SCENARIO 2 :: MAN-IN-THE-MIDDLE (IDENTITY CHECKS ON)', null, false, '', 'An attacker sits between the vehicles and tries to swap in its own key — identity checks are ON.'],
    [220, 'info', '[attacker] bound 127.0.0.1:9210 -- leader is mispointed here', null, false, 'SETUP', 'Attacker positions itself on the wire.'],
    [320, 'danger', "[!] attacker generated a ROGUE CA and self-issued cert 'mitm'", null, true, 'ATTACK', 'Attacker forges a fake identity certificate.'],
    [460, 'step', '[leader] sent HELLO + nonce (7b12ee04...)', { r: 'l2m', c: '#22d3ee' }, false, 'CONNECT', 'Leader’s HELLO actually reaches the attacker first.'],
    [420, 'danger', '[!] attacker relayed HELLO to follower-1:9211', { r: 'm2f', c: '#ec3013' }, false, 'ATTACK', 'Attacker forwards it onward, staying invisible so far.'],
    [520, 'danger', '[!] attacker presents rogue cert + swapped Kyber key', { r: 'm2l', c: '#ec3013' }, false, 'ATTACK', 'Attacker tries to hand the leader its own forged key.'],
    [560, 'info', "[leader] got follower cert 'mitm' + Kyber public key (1184 B)", null, false, 'AUTH', 'Leader receives the forged cert for inspection.'],
    [460, 'blocked', '[leader] certificate chain INVALID -- not signed by the trusted platoon CA', null, false, 'AUTH FAIL', 'Leader checks the signer — it is not the real CA.'],
    [420, 'blocked', '[leader] SignatureError raised: refusing to establish a session', null, false, 'AUTH FAIL', 'Leader refuses to proceed with an unverifiable identity.'],
    [420, 'blocked', 'MITM stopped. Attack failed.', null, false, 'BLOCKED', 'No session, no key, no data — attacker gets nothing.'],
    [380, 'ok', '== platoon integrity maintained -- 0 commands leaked, 0 injected ==', null, false, 'SECURE', 'Identity checks did their job.'],
    [340, 'info', '[follower-1] also rejected the attacker (expected, both directions checked)', null, false, 'BLOCKED', 'Mutual auth means both sides independently refuse.'],
  ] },
  3: { label: 'SCENARIO 3', status: 'hacked', steps: [
    [0, 'title', 'SCENARIO 3 :: MAN-IN-THE-MIDDLE (IDENTITY CHECKS OFF)', null, false, '', 'Same attacker, same position — but identity checks are OFF, so nothing stops it.'],
    [220, 'blocked', '[config] secure=False -- Dilithium/PKI identity layer DISABLED', null, false, 'CONFIG', 'The step that would have caught the forgery is switched off.'],
    [320, 'danger', '[!] attacker bound 127.0.0.1:9220, relaying to follower-1:9221', null, true, 'ATTACK', 'Attacker inserts itself between both vehicles.'],
    [440, 'step', '[leader] sent HELLO + nonce (c40b91af...)', { r: 'l2m', c: '#22d3ee' }, false, 'CONNECT', 'Leader’s HELLO goes straight to the attacker.'],
    [420, 'danger', '[!] INSECURE mode: skipping follower identity checks', { r: 'm2f', c: '#ec3013' }, false, 'AUTH SKIPPED', 'No certificate check happens here at all.'],
    [480, 'danger', '[!] attacker established BOTH sessions -- it is now in the middle', { r: 'm2l', c: '#ec3013' }, false, 'ATTACK', 'Attacker now shares a key with each side separately.'],
    [480, 'danger', '[!] handshake completed THROUGH the attacker (no identity checks)', null, false, 'COMPROMISED', 'Both vehicles think they are talking to each other directly.'],
    [460, 'step', '[leader] TX AEAD datagram: "SET GAP 20m"  (seq 1)', { r: 'l2m', c: '#22d3ee' }, false, 'MESSAGE', 'Leader sends an encrypted command, believing it’s private.'],
    [520, 'danger', '[!] STOLEN plaintext from leader: "SET GAP 20m"', null, false, 'INTERCEPTED', 'Attacker decrypts it with its own session key and reads it.'],
    [420, 'danger', '[!] MODIFIED command before forwarding -> "BRAKE (injected by attacker)"', { r: 'm2f', c: '#ec3013' }, false, 'TAMPERED', 'Attacker swaps the command before re-encrypting it onward.'],
    [560, 'blocked', "[follower-1] ACK 'BRAKE (injected by attacker)' -- vehicle braked", { r: 'f2m', c: '#f59e0b' }, false, 'HIJACKED', 'Follower obeys the forged command — no way to detect it.'],
    [520, 'step', '[leader] TX AEAD datagram: "SET GAP 25m"  (seq 2)', { r: 'l2m', c: '#22d3ee' }, false, 'MESSAGE', 'Leader sends another command.'],
    [460, 'danger', '[!] STOLEN plaintext from leader: "SET GAP 25m"', { r: 'm2f', c: '#ec3013' }, false, 'INTERCEPTED', 'Read again — every message leaks.'],
    [480, 'danger', '== COMPROMISED: encryption alone is not enough -- 2 commands read, 1 forged ==', null, false, 'COMPROMISED', 'Encryption hid nothing from the attacker who holds a key.'],
    [380, 'info', 'Kyber + AES-256-GCM without Dilithium/PKI = no identity, no defence.', null, false, 'LESSON', 'Encryption protects data in transit; only signatures prove who sent it.'],
  ] },
  4: { label: 'SCENARIO 4', status: 'blocked', steps: [
    [0, 'title', 'SCENARIO 4 :: REPLAY ATTACK (REPLAY PROTECTION ON)', null, false, '', 'A valid encrypted packet is captured and re-sent later to trigger the action twice.'],
    [220, 'step', '[leader] encrypt("OPEN GATE") -> AEAD packet, seq 1', { r: 'l2f', c: '#a855f7' }, false, 'MESSAGE', 'Leader sends a genuine, sequence-numbered command.'],
    [520, 'ok', '[follower-1] accepts genuine command: "OPEN GATE" (seq 1)', { r: 'f2l', c: '#4ade80' }, false, 'MESSAGE OK', 'Follower actions it and records sequence 1 as seen.'],
    [460, 'danger', '[!] attacker captures this encrypted packet off the air', null, false, 'ATTACK', 'Attacker doesn’t need the key — just a copy of the bytes.'],
    [460, 'danger', '[!] attacker re-sends the SAME captured packet...', { r: 'l2f', c: '#a855f7' }, false, 'ATTACK', 'Replays the identical packet later, unmodified.'],
    [560, 'blocked', '[follower-1] replay rejected -- sequence 1 already seen (window base 1)', null, false, 'AUTH FAIL', 'Follower recognizes the sequence number as already used.'],
    [420, 'blocked', '[follower-1] packet discarded before decryption side effects', null, false, 'BLOCKED', 'Discarded before it can trigger anything twice.'],
    [380, 'ok', '== replay window held -- nonce reuse prevented ==', null, false, 'SECURE', 'Replay protection did its job.'],
    [340, 'info', 'With check_replay=False the same packet would have been actioned twice.', null, false, 'LESSON', 'Encryption alone doesn’t stop a captured packet being resent.'],
  ] },
}

class App extends React.Component {
  state = { scenario: 0, running: false, status: 'idle', logs: [], packets: [], mitm: false, flow: null }
  logRef = React.createRef()
  timers = []
  pid = 0

  componentDidMount() {
    const q = Number(new URLSearchParams(window.location.search).get('scn'))
    const first = SCEN[q] ? q : 1
    this.timers.push(setTimeout(() => this.run(first), 700))
  }
  componentWillUnmount() { this.clear() }
  componentDidUpdate(_p, prev) {
    if (prev.logs !== this.state.logs && this.logRef.current) {
      const el = this.logRef.current
      el.scrollTop = el.scrollHeight
    }
  }
  clear() { this.timers.forEach(clearTimeout); this.timers = [] }

  run(id) {
    this.clear()
    const sc = SCEN[id]
    const speed = 1

    // Kick off the real backend scenario (no-op if the API is offline).
    fetch(`${API}/api/scenario/${SCENARIO_ENDPOINT[id]}`, { method: 'POST' }).catch(() => {})

    this.setState({ scenario: id, running: true, status: 'running', logs: [], packets: [], mitm: false, flow: null })
    let t = 0
    sc.steps.forEach(([d, level, text, pkt, mitm, tag, plain]) => {
      t += d / speed
      this.timers.push(setTimeout(() => {
        this.setState((st) => ({
          logs: st.logs.concat([{ level, text, tag }]),
          mitm: mitm ? true : st.mitm,
          flow: { level, tag, plain: plain || text },
        }))
        if (pkt) this.spawn(pkt.r, pkt.c, speed)
      }, t))
    })
    this.timers.push(setTimeout(() => this.setState({ running: false, status: sc.status }), t + 500 / speed))
  }

  spawn(route, color, speed) {
    const id = ++this.pid
    const dur = (route === 'l2f' || route === 'f2l' ? 1 : 0.6) / speed
    const p = { id, style: {
      position: 'absolute', top: '50%', width: '12px', height: '12px',
      transform: 'translate(-50%,-50%)', background: color, zIndex: 6,
      boxShadow: '0 0 14px 3px ' + color, border: '1px solid rgba(255,255,255,.7)',
      animation: 'pk-' + route + ' ' + dur + 's linear forwards',
    } }
    this.setState((st) => ({ packets: st.packets.concat([p]) }))
    this.timers.push(setTimeout(() => {
      this.setState((st) => ({ packets: st.packets.filter((x) => x.id !== id) }))
    }, dur * 1000 + 40))
  }

  renderVals() {
    const { status, running, scenario, logs, packets, mitm, flow } = this.state
    const isBlocked = scenario === 2
    const isHacked = scenario === 3
    const mitmLegStroke = isHacked ? '#ec3013' : (running ? '#f59e0b' : '#57534e')
    const mitmLegDash = isHacked ? '0' : '5 6'
    const banner = !running && isBlocked ? { c: '#f59e0b', bg: 'rgba(35,24,4,.92)', t: 'CONNECTION REJECTED — forged certificate failed Dilithium verification, no session, no leak' }
      : !running && isHacked ? { c: '#ec3013', bg: 'rgba(35,6,4,.92)', t: 'SESSION HIJACKED — attacker holds two live sessions and edits every message unseen' }
        : null
    const ICON = { ok: '✓', danger: '✕', blocked: '⛔', step: '→', info: '·', title: '' }
    const map = {
      idle: ['#78716c', 'STANDBY'],
      running: ['#22d3ee', 'LINK ACTIVE'],
      secure: ['#4ade80', 'SYSTEM SECURE'],
      blocked: ['#f59e0b', 'ATTACK BLOCKED'],
      hacked: ['#ec3013', 'SYSTEM COMPROMISED'],
    }
    const [col, label] = map[status]
    const tele = [
      ['Handshake', running ? '···' : (scenario ? '11.8 ms' : '--'), col],
      ['Session RTT', scenario === 1 ? '3.41 ms' : (scenario ? '4.02 ms' : '--'), '#f5f5f4'],
      ['Packets', String(logs.filter((l) => l.level === 'step' || l.level === 'danger').length), '#f5f5f4'],
      ['Auth failures', scenario === 2 ? '2  (rejected)' : scenario === 4 ? '1  (replay)' : scenario === 3 ? '0  (checks off)' : '0', scenario === 3 ? '#ec3013' : '#f5f5f4'],
    ]
    return {
      vehicleCount: 2,
      statusLabel: label,
      statusDotStyle: { width: 10, height: 10, flex: 'none', background: col, boxShadow: '0 0 12px ' + col, animation: running || status !== 'idle' ? 'v2v-pulse 1.4s infinite' : 'none' },
      statusTextStyle: { fontSize: 12, fontWeight: 800, letterSpacing: '.16em', textTransform: 'uppercase', color: col },
      isActive1: scenario === 1, isActive2: scenario === 2, isActive3: scenario === 3, isActive4: scenario === 4,
      mitm, noMitm: !mitm, packets,
      directLineStroke: isBlocked && !running ? 'rgba(74,222,128,.5)' : 'rgba(255,255,255,.18)',
      mitmLegStroke, mitmLegDash,
      mitmLegAnim: { animation: isHacked ? 'v2v-dash 1.2s linear infinite' : (running ? 'v2v-dash 2.5s linear infinite' : 'none'), filter: isHacked ? 'drop-shadow(0 0 4px #ec3013)' : 'none' },
      mitmBadgeText: running ? 'RELAYING TRAFFIC…' : isBlocked ? '✕ REJECTED — invalid cert' : isHacked ? '● ACTIVE — reading & editing' : '',
      mitmBadgeStyle: { width: '100%', padding: '6px 12px', borderTop: '1px solid rgba(236,48,19,.4)', fontSize: 9, fontWeight: 700, letterSpacing: '.1em', textTransform: 'uppercase', color: isBlocked && !running ? '#a8a29e' : '#fca5a5', textDecoration: isBlocked && !running ? 'line-through' : 'none' },
      leaderBadgeText: !running && scenario ? (isHacked ? '✕ IDENTITY NOT CHECKED' : '✓ IDENTITY VERIFIED') : '',
      leaderBadgeStyle: { width: '100%', padding: !running && scenario ? '6px 12px' : 0, height: !running && scenario ? 'auto' : 0, overflow: 'hidden', borderTop: !running && scenario ? '1px solid rgba(34,211,238,.3)' : 'none', fontSize: 9, fontWeight: 700, letterSpacing: '.1em', textTransform: 'uppercase', color: isHacked ? '#ec3013' : '#4ade80' },
      followerBadgeText: !running && scenario ? (isHacked ? '✕ TALKING TO ATTACKER' : '✓ IDENTITY VERIFIED') : '',
      followerBadgeStyle: { width: '100%', padding: !running && scenario ? '6px 12px' : 0, height: !running && scenario ? 'auto' : 0, overflow: 'hidden', borderTop: !running && scenario ? '1px solid rgba(74,222,128,.3)' : 'none', fontSize: 9, fontWeight: 700, letterSpacing: '.1em', textTransform: 'uppercase', color: isHacked ? '#ec3013' : '#4ade80' },
      bannerText: banner ? banner.t : null,
      bannerStyle: banner ? { position: 'absolute', left: '50%', top: '12%', transform: 'translateX(-50%)', zIndex: 7, maxWidth: '72%', padding: '10px 20px', border: '2px solid ' + banner.c, background: banner.bg, color: banner.c, fontSize: 12, fontWeight: 700, letterSpacing: '.03em', textAlign: 'center', boxShadow: '0 0 24px ' + banner.c + '55' } : null,
      flowTagText: flow && flow.tag ? flow.tag : '',
      flowTagStyle: { flex: 'none', padding: '2px 8px', border: '1px solid ' + (flow ? C[flow.level] || C.info : '#57534e'), color: flow ? C[flow.level] || C.info : '#57534e', fontSize: 9, fontWeight: 700, letterSpacing: '.14em', textTransform: 'uppercase' },
      flowLineText: flow ? flow.plain : 'Press a scenario to begin.',
      flowLineStyle: { color: flow ? '#d6d3d1' : '#57534e', fontWeight: 500 },
      logCount: logs.length,
      logs: logs.map((l) => ({
        text: (l.level === 'title' ? '' : (ICON[l.level] || '·') + '  ') + l.text,
        tag: l.tag || null,
        tagStyle: { flex: 'none', padding: '1px 6px', marginRight: 8, border: '1px solid ' + (C[l.level] || C.info), color: C[l.level] || C.info, fontSize: 8, fontWeight: 700, letterSpacing: '.1em' },
        wrapStyle: { display: 'flex', alignItems: 'baseline', borderLeft: l.level === 'danger' ? '2px solid #ec3013' : l.level === 'ok' ? '2px solid #4ade80' : l.level === 'blocked' ? '2px solid #f59e0b' : '2px solid transparent', paddingLeft: 6, marginTop: l.level === 'title' ? 8 : 1, paddingBottom: 2 },
        style: {
          color: C[l.level] || C.info,
          fontWeight: l.level === 'title' || l.level === 'blocked' || l.level === 'danger' ? 700 : 400,
          paddingBottom: 2,
          borderBottom: l.level === 'title' ? '1px solid rgba(34,211,238,.35)' : 'none',
          letterSpacing: l.level === 'title' ? '.08em' : 'normal',
          textWrap: 'pretty',
        },
      })),
      arenaCaption: scenario ? SCEN[scenario].label + ' · ' + (running ? 'RUNNING' : 'COMPLETE') : 'IDLE · NO TRAFFIC',
      arenaHint: mitm ? 'rogue node interposed on the loopback path — traffic is being relayed' : 'leader ⇄ follower-1 · 3-message mutual-auth handshake over UDP',
      telemetry: tele.map(([k, v, c]) => ({ k, v, style: { fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace', fontSize: 16, fontWeight: 700, color: c } })),
      params: [
        { k: 'KEM', v: 'ML-KEM-768 (Kyber)' },
        { k: 'Signature', v: 'ML-DSA-65 (Dilithium3)' },
        { k: 'AEAD', v: 'AES-256-GCM' },
        { k: 'KDF', v: 'HKDF-SHA256' },
        { k: 'Pub key', v: '1184 B' },
        { k: 'Transport', v: 'UDP / loopback' },
        { k: 'Identity', v: scenario === 3 ? 'DISABLED' : 'CA-signed, ON' },
      ],
    }
  }

  render() {
    const v = this.renderVals()
    const btns = [
      { n: 1, cls: 'scn-cyan', label: '1. Normal Handshake', active: v.isActive1, dot: '#22d3ee' },
      { n: 2, cls: 'scn-green', label: '2. MITM — Auth ON', active: v.isActive2, dot: '#4ade80' },
      { n: 3, cls: 'scn-red', label: '3. MITM — Auth OFF', active: v.isActive3, dot: '#ec3013' },
      { n: 4, cls: 'scn-purple', label: '4. Replay Attack', active: v.isActive4, dot: '#a855f7' },
    ]

    return (
      <div style={s('display:flex; flex-direction:column; height:100vh; min-height:0; background:#08090a; background-image:linear-gradient(to right, rgba(255,255,255,.035) 1px, transparent 1px), linear-gradient(to bottom, rgba(255,255,255,.035) 1px, transparent 1px); background-size:44px 44px; color:#e7e5e4; font-family:Archivo, sans-serif; overflow:hidden;')}>

        <header style={s('display:flex; align-items:stretch; justify-content:space-between; gap:24px; padding:0; border-bottom:2px solid rgba(255,255,255,.16); background:rgba(10,11,12,.72); backdrop-filter:blur(10px); flex:none;')}>
          <div style={s('display:flex; align-items:center; gap:16px; padding:18px 26px;')}>
            <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#22d3ee" strokeWidth="1.8" strokeLinecap="square" style={{ filter: 'drop-shadow(0 0 8px rgba(34,211,238,.7))' }}>
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
              <path d="M9 12l2 2 4-4" />
            </svg>
            <div style={s('display:flex; flex-direction:column; gap:3px;')}>
              <h1 style={s('margin:0; font-size:23px; font-weight:800; letter-spacing:-.02em; text-transform:uppercase; color:#f5f5f4;')}>V2V Platoon Monitor</h1>
              <p style={s('margin:0; font-size:11px; letter-spacing:.18em; text-transform:uppercase; color:#78716c;')}>Post-Quantum Secure Vehicle Network&nbsp;&nbsp;/&nbsp;&nbsp;Team 11&nbsp;&nbsp;/&nbsp;&nbsp;SKCT</p>
            </div>
          </div>
          <div style={s('display:flex; align-items:stretch;')}>
            <div style={s('display:flex; align-items:center; gap:10px; padding:0 24px; border-left:2px solid rgba(255,255,255,.16);')}>
              <span style={v.statusDotStyle} />
              <span style={v.statusTextStyle}>{v.statusLabel}</span>
            </div>
            <div style={s('display:flex; flex-direction:column; justify-content:center; gap:4px; padding:0 22px; border-left:2px solid rgba(255,255,255,.16); min-width:112px;')}>
              <span style={s('font-size:9px; letter-spacing:.2em; color:#78716c; text-transform:uppercase;')}>Vehicles</span>
              <span style={s('font-size:15px; font-weight:700; color:#f5f5f4;')}>{v.vehicleCount} active</span>
            </div>
            <div style={s('display:flex; flex-direction:column; justify-content:center; gap:4px; padding:0 22px; border-left:2px solid rgba(255,255,255,.16);')}>
              <span style={s('font-size:9px; letter-spacing:.2em; color:#78716c; text-transform:uppercase;')}>KEM / SIG</span>
              <span style={s('font-size:15px; font-weight:700; color:#22d3ee;')}>Kyber-768 / Dilithium3</span>
            </div>
            <div style={s('display:flex; flex-direction:column; justify-content:center; gap:4px; padding:0 26px 0 22px; border-left:2px solid rgba(255,255,255,.16);')}>
              <span style={s('font-size:9px; letter-spacing:.2em; color:#78716c; text-transform:uppercase;')}>AEAD / KDF</span>
              <span style={s('font-size:15px; font-weight:700; color:#f5f5f4;')}>AES-256-GCM / HKDF</span>
            </div>
          </div>
        </header>

        <main style={s('display:grid; grid-template-columns:minmax(190px,290px) minmax(480px,1fr) minmax(240px,400px); flex:1; min-height:0; overflow-x:auto;')}>

          <aside style={s('display:flex; flex-direction:column; min-height:0; overflow-y:auto; border-right:2px solid rgba(255,255,255,.16); background:rgba(255,255,255,.02);')}>
            <div style={s('padding:14px 20px; border-bottom:2px solid rgba(255,255,255,.16); font-size:10px; font-weight:700; letter-spacing:.22em; text-transform:uppercase; color:#a8a29e;')}>Control Panel</div>
            <div style={s('display:flex; flex-direction:column; gap:10px; padding:20px;')}>
              {btns.map((b) => (
                <button key={b.n} onClick={() => this.run(b.n)} className={'scn-btn ' + b.cls}>
                  <span>{b.label}</span>
                  {b.active && <span style={{ width: 8, height: 8, background: b.dot, boxShadow: '0 0 10px ' + b.dot, animation: 'v2v-pulse 1s infinite', flex: 'none' }} />}
                </button>
              ))}
            </div>

            <div style={s('padding:14px 20px; border-top:2px solid rgba(255,255,255,.16); border-bottom:2px solid rgba(255,255,255,.16); font-size:10px; font-weight:700; letter-spacing:.22em; text-transform:uppercase; color:#a8a29e;')}>Session Parameters</div>
            <div style={s('display:flex; flex-direction:column;')}>
              {v.params.map((row) => (
                <div key={row.k} style={s('display:flex; align-items:baseline; justify-content:space-between; gap:12px; padding:10px 20px; border-bottom:1px solid rgba(255,255,255,.07);')}>
                  <span style={s('font-size:10px; letter-spacing:.14em; text-transform:uppercase; color:#78716c;')}>{row.k}</span>
                  <span style={s('font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:11px; color:#d6d3d1; text-align:right;')}>{row.v}</span>
                </div>
              ))}
            </div>

            <div style={s('margin-top:auto; padding:16px 20px; border-top:2px solid rgba(255,255,255,.16); font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:10px; line-height:1.7; color:#57534e;')}>
              demo.py · dashboard/backend/app.py<br />ws://localhost:8000/ws
            </div>
          </aside>

          <section style={s('display:flex; flex-direction:column; min-width:0; min-height:0;')}>
            <div style={s('display:flex; align-items:center; justify-content:space-between; padding:14px 22px; border-bottom:2px solid rgba(255,255,255,.16);')}>
              <span style={s('font-size:10px; font-weight:700; letter-spacing:.22em; text-transform:uppercase; color:#a8a29e;')}>Live Network Arena</span>
              <span style={s('font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:10px; letter-spacing:.1em; color:#57534e;')}>{v.arenaCaption}</span>
            </div>
            <div style={s('display:flex; align-items:center; gap:10px; padding:9px 22px; border-bottom:1px solid rgba(255,255,255,.08); font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:12px; background:rgba(255,255,255,.015);')}>
              <span style={v.flowTagStyle}>{v.flowTagText}</span>
              <span style={v.flowLineStyle}>{v.flowLineText}</span>
            </div>

            <div style={s('position:relative; flex:1; min-height:0; overflow:hidden;')}>
              <svg style={s('position:absolute; inset:0; width:100%; height:100%; z-index:0;')} preserveAspectRatio="none">
                {v.noMitm && (
                  <line x1="20%" y1="50%" x2="80%" y2="50%" stroke={v.directLineStroke} strokeWidth="2" strokeDasharray="6 8" style={{ animation: 'v2v-dash 2.5s linear infinite' }} />
                )}
                {v.mitm && (
                  <>
                    <line x1="20%" y1="50%" x2="50%" y2="50%" stroke={v.mitmLegStroke} strokeWidth="3" strokeDasharray={v.mitmLegDash} style={v.mitmLegAnim} />
                    <line x1="50%" y1="50%" x2="80%" y2="50%" stroke={v.mitmLegStroke} strokeWidth="3" strokeDasharray={v.mitmLegDash} style={v.mitmLegAnim} />
                  </>
                )}
              </svg>

              {v.bannerText && <div style={v.bannerStyle}>{v.bannerText}</div>}

              <div style={s('position:absolute; left:20%; top:50%; transform:translate(-50%,-50%); z-index:3; display:flex; flex-direction:column; align-items:flex-start; gap:0; width:clamp(112px,25%,186px); border:2px solid rgba(34,211,238,.8); background:rgba(8,20,24,.9); box-shadow:0 0 26px rgba(34,211,238,.28);')}>
                <div style={s('width:100%; padding:8px 12px; border-bottom:2px solid rgba(34,211,238,.5); font-size:9px; font-weight:700; letter-spacing:.2em; text-transform:uppercase; color:#67e8f9;')}>Node 01 · Leader</div>
                <div style={s('display:flex; align-items:center; flex-wrap:wrap; gap:8px 12px; padding:14px 12px; min-width:0;')}>
                  <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#22d3ee" strokeWidth="1.7" strokeLinecap="square"><path d="M14 16H9m10 0h2v-3.6a2 2 0 0 0-.4-1.2l-2-2.6A2 2 0 0 0 17 8H5a2 2 0 0 0-2 2v6h2" /><circle cx="7" cy="17" r="2" /><circle cx="17" cy="17" r="2" /></svg>
                  <div style={s('display:flex; flex-direction:column; gap:2px;')}>
                    <span style={s('font-size:13px; font-weight:700; color:#f5f5f4;')}>leader</span>
                    <span style={s('font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:10px; color:#0891b2;')}>127.0.0.1:9200</span>
                  </div>
                </div>
                <div style={v.leaderBadgeStyle}>{v.leaderBadgeText}</div>
              </div>

              {v.mitm && (
                <div style={s('position:absolute; left:50%; top:50%; transform:translate(-50%,-50%); z-index:4; display:flex; flex-direction:column; align-items:flex-start; width:clamp(112px,26%,196px); border:2px solid #ec3013; background:rgba(30,8,6,.94); box-shadow:0 0 40px rgba(236,48,19,.45); animation:v2v-mitm .35s ease-out;')}>
                  <div style={s('width:100%; padding:8px 12px; border-bottom:2px solid rgba(236,48,19,.6); font-size:9px; font-weight:700; letter-spacing:.2em; text-transform:uppercase; color:#f87171;')}>Rogue Node · MITM</div>
                  <div style={s('display:flex; align-items:center; flex-wrap:wrap; gap:8px 12px; padding:14px 12px; min-width:0;')}>
                    <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#ec3013" strokeWidth="1.7" strokeLinecap="square" style={{ animation: 'v2v-pulse 1.1s infinite' }}><path d="M20 13c0 5-8 9-8 9s-8-4-8-9V5l8-3 8 3z" /><path d="M12 8v4" /><path d="M12 15h.01" /></svg>
                    <div style={s('display:flex; flex-direction:column; gap:2px;')}>
                      <span style={s('font-size:13px; font-weight:700; color:#fecaca;')}>attacker</span>
                      <span style={s("font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:10px; color:#ec3013;")}>rogue CA cert 'mitm'</span>
                    </div>
                  </div>
                  <div style={v.mitmBadgeStyle}>{v.mitmBadgeText}</div>
                </div>
              )}

              <div style={s('position:absolute; left:80%; top:50%; transform:translate(-50%,-50%); z-index:3; display:flex; flex-direction:column; align-items:flex-start; width:clamp(112px,25%,186px); border:2px solid rgba(74,222,128,.8); background:rgba(8,22,14,.9); box-shadow:0 0 26px rgba(74,222,128,.24);')}>
                <div style={s('width:100%; padding:8px 12px; border-bottom:2px solid rgba(74,222,128,.5); font-size:9px; font-weight:700; letter-spacing:.2em; text-transform:uppercase; color:#86efac;')}>Node 02 · Follower</div>
                <div style={s('display:flex; align-items:center; flex-wrap:wrap; gap:8px 12px; padding:14px 12px; min-width:0;')}>
                  <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#4ade80" strokeWidth="1.7" strokeLinecap="square"><path d="M14 16H9m10 0h2v-3.6a2 2 0 0 0-.4-1.2l-2-2.6A2 2 0 0 0 17 8H5a2 2 0 0 0-2 2v6h2" /><circle cx="7" cy="17" r="2" /><circle cx="17" cy="17" r="2" /></svg>
                  <div style={s('display:flex; flex-direction:column; gap:2px;')}>
                    <span style={s('font-size:13px; font-weight:700; color:#f5f5f4;')}>follower-1</span>
                    <span style={s('font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:10px; color:#16a34a;')}>127.0.0.1:9201</span>
                  </div>
                </div>
                <div style={v.followerBadgeStyle}>{v.followerBadgeText}</div>
              </div>

              {v.packets.map((p) => (<div key={p.id} style={p.style} />))}

              <div style={s('position:absolute; left:0; right:0; bottom:0; display:flex; align-items:center; gap:10px; padding:12px 22px; border-top:1px solid rgba(255,255,255,.08); font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:11px; color:#78716c; z-index:5;')}>
                <span style={{ color: '#22d3ee' }}>▸</span>
                <span>{v.arenaHint}</span>
              </div>
            </div>

            <div style={s('display:grid; grid-template-columns:repeat(4, 1fr); border-top:2px solid rgba(255,255,255,.16); flex:none;')}>
              {v.telemetry.map((t) => (
                <div key={t.k} style={s('display:flex; flex-direction:column; gap:6px; padding:16px 20px; border-right:1px solid rgba(255,255,255,.08);')}>
                  <span style={s('font-size:9px; letter-spacing:.2em; text-transform:uppercase; color:#78716c;')}>{t.k}</span>
                  <span style={t.style}>{t.v}</span>
                </div>
              ))}
            </div>
          </section>

          <aside style={s('display:flex; flex-direction:column; min-height:0; border-left:2px solid rgba(255,255,255,.16); background:rgba(4,5,6,.75);')}>
            <div style={s('display:flex; align-items:center; justify-content:space-between; padding:14px 20px; border-bottom:2px solid rgba(255,255,255,.16);')}>
              <span style={s('font-size:10px; font-weight:700; letter-spacing:.22em; text-transform:uppercase; color:#a8a29e;')}>Live Matrix Console</span>
              <span style={s('font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:10px; color:#57534e;')}>{v.logCount} events</span>
            </div>
            <div ref={this.logRef} style={s('flex:1; min-height:0; overflow-y:auto; padding:16px 18px 24px; font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:11.5px; line-height:1.65;')}>
              {v.logs.map((line, i) => (
                <div key={i} style={line.wrapStyle}>
                  {line.tag && <span style={line.tagStyle}>{line.tag}</span>}
                  <span style={line.style}>{line.text}</span>
                </div>
              ))}
              <div style={s('display:flex; gap:6px; color:#22d3ee; margin-top:6px;')}><span>&gt;</span><span style={{ width: 7, height: 14, background: '#22d3ee', animation: 'v2v-caret 1s step-end infinite' }} /></div>
            </div>
            <div style={s('padding:12px 18px; border-top:2px solid rgba(255,255,255,.16); font-family:ui-monospace, SFMono-Regular, Menlo, monospace; font-size:10px; color:#57534e;')}>udp/loopback · pqcrypto (PQClean) · 3-msg mutual auth</div>
          </aside>
        </main>
      </div>
    )
  }
}

export default App
