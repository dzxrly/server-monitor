import type {
  MetricsSnapshot,
  ProcessRow,
} from '@/features/monitoring/api/metrics-types';

export function mergeProcessRows(
  processes: MetricsSnapshot['processes'],
): ProcessRow[] {
  const rowsByPid = new Map<number, ProcessRow>();

  for (const rows of [processes.cpu, processes.memory, processes.gpu]) {
    for (const row of rows) {
      const existing = rowsByPid.get(row.pid);
      const definedFields = Object.fromEntries(
        Object.entries(row).filter(([, value]) => value !== undefined),
      ) as Partial<ProcessRow>;
      const merged = {
        ...existing,
        ...definedFields,
        pid: row.pid,
        name: existing?.name ?? row.name,
      } as ProcessRow;
      rowsByPid.set(row.pid, merged);
    }
  }

  return [...rowsByPid.values()].sort(
    (left, right) =>
      (right.cpuUsagePercent ?? -1) - (left.cpuUsagePercent ?? -1) ||
      (right.memoryBytes ?? -1) - (left.memoryBytes ?? -1) ||
      left.pid - right.pid,
  );
}
