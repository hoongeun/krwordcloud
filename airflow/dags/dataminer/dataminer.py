from krwordrank.word import KRWordRank
import krwordrank


def wordrank(textdir: str):
    def get_texts_scores(fname: str):
        with open(fname, encoding='utf-8') as f:
            docs = [doc.lower().replace('\n', '').split('\t') for doc in f]
            docs = [doc for doc in docs if len(doc) == 2]

            if not docs:
                return [], []

            texts, scores = zip(*docs)
            return list(texts), list(scores)

    # La La Land
    fname = '../data/134963.txt'
    texts, scores = get_texts_scores(fname)

    wordrank_extractor = KRWordRank(
        min_count=5,  # 단어의 최소 출현 빈도수 (그래프 생성 시)
        max_length=10,  # 단어의 최대 길이
        verbose=True
    )

    beta = 0.85    # PageRank의 decaying factor beta
    max_iter = 10

    keywords, rank, graph = wordrank_extractor.extract(texts, beta, max_iter)

    for word, r in sorted(keywords.items(), key=lambda x: -x[1])[:30]:
        print('%8s:\t%.4f' % (word, r))

    sortkeywords = sorted(keywords.items(), key=lambda x: -x[1])[:300]

    return {word: score filter(filterfn, sortkeywords)}
