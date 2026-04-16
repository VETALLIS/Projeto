const canvasBack = document.getElementById('canvas-ondas-back');
const canvasFront = document.getElementById('canvas-ondas-front');
const ctxBack = canvasBack.getContext('2d', { alpha: true });
const ctxFront = canvasFront.getContext('2d', { alpha: true });
const section = document.getElementById('sobre-nos-section');

function resize() {
    canvasBack.width = canvasFront.width = section.offsetWidth;
    canvasBack.height = canvasFront.height = section.offsetHeight;
}
resize();
window.addEventListener('resize', resize);

const waves = [
    { amp: 65, freq: 0.012, offset: 0.0,  alpha: 0.50, width: 3.5 },
    { amp: 65, freq: 0.012, offset: 0.08, alpha: 0.35, width: 2.8 },
    { amp: 65, freq: 0.012, offset: 0.16, alpha: 0.25, width: 4.2 },
    { amp: 65, freq: 0.012, offset: 0.24, alpha: 0.20, width: 2.0 },
];

const SPEED = 0.15;
const FADE_START = 0.35;
const FADE_END = 0.65;
let t = 0;
let animando = true;
let lastTime = 0;
const FPS = 30;
const INTERVALO = 1000 / FPS;

function drawWave(ctx, w, i, showMiddle) {
    ctx.beginPath();
    ctx.strokeStyle = `rgba(255,255,255,${w.alpha})`;
    ctx.lineWidth = w.width;
    ctx.lineJoin = 'round';
    ctx.lineCap = 'round';
    // ❌ shadowBlur removido — era o maior vilão de performance

    const cw = ctx.canvas.width;
    const ch = ctx.canvas.height;
    let penDown = false;

    for (let x = 0; x <= cw; x += 4) { // era x += 2
        const progress = x / cw;
        const arch = ch * (0.80 - progress * 0.60)
            + Math.sin(progress * Math.PI * 1.2) * (ch * 0.18);
        const baseY = arch + (i - 1.5) * 18;
        const y = baseY + Math.sin(x * w.freq + t * SPEED + w.offset) * w.amp;

        const inMiddle = progress > FADE_START && progress < FADE_END;
        const shouldDraw = showMiddle ? inMiddle : !inMiddle;

        if (shouldDraw) {
            if (!penDown) { ctx.moveTo(x, y); penDown = true; }
            else { ctx.lineTo(x, y); }
        } else {
            penDown = false;
        }
    }
    ctx.stroke();
}

function draw(timestamp) {
    if (!animando) return;

    // Throttle para 30fps
    if (timestamp - lastTime < INTERVALO) {
        requestAnimationFrame(draw);
        return;
    }
    lastTime = timestamp;

    ctxBack.clearRect(0, 0, canvasBack.width, canvasBack.height);
    ctxFront.clearRect(0, 0, canvasFront.width, canvasFront.height);

    waves.forEach((w, i) => {
        drawWave(ctxBack, w, i, false);
        drawWave(ctxFront, { ...w, alpha: w.alpha * 0.3 }, i, true);
    });

    t += 0.5;
    requestAnimationFrame(draw);
}

// Pausa quando a seção não está visível na tela
const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
        animando = e.isIntersecting;
        if (animando) requestAnimationFrame(draw);
    });
}, { threshold: 0.1 });

observer.observe(section);
requestAnimationFrame(draw);