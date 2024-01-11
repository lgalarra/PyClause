import c_clause
from c_clause import QAHandler, Loader
import numpy as np
from clause.config.options import Options
from clause.util.utils import get_base_dir


train = f"{get_base_dir()}/data/wnrr/train.txt"
filter = f"{get_base_dir()}/data/wnrr/valid.txt"
target = f"{get_base_dir()}/data/wnrr/test.txt"

rules = f"{get_base_dir()}/data/wnrr/anyburl-rules-c5-3600"


options = Options()

loader = Loader(options.get("loader"))
loader.load_data(train, filter)
loader.load_rules(rules)


options.set("qa_handler.collect_rules", True)
qa_handler = QAHandler(options=options.get("qa_handler"))



## string inputs mode
## input queries:
## list of tuples with 2 strings (or list of list)
## the first element of the tuple is the source entity the second element is the relation
queries = [("12184337","_hypernym"), ("12184337","_verb_group")]

## input args: queries (see above), string: "head" or "tail" the query type
## head: the query rel(?, sourceEnt) will be answered
## tail: the query rel(sourceEnt, ?) will be answered
##
## output: list[list[tuple[string,float]]] 
## e.g. output[0] contains a list with the answers for the first query
## note that output[i] does not have same length as output[k] as different queries have different amounts of answers
qa_handler.calculate_answers(queries=queries, loader=loader, direction="tail")
as_string = True
answers = qa_handler.get_answers(as_string=as_string)
rules = qa_handler.get_rules(as_string=False)
print(answers)
print(rules)


### idx input mode
### input: queries, string
### queries list of tuples with two integer, the integer are the idx's 
### or Nx2 np.array where N is the number of queries, first column are source entity ids second are relation ids
### output: the output remains a list[list[tuple[int,float]]] as different queries have different amounts of answers
### each set i of answers can be converted to np.array with np.array(output[i])
queries = np.array([(4,5), (0,1)])

# answers to first query

qa_handler.calculate_answers(queries, loader, "tail")
answers = qa_handler.get_answers(not as_string)
answer_set = np.array(answers[0], dtype=object)
# print idx answers
print(answer_set[:,0])
# print confidences
print(answer_set[:,1])

