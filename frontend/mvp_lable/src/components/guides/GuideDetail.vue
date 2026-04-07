<template>
  <section
    class="min-h-screen bg-linear-to-br from-black via-gray-900 to-gray-950 px-6 pt-24 pb-12"
    :class="{ 'no-select': !isDebug }"
  >
    <div class="max-w-4xl mx-auto">
      <router-link
        to="/guides"
        class="inline-flex items-center text-[#39FF14] hover:text-[#00CC00] text-lg font-bold mb-6"
      >
        &larr; Back to guides
      </router-link>

      <article
        ref="articleRef"
        class="bg-gray-900/70 border border-gray-700 rounded-2xl p-8"
        @contextmenu="preventContextMenu"
        @selectstart="preventSelect"
      >
        <h2 class="text-4xl font-black uppercase text-white mb-4">
          {{ currentGuide?.title }}
        </h2>

        <div class="text-gray-300 prose prose-invert max-w-none text-lg leading-relaxed">
          {{ currentGuide?.content }}
        </div>

        <div class="mt-8 p-6 bg-gray-800/30 border border-gray-700 rounded-xl">
          <h3 class="text-xl font-bold text-white mb-3">Watermark (пример)</h3>
          <p class="text-gray-400 text-sm">
            Все материалы лейбла CLASS TICKETS защищены условием авторского соглашения артиста.
          </p>
          <img
            src="/src/assets/watermark-class-tickets.png"
            alt="Watermark CLASS TICKETS"
            class="w-40 h-10 mt-4 opacity-10"
          />
        </div>
      </article>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'GuideDetail',
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      guides: [
        {
          id: 1,
          title: 'Как начать записывать свои треки дома',
          content:
            'Начни с базовой установки микрофона и простого аудиоинтерфейса. Важно, чтобы ты не сидел в окружении громких звуков и эхо, поэтому идеально — спальня с подручной изоляцией. Первые треки лучше записывать без лишней обработки: компресс, эквалайзер, реверберация — всё это ты будешь добавлять постепенно. Главное — экспериментируй, не бойся плохих записей, потому что именно из них приходит лучший результат.',
        },
        {
          id: 2,
          title: 'Как писать текст, чтобы его слышали',
          content:
            'Текст должен быть живым, а не похожим на школьное сочинение. Вспоминай истории, которые тебя реально задевали, и перекладывай их в рифму. Слушай себя вслух, ходи по комнате, проговаривай фразы, как будто рассказываешь кому‑то в реальной жизни. Не старайся писать слишком умно, лучше честно и просто. Смысл — важнее слова, а мелодия — чаще всего сама подскажет, какие строки оставить.',
        },
        {
          id: 3,
          title: 'Личный кабинет артиста: как работать с отчётами',
          content:
            'В кабинете доступны статистика прослушиваний, билеты, отчёты по релизам. Каждый цифровой трек — это отдельный «билет» со своей статистикой. Следи, откуда идёт трафик, как меняется аудитория, чтобы лучше понимать, куда развивать своё звучание и визуальный стиль.',
        },
      ] satisfies GuideItemData[],
      isDebug: false, // true — если хочешь включить выделение текста для тестов
    }
  },
  computed: {
    currentGuide(this: any): typeof this.guides[0] | undefined {
      const numId = Number(this.id)
      return this.guides.find((g: any) => g.id === numId)
    },
  },
  mounted() {
    const el = this.$refs.articleRef as HTMLElement | null
    if (el) {
      el.style.userSelect = 'none'
    }
  },
  methods: {
    preventContextMenu(e: Event) {
      e.preventDefault()
    },
    preventSelect(e: Event) {
      e.preventDefault()
    },
  },
})

interface GuideItemData {
  id: number
  title: string
  content: string
}
</script>