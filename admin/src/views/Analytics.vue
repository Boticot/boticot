<template>
  <div class="analytics chartSize" v-loading="loading">
    <el-row v-if="textMsg !== ''" :class="classMsg" class="marginBottomMedium marginLeftMedium">
          {{ textMsg }}
    </el-row>
    <el-row class="marginClass">
      <el-select v-model="period" placeholder="Select Period" @change="selectPeriod">
        <el-option
          v-for="item in ['Last 7 days', 'Last 30 days', 'Last 60 days', 'Custom filter']"
          :key="item.value"
          :label="item"
          :value="item">
        </el-option>
      </el-select>
    </el-row>
    <el-row justify="space-around" class="marginClass" style="margin-left: 350px" v-if="filterDateEnabled">
      <el-col :span="11">
        <el-date-picker
          v-model="filterDate"
          type="daterange"
          format="dd-MM-yyyy"
          value-format="dd-MM-yyyy"
          range-separator="To"
          start-placeholder="Start date"
          end-placeholder="End date">
        </el-date-picker>
      </el-col>
      <el-col :span="5">
        <el-button type="primary" @click="onSubmitFilterDate" :disabled="!filterDate">Filter</el-button>
      </el-col>
    </el-row>
    <LineChart class="marginClass" :chartData="chartDataLineTraffic" :options="chartOptions" />
    <LineChart class="marginClass" :chartData="chartDataLineUniqueUsers" :options="chartOptions" />
    <BarChart class="marginClass" :chartData="chartDataBarFallback" :options="chartOptionsRate" />
    <LineChart class="marginClass" :chartData="chartDataLineIntents"
      :options="chartDataLineIntentsOptions"  />
    <el-row class="marginClass">
      <el-select v-model="doghnutPeriod" placeholder="Select Period" @change="selectPeriodForDoghnut">
        <el-option
          v-for="item in ['Last day', 'Last 7 days', 'Last 30 days', 'Last 60 days', 'Custom filter']"
          :key="item.value"
          :label="item"
          :value="item">
        </el-option>
      </el-select>
    </el-row>
    <el-row justify="space-around"  class="marginClass" style="margin-left: 350px" v-if="filterDateDoghnutEnabled">
      <el-col :span="11">
        <el-date-picker
          v-model="filterDateDoghnut"
          type="daterange"
          format="dd-MM-yyyy"
          value-format="dd-MM-yyyy"
          range-separator="To"
          start-placeholder="Start date"
          end-placeholder="End date">
        </el-date-picker>
      </el-col>
      <el-col :span="5">
        <el-button type="primary" @click="onSubmitFilterDateDoghnut"
          :disabled="!filterDateDoghnut">Filter</el-button>
      </el-col>
    </el-row>
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
      filterDateEnabled: false,
      filterDateDoghnutEnabled: false,
      filterDate: [],
      filterDateDoghnut: [],
      loading: true,
      isAnalyticsDataEmpty: false,
      agentName: this.$route.params.agentName,
      textMsg: '',
      classMsg: '',
      analyticsData: '',
      period: 'Last 60 days',
      doghnutPeriod: 'Last 60 days',
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
      if (value === 'Custom filter') {
        this.filterDateEnabled = true;
        return;
      }
      if (value === 'Last 7 days') {
        this.filterDateEnabled = false;
        this.sliceData(-7);
      } else if (value === 'Last 30 days') {
        this.filterDateEnabled = false;
        this.sliceData(-30);
      } else if (value === 'Last 60 days') {
        this.filterDateEnabled = false;
        this.sliceData(-60);
      }
    },
    selectPeriodForDoghnut(value: string) {
      if (value === 'Custom filter') {
        this.filterDateDoghnutEnabled = true;
        return;
      }
      let limitedResult;
      this.countDataList = [];
      if (value === 'Last day') {
        this.filterDateDoghnutEnabled = false;
        limitedResult = _.takeRight((this.analyticsData as any).analytics, 1);
      } else if (value === 'Last 7 days') {
        this.filterDateDoghnutEnabled = false;
        limitedResult = _.takeRight((this.analyticsData as any).analytics, 7);
      } else if (value === 'Last 30 days') {
        this.filterDateDoghnutEnabled = false;
        limitedResult = _.takeRight((this.analyticsData as any).analytics, 30);
      } else if (value === 'Last 60 days') {
        this.filterDateDoghnutEnabled = false;
        limitedResult = _.takeRight((this.analyticsData as any).analytics, 60);
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
    onSubmitFilterDate() {
      this.initiliazeAnalytics(this.filterDate[0], this.filterDate[1]);
    },
    onSubmitFilterDateDoghnut() {
      this.initiliazeAnalytics(this.filterDateDoghnut[0], this.filterDateDoghnut[1]);
    },
    initiliazeAnalytics(startDate?: string, endDate?: string) {
      getAnalytics(this.agentName, 60, startDate, endDate).then((response) => {
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
          this.selectPeriod(this.period);
          this.selectPeriodForDoghnut(this.doghnutPeriod);
        }
      }).catch(() => {
        this.textMsg = 'error when loading analytics';
        this.classMsg = 'errorMsg';
      });
    },
  },
  mounted() {
    this.initiliazeAnalytics();
  },
});
</script>

<style scoped>
  .marginClass {
    margin-bottom: 5% !important;
  }
</style>
