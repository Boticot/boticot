<template>
  <div class="tree">
    <ul>
      <li>
        <div
        class="node"
        @click="selectIntent(baseIntent)"
        :class="{
          'root': isRoot,
          'selected': isSelected(),
          'single-select': selectedIntent._id === baseIntent._id}">
          <div v-if="'suggestion_text' in baseIntent">
            Suggestion: {{ baseIntent.suggestion_text }}
          </div>
          <div v-if="'suggestion_code' in baseIntent">
            Code: {{ baseIntent.suggestion_code }}
          </div>
          <div v-if="'suggestion_intent' in baseIntent">
            Intent: {{ baseIntent.suggestion_intent }}
          </div>
        </div>
        <ul v-if="getIntentSuggestions().length > 0">
          <li v-for="child in getIntentSuggestions()" :key="child._id">
            <SuggestionsTree
            v-if="child"
            :baseIntent="child"
            :agentName="agentName"
            :allSuggestions="suggestions"
            :selectedIntent="selectedIntent"
            :visitedNodes="visitedNodes"
            v-on:select-intent="selectIntent"/>
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>
<script lang="ts">
import Vue from 'vue';
import '../assets/css/global.css';
import {
  getSuggestions,
} from '../client/responses';

export default Vue.extend({
  name: 'SuggestionsTree',
  props: {
    baseIntent: {
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
    allSuggestions: {
      type: Array,
      default() {
        return [];
      },
    },
    isRoot: {
      type: Boolean,
      default() {
        return false;
      },
    },
    selectedIntent: {
      type: Object,
      default() {
        return {};
      },
    },
    visitedNodes: {
      type: Array,
      default() {
        return [];
      },
    },
  },
  data() {
    return {
      suggestions: Array<any>(),
      popoverVisible: false,
      intentSelected: false,
      visitedNodesCopy: Array<any>(),
    };
  },
  async mounted() {
    if (this.allSuggestions.length === 0) {
      this.suggestions = await getSuggestions(this.agentName, this.baseIntent.suggestion_intent);
    } else this.suggestions = this.allSuggestions;
    this.visitedNodes.push(this.baseIntent._id);
    this.visitedNodesCopy = JSON.parse(JSON.stringify(this.visitedNodes));
  },
  methods: {
    getIntentSuggestions() {
      const sugg_list = [];
      for (let i = 0; i < this.suggestions.length; i += 1) {
        if (this.suggestions[i]['intent' as keyof object] === this.baseIntent.suggestion_intent
        && !this.visitedNodesCopy.includes(this.suggestions[i]['_id' as keyof object])) {
          sugg_list.push(this.suggestions[i]);
        }
      }
      return sugg_list;
    },
    selectIntent(intent: any) {
      this.$emit('select-intent', intent);
    },
    isSelected() {
      return (this.selectedIntent.linked_to === 'INTENT'
      && this.selectedIntent.suggestion_intent === this.baseIntent.suggestion_intent)
      || (this.selectedIntent.linked_to === 'CODE'
      && this.selectedIntent.suggestion_code === this.baseIntent.suggestion_code)
      || this.selectedIntent._id === this.baseIntent._id;
    },
  },
});
</script>

<style>
.tree .root {
  border: 1px solid #eaeaea !important;
  -webkit-box-shadow:inset 0px 0px 0px 2px lightblue;
  -moz-box-shadow:inset 0px 0px 0px 2px lightblue;
  box-shadow:inset 0px 0px 0px 2px lightblue;
}

.tree .single-select {
  border: 1px solid #eaeaea !important;
  -webkit-box-shadow:inset 0px 0px 0px 2px rgb(255, 191, 72);
  -moz-box-shadow:inset 0px 0px 0px 2px rgb(255, 191, 72);
  box-shadow:inset 0px 0px 0px 2px rgb(255, 191, 72);
}

.tree .selected {
  background-color: #fff5e1 !important;
}

.tree * {
  margin: 0;
  padding: 0;
}

.tree ul {
  padding-top: 20px;
  position: relative;

  transition: all 0.5s;
  -webkit-transition: all 0.5s;
  -moz-transition: all 0.5s;
}

.tree li {
  float: left;
  text-align: center;
  list-style-type: none;
  position: relative;
  padding: 20px 5px 0 5px;

  transition: all 0.5s;
  -webkit-transition: all 0.5s;
  -moz-transition: all 0.5s;
}

.tree li::before,
.tree li::after {
  content: '';
  position: absolute;
  top: 0;
  right: 50%;
  border-top: 1px solid #ccc;
  width: 50%;
  height: 20px;
}

.tree li::after {
  right: auto;
  left: 50%;
  border-left: 1px solid #ccc;
}

.tree li:only-child::after,
.tree li:only-child::before {
  display: none;
}

.tree li:only-child {
  padding-top: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.tree li:first-child::before,
.tree li:last-child::after {
  border: 0 none;
}

.tree li:last-child::before {
  border-right: 1px solid #ccc;
  border-radius: 0 5px 0 0;
  -webkit-border-radius: 0 5px 0 0;
  -moz-border-radius: 0 5px 0 0;
}

.tree li:first-child::after {
  border-radius: 5px 0 0 0;
  -webkit-border-radius: 5px 0 0 0;
  -moz-border-radius: 5px 0 0 0;
}

.tree ul ul::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  border-left: 1px solid #ccc;
  width: 0;
  height: 20px;
}

.tree .node {
  border: 1px solid #ccc;
  padding: 5px 10px;
  text-decoration: none;
  color: #666;
  font-family: arial, verdana, tahoma;
  font-size: 12px;
  display: inline-block;
  line-height: 1.5;

  border-radius: 5px;
  -webkit-border-radius: 5px;
  -moz-border-radius: 5px;

  transition: all 0.5s;
  -webkit-transition: all 0.5s;
  -moz-transition: all 0.5s;
}

.tree .node:hover,
.tree .node:hover+ul li .node {
  background: #e8e8e8;
  color: #000;
  border: 1px solid #94a0b4;
  cursor: pointer;
}
</style>
