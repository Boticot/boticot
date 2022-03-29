import axios from 'axios';
import store from '@/store';
import { SynonymsData } from '@/types';

const getSynonyms = async (agentName: string): Promise<SynonymsData> => {
  const { VUE_APP_NLU_SERVICE_URL, VUE_APP_NLU_PATH } = process.env;
  const url = `${VUE_APP_NLU_SERVICE_URL}${VUE_APP_NLU_PATH}/${agentName}/synonyms`;
  const opt = {
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
      Authorization: `Bearer ${store.getters.authToken()}`,
    },
  };
  const agent = await axios.get(url, opt);
  return agent.data;
};

const addSynonyms = async (body: any, agentName: string): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL, VUE_APP_NLU_PATH } = process.env;
  const url = `${VUE_APP_NLU_SERVICE_URL}${VUE_APP_NLU_PATH}/${agentName}/synonyms`;
  const opt = {
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
      Authorization: `Bearer ${store.getters.authToken()}`,
    },
  };
  const response = await axios.post(url, body, opt);
  return response.data;
};

const updateSynonyms = async (body: any, agentName: string, id: string): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL, VUE_APP_NLU_PATH } = process.env;
  const url = `${VUE_APP_NLU_SERVICE_URL}${VUE_APP_NLU_PATH}/${agentName}/synonyms/${id}`;
  const opt = {
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
      Authorization: `Bearer ${store.getters.authToken()}`,
    },
  };
  const response = await axios.put(url, body, opt);
  return response.data;
};

const deleteSynonyms = async (agentName: string, id: string): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL, VUE_APP_NLU_PATH } = process.env;
  const url = `${VUE_APP_NLU_SERVICE_URL}${VUE_APP_NLU_PATH}/${agentName}/synonyms/${id}`;
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

export {
  getSynonyms, addSynonyms, updateSynonyms, deleteSynonyms,
};
