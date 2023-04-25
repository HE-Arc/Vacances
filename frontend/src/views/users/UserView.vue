<!-- eslint-disable prettier/prettier -->
<script setup>
import axios from "axios";
import { ref } from "vue";
import { useRouter } from "vue-router";

import { varToString } from "@/assets/js/utils.js"; // IMPORTANT : Need to be in { } to work !
import MessageBanner from "@/components/MessageBanner.vue";

let successTitle = ref("");
let success = ref([]);
let errorsTitle = ref("");
let errors = ref([]);

const username = ref("");
const password = ref("");

const router = useRouter();

const submit = async () => {
  errors.value = [];
  errorsTitle.value = "";

  // Validation
  if (!username.value) {
    errors.value.push("Le nom est obligatoire.");
  }
  if (!password.value) {
    errors.value.push("Le mot de passe est obligatoire.");
  }

  if (errors.value.length) {
    errorsTitle.value =
      "Erreur avec les données du formulaire, veuillez les corriger :";

    return; // There is some error, stop the buy process
  }

  // Send to backend
  await axios
    .post("users/login/", {
      username: username.value,
      password: password.value,
    })
    .then(() => {
      successTitle.value = "Connexion réussie !";
      success.value.push("Vous êtes connecté avec le pseudo " + username.value);

      sessionStorage.setItem(varToString({ successTitle }), successTitle.value);
      sessionStorage.setItem(
        varToString({ success }),
        JSON.stringify(success.value)
      );

      sessionStorage.setItem("isAuth", true); // TODO A token will be better
      router.push({ path: "/" });
    })
    .catch(() => {
      errorsTitle.value = "Identification échouée";
      errors.value.push("Est-ce le bon nom d'utilisateur et mot de passe ?");

      sessionStorage.removeItem("isAuth");
    });
};
</script>

<template>
  <q-page padding>
    <q-form class="q-gutter-md" @submit="submit()">
      <div class="row self-center justify-evenly">
        <div class="col-8 col-md-6 q-mt-md">
          <q-card class="q-pa-lg">
            <q-card-section class="">
              <q-btn color="blue-grey" :to="{ name: 'home' }">
                <q-icon left name="arrow_back_ios" />
                Retour
              </q-btn>
              <q-btn color="blue-grey" :to="{ name: 'users.create' }">
                Créer un compte
              </q-btn>
            </q-card-section>

            <q-card-section class="text-center">
              <div class="text-h5">Se connecter</div>
            </q-card-section>

            <MessageBanner
              :title="errorsTitle"
              :items="errors"
              icon="emoji_nature"
              color="red"
            />

            <q-card-section>
              <q-input
                v-model="username"
                label="*Nom"
                class="q-mb-md"
                outlined
              />
              <q-input
                v-model="password"
                type="password"
                label="*Mot de passe"
                class="q-mb-md"
                outlined
              />
            </q-card-section>

            <q-card-section class="q-gutter-y-sm">
              <div class="text-center">
                <q-btn type="submit" color="green">
                  <q-icon left name="fact_check" />
                  <div>Se connecter</div>
                </q-btn>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </q-form>
  </q-page>
</template>
