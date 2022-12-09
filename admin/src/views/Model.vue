<template>
  <div class="model tableSize">
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
      <div v-if="textMsg !== ''" :class="classMsg" class="marginBottomMedium">
      {{ textMsg }}
      </div>
      <div style="display: flex; justify-content: center;">
        <el-upload v-if="!isReadUser()" action="" :auto-upload="false" ref="upload" :on-change="handleIntentsFile"
        :on-remove="removeFile" :limit="1" class="upload-demo" style="margin-right: 10px;">
        <el-button type="primary" :disabled="file !== null">
        <el-icon class="el-icon-upload"></el-icon>
        Import intents from file
        </el-button>
        </el-upload>
        <el-button @click="addIntentDialogVisible = true" type="default" style="margin-left: 10px;">
          <el-icon class="el-icon-document-add"></el-icon>
          Create intent
        </el-button>
      </div>
      <el-dialog title="Add intent" :visible.sync="addIntentDialogVisible">
        <el-form :model="addIntentForm" ref="addIntentRef">
          <el-form-item label="Intent name" :label-width="'120px'"
          :rules="{
              required: true, message: 'intent name can not be null', trigger: 'blur'
            }"
          >
            <el-input v-model="addIntentForm.value"></el-input>
          </el-form-item>
          <div v-if="addDialogTextMsg !== ''" :class="addDialogClassMsg" style="margin-bottom: 30px;">
            {{ addDialogTextMsg }}
          </div>
          <el-button type="primary" v-if="addIntentForm.training_data.length === 0"
          @click.prevent="addTrainingData">Add training data</el-button>
          <el-form-item :label-width="'120px'"
            v-for="(td, index) in addIntentForm.training_data"
            :label="'Training data '"
            :key="td.key"
            :prop="'training_data.' + index + '.data'"
            :rules="{
              required: true, message: 'training data can not be null', trigger: 'blur'
            }"
          >
          <el-input style="margin-bottom: 10px;" v-model="td.data"></el-input>
          <el-button type="danger" @click.prevent="removeTrainingDataItem(td)">Delete</el-button>
          <el-button type="primary" @click.prevent="addTrainingData">Add More</el-button>
        </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button type="danger" @click="addIntentDialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="createIntent">Confirm</el-button>
        </span>
      </el-dialog>
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
            type="primary"
            @click="editSelectedIntent(scope.row.intent)"
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
            @click="deleteSelectedIntent(scope.row.intent)"
            icon="el-icon-delete"
            :style="{ marginLeft: '15px' }"
            plain
          ></el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-dialog :visible.sync="dialogIntentVisible" title="Edit intent">
      <div>
        <span style="display: flex; margin-bottom: 10px;">Intent name:</span>
        <el-input v-model="intentNameEdit" autocomplete="off" />
        <div v-if="editDialogTextMsg !== ''" :class="editDialogClassMsg" class="marginTopSmall">
            {{ editDialogTextMsg }}
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogIntentVisible = false">Cancel</el-button>
          <el-button type="primary" @click="updateIntent">
            Edit intent
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import { mapGetters } from 'vuex';
import { GlobalEntity } from '@/types';
import {
  getAgent,
  deleteAgentIntent,
  updateAgentIntent,
  getAgentIntentFile,
  addAgentIntent,
  addAgentIntents,
} from '@/client/agent';
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
      textMsg: '',
      classMsg: '',
      editDialogTextMsg: '',
      editDialogClassMsg: '',
      addDialogTextMsg: '',
      addDialogClassMsg: '',
      file: null,
      fileContent: null,
      dialogIntentVisible: false,
      intentNameEdit: '',
      previousIntentName: '',
      addIntentDialogVisible: false,
      addIntentForm: {
        training_data: Array<any>(),
        value: '',
      },
    };
  },
  computed: {
    allIntents(): Array<string> {
      return this.$store.state.intents;
    },
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
    cleanUpFile() {
      this.file = null;
      this.fileContent = null;
      (this.$refs.upload as any).clearFiles();
    },
    removeFile() {
      this.cleanUpFile();
      this.textMsg = '';
      this.classMsg = '';
    },
    checkIfJSONFile(file: any): boolean {
      return file.name.includes('.json');
    },
    checkIfValidJsonFormat(fileContent: any): boolean {
      if (!(Object.prototype.hasOwnProperty.call(fileContent, 'rasa_nlu_data')
        && Object.prototype.hasOwnProperty.call(fileContent, 'responses'))) {
        return false;
      }
      return true;
    },
    handleIntentsFile(file: any) {
      const newIntents = {
        training_data: Array<unknown>(),
        responses: Array<unknown>(),
      };
      this.file = file;
      this.textMsg = '';
      this.classMsg = '';
      if (!this.checkIfJSONFile(file)) {
        this.textMsg = 'Wrong file format (requires .json file)';
        this.classMsg = 'errorMsg';
        return;
      }
      const reader = new FileReader();
      reader.readAsText(file.raw);
      reader.onload = async (e) => {
        try {
          this.fileContent = JSON.parse(e.target ? e.target.result as string : '');
          if (!this.checkIfValidJsonFormat(this.fileContent)) {
            this.textMsg = 'Invalid json content';
            this.classMsg = 'errorMsg';
            return;
          }
          if (Object.prototype.hasOwnProperty.call((this.fileContent as any).rasa_nlu_data, 'common_examples')) {
            newIntents.training_data = (this.fileContent as any).rasa_nlu_data.common_examples;
          } else {
            newIntents.training_data = [];
          }
          newIntents.responses = (this.fileContent as any).responses;
          this.importIntents(newIntents);
        } catch (err) {
          this.textMsg = 'System Error';
          this.classMsg = 'errorMsg';
        }
      };
    },
    async importIntents(intents: any) {
      try {
        const response = await addAgentIntents(this.agentName, intents);
        this.$notify.success({
          title: 'Success',
          message: response.message,
          offset: 100,
        });
        const intent_set = new Set();
        intents.training_data.forEach((t_data: { [x: string]: unknown }) => {
          intent_set.add(t_data.intent);
        });
        intents.responses.forEach((resp: { [x: string]: unknown }) => {
          intent_set.add(resp.intent);
        });
        intent_set.forEach((intent) => {
          if (!this.allIntents.includes(intent as string)) {
            this.$store.commit('addIntent', intent);
          }
        });
        this.removeFile();
        this.updateModelDetails();
      } catch (error: any) {
        if (error.statusCode === 400) {
          if (error.error.message) {
            this.textMsg = error.error.message;
          }
        } else {
          this.textMsg = 'Server Error, please retry later.';
        }
        this.classMsg = 'errorMsg';
      }
    },
    editSelectedIntent(intent: string) {
      this.previousIntentName = intent;
      this.intentNameEdit = intent;
      this.dialogIntentVisible = true;
    },
    async updateIntent() {
      if (this.previousIntentName === this.intentNameEdit) {
        this.editDialogTextMsg = 'Please change intent name';
        this.editDialogClassMsg = 'errorMsg';
        return;
      }
      if (!this.intentNameEdit) {
        this.editDialogTextMsg = 'Empty value';
        this.editDialogClassMsg = 'errorMsg';
        return;
      }
      const format = /[`!@#$%^&*=[\]{};':"\\|,.<>/?~]/;
      if (format.test(this.intentNameEdit)) {
        this.editDialogTextMsg = 'Text includes forbidden special characters';
        this.editDialogClassMsg = 'errorMsg';
        return;
      }
      try {
        await updateAgentIntent(this.agentName, this.previousIntentName, this.intentNameEdit);
        this.$store.commit('deleteIntent', this.previousIntentName);
        this.$store.commit('addIntent', this.intentNameEdit);
        this.updateModelDetails();
        this.$notify.success({
          title: 'Success',
          message: `Intent ${this.previousIntentName} updated`,
          offset: 100,
        });
      } catch (e) {
        this.$notify.error({
          title: 'Error',
          message: `Error when editing intent ${this.previousIntentName}`,
          offset: 100,
        });
      }
      this.dialogIntentVisible = false;
      this.editDialogTextMsg = '';
      this.editDialogClassMsg = '';
    },
    addTrainingData() {
      this.addIntentForm.training_data.push({
        key: Date.now(),
        data: '',
      });
    },
    removeTrainingDataItem(item: any) {
      const index = this.addIntentForm.training_data.indexOf(item);
      if (index !== -1) {
        this.addIntentForm.training_data.splice(index, 1);
      }
    },
    async createIntent() {
      const { addIntentRef }: any = this.$refs;
      const tdArray = this.addIntentForm.training_data.map((item: any) => item.data);
      if (!this.addIntentForm.value) {
        this.addDialogTextMsg = 'Empty value';
        this.addDialogClassMsg = 'errorMsg';
        return;
      }
      const format = /[`!@#$%^&*=[\]{};':"\\|,.<>/?~]/;
      if (format.test(this.addIntentForm.value)) {
        this.addDialogTextMsg = 'Text includes forbidden special characters';
        this.addDialogClassMsg = 'errorMsg';
        return;
      }
      this.addDialogTextMsg = '';
      this.addDialogClassMsg = '';
      addIntentRef.validate(
        async (valid: any) => {
          if (valid) {
            const body = {
              intent: this.addIntentForm.value,
              training_data: tdArray,
            };
            await addAgentIntent(body, this.agentName)
              .then(() => {
                this.$message({
                  type: 'success',
                  message: 'Synonyms created successfully',
                });
                this.addIntentDialogVisible = false;
                this.$store.commit('addIntent', this.addIntentForm.value);
                this.updateModelDetails();
                this.addIntentForm = {
                  training_data: Array<any>(),
                  value: '',
                };
              })
              .catch(() => {
                this.$message.error('server error, please retry later !');
              });
          }
        },
      );
    },
  },
  mounted() {
    this.updateModelDetails();
  },
});
</script>
