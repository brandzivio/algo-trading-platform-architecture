// Reference sketch. Kite Connect order tags must be alphanumeric and at most 20 characters.
// Keep the tag short and look up the full detail in your own audit log.

export function makeOrderTag(strategyId: number, version: number, seq: number): string {
  const tag = `S${strategyId.toString(36)}V${version.toString(36)}N${seq.toString(36)}`.toUpperCase();
  if (!/^[A-Z0-9]{1,20}$/.test(tag)) throw new Error(`Invalid order tag: ${tag}`);
  return tag;
}

// Example: makeOrderTag(42, 3, 1057) -> "S16V3NTD" (maps to a row in the audit log with the full rule set)
