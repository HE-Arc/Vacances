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

async function fetchPokemonTypeById(id) {
  return (pokemonTypes.value = await axios.get(id).data);
}

// Execute le code quand le composant démarre
onMounted(() => {
  fetchPokemons();
  fetchPokemonTypes();
});
</script>

<template>
  <q-page>
    <div>Liste des Pokémon</div>
    <div class="row">
      <div
        class=""
        v-for="(item, index) in pokemons"
        :key="index"
      >
        <q-card class="my-card">
          <q-card-section>
            <div class="text-h4">{{ item.name }}</div>
            <div class="text-subtitle2">
              {{ fetchPokemonTypeById(item.pokemon_type) }}
            </div>
          </q-card-section>

          <q-separator inset />
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<style scoped></style>
