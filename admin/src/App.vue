<template>
  <div id="app">
    <el-row class="header-banner" style="height: 100px;">
      <el-image
      style="width: 304px; height: 84px; margin-top: 5px;"
      :src="require('@/assets/boticot.png')"
      fit="contain"></el-image>
      <div v-if="isLoggedIn" class="marginTopMedium marginRightSmall" style="float: right;">
        <el-button icon="el-icon-switch-button" @click="logout()" circle></el-button>
      </div>
    </el-row>
    <el-row>
      <el-col v-if="isLoggedIn">
        <div class="grid-content textAlignRight marginTopMedium">
          <span>Agent:</span>
          <el-select v-model="selectedAgent" placeholder="Select here" @change="selectAgent">
            <el-option
              v-for="choice in choices"
              :key="choice"
              :label="choice"
              :value="choice"
            ></el-option>
          </el-select>
        </div>
      </el-col>
    </el-row>
    <el-row v-if="isLoggedIn">
      <el-col>
        <div id="nav" style="padding: 10px">
          <el-tabs v-model="activeName" type="card" @tab-click="tabClick">
            <el-tab-pane label="Try it" name="try-it"/>
            <el-tab-pane label="Inputs" name="inputs" />
            <el-tab-pane label="Training Data" name="training-data" />
            <el-tab-pane label="Responses" name="responses" />
            <el-tab-pane label="Model" name="model" />
            <el-tab-pane label="Agents" name="agents" />
          </el-tabs>
        </div>
      </el-col>
    </el-row>
    <router-view :key="$route.name + ($route.params.agentName || '')" />
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { getAgentsNames } from '@/service/agentService';
import { getAgent } from '@/client/agent';

export default Vue.extend({
  name: 'app',
  data() {
    return {
      choices: this.$store.state.agents,
      selectedAgent: '',
      activeName: '',
    };
  },
  watch: {
    async choices() {
      [this.selectedAgent] = this.choices; // Select the first as default value
      this.$store.commit('updateAgent', await getAgent(this.selectedAgent));
    },
  },
  computed: {
    isLoggedIn() {
      return this.$store.getters.isLoggedIn();
    },
  },
  methods: {
    async selectAgent(value: string) {
      this.selectedAgent = value;
      if (this.$router.currentRoute.path !== '/agents') {
        this.$router.replace(value);
      }
      this.$store.commit('updateAgent', await getAgent(value));
    },
    tabClick(obj: any) {
      if (obj.name === 'agents') { // Except agents tab
        this.$router.replace(`/${obj.name}`);
      } else {
        this.$router.replace(`/${obj.name}/${this.selectedAgent}`);
      }
    },
    logout() {
      this.$store.commit('updateToken', '');
      window.location.reload();
    },
  },
  mounted() {
    if (this.$store.getters.isLoggedIn()) {
      getAgentsNames()
        .then((val) => {
          this.activeName = this.$router.currentRoute.name?.toLowerCase() || 'try-it';
          if (val.length === 0) {
            this.$router.replace('/agents');
          } else {
            this.$store.commit('initAgents', val);
            this.choices = this.$store.state.agents;
            if (this.$router.currentRoute.path === '/') {
              this.$router.replace(`/try-it/${this.choices[0]}`);
            }
          }
        })
        .catch(() => {
          this.choices = ['ERROR...'];
        });
    }
  },
});
</script>

<style>
  @import 'assets/css/global.css';
</style>
