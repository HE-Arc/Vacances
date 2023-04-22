<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

const pokemons = ref([]);

const interval = ref(null);

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

onMounted(() => {
  fetchPokemons();
  fetchPokemonTypes();
  coroutine();
});

const zones = [
  {
    source: "../assets/images/Beach.jpg",
    alt: "plage",
  },
  {
    source: "../assets/images/Forest.jpg",
    alt: "forêt",
  },
  {
    source: "../assets/images/Mountain.jpg",
    alt: "montagne",
  },
  {
    source: "../assets/images/Town.jpg",
    alt: "ville",
  },
  {
    source: "../assets/images/Cave.jpg",
    alt: "grotte",
  },
  {
    source: "../assets/images/PowerPlant.jpg",
    alt: "centrale",
  },
];

function pokemonRequest() {
  const randomIndexPokemon = Math.floor(Math.random() * pokemons.value.length);
  const randomIndexZone = Math.floor(Math.random() * zones.length);

  document.getElementById("Request").innerText =
    pokemons.value[randomIndexPokemon].name +
    " aimerait aller à la " +
    zones[randomIndexZone].alt +
    ".";
}

function coroutine() {
  interval.value = setInterval(pokemonRequest, 30000);
}
</script>

<template>
  <q-page>
    <h1>La pension</h1>
    <br />
    <p id="Request" style="color: deeppink; font-size: 3em"></p>
    <div class="row">
      <div class="col-xs-12 col-sm-12 col-md-9 col-lg-9">
        <div class="row">
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm">
            <q-img
              src="../assets/images/Beach.jpg"
              style="outline: solid; max-width: 300px; height: 150px"
              fit="cover"
              alt="plage"
            ></q-img>
          </div>
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm"></div>
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm">
            <q-img
              src="../assets/images/Mountain.jpg"
              style="outline: solid; max-width: 300px; height: 150px"
              fit="cover"
              alt="montagne"
            ></q-img>
          </div>
        </div>
        <div class="row">
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm"></div>
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm">
            <q-img
              src="../assets/images/Cave.jpg"
              style="outline: solid; max-width: 300px; height: 150px"
              fit="cover"
              alt="grotte"
            ></q-img>
          </div>
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm"></div>
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm">
            <q-img
              src="../assets/images/Forest.jpg"
              style="outline: solid; max-width: 300px; height: 150px"
              fit="cover"
              alt="forêt"
            ></q-img>
          </div>
        </div>
        <div class="row">
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm">
            <q-img
              src="../assets/images/Town.jpg"
              style="outline: solid; max-width: 300px; height: 150px"
              fit="cover"
              alt="ville"
            ></q-img>
          </div>
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm"></div>
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm">
            <q-img
              src="../assets/images/PowerPlant.jpg"
              style="outline: solid; max-width: 300px; height: 150px"
              fit="cover"
              alt="centrale"
            ></q-img>
          </div>
        </div>
      </div>
      <div class="col-xs-12 col-sm-12 col-md-3 col-lg-3 q-pl-xl">
        <div
          class="container"
          style="outline: solid; outline-offset: 2em; margin-top: 3em"
        >
          <h5>Mes Pokémon</h5>
          <br />
          <!-- Card list -->
          <div class="" v-for="(item, index) in pokemons" :key="index">
            <q-card class="q-mb-sm">
              <div class="flex justify-center">
                <q-card-section>
                  <div class="col justify-center items-center">
                    <div class="text-h7 row justify-center">
                      {{ item.name }}
                    </div>
                    <div
                      class="image-size-daycare row justify-center items-center q-ma-sm"
                    >
                      <q-img
                        :src="item.display_image_url"
                        :alt="item.name"
                        class="image-max-size-parent"
                        fit="contain"
                      />
                    </div>
                  </div>
                </q-card-section>
              </div>
              <q-separator inset />
            </q-card>
          </div>
        </div>
        <br />
        <div class="text-center q-mb-md q-mt-md">
          <q-btn color="green" :to="{ name: 'shop' }" @click="clearInterval(interval);">
            <q-icon left size="xl" name="add_circle_outline" />
            <div>Acheter un Pokémon</div>
          </q-btn>
        </div>
      </div>
    </div>
  </q-page>
</template>

<style scoped></style>
