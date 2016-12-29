#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Sample code to generate caption using beam search
'''
import sys
import json
import os
# comment out the below if you want to do type check. Remeber this have to be done BEFORE import chainer
# os.environ["CHAINER_TYPE_CHECK"] = "0"
import chainer 

import argparse
import numpy as np
import math
from chainer import cuda
import chainer.functions as F
from chainer import cuda, Function, FunctionSet, gradient_check, Variable, optimizers
from chainer import serializers

from CaptionGenerator import CaptionGenerator

#Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-g", "--gpu",default=-1, type=int, help=u"GPU ID.CPU is -1")
parser.add_argument('--vocab',default='../data/MSCOCO/mscoco_caption_train2014_processed_dic.json', type=str,help='path to the vocaburary json')
parser.add_argument('--dir',default='../data/MSCOCO/val2014_ResNet50_features/', type=str,help='path to the image directory')
parser.add_argument('--cnn-model', type=str, default='../data/ResNet50.model',help='place of the ResNet model')
parser.add_argument('--rnn-model', type=str, default='../data/caption_model_en.model',help='place of the caption model')
parser.add_argument('--beam',default=3, type=int,help='beam size in beam search')
parser.add_argument('--depth',default=50, type=int,help='depth limit in beam search')
parser.add_argument('--output',default="../data/MSCOCO/val2014_predected_captions.json", type=str,help='output file name')
parser.add_argument('--lang',default="<sos>", type=str,help='special word to indicate the langauge or just <sos>')
args = parser.parse_args()

caption_generator=CaptionGenerator(
    rnn_model_place=args.rnn_model,
    cnn_model_place=args.cnn_model,
    dictonary_place=args.vocab,
    beamsize=args.beam,
    depth_limit=args.depth,
    gpu_id=args.gpu,
    first_word= args.lang,
    )

output_annotations={}
for i,fname in enumerate(os.listdir(args.dir)):
    print i,fname
    if fname[-4:] == '.npz':
        image_feature=np.load(args.dir+"/"+fname)['arr_0'].reshape(1,2048)
        captions=caption_generator.generate_from_img_feature(image_feature)
    else:
        captions=caption_generator.generate(args.dir+"/"+fname)
    output_annotations[fname] = captions

with open(args.output, 'w') as f:
    json.dump(output_annotations, f, sort_keys=True, indent=4)
