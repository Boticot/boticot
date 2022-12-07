<template>
  <el-form :model="newAgent" :rules="rules" ref="newAgent"
  label-width="150px" label-position="left" v-loading="loading">
    <el-row v-if="textMsg !== ''" :class="classMsg" class="marginBottomMedium marginLeftMedium">
      {{ textMsg }}
    </el-row>
    <el-form-item label="Agent name" prop='name'>
      <el-input v-model="newAgent.name" :disabled="isEditor"></el-input>
    </el-form-item>
    <el-form-item style="text-align: left">
      <el-radio-group v-model="editorOption" @change="resetDefaultValue" v-if="!isEditor">
        <el-radio label="create_new_agent">
          Create new Agent
        </el-radio>
        <el-radio label="import_agent">
          Import Agent file
        </el-radio>
      </el-radio-group>
    </el-form-item>
    <div v-if="editorOption === 'import_agent'">
      <el-form-item>
        <el-upload v-if="!isReadUser()" action="" :auto-upload="false" ref="upload" drag :on-change="importAgent"
          :on-remove="removeFile" :limit="1" class="formItem">
          <el-icon class="el-icon-upload"></el-icon>
          <div class="el-upload__text">
            Drop file here or <em>click to upload</em>
          </div>
        </el-upload>
      </el-form-item>
    </div>
    <div v-if="file !== null || editorOption === 'create_new_agent'">
      <el-form-item label="Fallback">
        <el-tooltip class="item " effect="dark" content="percentage" placement="top-start">
          <el-input-number v-model="newAgent.fallback" :min="0" :max="100"
          class="formItem" style="width: 200px"></el-input-number>
        </el-tooltip>
      </el-form-item>
      <el-form-item label="NLU Conf" style="text-align: left">
        <el-radio-group v-model="newAgent.configType" @change="selectConf">
          <el-tooltip class="item" effect="dark"
          content="Recommended when you have more than 1000 training data" placement="top-start">
            <el-radio label="supervised_embeddings">
              Supervised Embeddings
            </el-radio>
          </el-tooltip>
          <el-tooltip class="item" effect="dark" content="Recommended when you need a specific nlu pipeline"
            placement="top-start">
            <el-radio label="specific_pipeline">
              Specific Pipeline
            </el-radio>
          </el-tooltip>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="Language" :class="[hideSpecificPipeline ? '' : 'displayNone']">
        <el-select v-model="newAgent.language" class="formItem" style="width: 200px">
          <el-option label="English" value="en"></el-option>
          <el-option label="French" value="fr"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="Specific pipeline" :class="[hideSpecificPipeline ? 'displayNone' : '']">
        <el-input type="textarea" :rows="10" v-model="newAgent.pipeline" class="formItem"></el-input>
      </el-form-item>
      <el-form-item label="Training Data" v-if="!isEditor">
        <el-input type="textarea" :disabled="isEditor" :rows="8"
        v-model="newAgent.trainingData" class="formItem"></el-input>
      </el-form-item>
      <el-form-item label="Responses" v-if="!isEditor">
        <el-input type="textarea" :disabled="isEditor" :rows="8"
        v-model="newAgent.responses" class="formItem"></el-input>
      </el-form-item>
    </div>
    <el-form-item v-if="!isReadUser()" class="formItem">
      <el-button type="primary" @click="createAgent">
        <span v-if="isEditor">Update Agent</span>
        <span v-else>Create Agent</span>
      </el-button>
    </el-form-item>
  </el-form>
</template>
<script lang='ts'>
import Vue from 'vue';
import { mapGetters } from 'vuex';
import { createAgent } from '@/service/agentService';

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
  name: 'AgentEditor',
  props: {
    isEditor: {
      type: Boolean,
      default() {
        return false;
      },
    },
    defaultData: {
      type: Object,
      default() {
        return {};
      },
    },
  },
  data() {
    return {
      file: null,
      fileContent: null,
      editorOption: 'create_new_agent',
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
      hideSpecificPipeline: true,
      error: '',
      textMsg: '',
      classMsg: '',
      loading: false,
    };
  },
  computed: {
    ...mapGetters([
      'isSuperAdmin',
      'isReadUser',
    ]),
  },
  async mounted() {
    if (this.isEditor) {
      this.loading = true;
      this.newAgent.name = this.defaultData.name;
      this.newAgent.fallback = this.defaultData.fallback * 100;
      if (this.defaultData.config.pipeline === 'supervised_embeddings') {
        this.newAgent.configType = 'supervised_embeddings';
        this.newAgent.language = this.defaultData.config.language;
      } else {
        this.newAgent.configType = 'specific_pipeline';
        this.newAgent.pipeline = JSON.stringify(this.defaultData.config, null, 2);
        this.hideSpecificPipeline = false;
      }
      this.loading = false;
    }
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
      if (this.editorOption === 'create_new_agent') {
        this.newAgent = {
          ...this.newAgent,
          name: '',
          language: 'en',
          configType: 'supervised_embeddings',
          pipeline: JSON.stringify(pipelineExample, null, 2),
          fallback: 40,
          trainingData: JSON.stringify(trainingDataExample, null, 2),
          responses: JSON.stringify(responsesExample, null, 2),
        };
      } else if (this.editorOption === 'import_agent') {
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
          this.fileContent = JSON.parse(e.target ? e.target.result as string : '');
          if (!this.checkIfValidJsonFormat(this.fileContent)) {
            return;
          }
          this.newAgent.configType = Array.isArray((this.fileContent as any).config.pipeline)
            ? 'specific_pipeline' : 'supervised_embeddings';
          this.newAgent.fallback = (this.fileContent as any).fallback * 100;
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
              if (this.editorOption === 'import_agent') {
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
              const response: any = await createAgent(
                this.newAgent.name,
                this.newAgent.configType,
                this.newAgent.language,
                JSON.parse(this.newAgent.pipeline),
                this.newAgent.fallback,
                this.newAgent.trainingData ? JSON.parse(this.newAgent.trainingData) : [],
                this.newAgent.responses ? JSON.parse(this.newAgent.responses) : [],
                this.isEditor,
              );
              this.$notify.success({
                title: 'Success',
                message: response.message,
                offset: 100,
              });
              this.loading = false;
            } catch (error: any) {
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
            if (!this.isEditor) this.$store.commit('addAgent', this.newAgent.name);
            this.$emit('updated');
            this.resetDefaultValue();
            this.cleanUpFile();
            e.preventDefault();
          }
          return false;
        },
      );
    },
    selectConf() {
      if (this.newAgent.configType === 'specific_pipeline') {
        this.hideSpecificPipeline = false;
      } else {
        this.hideSpecificPipeline = true;
      }
    },
  },
});
</script>
<style scoped>
.formItem {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 70%;
}
</style>
