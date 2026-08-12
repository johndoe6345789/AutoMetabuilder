/**
 * Tests for template detail page components:
 * TemplateRelatedSection, TemplateMainContent
 */

jest.mock('@metabuilder/components/cards', () => ({
  TemplateCard: ({ template }: any) => (
    <div data-testid="template-card">{template.name}</div>
  ),
}));

jest.mock('../TemplateWorkflowsList', () => ({
  __esModule: true,
  default: ({ workflows }: any) => (
    <div data-testid="workflows-list">{workflows?.length ?? 0} workflows</div>
  ),
}));

jest.mock('../TemplateTagsSection', () => ({
  __esModule: true,
  default: ({ tags }: any) => (
    <div data-testid="tags-section">{tags?.length ?? 0} tags</div>
  ),
}));

jest.mock('../TemplateRelatedSection', () => ({
  __esModule: true,
  default: ({ relatedTemplates }: any) => (
    <div data-testid="related-section">{relatedTemplates.length} related</div>
  ),
}));

import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TemplateMainContent from '../TemplateMainContent';
import type { ProjectTemplate } from '@/types/template';

const threeWorkflows: ProjectTemplate['workflows'] = [1, 2, 3].map((n) => ({
  name: `Workflow ${n}`,
  description: `Workflow ${n} description`,
  nodes: [],
}));

const makeTemplate = (
  overrides: Partial<ProjectTemplate> = {}
): ProjectTemplate => ({
  id: 'tpl-1',
  name: 'My Template',
  description: 'A template',
  longDescription: 'A longer description',
  category: 'automation',
  icon: 'bolt',
  color: 'var(--mat-sys-primary)',
  difficulty: 'beginner',
  workflows: [],
  tags: ['tag1', 'tag2'],
  metadata: {
    author: 'Test Author',
    version: '1.0.0',
    createdAt: 0,
    updatedAt: 0,
  },
  ...overrides,
});

// ---------------------------------------------------------------------------
// TemplateRelatedSection (original, not mocked)
// ---------------------------------------------------------------------------
describe('TemplateRelatedSection', () => {
  // Note: this uses the REAL component (jest.mock above mocks it for TemplateMainContent test)
  it('renders "Related Templates" heading', () => {
    // We need to test the original component - but since we mocked it above
    // we use the jest-actual import trick
    const { default: RealComponent } = jest.requireActual('../TemplateRelatedSection');
    const { render: rtlRender, screen: _rtlScreen } = jest.requireActual('@testing-library/react');
    const { React: _r } = { React: jest.requireActual('react') };
    // Render via standard render with requireActual
    const { container } = rtlRender(
      React.createElement(RealComponent, {
        relatedTemplates: [makeTemplate({ id: 'r1', name: 'Related 1' })],
      })
    );
    expect(container.textContent).toContain('Related Templates');
  });

  it('renders nothing gracefully for empty relatedTemplates', () => {
    const { default: RealComponent } = jest.requireActual('../TemplateRelatedSection');
    const { render: rtlRender } = jest.requireActual('@testing-library/react');
    const { container } = rtlRender(
      React.createElement(RealComponent, { relatedTemplates: [] })
    );
    expect(container).not.toBeNull();
  });
});

// ---------------------------------------------------------------------------
// TemplateMainContent
// ---------------------------------------------------------------------------
describe('TemplateMainContent', () => {
  const relatedTemplates = [makeTemplate({ id: 'r1', name: 'Related 1' })];

  it('renders Overview section', () => {
    render(
      <TemplateMainContent
        template={makeTemplate()}
        relatedTemplates={relatedTemplates}
        onCreateProject={jest.fn()}
      />
    );
    expect(screen.getByText('Overview')).toBeInTheDocument();
  });

  it('renders longDescription when available', () => {
    render(
      <TemplateMainContent
        template={makeTemplate({ longDescription: 'Long desc here' })}
        relatedTemplates={relatedTemplates}
        onCreateProject={jest.fn()}
      />
    );
    expect(screen.getByText('Long desc here')).toBeInTheDocument();
  });

  it('renders description when longDescription is absent', () => {
    render(
      <TemplateMainContent
        template={makeTemplate({ longDescription: undefined, description: 'Short desc' })}
        relatedTemplates={relatedTemplates}
        onCreateProject={jest.fn()}
      />
    );
    expect(screen.getByText('Short desc')).toBeInTheDocument();
  });

  it('renders Create Project button', () => {
    render(
      <TemplateMainContent
        template={makeTemplate()}
        relatedTemplates={relatedTemplates}
        onCreateProject={jest.fn()}
      />
    );
    expect(screen.getByRole('button', { name: /create project from template/i })).toBeInTheDocument();
  });

  it('calls onCreateProject when button clicked', () => {
    const onCreateProject = jest.fn();
    render(
      <TemplateMainContent
        template={makeTemplate()}
        relatedTemplates={relatedTemplates}
        onCreateProject={onCreateProject}
      />
    );
    fireEvent.click(screen.getByRole('button', { name: /create project from template/i }));
    expect(onCreateProject).toHaveBeenCalled();
  });

  it('renders workflows list via TemplateWorkflowsList', () => {
    render(
      <TemplateMainContent
        template={makeTemplate({ workflows: threeWorkflows })}
        relatedTemplates={[]}
        onCreateProject={jest.fn()}
      />
    );
    expect(screen.getByTestId('workflows-list')).toBeInTheDocument();
  });

  it('renders tags via TemplateTagsSection', () => {
    render(
      <TemplateMainContent
        template={makeTemplate()}
        relatedTemplates={[]}
        onCreateProject={jest.fn()}
      />
    );
    expect(screen.getByTestId('tags-section')).toBeInTheDocument();
  });

  it('renders related section', () => {
    render(
      <TemplateMainContent
        template={makeTemplate()}
        relatedTemplates={relatedTemplates}
        onCreateProject={jest.fn()}
      />
    );
    expect(screen.getByTestId('related-section')).toBeInTheDocument();
  });
});
