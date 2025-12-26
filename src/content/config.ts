import { defineCollection, z } from 'astro:content';

const lists = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
  }),
});

const projects = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    year: z.number().optional(),
    url: z.string().optional(),
    description: z.string().optional(),
  }),
});

export const collections = { lists, projects };
