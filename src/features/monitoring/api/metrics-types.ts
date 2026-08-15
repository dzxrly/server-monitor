export interface TemperatureSensor {
  hardware: string;
  hardwareType?: string;
  name: string;
  identifier?: string;
  currentCelsius: number;
  highCelsius: number | null;
  criticalCelsius: number | null;
}

export interface ProcessRow {
  pid: number;
  name: string;
  cpuUsagePercent?: number;
  memoryUsagePercent?: number;
  memoryBytes?: number;
  gpuUsagePercent?: number | null;
  gpuMemoryBytes?: number;
  deviceIndexes?: number[];
  types?: string[];
}

export interface MetricsSnapshot {
  apiVersion: 'v1';
  sequence: number;
  sampledAt: string;
  sampleIntervalSeconds: number;
  collectionDurationMilliseconds: number;
  system: {
    available: boolean;
    name: string;
    version: string;
    kernel: string;
    platform: string;
    architecture: string;
    bits: string;
    hostname: string;
    bootTimeEpochSeconds: number;
    uptimeSeconds: number;
    processId: number;
    pythonVersion: string;
  };
  cpu: {
    available: boolean;
    name: string;
    usagePercent: number;
    perCoreUsagePercent: number[];
    physicalCores: number | null;
    logicalCores: number | null;
    frequency: {
      currentMhz: number | null;
      minMhz: number | null;
      maxMhz: number | null;
    };
    temperatures: TemperatureSensor[];
  };
  memory: {
    available: boolean;
    totalBytes: number;
    availableBytes: number;
    usedBytes: number;
    freeBytes: number;
    usagePercent: number;
    swap: {
      totalBytes: number;
      usedBytes: number;
      freeBytes: number;
      usagePercent: number;
    };
  };
  gpu: {
    available: boolean;
    provider?: string;
    reason?: string | null;
    devices: Array<{
      index: number;
      name: string;
      uuid: string;
      driverVersion: string;
      usagePercent: number | null;
      memoryUsagePercent: number | null;
      memory: {
        totalBytes: number | null;
        usedBytes: number | null;
        freeBytes: number | null;
      };
      temperatureCelsius: number | null;
      fanSpeedPercent: number | null;
      powerWatts: number | null;
      powerLimitWatts: number | null;
    }>;
  };
  temperatures: {
    available: boolean;
    provider: string;
    reason: string | null;
    sensors: TemperatureSensor[];
    cpu: TemperatureSensor[];
  };
  storage: {
    available: boolean;
    volumes: Array<{
      device: string;
      mountpoint: string;
      fileSystem: string | null;
      options: string[];
      readOnly: boolean;
      totalBytes: number;
      usedBytes: number;
      freeBytes: number;
      usagePercent: number;
    }>;
    devices: Array<{
      name: string;
      readCount: number;
      writeCount: number;
      readBytes: number;
      writeBytes: number;
      readBytesPerSecond: number | null;
      writeBytesPerSecond: number | null;
      readOperationsPerSecond: number | null;
      writeOperationsPerSecond: number | null;
      busyTimeMilliseconds: number | null;
    }>;
  };
  network: {
    available: boolean;
    totals: {
      bytesSent: number;
      bytesReceived: number;
      bytesSentPerSecond: number | null;
      bytesReceivedPerSecond: number | null;
    };
    interfaces: Array<{
      name: string;
      isUp: boolean;
      duplex: number | null;
      speedMbps: number | null;
      mtu: number | null;
      addresses: Array<{
        family: string;
        address: string;
        netmask: string | null;
        broadcast: string | null;
        peer: string | null;
      }>;
      bytesSent: number;
      bytesReceived: number;
      packetsSent: number;
      packetsReceived: number;
      errorsIn: number;
      errorsOut: number;
      dropsIn: number;
      dropsOut: number;
      bytesSentPerSecond: number | null;
      bytesReceivedPerSecond: number | null;
    }>;
  };
  processes: {
    available: boolean;
    limit: number;
    cpu: ProcessRow[];
    memory: ProcessRow[];
    gpu: ProcessRow[];
  };
  capabilities: Record<string, unknown>;
  errors: Record<string, string>;
}
