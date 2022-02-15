<template>
  <div class="users halfSize">
    <el-card class="box-card textAlignLeft">
      <h4>Create new User</h4>
      <el-form :model="newUser" :rules="rules" ref="newUser" label-width="120px">
        <el-form-item label="First Name" prop="first_name">
          <el-input placeholder="Enter First Name" v-model="newUser.first_name"></el-input>
        </el-form-item>
        <el-form-item label="Last Name" prop="last_name">
          <el-input placeholder="Enter Last Name" v-model="newUser.last_name"></el-input>
        </el-form-item>
        <el-form-item label="User Login" prop="email">
          <el-input placeholder="Enter Login" v-model="newUser.email"></el-input>
        </el-form-item>
        <el-form-item label="Password">
          <el-input :disabled="newUser.login === ''" v-model="hiddenPassword" autocomplete="off">
            <el-tooltip slot="suffix" content="Copy" placement="top">
              <i :class="hiddenPasswordClass"
                @click="handleIconClick($event)">
              </i>
            </el-tooltip>
          </el-input>
        </el-form-item>
        <el-form-item label="Right" prop="role">
          <el-radio-group v-model="newUser.role">
            <el-radio :label="'super-admin'">Super Admin</el-radio>
            <el-radio :label="'admin'">Admin</el-radio>
            <el-radio :label="'write'">Write</el-radio>
            <el-radio :label="'read'" >Read</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="!(newUser.role === 'super-admin')" label="Available Agents">
            <el-select v-model="newUser.agents" multiple placeholder="Select here">
            <el-option
              v-for="item in agents"
              :key="item.id"
              :label="item.name"
              :value="item.name">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="createUser">Create User</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="box-card" :class="[isHideExistingUsers ? 'displayNone' : '']">
      <h4>Existing Users</h4>
      <el-table :data="users" style="width: 100%">
        <el-table-column prop="first_name" label="First Name" width="150"></el-table-column>
        <el-table-column prop="last_name" label="Last Name" width="150"></el-table-column>
        <el-table-column prop="email" label="Login" width="150"></el-table-column>
        <el-table-column prop="role" label="Right" width="150">
          <template slot-scope="scope" v-if="scope.row.role">
            <div slot="reference" class="name-wrapper">
              <el-tag size="medium">
                {{ scope.row.role }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="agents" label="Agents" width="150">
          <template slot-scope="scope">
            <div slot="reference" class="name-wrapper"
              v-for="item in scope.row.agents"
              :key="item.id"
              style="margin-bottom: 5%">
                <el-tag size="medium">{{ item }}</el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="firstLogin" label="Change Password" width="150">
          <template slot-scope="scope">
            <div slot="reference" class="name-wrapper">
              <el-tag v-if="scope.row.is_first_login === true"
                type="danger"
                size="medium">
                Required
              </el-tag>
              <el-tag v-if="!scope.row.is_first_login" type="success" size="medium">
                Done
              </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column v-if="!isReadUser()" label="Operations" width="150" fixed="right">
          <template slot-scope="scope">
            <el-button
              size="mini"
              @click="openEdit(scope.$index, scope.row)">Edit</el-button>
            <el-button
              size="mini"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)">Delete</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-if="editUser" title="Edit User" :close-on-click-modal="false" :visible.sync="showEditDialogForm">
      <el-form :model="editUser" :rules="rules">
        <el-form-item label="First Name" prop="first_name">
          <el-input placeholder="Enter First Name" v-model="editUser.first_name"></el-input>
        </el-form-item>
        <el-form-item label="Last Name" prop="last_name">
          <el-input placeholder="Enter Last Name" v-model="editUser.last_name"></el-input>
        </el-form-item>
        <el-form-item label="User Login" prop="email">
          <el-input placeholder="Enter Login" v-model="editUser.email"></el-input>
        </el-form-item>
        <el-form-item label="Right" prop="role">
          <el-radio-group v-model="editUser.role">
            <el-radio :label="'super-admin'">Super Admin</el-radio>
            <el-radio :label="'admin'">Admin</el-radio>
            <el-radio :label="'read'" >Read</el-radio>
            <el-radio :label="'write'">write</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="!(editUser.role === 'super-admin')" label="Available Agents">
            <el-select v-model="editUser.agents" multiple placeholder="Select here">
            <el-option
              v-for="item in agents"
              :key="item.id"
              :label="item.name"
              :value="item.name">
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancelEdit">Cancel</el-button>
        <el-button type="primary" @click="confirmEdit">Confirm</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { getAgents } from '@/client/agent';
import { cloneDeep } from 'lodash';
import {
  createUser, deleteUser, getAllUsers, UserType, updateUser,
} from '@/client/users';
import { mapGetters } from 'vuex';

