<template>
  <el-card v-if="hasResponses" class="box-card">
    <h4>Intent <span style="font-style:italic;">"{{ intent }}"</span> Responses</h4>
    <el-tabs v-model="activeTab">
      <el-tab-pane v-for="tab in tableTabs" :label="tab.label" :name="tab.name" :key="tab.label"
      :disabled="getResponsesByKey(tab.name).length === 0">
        <el-table :data="getResponsesByKey(tab.name)" row-key="_id" style="width: 100%"
          v-if="getResponsesByKey(tab.name).length !== 0 && tab.name !== 'suggestions'"
          header-cell-class-name='header-row' :show-header="!['texts', 'rich_texts'].includes(tab.name)">
          <el-table-column v-for="col in getTableTreePropsByKey(tab.name)" :label="col.label" :prop="col.prop"
            :key="col.prop">
            <template slot-scope="scope">
              <div v-if="tab.name === 'rich_texts'">
                <div style="width:35vw; height:14vh; overflow: auto;">
                  <div v-html="scope.row.rich_text"></div>
                </div>
              </div>
              <div v-else-if="tab.name === 'texts'">
                <span style="white-space: pre;">{{ scope.row.fulfillment_text }}</span>
              </div>
              <div v-else-if="tab.name === 'images'">
                <span v-if="col.prop !== 'image_preview'">{{ scope.row[col.prop] }}</span>
                <img v-else :src="scope.row.image_url" style="max-width: 20vw; max-height: 26vh;">
              </div>
              <div v-else-if="tab.name === 'links'">
                <span v-if="col.prop !== 'url'">{{ scope.row[col.prop] }}</span>
                <a v-else target="_blank" rel="noopener noreferrer" :href="scope.row.url">{{ scope.row.url }}</a>
              </div>
              <div v-else>
                <span>{{ scope.row[col.prop] }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column fixed="right" width="200" v-if="tab.name === 'rich_texts'">
            <template slot-scope="scope">
              <el-button type="primary" @click="showRichTextPreview(scope.row._id)" icon="el-icon-view"
                :style="{ marginLeft: '40px' }" plain>
                View content
              </el-button>
              <el-dialog v-if="scope.row._id === selectedRichTextId" :visible.sync="richTextPreviewVisible"
                title="Rich Text content" :modal="false" :lock-scroll="true">
                <div v-html="scope.row.rich_text" style="height:60vh; overflow:auto;"></div>
              </el-dialog>
            </template>
          </el-table-column>
          <el-table-column fixed="right" width="90">
            <template slot-scope="scope">
              <el-button type="primary" @click="editResponse(tab, scope.row)" icon="el-icon-edit"
                :style="{ marginLeft: '15px' }" plain></el-button>
            </template>
          </el-table-column>
          <el-table-column fixed="right" width="90">
            <template slot-scope="scope">
              <el-button type="danger" @click="openDeleteDialog(scope.row._id)" icon="el-icon-delete"
                :style="{ marginLeft: '15px' }" plain></el-button>
            </template>
          </el-table-column>
        </el-table>
        <div v-if="tab.name === 'suggestions'" :style="{
          'white-space': 'nowrap', 'width': '100%', 'overflow-x': 'auto',
          'padding-bottom': '20px'
        }">
          <div v-if="responses['suggestions'].length === 0" style="font-weight: bold;">
            No suggestion available
          </div>
          <SuggestionsTree
          v-else
          :suggestions="responses['suggestions']" :agent-name="agentName"
          :style="{ 'width': 'max-content', 'display': 'flex', 'justify-content': 'center' }"
          :baseIntent="{ 'suggestion_intent': intent, '_id': '', isRoot: true }" :isRoot="true"
          :selectedIntent="selectedIntentInTree" :key="intentTreeKey" v-on:select-intent="selectIntentInTree">
          </SuggestionsTree>
        </div>
        <div v-if="tab.name === 'suggestions'" style="display: flex; justify-content: end; margin-top: 20px;">
          <el-button type="primary" icon="el-icon-edit"
          :disabled="selectedIntentInTree._id === '0' ||
          selectedIntentInTree.isRoot"
            @click="editResponse({ name: 'suggestions', type: 'SUGGESTION' }, selectedIntentInTree)"
            :style="{ marginLeft: '15px' }" plain>
            Edit suggestion
          </el-button>
          <el-button type="primary" icon="el-icon-view"
          :disabled="selectedIntentInTree._id === '0' ||
          selectedIntentInTree.isRoot ||
          !selectedIntentInTree.suggestion_intent"
            @click="selectIntent(selectedIntentInTree.suggestion_intent)" :style="{ marginLeft: '15px' }" plain>
            View intent
          </el-button>
          <el-button type="danger" icon="el-icon-delete"
          :disabled="selectedIntentInTree._id === '0' ||
          selectedIntentInTree.isRoot"
            @click="openDeleteDialog(selectedIntentInTree._id)" :style="{ marginLeft: '15px' }" plain>
            Delete suggestion
          </el-button>
        </div>
      </el-tab-pane>
    </el-tabs>
    <el-dialog
    :visible.sync="editDialogVisible"
    title="Edit response"
    :lock-scroll="true"
    close-on-click-modal
    close-on-press-escape
    width="65%"
    >
      <ResponseEditor
      v-if="editDialogVisible"
      :intent="intent"
      :type="getSelectedType()"
      v-on:added-response="updateResponses"
      :editOptions="editOptions">
      </ResponseEditor>
    </el-dialog>
    <el-dialog :visible.sync="deleteResponseDialogVisible">
      <div style="font-size: 18px;">
        Are you sure you want to delete response ?
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="deleteResponseDialogVisible = false">Cancel</el-button>
          <el-button type="danger" @click="deleteResponseById(responseIdToDelete)">
            Delete response
          </el-button>
        </span>
      </template>
    </el-dialog>
  </el-card>
  <div v-else style="margin-top: 40px;" v-loading="loadingResponses"></div>
