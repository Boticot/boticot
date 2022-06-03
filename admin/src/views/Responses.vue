<template>
  <div class="responses halfSize">
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
        <div v-if="showSuggestionForm" key="suggestion">
          <el-form-item label="Suggesion Text" prop='suggestionText'>
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
      <el-table :data="responses.texts" row-key="_id" max-height="250" style="width: 100%"
      :class="[responses.texts.length == 0 ? 'displayNone' : '']" header-cell-class-name="header-row">
        <el-table-column prop="fulfillment_text" label="Text"></el-table-column>
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
      <el-table :data="responses.suggestions" row-key="_id" max-height="250" class="marginTopLarge" style="width: 100%"
      :class="[responses.suggestions.length == 0 ? 'displayNone' : '']" header-cell-class-name="header-row">
        <el-table-column prop="suggestion_text" label="Suggestion"></el-table-column>
        <el-table-column prop="linked_to" label="Linked To" width="150"></el-table-column>
        <el-table-column prop="suggestion_code" label="Code" width="200"></el-table-column>
        <el-table-column prop="suggestion_intent" label="Intent" width="200"></el-table-column>
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
      <el-table :data="responses.links" row-key="_id" max-height="250" class="marginTopLarge" style="width: 100%"
      :class="[responses.links.length == 0 ? 'displayNone' : '']" header-cell-class-name="header-row">
        <el-table-column prop="link_name" label="Link name" width="200"></el-table-column>
        <el-table-column prop="url" label="URL"></el-table-column>
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
      <el-table :data="responses.images" row-key="_id" max-height="250" class="marginTopLarge" style="width: 100%"
      :class="[responses.images.length == 0 ? 'displayNone' : '']" header-cell-class-name="header-row">
        <el-table-column prop="image_name" label="Image name" width="200"></el-table-column>
        <el-table-column prop="image_url" label="URL (gif, jpg, png)"></el-table-column>
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
    </el-card>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import {
  getResponses,
  addResponse,
  deleteResponse,
} from '../client/responses';

export default Vue.extend({
  name: 'responses',
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
      if (!/\.(gif|png|jpg)$/.test(value)) {
        return callback(new Error('Please input a valid image (gif, png or jpg)'));
      }

      return callback();
    };
    return {
      newResponse: {
        selectedIntent: '',
        type: 'TEXT',
        text: '',
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
        suggestions: Array<any>(),
        links: Array<any>(),
        images: Array<any>(),
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
  methods: {
    clearForm() {
      this.newResponse = {
        selectedIntent: this.newResponse?.selectedIntent,
        type: 'TEXT',
        text: '',
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
    },
    async selectIntent(value: string) {
      this.newResponse.selectedIntent = value;
      this.responses = await getResponses(this.agentName, value);
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
    },
    selectSuggestionLinkedTo() {
      if (this.newResponse.suggestionLinkedTo === 'INTENT') {
        this.newResponse.suggestionIntent = '';
      }
    },
  },
});
</script>
