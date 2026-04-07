
import CaseDetail from '@/components/cases/CaseDetail.vue'
import GuideDetail from '@/components/guides/GuideDetail.vue'
import TrackForm from '@/components/track/TrackForm.vue'
import Layout from '@/layouts/Layout.vue'
import About from '@/pages/About.vue'
import CasesPage from '@/pages/CasesPage.vue'
import Dashboard from '@/pages/Dashboard.vue'
import EventsPage from '@/pages/EventsPage.vue'
import GuidesPage from '@/pages/GuidesPage.vue'
import Home from '@/pages/Home.vue'
import Login from '@/pages/Login.vue'
import NewsPage from '@/pages/NewsPage.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/',
      component:Layout,
      children:[
        {path:'',component:Home},
        {path: 'about', component:About},
        {path: 'cases', component:CasesPage},
        {path: 'cases/:id', component:CaseDetail, name:"CaseDetail", props:true},
        {path: 'news', component:NewsPage},
        {path: 'events', component:EventsPage},
        {path: 'guides', component:GuidesPage},
        {path: 'guides/:id', component:GuideDetail, name:"GuideDetail", props:true},
        {path: 'upload', component:TrackForm},
        {path: 'dashboard', component:Dashboard},
        {path: 'login', component:Login},
      ]
    }
  ],
})

export default router
