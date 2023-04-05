<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

const pokemons = ref([]);

let success;
let queryString = window.location.search;
let urlParams = new URLSearchParams(queryString);
if (urlParams.has("success")) {
  success = urlParams.get("success");
}

const fetchPokemons = async () => {
  const result = await axios.get(
    import.meta.env.VITE_DATABASE_SERVER_NAME + "/api/pokemons/unowned_by_user/"
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

const buyPokemon = async (id) => {
  // await axios.delete(import.meta.env.VITE_DATABASE_SERVER_NAME + `/api/pokemons/${id}/`);
  // TODO : buy the pokemon
  // 1) Check if enough money
  // 2) Check if pokemon is not already owned
  // 3) Remove money
  // 4) Add pokemon to owned pokemons
  // 5) Redirect to /shop?success=true
  // note : example of axios post request :
  // await axios.post(import.meta.env.VITE_DATABASE_SERVER_NAME + `/api/pokemons/${id}/buy/`)
  
  await fetchPokemons();
};

let showBuyDialog = ref(false);
let buyItem = ref(null);

onMounted(() => {
  fetchPokemons();
  fetchPokemonTypes();
});
</script>

<template>
  <q-page>
    <h1>Magasin</h1>

    <br>

    <q-banner v-if="success" inline-actions class="q-mb-lg text-white bg-green">
      <div class="text-h6">
        <q-icon left size="md" name="check_circle" />
        Pokémon acheté avec succès !
      </div>
    </q-banner>

    <!-- Card list -->
    <div class="" v-for="(item, index) in pokemons" :key="index">
      <q-card class="q-mb-sm">
        <div class="flex justify-between">
          <q-card-section class="flex-auto">
            <div class="text-h4">{{ item.name }}</div>
            <div class="text-subtitle2">
              {{ item.pokemon_type_object.name }}
            </div>

            <div class="q-mt-md">
              <p><q-icon name="price_change" size="xs" /> Facteur de gain : {{ item.pokemon_type_object.cash_factor }}</p>
              <p><q-icon name="sentiment_very_satisfied" size="xs" /> Bonheur max : {{ item.pokemon_type_object.max_happiness }} </p>
            </div>
          </q-card-section>

          <div class="flex normal-btn-size">
            <q-btn
              color="blue"
              push
              @click="
                showBuyDialog = true;
                buyItem = item;
              "
              class="q-ma-xs"
              dense
            >
              <div>
                <q-icon left size="xs" name="price_check" />
                Acheter<br>
                {{ item.pokemon_type_object.cost }} <q-icon name="currency_ruble" size="xs" />
              </div>
            </q-btn>
          </div>
        </div>

        <q-separator inset />
      </q-card>
    </div>

    <!-- Delete dialog -->
    <q-dialog v-model="showBuyDialog">
      <q-card class="confirm-border-information">
        <q-card-section>
          <div class="text-h6 text-blue">
            <q-icon name="error" size="lg" />
            Confirmation d'achat
          </div>
        </q-card-section>

        <hr />

        <q-card-section>
          <p>
            Souhaitez-vous vraiment acheter
            <span class="text-teal">{{ buyItem.name }}</span> ?
          </p>
          <p>
            Il vous coutera <span class="text-teal">{{ buyItem.pokemon_type_object.cost }} <q-icon name="currency_ruble" size="xs" /></span>.
          </p>
          <p>
            Votre nouveau solde sera de
            <span class="text-teal"
              >§§§ TODO §§§
              <q-icon name="currency_ruble" size="xs" />
            </span>
            .
          </p>
          <!-- TODO When game implemented : change text to specify the refund the players and remove it -->
        </q-card-section>

        <hr />

        <q-card-actions align="right">
          <q-btn color="blue-grey" v-close-popup>
            <q-icon left size="xs" name="cancel" />
            Annuler
          </q-btn>
          <q-btn
            color="blue"
            @click="buyPokemon(removeItem.id)"
            v-close-popup
          >
            <q-icon left size="xs" name="price_check" />
            Acheter
          </q-btn>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<style scoped></style>
