import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const entries = (await getCollection('writing'))
    .filter(({ data }) => data.status === 'published')
    .sort((a, b) => b.data.published.getTime() - a.data.published.getTime());

  return rss({
    title: 'KnottyQuant writing',
    description: 'Writing on quantitative finance, topology, model evidence, and research practice.',
    site: context.site ?? 'https://knottyquant.com',
    items: entries.map(({ data }) => ({
      title: data.title,
      description: data.summary,
      pubDate: data.published,
      link: `/writing/${data.slug}.html`,
      categories: data.topics,
    })),
  });
}
