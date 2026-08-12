/**
 * TemplateWorkflowsList - List of workflows included in a template
 */

'use client';

import React from 'react';
import { Box, Typography } from '@metabuilder/m3';
import styles from '@scss/atoms/template-detail.module.scss';
import type { TemplateWorkflow } from '@/types/template';

interface TemplateWorkflowsListProps {
  /**
   * The workflows bundled with a template. Keyed by name: TemplateWorkflow
   * carries no id, the names are unique within a template, and inventing an
   * index key here would reorder badly if the list ever became sortable.
   */
  workflows: TemplateWorkflow[];
}

export default function TemplateWorkflowsList({
  workflows,
}: TemplateWorkflowsListProps) {
  return (
    <Box component="section" className={styles.section}>
      <Typography variant="h5">
        Included Workflows ({workflows.length})
      </Typography>
      <Box className={styles.workflowsList}>
        {workflows.map((workflow) => (
          <Box
            key={workflow.name}
            className={styles.workflowItem}
          >
            <Typography variant="h6">
              {workflow.name}
            </Typography>
            <Typography
              variant="body2"
              color="text.secondary"
            >
              {workflow.description}
            </Typography>
          </Box>
        ))}
      </Box>
    </Box>
  );
}
