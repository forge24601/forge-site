/**
 * Microphone -> 16 kHz mono 16-bit PCM for the FORGE guide (forge-guide.js). Runs on the audio
 * thread: averages the input down to 16 kHz and posts one Int16Array every 100 ms plus its level.
 */
class ForgePcm16k extends AudioWorkletProcessor {
    constructor() {
        super();
        this.ratio = sampleRate / 16000;
        this.acc = 0;
        this.sum = 0;
        this.n = 0;
        this.buf = new Int16Array(1600);
        this.len = 0;
        this.sq = 0;
    }

    process(inputs) {
        const ch = inputs[0] && inputs[0][0];
        if (!ch) {
            return true;
        }
        for (let i = 0; i < ch.length; i++) {
            this.sum += ch[i];
            this.n++;
            this.acc += 1;
            if (this.acc >= this.ratio) {
                this.acc -= this.ratio;
                let v = this.sum / this.n;
                this.sum = 0;
                this.n = 0;
                v = Math.max(-1, Math.min(1, v));
                this.sq += v * v;
                this.buf[this.len++] = v < 0 ? v * 0x8000 : v * 0x7fff;
                if (this.len === this.buf.length) {
                    this.port.postMessage({ pcm: this.buf.slice(0), rms: Math.sqrt(this.sq / this.len) });
                    this.len = 0;
                    this.sq = 0;
                }
            }
        }
        return true;
    }
}

registerProcessor("forge-pcm16k", ForgePcm16k);
