from functools import cache
import pdb

class InvalidTransitionProbabilities(Exception):
  """Raised when transition probabilities from a state don't sum to 1"""
  pass

## Transition probabilities from survival state

@cache
def extinction_given_survival(k):

  """I expect this to decrease slightly with the value of k, given civilisations in the state have
  evidently survived to reach perils."""
  base_estimate = 0.0003 # I've just lifted this from one of Rodriguez's most pessimistic scenarios
  # in this post: https://forum.effectivealtruism.org/posts/GsjmufaebreiaivF7/what-is-the-likelihood-that-civilizational-collapse-would
  # I don't think the first two scenarios really describe a state of 'survival' for much the reasons
  # she describes. It could be much higher, given model uncertainty or its sensitivity to
  # lower numbers of surviving humans or much lower if we define the survival state more broadly
  expected_number_of_previous_survivals = (k - 1) * 0.01 # Again, just intuition of what proportion
                                                         # of milestone regressions took us back to
                                                         # a survival state.
  probability_multiplier_per_previous_survival = 0.995 # This is very naively reduced by slightly less
                                                       # than the expected number of previous survivals
                                                       # - the more survival states we've been through, the
                                                       # faster the probability of extinction should fall
  return (base_estimate *
          probability_multiplier_per_previous_survival ** expected_number_of_previous_survivals)

@cache
def preindustrial_given_survival(k, k1):
  if k != k1:
    # We can't transition to different civilisations from a preperils state
    return 0
  else:
    return 1 - extinction_given_survival(k)

#  TODO - decide whether to reintroduce these checksums
#  if not extinction_given_survival(k) + preindustrial_given_survival(k) == 1:
#   raise InvalidTransitionProbabilities("Transition probabilities from survival must == 1")

## Transition probabilities from preindustrial state

