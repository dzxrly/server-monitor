export interface CPUNameResponse {
  cpuName: string,
}

export interface CPUCoreTemperature {
  coreCritical: number,
  coreCurrent: number,
  coreHigh: number,
  coreLabel: string,
}

export interface CPUTemperature {
  numaCritical?: number,
  numaCurrent?: number,
  numaHigh?: number,
  numaLabel?: string,
  coresTemperature?: Array<CPUCoreTemperature>,
}

export interface CPUStatePerCPUResponse {
  cpuCTXSwitches: number,
  cpuCores: {
    cores: number,
    threads: number,
  },
  cpuFreq: {
    avg: {
      current: number,
      max: number,
      min: number,
    },
    percpu: Array<{
      current: number,
      max: number,
      min: number,
    }>,
  },
  cpuInterrupts: number,
  cpuSoftInterrupts: number,
  cpuSyscalls: number,
  cpuTemperature: Array<CPUTemperature>,
  cpuUsage: {
    avg: number,
    percpu: Array<number>,
  }
}

export interface MemoryStateResponse {
  memoryAvailable: number,
  memoryFree: number,
  memoryTotal: number,
  memoryUsed: number,
  memoryPercent: number,
  swapFree: number,
  swapPercent: number,
  swapTotal: number,
  swapUsed: number,
}

export interface GPUInfoResponse {
  gpuIndex: number,
  gpuName: string,
  fanSpeed: number,
  gpuTemperature: number,
  gpuUsage: number,
  memoryFree: number,
  memoryPercent: number,
  memoryTotal: number,
  memoryUsed: number,
  powerCurrent: number,
  powerLimit: number,
}

export interface GPUStateResponse {
  driverVersion: string,
  gpuList: Array<GPUInfoResponse>,
}

export interface NetworkStateResponse {
  bytesSent: number,
  bytesRecv: number,
  packetsSent: number,
  packetsRecv: number,
  errIn: number,
  errOut: number,
  dropIn: number,
  dropOut: number,
}
