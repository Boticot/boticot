import * as request from 'request-promise';

const getAgents = async (): Promise<Array<any>> => {
  const { VUE_APP_NLU_SERVICE_URL, VUE_APP_NLU_PATH } = process.env;
  const opt = {
    url: `${VUE_APP_NLU_SERVICE_URL}${VUE_APP_NLU_PATH}`,
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
    },
    json: true,
  };
  const agents = await request.get(opt);
  return agents;
};

const getAgent = async (agentName: string): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL, VUE_APP_NLU_PATH } = process.env;
  const opt = {
    url: `${VUE_APP_NLU_SERVICE_URL}${VUE_APP_NLU_PATH}/${agentName}`,
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
    },
    json: true,
  };
  const agent = await request.get(opt);
  return agent;
};

const getAgentFile = async (agentName: string): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL, VUE_APP_NLU_PATH } = process.env;
  const opt = {
    url: `${VUE_APP_NLU_SERVICE_URL}${VUE_APP_NLU_PATH}/${agentName}/export`,
    headers: {
      encoding: null,
      'content-type': 'application/json',
    },
  };
  const agent = await request.get(opt);
  return agent;
};

const addAgent = async (data: any): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL, VUE_APP_NLU_PATH } = process.env;
  const opt = {
    url: `${VUE_APP_NLU_SERVICE_URL}${VUE_APP_NLU_PATH}`,
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
    },
    body: data,
    json: true,
  };
  const response = await request.put(opt);
  return response;
};

const deleteAgent = async (agentName: string): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL, VUE_APP_NLU_PATH } = process.env;
  const opt = {
    url: `${VUE_APP_NLU_SERVICE_URL}${VUE_APP_NLU_PATH}/${agentName}`,
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
    },
    json: true,
  };
  const response = await request.delete(opt);
  return response;
};

const getInputs = async (agentName: string, page: number): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL, VUE_APP_NLU_PATH, VUE_APP_NLU_ENTRIES_PAGE_SIZE } = process.env;
  const opt = {
    url: `${VUE_APP_NLU_SERVICE_URL}${VUE_APP_NLU_PATH}/${agentName}/inputs`
    + `?pageSize=${VUE_APP_NLU_ENTRIES_PAGE_SIZE}&pageNumber=${page}`,
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
    },
    json: true,
  };
  const response = await request.get(opt);
  return response;
};

const parseText = async (agentName: string, text: string): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL, VUE_APP_NLU_PATH } = process.env;
  const opt = {
    url: `${VUE_APP_NLU_SERVICE_URL}${VUE_APP_NLU_PATH}/${agentName}/parse?test=true`,
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
    },
    body: {
      text,
    },
    json: true,
  };
  const response = await request.post(opt);
  return response;
};

export {
  getAgents, addAgent, getInputs, parseText, getAgent, deleteAgent, getAgentFile,
};
