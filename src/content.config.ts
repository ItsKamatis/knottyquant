import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const artifactSchema = z.object({
  label: z.string(),
  url: z.string(),
  kind: z.enum(['data', 'document', 'source']),
});

const projects = defineCollection({
  loader: glob({ base: './src/content/projects', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    summary: z.string(),
    researchQuestion: z.string(),
    date: z.coerce.date(),
    order: z.number().int(),
    featured: z.boolean(),
    techniques: z.array(z.string()),
    dataBoundary: z.string(),
    repository: z.url().optional(),
    artifacts: z.array(artifactSchema),
    heroImage: z.string(),
    heroAlt: z.string(),
    heroWidth: z.number().int().positive(),
    heroHeight: z.number().int().positive(),
    seoDescription: z.string(),
  }),
});

const writing = defineCollection({
  loader: glob({ base: './src/content/writing', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    summary: z.string(),
    published: z.coerce.date(),
    updated: z.coerce.date().optional(),
    topics: z.array(z.string()),
    status: z.enum(['published', 'draft']),
    seoDescription: z.string(),
    references: z.array(z.object({ label: z.string(), url: z.url() })),
  }),
});

const papers = defineCollection({
  loader: glob({ base: './src/content/papers', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    summary: z.string(),
    published: z.coerce.date(),
    pdfUrl: z.string(),
    pages: z.number().int().positive(),
    topics: z.array(z.string()),
    featured: z.boolean(),
    supportingProject: z.string(),
    seoDescription: z.string(),
  }),
});

export const collections = { projects, writing, papers };
