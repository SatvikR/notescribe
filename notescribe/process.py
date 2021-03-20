from notescribe import settings, UPLOAD_FOLDER, MIDI_FOLDER, LILYPOND_FOLDER, IMAGES_FOLDER
from notescribe.s3_upload import upload_file, get_url
import subprocess
import os.path
import os
import hashlib
from typing import List

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
    image_folder = generate_images(file_hash, lilypond_filename)
    print(f'image_folder: {image_folder}')
    image_urls = process_images(image_folder)
    print(f'image_urls: {image_urls}')
    delete_file_success = delete_file(os.path.join(UPLOAD_FOLDER, upload_filename))
    print('upload deleted' if delete_file_success else 'upload failed to be deleted')

    return False

def convert_to_midi(file_hash: str, upload_filename: str) -> str:
    '''
    Converts a user uploaded file to midi.
    :param file_hash: SHA-1 hash of the user uploaded file
    :param upload_filename: Filename (excluding path) of the uploaded file to convert
    :returns: Filename (excluding path) of the newly created midi file
    '''
    # TODO: Call machine learning code
    print(f'Converting file {upload_filename} with hash {file_hash}')

    # Return example midi file
    return 'midi_123456789abcdefexample.mid'

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
    print(lilypond_path)
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    subprocess.run([lilypond_path, '-fpng', '-o', output_dir, os.path.join(LILYPOND_FOLDER, lilypond_filename)])

    # Remove extra copy of midi file that lilypond generates automatically
    assert delete_file(os.path.join(output_dir, lilypond_filename[:-3] + '.mid'))

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
        upload_file(path_to_image, s3_object_name)
        delete_file(path_to_image)
        image_urls.append(get_url(s3_object_name))
    os.rmdir(image_directory_path)
    return image_urls

def delete_file(filename: str) -> bool:
    try:
        os.remove(filename)
        return True
    except:
        return False
