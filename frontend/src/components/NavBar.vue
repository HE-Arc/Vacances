<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

const user = ref(null);
const isLogged = ref(false);

const fetchConnected = async () => {
  user.value = (await axios.get("users/current/")).data;
  isLogged.value = user.value !== null;
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
      <q-route-tab :to="{ name: 'home' }">
        <q-icon name="cottage" />
        Accueil
      </q-route-tab>
      <q-route-tab v-if="isLogged" :to="{ name: 'pokemons' }">
        <q-icon name="auto_stories" />
        Pokédex
      </q-route-tab>
      <q-route-tab v-if="isLogged" :to="{ name: 'daycare' }">
        <q-icon name="grass" />
        Pension
      </q-route-tab>
      <q-route-tab v-if="isLogged" :to="{ name: 'shop' }">
        <q-icon name="storefront" />
        Magasin
      </q-route-tab>

      <q-route-tab v-if="isLogged" :to="{ name: 'users.logout' }">
        <q-icon name="logout" />
        Deconnexion
      </q-route-tab>

      <q-route-tab v-if="!isLogged" :to="{ name: 'users' }">
        <q-icon name="login" />
        Connexion
      </q-route-tab>
    </q-tabs>

    <q-space />
  </q-header>
</template>

<style scoped></style>
