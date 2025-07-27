<template>
  <div id="app" class="dark-mode">
    <HeaderSection />
    <main class="main-content">
      <h1>Welcome to My Dashboard</h1>

      <!-- Charts / Components -->


      <VueUiRader />
    </main>
    <FooterSection />
  </div>
</template>

<script>
import HeaderSection from './components/HeaderSection.vue'
import FooterSection from './components/FooterSection.vue'

export default {
  name: 'App',
  components: {
    HeaderSection,
    FooterSection
  }
}
</script>

<style>
.dark-mode {
  background-color: #121212;
  color: #f5f5f5;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1; 
  padding: 20px;
}

h1 {
  text-align: center;
}

/* Removes white spaces around the web browser */
html, body, #app {
  margin: 0;
  padding: 0;
  height: 100%;
}
</style>