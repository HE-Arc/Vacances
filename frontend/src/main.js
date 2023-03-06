import { createApp } from "vue";
import { Quasar } from "quasar";
import App from "./App.vue";
import router from "./router";

import "./assets/main.css";
import '@quasar/extras/material-icons/material-icons.css'
import 'quasar/src/css/index.sass'

//import "@quasar/extras/mdi-v6/mdi-v6.css";
import "quasar/dist/quasar.css";

const app = createApp(App);

app.use(router);

app.use(router);
app.use(Quasar, {
  plugins: {}, // import Quasar plugins and add here
});

app.mount("#app");
