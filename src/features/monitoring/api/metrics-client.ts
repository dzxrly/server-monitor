import axios from 'axios';
import { z } from 'zod';

import type { MetricsSnapshot } from '@/features/monitoring/api/metrics-types';

const client = axios.create({ timeout: 12_000 });
const envelopeSchema = z.object({
  apiVersion: z.literal('v1'),
  sequence: z.number(),
  sampledAt: z.string(),
});

export async function fetchMetrics(
  serverUrl: string,
  processLimit: number,
  signal?: AbortSignal,
): Promise<MetricsSnapshot> {
  const baseUrl = serverUrl.replace(/\/+$/, '');
  const response = await client.get<MetricsSnapshot>(
    `${baseUrl}/api/v1/metrics`,
    {
      params: { processLimit },
      ...(signal ? { signal } : {}),
    },
  );
  const parsed = envelopeSchema.safeParse(response.data);
  if (!parsed.success)
    throw new Error('Unsupported backend response. API v1 is required.');
  return response.data;
}
