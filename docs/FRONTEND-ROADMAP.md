# Frontend Roadmap — CLASS TICKETS / MVP-lable

Статус на 2026-08-17. Живой превью: https://lustdsox.github.io/MVP-lable/  
Код: `frontend/mvp_lable` · ветки: `main` (код) + `gh-pages` (билд).

Цель: стабильный мобильный Y2K-фронт без лагов, с рабочей навигацией и страницами в едином стиле — до подключения реального API/бэка.

---

## 0. Уже сделано

- [x] Базовый адаптив (Tailwind `sm/md/lg`) на Home, About, Cases, News, Events, Guides, Login, cabinets
- [x] `img { max-width: 100%; height: auto }` + object-fit утилиты
- [x] Мобильное меню в Header
- [x] GitHub Pages (`gh-pages`), base `/MVP-lable/`
- [x] Сборка без битого import `line.svg`

---

## 1. Performance — долгая загрузка и лаги 🔴 P0

**Проблема:** бандл тянет гигантские PNG/GIF. На телефоне — долгий first paint, jank при скролле.

| Файл | ~размер | Где используется |
|------|---------|------------------|
| `chrome/chain_circle.png` | ~4.0 MB | News / декор |
| `chrome/chain_flow.png` | ~3.6 MB | News / декор |
| `texture/metall.png` | ~3.7 MB | фоны |
| `chrome/chain.png` | ~3.4 MB | декор |
| `kai-angel-viperr.gif` | ~1.3 MB | Home |
| `texture/silver.jpg` | ~1.1 MB | текстуры |

### Задачи

1. **Сжать / заменить ассеты**
   - PNG → WebP (или AVIF), цель ≤ 200–400 KB на декор
   - GIF → WebP-анимация или короткий MP4/`<video autoplay muted loop playsinline>`
   - Удалить неиспользуемые (`metall.png` если есть `metall.jpg`)
   - Инструмент: `sharp` / Squoosh / `imagemin`

2. **Ленивая загрузка**
   - `loading="lazy"` + `decoding="async"` на все не-LCP картинки
   - Декор ниже fold — `v-show` / Intersection Observer
   - На mobile (`< md`) не грузить тяжёлые absolute-декоры (`hidden md:block` + не импортировать в критический путь)

3. **Code splitting**
   - `() => import(...)` для Dashboard, ModeratorCabinet, AdminCabinet, TrackForm, CaseDetail, GuideDetail
   - Проверить что `vite-plugin-vue-devtools` не в prod-бандле

4. **Фоны и CSS**
   - Убрать full-screen blur/mix-blend на mobile
   - `prefers-reduced-motion: reduce` — отключить spin / animate-ping / CRT
   - `will-change` только точечно, не на всём layout

5. **Метрики (цель)**
   - LCP < 2.5s на 4G mid-tier
   - JS gzip < 150 KB initial
   - Нет layout shift от поздних картинок (`width`/`height` или aspect-ratio)

**Файлы:** `src/assets/**`, `NewsPage.vue`, `Home.vue`, `About.vue`, `vite.config.ts`, `Layout.vue`

---

## 2. Mobile / адаптив — добить 🔴 P0

Базовый grid есть, остаются edge-cases.

### Задачи

1. **Overflow**
   - Проверить `overflow-x: hidden` на `body` / Layout
   - Absolute-декоры с отрицательными `left/right` не расширяют ширину (`max-w`, `overflow-hidden` на родителях)

2. **Типографика**
   - Заголовки `text-6xl`/`text-8xl` на mobile → clamp: `text-3xl sm:text-5xl lg:text-7xl`
   - Длинные uppercase-строки: `break-words` / `hyphens`

3. **Touch targets**
   - Кнопки и ссылки ≥ 44×44 px
   - Убрать hover-only интеракции как единственный способ действия

4. **Safe area**
   - `padding-bottom: env(safe-area-inset-bottom)` для footer / fixed bar
   - `viewport-fit=cover` в `index.html` если нужен notch

5. **Страницы — чеклист mobile**
   - [ ] Home — GIF/кнопка не вылезают, CTA видна без горизонтального скролла
   - [ ] About — карточки philosophy в 1 колонку, SVG декор `hidden sm:block`
   - [ ] Cases / CaseDetail — модалка на весь экран, скролл контента, кнопка X доступна
   - [ ] News — сетка 1 col, тяжёлые chrome-картинки off на mobile
   - [ ] Events — карточки, даты читаемы
   - [ ] Guides + **GuideDetail** — см. §4
   - [ ] Login / Dashboard / Moderator / Admin — формы и таблицы без горизонтального скролла

6. **QA**
   - iPhone SE / 390px, 430px, Android 360px
   - Chrome DevTools + реальный телефон через Pages

**Файлы:** все `pages/*`, `components/Header.vue`, `components/Footer.vue`, `layouts/Layout.vue`, `base.css`

---

## 3. Нижний bar / Footer 🔴 P0

**Проблемы (по коду):**

- Ссылки в QUICK_MENU ведут на **несуществующие** роуты: `/packages`, `/artists`, `/rules`
- Внешний Giphy URL (нестабильно, privacy, лишняя сеть)
- На узких экранах зелёный блок + соцкнопки ломают сетку / тапы
- Нет связи с реальными разделами: `/cases`, `/news`, `/events`, `/guides`, `/login`

### Задачи

1. **Починить ссылки** — только живые routes:

```text
HOME → /
ABOUT → /about
CASES → /cases
NEWS → /news
EVENTS → /events
GUIDES → /guides
LOGIN / CABINET → /login или /dashboard
```

2. **Mobile footer**
   - 1 колонка: бренд → меню (wrap / 2 col grid) → соц/копирайт
   - Уменьшить `text-2xl` меню на mobile до `text-sm`/`text-base`
   - Убрать или упростить GIF-заглушку; локальный webp вместо Giphy

