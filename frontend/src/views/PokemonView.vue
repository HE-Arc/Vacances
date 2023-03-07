<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

const pokemons = ref([]);

let success;
let queryString = window.location.search;
let urlParams = new URLSearchParams(queryString);
if (urlParams.has("success")) {
  success = urlParams.get('success');
}



const fetchPokemons = async () => {
  const result = await axios.get(
    import.meta.env.VITE_DATABASE_SERVER_NAME + "/api/pokemons/"
  );
  pokemons.value = result.data;
};

const pokemonTypes = ref([]);

const fetchPokemonTypes = async () => {
  pokemonTypes.value = (
    await axios.get(import.meta.env.VITE_DATABASE_SERVER_NAME + "/api/pokemon-types/")
  ).data;
};

const removePokemon = async (id) => {
  await axios.delete(import.meta.env.VITE_DATABASE_SERVER_NAME + `/api/pokemons/${id}/`);
  await fetchPokemons();
};

onMounted(() => {
  fetchPokemons();
  fetchPokemonTypes();
});
</script>

<template>
  <q-page>
    <h1>Pokédex</h1>
    
    <div class="text-center q-mb-md q-mt-md">
      <q-btn color="green" :to="{ name: 'pokemons.create' }">
        <q-icon left size="xl" name="add_circle_outline" />
        <div>Créer un Pokémon</div>
      </q-btn>
    </div>
    
    <!-- Card list -->
    <q-banner v-if="success" inline-actions class="q-mb-lg text-white bg-green">
      <div class="text-h6">
        <q-icon left size="md" name="mdi-check-circle-outline" />
        Pokémon créé avec succès!
      </div>
    </q-banner>

    <div class="" v-for="(item, index) in pokemons" :key="index">
      <q-card class="my-card q-mb-sm">
        <div class="flex justify-between">
          <q-card-section class="flex-auto">
            <div class="text-h4">{{ item.name }}</div>
            <div class="text-subtitle2">{{ item.pokemon_type_object.name }}</div>
          </q-card-section>

          <div class="flex" style="height:3em">
            <q-btn
              color="red"
              push
              @click="removePokemon(item.id)"
              class="q-ma-xs"
              dense
            >
              <div>
                <q-icon left size="xs" name="delete_outline" />
                Supprimer
              </div>
            </q-btn>
          </div>
        </div>

        <q-separator inset />
      </q-card>
    </div>
  </q-page>
</template>

<style scoped></style>
