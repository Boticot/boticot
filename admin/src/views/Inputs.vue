<template>
  <div class="inputs" v-loading="loading">
    <h3 class="marginBottomMedium">Users Inputs for agent {{ agentName }}: {{count}}</h3>
    <el-pagination v-if="count != 0" background layout="prev, pager, next" @current-change="pageChange"
    :current-page="currentPage" :page-size="pageSize" :total="count">
    </el-pagination>
     <el-collapse
      v-model="activeNames"
      class="halfSize"
      accordion
    >
      <div v-for="data in inputs" :key="data.id">
                <NluEntryComponent :agentName='agentName' :data='data' v-on:select-new-entity="updateActiveItem"/>
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
import { getAgentInputs } from '@/service/nluService';

export default Vue.extend({
  name: 'inputs',
  components: {
    NluEntryComponent,
  },
  data() {
    return {
      agentName: this.$route.params.agentName,
      inputs: {},
      loading: true,
      activeNames: [''],
      count: 0,
      pageSize: 0,
      currentPage: 1,
    };
  },
  methods: {
    async updateInputs(page: number) {
      const resp = await getAgentInputs(this.agentName, page);
      this.inputs = resp.items;
      this.count = resp.count;
      this.loading = false;
    },
    pageChange(page: number) {
      this.currentPage = page;
      this.updateInputs(page);
    },
    updateActiveItem(id: string) {
      this.activeNames = [id];
    },
  },
  mounted() {
    const { VUE_APP_NLU_ENTRIES_PAGE_SIZE } = process.env;
    this.pageSize = Number(VUE_APP_NLU_ENTRIES_PAGE_SIZE);
    this.updateInputs(1);
  },
});
</script>
