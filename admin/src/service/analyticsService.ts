import _ from 'lodash';
import dayjs from 'dayjs';
import {
  Analytics, ChartData, PreparedAnalyticsData,
} from '@/types';
import { colorsArray, getRandomColor } from '@/utils';

const chartBorderColor = 'rgb(75, 192, 192)';
const DATE_FORMAT = 'YYYY-MM-DD';

function getCountsOfIntent(intentName: string, analyticsData: any) {
  return ([].concat(...(analyticsData
    .map((item: any) => {
      if (_.some(item.intents_count, { intent: intentName })) {
        const element = _.filter(item.intents_count, ['intent', intentName]);
        return element[0].count;
      }
      return 0;
    }) as any)) as any);
}

function getCountsOfEntity(entityName: string, analyticsData: any) {
  return ([].concat(...(analyticsData
    .map((item: any) => {
      if (_.some(item.entities_count, { entity: entityName })) {
        const element = _.filter(item.entities_count, ['entity', entityName]);
        return element[0].count;
      }
      return 0;
    }) as any)) as any);
}

const generateSingleChartData = (
  datasetLabel: string,
  dateDataList: Array<Date | string>,
  dataList: Array<number>,
): ChartData => ({
  labels: dateDataList,
  datasets: [
    {
      label: datasetLabel,
      data: dataList,
      fill: false,
      borderColor: chartBorderColor,
      backgroundColor: chartBorderColor,
      tension: 0.1,
    },
  ],
});

const generateChartDataLineIntents = (dateDataList: Array<Date | string>, period: string, analyticsData: Analytics):
  ChartData => {
  let limit;
  if (period === 'Last 7 days') {
    limit = 7;
  } else if (period === 'Last 30 days') {
    limit = 30;
  }
  const limitedAnalyticsData = _.takeRight((analyticsData as any).analytics, limit);
  const intentsDatasets = _((analyticsData as any).analytics)
    .takeRight(limit)
    .flatMap('intents_count')
    .uniqBy('intent')
    .map((item: any) => ({
      label: item.intent,
      data: getCountsOfIntent(item.intent, limitedAnalyticsData),
      fill: false,
      borderColor: getRandomColor(),
      tension: 0.1,
    }))
    .value();
  return {
    labels: _.takeRight(dateDataList, limit),
    datasets: intentsDatasets,
  };
};

const generateChartDataLineEntities = (dateDataList: Array<Date | string>, period: string, analyticsData: Analytics):
  ChartData => {
  let limit;
  if (period === 'Last 7 days') {
    limit = 7;
  } else if (period === 'Last 30 days') {
    limit = 30;
  }
  const limitedAnalyticsData = _.takeRight((analyticsData as any).analytics, limit);
  const entitiesDatasets = _((analyticsData as any).analytics)
    .takeRight(limit)
    .filter('entities_count')
    .flatMap('entities_count')
    .uniqBy('entity')
    .map((item: any) => ({
      label: item.entity,
      data: getCountsOfEntity(item.entity, limitedAnalyticsData),
      fill: false,
      borderColor: getRandomColor(),
      tension: 0.1,
    }))
    .value();
  return {
    labels: _.takeRight(dateDataList, limit),
    datasets: entitiesDatasets,
  };
};

const generateChartDoghnutIntents = (intentDataList: Array<string>, countDataList: Array<number>): ChartData => ({
  labels: intentDataList,
  datasets: [
    {
      data: countDataList,
      backgroundColor: [...colorsArray, ...colorsArray],
      hoverOffset: 4,
    },
  ],
});

const prepareAnalyticsData = (analyticsData: Analytics): PreparedAnalyticsData => {
  const result: PreparedAnalyticsData = {
    intentDataList: [],
    entitiesDataList: [],
    allDateDataList: [],
    allTrafficDataList: [],
    allUniqueUsersDataList: [],
    allFallbackDataList: [],
  };
  _.reverse((analyticsData as any).analytics);
  const intentDataList = (_((analyticsData as any).analytics)
    .flatMap('intents_count')
    .uniqBy('intent')
    .map((item: any) => item.intent)
    .value() as any);

  const entitiesDataList = (_((analyticsData as any).analytics)
    .filter('entities_count')
    .flatMap('entities_count')
    .uniqBy('entity')
    .map((item: any) => item.entity)
    .value() as any);

  const allDateDataList = (analyticsData as any).analytics
    .map((item: any) => dayjs(item.date).format(DATE_FORMAT));

  const allTrafficDataList = (analyticsData as any).analytics.map((item: any) => item.traffic);

  const allUniqueUsersDataList = (analyticsData as any).analytics.map((item: any) => item.unique_users);

  const allFallbackDataList = ([].concat(...((analyticsData as any).analytics
    .map((item: any) => {
      if (_.some(item.intents_count, { intent: 'FALLBACK' })) {
        const element = _.filter(item.intents_count, ['intent', 'FALLBACK']);
        return element[0].count / item.traffic;
      }
      return 0;
    }) as any)) as any);

  result.intentDataList = intentDataList;
  result.entitiesDataList = entitiesDataList;
  result.allDateDataList = allDateDataList;
  result.allTrafficDataList = allTrafficDataList;
  result.allUniqueUsersDataList = allUniqueUsersDataList;
  result.allFallbackDataList = allFallbackDataList;
  return result;
};

export {
  prepareAnalyticsData,
  generateSingleChartData,
  generateChartDataLineIntents,
  generateChartDataLineEntities,
  generateChartDoghnutIntents,
};
