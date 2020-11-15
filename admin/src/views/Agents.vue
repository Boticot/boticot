<template>
  <div class="agents halfSize">
    <el-card class="box-card textAlignLeft">
      <h4 class="textAlignCenter">Create New Agent</h4>
      <el-form :model="newAgent" :rules="rules" ref="newAgent" label-width="120px">
        <el-row v-if="textMsg !== ''" :class="classMsg" class="marginBottomMedium marginLeftMedium">
          {{ textMsg }}
        </el-row>
        <el-form-item label="Agent name" prop='name'>
          <el-input v-model="newAgent.name"></el-input>
        </el-form-item>
        <el-form-item label="NLU Conf">
          <el-radio-group v-model="newAgent.configType" @change="selectConf">
            <el-tooltip
              class="item"
              effect="dark"
              content="Recommended when you have more than 1000 training data"
              placement="top-start"
            >
              <el-radio label="supervised_embeddings">
                Supervised Embeddings
              </el-radio>
            </el-tooltip>
            <el-tooltip
              class="item"
              effect="dark"
              content="Recommended when you need a specific nlu pipeline"
              placement="top-start"
            >
              <el-radio label="specific_pipeline">
                Specific Pipeline
              </el-radio>
            </el-tooltip>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="Language" :class="[isHideSpecificPipeline ? '' : 'displayNone']">
          <el-select v-model="newAgent.language" placeholder="please select your zone">
            <el-option label="English" value="en"></el-option>
            <el-option label="French" value="fr"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Specific pipeline" :class="[isHideSpecificPipeline ? 'displayNone' : '']">
          <el-input type="textarea" :rows="10" v-model="newAgent.pipeline"></el-input>
        </el-form-item>
        <el-form-item label="Fallback">
          <el-tooltip
            class="item"
            effect="dark"
            content="percentage"
            placement="top-start"
          >
            <el-input-number v-model="newAgent.fallback" :min="0" :max="100"></el-input-number>
          </el-tooltip>
        </el-form-item>
        <el-form-item label="Training Data">
          <el-input type="textarea" :rows="7" v-model="newAgent.trainingData"></el-input>
        </el-form-item>
        <el-form-item label="Responses">
          <el-input type="textarea" :rows="7" v-model="newAgent.responses"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="createAgent">Create Agent</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <el-card class="box-card" :class="[isHideExistingAgents ? 'displayNone' : '']">
      <h4>Existing Agents</h4>
      <el-table :data="agents" style="width: 100%">
        <el-table-column prop="name" label="Name" width="150"></el-table-column>
        <el-table-column prop="currentVersion" label="Current Version" width="150"></el-table-column>
        <el-table-column prop="lastVersion" label="Last Version" width="150"></el-table-column>
        <el-table-column prop="lastTrain" label="Last Train" width="150"></el-table-column>
        <el-table-column prop="lastModified" label="Last Modified" width="150"></el-table-column>
        <el-table-column fixed="right" width="100">
          <template slot-scope="scope">
            <el-button
            type="danger"
            @click="deleteAgent(scope.row.name)"
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
import { createNewAgent } from '@/service/agentService';
import { getAgents, deleteAgent } from '@/client/agent';

const pipelineExample = {
  language: 'fr',
  pipeline: [
    { name: 'WhitespaceTokenizer' },
    { name: 'RegexFeaturizer' },
    { name: 'CountVectorsFeaturizer', analyzer: 'char_wb' },
    { name: 'CRFEntityExtractor' },
    { name: 'EntitySynonymMapper' },
    { name: 'EmbeddingIntentClassifier', epochs: 120 },
  ],
};

const trainingDataExample = {
  common_examples: [
    {
      intent: 'greetings_hello',
      text: 'hello',
    },
    {
      intent: 'greetings_bye',
      text: 'bye',
    },
  ],
};

const responsesExample = [
  {
    intent: 'greetings_hello',
    fulfillment_text: 'Hello !',
  },
  {
    intent: 'greetings_bye',
    fulfillment_text: 'See you soon, bye !',
  },
  {
    intent: 'greetings_bye',
    fulfillment_text: 'Bye !',
  },
];

export default Vue.extend({
  name: 'agents',
  data() {
    return {
      newAgent: {
        name: '',
        language: 'en',
        configType: 'supervised_embeddings',
        pipeline: JSON.stringify(pipelineExample, null, 2),
        fallback: 20,
        trainingData: JSON.stringify(trainingDataExample, null, 2),
        responses: JSON.stringify(responsesExample, null, 2),
      },
      rules: {
        name: [
          { required: true, message: 'Please input Agent name', trigger: 'blur' },
          { pattern: /^[a-zA-Z0-9]*$/, message: 'Must be only alphanumeric', trigger: 'blur' },
        ],
      },
      isHideSpecificPipeline: true,
      error: '',
      textMsg: '',
      classMsg: '',
      agents: Array<any>(),
      isHideExistingAgents: false,
    };
  },
  methods: {
    async createAgent(e: any) {
      const { newAgent }: any = this.$refs;
      newAgent.validate(
        async (valid: any) => {
          if (valid) {
            try {
              const response: any = await createNewAgent(
                this.newAgent.name,
                this.newAgent.configType,
                this.newAgent.language,
                JSON.parse(this.newAgent.pipeline),
                this.newAgent.fallback,
                JSON.parse(this.newAgent.trainingData),
                JSON.parse(this.newAgent.responses),
              );
              this.textMsg = response.message;
              this.classMsg = 'successMsg';
            } catch (error) {
              if (error.statusCode === 400) {
                if (error.error.message) {
                  this.textMsg = error.error.message;
                }
              } else {
                this.textMsg = 'Creation Agent server Error, please retry later.';
              }
              this.classMsg = 'errorMsg';
              return false;
            }
            this.agents.push({
              name: this.newAgent.name,
            });
            this.$store.commit('addAgent', this.newAgent.name);
            this.isHideExistingAgents = false;
            e.preventDefault();
          }
          return false;
        },
      );
    },
    selectConf() {
      if (this.newAgent.configType === 'specific_pipeline') {
        this.isHideSpecificPipeline = false;
      } else {
        this.isHideSpecificPipeline = true;
      }
    },
    deleteAgent(name: string) {
      deleteAgent(name);
      this.$store.commit('deleteAgent', name);
      this.agents = this.agents.filter((e: any) => (e.name !== name));
      if (this.agents.length === 0) {
        this.isHideExistingAgents = true;
      }
    },
  },
  mounted() {
    getAgents()
      .then((val: any) => {
        this.agents = val;
        if (this.agents.length === 0) {
          this.isHideExistingAgents = true;
        }
      })
      .catch(() => {
        this.isHideExistingAgents = true;
      });
  },
});
</script>
