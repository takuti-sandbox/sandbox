import numpy as np
from sklearn.metrics import roc_auc_score


def my_auc(pred, label):
    n = len(pred)

    a = 0.
    score_prev = float('-inf')
    fp = tp = 0
    fp_prev = tp_prev = 0

    for i in range(n):
        if pred[i] != score_prev:
            a += trapezoid(fp, fp_prev, tp, tp_prev)
            score_prev = pred[i]
            fp_prev = fp
            tp_prev = tp

        if label[i] == 1:
            tp += 1
        else:
            fp += 1

    return a, fp, tp, fp_prev, tp_prev


def trapezoid(x1, x2, y1, y2):
    base = abs(x1 - x2)
    height = (y1 + y2) / 2.
    return base * height


def single(pred, label):
    """
    >>> abs(single([.8, .7, .5, .3, .2], [1, 1, 0, 1, 0]) - roc_auc_score([1, 1, 0, 1, 0], [.8, .7, .5, .3, .2])) < 1e-4
    True
    >>> abs(single([.2, .7, .3, .5, .8], [0, 1, 1, 0, 1]) - roc_auc_score([0, 1, 1, 0, 1], [.2, .7, .3, .5, .8])) < 1e-4
    True
    """
    sorted_indices = np.argsort(pred)[::-1]
    pred = np.array(pred)[sorted_indices]
    label = np.array(label)[sorted_indices]

    a, fp, tp, fp_prev, tp_prev = my_auc(pred, label)

    # get()
    a += trapezoid(fp, fp_prev, tp, tp_prev)
    return a / (tp * fp)


def multi(pred, label, sep=2):
    """
    >>> multi([.8, .7, .5, .3, .2], [1, 1, 0, 1, 0], sep=0)
    0.8333333333333334
    >>> multi([.8, .7, .5, .3, .2], [1, 1, 0, 1, 0], sep=1)
    0.8333333333333334
    >>> multi([.8, .7, .5, .3, .2], [1, 1, 0, 1, 0], sep=2)
    0.8333333333333334
    >>> multi([.8, .7, .5, .3, .2], [1, 1, 0, 1, 0], sep=3)
    0.8333333333333334
    >>> multi([.8, .7, .5, .3, .2], [1, 1, 0, 1, 0], sep=4)
    0.8333333333333334
    """
    sorted_indices = np.argsort(pred)[::-1]
    pred = np.array(pred)[sorted_indices]
    label = np.array(label)[sorted_indices]

    a1, fp1, tp1, fp_prev1, tp_prev1 = my_auc(pred[:sep], label[:sep])
    a2, fp2, tp2, fp_prev2, tp_prev2 = my_auc(pred[sep:], label[sep:])

    a1 += trapezoid(fp1, fp_prev1, tp1, tp_prev1)
    a2 += trapezoid(fp2, fp_prev2, tp2, tp_prev2)

    # merge()
    a = (a1 + a2) + trapezoid(fp1 + fp2, fp1, tp1, tp1)

    fp = fp1 + fp2
    tp = tp1 + tp2

    fp_prev = fp1 + fp_prev2
    tp_prev = tp1 + tp_prev2

    a -= trapezoid(fp, fp_prev, tp, tp_prev)

    # get()
    a += trapezoid(fp, fp_prev, tp, tp_prev)
    return a / (tp * fp)


def sklearn_auc():
    n = 100

    labels = np.random.choice([0, 1], n)
    scores = np.random.choice([.1, .2, .3, .4, .5, .6, .7, .8, .9], n)

    print(roc_auc_score(labels, scores))

    for l, s in sorted(zip(labels, scores), key=lambda x: x[-1], reverse=True):
        print('%d,%.1f' % (l, s))


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    sklearn_auc()
