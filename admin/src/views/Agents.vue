<template>
  <div class="agents halfSize">
    <el-card class="box-card textAlignLeft" v-loading="loading">
      <h4 class="textAlignCenter">Create New Agent</h4>
      <el-form :model="newAgent" :rules="rules" ref="newAgent" label-width="120px">
        <el-row v-if="textMsg !== ''" :class="classMsg" class="marginBottomMedium marginLeftMedium">
          {{ textMsg }}
        </el-row>
        <el-form-item label="Agent name" prop='name'>
          <el-input v-model="newAgent.name"></el-input>
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
        <el-form-item>
          <el-radio-group v-model="agentCreationOption" @change="resetDefaultValue">
              <el-radio label="create_new_agent">
                Create new Agent
              </el-radio>
              <el-radio label="import_agent">
                Import Agent file
              </el-radio>
        </el-radio-group>
        </el-form-item>
         <div v-if="agentCreationOption === 'create_new_agent'">
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
            <el-select v-model="newAgent.language">
              <el-option label="English" value="en"></el-option>
              <el-option label="French" value="fr"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="Specific pipeline" :class="[isHideSpecificPipeline ? 'displayNone' : '']">
            <el-input type="textarea" :rows="10" v-model="newAgent.pipeline"></el-input>
          </el-form-item>
          <el-form-item label="Training Data">
            <el-input type="textarea" :rows="7" v-model="newAgent.trainingData"></el-input>
          </el-form-item>
          <el-form-item label="Responses">
            <el-input type="textarea" :rows="7" v-model="newAgent.responses"></el-input>
          </el-form-item>
        </div>
        <div v-else>
          <el-form-item>
            <el-upload
              action=""
              :auto-upload="false"
              ref="upload"
              :on-change="importAgent"
              :on-remove="removeFile"
              :limit="1">
              <el-button slot="trigger" size="small" type="primary">Upload agent file</el-button>
            </el-upload>
          </el-form-item>
        </div>
        <el-form-item>
          <el-button type="primary" @click="createAgent">Create Agent</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <el-card class="box-card" :class="[isHideExistingAgents ? 'displayNone' : '']">
      <h4>Existing Agents</h4>
      <el-table :data="agents" style="width: 100%">
        <el-table-column prop="name" label="Name" width="150"></el-table-column>
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
        <el-table-column fixed="right" width="90">
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
import { getAgents, deleteAgent, getAgentFile } from '@/client/agent';

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
    response_type: 'TEXT',
    data: {
      fulfillment_text: 'Hello !',
    },
  },
  {
    intent: 'greetings_bye',
    response_type: 'TEXT',
    data: {
      fulfillment_text: 'See you soon, bye !',
    },
  },
  {
    intent: 'greetings_bye',
    response_type: 'TEXT',
    data: {
      fulfillment_text: 'Bye !',
    },
  },
];

export default Vue.extend({
  name: 'agents',
  data() {
    return {
      file: null,
      fileContent: null,
      agentCreationOption: 'create_new_agent',
      newAgent: {
        name: '',
        language: 'en',
        configType: 'supervised_embeddings',
        pipeline: JSON.stringify(pipelineExample, null, 2),
        fallback: 40,
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
      loading: false,
    };
  },
  methods: {
    cleanUpFile() {
      this.file = null;
      this.fileContent = null;
      (this.$refs.upload as any).clearFiles();
    },
    resetDefaultValue() {
      this.textMsg = '';
      this.classMsg = '';
      if (this.agentCreationOption === 'create_new_agent') {
        this.newAgent = {
          ...this.newAgent,
          language: 'en',
          configType: 'supervised_embeddings',
          pipeline: JSON.stringify(pipelineExample, null, 2),
          fallback: 40,
          trainingData: JSON.stringify(trainingDataExample, null, 2),
          responses: JSON.stringify(responsesExample, null, 2),
        };
      } else if (this.agentCreationOption === 'import_agent') {
        this.cleanUpFile();
      }
    },
    checkIfJSONFile(file: any): boolean {
      return file.name.includes('.json');
    },
    checkIfValidJsonFormat(fileContent: any): boolean {
      if (!(Object.prototype.hasOwnProperty.call(fileContent, 'config')
            && Object.prototype.hasOwnProperty.call(fileContent, 'rasa_nlu_data')
            && Object.prototype.hasOwnProperty.call(fileContent, 'responses'))) {
        return false;
      }
      return true;
    },
    importAgent(file: any) {
      this.file = file;
      this.textMsg = '';
      this.classMsg = '';
      if (!this.checkIfJSONFile(file)) {
        return;
      }
      const reader = new FileReader();
      reader.readAsText(file.raw);
      reader.onload = async (e) => {
        try {
          this.fileContent = JSON.parse(e.target?.result as string);
          if (!this.checkIfValidJsonFormat(this.fileContent)) {
            return;
          }
          this.newAgent.configType = Array.isArray((this.fileContent as any).config.pipeline)
            ? 'specific_pipeline' : 'supervised_embeddings';
          this.newAgent.language = (this.fileContent as any).config.language;
          this.newAgent.pipeline = JSON.stringify((this.fileContent as any).config, null, 2);
          this.newAgent.trainingData = JSON.stringify((this.fileContent as any).rasa_nlu_data, null, 2);
          this.newAgent.responses = JSON.stringify((this.fileContent as any).responses, null, 2);
        } catch (err) {
          this.textMsg = 'System Error';
          this.classMsg = 'errorMsg';
        }
      };
    },
    removeFile() {
      this.cleanUpFile();
      this.textMsg = '';
      this.classMsg = '';
    },
    async createAgent(e: any) {
      const { newAgent }: any = this.$refs;
      newAgent.validate(
        async (valid: any) => {
          if (valid) {
            try {
              if (this.agentCreationOption === 'import_agent') {
                if (this.file === null) {
                  this.textMsg = 'Please upload an agent file';
                  this.classMsg = 'errorMsg';
                  return false;
                }
                if (!this.checkIfJSONFile(this.file)) {
                  this.textMsg = 'Please upload a json file of your agent';
                  this.classMsg = 'errorMsg';
                  this.cleanUpFile();
                  return false;
                }
                if (!this.checkIfValidJsonFormat(this.fileContent)) {
                  this.textMsg = 'Please upload a valid agent file';
                  this.classMsg = 'errorMsg';
                  this.cleanUpFile();
                  return false;
                }
              }
              this.loading = true;
              const response: any = await createNewAgent(
                this.newAgent.name,
                this.newAgent.configType,
                this.newAgent.language,
                JSON.parse(this.newAgent.pipeline),
                this.newAgent.fallback,
                JSON.parse(this.newAgent.trainingData),
                this.newAgent.responses ? JSON.parse(this.newAgent.responses) : [],
              );
              this.textMsg = response.message;
              this.classMsg = 'successMsg';
              this.loading = false;
            } catch (error) {
              if (error.statusCode === 400) {
                if (error.error.message) {
                  this.textMsg = error.error.message;
                }
              } else {
                this.textMsg = 'Creation Agent server Error, please retry later.';
              }
              this.classMsg = 'errorMsg';
              this.loading = false; // spinner should also be closed even if there is an error
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
