import { z } from 'zod';
import messages from 'src/i18n';

enum GPUType {
  NoneGPU = 'NoneGPU',
  NVIDIA = 'NVIDIA',
  AMD = 'AMD',
  INTEL = 'Intel',
}

enum ByteUnit {
  B = 'B',
  KB = 'KB',
  MB = 'MB',
  GB = 'GB',
  TB = 'TB',
}

class GPUServer {
  public gpuType = GPUType.NoneGPU;

  constructor() {
    this.gpuType = GPUType.NoneGPU;
  }

  public setGPUType(type: GPUType) {
    this.gpuType = type;
  }
}

class ServerConfig {
  public customName = '';
  public uniqueId = '';
  public serverUrl = '';
  public tagColor = '#000000';
  public gpuServer = new GPUServer();
}

class Config {
  public darkMode = false;
  public defaultLanguage = 'en-US';
  public indexPageServerPanelLayout = 'sm';
  public serverListConfig = Array<ServerConfig>();
  public refreshTimeSec = 5;
  public useFahrenheitUnit = false;
  public freeUsageThreshold = 30;
  public midUsageThreshold = 70;
  public memoryUnit = ByteUnit.GB;
  public gpuMemoryUnit = ByteUnit.GB;
  public showBackendTipsDialog = true;

  constructor() {
    const browserLanguage = navigator.language || 'en-US';
    this.defaultLanguage = messages.hasOwnProperty(browserLanguage)
      ? browserLanguage
      : 'en-US';
  }
}

// when you change the Config class and other classes in this file, you should also update the following zod schema
const configZod = z.object({
  darkMode: z.boolean(),
  defaultLanguage: z.string(),
  indexPageServerPanelLayout: z.string(),
  serverListConfig: z.array(
    z.object({
      customName: z.string(),
      uniqueId: z.string(),
      serverUrl: z.string(),
      tagColor: z.string(),
      gpuServer: z.object({
        gpuType: z.string(),
      }),
    })
  ),
  refreshTimeSec: z.number(),
  useFahrenheitUnit: z.boolean(),
  freeUsageThreshold: z.number(),
  midUsageThreshold: z.number(),
  memoryUnit: z.string(),
  gpuMemoryUnit: z.string(),
});

export { ByteUnit, ServerConfig, Config, GPUType, GPUServer, configZod };
