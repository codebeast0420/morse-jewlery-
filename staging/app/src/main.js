import { createApp } from 'vue'
//import './style.css'
import App from './App.vue'
//import vue3dLoader from "vue-3d-loader";
import { TroisJSVuePlugin } from 'troisjs';
import * as THREE from "three";
const app = createApp(App);
app.use(TroisJSVuePlugin);
app.mount('#app')
//createApp(App).mount('#app')

