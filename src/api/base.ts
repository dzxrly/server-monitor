import axios, { AxiosResponse } from 'axios';

axios.defaults.timeout = 30 * 1000;

export default function axiosRequest<T>(
  url: string,
  method:
    | 'get'
    | 'GET'
    | 'delete'
    | 'DELETE'
    | 'head'
    | 'HEAD'
    | 'options'
    | 'OPTIONS'
    | 'post'
    | 'POST'
    | 'put'
    | 'PUT'
    | 'patch'
    | 'PATCH'
    | 'purge'
    | 'PURGE'
    | 'link'
    | 'LINK'
    | 'unlink'
    | 'UNLINK'
    | undefined,
  data = {},
  params = {},
  headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers':
      'Content-Type, X-Requested-With, X-HTTP-Method-Override, Origin, Accept',
  }
): Promise<T> {
  const requestConfig = {
    url: url,
    method: method,
    headers: headers,
    data: data,
    params: params,
  };
  return new Promise((resolve, reject) => {
    axios(requestConfig)
      .then((response: AxiosResponse<T>) => {
        if (response.status === 200) {
          resolve(response.data);
        } else reject('Network Error');
      })
      .catch(() => {
        reject('Network Error');
      });
  });
}
