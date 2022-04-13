<template>
  <div class="analytics chartSize" v-loading="loading">
    <el-row v-if="textMsg !== ''" :class="classMsg" class="marginBottomMedium marginLeftMedium">
          {{ textMsg }}
    </el-row>
    <el-select class="marginClass" v-model="period" placeholder="Select Period" @change="selectPeriod">
    <el-option
      v-for="item in ['Last 7 days', 'Last 30 days']"
      :key="item.value"
      :label="item"
      :value="item">
    </el-option>
    </el-select>
    <LineChart class="marginClass" :chartData="chartDataLineTraffic" :options="chartOptions" />
    <LineChart class="marginClass" :chartData="chartDataLineUniqueUsers" :options="chartOptions" />
    <BarChart class="marginClass" :chartData="chartDataBarFallback" :options="chartOptionsRate" />
    <LineChart class="marginClass" :chartData="chartDataLineIntents"
      :options="chartDataLineIntentsOptions"  />
    <el-select v-model="doghnutPeriod"
      placeholder="Select Period" @change="selectPeriodForDoghnut">
    <el-option
      v-for="item in ['Last day', 'Last 7 days', 'Last 30 days']"
      :key="item.value"
      :label="item"
      :value="item">
    </el-option>
    </el-select>
    <DoghnutChart class="marginClass" :chartData="chartDoghnutIntents" :options="doghnutOptions"/>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import _ from 'lodash';
import LineChart from '@/components/analytics/LineChart.vue';
import BarChart from '@/components/analytics/BarChart.vue';
import DoghnutChart from '@/components/analytics/DoghnutChart.vue';
import { getAnalytics } from '@/client/analytics';
import { Analytics } from '@/types';
import {
  prepareAnalyticsData,
  generateSingleChartData,
  generateChartDataLineIntents,
  generateChartDoghnutIntents,
} from '@/service/analyticsService';

function handleIntentLegendClick(this: any, e: any, legendItem: any) {
  const index = legendItem.datasetIndex;
  const ci = this.chart;
  const size = ci.data.datasets.length;
  for (let i = 0; i < size; i += 1) {
    if (i !== index) {
      const meta = ci.getDatasetMeta(i);
      meta.hidden = meta.hidden === null ? !ci.data.datasets[i].hidden : null;
    }
  }
  // rerender the chart
  ci.update();
}

function formatRate(value: number) {
  return Number(value).toLocaleString(undefined, {
    style: 'percent',
    minimumFractionDigits: 2,
  });
}

