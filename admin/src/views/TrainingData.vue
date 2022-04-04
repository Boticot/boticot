<template>
  <div class="training-data halfSize" v-loading="loading">
    <el-row :gutter="10">
        <el-col :span="10">
          <el-select v-model="intentName" clearable="true" placeholder="Search by intent">
            <el-option v-for="choice in allIntents" :key="choice" :label="choice" :value="choice"></el-option>
          </el-select>
        </el-col>
        <el-col :span="10">
          <el-input placeholder="Search by text" v-model="text"></el-input>
        </el-col>
        <el-col :span="4" :style="{ textAlign: 'left'}">
          <el-button type="primary" @click="updateTrainingData(1)">Search</el-button>
        </el-col>
    </el-row>
    <h3 class="marginBottomMedium">Training Data count: {{ count }}</h3>
    <el-pagination v-if="count != 0" background layout="prev, pager, next" @current-change="pageChange"
    :current-page="currentPage" :page-size="pageSize" :total="count">
    </el-pagination>
    <el-collapse
      v-model="activeNames"
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
import { mapState } from 'vuex';
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
      intentName: '',
      text: '',
      count: 0,
      pageSize: 0,
      currentPage: 1,
    };
  },
  computed: {
    ...mapState({
      allIntents: 'intents',
    }),
  },
  methods: {
    async updateTrainingData(page: number) {
      this.loading = true;
      const resp = await getAgentTrainingData(this.agentName, this.intentName,
        this.text, page);
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
