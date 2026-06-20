/**
 * Plugin runtime singleton — set during register(), used by inbound handler.
 */

let runtime: any = null;

export function setEmailRuntime(next: any) {
  runtime = next;
}

export function getEmailRuntime(): any {
  if (!runtime) {
    throw new Error("Email plugin runtime not initialized");
  }
  return runtime;
}

