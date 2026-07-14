import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import { unified } from '@astrojs/markdown-remark';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

export default defineConfig({
  site: 'https://knottyquant.com',
  output: 'static', // Keep it static!
  trailingSlash: 'never',
  build: {
    format: 'file', // Keep your clean file structure!
  },
  integrations: [
    mdx(),
    sitemap({
      filter: (page) => !page.endsWith('/404') && !page.endsWith('/404.html'),
      serialize: (item) => {
        const url = new URL(item.url);
        if (url.pathname !== '/' && !url.pathname.endsWith('.html')) {
          url.pathname = `${url.pathname}.html`;
        }
        return { ...item, url: url.href };
      },
      namespaces: {
        news: false,
        xhtml: false,
        video: false,
      },
    }),
  ],
  markdown: {
    processor: unified({
      remarkPlugins: [remarkMath],
      rehypePlugins: [rehypeKatex],
    }),
    shikiConfig: {
      theme: 'github-dark',
      wrap: true,
    },
  },
});