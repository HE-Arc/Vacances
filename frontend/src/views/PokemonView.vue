<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

const pokemons = ref([]);

const fetchPokemons = async () => {
  const result = await axios.get(
    import.meta.env.VITE_DATABASE_SERVER_NAME + "/api/pokemons/"
  );
  pokemons.value = result.data;
};

const pokemonTypes = ref([]);

const fetchPokemonTypes = async () => {
  pokemonTypes.value = (
    await axios.get(
      import.meta.env.VITE_DATABASE_SERVER_NAME + "/api/pokemon-types/"
    )
  ).data;
};

const removePokemon = async (id) => {
  await axios.delete(
    import.meta.env.VITE_DATABASE_SERVER_NAME + `/api/pokemons/${id}/`
  );
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
      <q-btn color="green" :to="{ name: 'pokemons.create' }">
        <q-icon left size="xl" name="add_circle_outline" />
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
        </q-card-section>

        <q-separator inset />
      </q-card>
    </div>
  </q-page>
</template>

<style scoped></style>
