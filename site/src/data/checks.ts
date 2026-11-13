// Every check-off in the guide, for the progress tracker on the home page.
// keys must match the ids used by <Done> on each page.
const L = ['front-left', 'front-right', 'rear-left', 'rear-right'];
const legs = (id: string) => L.map((l) => `spot-guide:${id}:${l}`);
const one = (id: string) => [`spot-guide:${id}`];
export const CHECKS: { slug: string; title: string; keys: string[] }[] = [
	{ slug: 'start/parts', title: 'Parts checklist', keys: one('parts') },
	{ slug: 'start/hardware', title: 'Sort the hardware', keys: one('hardware') },
	{ slug: 'prepare/fit-check', title: 'Fit check', keys: one('fit-check') },
	{ slug: 'prepare/prints', title: 'Clean up the prints', keys: one('prints') },
	{ slug: 'prepare/bench', title: 'Servo shield and power', keys: one('bench') },
	{ slug: 'prepare/servos', title: 'Test and centre the servos', keys: one('servos') },
	{ slug: 'legs/lower-leg', title: 'Lower legs', keys: legs('lower-leg') },
	{ slug: 'legs/knee', title: 'Knee joints', keys: legs('knee') },
	{ slug: 'legs/upper-leg', title: 'Upper legs', keys: legs('upper-leg') },
	{ slug: 'shoulders/hip', title: 'Hip joints', keys: legs('hip') },
	{ slug: 'shoulders/shoulder-servo', title: 'Shoulder servos', keys: legs('shoulder-servo') },
	{ slug: 'shoulders/cover', title: 'Shoulder covers', keys: legs('cover') },
	{ slug: 'body/frame', title: 'Frame', keys: one('frame') },
	{ slug: 'body/install-shoulders', title: 'Shoulders into the frame', keys: one('install-shoulders') },
	{ slug: 'electronics/plate', title: 'Electronics plate', keys: one('plate') },
	{ slug: 'electronics/power', title: 'Power wiring', keys: one('power') },
	{ slug: 'electronics/servo-wiring', title: 'Servo wiring', keys: one('servo-wiring') },
	{ slug: 'electronics/head', title: 'Head and cameras', keys: one('head') },
	{ slug: 'close/covers', title: 'Battery and covers', keys: one('covers') },
];
