import { createApp } from 'vue'
import App from './App.vue'
import "vue-data-ui/style.css"  // Vue Data UI styles
import { VueUiRadar } from "vue-data-ui"

const app = createApp(App)

app.component("VueUiRadar", VueUiRadar)

app.mount('#app')