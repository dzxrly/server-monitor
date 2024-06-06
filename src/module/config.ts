import { z } from 'zod';

enum GPUType {
  NoneGPU = 'NoneGPU',
  NVIDIA = 'NVIDIA',
  AMD = 'AMD',
  INTEL = 'Intel',
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
}

// when you change the Config class and other classes in this file, you should also update the following zod schema
const configZod = z.object({
  darkMode: z.boolean(),
  defaultLanguage: z.string(),
  indexPageServerPanelLayout: z.string(),
  serverListConfig: z.array(z.object({
    customName: z.string(),
    uniqueId: z.string(),
    serverUrl: z.string(),
    tagColor: z.string(),
    gpuServer: z.object({
      gpuType: z.string()
    })
  })),
  refreshTimeSec: z.number(),
  useFahrenheitUnit: z.boolean(),
  freeUsageThreshold: z.number(),
  midUsageThreshold: z.number()
});

export {
  ServerConfig,
  Config,
  GPUType,
  GPUServer,

  configZod
};
