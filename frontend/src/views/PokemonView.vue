<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

const pokemons = ref([]);

const fetchPokemons = async () => {
  const result = await axios.get("http://localhost:8000/api/pokemons/");
  pokemons.value = result.data;
};

const pokemonTypes = ref([]);

const fetchPokemonTypes = async () => {
  pokemonTypes.value = (
    await axios.get("http://localhost:8000/api/pokemon-types/")
  ).data;
};

const removePokemon = async (id) => {
  await axios.delete(`http://127.0.0.1:8000/api/pokemons/${id}/`);
  await fetchPokemons();
};

// Execute le code quand le composant démarre
onMounted(() => {
  fetchPokemons();
  fetchPokemonTypes();
});
</script>

<template>
  <q-page>
    <div>Liste des Pokémon</div>
    <div class="">
      <q-btn color="primary" :to="{ name: 'pokemons.create' }">
        <q-icon left size="xl" name="mdi-plus-box" />
        <div>Créer un Pokémon</div>
      </q-btn>
    </div>
    <div class="" v-for="(item, index) in pokemons" :key="index">
      <q-card class="my-card">
        <q-card-section>
          <div class="text-h4">{{ item.name }}</div>
          <div class="text-subtitle2">
            {{ item.pokemon_type_object.name }}
          </div>
          <q-btn
            color="warning"
            push
            @click="removePokemon(item.id)"
            class="q-ma-xs"
            dense
          >
            <div>Supprimer</div>
          </q-btn>
        </q-card-section>

        <q-separator inset />
      </q-card>
    </div>
  </q-page>
</template>

<style scoped></style>
