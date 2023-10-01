<template>
  <Container>
    <div class="login-form">
      <b-card title="Login">
        <b-form @submit.prevent="login">
          <b-form-group label="Username" label-for="username">
            <b-form-input
              id="username"
              v-model="username"
              required
              placeholder="Enter your username"
            ></b-form-input>
          </b-form-group>
          <b-form-group label="Password" label-for="password">
            <b-form-input
              id="password"
              v-model="password"
              type="password"
              required
              placeholder="Enter your password"
            ></b-form-input>
          </b-form-group>
          <b-button type="submit" variant="primary">Login</b-button>
          <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
        </b-form>
      </b-card>
    </div>
  </Container>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator';
import { setAccessToken } from '~/utils/localStorageHelper';

@Component({})
export default class Login extends Vue {
  private username = '';
  private password = '';
  private errorMessage = '';

  async login(): Promise<void> {
    try {
      const encodedData = new URLSearchParams({
        username: this.username,
        password: this.password,
      });
      const response = await this.$axios.post(
        '/auth/login?' + encodedData.toString(),
        encodedData,
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );
      const accessToken = response.data.access_token;
      setAccessToken(accessToken);
      await this.$router.push('/authors');
    } catch (error: any) {
      if (error.response && error.response.status === 401) {
        this.errorMessage = error.response.data.detail;
      } else {
        this.errorMessage = 'An error occurred. Please try again.';
        console.error(error);
      }
    }
  }
}
</script>
