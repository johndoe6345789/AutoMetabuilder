/**
 * Narrow an M3 Select change value to a single string.
 *
 * Select reports `string | string[]` because the same component backs multiple
 * selection. Single selects never produce an array, but the type cannot say so,
 * and the alternative at each call site is a cast that would quietly stringify
 * an array as "a,b" if one ever arrived.
 */
export function singleValue(value: string | string[]): string {
  return Array.isArray(value) ? (value[0] ?? '') : value;
}
