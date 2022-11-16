<template>
  <div class="responses tableSize">
    <el-card class="box-card textAlignLeft">
      <h4 class="textAlignCenter">Agent Responses</h4>
      <el-form :model="newResponse" :rules="rules" ref="newResponse" label-width="150px" label-position="left">
        <el-form-item label="Intent" prop='selectedIntent'>
          <el-select v-model="newResponse.selectedIntent" filterable placeholder="Select Intent" @change="selectIntent">
            <el-option v-for="choice in allIntents" :key="choice" :label="choice" :value="choice"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Response type">
          <el-radio-group v-model="newResponse.type" @change="selectResponseType">
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
        <ResponseEditor
        :response="newResponse"
        :key="responseEditorKey"
        v-on:add-response="addResponse">
        </ResponseEditor>
      </el-form>
    </el-card>
    <el-card v-if="hasResponses" class="box-card">
      <h4>Intent "{{newResponse.selectedIntent}}" Responses</h4>
      <el-tabs v-model="activeName">
        <el-tab-pane v-for="tab in tableTabs" :label="tab.label" :name="tab.name" :key="tab.label">
          <el-table
          :data="getResponsesByKey(tab.name)"
          row-key="_id"
          style="width: 100%"
          v-if="getResponsesByKey(tab.name).length !== 0 && tab.name !== 'suggestions'"
          header-cell-class-name='header-row'
          :show-header="!['texts', 'rich_texts'].includes(tab.name)"
          >
            <el-table-column
            v-for="col in getTableTreePropsByKey(tab.name)"
            :label="col.label"
            :prop="col.prop"
            :key="col.prop"
            >
              <template slot-scope="scope">
                <div v-if="tab.name === 'rich_texts'">
                  <div style="width:35vw; height:14vh; overflow: auto;">
                    <div v-html="scope.row.rich_text"></div>
                  </div>
                </div>
                <div v-else-if="tab.name === 'texts'">
                  <span style="white-space: pre;">{{scope.row.fulfillment_text}}</span>
                </div>
                <div v-else-if="tab.name === 'images'">
                  <span v-if="col.prop !== 'image_preview'">{{scope.row[col.prop]}}</span>
                  <img v-else :src="scope.row.image_url" style="max-width: 20vw; max-height: 26vh;">
                </div>
                <div v-else-if="tab.name === 'links'">
                  <span v-if="col.prop !== 'url'">{{scope.row[col.prop]}}</span>
                  <a v-else target="_blank" rel="noopener noreferrer" :href="scope.row.url">{{scope.row.url}}</a>
                </div>
                <div v-else>
                  <span>{{scope.row[col.prop]}}</span>
                </div>
              </template>
            </el-table-column>
            <el-table-column fixed="right" width="200" v-if="tab.name === 'rich_texts'">
              <template slot-scope="scope">
                <el-button
                type="primary"
                @click="showRichTextPreview(scope.row._id)"
                icon="el-icon-view"
                :style="{ marginLeft: '40px' }"
                plain
                >
                View content
                </el-button>
                <el-dialog
                v-if="scope.row._id === selectedRichTextId"
                :visible.sync="richTextPreviewVisible"
                title="Rich Text content"
                :modal="false"
                :lock-scroll="true"
                >
                <div v-html="scope.row.rich_text" style="height:60vh; overflow:auto;"></div>
                </el-dialog>
              </template>
            </el-table-column>
            <el-table-column fixed="right" width="90">
              <template slot-scope="scope">
                <el-button
                type="primary"
                @click="editResponse(tab, scope.row)"
                icon="el-icon-edit"
                :style="{ marginLeft: '15px' }"
                plain
                ></el-button>
              </template>
            </el-table-column>
            <el-table-column fixed="right" width="90">
              <template slot-scope="scope">
                <el-button
                type="danger"
                @click="deleteResponseById(scope.row._id)"
                icon="el-icon-delete"
                :style="{ marginLeft: '15px' }"
                plain
                ></el-button>
              </template>
            </el-table-column>
          </el-table>
          <div
          v-if="tab.name === 'suggestions'"
          :style="{'white-space': 'nowrap', 'width': '100%', 'overflow-x': 'auto',
          'padding-bottom': '20px'}">
            <SuggestionsTree
            :suggestions="responses['suggestions']"
            :agent-name="agentName"
            :style="{'width': 'max-content', 'display': 'flex', 'justify-content': 'center'}"
            :baseIntent="{'suggestion_intent': newResponse.selectedIntent, '_id': ''}"
            :isRoot="true"
            :selectedIntent="selectedIntentInTree"
            :key="intentTreeKey"
            v-on:select-intent="selectIntentInTree">
            </SuggestionsTree>
          </div>
          <div v-if="tab.name === 'suggestions'" style="display: flex; justify-content: end; margin-top: 20px;">
            <el-button
              type="primary"
              icon="el-icon-edit"
              :disabled="selectedIntentInTree._id === '0' ||
              selectedIntentInTree._id === newResponse._id"
              @click="editResponse({name: 'suggestions', type: 'SUGGESTION'}, selectedIntentInTree)"
              :style="{ marginLeft: '15px' }"
              plain
              >Edit suggestion
            </el-button>
            <el-button
              type="primary"
              icon="el-icon-view"
              :disabled="selectedIntentInTree._id === '0' ||
              selectedIntentInTree._id === newResponse._id"
              @click="selectIntent(selectedIntentInTree.suggestion_intent)"
              :style="{ marginLeft: '15px' }"
              plain
              >View intent
            </el-button>
            <el-button
              type="danger"
              icon="el-icon-delete"
              :disabled="selectedIntentInTree._id === '0' ||
              selectedIntentInTree._id === newResponse._id"
              @click="deleteResponseById(selectedIntentInTree._id)"
              :style="{ marginLeft: '15px' }"
              plain
              >Delete suggestion
            </el-button>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    <el-dialog
    :visible.sync="editDialogVisible"
    title="Edit response"
    :lock-scroll="true"
    close-on-click-modal
    close-on-press-escape
    width="65%"
    >
      <el-form :model="newResponse" :rules="rules" ref="newResponse" label-width="150px" label-position="left">
        <ResponseEditor
        v-if="editDialogVisible"
        :response="newResponse"
        v-on:add-response="addResponse"
        :editOptions="editOptions">
        </ResponseEditor>
      </el-form>
    </el-dialog>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import SuggestionsTree from '@/components/SuggestionsTree.vue';
