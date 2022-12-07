<template>
  <el-form :model="response" :rules="rules" ref="response" label-width="150px" label-position="left">
    <div v-if="showTextForm" key="text">
      <el-form-item label="Text Response" prop='text'>
        <el-input type="textarea" :rows="4" v-model="response.text"></el-input>
      </el-form-item>
    </div>
    <div v-show="showRichTextForm" key="richtext">
      <el-form-item label="Rich Text Response" prop='richText'>
        <vue-editor v-model="response.richText" :editorOptions="editorSettings" ref="quillEditor" class="mb-2">
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
        <el-upload :file-list="imageList" class="textAlignCenter" drag action="" multiple list-type="picture"
          :auto-upload="false" :on-change="importImageData" :on-remove="removeImageData">
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
        <el-input v-model="response.suggestionText"></el-input>
      </el-form-item>
      <el-form-item label="Linked to">
        <div style="display: flex; flex-direction: column; justify-content: start; width:14rem;">
          <el-select v-model="response.suggestionLinkedTo" @change="selectSuggestionLinkedTo">
            <el-option v-for="choice in suggestionsLinkedToList" :key="choice.value" :label="choice.label"
              :value="choice.value">
            </el-option>
          </el-select>
        </div>
      </el-form-item>
      <el-form-item v-if="showSuggestionCodeForm" label="Code" prop='suggestionCode'>
        <div style="display: flex; flex-direction: column; justify-content: start; width:14rem;">
          <el-input v-model="response.suggestionCode"></el-input>
        </div>
      </el-form-item>
      <el-form-item v-if="showSuggestionIntentForm" label="Intent" prop='suggestionIntent'>
        <div style="display: flex; flex-direction: column; justify-content: start; width:40%;">
          <el-tooltip
            class="box-item"
            :content="response.suggestionIntent || 'No intent selected'"
            placement="top-start"
            effect="light"
          >
            <el-select v-model="response.suggestionIntent" filterable placeholder="Select an intent">
              <el-option v-for="choice in allIntents" :key="choice" :label="choice" :value="choice"></el-option>
              <el-option label="Create New Intent" value="NEW_INTENT"></el-option>
            </el-select>
          </el-tooltip>
        </div>
      </el-form-item>
      <el-form-item v-if="showSuggestionNewIntentForm" label="New intent" prop='suggestionNewIntent'>
        <div style="display: flex; flex-direction: column; justify-content: start; width:14rem;">
          <el-input v-model="response.suggestionNewIntent"></el-input>
        </div>
      </el-form-item>
    </div>
    <div v-if="showLinkForm" key="link">
      <el-form-item label="Link name" prop='linkName'>
        <el-input v-model="response.linkName"></el-input>
      </el-form-item>
      <el-form-item label="URL" prop='url'>
        <el-input v-model="response.url"></el-input>
      </el-form-item>
    </div>
    <div v-if="showImageForm" key="image">
      <el-form-item label="Image name" prop='imageName'>
        <el-input v-model="response.imageName"></el-input>
      </el-form-item>
      <el-form-item label="URL" prop='imageUrl'>
        <el-input v-model="response.imageUrl"></el-input>
      </el-form-item>
    </div>
    <el-form-item>
      <div style="display: flex; flex-direction: column; justify-content: start; width:10rem;">
        <el-button type="primary" @click="addResponse">
          <span v-if="isEditDialog">Edit Response</span>
          <span v-else>Add Response</span>
        </el-button>
      </div>
    </el-form-item>
  </el-form>
</template>

