import random

# CHIP STATES
CHIP_OFF = 0
CHIP_LOW = 1
CHIP_NOMINAL = 2
CHIP_HIGH = 3

CUT_IN_GAP = 0.5

# toggle an array randomly based on a variable voltage input, 
# gapped voltage cutin/disconnect to avoid feedback interference

def provision(chip_state, v, V_ULTRA_LOW, V_NOMINAL, V_MAX):
    num_chips = len(chip_state)
    
    # V intercept for parallel threshold lines on a Voltage v. chip plot
    on_intercept = V_ULTRA_LOW + CUT_IN_GAP
    off_intercept = V_ULTRA_LOW

    # slope is the same for both thresholds
    slope = num_chips / (V_NOMINAL+CUT_IN_GAP - on_intercept)
    
    off = [index for index,state in enumerate(chip_state) if state == CHIP_OFF]
    low = [index for index,state in enumerate(chip_state) if state == CHIP_LOW]
    
    if v > on_intercept:
        
        on_target = int((v-on_intercept) * slope) 
        if on_target > len(low):
            if(on_target > num_chips):
                on_target= num_chips
            delta_on = on_target - len(low)
            for i in range(delta_on):
                if len(off)>0:
                    random_index = random.choice(off)
                    chip_state[random_index] = CHIP_LOW
                    del off[off.index(random_index)]

    
    off_threshold = int((v-off_intercept) * slope)
    if off_threshold < len(low):
        if(off_threshold > num_chips):
            off_threshold = num_chips
        delta_off = len(low) - off_threshold 
        if(delta_off > 0 ):
            for i in range(delta_off):
                if len(low)>0:
                    random_index = random.choice(low)
                    print(str(random_index))
                    chip_state[random_index] = CHIP_OFF
                    del low[low.index(random_index)]

    return chip_state

