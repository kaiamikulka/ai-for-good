def test_load():
  return 'loaded'

def compute_probs(neg,pos):
  p0 = neg/(neg+pos)
  p1 = pos/(neg+pos)
  return [p0,p1]


def cond_prob (table, e, e_val, t, t_val):
  t_subset = up_table_subset(table, t, 'equals', t_val) 
  e_list = up_get_column(t_subset, e)  
  p_b_a = sum([1 if v==e_val else 0 for v in e_list])/len(e_list) 
  return p_b_a + 0.01

def cond_probs_product(table, e_val, t, t_val):
  table_columns = up_list_column_names(table)  #new puddles function
  evidence_columns = table_columns[:-1]
  evidence_complete = up_zip_lists(evidence_columns, e_val)
  cond_prob_list = []
  for evidence_column, evidence_val in evidence_complete:
    cond_prob_value = cond_prob(table, evidence_column, evidence_val, t, t_val)
    cond_prob_list += [cond_prob_value]
  partial_numerator = up_product(cond_prob_list)  #new puddles function
  return partial_numerator

def prior_prob(table, t, t_val):
 t_list = up_get_column(table, t)
 p_a = sum([1 if v==t_val else 0 for v in t_list])/len(t_list) 
 return p_a


def naive_bayes(table, evidence_row, target):
  x = cond_probs_product(table, evidence_row, target, 0)
  y = prior_prob(table, target, 0)
  no = x * y
  x = cond_probs_product(table, evidence_row, target, 1)
  y = prior_prob(table, target, 1)
  yes = x * y
  neg, pos = compute_probs(no, yes)
  return [neg, pos]

def metrics(list):
  tn = sum([1 if pair==[0,0] else 0 for pair in list])
  tp = sum([1 if pair==[1,1] else 0 for pair in list])
  fp = sum([1 if pair==[1,0] else 0 for pair in list])
  fn = sum([1 if pair==[0,1] else 0 for pair in list])
  precision = tp/(tp+fp) if tp+fp > 0 else 0
  recall = tp/(tp+fn) if tp+fn > 0 else 0
  f1 = 2*(precision*recall)/(precision+recall) if precision+recall > 0 else 0
  accuracy = sum([p==a for p,a in list])/len(list)
  return {'Precision': precision, 'Recall': recall, 'F1': f1, 'Accuracy': accuracy}

def run_random_forest(train, test, target, n):
  X = up_drop_column(train, target)
  y = up_get_column(train, target)  
  k_feature_table = up_drop_column(test, target) 
  k_actuals = up_get_column(test, target)  
  clf = RandomForestClassifier(n_estimators=11, max_depth=2, random_state=0)  
  clf.fit(X, y)  #builds the trees as specified above
  probs = clf.predict_proba(k_feature_table)
  pos_probs = [p for n,p in probs]  #probs is list of [neg,pos] like we are used to seeing.
  pos_probs[:5]
  all_mets = []
  for t in thresholds:
    all_predictions = [1 if pos>t else 0 for pos in pos_probs]
    pred_act_list = up_zip_lists(all_predictions, k_actuals)
    mets = metrics(pred_act_list)
    mets['Threshold'] = t
    all_mets = all_mets + [mets]
  all_mets[:2]
  metrics_table = up_metrics_table(all_mets)
  metrics_table
  #your code below
  print(metrics_table)  #output we really want - to see the table
  return None


