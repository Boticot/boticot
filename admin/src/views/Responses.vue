<template>
  <div class="responses tableSize">
    <el-card class="box-card textAlignLeft">
      <h4 class="textAlignCenter">Agent Responses</h4>
      <el-form :model="newResponse" :rules="rules" ref="newResponse" label-width="120px">
        <el-form-item label="Intent" prop='selectedIntent'>
          <el-select v-model="newResponse.selectedIntent" filterable placeholder="Select Intent" @change="selectIntent">
            <el-option v-for="choice in allIntents" :key="choice" :label="choice" :value="choice"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Response type">
          <el-radio-group v-model="newResponse.type">
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
        <div v-if="showTextForm" key="text">
          <el-form-item label="Text Response" prop='text'>
            <el-input type="textarea" :rows="4" v-model="newResponse.text"></el-input>
          </el-form-item>
        </div>
        <div v-show="showRichTextForm" key="richtext">
          <el-form-item label="Rich Text Response" prop='richText'>
            <vue-editor
            v-model="newResponse.richText"
            :editorOptions="editorSettings"
            ref="quillEditor"
            class="mb-2"
            >
            </vue-editor>
          </el-form-item>
        </div>
        <el-dialog :visible.sync="dialogImageVisible" title="Select image(s)">
          <div>
            <span>Paste URL :</span>
            <el-input v-model="imageURL" autocomplete="off" />
          </div>
          <div class="marginTopSmall">
            <span>Upload images :</span>
          <el-upload
            :file-list="imageList"
            class="textAlignCenter"
            drag
            action=""
            multiple
            list-type="picture"
            :auto-upload="false"
            :on-change="importImageData"
            :on-remove="removeImageData"
          >
            <el-icon class="el-icon-upload"></el-icon>
            <div class="el-upload__text">
              Drop file here or <em>click to upload</em>
            </div>
          </el-upload>
          </div>
          <template #footer>
            <span class="dialog-footer">
              <el-button @click="dialogImageVisible = false">Cancel</el-button>
              <el-button type="primary" @click="handleImages">
                Add image(s)
              </el-button>
            </span>
          </template>
        </el-dialog>
        <div v-if="showSuggestionForm" key="suggestion">
          <el-form-item label="Suggestion Text" prop='suggestionText'>
            <el-input v-model="newResponse.suggestionText"></el-input>
          </el-form-item>
          <el-form-item label="Linked to">
            <el-select v-model="newResponse.suggestionLinkedTo" @change="selectSuggestionLinkedTo">
              <el-option v-for="choice in suggestionsLinkedToList" :key="choice.value" :label="choice.label"
               :value="choice.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item  v-if="showSuggestionCodeForm" label="Code" prop='suggestionCode'>
            <el-input v-model="newResponse.suggestionCode"></el-input>
          </el-form-item>
          <el-form-item v-if="showSuggestionIntentForm" label="Intent" prop='suggestionIntent'>
            <el-select v-model="newResponse.suggestionIntent" filterable placeholder="Select an intent">
              <el-option v-for="choice in allIntents" :key="choice" :label="choice" :value="choice"></el-option>
              <el-option label="Create New Intent" value="NEW_INTENT"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item v-if="showSuggestionNewIntentForm" label="New intent"
          prop='suggestionNewIntent'>
            <el-input v-model="newResponse.suggestionNewIntent"></el-input>
          </el-form-item>
        </div>
        <div v-if="showLinkForm" key="link">
          <el-form-item label="Link name" prop='linkName'>
            <el-input v-model="newResponse.linkName"></el-input>
          </el-form-item>
          <el-form-item label="URL" prop='url'>
            <el-input v-model="newResponse.url"></el-input>
          </el-form-item>
        </div>
        <div v-if="showImageForm" key="image">
          <el-form-item label="Image name" prop='imageName'>
            <el-input v-model="newResponse.imageName"></el-input>
          </el-form-item>
          <el-form-item label="URL" prop='imageUrl'>
            <el-input v-model="newResponse.imageUrl"></el-input>
          </el-form-item>
        </div>
        <el-form-item>
          <el-button type="primary" @click="addResponse">Add Response</el-button>
        </el-form-item>
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
              icon="el-icon-view"
              :disabled="selectedIntentInTree._id === '0' ||
              selectedIntentInTree.suggestion_intent === newResponse.selectedIntent"
              @click="selectIntent(selectedIntentInTree.suggestion_intent)"
              :style="{ marginLeft: '15px' }"
              plain
              >View suggestion
            </el-button>
            <el-button
              type="danger"
              icon="el-icon-delete"
              :disabled="selectedIntentInTree._id === '0' ||
              selectedIntentInTree.suggestion_intent === newResponse.selectedIntent"
              @click="deleteResponseById(selectedIntentInTree._id)"
              :style="{ marginLeft: '15px' }"
              plain
              >Delete suggestion
            </el-button>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import { VueEditor, Quill } from 'vue2-editor';
