<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
    <div class="container">
      <router-link to="/" class="navbar-brand">DATACOSE BOOKSHOP</router-link>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav"
        aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <router-link to="/authors" class="nav-link">Authors</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/books" class="nav-link">Books</router-link>
          </li>
          <li class="nav-item">
            <button class="btn btn-light" @click="logout">Logout</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  methods: {
    logout() {
      // Remove the access token from the local storage
      localStorage.removeItem('accessToken');
      
      // Redirect the user to the login page
      this.$router.push('/login');
    }
  }
};
</script>