3. **Не путать с fixed bottom nav**
   - Сейчас footer в потоке документа — ок
   - Если нужен sticky bottom bar на mobile: отдельный `MobileTabBar` (Home / Cases / Guides / Login), footer оставить компактным

4. **Доступность**
   - `aria-label` на иконки соцсетей
   - Контраст текста на `#39FF14` фоне (чёрный, не серый)

**Файлы:** `src/components/Footer.vue`, при необходимости `Layout.vue`

---

## 4. Редизайн GuideDetail (страница курса) 🟡 P1

**Сейчас:** отдельный «терминальный» оверлей, визуально ближе к CaseDetail, но не к лендингу Guides; на mobile — max-h 90vh, мелкие зоны тача, слабый Y2K-ритм сайта.

### Целевой UX

- Полноэкранная **страница** (route `/guides/:id`), не только modal-feel
- Стиль как у Home/News: чёрный фон, acid green `#39FF14`, brutal borders, Impact/mono, лёгкий CRT только на desktop
- Структура:
  1. Top bar: back → `/guides` + id курса
  2. Hero: title + meta (level / duration / tags)
  3. Cover / key visual (оптимизированный asset)
  4. Body: секции шагов (accordion на mobile, list на desktop)
  5. CTA: «START» / «DOWNLOAD MATERIALS» (пока UI-only)

### Задачи

1. Переверстать `GuideDetail.vue` под design tokens сайта (те же border/shadow/цвета)
2. Mobile-first: одна колонка, sticky back-button, крупные заголовки через `clamp`
3. Убрать зависимость от огромных фоновых PNG
4. Пропы/данные: единый тип `Guide` в `src/types` + mock в `src/data/guides.ts`
5. Согласовать список на `GuidesPage` с detail (одинаковые id/title)

**Файлы:** `GuideDetail.vue`, `GuidesPage.vue`, `src/data/*`, `router/index.ts`

---

## 5. Header / навигация 🟡 P1

### Задачи

1. Мобильное меню: закрытие по route change, focus trap, `aria-expanded`
2. Активный пункт (`router-link-active`) с acid-underline
3. Не дублировать мёртвые ссылки (как в footer)
4. На desktop — компактный bar, без горизонтального overflow
5. Auth state: показывать LOGIN vs DASHBOARD / role badge

**Файлы:** `Header.vue`

---

## 6. CaseDetail / модалки 🟡 P1

### Задачи

1. На mobile — full-screen sheet (`h-dvh`), body scroll lock
2. Закрытие: X, backdrop, Escape
3. Картинки логотипов — object-contain + лимиты размера
4. Единый паттерн modal с ContractModal (переиспользовать shell)

**Файлы:** `CaseDetail.vue`, `ContractModal.vue`

---

## 7. Консистентность UI / дизайн-система 🟢 P2

1. Вынести токены в CSS variables или Tailwind theme:
   - `--acid: #39FF14`, `--alert: #ff0000`, borders, font stacks
2. Общие компоненты: `AcidButton`, `Panel`, `Tag`, `SectionTitle`
3. Убрать инлайн-дубли hover/shadow классов
4. Единый empty/error state
5. Favicon + `<title>` / meta per route (vue-router + useHead или ручной watch)

---

## 8. Роутинг и мёртвые страницы 🟢 P2

| Ссылка / path | Статус | Действие |
|---------------|--------|----------|
| `/purchase` (Home CTA) | нет route | stub page или scroll/modal «скоро» |
| `/packages`, `/artists`, `/rules` | нет | убрать из footer |
| `/upload` | есть TrackForm | проверить mobile form |
| Auth routes | mock store | не ломать UI при `isAuthenticated === false` |

---

## 9. Кабинеты (artist / moderator / admin) 🟢 P2

- ModeratorCabinet очень тяжёлый (~33KB vue) — split + упростить таблицы на mobile (card list вместо wide table)
- Dashboard — графики/списки релизов в 1 col
- Формы upload: file input + progress, крупные hit-area

---

## 10. Порядок работ (спринты)

### Sprint A — скорость и не ломать телефон (3–5 дней)
1. Сжать/вырезать ассеты (§1.1–1.2)
2. Footer ссылки + mobile layout (§3)
3. Overflow + typography pass (§2.1–2.2)
4. Lazy routes (§1.3)

### Sprint B — страницы и nav (3–5 дней)
1. GuideDetail redesign (§4)
2. Header a11y + active states (§5)
3. CaseDetail mobile sheet (§6)
4. Home CTA `/purchase` stub (§8)

### Sprint C — полировка (2–4 дня)
1. Tokens + AcidButton (§7)
2. Cabinets mobile (§9)
3. Lighthouse pass, фикс CLS/LCP
4. Обновить Pages, прогнать на реальном телефоне

---

## 11. Как работать локально

```bash
git clone https://github.com/lustDSOX/MVP-lable.git
cd MVP-lable
git checkout main
cd frontend/mvp_lable
npm ci
npm run dev
```

После правок — PR в `main`. Push в `main` триггерит деплой на `gh-pages`.

Проверка mobile: DevTools device mode + https://lustdsox.github.io/MVP-lable/

---

## 12. Definition of Done (фронт-MVP UI)

- [ ] Нет горизонтального скролла на 360–430px
- [ ] Footer/header только на существующие routes
- [ ] GuideDetail в стиле сайта, usable на телефоне
- [ ] Главные декоративные ассеты ≤ ~300KB каждый (webp)
- [ ] LCP приемлемый на mid-tier 4G
- [ ] `prefers-reduced-motion` уважается
- [ ] Pages обновлён с `main`
