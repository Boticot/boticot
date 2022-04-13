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
          <el-radio-group v-model="newResponse.type" @change="selectResponseType">
            <el-radio label="TEXT">
              Text
            </el-radio>
            <el-radio label="SUGGESTION">
              Suggestion
            </el-radio>
            <el-radio label="LINK">
              Link
            </el-radio>
          </el-radio-group>
        </el-form-item>
        <div :class="[isHideTextResponse ? 'displayNone' : '']">
          <el-form-item label="Text Response" prop='text'>
            <el-input type="textarea" :rows="4" v-model="newResponse.text"></el-input>
          </el-form-item>
        </div>
        <div :class="[isHideSuggestionsResponse ? 'displayNone' : '']">
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
          <el-form-item label="Code" prop='suggestionCode'
          :class="[isHideSuggestionCode ? 'displayNone' : '']">
            <el-input v-model="newResponse.suggestionCode"></el-input>
          </el-form-item>
          <el-form-item label="Intent" prop='suggestionIntent'
          :class="[isHideSuggestionIntent ? 'displayNone' : '']">
            <el-select v-model="newResponse.suggestionIntent" filterable placeholder="Select an intent"
            @change="selectSuggestionIntent">
              <el-option v-for="choice in allIntents" :key="choice" :label="choice" :value="choice"></el-option>
              <el-option label="Create New Intent" value="NEW_INTENT"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item :class="[isHideSuggestionNewIntent ? 'displayNone' : '']" label="New intent"
          prop='suggestionNewIntent'>
            <el-input v-model="newResponse.suggestionNewIntent"></el-input>
          </el-form-item>
        </div>
        <div :class="[isHideLinkResponse ? 'displayNone' : '']">
          <el-form-item label="Link name" prop='linkName'>
            <el-input v-model="newResponse.linkName"></el-input>
          </el-form-item>
          <el-form-item label="URL" prop='url'>
            <el-input v-model="newResponse.url"></el-input>
          </el-form-item>
        </div>
        <el-form-item>
          <el-button type="primary" @click="addResponse">Add Response</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <el-card class="box-card" :class="[isHideExistingResponses ? 'displayNone' : '']">
      <h4>Intent "{{newResponse.selectedIntent}}" Responses</h4>
      <el-table :data="responses.texts" row-key="_id" max-height="250" style="width: 100%"
      :class="[responses.texts.length == 0 ? 'displayNone' : '']" header-cell-class-name="header-row">
        <el-table-column prop="fulfillment_text" label="Text" width="750"></el-table-column>
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
        <el-table-column prop="suggestion_text" label="Suggestion" width="200"></el-table-column>
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
        <el-table-column prop="link_name" label="Link name" width="250"></el-table-column>
        <el-table-column prop="url" label="URL" width="500"></el-table-column>
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
import { getResponses, addResponse, deleteResponse } from '@/client/responses';

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
      },
      agentName: this.$route.params.agentName,
      isHideTextResponse: false,
      isHideSuggestionsResponse: true,
      isHideLinkResponse: true,
      isHideSuggestionCode: true,
      isHideSuggestionIntent: true,
      isHideSuggestionNewIntent: true,
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
      },
      isHideExistingResponses: true,
    };
  },
  computed: {
    allIntents() {
      return this.$store.state.intents;
    },
  },
  methods: {
    async selectIntent(value: string) {
      this.newResponse.selectedIntent = value;
      this.responses = await getResponses(this.agentName, value);
      if (this.responses.texts.length === 0 && this.responses.suggestions.length === 0
      && this.responses.links.length === 0) {
        this.isHideExistingResponses = true;
      } else {
        this.isHideExistingResponses = false;
      }
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
            }
            this.newResponse.text = '';
            this.newResponse.suggestionText = '';
            this.newResponse.suggestionCode = '';
            this.newResponse.suggestionIntent = '';
            this.newResponse.suggestionNewIntent = '';
            this.newResponse.linkName = '';
            this.newResponse.url = '';
            this.isHideExistingResponses = false;
            this.isHideSuggestionNewIntent = true;
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
      if (this.responses.texts.length === 0 && this.responses.suggestions.length === 0
      && this.responses.links.length === 0) {
        this.isHideExistingResponses = true;
      } else {
        this.isHideExistingResponses = false;
      }
    },
    selectResponseType() {
      if (this.newResponse.type === 'TEXT') {
        this.isHideTextResponse = false;
        this.isHideSuggestionsResponse = true;
        this.isHideLinkResponse = true;
      } else if (this.newResponse.type === 'SUGGESTION') {
        this.isHideTextResponse = true;
        this.isHideSuggestionsResponse = false;
        this.isHideLinkResponse = true;
      } else if (this.newResponse.type === 'LINK') {
        this.isHideTextResponse = true;
        this.isHideSuggestionsResponse = true;
        this.isHideLinkResponse = false;
      }
    },
    selectSuggestionLinkedTo() {
      if (this.newResponse.suggestionLinkedTo === 'CODE') {
        this.isHideSuggestionCode = false;
        this.isHideSuggestionIntent = true;
        this.isHideSuggestionNewIntent = true;
      } else if ((this.newResponse.suggestionLinkedTo === 'INTENT')) {
        this.newResponse.suggestionIntent = '';
        this.isHideSuggestionCode = true;
        this.isHideSuggestionIntent = false;
        this.isHideSuggestionNewIntent = true;
      } else {
        this.isHideSuggestionCode = true;
        this.isHideSuggestionIntent = true;
        this.isHideSuggestionNewIntent = true;
      }
    },
    selectSuggestionIntent(value: string) {
      if (value === 'NEW_INTENT') {
        this.isHideSuggestionNewIntent = false;
      } else {
        this.isHideSuggestionNewIntent = true;
      }
    },
  },
});
</script>
