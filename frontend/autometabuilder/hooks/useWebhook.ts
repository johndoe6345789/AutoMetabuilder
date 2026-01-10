import { useEffect } from "react";

const emitter = new EventTarget();

export function emitWebhook(event: string, detail?: unknown) {
  emitter.dispatchEvent(new CustomEvent(event, { detail }));
}

export default function useWebhook(
  name: string,
  handler: (detail: unknown) => void,
  deps: unknown[] = []
) {
  useEffect(() => {
    const listener = (evt: Event) => {
      handler((evt as CustomEvent).detail);
    };
    emitter.addEventListener(name, listener);
    return () => emitter.removeEventListener(name, listener);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [name, handler, ...deps]);
}
