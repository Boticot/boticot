<script>
import { Doughnut, mixins } from 'vue-chartjs';

export default {
  name: 'DoghnutChart',
  extends: Doughnut,
  mixins: [mixins.reactiveProp],
  props: {
    chartData: {
      type: Object,
      default: null,
      required: false,
    },
    options: {
      type: Object,
      default: null,
      required: false,
    },
  },
  mounted() {
    this.renderChart(this.chartData, this.options);
  },
};
</script>
