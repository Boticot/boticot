<template>
  <div :id="data.type + data.id" :class="[isHideElement ? 'displayNone' : '']">
    <el-card class="box-card">
      <el-row>
        <div @mouseup="mouseUp">
          <span
            v-for="splitText in data.splitTexts"
            :id="splitText.start"
            :key="splitText.text+splitText.start"
            :style="{ float: 'none', display: 'inline', fontSize: '18px' }"
          >
            <span v-text="' '"></span>
            <span
              :style="{ backgroundColor: getColor(splitText.entity) }"
            >{{ splitText.text }}</span>
          </span>
        </div>
      </el-row>
      <el-row
        type="flex"
        :class="[!isAddEntity ? 'displayNone' : '', 'marginTopSmall']"
        align="middle"
      >
        <el-col :span="8" class="textAlignRight marginRightSmall">
          Entity for
          <b>"{{ selectedEntityText }}"</b>
        </el-col>
        <el-col :span="8" v-if="!isAddNewEntity">
          <el-select v-model="newEntityValue" placeholder="Select Entity" @change="selectNewEntity">
            <el-option v-for="choice in allEntities" :key="choice" :label="choice" :value="choice"></el-option>
            <el-option label="Create New Entity" value="NEW_ENTITY"></el-option>
          </el-select>
        </el-col>
        <el-col :span="8" v-else>
          <el-input placeholder="New Entity Value" v-model="newEntity"></el-input>
        </el-col>
        <el-col :span="8" :pull="1" :class="['textAlignLeft','marginLeftMedium']">
          <el-button type="success" icon="el-icon-check" @click="addEntity()" plain></el-button>
          <el-button type="danger" icon="el-icon-close" @click="closeAddEntity()" plain></el-button>
        </el-col>
      </el-row>
      <el-collapse-item
        :title="'intent: ' + intentText(data.intent.name, data.intent.confidence)"
        :name="this.data.id"
      >
        <el-row>
          <el-col v-if="!isAddNewIntent">
            <el-select v-model="newIntentValue" placeholder="Select Intent" @change="selectNewIntent">
              <el-option v-for="choice in allIntents" :key="choice" :label="choice" :value="choice"></el-option>
              <el-option label="Create New Intent" value="NEW_INTENT"></el-option>
            </el-select>
          </el-col>
          <el-col v-else>
            <el-input
              placeholder="New Intent Value"
              v-model="newIntentValue"
              style="width: 50%; margin: auto;"
            ></el-input>
          </el-col>
        </el-row>
        <el-row class="marginTopSmall">
          <div v-for="entity in data.entities" :key="entity.value+entity.start" class="marginTopSmall">
            <el-row :gutter="0" type="flex" justify="start" class>
              <el-col :span="10" class="marginRightSmall textAlignRight">
                <el-button
                  :style="{
                      float: 'none',
                      display: 'inline',
                      fontWeight: 'bold',
                      backgroundColor: getColor(entity.entity),
                    }"
                  round
                >{{ entity.entity }}</el-button>
              </el-col>
              <el-col :style="{ textAlign: 'left', fontSize: '16px' }">
                {{ entity.value }}
                <span v-if="entity.confidence">({{ entity.confidence }}%)</span>
                <el-button
                  type="danger"
                  @click="deleteEntity(entity.start)"
                  icon="el-icon-delete"
                  :style="{ marginLeft: '15px' }"
                  plain
                ></el-button>
              </el-col>
            </el-row>
          </div>
        </el-row>
        <el-row v-if="data.type === 'TryIt' && data.fulfillmentText" class="marginTopSmall">
          Fulfillment text: <b>{{ data.fulfillmentText }}</b>
        </el-row>
        <el-row type="flex" class="marginTopMedium" justify="end">
          <el-button v-if="['TrainingData', 'Inputs'].includes(data.type)" type="danger" plain @click="remove()">
            Delete
          </el-button>
          <el-button type="primary" plain @click="validate()">Validate</el-button>
        </el-row>
      </el-collapse-item>
    </el-card>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { convertToNluData } from '@/service/nluService';
import { deleteElement, updateElement } from '@/service/agentService';
import { NluParseResult } from '../types';
import '../assets/css/global.css';