@cache
def extinction_given_preindustrial(k):
  """I expect this to decrease slightly with the value of k, given civilisations in the state have
  evidently survived to reach perils. Depleted resources will be a slight issue. There are various
  different suggested values in the comments below. The output of this function"""

  # Uncomment a value below to taste of expected time in years. The estimates of expected time to
  # recover come from Luisa Rodriguez's post,
  # https://forum.effectivealtruism.org/posts/Nc9fCzjBKYDaDJGiX/what-is-the-likelihood-that-civilizational-collapse-would-1
  # She now claims that she has updated towards 'technological stagnation', for which 'The biggest
  # reason is probably the risk of extreme, long-lasting climate change. It seems possible that
  # anthropogenic climate change could cause global warming extreme enough that agriculture would
  # become much more difficult than it was for early agriculturalists. Temperatures wouldn’t return to
  # current levels for hundreds of thousands of years, so if the warmer temperatures were much less
  # conducive to recovering agriculture and downstream technological developments, humanity might be
  # stagnant for millennia.' Unfortunately she doesn't further quantify this shift in estimates, but
  # hers is still the most comprehensive piece I know on the subject. So the first values are based
  # on her initial estimates (not they're in the order they appear in the post, not ascending):

  # 'If we think recovery time is limited by...'
  # 'Agricultural rev. and industrialization take as long as they did the first time'
  # expected_time_in_years = 300_000

  # 'Agricultural civilization returns quickly, industrial revolution takes as long as it did the
  # first time'
  # expected_time_in_years = 500 # Lower end of her range in this scenario
  # expected_time_in_years = 30_000 # Upper end of her range in this scenario

  # 'Inside view — If we assume that existing physical and human capital would accelerate the speed
  # of re-industrialization relative to the base rate'

  # 'Best case guess - Assumes the British industrial revolution happened about when we’d have expected'
  # expected_time_in_years = 100 # Lower end of her range in this scenario
  # expected_time_in_years = 3700 # Upper end of her range in this scenario

  # 'Pessimistic case guess - Assumes we got very lucky with the British industrial revolution'
  # expected_time_in_years = 1000 # Lower end of her range in this scenario
  # expected_time_in_years = 33_000 # Upper end of her range in this scenario

  # To account for her remarks about technological stagnation, I just naively add 10000 years to
  # each of the above:
  # expected_time_in_years = 10_100
  # expected_time_in_years = 10_500
  # expected_time_in_years = 11_000
  expected_time_in_years = 13_700
  # expected_time_in_years = 40_000
  # expected_time_in_years = 43_000
  # expected_time_in_years = 310_000

  # The below estimates of annual extinction rate come from this paper:
  # https://www.nature.com/articles/s41598-019-47540-7 - quotes from the same. Uncomment to taste.
  # Note that for narrative reasons they're in the order they appeared in that article, not ascending
  # extinction_probability_per_year = 1/14_000
  # 'Assuming a 200 thousand year (kyr) survival time, we can be exceptionally confident that rates
  # do not exceed 6.9 * 10^−5. This corresponds to an annual extinction probability below roughly 1 in 14,000.'

  # extinction_probability_per_year = 1/22_800
  # 'Extinction can be represented by the exponential distribution with constant extinction rate μ...
  # Using the fossil dated to 315ka as a starting point for humanity gives an upper bound
  # of μ < 4.4 * 10^−5, corresponding to an annual extinction probability below 1 in 22,800'

  # extinction_probability_per_year = 1/140_000
  # 'Using the emergence of Homo as our starting point pushes the initial bound back a full order of
  # magnitude, resulting in an annual extinction probability below 1 in 140,000.'

  extinction_probability_per_year = 1/87_000
  # 'We can also relax the one in million relative likelihood constraint and derive less conservative
  # upper bounds. An alternative bound would be rates with relative likelihood below 10−1 (1 in 10)
  # when compared to the baseline rate of 10−8. If we assume humanity has lasted 200kyr, we
  # obtain a bound of μ < 1.2 * 10^−5, corresponding to an annual extinction probability below 1 in 87,000.'

  # extinction_probability_per_year = 1/870_000
  # 'Using the 2Myr origin of Homo strengthens the bound by an order of magnitude in a
  # similar way and produces annual extinction probabilities below 1 in 870,000.''

  base_total_extinction_probability = 1 - ((1 - extinction_probability_per_year) ** expected_time_in_years)

  expected_number_of_previous_preindustrials = (k - 1) * 0.4
  # Thoughts behind above variable: I assume biopandemics would leave us enough technology to retain
  # industry; malevolent AI would most likely either wipe us out or be controlled by bad acting humans,
  # who would want to leave us with at least industrial technology; nuclear arsenals could eventually
  # destroy industry, but wouldn't be big enough for the first few years of a time of perils; some
  # kind of multiple catastrophe could also cause this

  multiplier_per_previous_preindustrial = 0.95 # Mostly intuition. Each iteration provides less evidence
                                               # for the probability of success than in the next than survival
                                               # since the period is much longer, and could be affected
                                               # by changing environmental factors. But we expect to
                                               # pass through many more of these states across reboots,
                                               # so we collect many more instances of this evidence.


  return (base_total_extinction_probability *
          multiplier_per_previous_preindustrial ** expected_number_of_previous_preindustrials)

@cache
def industrial_given_preindustrial(k, k1):
  if k != k1:
    # We can't transition to different civilisations from a preperils state
    return 0
  else:
    return 1 - extinction_given_preindustrial(k)

# if not extinction_given_preindustrial() + industrial_given_preindustrial() == 1:
#   raise InvalidTransitionProbabilities("Transition probabilities from preindustrial must == 1")


## Transition probabilities from industrial state

