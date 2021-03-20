from notescribe import UPLOAD_FOLDER, settings, MIDI_FOLDER, LILYPOND_FOLDER
import subprocess
import os.path
import os

def process_file(file_hash, upload_filename) -> bool:
    '''
    Processes a user upload file so that it can be sent to the client
    '''
    print(f'Processing file {upload_filename} with hash {file_hash}')
    
    # Convert to midi
    midi_filename = convert_to_midi(file_hash, upload_filename)
    print(f'midi_filename: {midi_filename}')
    lilypond_filename = convert_to_lilypond(file_hash, midi_filename)
    print(f'lilypond_filename: {lilypond_filename}')
    delete_file_success = delete_file(upload_filename)
    print('upload deleted' if delete_file_success else 'upload failed to be deleted')

    return False

def convert_to_midi(file_hash: str, upload_filename) -> str:
    '''
    Converts a user uploaded file to midi.
    Returns True upon success, False otherwise
    '''
    # TODO: Call machine learning code
    print(f'Converting file {upload_filename} with hash {file_hash}')

    # Return example midi file
    return 'midi_123456789abcdefexample.mid'

def convert_to_lilypond(file_hash: str, midi_filename) -> str:
    filename = os.path.join(MIDI_FOLDER, midi_filename)

    lilypond_path = settings['lilypond_path']
    if not os.path.isdir(os.path.join(LILYPOND_FOLDER)):
        os.makedirs(os.path.join(LILYPOND_FOLDER))

    output_file = os.path.join(LILYPOND_FOLDER, f'midi_{file_hash}.ly')
    subprocess.run(['python', lilypond_path, filename, '-o', output_file])
    return output_file

def delete_file(filename: str) -> bool:
    try:
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        return True
    except:
        return False
