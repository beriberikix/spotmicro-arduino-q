/**
 * Parts that come in normal and mirrored versions: which version each leg takes and how to tell them apart
 * by eye. Used by WhichSide.astro; renders in public/renders/sides from scripts/render_sides.py.
 */
export const LEGS = ['FL', 'FR', 'RL', 'RR'] as const;
export type Leg = (typeof LEGS)[number];
type Version = 'normal' | 'mirrored';

/** Leg parts: normal for the left legs, mirrored for the right. */
const BY_SIDE: Record<Leg, Version> = { FL: 'normal', RL: 'normal', FR: 'mirrored', RR: 'mirrored' };
/** The shoulder servo mount pairs diagonally, so both shoulder servo outputs on a side face outwards. */
const DIAGONAL: Record<Leg, Version> = { FL: 'normal', RR: 'normal', FR: 'mirrored', RL: 'mirrored' };

export interface Side {
	name: string;
	file: string;
	legs: Record<Leg, Version>;
	/** How the part lies in the pictures, for alt text. */
	pose: string;
	/** How to put the part down and what to look for (the orange area in the pictures). */
	tell: string;
}

export const SIDES = {
	wrist: {
		name: 'Wrist (lower leg)',
		file: 'Wrist',
		legs: BY_SIDE,
		pose: 'lying on its flat side, curved edge towards you',
		tell: 'Lay it on its flat side with the curved edge towards you. The round foot end with the small hole is on the left for the left legs, on the right for the right legs.',
	},
	'wrist-counterpart': {
		name: 'Wrist counterpart',
		file: 'Wrist_Counterpart',
		legs: BY_SIDE,
		pose: 'standing on its flat back, open side up, curved wall towards you',
		tell: 'Stand it on its flat back, open side up, with the curved wall towards you. The curve is on the left for the left legs, on the right for the right legs.',
	},
	'bearing-plate': {
		name: 'Ball-bearing knee plate',
		file: 'Limb_Ball_Bearing_Mount_long_v4',
		legs: BY_SIDE,
		pose: 'lying flat, recessed screw holes up, bearing hole towards you',
		tell: 'Lay it flat with the face where the two screw holes are recessed facing up and the bearing hole towards you. The square end with the two screw holes is on the left for the left legs, on the right for the right legs. Flipping the plate over swaps them, so check which face is up.',
	},
	'horn-plate': {
		name: 'Servo-horn knee plate',
		file: 'Limb_Servohorn_Mount_long_v4',
		legs: BY_SIDE,
		pose: 'lying flat, star-shaped horn recess up, round end towards you',
		tell: 'Lay it flat with the star-shaped horn recess facing up and the round end towards you. The square end with the two screw holes is on the right for the left legs, on the left for the right legs. Flipping the plate over swaps them, so check which face is up.',
	},
	'top-shell': {
		name: 'Upper leg top shell',
		file: 'Limb_Top_Shell_with_BB_hole',
		legs: BY_SIDE,
		pose: 'open side up, the side wall with one small hole towards you',
		tell: 'Lay it open side up with the long side wall that has one small hole towards you. The wide, notched hip end is on the left for the left legs, on the right for the right legs.',
	},
	'bottom-shell': {
		name: 'Upper leg bottom shell',
		file: 'Limb_Bottom_Shell',
		legs: BY_SIDE,
		pose: 'lying flat, rectangular servo pocket up, curved step towards you',
		tell: 'Lay it flat with the rectangular servo pocket facing up and the side with a curved step towards you. The forked hip end is on the left for the left legs, on the right for the right legs. Flipping it over swaps them, so check which face is up.',
	},
	'shoulder-mount': {
		name: 'Shoulder servo mount',
		file: 'Shoulder_Joint_Servomount_extended_BB',
		legs: DIAGONAL,
		pose: 'standing on its flat base, servo hole up, the U-shaped slot pointing away from you',
		tell: 'Stand it on its flat base, servo hole up, with the U-shaped slot at the top of the tall side wall pointing away from you. That wall is on the left for the front-left and rear-right legs, on the right for the front-right and rear-left legs.',
	},
} satisfies Record<string, Side>;
