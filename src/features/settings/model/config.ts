import { z } from 'zod';

import messages from '@/i18n';

export type PanelLayout = 'sm' | 'md' | 'lg';
export type ByteUnit = 'B' | 'KB' | 'MB' | 'GB' | 'TB';

export interface ServerConfig {
  customName: string;
  uniqueId: string;
  serverUrl: string;
  tagColor: string;
  // Kept when importing older config files. The v1 backend now auto-detects NVIDIA.
  gpuServer?: { gpuType: string } | undefined;
}

export interface AppConfig {
  darkMode: boolean;
  defaultLanguage: keyof typeof messages;
  indexPageServerPanelLayout: PanelLayout;
  serverListConfig: ServerConfig[];
  refreshTimeSec: number;
  processLimit: number;
  useFahrenheitUnit: boolean;
  freeUsageThreshold: number;
  midUsageThreshold: number;
  memoryUnit: ByteUnit;
  gpuMemoryUnit: ByteUnit;
  showBackendTipsDialog: boolean;
}

const serverSchema = z.object({
  customName: z.string().min(1).max(64),
  uniqueId: z.string().min(1),
  serverUrl: z.url().refine((value) => /^https?:\/\//i.test(value)),
  tagColor: z.string().regex(/^#[0-9a-f]{6}$/i),
  gpuServer: z.object({ gpuType: z.string() }).optional(),
});

export const partialConfigSchema = z
  .object({
    darkMode: z.boolean().optional(),
    defaultLanguage: z.string().optional(),
    indexPageServerPanelLayout: z.enum(['sm', 'md', 'lg']).optional(),
    serverListConfig: z.array(serverSchema).optional(),
    refreshTimeSec: z.number().min(1).max(3600).optional(),
    processLimit: z.number().int().min(1).max(50).optional(),
    useFahrenheitUnit: z.boolean().optional(),
    freeUsageThreshold: z.number().min(0).max(100).optional(),
    midUsageThreshold: z.number().min(0).max(100).optional(),
    memoryUnit: z.enum(['B', 'KB', 'MB', 'GB', 'TB']).optional(),
    gpuMemoryUnit: z.enum(['B', 'KB', 'MB', 'GB', 'TB']).optional(),
    showBackendTipsDialog: z.boolean().optional(),
  })
  .strict();

function browserLanguage(): keyof typeof messages {
  const language = navigator.language as keyof typeof messages;
  return Object.hasOwn(messages, language) ? language : 'en-US';
}

export function createDefaultConfig(): AppConfig {
  return {
    darkMode: false,
    defaultLanguage: browserLanguage(),
    indexPageServerPanelLayout: 'sm',
    serverListConfig: [],
    refreshTimeSec: 5,
    processLimit: 5,
    useFahrenheitUnit: false,
    freeUsageThreshold: 30,
    midUsageThreshold: 70,
    memoryUnit: 'GB',
    gpuMemoryUnit: 'GB',
    showBackendTipsDialog: true,
  };
}

export function normalizeConfig(input: unknown): AppConfig {
  const defaults = createDefaultConfig();
  const parsed = partialConfigSchema.safeParse(input);
  if (!parsed.success) return defaults;
  const language = parsed.data.defaultLanguage as
    keyof typeof messages | undefined;
  return {
    darkMode: parsed.data.darkMode ?? defaults.darkMode,
    defaultLanguage:
      language && Object.hasOwn(messages, language)
        ? language
        : defaults.defaultLanguage,
    indexPageServerPanelLayout:
      parsed.data.indexPageServerPanelLayout ??
      defaults.indexPageServerPanelLayout,
    serverListConfig: parsed.data.serverListConfig ?? defaults.serverListConfig,
    refreshTimeSec: parsed.data.refreshTimeSec ?? defaults.refreshTimeSec,
    processLimit: parsed.data.processLimit ?? defaults.processLimit,
    useFahrenheitUnit:
      parsed.data.useFahrenheitUnit ?? defaults.useFahrenheitUnit,
    freeUsageThreshold:
      parsed.data.freeUsageThreshold ?? defaults.freeUsageThreshold,
    midUsageThreshold:
      parsed.data.midUsageThreshold ?? defaults.midUsageThreshold,
    memoryUnit: parsed.data.memoryUnit ?? defaults.memoryUnit,
    gpuMemoryUnit: parsed.data.gpuMemoryUnit ?? defaults.gpuMemoryUnit,
    showBackendTipsDialog:
      parsed.data.showBackendTipsDialog ?? defaults.showBackendTipsDialog,
  };
}

export function createServerId(): string {
  if (typeof crypto.randomUUID === 'function') return crypto.randomUUID();
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(
    /[xy]/g,
    (character) => {
      const random = Math.floor(Math.random() * 16);
      const value = character === 'x' ? random : (random & 0x3) | 0x8;
      return value.toString(16);
    },
  );
}
