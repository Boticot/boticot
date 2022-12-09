<template>
  <div class="agents tableSize">
    <el-card class="box-card textAlignLeft" v-loading="loading">
      <h4 class="textAlignCenter">Create New Agent</h4>
      <AgentEditor
      :isEditor="false"
      v-on:updated="agentUpdated">
      </AgentEditor>
    </el-card>
    <el-card class="box-card" v-if="!hideExistingAgents">
      <h4>Existing Agents</h4>
      <el-table :data="agents" style="width: 100%">
        <el-table-column prop="name" label="Name" min-width="150"></el-table-column>
        <el-table-column prop="current_version" label="Current Version" width="150"></el-table-column>
        <el-table-column prop="last_version" label="Last Version" width="150"></el-table-column>
        <el-table-column prop="last_train" label="Last Train" width="110"></el-table-column>
        <el-table-column prop="last_modified" label="Last Modified" width="120"></el-table-column>
        <el-table-column fixed="right" width="90">
          <template slot-scope="scope">
            <el-button
            type="primary"
            @click="downloadAgentFile(scope.row.name)"
            icon="el-icon-download"
            :style="{ marginLeft: '15px' }"
            plain
          ></el-button>
          </template>
        </el-table-column>
        <el-table-column v-if="!isReadUser()" fixed="right" width="90">
          <template slot-scope="scope">
            <el-button
            type="primary"
            @click="editAgent(scope.row)"
            icon="el-icon-edit"
            :style="{ marginLeft: '15px' }"
            plain
          ></el-button>
          </template>
        </el-table-column>
        <el-table-column v-if="!isReadUser()" fixed="right" width="90">
          <template slot-scope="scope">
            <el-button
            type="danger"
            @click="openDeleteDialog(scope.row.name)"
            icon="el-icon-delete"
            :style="{ marginLeft: '15px' }"
            plain
          ></el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-dialog
    :visible.sync="editDialogVisible"
    :title="`Edit agent: ${editData.name}`"
    :lock-scroll="true"
    close-on-click-modal
    close-on-press-escape
    width="65%"
    >
      <AgentEditor
      :key="editorKey"
      v-if="editDialogVisible"
      :isEditor="true"
      :defaultData="editData"
      v-on:updated="agentUpdated">
      </AgentEditor>
    </el-dialog>
    <el-dialog :visible.sync="deleteAgentDialogVisible">
      <div style="font-size: 18px;">
        Are you sure you want to delete agent "{{agentToDelete}}"?
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteAgentDialogVisible = false">Cancel</el-button>
          <el-button type="danger" @click="deleteAgent(agentToDelete)">
            Delete agent
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import { mapGetters } from 'vuex';
import { getAgents, deleteAgent, getAgentFile } from '@/client/agent';
import AgentEditor from '@/components/AgentEditor.vue';

export default Vue.extend({
  name: 'agents',
  components: {
    AgentEditor,
  },
  data() {
    return {
      agentCreationOption: 'create_new_agent',
      agents: Array<any>(),
      hideExistingAgents: false,
      loading: false,
      editDialogVisible: false,
      deleteAgentDialogVisible: false,
      agentToDelete: '',
      editData: {
        name: '',
        language: 'en',
        configType: 'supervised_embeddings',
        pipeline: {},
        fallback: 40,
        trainingData: {},
        responses: {},
      },
      editorKey: 0,
    };
  },
  computed: {
    ...mapGetters([
      'isSuperAdmin',
      'isReadUser',
    ]),
  },
  methods: {
    openDeleteDialog(agent: string) {
      this.agentToDelete = agent;
      this.deleteAgentDialogVisible = true;
    },
    deleteAgent(name: string) {
      this.deleteAgentDialogVisible = false;
      deleteAgent(name);
      this.$store.commit('deleteAgent', name);
      this.agents = this.agents.filter((e: any) => (e.name !== name));
      if (this.agents.length === 0) {
        this.hideExistingAgents = true;
      }
      this.$notify.info({
        title: 'Info',
        message: `Agent '${name}' removed`,
        offset: 100,
      });
    },
    async downloadAgentFile(name: string) {
      const response = await getAgentFile(name);
      const buffer = Buffer.from(response);
      const fileURL = window.URL.createObjectURL(new Blob([buffer]));
      const fileLink = document.createElement('a');
      fileLink.href = fileURL;
      fileLink.setAttribute('download', `${name}.json`);
      document.body.appendChild(fileLink);
      fileLink.click();
    },
    editAgent(agentData: any) {
      this.editData = agentData;
      this.editorKey += 1;
      this.editDialogVisible = true;
    },
    agentUpdated() {
      this.editDialogVisible = false;
      getAgents()
        .then((val: any) => {
          this.agents = val;
          if (this.agents.length === 0) {
            this.hideExistingAgents = true;
          }
        })
        .catch(() => {
          this.hideExistingAgents = true;
        });
    },
  },
  mounted() {
    getAgents()
      .then((val: any) => {
        this.agents = val;
        if (this.agents.length === 0) {
          this.hideExistingAgents = true;
        }
      })
      .catch(() => {
        this.hideExistingAgents = true;
      });
  },
});
</script>
