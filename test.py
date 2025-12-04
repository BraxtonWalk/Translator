from huggingface_hub import snapshot_download

# Choose a folder to store the model
local_dir = r"C:\Users\Braxton\OneDrive\Desktop\College Classes\CS 385 - Natural Language Processing\FinalProject\WhisperSmall"

# Download the entire repo snapshot
snapshot_download(repo_id="Systran/faster-whisper-small", local_dir=local_dir)
