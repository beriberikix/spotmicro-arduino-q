/**
 * Draft action items for the builder, parsed from the page sources: <Todo> (photos and videos to shoot) and <Check>
 * (things to confirm on a real build). Used by the per-page summary box and the reference/media-todo list.
 */
export interface Action {
	type: 'photo' | 'video' | 'check';
	id: string;
	text: string;
	/** Page slug, e.g. legs/upper-leg */
	slug: string;
	page: string;
}

const pages = import.meta.glob('../content/docs/**/*.mdx', { query: '?raw', import: 'default', eager: true }) as Record<string, string>;
const attr = (attrs: string, name: string) => new RegExp(`${name}="([^"]*)"`).exec(attrs)?.[1];
const plain = (s: string) => s.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();

export const ACTIONS: Action[] = [];
for (const [file, raw] of Object.entries(pages)) {
	const slug = file.replace('../content/docs/', '').replace(/\.mdx$/, '').replace(/\/?index$/, '');
	const page = /^title:\s*(.+)$/m.exec(raw)?.[1]?.replace(/^['"]|['"]$/g, '') ?? slug;
	// In source order, so the summary box follows the page.
	for (const m of raw.matchAll(/<(Todo|Check)\b([^>]*)>([\s\S]*?)<\/\1>/g)) {
		const [, tag, attrs, body] = m;
		const id = attr(attrs, 'id') ?? '';
		if (tag === 'Check') ACTIONS.push({ type: 'check', id, text: attr(attrs, 'title') ?? plain(body), slug, page });
		else ACTIONS.push({ type: attr(attrs, 'kind') === 'video' ? 'video' : 'photo', id, text: plain(body), slug, page });
	}
}

export const actionsFor = (slug: string) => ACTIONS.filter((a) => a.slug === slug.replace(/\/$/, ''));
export const hideDrafts = import.meta.env.PUBLIC_HIDE_TODO === '1';
export const ICON = { photo: '📷', video: '🎥', check: '🔍' } as const;
