import type { Template } from '@metabuilder/interfaces/templates';
import type { ProjectTemplate } from '@/types/template';

/**
 * Convert the app's ProjectTemplate into the shared Template the m3 card
 * components consume.
 *
 * These two models are deliberately not the same type. ProjectTemplate is what
 * this app stores: timestamps as epoch numbers, a strict category union, and
 * workflows carrying their node graph. Template is the presentation contract:
 * ISO date strings, an open category, and workflows reduced to id/name/
 * description. Optional metadata (featured, rating, downloads) is required on
 * the presentation side, so it is defaulted here rather than left undefined for
 * a card to render as "undefined downloads".
 */
export function toSharedTemplate(template: ProjectTemplate): Template {
  return {
    id: template.id,
    name: template.name,
    description: template.description,
    longDescription: template.longDescription,
    icon: template.icon,
    color: template.color,
    category: template.category,
    difficulty: template.difficulty,
    tags: template.tags,
    workflows: template.workflows.map((workflow) => ({
      // TemplateWorkflow has no id; names are unique within a template.
      id: workflow.name,
      name: workflow.name,
      description: workflow.description,
    })),
    metadata: {
      featured: template.metadata.featured ?? false,
      rating: template.metadata.rating ?? 0,
      downloads: template.metadata.downloads ?? 0,
      author: template.metadata.author,
      createdAt: new Date(template.metadata.createdAt).toISOString(),
      updatedAt: new Date(template.metadata.updatedAt).toISOString(),
    },
  };
}
