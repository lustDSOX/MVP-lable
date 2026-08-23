import{G as h}from"./index-6sUDRUmL.js";const u="mvp_lable_cms_news",c="mvp_lable_cms_events",p="mvp_lable_cms_guides",o="mvp_lable_cms_v",l="4";function d(){const t=new Date().toISOString();return[{id:"n1",title:"GRID_OPENING",excerpt:"Лейбл открывает сезон",body:`## Сезон открыт

Лейбл запускает **новый цикл** релизов.

- CLASS TICKETS
- Live events

[Кабинет](/dashboard)`,date:"2026-03-01",status:"published",updatedAt:t},{id:"n2",title:"NEON_DROP",excerpt:"Новый релиз в сети",body:`### NEON_DROP

Стриминг со **всех площадок**.

\`premiere 2026-04-12\``,date:"2026-04-12",status:"published",updatedAt:t},{id:"n3",title:"CHAIN_PROTOCOL",excerpt:"Обновление пайплайна релизов",body:`## Protocol v2

Новый **flow** модерации.

1. Upload
2. Contract
3. Approve

\`status: live\``,date:"2026-05-01",status:"published",updatedAt:t},{id:"n4",title:"LIVE_ARCHIVE",excerpt:"Архив выступлений",body:`### Archive

Записи с **UNDERGROUND_NIGHT**.

![cover](https://picsum.photos/seed/live/800/400)`,date:"2026-05-20",status:"published",updatedAt:t},{id:"n5",title:"DRAFT_ONLY",excerpt:"Черновик",body:"Не публикуется",date:"2026-06-01",status:"draft",updatedAt:t}]}function a(){const t=new Date().toISOString();return[{id:"g1",title:"RELEASE_PIPELINE",excerpt:"Как сдать релиз без отказов",body:`# Release pipeline

1. **Метаданные** — title, genre, date
2. **Обложка** 3000×3000
3. **Треки** + тексты
4. **Договор** — один на релиз

> Модератор видит весь пакет целиком.`,category:"releases",status:"published",updatedAt:t},{id:"g2",title:"CONTRACT_SIGN",excerpt:"Подписание договора",body:`## Договор

Один контракт на **весь релиз** (не на трек).

- Проверь ФИО
- Подпиши в кабинете
- PDF уходит в архив`,category:"legal",status:"published",updatedAt:t},{id:"g3",title:"PLATFORMS_CONNECT",excerpt:"Spotify / Apple / VK",body:`### Площадки

Подключи OAuth в кабинете.

Статистика подтянется после первой синхронизации.`,category:"platforms",status:"published",updatedAt:t},{id:"g4",title:"INTERNAL_DRAFT",excerpt:"Внутренний",body:"draft",category:"internal",status:"draft",updatedAt:t}]}function r(){const t=new Date().toISOString();return[{id:"e1",title:"UNDERGROUND_NIGHT",venue:"Club Void",city:"Moscow",date:"15 AUG",time:"23:00",description:"Live set · CLASS TICKETS night",status:"published",updatedAt:t,ticketUrl:"/purchase",price:"1500 RUB",capacity:"400",ageLimit:"18+"},{id:"e2",title:"WAREHOUSE_RITUAL",venue:"Warehouse 7",city:"SPB",date:"22 AUG",time:"22:00",description:"Label showcase + guest DJs",status:"published",updatedAt:t,ticketUrl:"/purchase",price:"2000 RUB",capacity:"800",ageLimit:"18+"},{id:"e3",title:"NEON_OPEN_AIR",venue:"Roof Base",city:"Moscow",date:"05 SEP",time:"20:00",description:"Open-air set, limited capacity",status:"published",updatedAt:t,ticketUrl:"/purchase",price:"2500 RUB",capacity:"300",ageLimit:"16+"},{id:"e4",title:"LABEL_SHOWCASE_DRAFT",venue:"TBA",city:"SPB",date:"12 SEP",time:"21:00",description:"Draft event (not public)",status:"draft",updatedAt:t,ticketUrl:"/purchase",price:"TBA",capacity:"TBA",ageLimit:"18+"}]}const S=h("cms",{state:()=>({news:[],events:[],guides:[]}),getters:{publishedNews:t=>t.news.filter(e=>e.status==="published"),publishedEvents:t=>t.events.filter(e=>e.status==="published"),publishedGuides:t=>t.guides.filter(e=>e.status==="published")},actions:{hydrate(){try{if(localStorage.getItem(o)!==l){this.news=d(),this.events=r(),this.guides=a(),this.persist(),localStorage.setItem(o,l);return}const t=localStorage.getItem(u),e=localStorage.getItem(c),i=localStorage.getItem(p);this.news=t?JSON.parse(t):d(),this.events=e?JSON.parse(e):r(),this.guides=i?JSON.parse(i):a()}catch{this.news=d(),this.events=r(),this.guides=a()}},persist(){localStorage.setItem(u,JSON.stringify(this.news)),localStorage.setItem(c,JSON.stringify(this.events)),localStorage.setItem(p,JSON.stringify(this.guides))},upsertNews(t){const e=new Date().toISOString();if(t.id){const s=this.news.findIndex(n=>n.id===t.id);if(s>=0)return this.news[s]={...this.news[s],...t,id:t.id,updatedAt:e},this.persist(),t.id}const i=`n-${Date.now()}`;return this.news.unshift({id:i,title:t.title,excerpt:t.excerpt,body:t.body,date:t.date,status:t.status,updatedAt:e}),this.persist(),i},deleteNews(t){this.news=this.news.filter(e=>e.id!==t),this.persist()},upsertGuide(t){const e=new Date().toISOString();if(t.id){const s=this.guides.findIndex(n=>n.id===t.id);if(s>=0)return this.guides[s]={...this.guides[s],...t,updatedAt:e},this.persist(),this.guides[s]}const i={id:"g"+Date.now(),title:t.title,excerpt:t.excerpt||"",body:t.body||"",category:t.category||"general",status:t.status||"draft",updatedAt:e};return this.guides.unshift(i),this.persist(),i},deleteGuide(t){this.guides=this.guides.filter(e=>e.id!==t),this.persist()},upsertEvent(t){const e=new Date().toISOString();if(t.id){const s=this.events.findIndex(n=>n.id===t.id);if(s>=0)return this.events[s]={...this.events[s],...t,id:t.id,updatedAt:e},this.persist(),t.id}const i=`e-${Date.now()}`;return this.events.unshift({id:i,title:t.title,venue:t.venue,city:t.city,date:t.date,time:t.time,description:t.description,status:t.status,updatedAt:e,ticketUrl:t.ticketUrl||"/purchase",price:t.price||"",capacity:t.capacity||"",ageLimit:t.ageLimit||""}),this.persist(),i},deleteEvent(t){this.events=this.events.filter(e=>e.id!==t),this.persist()}}});export{S as u};
