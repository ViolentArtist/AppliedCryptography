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
    buckets = []
    for i in range(key_length):
        buckets.append([])

    for i in range(len(ciphertext)):
        buckets[i % key_length].append(ciphertext[i])

    for bucket in buckets:
        chi_squared = 0

        freq_dict = {}
        for char in bucket:
            if char in freq_dict.keys():
                freq_dict[char] += 1
            else:
                freq_dict[char] = 1

        # INCOMPLETE: Here we have to calculate the chi squared value for different shift amounts for each bucket and
        # pick the lowest as the key value. So for key length of 4, we get 4 buckets. We calculate the chi squared value
        # of every character's frequency in that bucket versus the expected in the English language and sum. So within
        # one bucket, we will have different chi squared values for every possible shift amount, the lowest being the
        # (probable) actual shift amount