export default Vue.extend({
  name: 'analytics',
  components: {
    LineChart,
    BarChart,
    DoghnutChart,
  },
  data() {
    return {
      loading: true,
      isAnalyticsDataEmpty: false,
      agentName: this.$route.params.agentName,
      textMsg: '',
      classMsg: '',
      analyticsData: '',
      period: 'Last 30 days',
      doghnutPeriod: 'Last 30 days',
      dateDataList: Array<Date>(),
      trafficDataList: Array<number>(),
      uniqueUsersDataList: Array<number>(),
      fallbackDataList: Array<number>(),
      intentDataList: Array<string>(),
      countDataList: Array<any>(),
      allDateDataList: Array<Date>(),
      allTrafficDataList: Array<number>(),
      allUniqueUsersDataList: Array<number>(),
      allFallbackDataList: Array<number>(),
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true,
            },
          }],
        },
      },
      chartOptionsRate: {
        responsive: true,
        maintainAspectRatio: false,
        tooltips: {
          callbacks: {
            label: (tooltipItem: any, data: any) => {
              const { label } = data.datasets[tooltipItem.datasetIndex];
              const value = formatRate(tooltipItem.yLabel);
              return `${label}: ${value}`;
            },
          },
        },
        scales: {
          yAxes: [{
            ticks: {
              callback: (value: number) => formatRate(value),
              beginAtZero: true,
            },
          }],
        },
      },
      chartDataLineIntentsOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          yAxes: [{
            display: false,
            ticks: {
              stepSize: 1,
              beginAtZero: true,
            },
          }],
        },
        legend: {
          onClick: handleIntentLegendClick,
        },
        title: {
          display: true,
          text: 'Intents',
          fontSize: 15,
          fontStyle: 'normal',
        },
      },
      doghnutOptions: {
        responsive: true,
        maintainAspectRatio: false,
        legend: {
          position: 'right',
        },
        title: {
          display: true,
          text: 'Cumulative Intents',
          fontSize: 15,
          fontStyle: 'normal',
        },
        tooltips: {
          callbacks: {
            label: (tooltipItem: any, data: any) => {
              const label = data.labels[tooltipItem.index];
              const value = formatRate(data.datasets[0].data[tooltipItem.index]);
              return `${label}: ${value}`;
            },
          },
        },
      },
    };
  },
  computed: {
    chartDataLineTraffic(): any {
      return generateSingleChartData('Traffic', this.dateDataList, this.trafficDataList);
    },
    chartDataLineUniqueUsers(): any {
      return generateSingleChartData('Unique Users', this.dateDataList, this.uniqueUsersDataList);
    },
    chartDataBarFallback(): any {
      return generateSingleChartData('Fallback', this.dateDataList, this.fallbackDataList);
    },
    chartDataLineIntents(): any {
      return generateChartDataLineIntents(this.dateDataList, this.period, this.analyticsData as unknown as Analytics);
    },
    chartDoghnutIntents(): any {
      return generateChartDoghnutIntents(this.intentDataList, this.countDataList);
    },
  },
  methods: {
    sliceData(size: number) {
      this.dateDataList = (this.allDateDataList as any).slice(size);
      this.trafficDataList = (this.allTrafficDataList as any).slice(size);
      this.uniqueUsersDataList = (this.allUniqueUsersDataList as any).slice(size);
      this.fallbackDataList = (this.allFallbackDataList as any).slice(size);
    },
    selectPeriod(value: string) {
      if (value === 'Last 7 days') {
        this.sliceData(-7);
      } else if (value === 'Last 30 days') {
        this.sliceData(-30);
      }
    },
    selectPeriodForDoghnut(value: string) {
      let limitedResult;
      this.countDataList = [];
      if (value === 'Last day') {
        limitedResult = _.takeRight((this.analyticsData as any).analytics, 1);
      } else if (value === 'Last 7 days') {
        limitedResult = _.takeRight((this.analyticsData as any).analytics, 7);
      } else if (value === 'Last 30 days') {
        limitedResult = _.takeRight((this.analyticsData as any).analytics, 30);
      }
      const flatResult = _.flatMap(limitedResult, 'intents_count');
      for (let i = 0; i < this.intentDataList.length; i += 1) {
        let sum = 0;
        for (let j = 0; j < flatResult.length; j += 1) {
          if (this.intentDataList[i] === flatResult[j].intent) {
            sum += flatResult[j].count;
          }
        }
        this.countDataList.push(sum);
      }
    },
  },
  mounted() {
    getAnalytics(this.agentName, 30).then((response) => {
      this.loading = false;
      this.analyticsData = _.cloneDeep(response);
      this.isAnalyticsDataEmpty = (this.analyticsData as any).analytics.length === 0;
      if (this.isAnalyticsDataEmpty) {
        this.$notify.info({
          title: 'Info',
          message: 'Empty Analytics Data',
          offset: 100,
        });
      } else {
        const preparedAnalyticsData = prepareAnalyticsData((this.analyticsData as unknown as Analytics));
        this.intentDataList = preparedAnalyticsData.intentDataList;
        this.allDateDataList = preparedAnalyticsData.allDateDataList;
        this.allTrafficDataList = preparedAnalyticsData.allTrafficDataList;
        this.allUniqueUsersDataList = preparedAnalyticsData.allUniqueUsersDataList as any;
        this.allFallbackDataList = preparedAnalyticsData.allFallbackDataList as any;
        this.selectPeriod('Last 30 days');
        this.selectPeriodForDoghnut('Last 30 days');
      }
    }).catch(() => {
      this.textMsg = 'error when loading analytics';
      this.classMsg = 'errorMsg';
    });
  },
});
</script>

<style scoped>
  .marginClass {
    margin-bottom: 5% !important;
  }
</style>
