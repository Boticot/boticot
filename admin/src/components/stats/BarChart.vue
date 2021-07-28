<script>
import { Bar, mixins } from 'vue-chartjs';

export default {
  name: 'BarChart',
  extends: Bar,
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
