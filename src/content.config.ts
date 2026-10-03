import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const music = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/music' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    language: z.enum(['ru', 'en']).default('ru'),
  }),
});

export const collections = { music };
