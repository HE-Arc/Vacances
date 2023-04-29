<script setup>
import axios from "axios";
import { ref } from "vue";
import { useRouter } from "vue-router";

import {isLogged, isManager, playerName} from "@/router/index.js";

const player = ref(null);

const router = useRouter();

async function disconnect() {
  await axios.get("users/logout/").then(() => {
    player.value = null;
    isLogged.value = false;

    localStorage.removeItem("isAuth");
    localStorage.removeItem("isManager");
    localStorage.removeItem("playerName");

    router.push({ name: "users", query: { logout: "true" } });
  });
}
</script>

<template>
  <q-header reveal elevated class="bg-grey-10 text-white" height-hint="98">
    <q-toolbar>
      <q-toolbar-title>Vacances ?</q-toolbar-title>

      <q-separator vertical />

      <div v-if="isLogged" class="q-ml-auto">
        <q-toolbar-title>
          {{ playerName }}
          <span v-if="isManager">[manager]</span>
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

      <q-route-tab v-if="!isLogged" :to="{ name: 'users' }">
        <q-icon name="login" />
        Connexion
      </q-route-tab>
    </q-tabs>

    <q-space />
  </q-header>
</template>

<style scoped></style>
