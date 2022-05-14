import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Admin from "@/components/Admin";
import Login from "@/components/Login";
import TwentyFourHourProhibition from "@/components/forms/TwentyFourHourProhibition/TwentyFourHourProhibition";
import TwelveHourProhibition from "@/components/forms/TwelveHourSuspension/TwelveHourProhibition";
import ImmediateRoadsideProhibition from "@/components/forms/ImmediateRoadsideProhibition";
import VehicleImpoundment from "@/components/forms/VehicleImpoundment/VehicleImpoundment";
import SVGPrint from "@/components/print/SvgPrint";
import NotFound from "@/components/NotFound";

Vue.use(Router)

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/admin',
      name: 'Admin',
      component: Admin,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/24Hour/:id',
      name: '24Hour',
      component: TwentyFourHourProhibition,
      props: true
    },
    {
      path: '/12Hour/:id',
      name: '12Hour',
      component: TwelveHourProhibition,
      props: true
    },
    {
      path: '/IRP/:id',
      name: 'IRP',
      component: ImmediateRoadsideProhibition,
      props: true
    },
    {
      path: '/VI/:id',
      name: 'VI',
      component: VehicleImpoundment,
      props: true
    },
    {
      path: '/:form_type/:id/print',
      name: 'print',
      component: SVGPrint,
      props: true
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: NotFound
    },
  ],
  scrollBehavior () {
    return { x: 0, y: 0 };
  }
})

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}


router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // We wait for Keycloak init, then we can call all methods safely
    while (router.app.$keycloak.createLoginUrl === null) {
      await sleep(100)
    }
    if (router.app.$keycloak.authenticated) {
      next()
    } else {
      const loginUrl = router.app.$keycloak.createLoginUrl()
      window.location.replace(loginUrl)
    }
  } else {
    next()
  }
})


export default router
