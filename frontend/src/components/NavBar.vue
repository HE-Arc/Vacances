<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

const user = ref(null);
const isLogged = ref(false);

// OnMounted we check if we are still connected
const fetchConnected = async () => {
  await axios
    .get("users/current/")
    .then((response) => {
      user.value = response.data;
      isLogged.value = true;
      sessionStorage.setItem("isAuth", true); // TODO A token will be better
    })
    .catch(() => {
      user.value = null;
      isLogged.value = false;
      sessionStorage.removeItem("isAuth");
    });
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
