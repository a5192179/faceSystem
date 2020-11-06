import numpy as np
import math

# distance similarity
def distance(embeddings1, embeddings2, distance_metric=0):
    if distance_metric == 0:
        # Euclidian distance
        diff = np.subtract(embeddings1, embeddings2)
        dist = np.sqrt(np.sum(np.square(diff)))
    elif distance_metric == 1:
        # Distance based on cosine similarity
        dot = np.dot(embeddings1, embeddings2)
        norm = np.linalg.norm(embeddings1) * np.linalg.norm(embeddings2)
        similarity = dot / norm
        dist = np.arccos(similarity) / math.pi
    elif distance_metric == 2:
        dist = np.linalg.norm(embeddings1 - embeddings2)
    else:
        raise 'Undefined distance metric %d' % distance_metric
    return dist