@cache
def extinction_given_industrial(k):
  """I expect this to have a complex relationship with k. Initially I think it decreases with k as
  resources are preferentially used up so each civilisation has to do more with less, but after some
  number of retries it should probably increase, as we gain evidence of our capacity to deal with
  those scarcer resources. There might also be dramatic differences in difficulty based exactly on what
  has been used up or left behind by previous civilisations, so we might want a branching function.
  Below I've used a branching function for the pessimistic case, but otherwise defaulted to the simple
  approach of assuming exponential decline
  """

  # For extinction probability per year, we can start with the base rates given in the previous
  # calculation, and then multiply them by some factor based on whether we think industry would make
  # humans more or less resilient.
  # base_annual_extinction_probability = 1/14_000
  # base_annual_extinction_probability = 1/22_800
  # base_annual_extinction_probability = 1/140_000
  base_annual_extinction_probability = 1/87_000
  # base_annual_extinction_probability = 1/870_000

  annual_extinction_probability_multiplier = 0.7 # Intuition based on the reasoning below:
  # This paper estimates that British grain output approxmately doubled between ~1760-1850, and had
  # approximately doubled over the 300 years before that:
  # https://www.researchgate.net/publication/228043115_Yields_Per_Acre_in_English_Agriculture_1250-1860_Evidence_from_Labour_Inputs
  # So if we assume losses of food are uncorrelated with each other, and the majority of the world
  # would go through a similar transition at once, that would suggest a lower bound on this multiplier
  # of ~0.25. Obviously the rest of the world was slower, though - going by these estimates of historical
  # *wheat* yield, the US took til about the 1930s to start catching up:
  # https://www.researchgate.net/figure/Wheat-Yields-1800-2004_fig1_263620307
  # https://www.agry.purdue.edu/ext/corn/news/timeless/yieldtrends.html
  # Declining resources might slow down the spread of agricultural improvements, though. Also,
  # surplus food production might not matter much for extreme events such as a supervolcano that blocked out
  # the sky for many years - although it might incentivise surplus food preservation. I suspect
  # such events constitute the majority of pre-modern extinction risk.

  # For expected time in years, we have to make some strong assumptions.

  # Pessimistic scenario
  # In this scenario, I assume all knowledge of previous civilisations' technology is either lost or
  # made useless by different resource constraints. Thus I imagine the original ~145 years for this
  # transition is stretched substantially by the decline in resource availability - most strongly so
  # from the initial lack of fossil fuels in reboot 1 and from phosphorus in subsequent reboots, then
  # somewhat more gently as rare earths etc are gradually left in unusable states.

  per_reboot_difficulty_modifier = 1.5 # How much longer/less long would it take a typical reboot than in the
  # previous one to develop modern technology given resource-depletion considerations

  if k == 1:
    expected_time_in_years = 1450
    # I mostly arbitrarily assume ten times the duration for rebooting with no oil, much less
    # coal that's more expensive to mine, and maybe 10% of the energy of our current civilisation
    # embodied in landfill:
    # https://scitechdaily.com/scientists-estimate-that-the-embodied-energy-of-waste-plastics-equates-to-12-of-u-s-industrial-energy-use/
    # Dartnell envisions what the process might look like here:
    # https://aeon.co/essays/could-we-reboot-a-modern-civilisation-without-fossil-fuels
    # He gives no probability estimates, but uses phrases like 'For a society to stand any chance of
    # industrialising under such conditions' and 'an industrial revolution without coal would be, at
    # a minimum, very difficult', suggesting he might think it's unlikely to *ever* happen.
  elif k == 2:
    expected_time_in_years = 2900
    # I imagine this disproportionately stretched again by the complete absence of coal and other easily
    # depletable resources. In particular easily phosphorus accessible rock phosphorus would be gone
    # (see discussion between John Halstead and David Denkenberger here):
    # https://forum.effectivealtruism.org/posts/rtoGkzQkAhymErh2Q/are-we-going-to-run-out-of-phosphorous
  else:
    expected_time_in_years = 2900 * per_reboot_difficulty_modifier ** (k - 2)

  # Optimistic scenario
  # In this scenario I assume the absence of fossil fuels/other resources is much less punitive
  # especially early on and enough knowledge from previous civilisations is mostly retained to actually
  # speed up this transition the first couple of times
  per_reboot_difficulty_modifier = 1.2
  expected_time_in_years = 100 * per_reboot_difficulty_modifier ** k

  return 1 - ((1 - base_annual_extinction_probability * annual_extinction_probability_multiplier) ** expected_time_in_years)

@cache
def perils_given_industrial(k, k1):
  if k != k1:
    # We can't transition to different civilisations from a preperils state
    return 0
  return 1 - extinction_given_industrial(k)

# if not extinction_given_industrial() + perils_given_industrial() == 1:
#   raise InvalidTransitionProbabilities("Transition probabilities from industrial must == 1")
