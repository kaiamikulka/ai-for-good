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

def all_column_dict(table): 
  for column in table:
    column_values = up_get_column(table, column)
    column_set= set(column_values)
    column_unique = sorted(column_set)
    column_ints = list(range(len(column_unique)))
    zipped = up_zip_lists(column_unique, column_ints)
    column_dict = dict(zipped)
      table = up_map_column(table, column, column_dict)

