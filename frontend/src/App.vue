<template>
  <div class="page">
    <!-- HEADER -->
    <header class="header">
      <div class="header-tag">[ OUTIL WEB ]</div>
      <h1 class="header-title">QR CODE<br />GENERATOR</h1>
      <div class="header-line"></div>
    </header>

    <!-- MAIN -->
    <main class="main">
      <!-- INPUT BLOCK -->
      <section class="block input-block">
        <label class="block-label" for="url-input">// ENTREZ VOTRE URL</label>
        <div class="input-row">
          <input
            id="url-input"
            v-model="url"
            @input="onInput"
            type="text"
            class="url-input"
            :class="{ 'input-valid': isValid, 'input-invalid': url && !isValid }"
            placeholder="https://example.com"
            autocomplete="off"
            spellcheck="false"
          />
          <div class="status-badge" :class="statusClass">
            {{ statusLabel }}
          </div>
        </div>

        <button
          id="generate-btn"
          class="btn btn-generate"
          :disabled="!isValid || loading"
          @click="generateQR"
        >
          <span v-if="loading">⏳ GÉNÉRATION...</span>
          <span v-else>▶ GÉNÉRER</span>
        </button>
      </section>

      <!-- ERROR -->
      <div v-if="error" class="error-box">
        ⚠ {{ error }}
      </div>

      <!-- RESULT BLOCK -->
      <section v-if="qrImage" class="block result-block">
        <div class="block-label">// QR CODE GÉNÉRÉ</div>
        <div class="qr-wrapper">
          <img :src="qrImage" alt="QR Code généré" class="qr-image" />
        </div>
        <div class="qr-url">{{ url }}</div>
        <button
          id="download-btn"
          class="btn btn-download"
          @click="downloadQR"
        >
          ↓ TÉLÉCHARGER (.PNG)
        </button>
      </section>
    </main>

    <!-- FOOTER -->
    <footer class="footer">
      <span>WHOZGHIAR — QR CODE GENERATOR</span>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const url = ref('')
const qrImage = ref(null)
const loading = ref(false)
const error = ref(null)

// Regex de validation d'URL — identique à celle du backend (app.py).
//
// Problèmes de l'ancienne regex (reprise de main.py) :
//   1. Elle refusait les tirets dans les domaines (ex: portefolio-kimberleyanique)
//   2. Elle ne gérait pas les sous-domaines multiples (ex: .my.canva.site)
//
// Nouvelle regex :
//   ^(https?://)?          → protocole optionnel
//   (([a-zA-Z0-9\-]+\.)+   → un ou plusieurs labels avec tirets + point
//   [a-zA-Z]{2,})          → TLD d'au moins 2 lettres
//   ([/?#].*)?$            → chemin / query / fragment optionnel
const URL_REGEX = /^(https?:\/\/)?(([a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,})([/?#].*)?$/

const isValid = computed(() => URL_REGEX.test(url.value.trim()) && url.value.trim().length > 0)

const statusLabel = computed(() => {
  if (!url.value) return '○ EN ATTENTE'
  return isValid.value ? '✓ VALIDE' : '✗ INVALIDE'
})

const statusClass = computed(() => {
  if (!url.value) return 'status-idle'
  return isValid.value ? 'status-ok' : 'status-error'
})

function onInput() {
  qrImage.value = null
  error.value = null
}

async function generateQR() {
  if (!isValid.value) return
  loading.value = true
  error.value = null
  qrImage.value = null

  try {
    const res = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: url.value.trim() })
    })
    const data = await res.json()
    if (!res.ok) {
      error.value = data.error || 'Erreur lors de la génération'
    } else {
      qrImage.value = data.image
    }
  } catch (e) {
    error.value = 'Impossible de contacter le serveur. Vérifiez que le backend Flask est démarré.'
  } finally {
    loading.value = false
  }
}

function downloadQR() {
  if (!qrImage.value) return
  const a = document.createElement('a')
  a.href = qrImage.value
  a.download = 'qrcode.png'
  a.click()
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--white);
}

