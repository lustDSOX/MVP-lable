<template>
  <form @submit.prevent="onSubmit" class="contract-form font-['Inter',sans-serif]">
    
    <!-- Секция 1: Личные данные -->
    <div class="form-section">
      <div class="section-header">
        <h4 class="section-title">01 // SUBJECT_INFO</h4>
        <div class="section-line"></div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-6">
        <div class="input-group">
          <label class="input-label">
            <span>FULL_LEGAL_NAME</span>
            <span class="required-mark">*REQ</span>
          </label>
          <input v-model="form.fullName" type="text" required placeholder="IVANOV IVAN" class="form-input" />
        </div>

        <div class="input-group">
          <label class="input-label">
            <span>UPLINK_MAIL</span>
            <span class="required-mark">*REQ</span>
          </label>
          <input v-model="form.email" type="email" required placeholder="USER@SOX.NET" class="form-input" />
        </div>

        <div class="input-group">
          <label class="input-label">
            <span>COMM_PHONE</span>
            <span class="required-mark">*REQ</span>
          </label>
          <input v-model="form.phone" type="tel" required placeholder="+7 (___) ___-__-__" class="form-input" />
        </div>

        <div class="input-group">
          <label class="input-label">
            <span>ARTIST_ALIAS</span>
            <span class="required-mark">*REQ</span>
          </label>
          <input v-model="form.nicknames" type="text" required placeholder="DJ_NEON" class="form-input" />
        </div>

        <div class="input-group md:col-span-2">
          <label class="input-label">
            <span>NETWORK_CREDENTIALS</span>
            <span class="required-mark">*REQ</span>
          </label>
          <input v-model="form.socialNetworks" type="text" required placeholder="VK.COM/ARTIST // TG/ALIAS" class="form-input" />
        </div>

        <div class="input-group">
          <label class="input-label"><span>AUDIO_GENRE</span></label>
          <input v-model="form.genre" type="text" placeholder="INDUSTRIAL / TRAP" class="form-input" />
        </div>

        <div class="input-group">
          <label class="input-label">
            <span>SUBJECT_AGE</span>
            <span class="required-mark">*REQ</span>
          </label>
          <input v-model.number="form.age" type="number" required min="14" max="100" placeholder="18" class="form-input" />
        </div>

        <div class="input-group md:col-span-2">
          <label class="input-label">
            <span>LOCATION_ZONE</span>
            <span class="required-mark">*REQ</span>
          </label>
          <input v-model="form.city" type="text" required placeholder="MOSCOW_UNDERGROUND" class="form-input" />
        </div>
      </div>
    </div>

    <!-- Секция 2: Релиз -->
    <div class="form-section">
      <div class="section-header">
        <h4 class="section-title text-red">02 // RELEASE_DATA</h4>
        <div class="section-line bg-red"></div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="input-group">
          <label class="input-label">
            <span class="text-[#ff0000]">PRIMARY_TRACK_TITLE</span>
            <span class="required-mark">*REQ</span>
          </label>
          <input v-model="form.trackTitle" type="text" required placeholder="TRACK_NAME_01" class="form-input border-red" />
        </div>

        <div class="input-group">
          <label class="input-label"><span>CO_AUTHORS</span></label>
          <input v-model="form.coAuthors" type="text" placeholder="FEAT_NAME / EMPTY" class="form-input" />
        </div>
      </div>
    </div>

    <!-- КНОПКА ОТПРАВКИ -->
    <button 
      type="submit" 
      :disabled="isLoading"
      class="submit-button group"
    >
      <span v-if="!isLoading" class="button-content">
        >>> GENERATE_CONTRACT
      </span>
      <span v-else class="button-content processing">
        <div class="spinner"></div>
        PROCESSING_DATA...
      </span>
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
/* Контейнер формы */
.contract-form {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
  position: relative;
  z-index: 10;
}

/* Секции и заголовки */
.form-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.section-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.5rem;
}
.section-title {
  font-family: 'Archivo Black', sans-serif;
  font-size: 1.5rem;
  color: white;
  text-transform: uppercase;
  letter-spacing: -0.025em;
  margin: 0;
}
.section-title.text-red {
  color: #ff0000;
}
.section-line {
  flex: 1;
  height: 2px;
  background-color: #333;
}
.section-line.bg-red {
  background-color: #ff0000;
  opacity: 0.5;
}

/* Группы инпутов */
.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.input-label {
  display: flex;
  justify-content: space-between;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.625rem; /* 10px */
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.1em;
}
.required-mark {
  color: #ff0000;
}

/* Сами поля ввода (Брутализм) */
.form-input {
  width: 100%;
  padding: 0.75rem 1rem;
  background-color: black;
  border: 2px solid #333;
  color: white;
  font-family: 'JetBrains Mono', monospace;
  font-size: 1rem;
  text-transform: uppercase;
  transition: border-color 0.2s, background-color 0.2s;
}
.form-input::placeholder {
  color: #333;
}
.form-input:focus {
  outline: none;
  border-color: #ffffff;
  background-color: #050505;
}
/* Спец-инпут для названия трека */
.form-input.border-red:focus {
  border-color: #ff0000;
}

/* Кнопка отправки */
.submit-button {
  width: 100%;
  padding: 1.5rem;
  background-color: white;
  color: black;
  border: 4px solid black;
  text-transform: uppercase;
  font-family: 'Archivo Black', sans-serif;
  font-size: 1.5rem;
  box-shadow: 6px 6px 0 #ff0000;
  transition: all 0.15s;
  cursor: pointer;
  margin-top: 1rem;
}
.submit-button:hover:not(:disabled) {
  box-shadow: none;
  transform: translate(6px, 6px);
  background-color: #ff0000;
  color: white;
}
.submit-button:active:not(:disabled) {
  transform: translate(4px, 4px);
  box-shadow: 2px 2px 0 #000;
}
.submit-button:disabled {
  background-color: #222;
  color: #555;
  box-shadow: none;
  border-color: #111;
  cursor: not-allowed;
}

/* Внутренности кнопки */
.button-content {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  letter-spacing: -0.025em;
}
.processing {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.25rem;
  font-weight: bold;
}

/* Спиннер загрузки */
.spinner {
  width: 1.5rem;
  height: 1.5rem;
  border: 3px solid black;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
.submit-button:disabled .spinner {
  border-color: #555;
  border-top-color: transparent;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>