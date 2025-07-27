<template>
  <div id="app" class="dark-mode">
    <HeaderSection />
    <main class="main-content">
      <div class="dashboard-grid">
        <DonutGraph />
        <CirclePack />
        <QuadrantGraph />
        <DonutGraph /> 
      </div>
    </main>
    <FooterSection />
  </div>
</template>

<script>
import HeaderSection from './components/HeaderSection.vue'
import FooterSection from './components/FooterSection.vue'
import DonutGraph from './components/DonutGraph.vue'
import QuadrantGraph from './components/QuadrantGraph.vue'
import CirclePack from './components/CirclePack.vue'

export default {
  name: 'App',
  components: {
    HeaderSection,
    FooterSection,
    DonutGraph,
    QuadrantGraph,
    CirclePack
  }
}
</script>

<style>

/* Removes white spaces around the web browser */
html, body, #app {
  margin: 0;
  padding: 0;
  height: 100%;
  background: #121212;
}

.main-content {
  flex: 1; 
  padding: 0px;
  display: flex;
  align-items: stretch;     /* Ensures children (like the grid) stretch */
  justify-content: center;  
}

h1 {
  text-align: center;
}



.dashboard-grid {
  flex: 1;                  /* Grid fills main-content vertically */
  width: 100%;
  max-width: 1200px;        /* Optional, for wide screens */
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 24px;
  min-height: 600px;        /* Ensures grid is always tall enough */
  background: none;         /* No extra background */
}

.dashboard-grid > * {
  all: unset;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>