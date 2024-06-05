import axios, { AxiosPromise, AxiosResponse } from 'axios';

axios.defaults.timeout = 30 * 1000;


export default function axiosRequest(
  url: string,
  method: 'get' | 'GET' | 'delete' | 'DELETE' | 'head' | 'HEAD' | 'options' | 'OPTIONS' | 'post' | 'POST' | 'put' | 'PUT' | 'patch' | 'PATCH' | 'purge' | 'PURGE' | 'link' | 'LINK' | 'unlink' | 'UNLINK' | undefined,
  data = {},
  params = {},
  headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-Requested-With, X-HTTP-Method-Override, Origin, Accept'
  }
): AxiosPromise {
  const requestConfig = {
    url: url,
    method: method,
    headers: headers,
    data: data,
    params: params
  };
  return new Promise((resolve, reject) => {
    axios(requestConfig)
      .then((response: AxiosResponse) => {
        if (response.status === 200) {
          resolve(response.data);
        } else reject('Network Error');
      })
      .catch(() => {
        reject('Network Error');
      });
  });
}
