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
    await axios.get(import.meta.env.VITE_DATABASE_SERVER_NAME + "/api/pokemon-types/")
  ).data;
};

onMounted(() => {
  fetchPokemons();
  fetchPokemonTypes();
});
</script>

<template>
  <q-page>
    <h1>La pension</h1>
    <br>

    <div class="row">
      <div class="col-xs-12 col-sm-12 col-md-9 col-lg-9">
        <img src="../assets/images/1.jpg" style="outline: solid;width: 40%;" alt="Plage" />
      </div>

      <div class="col-xs-12 col-sm-12 col-md-3 col-lg-3">

        <div class="container" style="outline: solid; outline-offset: 1em;"> 
          <h5>Mes Pokémon</h5>
          <br>
          <!-- Card list -->
          <div class="" v-for="(item, index) in pokemons" :key="index">
            <q-card class="q-mb-sm">
              <div class="flex justify-between">
                <q-card-section class="flex-end">
                  <div class="text-h4">{{ item.name }}</div>
                </q-card-section>
              </div>
              <q-separator inset />
            </q-card>
          </div>
        </div>
        <br>
        <div class="text-center q-mb-md q-mt-md">
          <q-btn color="green" :to="{ TODO }">
            <q-icon left size="xl" name="add_circle_outline" />
            <div>Acheter un Pokémon</div>
          </q-btn>
        </div>

      </div>
    </div>

  </q-page>
</template>

<style scoped></style>
