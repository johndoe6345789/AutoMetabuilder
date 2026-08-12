/**
 * useWorkflowState - Workflow data and CRUD operations
 */

'use client';

import { useState, useEffect } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { useWorkflows } from '@metabuilder/hooks';
import type { Workflow } from '@metabuilder/components/workflow-editor';
import {
  defaultWorkflow,
  buildSavePayload,
} from './workflowStateUtils';

/**
 * The shape this editor needs from a persisted workflow. useWorkflows().getWorkflow
 * is typed Promise<unknown | null> because the storage backend is pluggable, so the
 * record is narrowed here rather than cast - a bad record then skips the load
 * instead of populating the editor with undefined fields.
 */
interface StoredWorkflow {
  id: string;
  name: string;
  description?: string;
  nodes?: Workflow['nodes'];
  createdAt: string | number | Date;
  updatedAt: string | number | Date;
}

function isStoredWorkflow(value: unknown): value is StoredWorkflow {
  if (typeof value !== 'object' || value === null) return false;
  const record = value as Record<string, unknown>;
  return typeof record.id === 'string' && typeof record.name === 'string';
}

/**
 * Navigating to a freshly created workflow needs its id and nothing else, so
 * this deliberately does not require the full StoredWorkflow shape - createWorkflow
 * returns only what the backend echoes back.
 */
function hasWorkflowId(value: unknown): value is { id: string } {
  return typeof value === 'object' && value !== null
    && typeof (value as Record<string, unknown>).id === 'string';
}

export function useWorkflowState() {
  const router = useRouter();
  const params = useParams();
  const workflowId = params?.workflowId as string;
  const {
    getWorkflow,
    createWorkflow,
    updateWorkflow,
    isLoading: isSaving,
  } = useWorkflows();

  const [workflow, setWorkflow] = useState<Workflow>(
    () => defaultWorkflow(workflowId)
  );

  useEffect(() => {
    if (workflowId && workflowId !== 'new') {
      loadWorkflowData();
    }
  }, [workflowId]);

  const loadWorkflowData = async () => {
    if (!workflowId || workflowId === 'new') return;
    const data = await getWorkflow(workflowId);
    if (isStoredWorkflow(data)) {
      setWorkflow({
        id: data.id,
        name: data.name,
        description: data.description || '',
        nodes: data.nodes || [],
        connections: [],
        createdAt: new Date(data.createdAt).toISOString(),
        updatedAt: new Date(data.updatedAt).toISOString(),
      });
    }
  };

  const handleSave = async () => {
    const payload = buildSavePayload(workflow);
    if (workflowId && workflowId !== 'new') {
      await updateWorkflow(workflowId, payload);
    } else {
      const created = await createWorkflow(payload);
      if (hasWorkflowId(created)) router.push(`/editor/${created.id}`);
    }
  };

  const handleRun = async () => {
    if (workflowId && workflowId !== 'new') {
      await handleSave();
    }
    alert(
      `Workflow "${workflow.name}" execution simulated!\n\n` +
      `Nodes: ${workflow.nodes.length}\n` +
      `Connections: ${workflow.connections.length}\n\n` +
      `Full execution engine coming soon!`
    );
  };

  return {
    workflow,
    setWorkflow,
    workflowId,
    isSaving,
    handleSave,
    handleRun,
  };
}
