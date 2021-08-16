import axios from 'axios';
import store from '@/store';

const getResponses = async (agentName: string, intent: string): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL } = process.env;
  const url = `${VUE_APP_NLU_SERVICE_URL}/responses/agents/${agentName}/intents/${intent}`;
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

const deleteResponse = async (idResponse: string): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL } = process.env;
  const url = `${VUE_APP_NLU_SERVICE_URL}/responses/${idResponse}`;
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

const addResponse = async (agentName: string, responses: any): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL } = process.env;
  const url = `${VUE_APP_NLU_SERVICE_URL}/responses/agents/${agentName}`;
  const opt = {
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
      Authorization: `Bearer ${store.getters.authToken()}`,
    },
  };
  const response = await axios.put(url, responses, opt);
  return response.data;
};

export {
  getResponses, addResponse, deleteResponse,
};
