// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

const repo = 'https://github.com/beriberikix/spotmicro-arduino-q';

// https://astro.build/config
export default defineConfig({
	site: 'https://beriberikix.github.io',
	base: '/spotmicro-arduino-q',
	integrations: [
		starlight({
			title: 'SpotMicro UNO Q Build Guide',
			description:
				'Step-by-step assembly guide for a 3D-printed SpotMicro robot dog with an Arduino UNO Q and two cameras.',
			logo: { src: './src/assets/logo.svg', replacesTitle: false },
			social: [{ icon: 'github', label: 'GitHub', href: repo }],
			editLink: { baseUrl: `${repo}/edit/main/site/` },
			customCss: ['./src/styles/custom.css'],
			lastUpdated: true,
			sidebar: [
				{ label: 'Start here', items: [
					{ label: 'About this guide', slug: 'start/about' },
					{ label: 'Robot anatomy', slug: 'start/anatomy' },
					{ label: 'Tools and supplies', slug: 'start/tools' },
					{ label: 'Parts checklist', slug: 'start/parts' },
					{ label: 'Sort the hardware', slug: 'start/hardware' },
				] },
				{ label: '1 · Prepare', items: [
					{ label: 'Fit check', slug: 'prepare/fit-check' },
					{ label: 'Clean up the prints', slug: 'prepare/prints' },
					{ label: 'Servo shield and power', slug: 'prepare/bench' },
					{ label: 'Test and centre the servos', slug: 'prepare/servos' },
				] },
				{ label: '2 · Legs', items: [
					{ label: 'Lower leg', slug: 'legs/lower-leg' },
					{ label: 'Knee joint', slug: 'legs/knee' },
					{ label: 'Upper leg', slug: 'legs/upper-leg' },
				] },
				{ label: '3 · Shoulders', items: [
					{ label: 'Hip joint', slug: 'shoulders/hip' },
					{ label: 'Shoulder servo', slug: 'shoulders/shoulder-servo' },
					{ label: 'Shoulder cover', slug: 'shoulders/cover' },
				] },
				{ label: '4 · Body', items: [
					{ label: 'Frame', slug: 'body/frame' },
					{ label: 'Shoulders into the frame', slug: 'body/install-shoulders' },
				] },
				{ label: '5 · Electronics', items: [
					{ label: 'Electronics plate', slug: 'electronics/plate' },
					{ label: 'Power wiring', slug: 'electronics/power' },
					{ label: 'Servo wiring', slug: 'electronics/servo-wiring' },
					{ label: 'Head and cameras', slug: 'electronics/head' },
				] },
				{ label: '6 · Close up', items: [
					{ label: 'Battery and covers', slug: 'close/covers' },
				] },
				{ label: '7 · Bring it to life', badge: { text: 'Soon', variant: 'caution' }, items: [
					{ label: 'First power-on', slug: 'next/power-on' },
					{ label: 'Calibration', slug: 'next/calibration' },
					{ label: 'Firmware', slug: 'next/firmware' },
				] },
				{ label: 'Reference', items: [
					{ label: 'Servo channel map', slug: 'reference/servo-map' },
					{ label: '3D model viewer', slug: 'reference/viewer' },
					{ label: 'Troubleshooting', slug: 'reference/troubleshooting' },
					{ label: 'Credits and sources', slug: 'reference/credits' },
					{ label: 'Draft: photos and videos to shoot', slug: 'reference/media-todo' },
				] },
			],
		}),
	],
});
