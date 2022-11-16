<template>
  <div>
    <div v-if="showTextForm" key="text">
      <el-form-item label="Text Response" prop='text'>
        <el-input type="textarea" :rows="4" v-model="responseCopy.text"></el-input>
      </el-form-item>
    </div>
    <div v-show="showRichTextForm" key="richtext">
      <el-form-item label="Rich Text Response" prop='richText'>
        <vue-editor v-model="responseCopy.richText" :editorOptions="editorSettings" ref="quillEditor" class="mb-2">
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
        <el-input v-model="responseCopy.suggestionText"></el-input>
      </el-form-item>
      <el-form-item label="Linked to">
        <div style="display: flex; flex-direction: column; justify-content: start; width:14rem;">
          <el-select v-model="responseCopy.suggestionLinkedTo" @change="selectSuggestionLinkedTo">
            <el-option v-for="choice in suggestionsLinkedToList" :key="choice.value" :label="choice.label"
              :value="choice.value">
            </el-option>
          </el-select>
        </div>
      </el-form-item>
      <el-form-item v-if="showSuggestionCodeForm" label="Code" prop='suggestionCode'>
        <div style="display: flex; flex-direction: column; justify-content: start; width:14rem;">
          <el-input v-model="responseCopy.suggestionCode"></el-input>
        </div>
      </el-form-item>
      <el-form-item v-if="showSuggestionIntentForm" label="Intent" prop='suggestionIntent'>
        <div style="display: flex; flex-direction: column; justify-content: start; width:14rem;">
          <el-select v-model="responseCopy.suggestionIntent" filterable placeholder="Select an intent">
            <el-option v-for="choice in allIntents" :key="choice" :label="choice" :value="choice"></el-option>
            <el-option label="Create New Intent" value="NEW_INTENT"></el-option>
          </el-select>
        </div>
      </el-form-item>
      <el-form-item v-if="showSuggestionNewIntentForm" label="New intent" prop='suggestionNewIntent'>
        <div style="display: flex; flex-direction: column; justify-content: start; width:14rem;">
          <el-input v-model="responseCopy.suggestionNewIntent"></el-input>
        </div>
      </el-form-item>
    </div>
    <div v-if="showLinkForm" key="link">
      <el-form-item label="Link name" prop='linkName'>
        <el-input v-model="responseCopy.linkName"></el-input>
      </el-form-item>
      <el-form-item label="URL" prop='url'>
        <el-input v-model="responseCopy.url"></el-input>
      </el-form-item>
    </div>
    <div v-if="showImageForm" key="image">
      <el-form-item label="Image name" prop='imageName'>
        <el-input v-model="responseCopy.imageName"></el-input>
      </el-form-item>
      <el-form-item label="URL" prop='imageUrl'>
        <el-input v-model="responseCopy.imageUrl"></el-input>
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
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { VueEditor, Quill } from 'vue2-editor';
import { ImageDrop } from 'quill-image-drop-module';
import ImageResize from 'quill-image-resize-vue';
import Emoji from 'quill-emoji';

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
    response: {
      type: Object,
      default() {
        return {};
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
      return this.responseCopy.type === 'TEXT';
    },
    showRichTextForm(): boolean {
      return this.responseCopy.type === 'RICHTEXT';
    },
    showSuggestionForm(): boolean {
      return this.responseCopy.type === 'SUGGESTION';
    },
    showSuggestionIntentForm(): boolean {
      return this.responseCopy.suggestionLinkedTo === 'INTENT';
    },
    showSuggestionCodeForm(): boolean {
      return this.responseCopy.suggestionLinkedTo === 'CODE';
    },
    showSuggestionNewIntentForm(): boolean {
      return this.responseCopy.suggestionIntent === 'NEW_INTENT' && this.responseCopy.suggestionLinkedTo === 'INTENT';
    },
    showLinkForm(): boolean {
      return this.responseCopy.type === 'LINK';
    },
    showImageForm(): boolean {
      return this.responseCopy.type === 'IMAGE';
    },
  },
  data() {
    return {
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
      imageURL: null,
      imageList: [],
      imagesBlobURL: Array<any>(),
      savedRichTextIndex: 0,
      dialogImageVisible: false,
      isEditDialog: false,
      responseCopy: {
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
    this.responseCopy = JSON.parse(JSON.stringify(this.response));
    if (this.editOptions.name !== '') {
      this.isEditDialog = true;
      const objResp = this.responseCopy;
      Object.keys(this.editOptions.obj).forEach((key) => {
        this.responseCopy[key as keyof typeof objResp] = this.editOptions.obj[key];
      });
      this.responseCopy.type = this.editOptions.type;
    }
    const { quillEditor }: any = this.$refs;
    const toolbar = quillEditor.quill.getModule('toolbar');
    toolbar.addHandler('image', this.showImageDialog);
  },
  methods: {
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
      if (this.responseCopy.suggestionLinkedTo === 'INTENT') {
        this.responseCopy.suggestionIntent = '';
      }
    },
    addResponse() {
      this.$emit('add-response', this.responseCopy, this.isEditDialog);
    },
  },
});
</script>
