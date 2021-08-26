import axios from 'axios';

const authenticateUser = async (data: any): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL } = process.env;
  const url = `${VUE_APP_NLU_SERVICE_URL}/login`;
  const opt = {
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
    },
  };
  const response = await axios.post(url, data, opt);
  return response.data;
};

export {
  authenticateUser,
};