export default Vue.extend({
  name: 'users',
  data() {
    return {
      hiddenPasswordClass: 'el-input__icon el-icon-document-copy',
      showEditDialogForm: false,
      isHideExistingUsers: false,
      newUser: {
        first_name: '',
        last_name: '',
        email: '',
        role: '',
        agents: [],
      },
      editUser: {
        first_name: '',
        last_name: '',
        email: '',
        role: '',
        agents: [],
      },
      indexOfUserToEdit: null,
      users: Array<any>(),
      rules: {
        first_name: [
          { required: true, message: 'Please input First Name', trigger: 'blur' },
        ],
        last_name: [
          { required: true, message: 'Please input Last Name', trigger: 'blur' },
        ],
        email: [
          { required: true, message: 'Please input User Login', trigger: 'blur' },
          {
            // eslint-disable-next-line max-len
            pattern: /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,
            message: 'Please enter a valid login: email address',
            trigger: 'blur',
          },
        ],
        role: [
          { required: true, message: 'Please choose one Right', trigger: 'blur' },
        ],
      },
      agents: Array<any>(),
      errMsg: '',
    };
  },
  computed: {
    hiddenPassword: { // UpperCase first caracter, then append a random number
      get(): any {
        if (this.newUser.email === '') return null;
        return this.newUser.email.charAt(0).toUpperCase()
          + this.newUser.email.slice(1) + Math.floor(Math.random() * 1000000);
      },
      set(): any {
        if (this.newUser.email === '') return null;
        return this.newUser.email.charAt(0).toUpperCase()
          + this.newUser.email.slice(1) + Math.floor(Math.random() * 1000000);
      },
    },
    ...mapGetters([
      'isReadUser',
    ]),
  },
  methods: {
    async createUser() {
      const { newUser }: any = this.$refs;
      newUser.validate(
        (valid: any) => {
          if (valid) {
            let newUserItem: UserType = { ...this.newUser, password: this.hiddenPassword, is_first_login: true };
            if ((newUserItem as any).role === 'super-admin') {
              newUserItem = { ...newUserItem, agents: [] };
            }
            createUser(newUserItem)
              .then(() => {
                this.users.push(newUserItem);
                this.isHideExistingUsers = false;
                this.$message({
                  type: 'success',
                  message: 'User Creation completed',
                });
              })
              .catch((error) => {
                if (error.response.status === 409) {
                  this.errMsg = error.response.data.message;
                } else {
                  this.errMsg = 'Server Error, please retry later.';
                }
                this.$message.error(this.errMsg);
              });
          }
        },
      );
    },
    handleDelete(index: any, element: any) {
      this.$confirm('This will permanently delete the user. Continue?', 'Warning', {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        type: 'warning',
      }).then(() => {
        deleteUser(element.email).then(() => {
          this.users.splice(index, 1);
          this.$message({
            type: 'success',
            message: 'Delete completed',
          });
          if (this.users.length === 0) this.isHideExistingUsers = true;
        })
          .catch(() => {
            this.$message.error('Cannot delete User, please retry later !');
          });
      }).catch(() => { // in case of cancel delete
        this.$message({
          type: 'info',
          message: 'Delete canceled',
        });
      });
    },
    openEdit(index: any, element: any) {
      this.editUser = cloneDeep(element);
      this.indexOfUserToEdit = index;
      this.showEditDialogForm = true;
    },
    confirmEdit() {
      if (this.editUser.role === 'super-admin') {
        this.editUser = {
          ...this.editUser,
          agents: [],
        };
      }
      updateUser((this.editUser as unknown as UserType))
        .then(() => {
          this.users[(this.indexOfUserToEdit) as any] = cloneDeep(this.editUser);
          this._clearObject(this.editUser);
          this.showEditDialogForm = false;
          this.$message({
            type: 'success',
            message: 'Edit completed',
          });
        })
        .catch(() => {
          this.$message.error('server error while updating !');
        });
    },
    cancelEdit() {
      this._clearObject(this.editUser);
      this.showEditDialogForm = false;
      this.$message({
        type: 'info',
        message: 'Edit canceled',
      });
    },
    async handleIconClick() {
      this.hiddenPasswordClass = 'el-input__icon el-icon-success';
      await navigator.clipboard.writeText(this.hiddenPassword);
      setTimeout(() => {
        this.hiddenPasswordClass = 'el-input__icon el-icon-document-copy';
      }, 3000);
    },
    _clearObject(element: any) {
      Object.keys(element).forEach((index) => {
        element[index] = null;
      });
    },
  },
  mounted() {
    getAgents()
      .then((val: any) => {
        this.agents = val;
      });
    getAllUsers()
      .then((response: any) => { this.users = response.users; });
    if (this.users !== null) {
      this.isHideExistingUsers = false;
    } else {
      this.isHideExistingUsers = true;
    }
  },
});
</script>

<style scoped>

</style>
