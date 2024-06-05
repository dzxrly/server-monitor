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
  public userConfig = {
    darkMode: false,
    defaultLanguage: 'en-US',
    indexPageServerPanelLayout: 'sm',
    serverListConfig: Array<ServerConfig>(),
    refreshTimeSec: 5,
    useFahrenheitUnit: false,
    freeUsageThreshold: 30,
    midUsageThreshold: 70
  };

  public toString() {
    return JSON.stringify(this.userConfig);
  }

  public fromString(str: string) {
    this.userConfig = JSON.parse(str);
  }
}

export {
  ServerConfig,
  Config,
  GPUType,
  GPUServer
};
