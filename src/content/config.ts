import { defineCollection, z } from 'astro:content';

const lists = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
  }),
});

const writing = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.date().optional(),
    description: z.string().optional(),
  }),
});

export const collections = { lists, writing };
