<template>
  <div class="stats chartSize">
    <BarChart :chartData="chartDataBar" :options="chartOptionsBar" />
    <LineChart :chartData="chartDataLine" :options="chartOptionsLine" />
    <DoughnutChart :chartData="chartDataDoughnut" :options="chartOptionsDoughnut"/>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import BarChart from '@/components/stats/BarChart.vue';
import LineChart from '@/components/stats/LineChart.vue';
import DoughnutChart from '@/components/stats/DoughnutChart.vue';

export default Vue.extend({
  name: 'stats',
  components: {
    BarChart,
    LineChart,
    DoughnutChart,
  },
  data() {
    return {
      // Bar Data
      chartDataBar: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December'],
        datasets: [
          {
            label: 'Data One',
            backgroundColor: '#f87979',
            data: [40, 3, 10, 40, 5, 80, 5, 90, 23, 5, 20, 5],
          },
          {
            label: 'Data two',
            backgroundColor: '#f87979',
            data: [40, 3, 10, 40, 5, 80, 5, 90, 23, 5, 20, 5],
          },
        ],
      },
      chartOptionsBar: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
        responsive: true,
        maintainAspectRatio: false,
      },
      // Line Data
      chartDataLine: {
        labels: ['label1', 'label2', 'label3', 'label4', 'label5', 'label6', 'label7', 'label8',
          'label9', 'label10', 'label11', 'label12', 'label13', 'label14', 'label15', 'label16',
          'label17', 'label18', 'label19', 'label20'],
        datasets: [
          {
            label: 'My First Dataset',
            data: [65, 59, 80, 81, 56, 55, 40, 65, 59, 80, 81, 56, 55, 40, 65, 59, 80, 81, 56, 55],
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1,
          },
          {
            label: 'My second Dataset',
            data: [10, 59, 39, 81, 56, 55, 40, 10, 59, 10, 81, 56, 55, 40, 10, 59, 80, 81, 10, 55],
            fill: false,
            borderColor: 'rgb(47, 100, 50)',
            tension: 0.1,
          },
        ],
      },
      chartOptionsLine: {
        responsive: true,
        maintainAspectRatio: false,
      },
      // Doughnut Data
      chartDataDoughnut: {
        labels: [
          'Red',
          'Blue',
          'Yellow',
        ],
        datasets: [{
          label: 'My First Dataset',
          data: [300, 50, 100],
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)',
          ],
          hoverOffset: 4,
        }],
      },
      chartOptionsDoughnut: {
        responsive: true,
        maintainAspectRatio: false,
      },
    };
  },
});
</script>
