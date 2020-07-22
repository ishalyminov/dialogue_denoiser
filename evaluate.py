from argparse import ArgumentParser
import os
import sys

import tensorflow as tf

THIS_FILE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(THIS_FILE_DIR,
                        'deep_disfluency',
                        'deep_disfluency',
                        'data',
                        'disfluency_detection',
                        'switchboard')
sys.path.append(os.path.join(THIS_FILE_DIR, 'deep_disfluency'))
DEFAULT_HELDOUT_DATASET = DATA_DIR + '/swbd_disf_heldout_data_timings.csv'

from dialogue_denoiser_lstm import load, eval_deep_disfluency, eval_babi


def configure_argument_parser():
    parser = ArgumentParser(description='Evaluate the LSTM dialogue filter')
    parser.add_argument('model_folder')
    parser.add_argument('dataset')
    parser.add_argument('mode', help='[deep_disfluency/babi]')

    return parser


def main(in_dataset_file, in_model_folder, in_mode):
    with tf.Session() as sess:
        model, actual_config, vocab, char_vocab, label_vocab = load(in_model_folder, sess)
        rev_vocab = {word_id: word
                     for word, word_id in vocab.iteritems()} 
        rev_label_vocab = {label_id: label
                           for label, label_id in label_vocab.iteritems()}
        if in_mode == 'deep_disfluency':
            eval_result = eval_deep_disfluency(model,
                                               [(vocab, label_vocab, rev_label_vocab), (vocab, vocab, rev_vocab)],
                                               in_dataset_file,
                                               actual_config,
                                               sess)
        elif in_mode == 'babi':
            eval_result = eval_babi(model,
                                    [(vocab, label_vocab, rev_label_vocab), (vocab, vocab, rev_vocab)],
                                    in_dataset_file,
                                    actual_config,
                                    sess)
        else:
            raise NotImplementedError
        for key, value in eval_result.iteritems():
            print '{}:\t{}'.format(key, value)


if __name__ == '__main__':
    parser = configure_argument_parser()
    args = parser.parse_args()

    main(args.dataset, args.model_folder, args.mode)
