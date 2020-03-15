# Joon Hwang
def prep_trials(ciphertext):
    # for key length t{1-24}
    trials = []
    for i in range(1, 25):
        trial_t = []
        for i2 in range(i):
            trial_t.append([])
        trials.append(trial_t)

    for i in range(len(ciphertext)):
        for i2 in range(len(trials)):
            t = i2 + 1
            trials[i2][i % t].append(ciphertext[i])

    return trials


# Joon Hwang
def index_of_coincidence_analysis(ciphertext):
    trials = prep_trials(ciphertext)
    iocs = []
    for i in range(len(trials)):
        # within each group per key length t, calculate the index of coincidence
        # average the indices of coincidence across groups per key length t
        t = i + 1
        ioc_sum = 0
        for bucket in trials[i]:
            freq_dict = {}
            for char in bucket:
                if char in freq_dict.keys():
                    freq_dict[char] += 1
                else:
                    freq_dict[char] = 1

            ioc = 0
            N = len(bucket)
            for char in freq_dict:
                ioc += (freq_dict[char] * (freq_dict[char] - 1)) / (N * (N - 1))
            ioc_sum += ioc
        ioc_average = ioc_sum / t
        iocs.append((ioc_average, t))
    print(iocs)


# Joon Hwang
def chi_squared_analysis(ciphertext, key_length):
    english_percents = {'a': 0.0855, 'b': 0.0160, 'c': 0.0316, 'd': 0.0387, 'e': 0.1210, 'f': 0.0218, 'g': 0.0209,
                    'h': 0.0496, 'i': 0.0733, 'j': 0.0022, 'k': 0.0081, 'l': 0.0421, 'm': 0.0253, 'n': 0.0717,
                    'o': 0.0747, 'p': 0.0207, 'q': 0.0010, 'r': 0.0633, 's': 0.0673, 't': 0.0894, 'u': 0.0268,
                    'v': 0.0106, 'w': 0.0183, 'x': 0.0019, 'y': 0.0172, 'z': 0.0011}
    buckets = []
    for i in range(key_length):
        buckets.append([])

    for i in range(len(ciphertext)):
        buckets[i % key_length].append(ciphertext[i])

    for bucket in buckets:
        shift_buffer = bucket
        for i in range(1, 26):
            freq_dict = {}
            chi_squared = 0
            # shift shift_buffer by i
            for char in shift_buffer:
                if char in freq_dict.keys():
                    freq_dict[char] += 1
                else:
                    freq_dict[char] = 1

            for char in freq_dict.keys():
                char_chi_squared = ((freq_dict[char] - english_percents[char] * len(bucket)) ** 2) / \
                                   (english_percents[char] * len(bucket))
                chi_squared += char_chi_squared
            print("chi squared value for shift of ", i, ": ", chi_squared)