import argparse
import wer

# create a function that calls wer.string_edit_distance() on every utterance
# and accumulates the errors for the corpus. Then, report the word error rate (WER)
# and the sentence error rate (SER). The WER should include the the total errors as well as the
# separately reporting the percentage of insertions, deletions and substitutions.
# The function signature is
# num_tokens, num_errors, num_deletions, num_insertions, num_substitutions = wer.string_edit_distance(ref=reference_string, hyp=hypothesis_string)
#
def score(ref_trn=None, hyp_trn=None):
    sentence_error = 0
    num_words = 0
    word_error = 0
    sub_error = 0
    del_error = 0
    ins_error = 0

    ref_trn_tokens = {}
    hyp_trn_tokens = {}

    fh = open(ref_trn)
    for line in fh:
        ref_trn_tokens[line.split()[-1]] = line.split()[:-1]
    fh.close()

    fh = open(hyp_trn)
    for line in fh:
        hyp_trn_tokens[line.split()[-1]] = line.split()[:-1]
    fh.close()

    for key, value in ref_trn_tokens.items():
        num_tokens, num_errors, num_deletions, num_insertions, num_substitutions = wer.string_edit_distance(ref=value, hyp=hyp_trn_tokens[key])
        num_words += num_tokens
        if (num_errors != 0):
            sentence_error += 1
            word_error += num_errors
            sub_error += num_substitutions
            del_error += num_deletions
            ins_error += num_insertions

        print("id: {0:s}".format(key))
        print("Scores: N={0:d}, S={4:d}, D={2:d}, I={3:d}".format(num_tokens, num_errors, num_deletions, num_insertions, num_substitutions))
        print()

    print('---------------------------------')
    print('Sentence Error Rate:')
    print('Sum: N={0:d}, Err={1:d}'.format(len(ref_trn_tokens), sentence_error))
    print('Avg: N={0:d}, Err={1:0.2f}%'.format(len(ref_trn_tokens), 100*sentence_error/len(ref_trn_tokens)))
    print('---------------------------------')
    print('Word Error Rate:')
    print('Sum: N={0:d}, Err={1:d}, Sub={2:d}, Del={3:d}, Ins={4:d}'.format(num_words, word_error, sub_error, del_error, ins_error))
    print('Avg: N={0:d}, Err={1:0.2f}%, Sub={2:0.2f}%, Del={3:0.2f}%, Ins={4:0.2f}%'.format(num_words, 100*word_error/num_words, 100*sub_error/num_words, 100*del_error/num_words, 100*ins_error/num_words))

    return


if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Evaluate ASR results.\n"
                                                 "Computes Word Error Rate and Sentence Error Rate")
    parser.add_argument('-ht', '--hyptrn', help='Hypothesized transcripts in TRN format', required=True, default=None)
    parser.add_argument('-rt', '--reftrn', help='Reference transcripts in TRN format', required=True, default=None)
    args = parser.parse_args()

    if args.reftrn is None or args.hyptrn is None:
        RuntimeError("Must specify reference trn and hypothesis trn files.")

    score(ref_trn=args.reftrn, hyp_trn=args.hyptrn)
