import logging
import os
import pprint

from gensim.matutils import Sparse2Corpus
from gensim.models import LsiModel
from gensim.similarities import MatrixSimilarity, SparseMatrixSimilarity

from lab5.access_functions import getTfIdfModel
from lab5.compare import noteTestId

logger = logging.getLogger(__name__)


def getLsiModel(tfidfModel) -> LsiModel:
    modelPath = os.path.join('.cache', 'lsi.gensim_model')
    try:
        lsiModel = LsiModel.load(modelPath)
    except FileNotFoundError:
        corpus = Sparse2Corpus(tfidfModel.vectors, documents_columns=False)
        lsiModel = LsiModel(corpus, num_topics=200)
        lsiModel.save(modelPath)

    return lsiModel


def getTestCorpus(tfidfModel):
    testSparseVector = tfidfModel.vectors.tocsr()[noteTestId]
    testCorpus = Sparse2Corpus(testSparseVector, documents_columns=False)
    return testCorpus


def getMatrixSimilarity(tfidfModel, lsiModel=None) -> SparseMatrixSimilarity:
    similarityPath = os.path.join('.cache', 'sim_mat.gensim_sim')
    try:
        sim = MatrixSimilarity.load(similarityPath)
    except FileNotFoundError:
        corpus = Sparse2Corpus(tfidfModel.vectors, documents_columns=False)
        if lsiModel is None:
            lsiModel = getLsiModel(tfidfModel)
        sim = SparseMatrixSimilarity(
            lsiModel[corpus], num_best=10,
            num_features=tfidfModel.vectors.shape[0])
        sim.save(similarityPath)
    return sim


def main():
    tfidfModel = getTfIdfModel()
    lsiModel = getLsiModel(tfidfModel)
    index = getMatrixSimilarity(tfidfModel, lsiModel)
    testCorpus = getTestCorpus(tfidfModel)
    testVector = lsiModel[testCorpus]
    sim = index[testVector]
    logger.info(pprint.pformat(sim))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.INFO)
    main()
