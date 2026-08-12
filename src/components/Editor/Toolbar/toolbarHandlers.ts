/** toolbarHandlers - Async handlers for ExecutionToolbar */

type ValidateFn = () => Promise<{ valid: boolean }>;
/**
 * The executor resolves with an ExecutionResult; doExecute only awaits it, so
 * the return is left unknown rather than void - Promise<T> is not assignable to
 * Promise<void>, and narrowing it here would just push a cast to the caller.
 */
type ExecuteFn = (id: string) => Promise<unknown>;
type SetLoadingFn = (v: boolean) => void;
type SetMessageFn = (v: string | null) => void;

export async function doSave(
  save: () => Promise<void>
): Promise<void> {
  try {
    await save();
  } catch (error) {
    console.error('Failed to save:', error);
  }
}

export async function doExecute(
  workflowId: string,
  validate: ValidateFn,
  execute: ExecuteFn,
  setLoading: SetLoadingFn,
  setLoadingMessage: SetMessageFn,
  onValidationShow?: (show: boolean) => void
): Promise<void> {
  try {
    setLoading(true);
    setLoadingMessage('Validating workflow...');
    const validation = await validate();
    if (!validation.valid) {
      onValidationShow?.(true);
      setLoading(false);
      return;
    }
    setLoadingMessage('Executing workflow...');
    await execute(workflowId);
  } catch (error) {
    console.error('Failed to execute:', error);
  } finally {
    setLoading(false);
    setLoadingMessage(null);
  }
}

export async function doValidate(
  validate: ValidateFn,
  onValidationShow?: (show: boolean) => void
): Promise<void> {
  try {
    await validate();
    onValidationShow?.(true);
  } catch (error) {
    console.error('Failed to validate:', error);
  }
}
