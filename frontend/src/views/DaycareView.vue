<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

const ownedPokemons = ref([]);

const interval = ref(null);

const fetchOwnedPokemons = async () => {
  ownedPokemons.value = (await axios.get("owned-pokemons/my_pokemons")).data;
};

const pokemonTypes = ref([]);

const fetchPokemonTypes = async () => {
  pokemonTypes.value = (await axios.get("pokemon-types/")).data;
};

onMounted(() => {
  fetchOwnedPokemons();
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
  const randomIndexPokemon = Math.floor(Math.random() * ownedPokemons.value.length);
  const randomIndexZone = Math.floor(Math.random() * zones.length);

  document.getElementById("Request").innerText =
    ownedPokemons.value.pokemon_object.value[randomIndexPokemon].name +
    " aimerait aller à la " +
    zones[randomIndexZone].alt +
    ".";
}

function coroutine() {
  interval.value = setInterval(pokemonRequest, 30000);
}

var imageElement = ref("https://upload.wikimedia.org/wikipedia/commons/4/49/Draw-1-black-line.svg");

function moveImage(event) {
  imageElement.value = event.target;
}

function receiveImage(event) {

  if(imageElement.value != "https://upload.wikimedia.org/wikipedia/commons/4/49/Draw-1-black-line.svg")
  {
    event.target.src = imageElement.value.src;
    imageElement = ref("https://upload.wikimedia.org/wikipedia/commons/4/49/Draw-1-black-line.svg");
  }
}
</script>

<template>
  <q-page>
    <h1>La pension</h1>
    <br />
    <p id="Request" style="color: deeppink; font-size: 2em"></p>
    <div class="row">
      <div class="col-xs-12 col-sm-12 col-md-9 col-lg-9">
        <div class="row">
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm">
            <q-img
               src="../assets/images/Beach.jpg"
              style="outline: solid; max-width: 300px; height: 150px"
              fit="cover"
              alt="plage"
            >
              <q-img
                style="
                  outline: solid;
                  max-width: 100px;
                  height: 100px;
                  margin-top: 2em;
                  margin-left: 7em;
                "
                fit="cover"
                src="https://upload.wikimedia.org/wikipedia/commons/4/49/Draw-1-black-line.svg"
               @click="receiveImage"
              ></q-img>
            </q-img>
          </div>
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm"></div>
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm">
            <q-img
              src="../assets/images/Mountain.jpg"
              style="outline: solid; max-width: 300px; height: 150px"
              fit="cover"
              alt="montagne"
            >
            <q-img
                style="
                  outline: solid;
                  max-width: 100px;
                  height: 100px;
                  margin-top: 2em;
                  margin-left: 7em;
                "
                fit="cover"
                src="https://upload.wikimedia.org/wikipedia/commons/4/49/Draw-1-black-line.svg"
                @click="receiveImage"
              ></q-img>
            </q-img>
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
            >
            <q-img
                style="
                  outline: solid;
                  max-width: 100px;
                  height: 100px;
                  margin-top: 2em;
                  margin-left: 7em;
                "
                fit="cover"
                src="https://upload.wikimedia.org/wikipedia/commons/4/49/Draw-1-black-line.svg"
               @click="receiveImage"
              ></q-img>
            </q-img>
          </div>
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm"></div>
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm">
            <q-img
              src="../assets/images/Forest.jpg"
              style="outline: solid; max-width: 300px; height: 150px"
              fit="cover"
              alt="forêt"
            >
            <q-img
                style="
                  outline: solid;
                  max-width: 100px;
                  height: 100px;
                  margin-top: 2em;
                  margin-left: 7em;
                "
                fit="cover"
               @click="receiveImage"
                src="https://upload.wikimedia.org/wikipedia/commons/4/49/Draw-1-black-line.svg"
              ></q-img>
            </q-img>
          </div>
        </div>
        <div class="row">
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm">
            <q-img
              src="../assets/images/Town.jpg"
              style="outline: solid; max-width: 300px; height: 150px"
              fit="cover"
              alt="ville"
            >
            <q-img
                style="
                  outline: solid;
                  max-width: 100px;
                  height: 100px;
                  margin-top: 2em;
                  margin-left: 7em;
                "
                fit="cover"
                src="https://upload.wikimedia.org/wikipedia/commons/4/49/Draw-1-black-line.svg"
               @click="receiveImage"
              ></q-img>
            </q-img>
          </div>
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm"></div>
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm">
            <q-img
              src="../assets/images/PowerPlant.jpg"
              style="outline: solid; max-width: 300px; height: 150px"
              fit="cover"
              alt="centrale"
            >
            <q-img
                style="
                  outline: solid;
                  max-width: 100px;
                  height: 100px;
                  margin-top: 2em;
                  margin-left: 7em;
                "
                fit="cover"
               @click="receiveImage"
               src="https://upload.wikimedia.org/wikipedia/commons/4/49/Draw-1-black-line.svg"
              ></q-img>
            </q-img>
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
          <div class="" v-for="(item, index) in ownedPokemons" :key="index">
            <q-card class="q-mb-sm">
              <div class="flex justify-center">
                <q-card-section>
                  <div class="col justify-center items-center">
                    <div class="text-h7 row justify-center">
                      {{ item.pokemon_object.name }}
                    </div>
                    <div
                      class="image-size-daycare row justify-center items-center q-ma-sm"
                    >
                      <q-img
                        :src="item.pokemon_object.display_image_url"
                        :alt="item.pokemon_object.name"
                        class="image-max-size-parent"
                        fit="contain"
                        @click="moveImage"
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
          <q-btn
            color="green"
            :to="{ name: 'shop' }"
            @click="clearInterval(interval)"
          >
            <q-icon left size="xl" name="add_circle_outline" />
            <div>Acheter un Pokémon</div>
          </q-btn>
        </div>
      </div>
    </div>
  </q-page>
</template>

<style scoped></style>
