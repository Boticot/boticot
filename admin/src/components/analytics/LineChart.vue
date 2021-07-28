<script>
import { Line, mixins } from 'vue-chartjs';

export default {
  name: 'LineChart',
  extends: Line,
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
