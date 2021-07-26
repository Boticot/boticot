<script>
import { Doughnut, mixins } from 'vue-chartjs';

export default {
  name: 'DoughnutChart',
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

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
