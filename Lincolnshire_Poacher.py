import numpy as np
from scipy.io import wavfile

# function that generates the first two bars of Lincolnshire Poacher and repeats it twice
# outputs a wav file
def generate_song(filename='lincolnshire_poacher.wav', repeats=2, sample_rate=44100):
    notes = [
        (293.66, 0.1), # D
        (392.00, 0.1), # G
        (392.00, 0.1), # G
        (392.00, 0.1), # G
        (392.00, 0.2), # G extra note
        (369.99, 0.2), # F#
        (329.63, 0.17),# E
        (293.66, 0.4), # D
        (261.63, 0.2), # C
        (246.94, 0.35),# B
        (293.66, 0.1), # D
        (392.00, 0.15),# G
        (000.00, 0.1),
        (392.00, 0.1), # G
        (440.00, 0.15),# A
        (000.00, 0.1),
        (369.99, 0.1), # F#
        (392.00, 0.5), # G

        (000.00, 0.3), # rest
    ]

    audio = np.array([], dtype=np.float32)

    attack_time = 0.005   # 5 ms
    release_time = 0.015  # 15 ms

    for _ in range(repeats):
        for i, (freq, duration) in enumerate(notes):

            # tuning temp and pitch of song, optional
            duration *= 1.15
            #freq *= 1.06

            total_samples = int(sample_rate * duration)
            t = np.linspace(0, duration, total_samples, endpoint=False)
            note = 0.5 * np.sin(2 * np.pi * freq * t)
            
            # decay envelope
            decay_envelope = np.exp(-t * 4.5) * 0.7 + 0.3
            
            attack_samples = int(attack_time * sample_rate)
            release_samples = int(release_time * sample_rate)
            
            # apply attack sustain release
            if total_samples > attack_samples + release_samples:
                attack = np.linspace(0, 1, attack_samples)
                sustain = np.ones(total_samples - attack_samples - release_samples)
                release = np.linspace(1, 0, release_samples)
                ar_envelope = np.concatenate((attack, sustain, release))
            else:
                # fallback if note is too short
                ar_envelope = np.bartlett(total_samples) 
                
            # apply decay
            note *= decay_envelope * ar_envelope
            audio = np.concatenate((audio, note))

            # slurred notes
            if freq == 0 or i == 4 or i == 5 or i == 6 or i == 7 or i == 8 or i == 9 or i == 15:
                pass 
            else:
                # small gap between notes
                gap = np.zeros(int(sample_rate * 0.1), dtype=np.float32)
                audio = np.concatenate((audio, gap))

    # normalize to 16 bit
    audio_int16 = np.int16(audio * 32767)
        
    # save audio to file
    wavfile.write(filename, sample_rate, audio_int16)

    return filename

if __name__ == "__main__":
    filename = generate_song()
    print(f"Generated {filename}")