import os
import pandas as pd
import numpy as np
import sys

# 1. Higher square footage increases home sale price<sup>1, 2</sup>
# 2. Having a porch increases home sale price<sup>3, 4</sup>
# 3. Having a beachfront or lakefront increases home sale price<sup>5</sup>
# 4. The house filling a higher proportion of the overall lot decreases home sale price<sup>6</sup>
# 5. The cost per square foot is lower in duplexes than in single-family homes<sup>7</sup>
# 6. The presence of a nuisance (power lines, traffic noise, airport noise) decreases home sale price<sup>1, 5</sup>

def build_lr(df):

    print(df.shape)

    return True