import { ImageDrop } from 'quill-image-drop-module';
import ImageResize from 'quill-image-resize-vue';
import Emoji from 'quill-emoji';
import SuggestionsTree from '@/components/SuggestionsTree.vue';
import 'quill-emoji/dist/quill-emoji.css';
import {
  getResponses,
  addResponse,
  deleteResponse,
} from '../client/responses';

const QuillImage = Quill.import('formats/image');
QuillImage.sanitize = (url: any) => url;
Quill.register('modules/imageDrop', ImageDrop);
Quill.register('modules/imageResize', ImageResize);
Quill.register({
  'formats/emoji': Emoji.EmojiBlot,
  'modules/short_name_emoji': Emoji.ShortNameEmoji,
  'modules/toolbar_emoji': Emoji.ToolbarEmoji,
  'modules/textarea_emoji': Emoji.TextAreaEmoji,
}, true);

export default Vue.extend({
  name: 'responses',
  components: {
    VueEditor,
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
      suggestionsLinkedToList: [
        {
          value: 'NONE',
          label: 'None',
        },
        {
          value: 'CODE',
          label: 'Code',
        },
        {
          value: 'INTENT',
          label: 'Intent',
        },
      ],
      responses: {
        texts: Array<any>(),
        rich_texts: Array<any>(),
        suggestions: Array<any>(),
        links: Array<any>(),
        images: Array<any>(),
      },
      editorSettings: {
        modules: {
          imageDrop: true,
          imageResize: {},
          'emoji-toolbar': true,
          'emoji-textarea': false,
          'emoji-shortname': true,
          toolbar: {
            container: [
              [{ size: [] }],
              ['bold', 'italic', 'underline'],
              [{ list: 'ordered' }, { list: 'bullet' }],
              ['image', 'link'],
              [{ align: '' }, { align: 'center' }, { align: 'right' }, { align: 'justify' }],
              ['emoji'],
            ],
          },
        },
      },
      quill: null,
      htmlPaste: '',
      advanced: false,
      dialogImageVisible: false,
      imageURL: null,
      savedRichTextIndex: 0,
      imageList: [],
      imagesBlobURL: Array<any>(),
      richTextPreviewVisible: false,
      selectedRichTextId: '',
      activeName: 'texts',
      tableTabs: [
        { name: 'texts', label: 'Texts' },
        { name: 'rich_texts', label: 'Rich Texts' },
        { name: 'suggestions', label: 'Suggestions' },
        { name: 'images', label: 'Images' },
        { name: 'links', label: 'Links' },
      ],
      tableTree: {
        texts: [{ prop: 'fulfillment_text', label: 'Text' }],
        rich_texts: [{ prop: 'rich_text', label: 'Rich Text' }],
        suggestions: [
          { prop: 'suggestion_text', label: 'Suggestion' },
          { prop: 'linked_to', label: 'Linked To' },
          { prop: 'suggestion_code', label: 'Code' },
          { prop: 'suggestion_intent', label: 'Intent' },
        ],
        links: [
          { prop: 'link_name', label: 'Link name' },
          { prop: 'url', label: 'URL' },
        ],
        images: [
          { prop: 'image_name', label: 'Image name' },
          { prop: 'image_url', label: 'Image URL (gif, jpg, png)' },
          { prop: 'image_preview', label: 'Preview' },
        ],
      },
      selectedIntentInTree: { _id: '0', suggestion_intent: '' },
      intentTreeKey: 0,
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
      return this.newResponse.suggestionLinkedTo !== 'CODE';
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
  mounted() {
    const { quillEditor }: any = this.$refs;
    const toolbar = quillEditor.quill.getModule('toolbar');
    toolbar.addHandler('image', this.showImageDialog);
  },
  methods: {
    clearForm() {
      this.newResponse = {
        selectedIntent: this.newResponse ? this.newResponse.selectedIntent : '',
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
      };
      this.intentTreeKey += 1;
    },
    async selectIntent(value: string) {
      this.newResponse.selectedIntent = value;
      this.responses = await getResponses(this.agentName, value);
      this.intentTreeKey += 1;
    },
    async addResponse(e: any) {
      const { newResponse }: any = this.$refs;
      newResponse.validate(
        async (valid: any) => {
          if (valid) {
            if (this.newResponse.type === 'TEXT') {
              const responsesBody = {
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
              await addResponse(this.agentName, responsesBody);
            } else if (this.newResponse.type === 'RICHTEXT') {
              const responsesBody = {
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
              await addResponse(this.agentName, responsesBody);
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
              const responsesBody = {
                responses: [
                  {
                    intent: this.newResponse.selectedIntent,
                    response_type: this.newResponse.type,
                    data,
                  },
                ],
              };
              await addResponse(this.agentName, responsesBody);
            } else if (this.newResponse.type === 'LINK') {
              const responsesBody = {
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
              await addResponse(this.agentName, responsesBody);
            } else if (this.newResponse.type === 'IMAGE') {
              const responsesBody = {
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
              await addResponse(this.agentName, responsesBody);
            }

            this.clearForm();

            this.responses = await getResponses(this.agentName, this.newResponse.selectedIntent);
            e.preventDefault();
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
    selectSuggestionLinkedTo() {
      if (this.newResponse.suggestionLinkedTo === 'INTENT') {
        this.newResponse.suggestionIntent = '';
      }
    },
    parseHtml() {
      const { quillEditor }: any = this.$refs;
      quillEditor.quill.clipboard.dangerouslyPasteHTML(0, this.htmlPaste);
      this.htmlPaste = '';
    },
    async handleImages() {
      const { quillEditor }: any = this.$refs;
      const promises = [];
      for (let i = 0; i < this.imagesBlobURL.length; i += 1) {
        promises.push(fetch(this.imagesBlobURL[i]).then((r) => r.blob()));
      }
      const blobs = await Promise.all(promises);
      for (let i = 0; i < blobs.length; i += 1) {
        const reader = new FileReader();
        reader.readAsDataURL(blobs[i]);
        reader.onloadend = () => {
          const base64data = reader.result;
          quillEditor.quill.insertEmbed(this.savedRichTextIndex, 'image', base64data, Quill.sources.USER);
        };
      }
      if (this.imageURL) {
        quillEditor.quill.insertEmbed(this.savedRichTextIndex, 'image', this.imageURL, Quill.sources.USER);
      }
      this.imageURL = null;
      this.imageList = [];
      this.imagesBlobURL = Array<any>();
      this.dialogImageVisible = false;
    },
    importImageData(file: any) {
      this.imagesBlobURL.push(file.url);
    },
    removeImageData(file: any) {
      const index = this.imagesBlobURL.indexOf(file.url);
      if (index !== -1) {
        this.imagesBlobURL.splice(index, 1);
      }
    },
    showImageDialog() {
      const { quillEditor }: any = this.$refs;
      const range = quillEditor.quill.getSelection();
      this.savedRichTextIndex = range.index;
      this.dialogImageVisible = true;
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
  },
});
</script>
