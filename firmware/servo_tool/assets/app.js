// servo_tool web page: the build guide's servo steps, one tab per guide page.
// Channel map and angles must match sketch/sketch.ino and the guide (site/src/data/servos.ts).

const LEGS = ['FL', 'FR', 'RL', 'RR'];
const LEG_NAME = { FL: 'Front left', FR: 'Front right', RL: 'Rear left', RR: 'Rear right' };
const JOINT_OFFSET = { shoulder: 0, hip: 1, knee: 2 };
const isLeft = (leg) => leg === 'FL' || leg === 'RL';
const ch = (leg, joint) => LEGS.indexOf(leg) * 3 + JOINT_OFFSET[joint];
const tag = (leg, joint) => `${leg}-${joint[0].toUpperCase()}`;
const side = (leg) => (isLeft(leg) ? 'left' : 'right');

const ANGLE = {
  shoulder: () => 90,
  knee: (leg) => (isLeft(leg) ? 180 : 0),
  hipStanding: (leg) => (isLeft(leg) ? 120 : 60),
  // Upper leg hanging straight down is one horn arm (60 degrees) from standing; which way depends on the servo's
  // direction, so the hip step tries the first value and checks it.
  hipDown: (leg) => (isLeft(leg) ? [60, 180] : [120, 0]),
};

const GUIDE = 'https://beriberikix.github.io/spotmicro-arduino-q';

// The shoulder servo mount pairs diagonally (see the guide's "Which servo mount?"): FL and RR take the normal file,
// FR and RL the mirrored one, so both shoulder servos on a side face outwards.
const MOUNT = { FL: 'normal', RR: 'normal', FR: 'mirrored', RL: 'mirrored' };
function mountCard(leg) {
  const v = MOUNT[leg];
  const wall = v === 'normal' ? 'left' : 'right';
  return el('div', { class: 'card which' },
    el('img', { src: `img/shoulder-mount-${v}.png`, alt: `Shoulder servo mount, ${v} version, standing on its base with the tall side wall on the ${wall}.`, width: 320, height: 240 }),
    el('div', {},
      el('h3', {}, 'Which servo mount?'),
      el('p', { html: `${LEG_NAME[leg]} takes the <b>${v}</b> mount, engraved <b>${v === 'normal' ? 'FL RR' : 'FR RL'}</b> on a hidden face.` }),
      el('p', { class: 'note' }, `No engraving? Stand it on its flat base, servo hole up, with the U-shaped slot at the top of the tall side wall pointing away from you. For this leg the tall wall (orange) is on the ${wall}.`)));
}

// ---------------------------------------------------------------- connection
const ui = new WebUI();
const conn = document.querySelector('#conn');
const statusEl = document.querySelector('#status');
let state = {};

ui.on_connect(() => {
  conn.textContent = 'connected';
  conn.classList.add('ok');
  request('state_get').then((s) => { state = s || {}; render(); });
});
ui.on_disconnect(() => {
  conn.textContent = 'disconnected: is the app running?';
  conn.classList.remove('ok');
});

const waiting = {};
for (const t of ['set', 'off', 'test', 'state_get', 'state_set']) {
  ui.on_message(`${t}_response`, (data) => {
    const q = waiting[t];
    if (q && q.length) q.shift()(data);
  });
}
function request(type, data) {
  return new Promise((resolve) => {
    (waiting[type] = waiting[type] || []).push(resolve);
    ui.send_message(type, data || {});
  });
}
async function command(type, data, label) {
  const r = await request(type, data);
  if (r && r.ok === false) {
    status(`Didn't work: ${r.error || 'no answer from the sketch'}. Is the app running and the shield powered?`, true);
    return false;
  }
  if (label) status(label);
  return true;
}
const setAngle = (c, deg) => command('set', { ch: c, deg }, `Channel ${c} → ${deg}°`);
const off = (c) => command('off', { ch: c }, c < 0 ? 'All servos off' : `Channel ${c} off`);
function status(text, bad) {
  statusEl.textContent = text;
  statusEl.style.color = bad ? 'var(--danger)' : '';
}
document.querySelector('#all-off').onclick = () => off(-1);

// ---------------------------------------------------------------- tiny DOM helpers
function el(tagName, attrs = {}, ...kids) {
  const e = document.createElement(tagName);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === 'onclick') e.onclick = v;
    else if (k === 'html') e.innerHTML = v;
    else e.setAttribute(k, v);
  }
  for (const k of kids.flat()) if (k != null) e.append(k.nodeType ? k : document.createTextNode(k));
  return e;
}
const btn = (label, onclick, cls = 'btn') => el('button', { class: cls, onclick }, label);
const steps = (...items) => el('ol', { class: 'steps' }, items.map((i) => el('li', { html: i })));
const T = (leg, joint) => `<span class="tag">${tag(leg, joint)}</span>`;

