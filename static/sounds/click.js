// Drone UI Sound Engine — Web Audio API, no external files needed
(function () {
  const AudioCtx = window.AudioContext || window.webkitAudioContext;
  if (!AudioCtx) return;

  let ctx = null;
  function getCtx() {
    if (!ctx) ctx = new AudioCtx();
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }

  // ── Sound primitives ────────────────────────────────────────────────────

  function playTone(freq, type, duration, gain, startDelay = 0) {
    const c = getCtx();
    const osc = c.createOscillator();
    const gainNode = c.createGain();
    osc.connect(gainNode);
    gainNode.connect(c.destination);
    osc.type = type;
    osc.frequency.setValueAtTime(freq, c.currentTime + startDelay);
    gainNode.gain.setValueAtTime(gain, c.currentTime + startDelay);
    gainNode.gain.exponentialRampToValueAtTime(0.001, c.currentTime + startDelay + duration);
    osc.start(c.currentTime + startDelay);
    osc.stop(c.currentTime + startDelay + duration + 0.05);
  }

  function playNoise(duration, gain, filterFreq = 2000) {
    const c = getCtx();
    const bufferSize = c.sampleRate * duration;
    const buffer = c.createBuffer(1, bufferSize, c.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) data[i] = Math.random() * 2 - 1;
    const source = c.createBufferSource();
    source.buffer = buffer;
    const filter = c.createBiquadFilter();
    filter.type = 'bandpass';
    filter.frequency.value = filterFreq;
    filter.Q.value = 0.5;
    const gainNode = c.createGain();
    gainNode.gain.setValueAtTime(gain, c.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.001, c.currentTime + duration);
    source.connect(filter);
    filter.connect(gainNode);
    gainNode.connect(c.destination);
    source.start();
    source.stop(c.currentTime + duration);
  }

  // ── Named sounds ─────────────────────────────────────────────────────────

  window.DroneSound = {

    // Soft UI click — used on nav links, buttons
    click() {
      playTone(880, 'sine', 0.08, 0.15);
      playTone(1320, 'sine', 0.06, 0.08, 0.04);
    },

    // Drone card hover/select — propeller spin-up feel
    droneSelect() {
      const c = getCtx();
      const osc = c.createOscillator();
      const gain = c.createGain();
      osc.connect(gain); gain.connect(c.destination);
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(80, c.currentTime);
      osc.frequency.exponentialRampToValueAtTime(320, c.currentTime + 0.25);
      gain.gain.setValueAtTime(0.12, c.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, c.currentTime + 0.3);
      osc.start(); osc.stop(c.currentTime + 0.35);
      // high whine layer
      playTone(2400, 'sine', 0.2, 0.04, 0.1);
    },

    // Buy / order confirmation — success chime
    orderSuccess() {
      [523, 659, 784, 1047].forEach((f, i) => playTone(f, 'sine', 0.3, 0.12, i * 0.08));
    },

    // Repair request submit — mechanical click + beep
    repairSubmit() {
      playNoise(0.05, 0.3, 1200);
      playTone(440, 'square', 0.1, 0.08, 0.06);
      playTone(880, 'sine', 0.15, 0.1, 0.12);
    },

    // Navigation — subtle whoosh
    navigate() {
      const c = getCtx();
      const osc = c.createOscillator();
      const gain = c.createGain();
      osc.connect(gain); gain.connect(c.destination);
      osc.type = 'sine';
      osc.frequency.setValueAtTime(600, c.currentTime);
      osc.frequency.exponentialRampToValueAtTime(200, c.currentTime + 0.12);
      gain.gain.setValueAtTime(0.08, c.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, c.currentTime + 0.15);
      osc.start(); osc.stop(c.currentTime + 0.2);
    },

    // Login success
    loginSuccess() {
      playTone(660, 'sine', 0.15, 0.12);
      playTone(880, 'sine', 0.2, 0.1, 0.1);
    },

    // Error / warning
    error() {
      playTone(220, 'sawtooth', 0.15, 0.15);
      playTone(180, 'sawtooth', 0.2, 0.12, 0.1);
    },
  };

  // ── Auto-attach to elements ───────────────────────────────────────────────

  function attachSounds() {
    // Nav links
    document.querySelectorAll('.nav-link, .navbar-brand').forEach(el => {
      el.addEventListener('click', () => DroneSound.navigate(), { passive: true });
    });

    // Drone cards
    document.querySelectorAll('.drone-card').forEach(el => {
      el.addEventListener('click', () => DroneSound.droneSelect(), { passive: true });
      el.addEventListener('mouseenter', () => {
        const c = getCtx();
        const osc = c.createOscillator();
        const g = c.createGain();
        osc.connect(g); g.connect(c.destination);
        osc.type = 'sine';
        osc.frequency.value = 1800;
        g.gain.setValueAtTime(0.03, c.currentTime);
        g.gain.exponentialRampToValueAtTime(0.001, c.currentTime + 0.06);
        osc.start(); osc.stop(c.currentTime + 0.08);
      }, { passive: true });
    });

    // Buy / order buttons
    document.querySelectorAll('form[action*="buy"] button[type="submit"]').forEach(el => {
      el.addEventListener('click', () => DroneSound.orderSuccess(), { passive: true });
    });

    // Repair submit
    document.querySelectorAll('form button[type="submit"]').forEach(el => {
      if (el.closest('form[action*="repair"]') || el.closest('.repair-form')) {
        el.addEventListener('click', () => DroneSound.repairSubmit(), { passive: true });
      }
    });

    // All other buttons and links
    document.querySelectorAll('.btn:not(.nav-link):not(.navbar-brand)').forEach(el => {
      if (!el.dataset.soundAttached) {
        el.dataset.soundAttached = '1';
        el.addEventListener('click', () => DroneSound.click(), { passive: true });
      }
    });

    // Alerts (success/error feedback)
    document.querySelectorAll('.alert-success').forEach(() => DroneSound.orderSuccess());
    document.querySelectorAll('.alert-danger').forEach(() => DroneSound.error());
  }

  // Run after DOM ready and after any dynamic content
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', attachSounds);
  } else {
    attachSounds();
  }

  // Re-attach after Bootstrap collapse/modal events
  document.addEventListener('shown.bs.collapse', attachSounds);

})();
