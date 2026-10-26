/**
 * Videos play as normal media (the iPhone's media route: AirPods, car, speaker as chosen), never on a
 * voice-call route left over from the Ask about FORGE guide. BT 2026-10-25: a Session Media video jumped
 * from AirPods to the phone speaker.
 */
(function () {
    'use strict';
    if (!('audioSession' in navigator)) { return; }
    document.addEventListener('play', function (e) {
        if (!e.target || e.target.tagName !== 'VIDEO') { return; }
        try { if (navigator.audioSession.type !== 'playback') { navigator.audioSession.type = 'playback'; } } catch (err) { /* older browsers */ }
    }, true);
}());
