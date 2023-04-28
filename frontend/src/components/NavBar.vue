<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import interval from "../views/DaycareView.vue";
import { useRoute } from "vue-router";

const player = ref(null);
const isLogged = ref(false);

async function disconnect() {
  await axios.get("users/logout/").then(() => {
    player.value = null;
    isLogged.value = false;
    localStorage.removeItem("isAuth");
    localStorage.removeItem("isManager");
    window.location.href = "users?logout=true";
  });
}

// OnMounted we check if we are still connected
const fetchConnected = async () => {
  const route = useRoute();
  if (route.query == "users") {
    return;
  }
  await axios
    .get("players/my-data/")
    .then(async (response) => {
      player.value = response.data;
      isLogged.value = true;

      localStorage.setItem("isAuth", true); // TODO A token will be better
      localStorage.setItem("isManager", player.value.is_manager);
    })
    .catch(() => {
      player.value = null;
      isLogged.value = false;
      localStorage.removeItem("isAuth");
      localStorage.removeItem("isManager");
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
        <q-toolbar-title>
          {{ player.username }}
          <span v-if="player.is_manager">[manager]</span>
        </q-toolbar-title>
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

      <q-route-tab v-if="isLogged" @click="disconnect()">
        <q-icon name="logout" />
        Deconnexion
      </q-route-tab>

      <q-route-tab
        v-if="!isLogged"
        :to="{ name: 'users' }"
      >
        <q-icon name="login" />
        Connexion
      </q-route-tab>
    </q-tabs>

    <q-space />
  </q-header>
</template>

<style scoped></style>
