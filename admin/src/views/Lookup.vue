<template>
  <div class="synonyms halfSize" v-loading="loading">
    <el-card class="box-card">
      <el-button type="primary"
        class="textAlignCenter"
        @click="openAddLookupDialog()">
        Add Lookup
      </el-button>
      <el-collapse style="margin-top: 10%" accordion>
        <el-collapse-item
          v-for="lookupItem in lookupsData"
          :key="lookupItem._id"
          :title="lookupItem.lookups.name"
          style="{height: 70px; max-height: 120px; overflow-y: auto;}">
          <el-row v-if="!isReadUser()" type="flex" style="margin-bottom: 2%" justify="center">
            <el-button type="danger" plain @click="deleteLookup(lookupItem.lookups.name)">
              Delete
            </el-button>
          </el-row>
          <el-row v-for="element in lookupItem.lookups.elements" :key="element.index">
             <el-col>
               <el-tag size="medium" style="margin-left: 5px; margin-bottom: 5px; width=90px">
                {{element}}
                </el-tag>
              </el-col>
             <el-col></el-col>
          </el-row>
        </el-collapse-item>
      </el-collapse>
    </el-card>
  </div>
</template>

<script lang='ts'>
import { LookupsData, LookupsItemData } from '@/types';
import { getLookups, deleteLookups } from '@/client/lookups';
import Vue from 'vue';
import { mapGetters } from 'vuex';

export default Vue.extend({
  name: 'lookup',
  data() {
    return {
      agentName: this.$route.params.agentName,
      loading: true,
      isHideExistingLookups: false,
      lookupsData: null as unknown as LookupsItemData[],
    };
  },
  methods: {
    openAddLookupDialog() {
      // test
    },
    loadSynonyms() {
      getLookups(this.agentName)
        .then((val: LookupsData) => {
          this.loading = false;
          this.lookupsData = val.items;
          if (this.lookupsData.length === 0) {
            this.isHideExistingLookups = true;
          }
        })
        .catch(() => {
          this.isHideExistingLookups = true;
        });
    },
    deleteLookup(lookupName: string) {
      this.loading = true;
      deleteLookups(this.agentName, lookupName)
        .then(() => {
          this.loadSynonyms();
          this.loading = false;
        });
    },
  },
  computed: {
    ...mapGetters({
      allEntities: 'entitiesNames',
      isReadUser: 'isReadUser',
    }),
  },
  mounted() {
    this.loadSynonyms();
  },
});
</script>
