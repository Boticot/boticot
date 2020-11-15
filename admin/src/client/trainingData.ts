import * as request from 'request-promise';

const getTrainingData = async (agentName: string, page: number): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL, VUE_APP_NLU_PATH, VUE_APP_NLU_ENTRIES_PAGE_SIZE } = process.env;
  const opt = {
    url: `${VUE_APP_NLU_SERVICE_URL}${VUE_APP_NLU_PATH}/${agentName}/training-data`
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

const deleteTrainingData = async (agentName: string, idTrainingData: string): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL, VUE_APP_NLU_PATH } = process.env;
  const opt = {
    url: `${VUE_APP_NLU_SERVICE_URL}${VUE_APP_NLU_PATH}/${agentName}/training-data/${idTrainingData}`,
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
    },
    json: true,
  };
  const response = await request.delete(opt);
  return response;
};

const updateTrainingData = async (agentName: string, idTrainingData: string, data: unknown): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL, VUE_APP_NLU_PATH } = process.env;
  const opt = {
    url: `${VUE_APP_NLU_SERVICE_URL}${VUE_APP_NLU_PATH}/${agentName}/training-data/${idTrainingData}`,
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

const addTrainingData = async (agentName: string, data: any): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL, VUE_APP_NLU_PATH } = process.env;
  const opt = {
    url: `${VUE_APP_NLU_SERVICE_URL}${VUE_APP_NLU_PATH}/${agentName}/training-data`,
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
    },
    body: data,
    json: true,
  };
  const response = await request.post(opt);
  return response;
};

export {
  getTrainingData, deleteTrainingData, updateTrainingData, addTrainingData,
};
