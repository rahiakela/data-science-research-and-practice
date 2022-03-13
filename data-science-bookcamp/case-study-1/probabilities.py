from itertools import product
from collections import defaultdict


sample_space = {"heads", "tails"}
weighted_sample_space = {"heads": 4, "tails": 1}

possible_children = ["boy", "girl"]
sample_space_efficient = set(product(possible_children, repeat=4))

possible_rolls = list(range(1, 7))
roll_sample_space = set(product(possible_rolls, repeat=6))


def is_heads_or_tails(outcome):
  return outcome in sample_space
  
def is_neither(outcome):
  return not is_heads_or_tails(outcome)
  
def is_heads(outcome):
  return outcome == "heads"

def is_tails(outcome):
  return outcome == "tails"
  
def get_matching_event(event_condition, sample_space):
  return set([outcome for outcome in sample_space if event_condition(outcome)])
  
def compute_probability(event_condition, generic_sample_space):
  # The compute_probability function extracts the event associated with an inputted event condition to compute its probability
  event = get_matching_event(event_condition, generic_sample_space)
  return len(event) / len(generic_sample_space)  # Probability is equal to event size divided by sample space size
  
def compute_event_probability(event_condition, generic_sample_space):
  event = get_matching_event(event_condition, generic_sample_space)

  # Checks whether generic_event_space is a set
  if type(generic_sample_space) == type(set()):
    return len(event) / len(generic_sample_space)

  event_size = sum(generic_sample_space[outcome] for outcome in event)
  return event_size / sum(generic_sample_space.values())
  

def has_two_boys(outcome):
  return len([child for child in outcome if child == "boy"]) == 2
  
def has_sum_of_21(outcome):
  return sum(outcome) == 21
  

def is_in_interval(number, min, max):
  # In open intervals, at least one of the boundaries is excluded
  return min <= number <= max
  
def generate_coin_sample_space(num_flips=10):
  weighted_sample_space = defaultdict(int)
  for coin_flips in product(["heads", "tails"], repeat=num_flips):
    # Number of heads in a unique sequence of num_flips coin flips
    heads_count = len([outcome for outcome in coin_flips if outcome == "heads"])
    weighted_sample_space[heads_count] += 1
  return weighted_sample_space