/* ── HEADER ── */
.header {
  padding: 2.5rem 2rem 1.5rem;
  border-bottom: var(--border);
  background: var(--black);
  color: var(--white);
  position: relative;
}

.header-tag {
  font-size: 0.75rem;
  letter-spacing: 0.2em;
  opacity: 0.6;
  margin-bottom: 0.75rem;
}

.header-title {
  font-size: clamp(2.5rem, 6vw, 4.5rem);
  font-weight: 700;
  line-height: 1;
  letter-spacing: -0.02em;
}

.header-line {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: var(--yellow);
}

/* ── MAIN ── */
.main {
  flex: 1;
  padding: 3rem 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  max-width: 720px;
  margin: 0 auto;
  width: 100%;
}

/* ── BLOCKS ── */
.block {
  width: 100%;
  border: var(--border);
  padding: 2rem;
  box-shadow: var(--shadow);
  background: var(--white);
}

.block-label {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.15em;
  opacity: 0.5;
  margin-bottom: 1.25rem;
}

/* ── INPUT ── */
.input-row {
  display: flex;
  align-items: stretch;
  gap: 0;
  margin-bottom: 1.5rem;
  border: var(--border);
  box-shadow: var(--shadow);
}

.url-input {
  flex: 1;
  padding: 0.9rem 1rem;
  font-family: var(--font);
  font-size: 0.95rem;
  border: none;
  outline: none;
  background: var(--white);
  color: var(--black);
  min-width: 0;
}

.url-input::placeholder {
  opacity: 0.3;
}

.url-input.input-valid {
  background: #f0fff0;
}

.url-input.input-invalid {
  background: #fff0f0;
}

.status-badge {
  padding: 0.9rem 1rem;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  white-space: nowrap;
  border-left: var(--border);
  display: flex;
  align-items: center;
}

.status-idle {
  background: #eee;
  color: #666;
}

.status-ok {
  background: var(--yellow);
  color: var(--black);
}

.status-error {
  background: var(--red);
  color: var(--white);
}

/* ── BUTTONS ── */
.btn {
  font-family: var(--font);
  font-weight: 700;
  font-size: 0.95rem;
  letter-spacing: 0.1em;
  padding: 0.85rem 2rem;
  border: var(--border);
  cursor: pointer;
  transition: transform 0.08s ease, box-shadow 0.08s ease;
  box-shadow: var(--shadow);
}

.btn:active:not(:disabled) {
  transform: translate(3px, 3px);
  box-shadow: 2px 2px 0 var(--black);
}

.btn-generate {
  background: var(--yellow);
  color: var(--black);
  width: 100%;
}

.btn-generate:disabled {
  background: #ddd;
  color: #999;
  cursor: not-allowed;
  box-shadow: none;
}

.btn-download {
  background: var(--black);
  color: var(--white);
  margin-top: 1.5rem;
  width: 100%;
}

/* ── ERROR ── */
.error-box {
  width: 100%;
  border: 3px solid var(--red);
  background: #fff0f0;
  padding: 1rem 1.5rem;
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--red);
  box-shadow: 5px 5px 0 var(--red);
}

/* ── RESULT ── */
.qr-wrapper {
  display: flex;
  justify-content: center;
  margin: 1.5rem 0 1rem;
  border: var(--border);
  box-shadow: var(--shadow);
  padding: 1.5rem;
  background: white;
}

.qr-image {
  width: 220px;
  height: 220px;
  image-rendering: pixelated;
}

.qr-url {
  font-size: 0.8rem;
  word-break: break-all;
  opacity: 0.5;
  text-align: center;
  margin-bottom: 0.5rem;
}

/* ── FOOTER ── */
.footer {
  border-top: var(--border);
  padding: 1rem 2rem;
  font-size: 0.7rem;
  letter-spacing: 0.2em;
  opacity: 0.4;
  text-align: center;
  background: var(--white);
}
</style>
