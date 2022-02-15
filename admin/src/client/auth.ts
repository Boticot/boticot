import axios from 'axios';
import store from '@/store';

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

const resetPassword = (email: string, newPassword: string): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL } = process.env;
  const url = `${VUE_APP_NLU_SERVICE_URL}/users/${email}/reset-password`;
  const opt = {
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
      Authorization: `Bearer ${store.getters.authToken()}`,
    },
  };
  const body = { ...{ }, new_password: newPassword };
  return new Promise((resolve, reject) => {
    axios.post(url, body, opt)
      .then((res) => resolve(res.data))
      .catch((err) => reject(err));
  });
};

export {
  authenticateUser, resetPassword,
};
