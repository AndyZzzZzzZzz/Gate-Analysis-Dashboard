import { createApp } from 'vue'
import App from './App.vue';
import "vue-data-ui/style.css";
import { VueUiRader } from "vue-data-ui";


const app = createApp(App);
app.component("VueUiRader", VueUiRader);

app.mount('#app');
