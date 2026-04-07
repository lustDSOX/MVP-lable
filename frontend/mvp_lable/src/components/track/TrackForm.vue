<template>
  <!-- Оставляем только форму. Весь "корпус" теперь снаружи в ContractModal -->
  <form @submit.prevent="onSubmit" class="flex flex-col gap-8 relative z-10 font-['Impact','Arial_Black',sans-serif]">
    
    <!-- Секция 1: Личные данные -->
    <div class="space-y-6">
      <div class="flex items-center gap-4 mb-4">
        <h4 class="text-2xl font-black text-white italic uppercase tracking-tighter">01_SUBJECT_INFO</h4>
        <div class="flex-1 h-0.5 bg-[#333]"></div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6">
        <div class="flex flex-col gap-2">
          <label class="text-[10px] font-mono text-[#39FF14] uppercase tracking-widest flex justify-between">
            <span>FULL_LEGAL_NAME</span>
            <span class="text-[#ff0000]">*REQUIRED</span>
          </label>
          <input v-model="form.fullName" type="text" required placeholder="IVANOV IVAN" class="modal-input" />
        </div>

        <div class="flex flex-col gap-2">
          <label class="text-[10px] font-mono text-[#39FF14] uppercase tracking-widest flex justify-between">
            <span>UPLINK_MAIL</span>
            <span class="text-[#ff0000]">*REQUIRED</span>
          </label>
          <input v-model="form.email" type="email" required placeholder="USER@SOX.NET" class="modal-input" />
        </div>

        <div class="flex flex-col gap-2">
          <label class="text-[10px] font-mono text-[#39FF14] uppercase tracking-widest flex justify-between">
            <span>COMM_PHONE</span>
            <span class="text-[#ff0000]">*REQUIRED</span>
          </label>
          <input v-model="form.phone" type="tel" required placeholder="+7 (___) ___-__-__" class="modal-input" />
        </div>

        <div class="flex flex-col gap-2">
          <label class="text-[10px] font-mono text-[#39FF14] uppercase tracking-widest flex justify-between">
            <span>ARTIST_ALIAS</span>
            <span class="text-[#ff0000]">*REQUIRED</span>
          </label>
          <input v-model="form.nicknames" type="text" required placeholder="DJ_NEON" class="modal-input" />
        </div>

        <div class="flex flex-col gap-2 md:col-span-2">
          <label class="text-[10px] font-mono text-[#39FF14] uppercase tracking-widest italic">NETWORK_CREDENTIALS</label>
          <input v-model="form.socialNetworks" type="text" required placeholder="VK.COM/ARTIST // TG/ALIAS" class="modal-input" />
        </div>

        <div class="flex flex-col gap-2">
          <label class="text-[10px] font-mono text-[#39FF14] uppercase tracking-widest">AUDIO_GENRE</label>
          <input v-model="form.genre" type="text" placeholder="INDUSTRIAL/TRAP" class="modal-input" />
        </div>

        <div class="flex flex-col gap-2">
          <label class="text-[10px] font-mono text-[#39FF14] uppercase tracking-widest">SUBJECT_AGE</label>
          <input v-model.number="form.age" type="number" required min="14" max="100" placeholder="18" class="modal-input" />
        </div>

        <div class="flex flex-col gap-2 md:col-span-2">
          <label class="text-[10px] font-mono text-[#39FF14] uppercase tracking-widest">LOCATION_ZONE</label>
          <input v-model="form.city" type="text" required placeholder="MOSCOW_UNDERGROUND" class="modal-input" />
        </div>
      </div>
    </div>

    <!-- Секция 2: Релиз -->
    <div class="pt-8 border-t-4 border-dashed border-[#222]">
      <div class="flex items-center gap-4 mb-6">
        <h4 class="text-2xl font-black text-[#ff0000] italic uppercase tracking-tighter">02_RELEASE_DATA</h4>
        <div class="flex-1 h-0.5 bg-[#333]"></div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="flex flex-col gap-2">
          <label class="text-[10px] font-mono text-[#ff0000] uppercase tracking-widest">PRIMARY_TRACK_TITLE</label>
          <input v-model="form.trackTitle" type="text" required placeholder="TRACK_NAME_01" class="modal-input-red" />
        </div>

        <div class="flex flex-col gap-2">
          <label class="text-[10px] font-mono text-gray-600 uppercase tracking-widest">CO_AUTHORS</label>
          <input v-model="form.coAuthors" type="text" placeholder="FEAT_NAME / EMPTY" class="modal-input" />
        </div>
      </div>
    </div>

    <!-- КНОПКА ОТПРАВКИ -->
    <button 
      type="submit" 
      :disabled="isLoading"
      class="group relative w-full py-6 bg-[#39FF14] text-black font-black uppercase text-3xl border-4 border-black shadow-[10px_10px_0_#fff] hover:shadow-none hover:translate-x-1 hover:translate-y-1 active:translate-x-2 active:translate-y-2 disabled:bg-gray-800 disabled:text-gray-500 disabled:shadow-none transition-none overflow-hidden"
    >
      <div class="relative z-10 flex items-center justify-center gap-4 italic tracking-tighter">
        <span v-if="!isLoading">>> GENERATE_CONTRACT</span>
        <span v-else class="flex items-center gap-3 uppercase">
           <div class="w-6 h-6 border-4 border-black border-t-transparent rounded-full animate-spin"></div>
           PROCESSING...
        </span>
      </div>
      <div class="absolute inset-0 bg-white opacity-0 group-hover:opacity-10 pointer-events-none"></div>
    </button>
  </form>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export interface ContractFormData {
  fullName: string;
  email: string;
  phone: string;
  nicknames: string;
  socialNetworks: string;
  genre: string;
  age: number | null;
  city: string;
  trackTitle: string;
  coAuthors: string;
}

export default defineComponent({
  name: 'TrackForm',
  props: {
    isLoading: { type: Boolean, default: false }
  },
  emits: {
    'submit-form': (payload: ContractFormData) => true
  },
  data() {
    return {
      form: {
        fullName: '', email: '', phone: '',
        nicknames: '', socialNetworks: '', genre: '',
        age: null as number | null, city: '',
        trackTitle: '', coAuthors: ''
      } as ContractFormData
    }
  },
  methods: {
    onSubmit() {
      this.$emit('submit-form', { ...this.form })
    }
  }
})
</script>

<style scoped>
@reference "tailwindcss"; 

.modal-input {
  @apply w-full px-4 py-3 bg-black border-2 border-[#333] text-white font-mono text-lg 
         focus:outline-none focus:border-[#39FF14] shadow-[inset_0_4px_10px_rgba(0,0,0,1)] 
         transition-none placeholder:text-gray-800 uppercase;
}
.modal-input-red {
  @apply w-full px-4 py-3 bg-black border-2 border-[#333] text-white font-mono text-lg 
         focus:outline-none focus:border-[#ff0000] shadow-[inset_0_4px_10px_rgba(0,0,0,1)] 
         transition-none placeholder:text-gray-800 uppercase;
}
</style>