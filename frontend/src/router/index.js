import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/about",
      name: "about",
      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/daycare",
      name: "daycare",
      component: () => import("../views/DaycareView.vue"),
      meta: { auth: true },
    },
    {
      path: "/pokemons:success?",
      name: "pokemons",
      props: true,
      component: () => import("../views/PokemonView.vue"),
      meta: { auth: true },
    },
    {
      path: "/pokemons/create",
      name: "pokemons.create",
      component: () => import("../views/CreatePokemonView.vue"),
      meta: { auth: true },
    },
    {
      path: "/pokemons/:id/edit",
      name: "pokemons.edit",
      component: () => import("../views/CreatePokemonView.vue"),
      meta: { auth: true },
    },

    /* ====== SHOP ====== */
    {
      path: "/shop",
      name: "shop",
      component: () => import("../views/ShopView.vue"),
      meta: { auth: true },
    },

    /* ====== USERS ====== */
    {
      path: "/users/create",
      name: "users.create",
      component: () => import("../views/users/CreateUserView.vue"),
    },
    {
      path: "/users:success?",
      name: "users",
      component: () => import("../views/users/UserView.vue"),
    },
  ],
});

router.beforeEach((to, from, next) => {
  const auth = to.matched.some((record) => record.meta.auth);

  if (auth && !sessionStorage.getItem("isAuth")) {
    next({ name: "users" });
  } else {
    next();
  }
});

export default router;
