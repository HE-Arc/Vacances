<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import interval from "../views/DaycareView.vue";

const user = ref(null);
const isLogged = ref(false);
const isManager = ref(false);

// OnMounted we check if we are still connected
const fetchConnected = async () => {
  await axios
    .get("users/current/")
    .then(async (response) => {
      user.value = response.data;
      isLogged.value = true;
      sessionStorage.setItem("isAuth", true); // TODO A token will be better

      // Is manager
      await axios.get("players/my_data/").then((response) => {
        isManager.value = response.data.is_manager;
        sessionStorage.setItem("isManager", isManager.value);
      });
    })
    .catch(() => {
      user.value = null;
      isLogged.value = false;
      sessionStorage.removeItem("isAuth");
      sessionStorage.removeItem("isManager");
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
          {{ user.username }}
          <span v-if="isManager">[manager]</span>
        </q-toolbar-title>
      </div>
    </q-toolbar>

    <q-tabs align="left">
      <q-route-tab :to="{ name: 'home' }" @click="clearInterval(interval)">
        <q-icon name="cottage" />
        Accueil
      </q-route-tab>
      <q-route-tab
        v-if="isLogged"
        :to="{ name: 'pokemons' }"
        @click="clearInterval(interval)"
      >
        <q-icon name="auto_stories" />
        Pokédex
      </q-route-tab>
      <q-route-tab
        v-if="isLogged"
        :to="{ name: 'daycare' }"
        @click="clearInterval(interval)"
      >
        <q-icon name="grass" />
        Pension
      </q-route-tab>
      <q-route-tab
        v-if="isLogged"
        :to="{ name: 'shop' }"
        @click="clearInterval(interval)"
      >
        <q-icon name="storefront" />
        Magasin
      </q-route-tab>

      <q-route-tab
        v-if="isLogged"
        :to="{ name: 'users.logout' }"
        @click="clearInterval(interval)"
      >
        <q-icon name="logout" />
        Deconnexion
      </q-route-tab>

      <q-route-tab
        v-if="!isLogged"
        :to="{ name: 'users' }"
        @click="clearInterval(interval)"
      >
        <q-icon name="login" />
        Connexion
      </q-route-tab>
    </q-tabs>

    <q-space />
  </q-header>
</template>

<style scoped></style>
