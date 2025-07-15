import os
import subprocess

def convert_m4a_to_wav():
    """Convierte todos los archivos m4a de la carpeta audios a formato wav"""
    # Crear una carpeta para los archivos WAV si no existe
    os.makedirs("audios_wav", exist_ok=True)
    
    # Buscar todos los archivos m4a en la carpeta audios
    audio_files = [f for f in os.listdir("audios") if f.endswith(".m4a")]
    
    print(f"Se encontraron {len(audio_files)} archivos de audio para convertir...")
    
    # Convertir cada archivo m4a a wav
    for audio_file in audio_files:
        input_path = os.path.join("audios", audio_file)
        output_path = os.path.join("audios_wav", audio_file.replace(".m4a", ".wav"))
        
        # Usar ffmpeg para convertir
        cmd = ["ffmpeg", "-i", input_path, "-y", output_path]
        print(f"Convirtiendo {audio_file}...")
        
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error al convertir {audio_file}: {e}")
    
    print("Conversión completada.")

if __name__ == "__main__":
    convert_m4a_to_wav()
