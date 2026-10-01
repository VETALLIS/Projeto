const canvasBack = document.getElementById('canvas-ondas-back'); //ondas de trás
const canvasFront = document.getElementById('canvas-ondas-front'); //ondas da frente
const ctxBack = canvasBack.getContext('2d', { alpha: true });// define se é 2d as ondas
const ctxFront = canvasFront.getContext('2d', { alpha: true });// define se é 2d as ondas
const section = document.getElementById('sobre-nos-section'); //seção onde as ondas vão ficar

//faz as duas ondas ondas terem o mesmo tamanho
function resize() {
    canvasBack.width = canvasFront.width = section.offsetWidth;
    canvasBack.height = canvasFront.height = section.offsetHeight;
}
resize();//ajusta ao carregar
window.addEventListener('resize', resize);
//configura as ondas
const waves = [
    { amp: 65, freq: 0.012, offset: 0.0,  alpha: 0.50, width: 3.5 }, //amp = amplitude da onda
    { amp: 65, freq: 0.012, offset: 0.08, alpha: 0.35, width: 2.8 }, // freq = frequência da onda, ou seja, as ondulações do canva
    { amp: 65, freq: 0.012, offset: 0.16, alpha: 0.25, width: 4.2 }, // alpha = transparência
    { amp: 65, freq: 0.012, offset: 0.24, alpha: 0.20, width: 2.0 }, // offset = defasagem entre as ondas, width = a largura da onda
];

const SPEED = 0.15;
const FADE_START = 0.35;
const FADE_END = 0.65;
let t = 0;
let animando = true;
let lastTime = 0;
const FPS = 30;
const INTERVALO = 1000 / FPS;

// Desenha a onda, ctx - como desenhar, w- informações da onda, showMiddle - desenha somente o meio, i - indíce da onda
function drawWave(ctx, w, i, showMiddle) {
    ctx.beginPath();
    ctx.strokeStyle = `rgba(255,255,255,${w.alpha})`; //branco com transparência
    ctx.lineWidth = w.width;
    ctx.lineJoin = 'round'; //cantos arredondados
    ctx.lineCap = 'round'; // pontas arrendodadas

    const cw = ctx.canvas.width;
    const ch = ctx.canvas.height;
    let penDown = false; //indica se está desenhando

    //Percorre a largura em passos de 4px
    for (let x = 0; x <= cw; x += 4) { // era x += 2
        const progress = x / cw;

        // Curva base (arco): começa baixa à esquerda e sobe para a direita,
        // com uma leve curvatura dada por um seno
        const arch = ch * (0.80 - progress * 0.60)
            + Math.sin(progress * Math.PI * 1.2) * (ch * 0.18);

        //Separa verticamente as ondas
        const baseY = arch + (i - 1.5) * 18;

        // Posição final: curva base + oscilação senoidal que se move com o tempo
        const y = baseY + Math.sin(x * w.freq + t * SPEED + w.offset) * w.amp;

        //Verifica se o ponto está no meio
        const inMiddle = progress > FADE_START && progress < FADE_END;

        // se showMiddle for ShowMiddle desenha o meio, se não ao redor
        const shouldDraw = showMiddle ? inMiddle : !inMiddle;

        if (shouldDraw) {
            if (!penDown) { ctx.moveTo(x, y); penDown = true; } //começa a desenhar
            else { ctx.lineTo(x, y); }
        } else {
            penDown = false; //para de escrever
        }
    }
    ctx.stroke(); //desenha a linha
}

function draw(timestamp) {
    if (!animando) return;

    // Throttle para 30fps
    if (timestamp - lastTime < INTERVALO) {
        // Limita a 30fps: se passou pouco tempo desde o último frame, espera
        requestAnimationFrame(draw);
        return;
    }
    lastTime = timestamp;
    //Limpa as duas ondas antes de redesenhar
    ctxBack.clearRect(0, 0, canvasBack.width, canvasBack.height);
    ctxFront.clearRect(0, 0, canvasFront.width, canvasFront.height);

    waves.forEach((w, i) => {
        drawWave(ctxBack, w, i, false);
        drawWave(ctxFront, { ...w, alpha: w.alpha * 0.3 }, i, true);
    });

    t += 0.5; // avança a onda e o tempo também
    requestAnimationFrame(draw);//agenda o próximo frame
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


// Local Storage
function salvarLogin() {
    const email = document.getElementById("email").value; //pega o email
    const senha = document.getElementById("senha"). value //pega a senha

    const dados = {
        email: email,
        senha: senha
    }
}



