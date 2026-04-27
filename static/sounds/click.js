// Minimal UI click sound — used globally on buttons
(function () {
  const AC = window.AudioContext || window.webkitAudioContext;
  if (!AC) return;
  let ctx = null;
  function getCtx() {
    if (!ctx) ctx = new AC();
    if (ctx.state === 'suspended') ctx.resume();
    return ctx;
  }

  window.DroneSound = {
    click() {
      const c = getCtx();
      const o = c.createOscillator();
      const g = c.createGain();
      o.connect(g); g.connect(c.destination);
      o.type = 'sine'; o.frequency.value = 1000;
      g.gain.setValueAtTime(0.06, c.currentTime);
      g.gain.exponentialRampToValueAtTime(0.001, c.currentTime + 0.07);
      o.start(); o.stop(c.currentTime + 0.08);
    }
  };

  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.btn').forEach(btn => {
      btn.addEventListener('click', () => window.DroneSound && window.DroneSound.click(), { passive: true });
    });
  });
})();
