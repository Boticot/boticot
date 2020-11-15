<template>
  <div class="login" style="width: 30%; margin: auto;">
    <form>
      <el-row v-if="error !== ''">
        <span style="color: red;">{{ error }}</span>
      </el-row>
      <el-row>
        <el-input placeholder="Enter your login" v-model="login"></el-input>
      </el-row>
      <el-row>
        <el-input placeholder="Enter your password" v-model="password" show-password></el-input>
      </el-row>
      <el-row>
        <el-button type="primary" @click="loginUser">LOGIN</el-button>
      </el-row>
    </form>
  </div>
</template>

<script lang='ts'>
import Vue from 'vue';
import { authenticateUser } from '@/client/auth';

export default Vue.extend({
  name: 'login',
  data() {
    return {
      login: '',
      password: '',
      error: '',
    };
  },
  methods: {
    async loginUser() {
      this.error = '';
      try {
        const authUser = await authenticateUser({
          email: this.login,
          password: this.password,
        });
        this.$store.commit('updateToken', authUser.access_token);
        this.$router.replace('/');
        window.location.reload();
      } catch (e) {
        if (e.statusCode === 401) {
          if (e.error.message) {
            this.error = e.error.message;
          }
        } else {
          this.error = 'Authentication Server Error, please retry later.';
        }
      }
    },
  },
});
</script>

<style>
.el-row {
  margin-bottom: 20px;
}
</style>