</template>
<script lang='ts'>
import Vue from 'vue';
import SuggestionsTree from '@/components/SuggestionsTree.vue';
import ResponseEditor from '@/components/responses/ResponseEditor.vue';
import 'quill-emoji/dist/quill-emoji.css';
import {
  getResponses,
  deleteResponse,
} from '../../client/responses';

export default Vue.extend({
  name: 'ResponsesTable',
  props: {
    intent: {
      type: String,
      default() {
        return '';
      },
    },
    defaultTab: {
      type: String,
      default() {
        return '';
      },
    },
  },
  components: {
    SuggestionsTree,
    ResponseEditor,
  },
  data() {
    return {
      agentName: this.$route.params.agentName,
      responses: {
        texts: Array<any>(),
        rich_texts: Array<any>(),
        suggestions: Array<any>(),
        images: Array<any>(),
        links: Array<any>(),
      },
      selectedIntentInTree: { _id: '0', suggestion_intent: '', isRoot: false },
      intentTreeKey: 0,
      responseEditorKey: 0,
      activeTab: 'texts',
      tableTabs: [
        { name: 'texts', label: 'Texts', type: 'TEXT' },
        { name: 'rich_texts', label: 'Rich Texts', type: 'RICHTEXT' },
        { name: 'suggestions', label: 'Suggestions', type: 'SUGGESTION' },
        { name: 'links', label: 'Links', type: 'LINK' },
        { name: 'images', label: 'Images', type: 'IMAGE' },
      ],
      tabTypeDict: {
        texts: 'TEXT',
        richTexts: 'RICHTEXT',
        suggestions: 'SUGGESTION',
        links: 'LINK',
        images: 'IMAGE',
      },
      tableTree: {
        texts: [{ prop: 'fulfillment_text', label: 'Text', dict_key: 'text' }],
        rich_texts: [{ prop: 'rich_text', label: 'Rich Text', dict_key: 'richText' }],
        suggestions: [
          { prop: 'suggestion_text', label: 'Suggestion', dict_key: 'suggestionText' },
          { prop: 'linked_to', label: 'Linked To', dict_key: 'suggestionLinkedTo' },
          { prop: 'suggestion_code', label: 'Code', dict_key: 'suggestionCode' },
          { prop: 'suggestion_intent', label: 'Intent', dict_key: 'suggestionIntent' },
        ],
        images: [
          { prop: 'image_name', label: 'Image name', dict_key: 'imageName' },
          { prop: 'image_url', label: 'Image URL (gif, jpg, png)', dict_key: 'imageUrl' },
          { prop: 'image_preview', label: 'Preview', dict_key: 'imagePreview' },
        ],
        links: [
          { prop: 'link_name', label: 'Link name', dict_key: 'linkName' },
          { prop: 'url', label: 'URL', dict_key: 'url' },
        ],
      },
      richTextPreviewVisible: false,
      selectedRichTextId: '',
      editOptions: {
        obj: {},
        name: '',
        type: '',
        isEdition: false,
      },
      editDialogVisible: false,
      loadingResponses: false,
      deleteResponseDialogVisible: false,
      responseIdToDelete: '',
    };
  },
  computed: {
    allIntents(): boolean {
      return this.$store.state.intents;
    },
    hasResponses(): boolean {
      return typeof Object.values(this.responses).find((table: any[]) => table.length) !== 'undefined';
    },
  },
  mounted() {
    if (this.intent) this.updateResponses();
    this.activeTab = this.defaultTab;
  },
  methods: {
    async updateResponses() {
      this.loadingResponses = true;
      this.responses = await getResponses(this.agentName, this.intent);
      this.loadingResponses = false;
      this.editDialogVisible = false;
      if (this.activeTab === 'suggestions') {
        this.intentTreeKey += 1;
      }
    },
    async selectIntent(value: string) {
      this.$emit('select-intent', value, 'suggestions');
    },
    async selectResponseType() {
      this.responseEditorKey += 1;
    },
    openDeleteDialog(id: string) {
      this.responseIdToDelete = id;
      this.deleteResponseDialogVisible = true;
    },
    async deleteResponseById(id: string) {
      this.deleteResponseDialogVisible = false;
      await deleteResponse(id);
      this.responses = await getResponses(this.agentName, this.intent);
      this.selectedIntentInTree = { _id: '0', suggestion_intent: '', isRoot: false };
      this.intentTreeKey += 1;
    },
    showRichTextPreview(id: string) {
      this.selectedRichTextId = id;
      this.richTextPreviewVisible = true;
    },
    getResponsesByKey(key: string) {
      return this.responses[key as keyof object];
    },
    getTableTreePropsByKey(key: string) {
      return this.tableTree[key as keyof object];
    },
    selectIntentInTree(intent: any) {
      this.selectedIntentInTree = intent;
    },
    getSelectedType() {
      return this.tabTypeDict[this.activeTab as keyof object];
    },
    editResponse(tab: any, responseObj: any) {
      const formattedObj: any = {};
      // Creating fields for edition
      Object.keys(responseObj).forEach((key) => {
        // Getting relevant fields for selected intent type
        const tabProps: Array<any> = this.tableTree[tab.name as keyof object];
        const filtered = tabProps.filter((table: any) => table.prop === key);
        if (filtered.length > 0) {
          const { dict_key } = filtered[0];
          formattedObj[dict_key] = responseObj[key];
        } else formattedObj[key] = responseObj[key];
      });
      this.editOptions.obj = formattedObj;
      this.editOptions.name = tab.name;
      this.editOptions.type = tab.type;
      this.editDialogVisible = true;
    },
  },
});
</script>
