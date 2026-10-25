/**
 * FORGE guide — our own voice player for the FORGE agent (ElevenLabs Agents, public, no server).
 *
 * Why not the ElevenLabs widget: on iPhone it keeps the microphone open while the guide talks
 * (so you can interrupt), which puts iOS into phone-call audio mode, and the guide's voice clicked —
 * with the websocket player and with WebRTC alike, while the stream itself measured clean (2026-10-24).
 * This player closes the microphone whenever the guide speaks and opens it when it is your turn.
 *
 * Protocol: wss://api.elevenlabs.io/v1/convai/conversation?agent_id=… — we send
 * conversation_initiation_client_data, {user_audio_chunk} (16 kHz PCM, from forge-pcm-worklet.js)
 * and {type:'user_message'} for typed questions; we receive audio (PCM), agent_response,
 * user_transcript, interruption, ping.
 */
(function () {
    'use strict';

    var AGENT = 'agent_3101m5ra4phtfs894pc9jkrcdc0h';
    var WS_URL = 'wss://api.elevenlabs.io/v1/convai/conversation?agent_id=' + AGENT;
    var WORKLET = '/js/forge-pcm-worklet.js';

    var T = {
        en: {
            start: 'Start talking', ready: 'Press Start talking and allow the microphone, or type a question.',
            connecting: 'Connecting…', speaking: 'The guide is speaking…', listening: 'Your turn — go ahead and ask.',
            thinking: 'Thinking…', ended: 'Conversation ended. Press Start talking to begin again.',
            micBlocked: 'The microphone is blocked. Allow it in your browser settings, or type your question.',
            error: 'The guide could not connect. Please try again in a moment.',
            stop: 'Skip', end: 'End conversation', you: 'You', guide: 'FORGE guide',
            typePh: 'Or type a question', send: 'Send'
        },
        es: {
            start: 'Empieza a hablar', ready: 'Pulsa Empieza a hablar y permite el micrófono, o escribe una pregunta.',
            connecting: 'Conectando…', speaking: 'La guía está hablando…', listening: 'Tu turno: pregunta lo que quieras.',
            thinking: 'Pensando…', ended: 'La conversación terminó. Pulsa Empieza a hablar para comenzar otra vez.',
            micBlocked: 'El micrófono está bloqueado. Permítelo en los ajustes del navegador o escribe tu pregunta.',
            error: 'La guía no pudo conectarse. Inténtalo de nuevo en un momento.',
            stop: 'Saltar', end: 'Terminar conversación', you: 'Tú', guide: 'Guía de FORGE',
            typePh: 'O escribe una pregunta', send: 'Enviar'
        }
    };

    var S = {
        lang: 'en', ws: null, actx: null, worklet: null, stream: null, src: null, node: null, sink: null,
        sources: [], tEnd: 0, lastAudio: 0, state: 'idle', outRate: 24000, agentBubble: null, timer: null, micAllowed: false
    };
    var $ = function (id) { return document.getElementById(id); };
    var t = function (k) { return (T[S.lang] || T.en)[k]; };

    function ctx() {
        if (S.actx && S.actx.state === 'closed') { S.actx = null; S.worklet = null; }
        if (!S.actx) { S.actx = new (window.AudioContext || window.webkitAudioContext)(); }
        if (S.actx.state !== 'running') { S.actx.resume().catch(function () {}); }
        return S.actx;
    }

    function setState(s, msg) {
        S.state = s;
        $('fg-status').textContent = msg || t({ idle: 'ready', connecting: 'connecting', agent: 'speaking', listening: 'listening', thinking: 'thinking', ended: 'ended' }[s] || 'ready');
        var live = s === 'connecting' || s === 'agent' || s === 'listening' || s === 'thinking';
        $('fg-start').hidden = live;
        $('fg-end').hidden = !live;
        $('fg-stop').hidden = s !== 'agent';
        $('fg-panel').classList.toggle('fg-listening', s === 'listening');
        $('fg-panel').classList.toggle('fg-speaking', s === 'agent');
    }

    function bubble(role, text) {
        var b = document.createElement('div');
        b.className = 'fg-msg fg-' + role;
        var who = document.createElement('span');
        who.className = 'fg-who';
        who.textContent = role === 'user' ? t('you') : t('guide');
        var p = document.createElement('p');
        p.textContent = text;
        b.appendChild(who);
        b.appendChild(p);
        $('fg-log').appendChild(b);
        $('fg-log').hidden = false;
        b.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        return p;
    }

    function b64(u8) {
        var s = '';
        for (var i = 0; i < u8.length; i += 0x8000) { s += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000)); }
        return btoa(s);
    }

    /* ---------------- microphone: open only on your turn ---------------- */

    function openMic() {
        if (S.stream || !S.ws || S.ws.readyState !== 1) { return; }
        var ac = ctx();
        S.worklet = S.worklet || ac.audioWorklet.addModule(WORKLET);
        navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true, channelCount: 1 } })
            .then(function (stream) {
                if (S.state !== 'listening' && S.state !== 'thinking') { stream.getTracks().forEach(function (tr) { tr.stop(); }); return null; }
                S.stream = stream;
                return S.worklet.then(function () {
                    if (!S.stream) { return; }
                    S.src = ac.createMediaStreamSource(stream);
                    S.node = new AudioWorkletNode(ac, 'forge-pcm16k');
                    S.sink = ac.createGain();
                    S.sink.gain.value = 0;
                    S.node.port.onmessage = function (e) {
                        if (S.ws && S.ws.readyState === 1 && S.stream) {
                            S.ws.send(JSON.stringify({ user_audio_chunk: b64(new Uint8Array(e.data.pcm.buffer)) }));
                        }
                        $('fg-ring').style.transform = 'scale(' + (1 + Math.min(e.data.rms * 9, 0.5)).toFixed(3) + ')';
                    };
                    S.src.connect(S.node);
                    S.node.connect(S.sink);
                    S.sink.connect(ac.destination);
                });
            })
            .catch(function (err) {
                setState('listening', err && err.name === 'NotAllowedError' ? t('micBlocked') : t('micBlocked'));
            });
    }

    /** Close the microphone completely (tracks stopped), so the phone leaves call-audio mode. */
    function closeMic() {
        try { if (S.src) { S.src.disconnect(); } } catch (e) { /* gone */ }
        try { if (S.node) { S.node.port.onmessage = null; S.node.disconnect(); } } catch (e) { /* gone */ }
        try { if (S.sink) { S.sink.disconnect(); } } catch (e) { /* gone */ }
        if (S.stream) { S.stream.getTracks().forEach(function (tr) { tr.stop(); }); }
        S.stream = S.src = S.node = S.sink = null;
        $('fg-ring').style.transform = '';
    }

    /* ---------------- the guide's voice ---------------- */

    function playChunk(base64) {
        var ac = ctx();
        var bin = atob(base64);
        var n = bin.length >> 1;
        if (!n) { return; }
        var buf = ac.createBuffer(1, n, S.outRate);
        var ch = buf.getChannelData(0);
        for (var i = 0; i < n; i++) {
            var v = bin.charCodeAt(2 * i) | (bin.charCodeAt(2 * i + 1) << 8);
            ch[i] = (v >= 0x8000 ? v - 0x10000 : v) / 32768;
        }
        var at = Math.max(ac.currentTime + 0.08, S.tEnd);
        var src = ac.createBufferSource();
        src.buffer = buf;
        src.connect(ac.destination);
        src.start(at);
        S.sources.push(src);
        src.onended = function () { S.sources = S.sources.filter(function (x) { return x !== src; }); };
        S.tEnd = at + buf.duration;
        S.lastAudio = Date.now();
    }

    function stopVoice() {
        S.sources.forEach(function (s) { try { s.stop(); } catch (e) { /* ended */ } });
        S.sources = [];
        S.tEnd = 0;
    }

    /** When the guide has finished speaking (all audio played, none arriving), it is your turn. */
    function tick() {
        if (S.state !== 'agent' || !S.actx) { return; }
        if (S.actx.currentTime >= S.tEnd + 0.2 && Date.now() - S.lastAudio > 500) {
            S.agentBubble = null;
            setState('listening');
            openMic();
        }
    }

    /* ---------------- the conversation ---------------- */

    function start(firstText) {
        ctx();
        setState('connecting');
        $('fg-log').hidden = false;
        // ask for the microphone inside the tap, then release it until it is your turn
        if (!S.micAllowed && navigator.mediaDevices && navigator.mediaDevices.getUserMedia && !firstText) {
            navigator.mediaDevices.getUserMedia({ audio: true }).then(function (st) {
                S.micAllowed = true;
                st.getTracks().forEach(function (tr) { tr.stop(); });
            }).catch(function () { /* typed questions still work */ });
        }
        var ws = new WebSocket(WS_URL);
        S.ws = ws;
        ws.onopen = function () {
            var init = { type: 'conversation_initiation_client_data' };
            if (S.lang !== 'en') { init.conversation_config_override = { agent: { language: S.lang } }; }
            ws.send(JSON.stringify(init));
            if (firstText) { ws.send(JSON.stringify({ type: 'user_message', text: firstText })); }
        };
        ws.onmessage = function (ev) {
            var m;
            try { m = JSON.parse(ev.data); } catch (e) { return; }
            var type = m.type;
            if (type === 'conversation_initiation_metadata') {
                var f = (m.conversation_initiation_metadata_event || {}).agent_output_audio_format || 'pcm_24000';
                var r = parseInt(String(f).replace(/\D/g, ''), 10);
                if (r) { S.outRate = r; }
            } else if (type === 'audio') {
                var a = (m.audio_event || {}).audio_base_64;
                if (a && !S.skipping) {
                    if (S.state !== 'agent') { closeMic(); setState('agent'); }
                    playChunk(a);
                }
            } else if (type === 'agent_response') {
                var txt = ((m.agent_response_event || {}).agent_response || '').replace(/\[[a-z ]+\]\s*/gi, '');
                if (txt) {
                    if (S.agentBubble) { S.agentBubble.textContent += ' ' + txt; } else { S.agentBubble = bubble('agent', txt); }
                }
            } else if (type === 'agent_response_correction') {
                var c = (m.agent_response_correction_event || {}).corrected_agent_response;
                if (c && S.agentBubble) { S.agentBubble.textContent = c; }
            } else if (type === 'user_transcript') {
                var u = ((m.user_transcription_event || {}).user_transcript || '').trim();
                if (u && u !== '...') { bubble('user', u); S.agentBubble = null; S.skipping = false; setState('thinking'); }
            } else if (type === 'interruption') {
                stopVoice();
            } else if (type === 'ping') {
                var id = (m.ping_event || {}).event_id;
                setTimeout(function () {
                    if (ws.readyState === 1) { ws.send(JSON.stringify({ type: 'pong', event_id: id })); }
                }, (m.ping_event || {}).ping_ms || 0);
            }
        };
        ws.onerror = function () { if (S.state === 'connecting') { finish(t('error')); } };
        ws.onclose = function () { if (S.ws === ws) { finish(); } };
        clearInterval(S.timer);
        S.timer = setInterval(tick, 100);
    }

    function finish(msg) {
        clearInterval(S.timer);
        closeMic();
        stopVoice();
        var ws = S.ws;
        S.ws = null;
        S.agentBubble = null;
        try { if (ws && ws.readyState <= 1) { ws.close(); } } catch (e) { /* closed */ }
        setState('ended', msg);
    }

    function askTyped(text) {
        if (!S.ws || S.ws.readyState > 1) { bubble('user', text); start(text); return; }
        bubble('user', text);
        S.agentBubble = null;
        S.skipping = false;
        closeMic();
        stopVoice();
        if (S.ws.readyState === 1) { S.ws.send(JSON.stringify({ type: 'user_message', text: text })); }
        setState('thinking');
    }

    /* ---------------- page wiring ---------------- */

    function labels() {
        $('fg-start-label').textContent = t('start');
        $('fg-stop').textContent = t('stop');
        $('fg-end').textContent = t('end');
        $('fg-input').placeholder = t('typePh');
        $('fg-send').textContent = t('send');
        if (S.state === 'idle' || S.state === 'ended') { setState(S.state); }
    }

    window.FORGEGuide = {
        setLang: function (lang) {
            S.lang = lang === 'es' ? 'es' : 'en';
            if (S.ws) { finish(); $('fg-log').textContent = ''; $('fg-log').hidden = true; setState('idle'); }
            labels();
        }
    };

    function init() {
        $('fg-start').addEventListener('click', function () { start(); });
        $('fg-end').addEventListener('click', function () { finish(); });
        $('fg-stop').addEventListener('click', function () {        // skip the rest of this answer
            stopVoice();
            S.lastAudio = 0;
            S.skipping = true;                 // drop the rest of this answer's audio until you speak again
        });
        $('fg-type').addEventListener('submit', function (e) {
            e.preventDefault();
            var v = $('fg-input').value.trim();
            if (!v) { return; }
            ctx();
            $('fg-input').value = '';
            askTyped(v);
        });
        document.addEventListener('visibilitychange', function () { if (document.hidden && S.ws) { finish(); } });
        labels();
        setState('idle');
    }

    if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', init); } else { init(); }
})();