const NluEntryComponent = Vue.extend({
  name: 'NluEntryComponent',
  props: {
    data: {
      type: Object,
      default() {
        return {};
      },
    },
    agentName: {
      type: String,
      default() {
        return '';
      },
    },
  },
  data() {
    return {
      selectedEntity: Object(),
      selectedEntityText: '',
      newEntityValue: '',
      isAddEntity: false,
      isAddNewEntity: false,
      newEntity: '',
      newIntentValue: this.data.intent.name,
      isAddNewIntent: false,
      isHideElement: false,
    };
  },
  watch: {
    data() {
      this.isAddEntity = false;
      this.isAddNewEntity = false;
      this.isAddNewIntent = false;
      this.newIntentValue = this.data.intent.name;
    },
  },
  computed: {
    allIntents() {
      return this.$store.state.intents;
    },
    allEntities() {
      return this.$store.getters.entitiesNames();
    },
  },
  methods: {
    intentText(intent: string, confidence?: number): string {
      if (confidence) {
        return `${intent} (${confidence}%)`;
      }
      return intent;
    },
    getColor(entity: string): string {
      return this.$store.getters.entityColor(entity);
    },
    selectNewEntity(val: string): void {
      if (val === 'NEW_ENTITY') {
        this.isAddNewEntity = true;
      } else {
        this.selectedEntity.entity = val;
      }
    },
    selectNewIntent(val: string): void {
      if (val === 'NEW_INTENT') {
        this.newIntentValue = '';
        this.isAddNewIntent = true;
      } else {
        this.newIntentValue = val;
      }
    },
    deleteEntity(start: number): void {
      this.isAddEntity = false;
      this.data.entities = this.data.entities.filter(
        (e: any) => e.start !== start,
      );
      this.updateNluData();
    },
    updateNluData() {
      const nluParse: NluParseResult = {
        id: this.data.id,
        text: this.data.text,
        intent: this.data.intent,
        entities: this.data.entities,
      };
      const result = convertToNluData(nluParse, this.data.type);
      this.data.splitTexts = result.splitTexts;
      this.data.entities = result.entities;
    },
    addEntity(): void {
      if (this.isAddNewEntity) {
        this.selectedEntity.entity = this.newEntity;
        this.$store.commit('addEntity', this.newEntity);
      }
      if (this.selectedEntity.entity) {
        this.data.entities.push({ ...this.selectedEntity });
        this.updateNluData();
      }
      // Reset elements
      this.newEntityValue = '';
      this.newEntity = '';
      this.isAddNewEntity = false;
      this.isAddEntity = false;
    },
    closeAddEntity(): void {
      this.newEntityValue = '';
      this.newEntity = '';
      this.isAddEntity = false;
      this.isAddNewEntity = false;
    },
    mouseUp(): void {
      if (document.getSelection() !== undefined) {
        this.newEntityValue = '';
        this.newEntity = '';
        this.isAddNewEntity = false;
        const defaultStart = +(window!.getSelection()!.anchorNode!.parentNode!.parentNode! as any).id;
        const selectedText: Selection = document.getSelection()!;
        let start: number = defaultStart;
        let end: number = defaultStart;
        if (selectedText.anchorOffset <= selectedText.focusOffset) {
          start += selectedText.anchorOffset;
          end += selectedText.focusOffset;
        } else {
          start += selectedText.focusOffset;
          end += selectedText.anchorOffset;
        }
        const text = `${selectedText}`;
        if (text.startsWith(' ')) {
          start += 1;
        }
        if (text.endsWith(' ')) {
          end -= 1;
        }
        const isNewEntity = this.data.splitTexts.some(
          (elem: any) => elem.entity === undefined && elem.text.includes(text),
        );
        if (isNewEntity) {
          const selection = this.data.text.substring(start, end);
          this.selectedEntity.value = selection;
          this.selectedEntity.start = start;
          this.selectedEntity.end = end;
          this.selectedEntityText = selection;
          if (selection !== '' && selection.trim() !== '') {
            this.$emit('select-new-entity', this.data.id);
            this.isAddEntity = true;
            return;
          }
        }
      }
      this.isAddEntity = false;
    },
    validate(): void {
      if (
        this.newIntentValue
        && this.newIntentValue !== this.data.intent.name
      ) {
        this.data.intent.name = this.newIntentValue;
        this.data.intent.confidence = 0;
        this.data.fulfillmentText = '';
        if (this.isAddNewIntent) {
          this.$store.commit('addIntent', this.newIntentValue);
          this.isAddNewIntent = false;
        }
      }
      updateElement(this.agentName, this.data);
      if (this.data.type === 'Inputs') {
        this.isHideElement = true;
      }
      this.$notify.success({
        title: 'Success',
        message: `Data added: '${this.data.text}'`,
        offset: 100,
      });
    },
    remove(): void {
      deleteElement(this.data.type, this.agentName, this.data.id);
      this.isHideElement = true;
      this.$notify.info({
        title: 'Info',
        message: `Data removed: '${this.data.text}'`,
        offset: 100,
      });
    },
  },
});

export default NluEntryComponent;
</script>

<style>
h3 {
  margin: 40px 0 0;
}
</style>
