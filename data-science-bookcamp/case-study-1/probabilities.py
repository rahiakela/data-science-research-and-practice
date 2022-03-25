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

def frequency_heads(coin_flip_sequence):
  total_heads = len([head for head in coin_flip_sequence if head == 1])
  return total_heads / len(coin_flip_sequence)
  
# Getting a bin’s frequency and size
def output_bin_coverage(i):
  # A bin at position i contains counts[i] frequencies
  count = int(counts[i])  
  # A bin at position i covers a frequency range of bin_edges[i] through bin_edges[i+1]
  range_start, range_end = bin_edges[i], bin_edges[i + 1]
  range_string = f"{range_start} - {range_end}"
  print(f"The bin for frequency range {range_string} contains {count} element{'' if count == 1 else 's'}")
  
# Computing a high confidence interval
def compute_high_confidence_interval(likelihoods, bin_width):
  peak_index = likelihoods.argmax()
  area = likelihoods[peak_index] * bin_width
  start_index, end_index = peak_index, peak_index + 1

  while area < 0.95:
    if start_index > 0:
      start_index -= 1
    if end_index < likelihoods.size - 1:
      end_index += 1
    area = likelihoods[start_index: end_index + 1].sum() * bin_width

  range_start, range_end = bin_edges[start_index], bin_edges[end_index]
  range_string = f"{range_start:.6f} - {range_end:.6f}"
  print(f"The frequency range {range_string} represents a {100 * area:.2f}% confidence interval")

  return start_index, end_index