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
import { mapGetters } from 'vuex';
import { authenticateUser } from '@/client/auth';
import { getUser, UserType } from '@/client/users';

export default Vue.extend({
  name: 'login',
  data() {
    return {
      login: '',
      password: '',
      error: '',
    };
  },
  computed: {
    ...mapGetters({
      currentLogin: 'login',
    }),
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
        const currentUser: UserType = await getUser(this.currentLogin());
        this.$store.commit('updateRole', currentUser.role);
        if (currentUser.is_first_login) {
          this.$router.replace('/changePassword');
        } else {
          window.location.reload();
        }
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
