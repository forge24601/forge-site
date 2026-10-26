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

    /**
     * Mic modes (BT 2026-10-24, iPhone): 'close' = mic closed while the guide talks (no clicks, but iOS
     * then plays through the earpiece: too quiet even at max volume); 'open-raw' = mic stays open all
     * conversation with echo cancellation / noise suppression / auto gain OFF (keeps the loudspeaker;
     * the clicks came from the call-audio processing) and nothing is sent while the guide talks;
     * 'open-aec' = mic open with processing ON (the widget's behaviour). Pick with ?mic=…
     */
    var MIC_MODE = (function () {
        var m = new URLSearchParams(location.search).get('mic');
        // BT 2026-10-24 on iPhone: 'open-aec' was loud AND click-free -> the default
        return m === 'open-raw' || m === 'open-aec' || m === 'close' ? m : 'open-aec';
    })();

    var S = {
        lang: 'en', ws: null, actx: null, worklet: null, stream: null, src: null, node: null, sink: null,
        sources: [], tEnd: 0, lastAudio: 0, state: 'idle', outRate: 24000, agentBubble: null, timer: null, micAllowed: false
    };
    var $ = function (id) { return document.getElementById(id); };
    var t = function (k) { return (T[S.lang] || T.en)[k]; };

    /**
     * iPhone: with the microphone closed, Safari puts web audio in the "ambient" category, which the
     * silent switch mutes — the guide went silent (BT 2026-10-24, phone on silent). Declare "playback"
     * while the guide talks and "play-and-record" only while the mic is open (Safari 16.4+ Audio Session API).
     */
    function audioSession(type) {
        try { if (navigator.audioSession && navigator.audioSession.type !== type) { navigator.audioSession.type = type; } } catch (e) { /* older browsers */ }
    }

    function ctx() {
        if (S.actx && S.actx.state === 'closed') { S.actx = null; S.worklet = null; S.out = null; }
        if (!S.actx) { S.actx = new (window.AudioContext || window.webkitAudioContext)(); }
        if (S.actx.state !== 'running') { S.actx.resume().catch(function () {}); }
        return S.actx;
    }

    /**
     * The guide's output chain: +6 dB with a limiter (the agent's speech averages about -22 dBFS) and,
     * with ?route=media, out through an <audio> element (a media player's route and volume) instead of
     * straight to the speakers. BT 2026-10-24: "really quiet" on iPhone after the mic had been used.
     */
    // BT 2026-10-24: the media route was louder on iPhone, so it is now the default (?route=direct = old way)
    var ROUTE_MEDIA = new URLSearchParams(location.search).get('route') !== 'direct';
    function out() {
        var ac = ctx();
        if (S.out) { return S.out; }
        // speech arrives around -22 dBFS: +12 dB into a limiter brings it to normal media loudness
        // ("louder, but not loud enough" at +6 dB) without clipping
        var gain = ac.createGain();
        gain.gain.value = 4.0;
        var comp = ac.createDynamicsCompressor();
        comp.threshold.value = -9; comp.knee.value = 2; comp.ratio.value = 20;
        comp.attack.value = 0.002; comp.release.value = 0.15;
        gain.connect(comp);
        if (ROUTE_MEDIA && ac.createMediaStreamDestination) {
            var dest = ac.createMediaStreamDestination();
            comp.connect(dest);
            var el = new Audio();
            el.autoplay = true;
            el.setAttribute('playsinline', '');
            el.srcObject = dest.stream;
            el.play().catch(function () {});
            S.mediaEl = el;
        } else {
            comp.connect(ac.destination);
        }
        S.out = gain;
        return gain;
    }

    /** Let go of the sound output entirely (tab hidden or page left); out() rebuilds it on next use. */
    function releaseOutput() {
        stopVoice();
        if (S.mediaEl) { try { S.mediaEl.pause(); S.mediaEl.srcObject = null; } catch (e) { /* gone */ } S.mediaEl = null; }
        if (S.out) { try { S.out.disconnect(); } catch (e) { /* gone */ } S.out = null; }
        if (S.actx && S.actx.state === 'running') { S.actx.suspend().catch(function () {}); }
        audioSession('auto');
    }

    /**
     * Rebuild the output after the mic switches ON: on iPhone, sound started before capture began stays
     * on the quiet route afterwards ("loud until I clicked on the prompt to allow the mic", BT 2026-10-24).
     * A new <audio> element may start on its own while the page is capturing (WebKit autoplay rule).
     */
    function rebuildOutput() {
        if (S.mediaEl) { try { S.mediaEl.pause(); S.mediaEl.srcObject = null; } catch (e) { /* gone */ } S.mediaEl = null; }
        if (S.out) { try { S.out.disconnect(); } catch (e) { /* gone */ } S.out = null; }
        // no suspend/resume here: outside a tap iPhone may refuse the resume and leave the page's audio
        // paused — the guide then never "finishes" and the mic never gets its turn (BT 2026-10-24,
        // "I hear the Spanish but it doesn't hear me")
        if (S.actx && S.actx.state !== 'running') { S.actx.resume().catch(function () {}); }
        out();
    }

    /** After the mic closes, make the phone re-pick the loudspeaker (suspend + resume re-routes). */
    function reroute() {
        if (!S.actx) { return; }
        var ac = S.actx;
        ac.suspend().then(function () { return ac.resume(); }).catch(function () { ac.resume().catch(function () {}); });
        if (S.mediaEl) { S.mediaEl.play().catch(function () {}); }
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
        if (S.stream || S.micOpening || !S.ws || S.ws.readyState > 1) { return; }
        S.micOpening = true;
        audioSession('play-and-record');
        var ac = ctx();
        S.worklet = S.worklet || ac.audioWorklet.addModule(WORKLET);
        var processing = MIC_MODE !== 'open-raw';
        navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: processing, noiseSuppression: processing, autoGainControl: processing, channelCount: 1 } })
            .then(function (stream) {
                S.micOpening = false;
                if (MIC_MODE === 'close' && S.state !== 'listening' && S.state !== 'thinking') { stream.getTracks().forEach(function (tr) { tr.stop(); }); return null; }
                S.stream = stream;
                rebuildOutput();
                return S.worklet.then(function () {
                    if (!S.stream) { return; }
                    S.src = ac.createMediaStreamSource(stream);
                    S.node = new AudioWorkletNode(ac, 'forge-pcm16k');
                    S.sink = ac.createGain();
                    S.sink.gain.value = 0;
                    S.node.port.onmessage = function (e) {
                        // send only on your turn (the open modes keep the mic running while the guide talks)
                        if (S.ws && S.ws.readyState === 1 && S.stream && (S.state === 'listening' || S.state === 'thinking')) {
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
                S.micOpening = false;
                setState('listening', err && err.name === 'NotAllowedError' ? t('micBlocked') : t('micBlocked'));
            });
    }

    /** Close the microphone completely (tracks stopped), so the phone leaves call-audio mode. */
    /** In the open modes the mic stays on until the conversation ends (finish() calls closeMic(true)). */
    function pauseMic() {
        if (MIC_MODE === 'close') { closeMic(); }
    }

    function closeMic() {
        try { if (S.src) { S.src.disconnect(); } } catch (e) { /* gone */ }
        try { if (S.node) { S.node.port.onmessage = null; S.node.disconnect(); } } catch (e) { /* gone */ }
        try { if (S.sink) { S.sink.disconnect(); } } catch (e) { /* gone */ }
        if (S.stream) { S.stream.getTracks().forEach(function (tr) { tr.stop(); }); }
        S.stream = S.src = S.node = S.sink = null;
        $('fg-ring').style.transform = '';
        audioSession('playback');
        reroute();
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
        src.connect(out());
        src.start(at);
        S.sources.push(src);
        src.onended = function () { S.sources = S.sources.filter(function (x) { return x !== src; }); };
        S.tEnd = at + buf.duration;
        S.lastAudio = Date.now();
        S.wallEnd = Math.max(S.wallEnd || 0, Date.now() + (at - ac.currentTime + buf.duration) * 1000);
    }

    function stopVoice() {
        S.sources.forEach(function (s) { try { s.stop(); } catch (e) { /* ended */ } });
        S.sources = [];
        S.tEnd = 0;
        S.wallEnd = 0;
    }

    /** When the guide has finished speaking (all audio played, none arriving), it is your turn. */
    function tick() {
        // the mic stays on through the conversation: end it after 90 s of nobody speaking
        if (S.state === 'listening' && S.listenSince && Date.now() - S.listenSince > 90000) { finish(); return; }
        if (S.state !== 'agent' || !S.actx) { return; }
        if (S.actx.state !== 'running') { S.actx.resume().catch(function () {}); }
        var audioDone = S.actx.currentTime >= S.tEnd + 0.2;
        var wallDone = Date.now() > (S.wallEnd || 0) + 400;      // if the audio clock is stuck
        if ((audioDone || wallDone) && Date.now() - S.lastAudio > 500) {
            S.agentBubble = null;
            setState('listening');
            S.listenSince = Date.now();
            if (S.actx.state !== 'running') { S.actx.resume().catch(function () {}); }
            openMic();
        }
    }

    /* ---------------- the conversation ---------------- */

    function start(firstText) {
        audioSession('playback');
        ctx();
        out();                                   // build the output chain (and start the media element) inside the tap
        setState('connecting');
        $('fg-log').hidden = false;
        // ask for the microphone inside the tap, then release it until it is your turn
        if (MIC_MODE !== 'close' && !firstText) { S.micAllowed = true; }      // opened when the socket opens
        else if (!S.micAllowed && navigator.mediaDevices && navigator.mediaDevices.getUserMedia && !firstText) {
            audioSession('play-and-record');
            navigator.mediaDevices.getUserMedia({ audio: true }).then(function (st) {
                S.micAllowed = true;
                st.getTracks().forEach(function (tr) { tr.stop(); });
                audioSession('playback');
                reroute();
            }).catch(function () { audioSession('playback'); /* typed questions still work */ });
        }
        var ws = new WebSocket(WS_URL);
        S.ws = ws;
        ws.onopen = function () {
            var init = { type: 'conversation_initiation_client_data' };
            if (S.lang !== 'en') { init.conversation_config_override = { agent: { language: S.lang } }; }
            ws.send(JSON.stringify(init));
            if (firstText) { ws.send(JSON.stringify({ type: 'user_message', text: firstText })); }
            if (MIC_MODE !== 'close' && !firstText) { openMic(); }
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
                    if (S.state !== 'agent') { pauseMic(); setState('agent'); }
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
        pauseMic();
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
            audioSession('playback');
            askTyped(v);
        });
        // leaving the tab or the page ends the conversation AND lets go of the sound output: a hidden tab that
        // keeps its <audio> media route playing can take the iPhone's audio away from a video in another tab
        // (BT 2026-10-25: Session Media video jumped from AirPods to the phone speaker)
        document.addEventListener('visibilitychange', function () { if (document.hidden) { if (S.ws) { finish(); } releaseOutput(); } });
        window.addEventListener('pagehide', function () { if (S.ws) { finish(); } releaseOutput(); });
        labels();
        setState('idle');
    }

    if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', init); } else { init(); }
})();
