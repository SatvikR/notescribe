<p align="center">
  <img src="https://github.com/SatvikR/notescribe/blob/dev/.github/images/logo.png?raw=true" />
</p>
<p align="center">
  <strong>Open source music transcriber made for DVHacks |||</strong>
</p>

## Contributors

- [Satvik Reddy](https://github.com/SatvikR)
- [Niels Voss](https://github.com/osbourn)
- [Soham Patil](https://github.com/soham1053)

## Run Locally

```sh
python3 -m notescribe
```

## Used Services and Libraries

| Library/Service                                                                        | Usage                               |
| -------------------------------------------------------------------------------------- | ----------------------------------- |
| [Pytorch](https://pytorch.org)                                                         | Provides user with web pages        |
| [Pydub](https://pydub.com)                                                             | Machine learning models             |
| [LilyPond](https://lilypond.org)                                                       | Rendering midi as images            |
| [FPDF for Python](https://pyfpdf.readthedocs.io)                                       | Packaging images as PDF             |
| [AWS S3](https://aws.amazon.com/s3) and [boto3](https://aws.amazon.com/sdk-for-python) | Asset storage and upload management |
| [Docker](https://www.docker.com)                                                       | Deployment configuration            |
| [AWS EC2](https://aws.amazon.com/ec2)                                                  | Website hosting                     |

## How it works

The user uploads a file to to a website. That file is processed and converted to
WAV format. The newly created WAV file is processed by a machine learning
algorithm, which generates a MIDI file.

The MIDI file is then converted to the intermediate LilyPond (.ly) format using
[midi2ly](https://lilypond.org/doc/v2.18/Documentation/usage/invoking-midi2ly.en.html),
and is then rendered as collection of images.

These images are packaged into a PDF document using FPDF. The PDF document, MIDI
file, and generated images are stored in AWS S3 and their URLs are recorded in a
json file. That json file is also uploaded to S3.

The user is sent back a URL that points ot the json file in S3, and client side
JavaScript renders the images and provides links to download the PDF and MIDI.

## License

Notescribe is licensed under the [Apache License, Version
2.0.](https://www.apache.org/licenses/LICENSE-2.0.html) See [LICENSE](LICENSE)
for more details.
