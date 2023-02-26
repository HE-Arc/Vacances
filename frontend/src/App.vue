<script setup>
import NavBar from "./components/NavBar.vue";
</script>

<template>
  <q-layout>
    <!-- navbar -->
    <NavBar />

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>
