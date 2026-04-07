<template>
  <div id="app" class="flex flex-col min-h-screen bg-black overflow-x-hidden selection:bg-[#39FF14] selection:text-black font-['Impact','Arial_Black',sans-serif]">
    
    <!-- 1. ГЛОБАЛЬНЫЙ ФОН: Он лежит ПОД всем -->
    <div class="fixed inset-0 z-0 pointer-events-none select-none">
      <!-- Слой 1: Техническая сетка -->
      <div class="absolute inset-0 bg-[radial-gradient(#1a1a1a_2px,transparent_2px)] bg-size-[25px_25px] opacity-60"></div>
      <!-- Слой 2: Текстура карбона -->
      <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] bg-size-[40px_40px] opacity-80"></div>
      <!-- Слой 3: CRT-эффект -->
      <div class="absolute inset-0 crt-overlay opacity-40"></div>
    </div>

    <!-- 2. HEADER: Над фоном (z-50) -->
    <Header  ></Header>

    <!-- 3. MAIN: Зона контента (Прозрачная!) -->
    <main class="relative z-10 flex-1 flex flex-col">
      <!-- RouterView просто отрисовывает контент страницы -->
      <router-view />
    </main>

    <!-- 4. FOOTER: Над фоном (z-50) -->
    <Footer  ></Footer>
  </div>
</template>

<style>
/* Обязательно добавь CRT-стили здесь */
.crt-overlay {
  background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%),
              linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
  background-size: 100% 4px, 3px 100%;
  pointer-events: none;
}
</style>

<script lang="ts">
import { defineComponent } from 'vue';
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';

export default defineComponent({
  name:'Layout',
  components:{
    Header,
    Footer
  }
})
</script>