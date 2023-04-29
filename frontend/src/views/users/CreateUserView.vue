<!-- eslint-disable prettier/prettier -->
<script setup>
import axios from "axios";
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";

import { onConnect } from "@/assets/js/persistanceLoginInfo";

import { varToString } from "@/assets/js/utils.js"; // IMPORTANT : Need to be in { } to work !
import MessageBanner from "@/components/MessageBanner.vue";

const route = useRoute();
const router = useRouter();

let successTitle = ref("");
let success = ref([]);
let errorsTitle = ref("");
let errors = ref([]);

const username = ref("");
const password = ref("");
const confirmPassword = ref("");

username.value = route.query.username;

const submit = async () => {
  errors.value = [];
  errorsTitle.value = "";

  // Validation
  if (!username.value) {
    errors.value.push("Le nom d'utilisateur est obligatoire.");
  }
  if (!password.value) {
    errors.value.push("Le mot de passe est obligatoire.");
  }
  if (!confirmPassword.value) {
    errors.value.push("La confirmation de mot de passe est obligatoire.");
  }
  if (password.value !== confirmPassword.value) {
    errors.value.push("Les mots de passe ne correspondent pas.");
  }

  if (errors.value.length) {
    errorsTitle.value =
      "Erreur avec les données du formulaire, veuillez les corriger :";

    return; // There is some error, stop the process
  }

  // // Send to backend
  await axios
    .post("users/", {
      username: username.value,
      password: password.value,
    })
    .then(() => {
      successTitle.value = "Compte créé avec succès";
      success.value.push("Vous êtes automatiquement connecté.");

      sessionStorage.setItem(varToString({ successTitle }), successTitle.value);
      sessionStorage.setItem(
        varToString({ success }),
        JSON.stringify(success.value)
      );

      onConnect(true, false, username.value);

      router.push({ name: "home" });
    })
    .catch((error) => {
      console.log(error);
      errorsTitle.value = "La création a échoué";
      errors.value.push("Ce nom est peut-être déjà pris ?");
    });
};
</script>

<template>
  <q-page padding>
    <q-form class="q-gutter-md" @submit="submit()">
      <div class="row self-center justify-evenly">
        <div class="col-12 col-sm-10 col-md-8">
          <q-card class="q-pa-lg">
            <q-card-section class="">
              <q-btn color="blue-grey" :to="{ name: 'users' }">
                <q-icon left name="arrow_back_ios" />
                Retour
              </q-btn>
            </q-card-section>

            <q-card-section class="text-center">
              <div class="text-h5">Créer un compte</div>
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
              <q-input
                v-model="confirmPassword"
                type="password"
                label="*Confirmation de mot de passe"
                class="q-mb-md"
                outlined
              />
            </q-card-section>

            <q-card-section class="q-gutter-y-sm">
              <div class="row justify-center q-gutter-sm">
                <q-btn
                  type="submit"
                  color="green"
                  class="col-12 col-sm-8 col-md-6"
                >
                  <q-icon left name="fact_check" />
                  <div>Créer</div>
                </q-btn>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </q-form>
  </q-page>
</template>