function legPicker(joint, current, onpick) {
  const box = el('div', { class: 'legs' }, el('div', { class: 'head' }, '▲ head · seen from above'));
  const order = ['FL', null, 'FR', 'RL', 'RR'];
  for (const leg of order) {
    if (leg === null) { box.append(el('div', { class: 'body' })); continue; }
    box.append(el('button', { class: leg === current ? 'on' : '', onclick: () => onpick(leg) },
      LEG_NAME[leg], el('small', {}, `${tag(leg, joint)} · channel ${ch(leg, joint)}`)));
  }
  return box;
}

// ---------------------------------------------------------------- pages
const pages = {};
let tab = 'test';
const view = { test: {}, knee: {}, hip: {}, install: {} };

pages.test = {
  title: 'Test servos',
  guide: '/prepare/servos/',
  render() {
    const v = view.test;
    const rows = [];
    for (const leg of LEGS) for (const joint of ['shoulder', 'hip', 'knee']) {
      const c = ch(leg, joint);
      rows.push(el('tr', {},
        el('td', {}, String(c)),
        el('td', { html: `${T(leg, joint)} ${LEG_NAME[leg]} ${joint}` }),
        el('td', {}, btn('Test', () => command('test', { ch: c }, `Sweeping channel ${c}`)),
          btn('0°', () => setAngle(c, 0), 'btn ghost'), btn('180°', () => setAngle(c, 180), 'btn ghost'),
          btn('Off', () => off(c), 'btn ghost'))));
    }
    return [
      el('p', { class: 'lead' }, 'Plug one servo into channel 0 and push a horn loosely onto its shaft as a pointer. Press Test: it should sweep smoothly twice and stop. Then 0° and 180°: about half a turn apart (three-quarters means a 270° servo, return it). Press Off before unplugging.'),
      el('div', { class: 'card' }, el('table', {}, rows)),
    ];
  },
};

pages.knee = {
  title: 'Knee joint',
  guide: '/legs/knee/#2-mount-onto-the-knee-servo',
  render() {
    const v = view.knee;
    const out = [el('p', { class: 'lead' }, 'Knee joint, step 2: the servohorn mount onto the knee servo. Pick the leg you are building.'),
      legPicker('knee', v.leg, (leg) => { view.knee = { leg }; render(); })];
    if (!v.leg) return out;
    const c = ch(v.leg, 'knee');
    const deg = ANGLE.knee(v.leg);
    out.push(el('div', { class: 'card' },
      steps(`Plug the lower leg's extension lead (${T(v.leg, 'knee')}) into <b>channel ${c}</b> on the shield.`),
      btn(`Move ${tag(v.leg, 'knee')} to ${deg}°`, async () => { if (await setAngle(c, deg)) { v.set = true; render(); } }),
      v.set ? steps(
        'Hold the upper-leg shells against the servohorn mount\'s square end, as if bolted on.',
        'Fold them down so they lie <b>parallel to the lower leg</b>, just above it, and push the horn onto the shaft wherever it lands. If no position is parallel, turn the horn one arm round in the mount and try again.',
        'Put the shells aside and screw the mount on with an M3×8 through the horn centre.',
      ) : null,
      v.set ? btn('Done: servo off', async () => { await off(c); view.knee = { leg: v.leg, done: true }; render(); }) : null,
      v.done ? el('p', { class: 'done' }, `${tag(v.leg, 'knee')} done. Pick the next leg.`) : null));
    return out;
  },
};

