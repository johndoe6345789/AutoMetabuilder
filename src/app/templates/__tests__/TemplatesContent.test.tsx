/**
 * Tests for TemplatesContent component
 */

import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import TemplatesContent from '../TemplatesContent';
import type { ProjectTemplate } from '@/types/template';

const makeTemplate = (
  overrides: Partial<ProjectTemplate>
): ProjectTemplate => ({
  id: 'tpl',
  name: 'Template',
  description: 'A template',
  category: 'automation',
  icon: 'bolt',
  color: 'var(--mat-sys-primary)',
  difficulty: 'beginner',
  workflows: [],
  tags: [],
  metadata: {
    author: 'Test Author',
    version: '1.0.0',
    createdAt: 0,
    updatedAt: 0,
  },
  ...overrides,
});

const templates: ProjectTemplate[] = [
  makeTemplate({ id: 't1', name: 'Email Template', category: 'communication' }),
  // 'api' is not a TemplateCategory; integration is the closest member.
  makeTemplate({ id: 't2', name: 'HTTP Request', category: 'integration' }),
];

describe('TemplatesContent', () => {
  it('renders results count', () => {
    render(
      <TemplatesContent
        filteredTemplates={templates}
        allTemplatesCount={10}
        viewMode="grid"
        onResetFilters={jest.fn()}
      />
    );
    expect(screen.getByText('Showing 2 of 10 templates')).toBeInTheDocument();
  });

  it('renders grid view', () => {
    render(
      <TemplatesContent
        filteredTemplates={templates}
        allTemplatesCount={2}
        viewMode="grid"
        onResetFilters={jest.fn()}
      />
    );
    // Grid view renders a list with role="list"
    const list = screen.getByRole('list');
    expect(list).toBeInTheDocument();
  });

  it('renders list view', () => {
    render(
      <TemplatesContent
        filteredTemplates={templates}
        allTemplatesCount={2}
        viewMode="list"
        onResetFilters={jest.fn()}
      />
    );
    const list = screen.getByRole('list');
    expect(list).toBeInTheDocument();
  });

  it('renders empty state when no templates', () => {
    render(
      <TemplatesContent
        filteredTemplates={[]}
        allTemplatesCount={5}
        viewMode="grid"
        onResetFilters={jest.fn()}
      />
    );
    expect(screen.getByText('No templates found')).toBeInTheDocument();
  });

  it('renders "Reset Filters" button when empty', () => {
    render(
      <TemplatesContent
        filteredTemplates={[]}
        allTemplatesCount={5}
        viewMode="grid"
        onResetFilters={jest.fn()}
      />
    );
    expect(screen.getByText('Reset Filters')).toBeInTheDocument();
  });

  it('calls onResetFilters when reset button clicked', async () => {
    const onResetFilters = jest.fn();
    render(
      <TemplatesContent
        filteredTemplates={[]}
        allTemplatesCount={5}
        viewMode="grid"
        onResetFilters={onResetFilters}
      />
    );
    await userEvent.click(screen.getByText('Reset Filters'));
    expect(onResetFilters).toHaveBeenCalledTimes(1);
  });

  it('renders 0 of N when empty', () => {
    render(
      <TemplatesContent
        filteredTemplates={[]}
        allTemplatesCount={3}
        viewMode="grid"
        onResetFilters={jest.fn()}
      />
    );
    expect(screen.getByText('Showing 0 of 3 templates')).toBeInTheDocument();
  });

  it('shows emoji search icon in empty state', () => {
    render(
      <TemplatesContent
        filteredTemplates={[]}
        allTemplatesCount={5}
        viewMode="grid"
        onResetFilters={jest.fn()}
      />
    );
    expect(screen.getByText('🔍')).toBeInTheDocument();
  });
});
