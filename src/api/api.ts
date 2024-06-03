import axiosRequest from 'src/api/base';

export default {
  getCpuName(
    serverUrl: string
  ) {
    return axiosRequest(`${serverUrl}/cpu_name`, 'GET');
  }
};
