import nltk
import re
import sys
import argparse

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

import numpy as np

nltk.download('punkt_tab',quiet=True)
nltk.download('stopwords', quiet=True)

def tokenize_words(text):
    return re.findall(r"\b\w+(?:'\w+)?\b|[.,!?;:]", text)

def clean_for_tfidf(text):
    """
    All to lowercase, strip non alphabets, remove stopwords
    """
    stop = set(stopwords.words('english')) # Assuming language is english
    words =  word_tokenize(text.lower())

    return ' '.join([w for w in words if w.isalpha() and w not in stop])

def tfidf_scores(sentences):
    cleaned =  [clean_for_tfidf(s) for s in sentences]

    try:
        matrix = TfidfVectorizer().fit_transform(cleaned)
        return np.array(matrix.mean(axis=1)).flatten().tolist()
    except Exception:
        return [1.0] * len(sentences)
    
def summarize(text:str, n=3):
    """
    Summarizes text by extracting top sentences.
    Returns dict with summary and stats
    """
    text = text.strip()
    if not text:
        raise ValueError("No text provided.")
    if len(text.split()) < 20:
        raise ValueError("Text too short. atleast a paragraph is required")
    
    sentences =  sent_tokenize(text)

    if len(sentences) <= n:
        selected_idx = list(range(len(sentences)))
        scores = [1.0] * len(sentences)

    else:
        scores =  tfidf_scores(sentences)

        for i in range(len(scores)):
            if i == 0:
                scores[i] *= 1.5
            elif i < len(sentences) * 0.2:
                scores[i]  *= 1.2

        selected_idx = sorted(sorted(range(len(scores)), key=lambda i:scores[i],reverse=True)[:n])

    summary = " ".join(sentences[i] for i in selected_idx)

    orig_tokens =  tokenize_words(text)
    sum_tokens =  tokenize_words(summary)
    orig_count =  len(orig_tokens)
    sum_count = len(sum_tokens)
    dropped = orig_count - sum_count
    kept_pct = round(sum_count / orig_count * 100,1) if orig_count else 0

    stats = {
        "original_tokens": orig_count,
        "summary_tokens": sum_count,
        "tokens_removed": dropped,
        "kept_pct": kept_pct,
        "removed_pct": round(100 - kept_pct,1),
        "compression_ratio": round(orig_count / sum_count, 2) if sum_count else 0,
    }  

    return {
        "summary": summary,
        "stats" : stats,
    }


# --------------------------- CLI --------------------------------

def print_stats(result):
    s =  result['stats']
    print('\n'+ "-" * 44)
    print(f"  Original tokens  : {s['original_tokens']}")
    print(f"  Summary tokens   : {s['summary_tokens']}  ({s['kept_pct']}% of original)")
    print(f"  Tokens removed   : {s['tokens_removed']}  ({s['removed_pct']}%)")
    print(f"  Compression ratio: {s['compression_ratio']}x")
    print("─" * 44)

    print("\nSummary:\n")
    for line in result["summary"].split(". "):
        print(f"  {line.strip()}.")
    print()

def cli():
    parser =  argparse.ArgumentParser(
        description="Extractive text summarizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
    examples:
    python summarizer.py article.txt
    python summarizer.py article.txt --senteces 5
    cat artcile.txt | python summarizer.py -
    """
    )

    parser.add_argument(
        "file",
        nargs="?",
        help = "path to a .txt file, or '-' to read from stdin"
    )

    parser.add_argument(
        "--sentences", "-n",
        type=int, default=3,
        metavar="N",
        help = "number of senteces in summary (default : 3)" 
    ) 

    parser.add_argument(
        "--stats",
        action = "store_true",
        help = "print token stats"
    )

    args = parser.parse_args()

    if args.file is None or args.file == '-':
        print("paste your text below, then press ctrl+D or (ctrl+Z on Windows):\n")
    else:
        try:
            with open(args.file, encoding='utf-8', errors="ignore") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: file '{args.file}' not found.", file=sys.stderr)
            sys.exit(1)

        try:
            result =  summarize(text, n=args.sentences)
        except ValueError as e:
            print(f"Error: {e}",file = sys.stderr)
            sys.exit(1)

        if args.stats:
            print_stats(result)
        else:
            print("\n" + result["summary"] + "\n")

if __name__ == '__main__':
    cli()