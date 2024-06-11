import axiosRequest from 'src/api/base';

export default {
  getCpuName(serverUrl: string) {
    return axiosRequest(`${serverUrl}/cpu_name`, 'GET');
  },
  getCpuState(serverUrl: string, percpu: boolean, fahrenheit: boolean) {
    return axiosRequest(
      `${serverUrl}/cpu_state`,
      'GET',
      {},
      {
        percpu: percpu,
        fahrenheit: fahrenheit,
      }
    );
  },
  getMemoryState(serverUrl: string, unit: string) {
    return axiosRequest(
      `${serverUrl}/memory_state`,
      'GET',
      {},
      {
        unit: unit,
      }
    );
  },
  getNVGPUState(serverUrl: string, unit: string, fahrenheit: boolean) {
    return axiosRequest(
      `${serverUrl}/gpu_state`,
      'GET',
      {},
      {
        unit: unit,
        fahrenheit: fahrenheit,
      }
    );
  },
};
