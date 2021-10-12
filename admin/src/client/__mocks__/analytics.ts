import mockedData from './mockedAnalyticsData.json';

module.exports = {
  getAnalytics: () => Promise.resolve(mockedData),
};
