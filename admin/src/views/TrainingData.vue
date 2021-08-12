<template>
  <div class="training-data" v-loading="loading">
    <h3 class="marginBottomMedium">Training Data for agent {{ agentName }}: {{ count }}</h3>
    <el-pagination v-if="count != 0" background layout="prev, pager, next" @current-change="pageChange"
    :current-page="currentPage" :page-size="pageSize" :total="count">
    </el-pagination>
    <el-collapse
      v-model="activeNames"
      class="halfSize"
      accordion
    >
      <div v-for="data in trainingData" :key="data.id">
        <NluEntryComponent :agentName='agentName' :data='data'  v-on:select-new-entity="updateActiveItem"/>
      </div>
    </el-collapse>
    <el-pagination v-if="count != 0" background layout="prev, pager, next" @current-change="pageChange"
    :current-page="currentPage" :page-size="pageSize" :total="count">
    </el-pagination>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import NluEntryComponent from '@/components/NluEntry.vue';
import { getAgentTrainingData } from '@/service/nluService';

export default Vue.extend({
  name: 'training-data',
  components: {
    NluEntryComponent,
  },
  data() {
    return {
      agentName: this.$route.params.agentName,
      trainingData: {},
      loading: true,
      activeNames: [''],
      count: 0,
      pageSize: 0,
      currentPage: 1,
    };
  },
  methods: {
    async updateTrainingData(page: number) {
      const resp = await getAgentTrainingData(this.agentName, page);
      this.trainingData = resp.items;
      this.count = resp.count;
      this.loading = false;
    },
    pageChange(page: number) {
      this.currentPage = page;
      this.loading = true;
      this.updateTrainingData(page);
    },
    updateActiveItem(id: string) {
      this.activeNames = [id];
    },
  },
  mounted() {
    const { VUE_APP_NLU_ENTRIES_PAGE_SIZE } = process.env;
    this.pageSize = Number(VUE_APP_NLU_ENTRIES_PAGE_SIZE);
    this.updateTrainingData(1);
  },
});
</script>
