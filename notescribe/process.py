from notescribe import settings, UPLOAD_FOLDER, WAV_FOLDER, MIDI_FOLDER, LILYPOND_FOLDER, IMAGES_FOLDER, JSON_FOLDER
from notescribe.s3_upload import upload_file, get_url
from pydub import AudioSegment
import subprocess
import os.path
import os
import json
import hashlib
from typing import List
import shutil

def process_file(file_hash, upload_filename) -> str:
    '''
    Processes a user uploaded file so that it can be sent to the client
    :param file_hash: SHA-1 hash of the user uploaded file
    :param upload_filename: Filename (excluding path) of the user uploaded file
    :returns: URL to the json document containing locations of media assets, or None if audio decoding fails
    '''
    print(f'Processing file {upload_filename} with hash {file_hash}')
    try:
        wav_filename = convert_to_wav(file_hash, upload_filename, 'mp3')
    except Exception as e:
        print(e)
        return None
    midi_filename = convert_to_midi(file_hash, wav_filename)
    lilypond_filename = convert_to_lilypond(file_hash, midi_filename)
    image_folder = generate_images(file_hash, lilypond_filename)
    midi_url = upload_midi(file_hash, midi_filename)
    image_urls = process_images(image_folder)
    json_data = {
        "midi_url": midi_url,
        "image_urls": image_urls
    }
    json_url = package_json(file_hash, json_data)

    for f in [
        os.path.join(UPLOAD_FOLDER, upload_filename),
        os.path.join(WAV_FOLDER, wav_filename),
        os.path.join(MIDI_FOLDER, midi_filename),
        os.path.join(LILYPOND_FOLDER, lilypond_filename)
    ]:
        delete_file(f)

    return json_url

def convert_to_wav(file_hash: str, upload_filename: str, input_format: str) -> str:
    '''
    Converts a user uploaded file to WAV format.
    :param file_hash: SHA-1 hash of the user uploaded file
    :param upload_filename: Filename (excluding path) of the user uploaded file
    :param input_format: The audio format (e.g. "mp3") to convert
    :return: Filename (excluding path) of the newly created wav file
    '''
    if not os.path.isdir(os.path.join(WAV_FOLDER)):
        os.makedirs(os.path.join(WAV_FOLDER))

    path_to_input = os.path.join(UPLOAD_FOLDER, upload_filename)
    output_filename = f'wav_{file_hash}.wav'
    path_to_output = os.path.join(WAV_FOLDER, output_filename)
    
    input_audio = AudioSegment.from_file(path_to_input, format=input_format)
    input_audio.export(path_to_output, format="wav")
    
    return output_filename

def convert_to_midi(file_hash: str, wav_filename: str) -> str:
    '''
    Converts a wav file to midi.
    :param file_hash: SHA-1 hash of the user uploaded file
    :param wav_filename: Filename (excluding path) of the wav file to convert
    :returns: Filename (excluding path) of the newly created midi file
    '''
    # TODO: Call machine learning code
    print(f'Converting file {wav_filename} with hash {file_hash}')

    path_to_input = os.path.join(UPLOAD_FOLDER, wav_filename)
    output_filename = f'midi_{file_hash}.mid'
    path_to_output = os.path.join(MIDI_FOLDER, output_filename)

    # Returns a placeholder midi file
    path_to_placeholder = os.path.join('object_storage', 'placeholder', 'placeholder.mid')
    shutil.copyfile(path_to_placeholder, path_to_output)

    # Return example midi file
    return output_filename

def convert_to_lilypond(file_hash: str, midi_filename: str) -> str:
    '''
    Converts a midi file to lilypond.
    :param file_hash: SHA-1 hash of the user uploaded file
    :param upload_filename: Filename (excluding path) of the midi file to convert
    :returns: Filename (excluding path) of the newly created lilypond file
    '''
    filename = os.path.join(MIDI_FOLDER, midi_filename)

    lilypond_converter_path = settings['lilypond_converter_path']
    if not os.path.isdir(os.path.join(LILYPOND_FOLDER)):
        os.makedirs(os.path.join(LILYPOND_FOLDER))

    output_filename = f'lilypond_{file_hash}.ly'
    output_file = os.path.join(LILYPOND_FOLDER, output_filename) 
    subprocess.run(['python', lilypond_converter_path, filename, '-o', output_file])
    return output_filename

def generate_images(file_hash: str, lilypond_filename: str) -> str:
    '''
    Converts a lilypond file to a set of images.
    :param file_hash: SHA-1 hash of the user uploaded file
    :param upload_filename: Filename (excluding path) of the lilypond file to convert
    :returns: Path to the directory where images are stored
    '''
    lilypond_path = settings['lilypond_path']
    output_dir = os.path.join(IMAGES_FOLDER, file_hash)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    subprocess.run([lilypond_path, '-fpng', '-o', output_dir, os.path.join(LILYPOND_FOLDER, lilypond_filename)])

    # Remove extra copy of midi file that lilypond generates automatically
    delete_file(os.path.join(output_dir, lilypond_filename[:-3] + '.mid'))

    return output_dir

def process_images(image_directory_path: str) -> List[str]:
    '''
    Uploads and deletes local copies of the images in the directory
    :param image_directory_path: Path to the directory where the images are stored
    :returns: List of image urls
    '''
    image_filenames = os.listdir(image_directory_path)
    image_urls = []
    for image in image_filenames:
        path_to_image = os.path.join(image_directory_path, image)
        image_hash = None
        with open(path_to_image, 'rb') as f:
           image_hash = hashlib.sha1(f.read()).hexdigest()
        s3_object_name = f'images/{image_hash}.png'
        upload_file(path_to_image, s3_object_name, True)
        delete_file(path_to_image)
        image_urls.append(get_url(s3_object_name))
    os.rmdir(image_directory_path)
    return image_urls

def upload_midi(file_hash: str, midi_filename: str) -> str:
    '''
    Uploads a midi file to S3
    :param midi_filename: Filename (excluding path) of the midi file to upload
    :returns: S3 url of midi file
    '''
    filename = os.path.join(MIDI_FOLDER, midi_filename)
    s3_object_name = f'midi/{file_hash}.mid'
    upload_file(filename, s3_object_name, True)
    return get_url(s3_object_name)

def package_json(file_hash: str, data: json) -> str:
    '''
    Uploads json data to S3
    :param file_hash: SHA-1 hash of the user uploaded file
    :param data: JSON data to upload
    :returns: URL to uploaded json data
    '''
    if not os.path.isdir(os.path.join(JSON_FOLDER)):
        os.makedirs(os.path.join(JSON_FOLDER))
    filename = os.path.join(JSON_FOLDER, f'{file_hash}.json')
    with open(filename, 'w') as f:
        json.dump(data, f)
    s3_object_name = f'json/{file_hash}.json'
    upload_file(filename, s3_object_name, True)
    delete_file(filename)
    return get_url(s3_object_name)

def delete_file(filename: str) -> bool:
    try:
        os.remove(filename)
        return True
    except:
        return False
