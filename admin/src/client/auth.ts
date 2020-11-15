import * as request from 'request-promise';

const authenticateUser = async (data: any): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL } = process.env;
  const opt = {
    url: `${VUE_APP_NLU_SERVICE_URL}/login`,
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
  authenticateUser,
};
