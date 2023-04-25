<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import interval from "../views/DaycareView.vue";

const user = ref(null);
const isLogged = ref(false);

const fetchConnected = async () => {
  user.value = (await axios.get("users/current/")).data;
  isLogged.value = user.value !== null;

  if (isLogged.value) { // It is good to manage this "session item" here ?, should not be in top level (like App.vue) ?
    sessionStorage.setItem("isAuth", true); // TODO A token will be better
  }
  else {
    sessionStorage.removeItem("isAuth");
  }
  console.log("logged = " + isLogged.value);
  console.log(user.value);
};

onMounted(() => {
  fetchConnected();
});
</script>

<template>
  <q-header reveal elevated class="bg-grey-10 text-white" height-hint="98">
    <q-toolbar>
      <q-toolbar-title>Vacances ?</q-toolbar-title>

      <q-separator vertical />

      <div v-if="isLogged" class="q-ml-auto">
        <q-toolbar-title>{{ user.username }}</q-toolbar-title>
      </div>
    </q-toolbar>

    <q-tabs align="left">
      <q-route-tab :to="{ name: 'home' }"
      @click="clearInterval(interval)">
        <q-icon name="cottage" />
        Accueil
      </q-route-tab>
      <q-route-tab v-if="isLogged" :to="{ name: 'pokemons' }"
      @click="clearInterval(interval)">
        <q-icon name="auto_stories" />
        Pokédex
      </q-route-tab>
      <q-route-tab v-if="isLogged" :to="{ name: 'daycare' }"
      @click="clearInterval(interval)">
        <q-icon name="grass" />
        Pension
      </q-route-tab>
      <q-route-tab v-if="isLogged" :to="{ name: 'shop' }"
      @click="clearInterval(interval)">
        <q-icon name="storefront" />
        Magasin
      </q-route-tab>

      <q-route-tab v-if="isLogged" :to="{ name: 'users.logout' }"
      @click="clearInterval(interval)">
        <q-icon name="logout" />
        Deconnexion
      </q-route-tab>

      <q-route-tab v-if="!isLogged" :to="{ name: 'users' }"
      @click="clearInterval(interval)">
        <q-icon name="login" />
        Connexion
      </q-route-tab>
    </q-tabs>

    <q-space />
  </q-header>
</template>

<style scoped></style>
