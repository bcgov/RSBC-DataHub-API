'use server'

import { ActionResponse } from '@/app/interfaces';
import axios, { AxiosError, AxiosRequestHeaders, AxiosResponse } from 'axios';

export const axiosApiClient = axios.create({
  baseURL: `${process.env.FLASK_API_ENDPOINT}`,
  timeout: parseInt(`${process.env.KEEP_ALIVE_TIMEOUT}`),
});

export const axiosVirusScanClient = axios.create({
  baseURL: `${process.env.CLAMAV_VIRUS_SCAN_URL}`,
  timeout: parseInt(`${process.env.KEEP_ALIVE_TIMEOUT}`),
});


export const axiosMailItClient = axios.create({
  baseURL: `${process.env.EMAIL_BASE_URL}`,
  timeout: parseInt(`${process.env.KEEP_ALIVE_TIMEOUT}`),
});

// axiosMailItClient.interceptors.response.use(
//   function (response) {
//     // Any status code that lie within the range of 2xx cause this function to trigger
//     // Do something with response data
//     return response;
//   }, 
//   function (error) {
//     // Any status codes that falls outside the range of 2xx cause this function to trigger
//     // Do something with response error
//     handleError(error);
//     // keep propagating the error
//     return Promise.reject(error);
//     // Stop the error
//     //Promise.resolve(error);
//   }
// );


export async function handleError(error: unknown): Promise<ActionResponse> {
  let message = ''
  if (error instanceof AxiosError) {
    console.log("axios error", error.response);
    if (error.response && error.response.data) {
      message = error.response.data.errorMessage || error.message;
    } else {
      message = error.message;
    }
  } else {
    console.log("noneaxios error", error);
    message = error as string;
  }
  return {
    data: {
      is_success: false,
      error: 'Internal Server Error: ' + message,
    },
  };
}
