import * as request from 'request-promise';

const getResponses = async (agentName: string, intent: string): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL } = process.env;
  const opt = {
    url: `${VUE_APP_NLU_SERVICE_URL}/responses/agents/${agentName}/intents/${intent}`,
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
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