<script lang="ts">
import Vue from 'vue';
import { VueEditor, Quill } from 'vue2-editor';
import { ImageDrop } from 'quill-image-drop-module';
import ImageResize from 'quill-image-resize-vue';
import Emoji from 'quill-emoji';
import {
  addResponse,
  editResponse,
} from '../../client/responses';

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
  name: 'ResponseEditor',
  props: {
    intent: {
      type: String,
      default() {
        return '';
      },
    },
    type: {
      type: String,
      default() {
        return '';
      },
    },
    editOptions: {
      type: Object,
      default() {
        return {
          obj: {},
          name: '',
          type: '',
        };
      },
    },
  },
  components: {
    VueEditor,
  },
  computed: {
    allIntents(): boolean {
      return this.$store.state.intents;
    },
    showTextForm(): boolean {
      return this.response.type === 'TEXT';
    },
    showRichTextForm(): boolean {
      return this.response.type === 'RICHTEXT';
    },
    showSuggestionForm(): boolean {
      return this.response.type === 'SUGGESTION';
    },
    showSuggestionIntentForm(): boolean {
      return this.response.suggestionLinkedTo === 'INTENT';
    },
    showSuggestionCodeForm(): boolean {
      return this.response.suggestionLinkedTo === 'CODE';
    },
    showSuggestionNewIntentForm(): boolean {
      return this.response.suggestionIntent === 'NEW_INTENT' && this.response.suggestionLinkedTo === 'INTENT';
    },
    showLinkForm(): boolean {
      return this.response.type === 'LINK';
    },
    showImageForm(): boolean {
      return this.response.type === 'IMAGE';
    },
  },
  data() {
    const validateField = (value: string, type: string, errorMsg: string, callback: any) => {
      const { response }: any = this;
      if (value === '' && response.type === type) {
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
      const { response }: any = this;
      if (value === '' && response.type === 'SUGGESTION' && response.suggestionLinkedTo === 'CODE') {
        callback(new Error('Please input suggestion Code'));
      }
      callback();
    };
    const checkSuggestionIntent = (rule: any, value: string, callback: any) => {
      const { response }: any = this;
      if (value === '' && response.type === 'SUGGESTION' && response.suggestionLinkedTo === 'INTENT') {
        callback(new Error('Please input suggestion Intent'));
      }
      callback();
    };
    const checkSuggestionNewIntent = (rule: any, value: string, callback: any) => {
      const { response }: any = this;
      if (value === '' && response.type === 'SUGGESTION' && response.suggestionLinkedTo === 'INTENT'
      && response.suggestionIntent === 'NEW_INTENT') {
        callback(new Error('Please input new Intent'));
      }
      const format = /[`!@#$%^&*=[\]{};':"\\|,.<>/?~]/;
      if (format.test(value)) {
        callback(new Error('Text includes forbidden special characters'));
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
      editorSettings: {
        modules: {
          imageDrop: true,
          imageResize: {},
          'emoji-toolbar': true,
          'emoji-textarea': false,
          'emoji-shortname': true,
          toolbar: {
            container: [
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
      imageURL: null,
      imageList: [],
      imagesBlobURL: Array<any>(),
      savedRichTextIndex: 0,
      dialogImageVisible: false,
      isEditDialog: false,
      response: {
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
    };
  },
  mounted() {
    this.response.selectedIntent = this.intent;
    this.response.type = this.type;
    if (Object.keys(this.editOptions.obj).length > 0) {
      this.isEditDialog = true;
      const objResp = this.response;
      Object.keys(this.editOptions.obj).forEach((key) => {
        this.response[key as keyof typeof objResp] = this.editOptions.obj[key];
      });
      this.response.type = this.editOptions.type;
    }
    const { quillEditor }: any = this.$refs;
    const toolbar = quillEditor.quill.getModule('toolbar');
    toolbar.addHandler('image', this.showImageDialog);
  },
  methods: {
    clearForm() {
      this.response = {
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
      this.response.selectedIntent = this.intent;
      this.response.type = this.type;
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
    selectSuggestionLinkedTo() {
      if (this.response.suggestionLinkedTo === 'INTENT') {
        this.response.suggestionIntent = '';
      }
    },
    async addResponse() {
      const { response }: any = this.$refs;
      response.validate(
        async (valid: any) => {
          if (valid) {
            let responseBody = {};
            if (this.response.type === 'TEXT') {
              responseBody = {
                responses: [
                  {
                    intent: this.response.selectedIntent,
                    response_type: this.response.type,
                    data: {
                      fulfillment_text: this.response.text,
                    },
                  },
                ],
              };
            } else if (this.response.type === 'RICHTEXT') {
              responseBody = {
                responses: [
                  {
                    intent: this.response.selectedIntent,
                    response_type: this.response.type,
                    data: {
                      rich_text: this.response.richText,
                    },
                  },
                ],
              };
            } else if (this.response.type === 'SUGGESTION') {
              let data = {};
              if (this.response.suggestionLinkedTo === 'NONE') {
                data = {
                  suggestion_text: this.response.suggestionText,
                  linked_to: this.response.suggestionLinkedTo,
                };
              } else if (this.response.suggestionLinkedTo === 'CODE') {
                data = {
                  suggestion_text: this.response.suggestionText,
                  linked_to: this.response.suggestionLinkedTo,
                  suggestion_code: this.response.suggestionCode,
                };
              } else if (this.response.suggestionLinkedTo === 'INTENT') {
                const suggestionIntentValue: string = (this.response.suggestionIntent === 'NEW_INTENT')
                  ? this.response.suggestionNewIntent : this.response.suggestionIntent;
                const isNewIntent: boolean = (this.response.suggestionIntent === 'NEW_INTENT');
                if (isNewIntent) {
                  this.$store.commit('addIntent', suggestionIntentValue);
                }
                data = {
                  suggestion_text: this.response.suggestionText,
                  linked_to: this.response.suggestionLinkedTo,
                  suggestion_intent: suggestionIntentValue,
                };
              }
              responseBody = {
                responses: [
                  {
                    intent: this.response.selectedIntent,
                    response_type: this.response.type,
                    data,
                  },
                ],
              };
            } else if (this.response.type === 'LINK') {
              responseBody = {
                responses: [
                  {
                    intent: this.response.selectedIntent,
                    response_type: this.response.type,
                    data: {
                      link_name: this.response.linkName,
                      url: this.response.url,
                    },
                  },
                ],
              };
            } else if (this.response.type === 'IMAGE') {
              responseBody = {
                responses: [
                  {
                    intent: this.response.selectedIntent,
                    response_type: this.response.type,
                    data: {
                      image_name: this.response.imageName,
                      image_url: this.response.imageUrl,
                    },
                  },
                ],
              };
            }
            if (this.isEditDialog) {
              await editResponse(this.agentName, responseBody, this.response._id);
            } else await addResponse(this.agentName, responseBody);
            const currIntent = this.response.selectedIntent;
            this.clearForm();
            this.response.selectedIntent = currIntent;
            this.$emit('added-response');
          }
          return false;
        },
      );
    },
  },
});
</script>
