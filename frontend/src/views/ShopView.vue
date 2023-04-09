<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

const pokemons = ref([]);

let successTitle = ref("abc");
let success = ref(["a", "b", "c"]);
let errorsTitle = ref("def");
let errors = ref(["a", "b", "c"]);

const fetchPokemons = async () => {
  const result = await axios.get("pokemons/unowned_by_user/");
  pokemons.value = result.data;
};

const pokemonTypes = ref([]);

const fetchPokemonTypes = async () => {
  pokemonTypes.value = (await axios.get("pokemon-types/")).data;
};

const playerCash = ref(0);

const fetchPlayerCash = async () => {
  playerCash.value = (await axios.get("players/my_data/")).data.money;
};

const fetchPokemon = async (id) => {
  const result = await axios.get(`pokemons/${id}/`);
  return result.data;
};

const buyPokemon = async (id) => {
  // Clean messages
  success.value = [];
  successTitle.value = "";
  errors.value = [];
  errorsTitle.value = "";

  // update data of the player (to be sure of the real value)
  // TODO : It is realy necessary ?
  await fetchPlayerCash();
  await fetchPokemons();

  let buyedPokemon = await fetchPokemon(id);

  console.log(buyedPokemon);
  // 1) Check errors
  // 1.a) Check if enough money
  if (playerCash.value < buyedPokemon.pokemon_type_object.cost) {
    errors.value.push("Vous n'avez pas suffisament d'argent.");
  }

  // 1.b) Check if pokemon is already owned
  if (!pokemons.value.find((pokemon) => pokemon.id === id)) {
    errors.value.push("Vous possédez déjà ce Pokémon.");
  }

  // 1.c) add global error message + handle case
  if (errors.value.length) {
    errorsTitle.value = "Erreur lors de l'achat de " + buyedPokemon.name + " :";

    return; // There is some error, stop the buy process
  }

  // TODO : buy the pokemon

  // 2) Remove money

  // 3) Add pokemon to owned pokemons

  try {
    await axios.post(`pokemons/${id}/buy`, {
      
    });

    successTitle.value = "Achat réussi !";
    success.value.push(buyedPokemon.name + " vous attend !");
  } catch (error) {
    errorsTitle.value = "Erreur lors de l'achat de " + buyedPokemon.name + " :";
    errors.value.push("Une erreur est survenue lors de l'achat.");
  }

  // 4) Update data with new values

  await playerCash();
  await fetchPokemons();
};

let showBuyDialog = ref(false);
let buyItem = ref(null);

onMounted(() => {
  fetchPokemons();
  fetchPokemonTypes();

  fetchPlayerCash();
});
</script>

<template>
  <q-page>
    <h1>Magasin</h1>

    <br />

    <q-page-sticky
      position="top-right"
      :offset="[18, 18]"
      class="text-h6 bg-info text-black border-info q-pa-sm rounded-borders z-top"
    >
      Vous avez {{ playerCash }} <q-icon name="currency_ruble" />
    </q-page-sticky>

    <q-banner
      v-if="successTitle || success.length"
      inline-actions
      class="q-mb-lg text-white bg-green"
    >
      <div class="text-h6 flex">
        <q-icon left size="md" name="check_circle" />
        <div>
          {{ successTitle }}

          <q-list dense class="text-subtitle2">
            <q-item v-for="(item, index) in success" :key="index">
              {{ item }}
            </q-item>
          </q-list>
        </div>
      </div>
    </q-banner>

    <q-banner
      v-if="errorsTitle || errors.length"
      inline-actions
      class="q-mb-lg text-white bg-red"
    >
      <div class="text-h6 flex">
        <q-icon left size="md" name="emoji_nature" />
        <div>
          {{ errorsTitle }}

          <q-list dense class="text-subtitle2">
            <q-item v-for="(item, index) in errors" :key="index">
              {{ item }}
            </q-item>
          </q-list>
        </div>
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
              <p>
                <q-icon name="price_change" size="xs" /> Facteur de gain :
                {{ item.pokemon_type_object.cash_factor }}
              </p>
              <p>
                <q-icon name="sentiment_very_satisfied" size="xs" /> Bonheur max
                : {{ item.pokemon_type_object.max_happiness }}
              </p>
            </div>
          </q-card-section>

          <div class="flex normal-btn-size">
            <q-tooltip v-if="playerCash < item.pokemon_type_object.cost">
              Vous n'avez pas assez d'argent pour acheter ce Pokémon.
            </q-tooltip>
            <q-btn
              color="blue"
              push
              @click="
                showBuyDialog = true;
                buyItem = item;
              "
              class="q-ma-xs"
              dense
              :disable="playerCash < item.pokemon_type_object.cost"
            >
              <div>
                <q-icon left size="xs" name="price_check" />
                Acheter<br />
                {{ item.pokemon_type_object.cost }}
                <q-icon name="currency_ruble" size="xs" />
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
            Il vous coutera
            <span class="text-teal"
              >{{ buyItem.pokemon_type_object.cost }}
              <q-icon name="currency_ruble" size="xs" /></span
            >.
          </p>
          <p>
            Votre nouveau solde sera de
            <span class="text-teal"
              >{{ playerCash - buyItem.pokemon_type_object.cost }}
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
          <q-btn color="blue" @click="buyPokemon(buyItem.id)" v-close-popup>
            <q-icon left size="xs" name="price_check" />
            Acheter
          </q-btn>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<style scoped></style>
