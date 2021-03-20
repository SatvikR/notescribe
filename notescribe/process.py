def process_file(file_hash, upload_filename) -> bool:
    '''
    Processes a user upload file so that it can be sent to the client
    '''
    print(f'Processing file {upload_filename} with hash {file_hash}')
    
    # Convert to midi
    midi_filename = convert_to_midi(file_hash, upload_filename)
    print(f'midi_filename: {midi_filename}')

    return False

def convert_to_midi(file_hash: str, filename) -> str:
    '''
    Converts a user uploaded file to midi.
    Returns True upon success, False otherwise
    '''
    # TODO: Call machine learning code
    print(f'Converting file {filename} with hash {file_hash}')

    # Return example midi file
    return 'midi_123456789abcdefexample.mid'
