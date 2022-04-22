import axios from 'axios';
import store from '@/store';

type UserType = {
  email: string;
  password: string;
  is_first_login?: boolean;
  role: string;
  agents: string[];
};

const createUser = (newUser: UserType): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL } = process.env;
  const url = `${VUE_APP_NLU_SERVICE_URL}/users/register`;
  const opt = {
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
      Authorization: `Bearer ${store.getters.authToken()}`,
    },
  };
  return new Promise<any>((resolve, reject) => {
    axios.post(url, newUser, opt).then((res) => {
      resolve(res.data);
    })
      .catch((err) => {
        reject(err);
      });
  });
};

const getAllUsers = async (): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL } = process.env;
  const url = `${VUE_APP_NLU_SERVICE_URL}/users`;
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

const getUser = async (login: string): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL } = process.env;
  const url = `${VUE_APP_NLU_SERVICE_URL}/users/${login}`;
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

const updateUser = (editUser: UserType): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL } = process.env;
  const url = `${VUE_APP_NLU_SERVICE_URL}/users/${editUser.email}`;
  const opt = {
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
      Authorization: `Bearer ${store.getters.authToken()}`,
    },
  };
  return new Promise<any>((resolve, reject) => {
    axios.put(url, editUser, opt).then((res) => {
      resolve(res.data);
    })
      .catch((err) => {
        reject(err);
      });
  });
};

const deleteUser = (login: string): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL } = process.env;
  const url = `${VUE_APP_NLU_SERVICE_URL}/users/${login}`;
  const opt = {
    headers: {
      accept: 'application/json',
      'content-type': 'application/json',
      Authorization: `Bearer ${store.getters.authToken()}`,
    },
  };
  return new Promise<any>((resolve, reject) => {
    axios.delete(url, opt).then((res) => {
      resolve(res.data);
    })
      .catch((err) => {
        reject(err);
      });
  });
};

export {
  UserType, createUser, getAllUsers, getUser, updateUser, deleteUser,
};
