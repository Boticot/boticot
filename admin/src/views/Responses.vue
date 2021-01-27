<template>
  <div class="responses halfSize">
    <el-card class="box-card textAlignLeft">
      <h4 class="textAlignCenter">Agent Responses</h4>
      <el-form label-width="120px">
        <el-form-item label="Intent">
          <el-select v-model="selectedIntent" placeholder="Select Intent" @change="selectIntent">
            <el-option v-for="choice in allIntents" :key="choice" :label="choice" :value="choice"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="New Response">
          <el-input type="textarea" :rows="4" v-model="newResponse"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addResponse">Add Response</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <el-card class="box-card" :class="[isHideExistingResponses ? 'displayNone' : '']">
      <h4>Intent "{{selectedIntent}}" Responses</h4>
      <el-table :data="responses" row-key="_id" style="width: 100%">
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
    </el-card>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import { getResponses, addResponse, deleteResponse } from '@/client/responses';

export default Vue.extend({
  name: 'responses',
  data() {
    return {
      agentName: this.$route.params.agentName,
      newResponse: '',
      selectedIntent: '',
      responses: Array<any>(),
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
      this.selectedIntent = value;
      this.responses = await getResponses(this.agentName, value);
      if (this.responses.length === 0) {
        this.isHideExistingResponses = true;
      } else {
        this.isHideExistingResponses = false;
      }
    },
    async addResponse() {
      const responsesBody = {
        responses: [
          {
            intent: this.selectedIntent,
            fulfillment_text: this.newResponse,
          },
        ],
      };
      await addResponse(this.agentName, responsesBody);
      this.isHideExistingResponses = false;
      this.responses = await getResponses(this.agentName, this.selectedIntent);
      this.newResponse = '';
    },
    async deleteResponseById(id: string) {
      await deleteResponse(id);
      this.responses = this.responses.filter((e: any) => (e._id !== id));
      if (this.responses.length === 0) {
        this.isHideExistingResponses = true;
      }
    },
  },
});
</script>
