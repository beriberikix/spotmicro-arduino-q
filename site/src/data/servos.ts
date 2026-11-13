// Servo channel map: shield channel -> joint. Must match firmware/servo_tool/servo_tool.ino.
export type Leg = 'FL' | 'FR' | 'RL' | 'RR';
export type JointName = 'shoulder' | 'hip' | 'knee';
export interface Servo {
	ch: number;
	leg: Leg;
	joint: JointName;
	assembly: number; // degrees when the horn is fitted
	pose: string; // what the part should look like at that angle
	route: string; // where the cable runs
}
const legName: Record<Leg, string> = { FL: 'Front left', FR: 'Front right', RL: 'Rear left', RR: 'Rear right' };
export const LEG_NAME = legName;
const left = (l: Leg) => l === 'FL' || l === 'RL';
const legs: Leg[] = ['FL', 'FR', 'RL', 'RR'];
export const SERVOS: Servo[] = legs.flatMap((leg, i) => [
	{
		ch: i * 3,
		leg,
		joint: 'shoulder' as const,
		assembly: 90,
		pose: 'Leg hangs straight down, square to the body; horn arms square to the outer shoulder plate.',
		route: 'Short lead, straight up out of the shoulder servo mount into the body.',
	},
	{
		ch: i * 3 + 1,
		leg,
		joint: 'hip' as const,
		assembly: left(leg) ? 120 : 60,
		pose: 'Upper leg at the standing angle (one horn arm, 60°, past the top arm), lower leg folded.',
		route: 'Out through the hole in the upper leg’s top shell, together with the knee lead, into the shoulder.',
	},
	{
		ch: i * 3 + 2,
		leg,
		joint: 'knee' as const,
		assembly: left(leg) ? 180 : 0,
		pose: 'Lower leg folded flat against the upper leg (the rest position).',
		route: 'Extension cable; through the gap between the upper-leg shells, in the groove under the top shell, out of the top-shell hole.',
	},
]);
