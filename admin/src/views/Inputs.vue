<template>
  <div class="inputs halfSize" v-loading="loading">
    <el-row :gutter="10">
        <el-col :span="10">
          <el-tooltip
              class="box-item"
              :content="intentName || 'No intent selected'"
              placement="top-start"
              effect="light"
            >
            <el-select class="w-100" v-model="intentName" clearable="true" placeholder="Search by intent">
              <el-option v-for="choice in allIntents" :key="choice" :label="choice" :value="choice"></el-option>
            </el-select>
          </el-tooltip>
        </el-col>
        <el-col :span="10">
          <el-input placeholder="Search by text" v-model="text"></el-input>
        </el-col>
        <el-col :span="4" :style="{ textAlign: 'left'}">
          <el-button class="w-100" type="primary" @click="updateInputs(1)">Search</el-button>
        </el-col>
    </el-row>
    <h3 class="marginBottomMedium">
      <span>Users Inputs count: {{count}}</span>
      <el-button
        type="primary"
        @click="pageChange(1)"
        icon="el-icon-refresh-right"
        :style="{ marginLeft: '15px' }"
        plain>
      </el-button>
    </h3>
    <el-pagination v-if="count != 0" background layout="prev, pager, next" @current-change="pageChange"
    :current-page="currentPage" :page-size="pageSize" :total="count">
    </el-pagination>
     <el-collapse
      v-model="activeNames"
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
import { mapState } from 'vuex';
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
    async updateInputs(page: number) {
      this.loading = true;
      const resp = await getAgentInputs(this.agentName, this.intentName,
        this.text, page);
      this.inputs = resp.items;
      this.count = resp.count;
      this.loading = false;
    },
    pageChange(page: number) {
      this.currentPage = page;
      this.loading = true;
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