pages.hip = {
  title: 'Hip joint',
  guide: '/shoulders/hip/#4-shoulder-joint-onto-the-hip-servo',
  render() {
    const v = view.hip;
    const out = [el('p', { class: 'lead' }, 'Hip joint, step 4: the shoulder joint onto the hip servo, fitted with the upper leg hanging straight down. Pick the leg you are building.'),
      legPicker('hip', v.leg, (leg) => { view.hip = { leg, stage: 'plug' }; render(); })];
    if (!v.leg) return out;
    const leg = v.leg;
    const c = ch(leg, 'hip');
    const known = state[`hip_down_${side(leg)}`];
    const tries = known != null ? [known, ...ANGLE.hipDown(leg).filter((d) => d !== known)] : ANGLE.hipDown(leg);
    const down = tries[v.attempt || 0];
    const standing = ANGLE.hipStanding(leg);
    out.push(mountCard(leg));
    const card = el('div', { class: 'card' });
    out.push(card);

    if (v.stage === 'plug' || v.stage === 'fit') {
      card.append(steps(`Plug the hip servo's lead (${T(leg, 'hip')}) into <b>channel ${c}</b>.`));
      card.append(btn(`Move ${tag(leg, 'hip')} to ${down}°`, async () => { if (await setAngle(c, down)) { v.stage = 'fit'; render(); } }));
      if (known != null && !v.attempt) card.append(el('p', { class: 'note' }, `${down}° worked on the other ${side(leg)} leg.`));
    }
    if (v.stage === 'fit') {
      card.append(el('img', { class: 'wide', src: 'img/hip-fit-check.jpg', alt: 'Left: the upper leg hanging straight down, parallel to the servo mount\'s side walls, cable slot end up. Right: after the check it has swung up towards the bearing pin.', width: 1100, height: 622 }));
      card.append(el('p', { class: 'note' }, `Front left shown. ${leg[0] === 'F' ? 'Front legs swing towards the pin' : 'Rear legs swing away from the pin'}${isLeft(leg) ? '' : '; right legs are the mirror image'}.`));
      card.append(steps(
        'Hold the shoulder joint so the <b>upper leg hangs straight down</b>, parallel to the servo mount\'s side walls, with the cable slot end up.',
        'Push the cap\'s horn onto the hip servo shaft in the position nearest to parallel. If none is, pull it off, turn the horn one arm round in the cap and try again. <b>Don\'t screw it yet.</b>',
      ));
      card.append(btn('Check it', async () => { if (await setAngle(c, standing)) { v.stage = 'check'; render(); } }));
    }
    if (v.stage === 'check') {
      const front = leg[0] === 'F';
      card.append(el('p', {}, `${tag(leg, 'hip')} has turned 60°, one horn arm. Hold the servo mount still, cable slot end up, and watch the upper leg.`));
      card.append(el('p', { class: 'ask' }, `Did the upper leg swing up ${front ? 'towards' : 'away from'} the side of the mount with the bearing pin?`));
      card.append(el('p', { class: 'note' }, `It should now point down and ${front ? 'towards the pin' : 'away from the pin'}, about a third of the way up from straight down.`));
      card.append(btn('Yes', async () => {
        state = await request('state_set', { key: `hip_down_${side(leg)}`, value: down });
        v.stage = 'screw'; render();
      }));
      card.append(btn(`No, it swung ${front ? 'away from' : 'towards'} the pin`, () => {
        if ((v.attempt || 0) + 1 < tries.length) { v.attempt = (v.attempt || 0) + 1; v.stage = 'refit'; } else { v.stage = 'stuck'; }
        render();
      }, 'btn ghost'));
    }
    if (v.stage === 'refit') {
      card.append(steps('Pull the shoulder joint off the shaft.'));
      card.append(btn(`Move ${tag(leg, 'hip')} to ${down}°`, async () => { if (await setAngle(c, down)) { v.stage = 'fit'; render(); } }));
    }
    if (v.stage === 'screw') {
      card.append(steps('Screw the joint on with an M3×8 through the horn centre.'));
      card.append(btn('Done: servo off', async () => { await off(c); v.stage = 'done'; render(); }));
    }
    if (v.stage === 'done') card.append(el('p', { class: 'done' }, `${tag(leg, 'hip')} done. Pick the next leg.`));
    if (v.stage === 'stuck') card.append(el('p', {}, 'Neither angle swung the leg the right way. Check the lead is in the right channel and that this is the right leg, then start again.'));
    return out;
  },
};

pages.install = {
  title: 'Install shoulders',
  guide: '/body/install-shoulders/',
  render() {
    const v = view.install;
    const pair = (name, legs) => {
      const cs = legs.map((l) => ch(l, 'shoulder'));
      return el('div', { class: 'card' },
        el('h3', {}, name),
        steps(`Plug ${legs.map((l) => T(l, 'shoulder')).join(' and ')} into channels ${cs.join(' and ')}.`),
        btn(`Move both to 90°`, async () => {
          for (const c of cs) if (!(await setAngle(c, 90))) return;
          v[name] = 'set'; render();
        }),
        v[name] === 'set' ? steps('Hold both legs hanging straight down and push the outer shoulder\'s horns onto both shafts, horn arms square. Screw each on with an M3×8.') : null,
        v[name] === 'set' ? btn('Done: servos off', async () => { for (const c of cs) await off(c); v[name] = 'done'; render(); }) : null,
        v[name] === 'done' ? el('p', { class: 'done' }, `${name} done.`) : null);
    };
    return [el('p', { class: 'lead' }, 'Install shoulders, step 2: each pair of legs onto its outer shoulder at 90°.'),
      pair('Front pair', ['FL', 'FR']), pair('Rear pair', ['RL', 'RR'])];
  },
};

// ---------------------------------------------------------------- shell
function render() {
  const nav = document.querySelector('#tabs');
  nav.replaceChildren(...Object.entries(pages).map(([k, p]) =>
    el('button', { class: k === tab ? 'on' : '', onclick: () => { tab = k; render(); } }, p.title)));
  const p = pages[tab];
  document.querySelector('#page').replaceChildren(
    el('h2', {}, p.title),
    ...p.render(),
    el('p', { class: 'note', html: `Same steps as the guide: <a href="${GUIDE}${p.guide}" target="_blank" rel="noopener">${p.title}</a>.` }));
}
render();
