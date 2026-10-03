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

const charter = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/charter' }),
  schema: z.object({
    title: z.string(),
    number: z.string(),
    book: z.number(),
    bookTitle: z.string(),
    part: z.number(),
    partTitle: z.string(),
    order: z.number(),
    source: z.string().optional(),
  }),
});

export const collections = { music, charter };
