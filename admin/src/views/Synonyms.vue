<template>
  <div class="synonyms tableSize">
    <el-card class="box-card">
      <el-button type="primary"
       class="textAlignCenter"
        @click="openAddOrEditSynonymDialog()">
        Add Synonyms
      </el-button>
      <el-table :class="[isHideExistingSynonyms ? 'displayNone' : '']"
        v-if="synonymsData"
        :data="synonymsData.items"
        style="width: 100%"
        >
        <el-table-column prop="synonyms.value" label="Name" width="120"></el-table-column>
        <el-table-column prop="synonyms.synonyms" label="Synonyms" min-width="300">
          <template slot-scope="scope" >
            <div style="{height: 70px; max-height: 120px; overflow-y: auto;}">
              <el-tag size="medium" slot="reference" class="name-wrapper"
                v-for="item in scope.row.synonyms.synonyms"
                :key="item.id"
                style="margin-left: 5px; margin-bottom: 5px; width=90px"
              >
                {{ item }}
              </el-tag>
            </div>
         </template>
        </el-table-column>
        <el-table-column fixed="right" width="150">
          <template slot-scope="scope">
            <el-button
            type="primary"
            @click="openAddOrEditSynonymDialog(scope.row)"
            icon="el-icon-edit"
            plain
          ></el-button>
            <el-button
            type="danger"
            @click="deleteSelectedSynonym(scope.row)"
            icon="el-icon-delete"
            plain
          ></el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="dialogTitle" :visible.sync="dialogaddOrEditSynonymVisible" :close-on-click-modal="false">
      <el-form :model="addOrEditSynonymForm" ref="addOrEditSynonymsRef">
        <el-form-item label="Name" :label-width="'120px'">
          <el-input v-model="addOrEditSynonymForm.value"></el-input>
        </el-form-item>
        <el-form-item :label-width="'120px'"
          v-for="(synonym, index) in addOrEditSynonymForm.synonyms"
          :label="'Synonym '"
          :key="synonym.key"
          :prop="'synonyms.' + index + '.data'"
          :rules="{
            required: true, message: 'synonym can not be null', trigger: 'blur'
          }"
        >
        <el-input v-model="synonym.data"></el-input>
        <el-button @click.prevent="removeSynonymItem(synonym)">Delete</el-button>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="dialogaddOrEditSynonymVisible = false">Cancel</el-button>
      <el-button @click.prevent="addSynonym">Add Synonym</el-button>
      <el-button type="primary" @click="createOrEditSynonyms">Confirm</el-button>
    </span>
  </el-dialog>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import { SynonymsData, SynonymsItemData } from '@/types';
import {
  getSynonyms, addSynonyms, updateSynonyms, deleteSynonyms,
} from '@/client/synonyms';

export default Vue.extend({
  name: 'synonyms',
  data() {
    return {
      agentName: this.$route.params.agentName,
      dialogTitle: '',
      isHideExistingSynonyms: false,
      addOrEditSynonymForm: {
        synonyms: [{
          key: 1,
          data: '',
        }],
        value: '',
      },
      dialogaddOrEditSynonymVisible: false,
      synonymsData: null as unknown as SynonymsData,
      selectedSynonymId: '',
      isCreatingSynonyms: false,
      idOfSynonymsToEdit: '',
    };
  },
  methods: {
    async createOrEditSynonyms() {
      const { addOrEditSynonymsRef }: any = this.$refs;
      const synonymsArray = this.addOrEditSynonymForm.synonyms.map((item: any) => item.data);
      addOrEditSynonymsRef.validate(
        async (valid: any) => {
          if (valid) {
            if (this.isCreatingSynonyms) {
              const body = {
                synonyms: [
                  {
                    value: this.addOrEditSynonymForm.value,
                    synonyms: synonymsArray,
                  },
                ],
              };
              await addSynonyms(body, this.agentName)
                .then(() => {
                  this.$message({
                    type: 'success',
                    message: 'Synonyms created successfully',
                  });
                  this.dialogaddOrEditSynonymVisible = false;
                  this.loadSynonyms();
                  this.isHideExistingSynonyms = false;
                })
                .catch(() => {
                  this.$message.error('server error, please retry later !');
                });
            } else {
              const body = {
                synonyms:
                  {
                    value: this.addOrEditSynonymForm.value,
                    synonyms: synonymsArray,
                  },
              };
              await updateSynonyms(body, this.agentName, this.idOfSynonymsToEdit)
                .then(() => {
                  this.$message({
                    type: 'success',
                    message: 'Synonyms updated successfully',
                  });
                  this.dialogaddOrEditSynonymVisible = false;
                  this.loadSynonyms();
                })
                .catch(() => {
                  this.$message.error('server error, please retry later !');
                });
            }
          }
        },
      );
    },
    addSynonym() {
      this.addOrEditSynonymForm.synonyms.push({
        key: Date.now(),
        data: '',
      });
    },
    removeSynonymItem(item: any) {
      const index = this.addOrEditSynonymForm.synonyms.indexOf(item);
      if (index !== -1) {
        this.addOrEditSynonymForm.synonyms.splice(index, 1);
      }
    },
    openAddOrEditSynonymDialog(synonymItem: SynonymsItemData) {
      this.addOrEditSynonymForm.synonyms = [{
        key: 1,
        data: '',
      }];
      this.addOrEditSynonymForm.value = '';
      this.dialogaddOrEditSynonymVisible = true;
      if (!synonymItem) {
        this.isCreatingSynonyms = true;
        this.dialogTitle = 'Add synonyms';
      } else {
        this.isCreatingSynonyms = false;
        this.idOfSynonymsToEdit = synonymItem._id;
        this.dialogTitle = 'Update synonyms';
        this.addOrEditSynonymForm.value = synonymItem.synonyms.value;
        this.addOrEditSynonymForm.synonyms = synonymItem.synonyms.synonyms.map((currentItem, index) => ({
          key: index,
          data: currentItem,
        }));
      }
    },
    async deleteSelectedSynonym(synonymItem: SynonymsItemData) {
      this.synonymsData.items = this.synonymsData.items
        .filter((i: SynonymsItemData) => (i._id !== synonymItem._id));
      await deleteSynonyms(this.agentName, synonymItem._id)
        .then(() => {
          this.$message({
            type: 'success',
            message: 'Synonyms deleted successfully',
          });
        });
      if (this.synonymsData.items.length === 0) {
        this.isHideExistingSynonyms = false;
      }
    },
    loadSynonyms() {
      getSynonyms(this.agentName)
        .then((val: SynonymsData) => {
          this.synonymsData = val;
          if (this.synonymsData.items.length === 0) {
            this.isHideExistingSynonyms = true;
          }
        })
        .catch(() => {
          this.isHideExistingSynonyms = true;
        });
    },
  },
  mounted() {
    this.loadSynonyms();
  },
});
</script>
