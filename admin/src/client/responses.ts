import * as request from 'request-promise';
import store from '@/store';

const getResponses = async (agentName: string, intent: string): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL } = process.env;
  const opt = {
    url: `${VUE_APP_NLU_SERVICE_URL}/responses/agents/${agentName}/intents/${intent}`,
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
      Authorization: `Bearer ${store.getters.authToken()}`,
    },
    json: true,
  };
  const response = await request.get(opt);
  return response;
};

const deleteResponse = async (idResponse: string): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL } = process.env;
  const opt = {
    url: `${VUE_APP_NLU_SERVICE_URL}/responses/${idResponse}`,
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
      Authorization: `Bearer ${store.getters.authToken()}`,
    },
    json: true,
  };
  const response = await request.delete(opt);
  return response;
};

const addResponse = async (agentName: string, responses: any): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL } = process.env;
  const opt = {
    url: `${VUE_APP_NLU_SERVICE_URL}/responses/agents/${agentName}`,
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
      Authorization: `Bearer ${store.getters.authToken()}`,
    },
    body: responses,
    json: true,
  };
  const response = await request.put(opt);
  return response;
};

export {
  getResponses, addResponse, deleteResponse,
};