import ResponseEditor from '@/components/ResponseEditor.vue';
import 'quill-emoji/dist/quill-emoji.css';
import {
  getResponses,
  addResponse,
  editResponse,
  deleteResponse,
} from '../client/responses';

export default Vue.extend({
  name: 'responses',
  components: {
    ResponseEditor,
    SuggestionsTree,
  },
  data() {
    const validateField = (value: string, type: string, errorMsg: string, callback: any) => {
      const { newResponse }: any = this;
      if (value === '' && newResponse.type === type) {
        callback(new Error(errorMsg));
      }
      callback();
    };
    const checkText = (rule: any, value: string, callback: any) => {
      validateField(value, 'TEXT', 'Please input response text', callback);
    };
    const checkRichText = (rule: any, value: string, callback: any) => {
      validateField(value, 'RICHTEXT', 'Please input response text', callback);
    };
    const checkSuggestionText = (rule: any, value: string, callback: any) => {
      validateField(value, 'SUGGESTION', 'Please input suggestion text', callback);
    };
    const checkSuggestionCode = (rule: any, value: string, callback: any) => {
      const { newResponse }: any = this;
      if (value === '' && newResponse.type === 'SUGGESTION' && newResponse.suggestionLinkedTo === 'CODE') {
        callback(new Error('Please input suggestion Code'));
      }
      callback();
    };
    const checkSuggestionIntent = (rule: any, value: string, callback: any) => {
      const { newResponse }: any = this;
      if (value === '' && newResponse.type === 'SUGGESTION' && newResponse.suggestionLinkedTo === 'INTENT') {
        callback(new Error('Please input suggestion Intent'));
      }
      callback();
    };
    const checkSuggestionNewIntent = (rule: any, value: string, callback: any) => {
      const { newResponse }: any = this;
      if (value === '' && newResponse.type === 'SUGGESTION' && newResponse.suggestionLinkedTo === 'INTENT'
      && newResponse.suggestionIntent === 'NEW_INTENT') {
        callback(new Error('Please input new Intent'));
      }
      callback();
    };
    const checkLinkName = (rule: any, value: string, callback: any) => {
      validateField(value, 'LINK', 'Please input link name', callback);
    };
    const checkUrl = (rule: any, value: string, callback: any) => {
      validateField(value, 'LINK', 'Please input url', callback);
    };
    const checkImageName = (rule: any, value: string, callback: any) => {
      validateField(value, 'IMAGE', 'Please input image name', callback);
    };
    const checkImageUrl = (rule: any, value: string, callback: any) => {
      validateField(value, 'IMAGE', 'Please input image (gif, png or jpg)', callback);
    };
    return {
      newResponse: {
        selectedIntent: '',
        type: 'TEXT',
        text: '',
        richText: '',
        suggestionText: '',
        suggestionLinkedTo: 'NONE',
        suggestionCode: '',
        suggestionIntent: '',
        suggestionNewIntent: '',
        linkName: '',
        url: '',
        imageName: '',
        imageUrl: '',
        _id: '',
      },
      rules: {
        selectedIntent: [
          { required: true, message: 'Please select an intent', trigger: 'blur' },
        ],
        text: [
          { required: true, validator: checkText, trigger: 'blur' },
        ],
        richText: [
          { required: true, validator: checkRichText, trigger: 'blur' },
        ],
        suggestionText: [
          { required: true, validator: checkSuggestionText, trigger: 'blur' },
        ],
        suggestionCode: [
          { required: true, validator: checkSuggestionCode, trigger: 'blur' },
        ],
        suggestionIntent: [
          { required: true, validator: checkSuggestionIntent, trigger: 'blur' },
        ],
        suggestionNewIntent: [
          { required: true, validator: checkSuggestionNewIntent, trigger: 'blur' },
        ],
        linkName: [
          { required: true, validator: checkLinkName, trigger: 'blur' },
        ],
        url: [
          { required: true, validator: checkUrl, trigger: 'blur' },
        ],
        imageName: [
          { required: true, validator: checkImageName, trigger: 'blur' },
        ],
        imageUrl: [
          { required: true, validator: checkImageUrl, trigger: 'blur' },
        ],
      },
      agentName: this.$route.params.agentName,
      responses: {
        texts: Array<any>(),
        rich_texts: Array<any>(),
        suggestions: Array<any>(),
        links: Array<any>(),
        images: Array<any>(),
      },
      selectedIntentInTree: { _id: '0', suggestion_intent: '' },
      intentTreeKey: 0,
      responseEditorKey: 0,
      activeName: 'texts',
      tableTabs: [
        { name: 'texts', label: 'Texts', type: 'TEXT' },
        { name: 'rich_texts', label: 'Rich Texts', type: 'RICHTEXT' },
        { name: 'suggestions', label: 'Suggestions', type: 'SUGGESTION' },
        { name: 'images', label: 'Images', type: 'IMAGE' },
        { name: 'links', label: 'Links', type: 'LINK' },
      ],
      tableTree: {
        texts: [{ prop: 'fulfillment_text', label: 'Text', dict_key: 'text' }],
        rich_texts: [{ prop: 'rich_text', label: 'Rich Text', dict_key: 'richText' }],
        suggestions: [
          { prop: 'suggestion_text', label: 'Suggestion', dict_key: 'suggestionText' },
          { prop: 'linked_to', label: 'Linked To', dict_key: 'suggestionLinkedTo' },
          { prop: 'suggestion_code', label: 'Code', dict_key: 'suggestionCode' },
          { prop: 'suggestion_intent', label: 'Intent', dict_key: 'suggestionIntent' },
        ],
        links: [
          { prop: 'link_name', label: 'Link name', dict_key: 'linkName' },
          { prop: 'url', label: 'URL', dict_key: 'url' },
        ],
        images: [
          { prop: 'image_name', label: 'Image name', dict_key: 'imageName' },
          { prop: 'image_url', label: 'Image URL (gif, jpg, png)', dict_key: 'imageUrl' },
          { prop: 'image_preview', label: 'Preview', dict_key: 'imagePreview' },
        ],
      },
      richTextPreviewVisible: false,
      selectedRichTextId: '',
      editDialogVisible: false,
      editOptions: {
        obj: {},
        name: '',
        type: '',
      },
    };
  },
  computed: {
    allIntents(): boolean {
      return this.$store.state.intents;
    },
    showTextForm(): boolean {
      return this.newResponse.type === 'TEXT';
    },
    showRichTextForm(): boolean {
      return this.newResponse.type === 'RICHTEXT';
    },
    showSuggestionForm(): boolean {
      return this.newResponse.type === 'SUGGESTION';
    },
    showSuggestionIntentForm(): boolean {
      return this.newResponse.suggestionLinkedTo === 'INTENT';
    },
    showSuggestionCodeForm(): boolean {
      return this.newResponse.suggestionLinkedTo === 'CODE';
    },
    showSuggestionNewIntentForm(): boolean {
      return this.newResponse.suggestionIntent === 'NEW_INTENT' && this.newResponse.suggestionLinkedTo === 'INTENT';
    },
    showLinkForm(): boolean {
      return this.newResponse.type === 'LINK';
    },
    showImageForm(): boolean {
      return this.newResponse.type === 'IMAGE';
    },
    hasResponses(): boolean {
      return typeof Object.values(this.responses).find((table: any[]) => table.length) !== 'undefined';
    },
  },
  created() {
    this.clearForm();
  },
  methods: {
    clearForm() {
      this.newResponse = {
        selectedIntent: '',
        type: 'TEXT',
        text: '',
        richText: '',
        suggestionText: '',
        suggestionLinkedTo: 'NONE',
        suggestionCode: '',
        suggestionIntent: '',
        suggestionNewIntent: '',
        linkName: '',
        url: '',
        imageName: '',
        imageUrl: '',
        _id: '',
      };
      this.intentTreeKey += 1;
      this.responseEditorKey += 1;
    },
    async selectIntent(value: string) {
      this.newResponse.selectedIntent = value;
      this.responses = await getResponses(this.agentName, value);
      this.intentTreeKey += 1;
      this.responseEditorKey += 1;
    },
    async selectResponseType() {
      this.responseEditorKey += 1;
    },
    async addResponse(copy: any, edit = false) {
      const objResp = this.newResponse;
      Object.keys(copy).forEach((key) => {
        this.newResponse[key as keyof typeof objResp] = copy[key];
      });
      const { newResponse }: any = this.$refs;
      newResponse.validate(
        async (valid: any) => {
          if (valid) {
            let responseBody = {};
            if (this.newResponse.type === 'TEXT') {
              responseBody = {
                responses: [
                  {
                    intent: this.newResponse.selectedIntent,
                    response_type: this.newResponse.type,
                    data: {
                      fulfillment_text: this.newResponse.text,
                    },
                  },
                ],
              };
            } else if (this.newResponse.type === 'RICHTEXT') {
              responseBody = {
                responses: [
                  {
                    intent: this.newResponse.selectedIntent,
                    response_type: this.newResponse.type,
                    data: {
                      rich_text: this.newResponse.richText,
                    },
                  },
                ],
              };
            } else if (this.newResponse.type === 'SUGGESTION') {
              let data = {};
              if (this.newResponse.suggestionLinkedTo === 'NONE') {
                data = {
                  suggestion_text: this.newResponse.suggestionText,
                  linked_to: this.newResponse.suggestionLinkedTo,
                };
              } else if (this.newResponse.suggestionLinkedTo === 'CODE') {
                data = {
                  suggestion_text: this.newResponse.suggestionText,
                  linked_to: this.newResponse.suggestionLinkedTo,
                  suggestion_code: this.newResponse.suggestionCode,
                };
              } else if (this.newResponse.suggestionLinkedTo === 'INTENT') {
                const suggestionIntentValue: string = (this.newResponse.suggestionIntent === 'NEW_INTENT')
                  ? this.newResponse.suggestionNewIntent : this.newResponse.suggestionIntent;
                const isNewIntent: boolean = (this.newResponse.suggestionIntent === 'NEW_INTENT');
                if (isNewIntent) {
                  this.$store.commit('addIntent', suggestionIntentValue);
                }
                data = {
                  suggestion_text: this.newResponse.suggestionText,
                  linked_to: this.newResponse.suggestionLinkedTo,
                  suggestion_intent: suggestionIntentValue,
                };
              }
              responseBody = {
                responses: [
                  {
                    intent: this.newResponse.selectedIntent,
                    response_type: this.newResponse.type,
                    data,
                  },
                ],
              };
            } else if (this.newResponse.type === 'LINK') {
              responseBody = {
                responses: [
                  {
                    intent: this.newResponse.selectedIntent,
                    response_type: this.newResponse.type,
                    data: {
                      link_name: this.newResponse.linkName,
                      url: this.newResponse.url,
                    },
                  },
                ],
              };
            } else if (this.newResponse.type === 'IMAGE') {
              responseBody = {
                responses: [
                  {
                    intent: this.newResponse.selectedIntent,
                    response_type: this.newResponse.type,
                    data: {
                      image_name: this.newResponse.imageName,
                      image_url: this.newResponse.imageUrl,
                    },
                  },
                ],
              };
            }
            if (edit) {
              await editResponse(this.agentName, responseBody, this.newResponse._id);
            } else await addResponse(this.agentName, responseBody);
            const currIntent = this.newResponse.selectedIntent;
            this.clearForm();
            this.newResponse.selectedIntent = currIntent;
            this.responses = await getResponses(this.agentName, this.newResponse.selectedIntent);
            this.editDialogVisible = false;
          }
          return false;
        },
      );
    },
    async deleteResponseById(id: string) {
      await deleteResponse(id);
      this.responses = await getResponses(this.agentName, this.newResponse.selectedIntent);
      this.selectedIntentInTree = { _id: '0', suggestion_intent: '' };
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
    editResponse(tab: any, responseObj: any) {
      const formattedObj: any = {};
      Object.keys(responseObj).forEach((key) => {
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
