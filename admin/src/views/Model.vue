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
      <el-table :data="intents" style="width: 100%">
        <el-table-column prop="intent" label="Intent"></el-table-column>
        <el-table-column fixed="right" width="90">
          <template slot-scope="scope">
            <el-tooltip
            class="box-item"
            effect="light"
            content="Export intent"
            placement="top"
            >
              <el-button
              type="primary"
              @click="downloadAgentIntentFile(agentName, scope.row.intent, false)"
              icon="el-icon-download"
              :style="{ marginLeft: '15px' }"
              plain
              ></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column fixed="right" width="90">
          <template slot-scope="scope">
            <el-tooltip
            class="box-item"
            effect="light"
            content="Export full intent tree"
            placement="top"
            >
              <el-button
                type="primary"
                @click="downloadAgentIntentFile(agentName, scope.row.intent, true)"
                icon="el-icon-folder-add"
                :style="{ marginLeft: '15px' }"
                plain
              ></el-button>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column v-if="!isReadUser()" fixed="right" width="90">
          <template slot-scope="scope">
            <el-button
            type="danger"
            @click="deleteSelectedIntent(scope.row.intent)"
            icon="el-icon-delete"
            :style="{ marginLeft: '15px' }"
            plain
          ></el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import { mapGetters } from 'vuex';
import { GlobalEntity } from '@/types';
import { getAgent, deleteAgentIntent, getAgentIntentFile } from '@/client/agent';
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
  computed: {
    ...mapGetters([
      'isReadUser',
    ]),
  },
  methods: {
    async updateModelDetails() {
      const agentResponse = await getAgent(this.agentName);
      if (agentResponse.versions && agentResponse.versions.length !== 0) {
        this.versions = agentResponse.versions.map(
          (e: any) => ({ name: e, current: (e === agentResponse.current_version) ? 'X' : '' }),
        );
        this.displayVersions = true;
      }
      if (agentResponse.intents && agentResponse.intents.length !== 0) {
        this.intents = agentResponse.intents.sort().map(
          (intent: string) => ({ intent }),
        );
        this.displayIntents = true;
      }
      if (agentResponse.entities && agentResponse.entities.length !== 0) {
        this.entities = initEntities(agentResponse.entities);
        this.displayEntities = true;
      }
      this.config = JSON.stringify(agentResponse.config, null, 2);
    },
    async deleteSelectedIntent(intent: string) {
      try {
        await deleteAgentIntent(this.agentName, intent);
        this.$store.commit('deleteIntent', intent);
        this.intents = this.intents.filter((i: any) => (i.intent !== intent));
        if (this.intents.length === 0) {
          this.displayIntents = false;
        }
        this.$notify.success({
          title: 'Success',
          message: `Intent ${intent} removed`,
          offset: 100,
        });
      } catch (e) {
        this.$notify.error({
          title: 'Error',
          message: `Error when remove intent ${intent}`,
          offset: 100,
        });
      }
    },
    async downloadAgentIntentFile(agentName: string, intent: string, fullTree: boolean) {
      const response = await getAgentIntentFile(agentName, intent, fullTree);
      const buffer = Buffer.from(response);
      const fileURL = window.URL.createObjectURL(new Blob([buffer]));
      const fileLink = document.createElement('a');
      fileLink.href = fileURL;
      fileLink.setAttribute('download', `${agentName}_${intent}${fullTree ? '_full' : ''}.json`);
      document.body.appendChild(fileLink);
      fileLink.click();
    },
  },
  mounted() {
    this.updateModelDetails();
  },
});
</script>
