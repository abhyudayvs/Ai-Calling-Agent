import audioop

def mulaw_to_pcm(audio_bytes):
    """
    Converts telephone-quality audio (mulaw) to 
    computer-quality audio (pcm) so AI can understand it.
    """
    # 2 is the sample width (16-bit)
    return audioop.ulaw2lin(audio_bytes, 2)

def pcm_to_mulaw(audio_bytes):
    """
    Converts AI audio (pcm) back to telephone audio (mulaw)
    so the user can hear it on their phone.
    """
    # 2 is the sample width (16-bit)
    return audioop.lin2ulaw(audio_bytes, 2)