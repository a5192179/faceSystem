male = 692
female = 633
allNum = male + female
tpr = int(0.885 * male) / male
tnr = int(0.899 * female) / female
fpr = 1 - tpr
fnr = 1 - tnr
acc = (tpr + tnr)/(tpr + tnr + fpr + fnr)
# precision = ()
# recall = 

print('acc', acc)
print('tp', tpr * male)
print('tn', tnr * female)
print('fp', fpr * male)
print('fn', fnr * female)
# print('precision', acc)
# print('recall', acc)
# print('fpr', acc)