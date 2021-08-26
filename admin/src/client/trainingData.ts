import axios from 'axios';
import store from '@/store';

const getTrainingData = async (agentName: string, page: number): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL, VUE_APP_NLU_PATH, VUE_APP_NLU_ENTRIES_PAGE_SIZE } = process.env;
  const url = `${VUE_APP_NLU_SERVICE_URL}${VUE_APP_NLU_PATH}/${agentName}/training-data`
    + `?pageSize=${VUE_APP_NLU_ENTRIES_PAGE_SIZE}&pageNumber=${page}`;
  const opt = {
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
      Authorization: `Bearer ${store.getters.authToken()}`,
    },
  };
  const response = await axios.get(url, opt);
  return response.data;
};

const deleteTrainingData = async (agentName: string, idTrainingData: string): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL, VUE_APP_NLU_PATH } = process.env;
  const url = `${VUE_APP_NLU_SERVICE_URL}${VUE_APP_NLU_PATH}/${agentName}/training-data/${idTrainingData}`;
  const opt = {
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
      Authorization: `Bearer ${store.getters.authToken()}`,
    },
  };
  const response = await axios.delete(url, opt);
  return response.data;
};

const updateTrainingData = async (agentName: string, idTrainingData: string, data: unknown): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL, VUE_APP_NLU_PATH } = process.env;
  const url = `${VUE_APP_NLU_SERVICE_URL}${VUE_APP_NLU_PATH}/${agentName}/training-data/${idTrainingData}`;
  const opt = {
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
      Authorization: `Bearer ${store.getters.authToken()}`,
    },
  };
  const response = await axios.put(url, data, opt);
  return response.data;
};

const addTrainingData = async (agentName: string, data: any): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL, VUE_APP_NLU_PATH } = process.env;
  const url = `${VUE_APP_NLU_SERVICE_URL}${VUE_APP_NLU_PATH}/${agentName}/training-data`;
  const opt = {
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
      Authorization: `Bearer ${store.getters.authToken()}`,
    },
  };
  const response = await axios.post(url, data, opt);
  return response.data;
};

export {
  getTrainingData, deleteTrainingData, updateTrainingData, addTrainingData,
};
