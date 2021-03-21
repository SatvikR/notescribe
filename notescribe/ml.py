import torch.nn as nn
import torch
import random
import librosa
import numpy as np
import mido
import os

num_epochs = 10
batch_size = 1
learning_rate = 0.001

input_size = 1025
output_size = 88
# sequence_length = 28
hidden_size = 128
num_layers = 2

device = torch.device('cpu')

FRAME_SIZE = 2048
HOP_SIZE = 512
SAMPLE_RATE = 22050

class Encoder(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        super().__init__()
        
        self.num_layers = num_layers
        self.hidden_size = hidden_size

        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        # inpt -> (batch_size, seq_len, input_size) 
        
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(device)
        
        
        out, (hidden, cell) = self.lstm(x, (h0, c0))
        # out -> (batch_size, seq_len, hidden_size)
        
        return hidden, cell
class Decoder(nn.Module):
    def __init__(self, output_size, hidden_size, num_layers):
        super().__init__()
        
        self.output_size = output_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.rnn = nn.LSTM(output_size, hidden_size, num_layers, batch_first=True)
        
        self.fc_out = nn.Linear(hidden_size, output_size)
        
    def forward(self, inpt, hidden, cell):
        inpt = inpt.unsqueeze(0)
        output, (hidden, cell) = self.rnn(inpt, (hidden, cell))
        
        prediction = torch.sigmoid(self.fc_out(output.squeeze(0)))
        
        #prediction -> [batch size, output dim]
        
        return prediction, hidden, cell
    
class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder, device):
        super().__init__()
        
        self.encoder = encoder
        self.decoder = decoder
        self.device = device
        
        assert encoder.hidden_size == decoder.hidden_size, \
            "Hidden dimensions of encoder and decoder must be equal!"
        assert encoder.num_layers == decoder.num_layers, \
            "Encoder and decoder must have equal number of layers!"
        
    def forward(self, src, trg, teacher_forcing_ratio = 0.5):
        if str(type(trg)) =="<class 'bool'>":
            if trg == False:
                batch_size = src.shape[0]
                trg_len = src.shape[1] * 22
                trg_note_count = self.decoder.output_size

                #store decoder outputs
                outputs = torch.zeros(trg_len, batch_size, trg_note_count).to(self.device)

                #last hidden state of the encoder is used as the initial hidden state of the decoder
                hidden, cell = self.encoder(src.to(self.device))
                hidden, cell = hidden.to(self.device), cell.to(self.device)
                #first input to the decoder is zerozerozero and soo ooonnnn
                inpt = torch.zeros(batch_size, trg_note_count)

                for t in range(1, trg_len):
                    output, hidden, cell = self.decoder(inpt.to(self.device), hidden, cell)

                    #place predictions in a tensor holding predictions for each token
                    outputs[t] = output
                    
                    inpt = output

                return outputs
        
        batch_size = trg.shape[0]
        trg_len = trg.shape[1]
        trg_note_count = self.decoder.output_size
        
        #store decoder outputs
        outputs = torch.zeros(trg_len, batch_size, trg_note_count).to(self.device)
        
        #last hidden state of the encoder is used as the initial hidden state of the decoder
        hidden, cell = self.encoder(src.to(self.device))
        hidden, cell = hidden.to(self.device), cell.to(self.device)
        #first input to the decoder is zerozerozero and soo ooonnnn
        inpt = torch.zeros(batch_size, trg_note_count)
        
        for t in range(1, trg_len):
            output, hidden, cell = self.decoder(inpt.to(self.device), hidden, cell)
            
            #place predictions in a tensor holding predictions for each token
            outputs[t] = output
            
            #decide if we are going to use teacher forcing or not
            teacher_force = random.random() < teacher_forcing_ratio
            
            #if teacher forcing, use actual next token as next input
            #if not, use predicted token
            inpt = trg[:, t, :] if teacher_force else output
        
        return outputs

encoder = Encoder(input_size, hidden_size, num_layers).to(device)
decoder = Decoder(output_size, hidden_size, num_layers).to(device)
model = Seq2Seq(encoder, decoder, device)

def wavfile2spec(wavfile):
    wavRaw, sample_rate = librosa.load(wavfile)
    wavSpec = librosa.stft(wavRaw, n_fft=FRAME_SIZE, hop_length=HOP_SIZE)
    wavSpec = np.abs(wavSpec) ** 2
    wavSpec = librosa.power_to_db(wavSpec)
    return torch.from_numpy(wavSpec)

model_load = torch.load(os.path.join('model', 'notescribe.pt'), map_location=device)
# print(model_load.items())
for k, v in model_load.items():
    print(k, v)
# model_load.eval()
# print(model_load)
model = model.load_state_dict(model_load)
print('MODEL: ', model, 'TYPE: ', type(model))
model.eval()


def wavfile2midifile(wavfile, out_path):
    wavSpec = wavfile2spec(wavfile).transpose(0, 1).unsqueeze(0)
    midiData = torch.round(model(wavSpec, False).squeeze()).int()
    midi = tnsr2mid(midiData)
    midi.save(out_path)

def tnsr2mid(tnsr, tempo=500000):
    ary = tnsr.cpu().detach().numpy()
    # get the difference
    new_ary = np.concatenate([np.array([[0] * 88]), np.array(ary)], axis=0)
    changes = new_ary[1:] - new_ary[:-1]
    # create a midi file with an empty track
    mid_new = mido.MidiFile()
    track = mido.MidiTrack()
    mid_new.tracks.append(track)
    track.append(mido.MetaMessage('set_tempo', tempo=tempo, time=0))
    # add difference in the empty track
    last_time = 0
    for ch in changes:
        if set(ch) == {0}:  # no change
            last_time += 1
        else:
            on_notes = np.where(ch > 0)[0]
            on_notes_vol = ch[on_notes]
            off_notes = np.where(ch < 0)[0]
            first_ = True
            for n, v in zip(on_notes, on_notes_vol):
                new_time = last_time if first_ else 0
                track.append(mido.Message('note_on', note=n + 21, velocity=v, time=new_time))
                first_ = False
            for n in off_notes:
                new_time = last_time if first_ else 0
                track.append(mido.Message('note_off', note=n + 21, velocity=0, time=new_time))
                first_ = False
            last_time = 0
    return mid_new