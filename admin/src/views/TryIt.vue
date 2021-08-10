<template>
  <div class="try-it halfSize">
    <form v-on:submit.prevent="onSubmit">
      <el-row v-if="error !== ''" class="marginLeftMedium marginBottomMedium">
        <span style="color: red;">{{ error }}</span>
      </el-row>
      <el-row :gutter="10">
        <el-col :span="20">
          <el-input placeholder="Enter a text" v-model="text"></el-input>
        </el-col>
        <el-col :span="4" :style="{ textAlign: 'left'}">
          <el-button type="primary" @click="onSubmit">Try it</el-button>
        </el-col>
      </el-row>
    </form>
    <div v-if="isNluDataNotEmpty()">
      <el-row style="margin-top: 20px;">
        <el-collapse v-model="activeNames">
          <NluEntryComponent :agentName='agentName' :data="nluData" />
        </el-collapse>
      </el-row>
    </div>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import _ from 'lodash';
import NluEntryComponent from '@/components/NluEntry.vue';
import { getNluEntryFromParseText } from '@/service/nluService';

export default Vue.extend({
  name: 'try-it',
  components: {
    NluEntryComponent,
  },
  data() {
    return {
      agentName: this.$route.params.agentName,
      text: '',
      error: '',
      nluData: {},
      activeNames: ['1'],
    };
  },
  methods: {
    isNluDataNotEmpty() {
      return !_.isEmpty(this.nluData);
    },
    async onSubmit() {
      try {
        this.nluData = await getNluEntryFromParseText(this.agentName, this.text);
      } catch (e) {
        this.error = 'Server Error, please retry later.';
      }
    },
  },
});
</script>
