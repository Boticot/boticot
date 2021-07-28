import mockedData from '@/client/__mocks__/mockedAnalyticsData.json';
import {
  generateSingleChartData,
  generateChartDataLineIntents,
  generateChartDoghnutIntents,
  prepareAnalyticsData,
} from '@/service/analyticsService';
import { colorsArray } from '@/utils';
import _ from 'lodash';

describe('analyticsService.ts', () => {
  const chartColor = 'rgb(75, 192, 192)';
  const intentDataList = ['intent1', 'intent2', 'FALLBACK', 'intent3', 'intent4'];
  const dateDataList = [
    '2021-08-01',
    '2021-08-02',
    '2021-08-03',
    '2021-08-04',
    '2021-08-05',
    '2021-08-06',
    '2021-08-07',
    '2021-08-08',
  ];
  const trafficDataList = [4, 2, 4, 4, 4, 4, 8, 5];
  const uniqueUsersDataList = [3, 11, 3, 3, 3, 3, 3, 1];
  const fallbackDataList = [3, 0, 3, 3, 3, 1, 3, 5];
  it('should prepare analyticsa data', () => {
    const {
      intentDataList: intentDataListResult,
      allDateDataList: allDateDataListResult,
      allTrafficDataList: allTrafficDataListResult,
      allUniqueUsersDataList: allUniqueUsersDataListResult,
      allFallbackDataList: allFallbackDataListResult,
    } = prepareAnalyticsData(mockedData);

    expect(intentDataListResult).toEqual(intentDataList);

    expect(allDateDataListResult).toEqual(dateDataList);

    expect(allTrafficDataListResult).toEqual(trafficDataList);

    expect(allUniqueUsersDataListResult).toEqual(uniqueUsersDataList);

    expect(allFallbackDataListResult).toEqual(fallbackDataList);
  });

  it('should generate chart dataLine traffic', () => {
    const chartDataLineTraffic = generateSingleChartData('Traffic', dateDataList, trafficDataList);
    const expectedChartDataLineTraffic = {
      labels: dateDataList,
      datasets: [
        {
          label: 'Traffic',
          data: trafficDataList,
          fill: false,
          borderColor: chartColor,
          backgroundColor: chartColor,
          tension: 0.1,
        },
      ],
    };
    expect(chartDataLineTraffic).toEqual(expectedChartDataLineTraffic);
  });

  it('should generate chart dataLine unique users', () => {
    const chartDataLineUniqueUsers = generateSingleChartData('Unique Users', dateDataList, uniqueUsersDataList);
    const expectedChartDataLineUniqueUsers = {
      labels: dateDataList,
      datasets: [
        {
          label: 'Unique Users',
          data: uniqueUsersDataList,
          fill: false,
          borderColor: chartColor,
          backgroundColor: chartColor,
          tension: 0.1,
        },
      ],
    };
    expect(chartDataLineUniqueUsers).toEqual(expectedChartDataLineUniqueUsers);
  });

  it('should generate chart dataBar fallback', () => {
    const chartDataBarFallback = generateSingleChartData('Fallback', dateDataList, fallbackDataList);
    const expectedChartDataBarFallback = {
      labels: dateDataList,
      datasets: [
        {
          label: 'Fallback',
          data: fallbackDataList,
          fill: false,
          backgroundColor: chartColor,
          borderColor: chartColor,
          tension: 0.1,
        },
      ],
    };
    expect(chartDataBarFallback).toEqual(expectedChartDataBarFallback);
  });

  it('should generate chart dataLine intents', () => {
    const chartDataLineIntents = generateChartDataLineIntents(dateDataList, 'Last 30 days', mockedData);
    const expectedDataFieldOfChartDataLineIntentOfNameIntent1 = [5, 2, 3, 8, 11, 4, 0, 2];
    expect(chartDataLineIntents.datasets[0].data).toEqual(expectedDataFieldOfChartDataLineIntentOfNameIntent1);
  });

  it('should generate chart doghnut intents', () => {
    // given
    const countDataList = [];
    const flatResult = _(mockedData.analytics)
      .takeRight(30)
      .flatMap('intents_count');
    for (let i = 0; i < intentDataList.length; i += 1) {
      let sum = 0;
      for (let j = 0; j < (flatResult as any).length; j += 1) {
        if (intentDataList[i] === (flatResult as any)[j].intent) {
          sum += (flatResult as any)[j].count;
        }
      }
      countDataList.push(sum);
    }
    const expectedChartDoghnutIntents = {
      labels: intentDataList,
      datasets: [
        {
          data: countDataList,
          backgroundColor: [...colorsArray, ...colorsArray],
          hoverOffset: 4,
        },
      ],
    };

    // when
    const chartDoghnutIntents = generateChartDoghnutIntents(intentDataList, countDataList);

    // then
    expect(chartDoghnutIntents).toEqual(expectedChartDoghnutIntents);
  });
});
