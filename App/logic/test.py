import pyaudio


def test_audio_input_present() -> bool:
    try:
        p = pyaudio.PyAudio()
        for device_id in range(p.get_device_count()):
            device = p.get_device_info_by_index(device_id)
            if "BlackHole 2ch" in device["name"]:
                return True
                
        raise Exception("BlackHole 2ch not found")
    except Exception as e:
        print(e)
        return False

def test_audio_multi_output_active() -> bool:
    
    p = pyaudio.PyAudio()
    if p.get_default_output_device_info()["name"] == "Multi-Output Device":
        return True
    raise Exception("Multi-Output is not set as default")
     



def test_all() -> bool:
    return test_audio_input_present() and test_audio_multi_output_active()