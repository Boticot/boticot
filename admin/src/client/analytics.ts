import axios from 'axios';
import store from '@/store';

const getAnalytics = async (agentName: string,
  daysNumber: number, startDate?: string,
  endDate?: string): Promise<any> => {
  const { VUE_APP_NLU_SERVICE_URL } = process.env;
  const url = `${VUE_APP_NLU_SERVICE_URL}/analytics/${agentName}`
  + `?days_number=${daysNumber}&start_date=${startDate}&end_date=${endDate}`;
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

export {
  getAnalytics,
};
