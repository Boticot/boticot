<template>
  <el-dialog title="Change Password" :close-on-click-modal="false" :visible.sync="showChangePasswordForm">
      <el-form :model="changePasswordModel" :rules="rules" ref="changePasswordModel" label-width="120px">
        <el-form-item label="User Login" prop="login">
          <el-input :disabled="true" placeholder="Enter Login" v-model="changePasswordModel.login"></el-input>
        </el-form-item>
        <el-form-item label="New Password" prop="password">
          <el-input type="password" v-model="changePasswordModel.password" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="Confirm" prop="checkPassword">
          <el-input type="password" v-model="changePasswordModel.checkPassword" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancelChangePassword">Cancel</el-button>
        <el-button type="primary" @click="confirmChangePassword">Confirm</el-button>
      </span>
    </el-dialog>
</template>

<script lang="ts">
import { resetPassword } from '@/client/auth';
import Vue from 'vue';

export default Vue.extend({
  name: 'confirmAccount',
  data() {
    const validatePassword = (rule: any, value: any, callback: any) => {
      if (value === '') {
        callback(new Error('Please input the password'));
      } else {
        if (this.$data.changePasswordModel.checkPassword !== '') {
          (this.$refs.changePasswordModel as any).validateField('checkPassword');
        }
        callback();
      }
    };
    const validatePassConfirmation = (rule: any, value: any, callback: any) => {
      if (value === '') {
        callback(new Error('Please input the password again'));
      } else if (value !== this.$data.changePasswordModel.password) {
        callback(new Error('The two passwords  don\'t match!'));
      } else {
        callback();
      }
    };
    return {
      showChangePasswordForm: true,
      changePasswordModel: {
        login: this.$store.getters.login() ? this.$store.getters.login() : null,
        password: '',
        checkPassword: '',
      },
      rules: {
        password: [
          {
            validator: validatePassword, trigger: 'null',
          },
          {
            required: true,
            pattern: /(?=.*\d)(?=.*[a-z])(?=.*[A-Z])/,
            message: 'Please input Valid Password.',
            trigger: 'blur',
          },
          {
            min: 8, message: 'Length should be at least 8', trigger: 'blur',
          },
        ],
        checkPassword: [
          { validator: validatePassConfirmation, trigger: 'null' },
        ],
      },
    };
  },
  methods: {
    confirmChangePassword() {
      const { changePasswordModel }: any = this.$refs;
      changePasswordModel.validate(
        (valid: any) => {
          if (valid) {
            resetPassword(this.changePasswordModel.login,
              this.changePasswordModel.password).then(() => {
              this.$message({
                type: 'success',
                message: 'Password reset successfully',
              });
              this.showChangePasswordForm = false;
              this.$router.replace('/');
            })
              .catch(() => {
                this.$message.error('server error, please retry later !');
              });
          }
        },
      );
    },
    cancelChangePassword() {
      this.showChangePasswordForm = false;
      this.$router.replace('login');
    },
  },
});
</script>

<style scoped>

</style>
