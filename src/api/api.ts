import axiosRequest from 'src/api/base';

export default {
  getCpuName<T>(serverUrl: string) {
    return axiosRequest<T>(`${serverUrl}/cpu_name`, 'GET');
  },
  getCpuState<T>(serverUrl: string, percpu: boolean, fahrenheit: boolean) {
    return axiosRequest<T>(
      `${serverUrl}/cpu_state`,
      'GET',
      {},
      {
        percpu: percpu,
        fahrenheit: fahrenheit,
      }
    );
  },
  getMemoryState<T>(serverUrl: string, unit: string) {
    return axiosRequest<T>(
      `${serverUrl}/memory_state`,
      'GET',
      {},
      {
        unit: unit,
      }
    );
  },
  getNVGPUState<T>(serverUrl: string, unit: string, fahrenheit: boolean) {
    return axiosRequest<T>(
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
