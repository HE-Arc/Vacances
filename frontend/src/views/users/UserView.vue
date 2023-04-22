<!-- eslint-disable prettier/prettier -->
<script setup>
import axios from "axios";
import { ref } from "vue";


const errors = ref(false);

const username = ref("");
const password = ref("");


const submit = async () => {
  try {
    errors.value = false;
    const resultUser = await axios.post("users/login/",
    {
      username: username.value,
      password: password.value,
      withCredentials : true,
    });
    if(resultUser.data.success == null)
    {
      errors.value = true;
    }
    else
    {
      location.href = "/?success=true";
    }
    

  } catch (error) {
    console.log(error);
    errors.value = true;
  }
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

            <q-card-section>
              <q-input
                v-model="username"
                label="*Nom"
                class="q-mb-md"
                outlined
              />
              <q-input
                v-model="password"
                label="*Mot de passe"
                class="q-mb-md"
                outlined
              />
            </q-card-section>

            <q-banner
              v-if="errors"
              inline-actions
              class="q-mb-lg text-white bg-red"
            >
              <div class="text-h6">
                <q-icon left size="md" name="emoji_nature" />
                Erreur! utilisateur incorrect!
              </div>
            </q-banner>

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
