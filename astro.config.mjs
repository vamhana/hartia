// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import pagefind from 'astro-pagefind';

export default defineConfig({
  site: 'https://vamhana.github.io',
  base: '/hartia',
  integrations: [mdx(), sitemap(), pagefind()],
  markdown: {
    shikiConfig: {
      theme: 'github-dark',
    },
  },
});