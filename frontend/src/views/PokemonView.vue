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

let showDelDialog = ref(false);
let removeItem = ref(null);

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
    
    <q-banner v-if="success" inline-actions class="q-mb-lg text-white bg-green">
      <div class="text-h6">
        <q-icon left size="md" name="check_circle" />
        Pokémon créé avec succès !
      </div>
    </q-banner>

    <!-- Card list -->
    <div class="" v-for="(item, index) in pokemons" :key="index">
      <q-card class="q-mb-sm">
        <div class="flex justify-between">
          <q-card-section class="flex-auto">
            <div class="text-h4">{{ item.name }}</div>
            <div class="text-subtitle2">{{ item.pokemon_type_object.name }}</div>
          </q-card-section>

          <div class="flex normal-btn-size">
            <q-btn
              color="red"
              push
              @click="showDelDialog = true; removeItem = item;"
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

    <!-- Delete dialog -->
    <q-dialog v-model="showDelDialog">
      <q-card class="confirm-border">
        <q-card-section>
          <div class="text-h6 text-red">
            <q-icon name="error" size="lg" />
            Confirmation de suppression
          </div>
        </q-card-section>

        <hr>

        <q-card-section>
          <p>Souhaitez-vous réellement supprimer le pokémon <span class="text-teal">{{ removeItem.name }}</span></p>
          <p>Si vous le supprimez, toutes les données associées le seront également.</p>
          <!-- TODO When game implemented : change text to specify the refund the players and remove it -->
          <p class="text-red">
            <q-icon name="crisis_alert" size="sm" />
            Attention, cette action est irréversible.
          </p>
        </q-card-section>

        <hr>
        
        <q-card-actions align="right">
          <q-btn color="blue-grey" v-close-popup>
            <q-icon left size="xs" name="cancel" />
            Annuler
          </q-btn>
          <q-btn color="red" @click="removePokemon(removeItem.id)" v-close-popup>
            <q-icon left size="xs" name="delete_outline" />
            Supprimer
          </q-btn>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<style scoped></style>
