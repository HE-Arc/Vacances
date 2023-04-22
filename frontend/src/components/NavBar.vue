<script setup></script>

<template>
  <q-header reveal elevated class="bg-grey-10 text-white" height-hint="98">
    <q-toolbar>
      <q-toolbar-title>Vacances ?</q-toolbar-title>
    </q-toolbar>

    <q-tabs align="left">
      <q-route-tab :to="{ name: 'home' }">
        <q-icon name="cottage" />
        Accueil
      </q-route-tab>
      <q-route-tab :to="{ name: 'pokemons' }">
        <q-icon name="auto_stories" />
        Pokédex
      </q-route-tab>
      <q-route-tab :to="{ name: 'users' }">
        Se connecter
      </q-route-tab>
      <q-route-tab :to="{ name: 'users.logout' }">
        Se déconnecter
      </q-route-tab>
      <q-route-tab :to="{ name: 'daycare' }">
        <q-icon name="grass" />
        Pension
      </q-route-tab>
      <q-route-tab :to="{ name: 'shop' }">
        <q-icon name="storefront" />
        Magasin
      </q-route-tab>
    </q-tabs>
  </q-header>
</template>

<style scoped></style>
