<template>
  <div class="model halfSize">
    <el-card class="box-card" :class="[displayVersions ? '' : 'displayNone']">
      <h4>Versions</h4>
      <el-table :data="versions" style="width: 100%">
        <el-table-column prop="name" label="Name" width="180"></el-table-column>
        <el-table-column prop="current" label="Current" width="180"></el-table-column>
      </el-table>
    </el-card>
    <el-card class="box-card">
      <h4>Configuration</h4>
      <el-input type="textarea" :rows="8" placeholder="Configuration" v-model="config"></el-input>
    </el-card>
    <el-card class="box-card" :class="[displayEntities ? '' : 'displayNone']">
      <h4>Entities</h4>
      <div v-for="entity in entities" :key="entity.entity" class="marginTopSmall">
        <span style="vertical-align: -webkit-baseline-middle;">{{entity.entity}}</span>
        <el-button
          :style="{ marginLeft: '15px', backgroundColor: entity.color }"
          plain
        ></el-button>
      </div>
    </el-card>
    <el-card class="box-card" :class="[displayIntents ? '' : 'displayNone']">
      <h4>Intents</h4>
      <div v-for="intent in intents" :key="intent">
        <li class="textAlignLeft marginLeftMedium">{{intent}}</li>
      </div>
    </el-card>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import { GlobalEntity } from '@/types';
import { getAgent } from '@/client/agent';
import { initEntities } from '@/service/entityService';

export default Vue.extend({
  name: 'model',
  data() {
    return {
      agentName: this.$route.params.agentName,
      displayIntents: false,
      intents: Array<string>(),
      displayEntities: false,
      entities: Array<GlobalEntity>(),
      displayVersions: false,
      versions: Array<unknown>(),
      config: '',
    };
  },
  methods: {
    async updateModelDetails() {
      const agentResponse = await getAgent(this.agentName);
      if (agentResponse.versions && agentResponse.versions.length !== 0) {
        this.versions = agentResponse.versions.map(
          (e: any) => ({ name: e, current: (e === agentResponse.currentVersion) ? 'X' : '' }),
        );
        this.displayVersions = true;
      }
      if (agentResponse.intents && agentResponse.intents.length !== 0) {
        this.intents = agentResponse.intents;
        this.displayIntents = true;
      }
      if (agentResponse.entities && agentResponse.entities.length !== 0) {
        this.entities = initEntities(agentResponse.entities);
        this.displayEntities = true;
      }
      this.config = JSON.stringify(agentResponse.config, null, 2);
    },
  },
  mounted() {
    this.updateModelDetails();
  },
});
</script>
