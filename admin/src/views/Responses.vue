<template>
  <div class="responses tableSize">
    <el-card class="box-card textAlignLeft">
      <h4 class="textAlignCenter">Agent Responses</h4>
      <el-form :model="selection" ref="selection" label-width="150px" label-position="left">
        <el-form-item label="Intent" prop='selectedIntent'>
          <el-select v-model="selection.selectedIntent" filterable placeholder="Select Intent" @change="selectIntent">
            <el-option v-for="choice in allIntents" :key="choice" :label="choice" :value="choice"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Response type">
          <el-radio-group v-model="selection.type" @change="selectResponseType">
            <el-radio label="TEXT">
              Text
            </el-radio>
            <el-radio label="RICHTEXT">
              Rich Text
            </el-radio>
            <el-radio label="SUGGESTION">
              Suggestion
            </el-radio>
            <el-radio label="LINK">
              Link
            </el-radio>
            <el-radio label="IMAGE">
              Image
            </el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <ResponseEditor
      :key="responseEditorKey"
      :intent="selection.selectedIntent"
      :type="selection.type"
      v-on:added-response="updateResponses">
      </ResponseEditor>
    </el-card>
    <ResponsesTable
    :key="responsesTableKey"
    :intent="selection.selectedIntent"
    :defaultTab="defaultResponsesTab"
    v-on:select-intent="selectIntent"
    class="marginTopSmall">
    </ResponsesTable>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import ResponseEditor from '@/components/responses/ResponseEditor.vue';
import ResponsesTable from '@/components/responses/ResponsesTable.vue';

export default Vue.extend({
  name: 'responses',
  components: {
    ResponseEditor,
    ResponsesTable,
  },
  data() {
    return {
      selection: {
        selectedIntent: '',
        type: 'TEXT',
      },
      responsesTableKey: 0,
      responseEditorKey: 0,
      defaultResponsesTab: 'texts',
    };
  },
  computed: {
    allIntents(): boolean {
      return this.$store.state.intents;
    },
  },
  created() {
    this.clearForm();
  },
  methods: {
    clearForm() {
      this.selection = {
        selectedIntent: '',
        type: 'TEXT',
      };
      this.responsesTableKey += 1;
      this.responseEditorKey += 1;
    },
    async selectIntent(value: string, defaultTab = 'texts') {
      this.selection.selectedIntent = value;
      this.defaultResponsesTab = defaultTab;
      this.responseEditorKey += 1;
      this.responsesTableKey += 1;
    },
    async updateResponses(defaultTab = 'texts') {
      this.defaultResponsesTab = defaultTab;
      this.responsesTableKey += 1;
    },
    async selectResponseType() {
      this.responseEditorKey += 1;
    },
  },
});
</script>
